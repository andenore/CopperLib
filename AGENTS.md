# Agent guidance

- Do not copy CopperScript compiler code into this repository.
- Do not invent package pins, electrical limits, or mux facts. Use `?` and mark evidence `unresolved` when a source does not establish a value.
- Downloaded source documents belong in ignored `cache/`; commit only manifests, hashes, evidence, and concise generated bundles.
- Never execute downloaded source-provided code.
- Keep generated files deterministic and run `python -m pytest` before committing.
- Production publication is blocked by unresolved facts; illustrative values are never acceptable in a production bundle.
