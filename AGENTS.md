# Agent guidance

- Do not copy CopperScript compiler code into this repository.
- Do not invent package pins, electrical limits, or mux facts. Use `?` and mark evidence `unresolved` when a source does not establish a value.
- Downloaded source documents belong in ignored `cache/`; commit only manifests, hashes, evidence, and concise generated bundles.
- Never execute downloaded source-provided code.
- Keep generated files deterministic and run `python -m pytest` before committing.
- Production publication is blocked by unresolved facts; illustrative values are never acceptable in a production bundle.
- Treat an installed STM32CubeMX `db/mcu` tree as local source only; never commit or redistribute ST XML.
- Hash every XML file actually consumed and keep only compact extraction artifacts/manifests in ignored `cache/` or `work/` paths.
- Do not infer alternate-function selector numbers from CubeMX signal names; if XML does not provide a selector, leave mux generation out or unresolved.
- Keep cross-vendor case studies bounded and source-first. Use official vendor URLs only and retain exact revision/table/page locators.
- Do not turn a lossy or unrepresentable case into a fake production bundle. Use an explicit non-representable fixture and classify the model gap.
- Run `python -m copperscript_stm32g0 compatibility` and keep both reports deterministic.
