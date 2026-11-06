# tps7a20

Import `github.com/andenore/CopperLib/packages/parts/ti/tps7a20`.
Exports: `TPS7A2018PDBVR`, `TPS7A2025PDBVR`.

- `TPS7A2018PDBVR`: Fixed low-noise LDO; preserve effective input/output capacitance.
  Footprint `Package_TO_SOT_SMD:SOT-23-5`; source [https://www.ti.com/lit/ds/symlink/tps7a20.pdf](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), SBVS338H p4 DBV map; operating conditions and stability.
- `TPS7A2025PDBVR`: Fixed low-noise LDO; preserve effective input/output capacitance.
  Footprint `Package_TO_SOT_SMD:SOT-23-5`; source [https://www.ti.com/lit/ds/symlink/tps7a20.pdf](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), SBVS338H p4 DBV map; operating conditions and stability.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path was rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

Standard footprint: `Package_TO_SOT_SMD:SOT-23-5` (KiCad 10 library); consumers declare and lock their KiCad footprint provider.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
