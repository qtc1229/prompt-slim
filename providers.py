"""Explicit opt-in single-turn cloud adapters. No agent proxy or automatic retries."""
import json
import os
import urllib.request
import urllib.error

PROVIDERS = {
    'openai': ('https://api.openai.com/v1/responses', 'OPENAI_API_KEY'),
    'claude': ('https://api.anthropic.com/v1/messages', 'ANTHROPIC_API_KEY'),
    'deepseek': ('https://api.deepseek.com/chat/completions', 'DEEPSEEK_API_KEY'),
}

def build_request(provider, model, text, max_output_tokens=1024):
    if provider not in PROVIDERS:
        raise ValueError('Unknown provider')
    if not isinstance(model, str) or not model.strip():
        raise ValueError('A cloud model name is required')
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Prompt cannot be empty')
    if not isinstance(max_output_tokens, int) or not 1 <= max_output_tokens <= 32768:
        raise ValueError('Output limit must be 1..32768')
    url, key_name = PROVIDERS[provider]
    key = os.environ.get(key_name)
    if not key:
        raise ValueError(f'Set {key_name} locally; never put keys in prompts or source files')
    headers = {'Content-Type': 'application/json'}
    payload = {'model': model, 'stream': False}
    if provider == 'openai':
        headers['Authorization'] = 'Bearer ' + key
        payload.update(input=text, max_output_tokens=max_output_tokens, store=False)
    else:
        payload.update(messages=[{'role':'user','content':text}], max_tokens=max_output_tokens)
        if provider == 'claude':
            headers.update({'x-api-key':key, 'anthropic-version':'2023-06-01'})
            workspace = os.environ.get('ANTHROPIC_WORKSPACE_ID')
            if workspace:
                headers['anthropic-workspace-id'] = workspace
        else:
            headers['Authorization'] = 'Bearer ' + key
    return urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def send(provider, model, text, max_output_tokens=1024):
    request = build_request(provider, model, text, max_output_tokens)
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=180) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        # Do not print response bodies or credentials. Do not automatically retry billable calls.
        raise RuntimeError(f'{provider} HTTP {error.code}; check account, model and API access') from None
    except (OSError, ValueError):
        raise RuntimeError(f'{provider} request failed or returned invalid JSON; no automatic retry was made') from None
    if provider == 'openai':
        output = '\n'.join(block.get('text','') for item in data.get('output',[])
                           if item.get('type') == 'message' for block in item.get('content',[])
                           if block.get('type') == 'output_text')
    elif provider == 'claude':
        output = '\n'.join(block.get('text','') for block in data.get('content',[]) if block.get('type')=='text')
    else:
        output = (data.get('choices') or [{}])[0].get('message',{}).get('content') or ''
    return {'provider':provider, 'model':data.get('model',model), 'text':output,
            'usage':data.get('usage'), 'id':data.get('id'),
            'status':data.get('status'), 'stop_reason':data.get('stop_reason'),
            'note':'Provider-reported usage for this call only; no baseline cost comparison.'}
