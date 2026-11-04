# ths4541

Import `github.com/andenore/CopperLib/packages/parts/ti/ths4541`.
Exports: `THS4541IRGTR`.

- `THS4541IRGTR`: EP electrically isolated; tie to ground for heat spreading. Split-supply adaptation requires simulation and bench qualification.
  Footprint `footprints/Texas_RGT0016A_VQFN-16-1EP_3x3mm_P0.5mm_EP1.45x1.45mm.kicad_mod`; source [https://www.ti.com/lit/ds/symlink/ths4541.pdf](https://www.ti.com/lit/ds/symlink/ths4541.pdf), SLOS375B pp3,35,50-51; RGT0016A land pattern.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path, the bundled footprint reference, and evidence locations were rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

The RGT0016A land in `footprints/` is authored from TI SLOS375B PDF pp60-61 (drawing 4219032/A); KiCad 10 has no RGT0016A footprint, so the reference now points at this copy instead of `Package_DFN_QFN:`.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
