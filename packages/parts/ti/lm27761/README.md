# lm27761

Import `github.com/andenore/CopperLib/packages/parts/ti/lm27761`.
Exports: `LM27761DSGR`.

- `LM27761DSGR`: Negative regulator 1.22 V reference; flying, reservoir and output capacitors mandatory.
  Footprint `Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm`; source [https://www.ti.com/lit/ds/symlink/lm27761.pdf](https://www.ti.com/lit/ds/symlink/lm27761.pdf), SNVSA85D p3 Table4-1; pp12-17 support and layout.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path was rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

Standard footprint: `Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm` (KiCad 10 library); consumers declare and lock their KiCad footprint provider.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
