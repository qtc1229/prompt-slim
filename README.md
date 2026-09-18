# Prompt Slim

**v0.1.0-alpha · experimental / 实验版本**

Local-first prompt compression with Ollama. Inspect changes, preserve exact constraints, and measure reference text tokens before copying your prompt into an AI tool.

本地 Prompt 压缩工具：保留指定片段、并排核对修改、测量参考 token。名称暂定；这是早期原型，尚已完成小样本本地压缩测试，尚未验证下游任务质量或费用收益。

## Quick start / 快速启动

Requirements: Python 3.11+, [Ollama](https://ollama.com/download), a downloaded text model.

```sh
ollama pull qwen3:4b
python -m venv .venv
# Windows:
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python app.py
# macOS/Linux: use .venv/bin/python instead.
```

Open http://127.0.0.1:8765. Windows users can double-click `start.cmd` after installing Python and Ollama.

```sh
python cli.py prompt.txt --model qwen3:4b --protect "do not overwrite" --json
python -m unittest -v
```

Run CLI/tests inside the virtual environment, or replace python with its full virtual-environment path.

## What is measured?

- Exact text token count for the named **o200k_base** reference encoding.
- This is **not** a universal tokenizer for Claude/DeepSeek, complete request accounting, or a bill estimate.
- Candidate must reduce reference tokens and preserve every user-specified literal fragment; otherwise the original is returned.
- Automatic checks do not prove semantic equivalence. Review negations, numbers, conditions, code and paths yourself.
- A smaller prompt can still increase total cost by damaging caching or causing retries.

## Privacy and limitations

The app binds to 127.0.0.1 and calls local Ollama at 127.0.0.1:11434. It does not save prompt history or send prompts to cloud providers. Ollama's own behavior is separate. The tokenizer may download its public vocabulary on first use; this does not include prompts.

Maximum input: 12,000 characters. This is an application limit, not a guarantee that every model can fit the input. There is no automatic chunking yet. The client requests a 16K context; use a compatible model. CLI offers opt-in single-turn cloud API calls. No transparent gateway, tool passthrough or subscription integration is currently implemented.

## Roadmap

See [PROGRESS.md](PROGRESS.md). Priority: real bilingual benchmark, downstream quality checks, target-provider accounting, easy installation, then cloud adapters and agent compatibility.

## Contributing

Bug reports with a minimal reproducible prompt are welcome. Remove secrets and private information from public issues. Include model name, Ollama version and expected constraints. Claims about compression should identify the encoding, dataset, fallback rate and quality evaluation.

MIT License. Third-party models retain their own licenses.

## Optional cloud calls / 可选云端调用

CLI `--send` explicitly sends the final prompt to a cloud provider and may incur API charges. If compression falls back, it sends the original. Without `--send`, prompts stay local. The web UI remains local-only. Set keys in your local environment, not in project files:

| Provider | Environment variable | Protocol |
|---|---|---|
| openai | OPENAI_API_KEY | Responses |
| claude | ANTHROPIC_API_KEY | Messages |
| deepseek | DEEPSEEK_API_KEY | Chat Completions |

For Claude multi-workspace keys, also set ANTHROPIC_WORKSPACE_ID.

```sh
python cli.py prompt.txt --send deepseek --cloud-model YOUR_MODEL_ID --json
```

The JSON includes the provider's original usage object. No automatic retries, cost-savings claim, or API-key storage. Model IDs must be chosen from your account. These adapters have mocked protocol tests; live cloud validation is pending because no cloud API keys are configured on the development machine. OpenAI API access is not equivalent to a Codex subscription or transparent Codex integration.

Sources: [OpenAI quickstart](https://developers.openai.com/api/docs/quickstart), [Claude API overview](https://platform.claude.com/docs/en/api/overview), [DeepSeek first call](https://api-docs.deepseek.com/).

## Initial local measurements

See [the smoke benchmark](evals/REPORT.md): 319 to 278 reference tokens across six development cases, including fallbacks. This is 12.9% in this small, non-held-out sample, not a general savings promise. Accepted prompts were manually compared; downstream task performance remains untested.


## Browser verification

Install requirements-dev.txt, start app.py, and run `python browser_smoke.py`. The current smoke test uses installed Microsoft Edge in an isolated headless profile and a local qwen3:4b model. It checks real compression, exact fragments, invalid-input recovery, JavaScript errors and mobile overflow.
