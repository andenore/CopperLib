# CopperScript STM32G0 library

Deterministic, provenance-first device data for CopperScript, starting with a bounded proof of concept for `STM32G0B1CBT6`.

This repository is intentionally separate from the CopperScript compiler. It records a compatible compiler revision (`ee63d69`) and feeds the upstream `pcbir.devicegen` implementation. The proof currently covers four verified LQFP48 GPIO pins (`PA0`–`PA1`, `PC0`–`PC1`) and their package bonds. It is incomplete and cannot be published as a production package.

## Quick start

```powershell
python -m pip install -e '.[test,upstream]'
python -m copperscript_stm32g0 validate
python -m copperscript_stm32g0 generate
python -m copperscript_stm32g0 coverage
python -m pytest
```

The normalized bundle is in `data/bundles/stm32g0b1/`. The generated `.copper` files are written under `generated/` by upstream `pcbir.devicegen`. A production package is refused unless the request declares complete coverage and contains no unresolved or illustrative facts. Network acquisition is opt-in and writes only to the ignored `cache/` directory.

## Workflow

1. `data/requests.json` declares requested orderable devices and bounded work packets.
2. `scripts/acquire_sources.py` records source URLs and SHA-256 files without executing downloaded content.
3. A low-cost Codex agent processes one packet at a time, using the instructions in `work-packets/README.md`, and writes JSONL evidence.
4. `generate` calls the pinned upstream `pcbir.devicegen` validator and renderer.
5. CI installs CopperScript at `ee63d69`, validates the bundle, regenerates `.copper` files, and fails on a dirty diff.

Evidence lives in `data/evidence.jsonl`; the generated bundle is intentionally concise. Facts are labelled `verified`, `inferred`, `unresolved`, or `illustrative`. `?` is reserved for unresolved cells and is rejected by upstream validation.

## Sources

- ST product page: https://www.st.com/en/microcontrollers-microprocessors/stm32g0b1cb.html
- ST datasheet `DS13560`, `STM32G0B1xB/xC/xE`, PDF: https://www.st.com/resource/en/datasheet/stm32g0b1cc.pdf
- CopperScript compatibility target: https://github.com/andenore/CopperScript/tree/ee63d69

No remote is configured by this repository. See `AGENTS.md` for contribution rules.
