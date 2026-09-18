"""Compress a UTF-8 file locally: python cli.py input.txt --model qwen3:4b."""
import argparse
import json
import sys
from pathlib import Path
from app import compress
from providers import send, build_request


def main():
    parser = argparse.ArgumentParser(description='Local prompt compression using Ollama')
    parser.add_argument('input', help='UTF-8 input file, or - for stdin')
    parser.add_argument('--model', default='qwen3:4b')
    parser.add_argument('--protect', action='append', default=[], help='Exact fragment; repeat for multiple')
    parser.add_argument('--json', action='store_true', help='Include reference token counts and warnings')
    parser.add_argument('--send', choices=['openai','claude','deepseek'], help='Opt in to sending final text to this cloud API (may incur charges)')
    parser.add_argument('--cloud-model', help='Exact model ID from your provider account')
    parser.add_argument('--max-output-tokens', type=int, default=1024)
    args = parser.parse_args()
    try:
        text = sys.stdin.read() if args.input == '-' else Path(args.input).read_text(encoding='utf-8')
        if args.send:
            if not args.cloud_model:
                parser.error('--send requires --cloud-model')
            build_request(args.send, args.cloud_model, text, args.max_output_tokens)
        result = compress({'text':text, 'model':args.model, 'protected':'\n'.join(args.protect)})
        if args.send:
            result['cloud'] = send(args.send, args.cloud_model, result['text'], args.max_output_tokens)
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result.get('cloud', {}).get('text', result['text']))
        if not args.json:
            print(f"o200k_base text tokens: {result['original_tokens']} -> {result['compressed_tokens']}; not provider billing", file=sys.stderr)
            for warning in result['warnings']:
                print(warning,file=sys.stderr)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        parser.exit(1, f'Compression failed: {error}\n')

if __name__ == '__main__':
    main()