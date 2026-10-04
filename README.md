# CopperScript device-model compatibility lab

Deterministic, provenance-first device data and compatibility fixtures for CopperScript. The repository retains a bounded `STM32G0B1CBT6` proof and adds four cross-vendor model-gap case studies.

This repository is intentionally separate from the CopperScript compiler. It records a compatible compiler revision (`8706292`, including mechanical profiles) and feeds the upstream `pcbir.devicegen` implementation. The proof currently covers four verified LQFP48 GPIO pins (`PA0`–`PA1`, `PC0`–`PC1`) and their package bonds. It is incomplete and cannot be published as a production package.

Part-generation agents must follow the [internal pad connectivity checklist](internal-pad-connectivity.md).
The pinned compiler supports permanent battery/switch contact groups and KiCad 10 exports.
Publish the compiler revision before publishing this library revision so CI can fetch the pin.

## Quick start

```powershell
python -m pip install -e '.[test,upstream]'
python -m copperscript_stm32g0 validate
python -m copperscript_stm32g0 generate
python -m copperscript_stm32g0 coverage
python -m pytest
python -m copperscript_stm32g0 compatibility
```

The normalized bundle is in `data/bundles/stm32g0b1/`. The generated `.copper` files are written under `generated/` by upstream `pcbir.devicegen`. A production package is refused unless the request declares complete coverage and contains no unresolved or illustrative facts. Network acquisition is opt-in and writes only to the ignored `cache/` directory.

## Workflow

1. `data/requests.json` declares requested orderable devices and bounded work packets.
2. `scripts/acquire_sources.py` records source URLs and SHA-256 files without executing downloaded content.
3. A low-cost Codex agent processes one packet at a time, using the instructions in `work-packets/README.md`, and writes JSONL evidence.
4. `generate` calls the pinned upstream `pcbir.devicegen` validator and renderer.
5. CI installs the exact CopperScript revision in `pyproject.toml`, validates the bundle, regenerates `.copper` files, and fails on a dirty diff. The older bounded case-study reports retain their original revision/evidence rather than being silently relabelled.

Evidence lives in `data/evidence.jsonl`; the generated bundle is intentionally concise. Facts are labelled `verified`, `inferred`, `unresolved`, or `illustrative`. `?` is reserved for unresolved cells and is rejected by upstream validation.

## STM32CubeMX ingestion

The optional CubeMX importer accepts either an installation root or its `db/mcu` directory. It reads the requested MCU XML plus referenced IP/config XML, including CubeMX's `Name` + `Version` file convention such as `<IP>-<version>_Modes.xml`. It extracts identity/package/pins/signals and writes only a compact JSON artifact plus adjacent SHA-256 source manifest under ignored output:

```powershell
python -m copperscript_stm32g0 cubemx-ingest --cubemx-root C:\Path\To\STM32CubeMX --cubemx-identity STM32G0B1CBTx --output cache\cubemx\stm32g0b1.json
python -m copperscript_stm32g0 cubemx-reconcile --cubemx-root C:\Path\To\STM32CubeMX --cubemx-identity STM32G0B1CBTx
python -m copperscript_stm32g0 cubemx-packet --cubemx-root C:\Path\To\STM32CubeMX --cubemx-identity STM32G0B1CBTx --pin PC0
```

Typical locations are `C:\Program Files\STMicroelectronics\...\STM32CubeMX\db\mcu` on Windows, `/usr/local/STMicroelectronics/STM32CubeMX/db/mcu` on Linux, and `/Applications/STMicroelectronics/STM32CubeMX.app/Contents/Resources/db/mcu` on macOS, but the importer does not assume these paths. The host used for this proof had no CubeMX installation at the standard Windows paths, so no real local import was performed. CI uses the clearly synthetic fixtures in `tests/fixtures/cubemx/`. Raw ST XML is intentionally never committed or redistributed.

## Sources

- ST product page: https://www.st.com/en/microcontrollers-microprocessors/stm32g0b1cb.html
- ST datasheet `DS13560 Rev 6` (February 2026), `STM32G0B1xB/xC/xE`, PDF: https://www.st.com/resource/en/datasheet/stm32g0b1cc.pdf
- Current CopperScript dependency: https://github.com/andenore/CopperScript/tree/87062923657a1f1aef4b9ba87146d8119318f8ea

See `AGENTS.md` for contribution rules.

## Cross-vendor compatibility lab

`python -m copperscript_stm32g0 compatibility` writes deterministic JSON and Markdown reports under `reports/`. The case studies are intentionally bounded and non-publishable: Nordic `nRF52840-QIAA`, Infineon `CYUSB4014-FCAXI`, Analog Devices `AD4134BCPZ`, and Texas Instruments `OPA2197ID`. Their source facts and locators are kept in `data/case-studies/`; the reports classify current CopperScript support as represented, lossy, unrepresentable, or expansion-risk.

The lab currently exposes gaps around closed part kinds, analog direction semantics, differential grouping/polarity, repeated functional units, shared supplies, wildcard/parametric routing, high-speed interface semantics, no-connect/exposed-pad rules, voltage/current/range metadata, and interface kinds beyond I2C. It does not change the CopperScript language or model.

## Consumable CopperScript packages

CopperLib is also the canonical repository for reusable `.copper` part,
device, and circuit-module definitions. The repository declares the module
path `github.com/andenore/CopperLib`; packages live below `packages/` and are
imported using stable URL-like paths.

The first package is
`github.com/andenore/CopperLib/packages/full_vertical`, used by CopperScript's
full-vertical tracker acceptance design. It is explicitly a non-production
package while its bounded device models and prototype support parts are being
replaced by complete, evidence-backed definitions. See
`packages/full_vertical/README.md` for its publication blockers.

The [CM4 package](packages/raspberry_pi_cm4/README.md) adds two real Hirose
100-contact carrier sockets with complete CM4 signal numbering, four mounting
holes and a reusable zero-height module-body reservation. The CopperScript
carrier example composes the profile with its own outline and antenna keepout.
These are carrier interfaces, not an active CM4 model or an order-ready bundle;
generic reference headers still need exact assembly selections.
