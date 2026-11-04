# blm15px

Import `github.com/andenore/CopperLib/packages/parts/murata/blm15px`.
Exports: `BLM15PX221SN1D`.

- `BLM15PX221SN1D`: Exact FX10 reference-kit bead; host current/bias and assembly qualification remain required.
  Footprint `footprints/BLM15PX_Kit0402.kicad_mod`; source [https://www.infineon.com/assets/row/public/documents/30/60/infineon-hardware-design-file-kit-fx10-fmc-001-pcbdesigndata-en.zip](https://www.infineon.com/assets/row/public/documents/30/60/infineon-hardware-design-file-kit-fx10-fmc-001-pcbdesigndata-en.zip), KIT_FX10_FMC_001 schematic 630-60643-01 Rev03 sheets5-8 FB1-FB7; 220 ohm at 100 MHz.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path and evidence locations were rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

`footprints/` holds the 0402 land taken from the Infineon KIT_FX10_FMC_001 design data; it needs independent assembly review.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
