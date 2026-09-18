# Prompt Slim

Local-first prompt compression with Ollama. Inspect changes, preserve exact constraints, and measure reference text tokens before copying your prompt into an AI tool.

本地 Prompt 压缩工具：保留指定片段、并排核对修改、测量参考 token。名称暂定；这是早期原型，尚未验证真实模型质量或费用收益。

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

Maximum input: 12,000 characters. This is an application limit, not a guarantee that every model can fit the input. There is no automatic chunking yet. The client requests a 16K context; use a compatible model. No cloud gateway, tool passthrough or subscription integration is currently implemented.

## Roadmap

See [PROGRESS.md](PROGRESS.md). Priority: real bilingual benchmark, downstream quality checks, target-provider accounting, easy installation, then cloud adapters and agent compatibility.

## Contributing

Bug reports with a minimal reproducible prompt are welcome. Remove secrets and private information from public issues. Include model name, Ollama version and expected constraints. Claims about compression should identify the encoding, dataset, fallback rate and quality evaluation.

MIT License. Third-party models retain their own licenses.