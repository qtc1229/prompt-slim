# Delivery checklist

Objective: local prompt compression open-source project; attract GitHub users.

- [x] Local UI and Ollama structured-output client
- [x] Literal protection and fallback
- [x] Reference token counting (o200k_base, NOT all-provider billing)
- [x] Install Ollama and Qwen3 4B, verify GPU inference
- [ ] Real reproducible bilingual compression benchmark with quality limitations
- [ ] Durable unit/integration tests and browser QA
- [ ] CLI and cloud adapter(s); Codex/Claude protocol compatibility
- [ ] Improve documentation, onboarding, CI and release artifacts
- [ ] Inspect GitHub authentication; publish only reviewed project files

Ollama 0.34.2 installed from official installer after valid Ollama Inc. Authenticode check. Local API /api/version verified. Qwen3 4B download active, exec session 43596.

Six unit tests pass; CLI implemented; CI matrix configured but not yet run on GitHub. Bilingual eval cases and benchmark.py ready.
No cloud keys detected in GH_TOKEN/GITHUB_TOKEN environment names. No gh executable detected.

Verified Qwen3 4B digest 359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7. Ollama ps reports 100% GPU, 16K context, 5.1 GB.
Real benchmark active in exec session 9713. Local UI PID 71700; HTTP 200 verified. Browser control tool timed out twice; UI interaction QA remains pending.
GitHub connector authenticates as qtc1229. No repository-creation tool exposed; publication path remains to be resolved.
