# Local smoke benchmark — Qwen3 4B

Environment: Windows, RTX 3060 12GB; Ollama 0.34.2; model qwen3:4b Q4_K_M. Ollama reports 100% GPU and 16,384 context. Model digest: 359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7.

Six developer-authored cases, used for prompt iteration; **not a held-out benchmark**. Reference encoding: o200k_base, text only. No cloud billing or downstream task success measured.

| Case | Before | Final | Outcome |
|---|---:|---:|---|
| Chinese file script | 70 | 70 | Reverted: protected phrase missing |
| Chinese purchasing | 76 | 64 | Compressed |
| English API | 67 | 67 | Reverted: no-logging constraint missing |
| Short Chinese question | 6 | 6 | Unchanged |
| Literal special string | 39 | 28 | Compressed |
| Chinese JSON format | 61 | 43 | Compressed |

Aggregate final tokens: 319 → 278, 12.9% reduction including fallbacks. Three accepted candidates, three fallbacks. Warm wall time: 0.25–1.48 seconds per case in this run. First baseline cold call took 64.48 seconds; this is not included in warm timings.

Assistant manual review of accepted candidates: purchasing quantities, minimum size, HDMI, price uncertainty and budget ceiling remain; literal-string short-paragraph instruction remains; JSON schema/array/null/Chinese constraints remain. This is a manual prompt comparison, not an independent quality test or task execution. The two missing-constraint candidates demonstrate why literal checks and user review are necessary.

Failure baseline is preserved in baseline-results.json, prompt-only revision in revised-results.json, current masked-literal run in masked-results.json. Reproduce current behavior with `python benchmark.py --output evals/new-results.json` in the virtual environment. Results may vary across hardware and runtime versions.

Next gate: larger held-out cases, automatic protection of high-risk text, downstream quality tests, and browser interaction QA. Current version remains a review-before-use prototype.