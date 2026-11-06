# ltc6268

Import `github.com/andenore/CopperLib/packages/parts/adi/ltc6268`.
Exports: `LTC6268IS6`.

- `LTC6268IS6`: Unity-gain stable version; input capacitance 0.45 pF typical, not a complete probe capacitance guarantee.
  Footprint `Package_TO_SOT_SMD:SOT-23-6`; source [https://www.analog.com/media/en/technical-documentation/data-sheets/62689f.pdf](https://www.analog.com/media/en/technical-documentation/data-sheets/62689f.pdf), 62689f p2 TSOT23 diagram; p3 ordering; input-node layout pp14-17.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path was rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

Standard footprint: `Package_TO_SOT_SMD:SOT-23-6` (KiCad 10 library); consumers declare and lock their KiCad footprint provider.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
