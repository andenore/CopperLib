# abm8

Import `github.com/andenore/CopperLib/packages/parts/abracon/abm8`.
Exports: `ABM8_24MHZ`.

- `ABM8_24MHZ`: Load capacitors are provisional until installed stray capacitance is established.
  Footprint `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm`; source [https://abracon.com/Resonators/ABM8.pdf](https://abracon.com/Resonators/ABM8.pdf), ABM8 pin diagram; 24 MHz B2 18 pF load ordering code.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path was rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

Standard footprint: `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` (KiCad 10 library); consumers declare and lock their KiCad footprint provider.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
