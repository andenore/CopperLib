# cyusb4013

Import `github.com/andenore/CopperLib/packages/parts/infineon/cyusb4013`.
Exports: `CYUSB4013_FCAXI`.

- `CYUSB4013_FCAXI`: Port0 narrow SDR pin assignment; GPIO mappings selected by firmware; unused balls cannot be connected without modeling.
  Footprint `footprints/FX10_FCA169.kicad_mod`; source [https://www.infineon.com/dgdl/Infineon-CYUSB401x_EZ-USB_FX10_USB_10_Gbps_peripheral_controller-DataSheet-v02_00-EN.pdf?fileId=8ac78c8c956a0a4701959618c62d4947](https://www.infineon.com/dgdl/Infineon-CYUSB401x_EZ-USB_FX10_USB_10_Gbps_peripheral_controller-DataSheet-v02_00-EN.pdf?fileId=8ac78c8c956a0a4701959618c62d4947), 002-40837 Rev C pp31-39 Tables9-12; p83 FCA169 drawing.

Migrated from CopperProbeParts 0.1.6-candidate (`96dbd68`) with the definitions, pin maps, custom footprint bytes and layout contracts unchanged; only the package path and evidence locations were rebound. `evidence/contract.json` keeps the CopperProbeParts source/pin inventory for each part.

`footprints/` holds the FCA169 land authored from the p83 drawing with the 0.25 mm land diameter measured in KIT_FX10_FMC_001 (`evidence/fx10-kit-escape/`); mask/paste and assembly qualification remain open. Its SHA-256 is `4592df9cbf07ad033e162ee52fb36bea4e23ee3fc2a7411f0dd4500c9cb04f6e`; the `footprint_sha256` in `evidence/contract.json` predates the 0.25 mm land change and is kept as recorded.

Download the cited source documents to the ignored repository-root `cache/cyusb4013/KIT_FX10_FMC_001_SCH.pdf, cache/cyusb4013/an238422-hardware-guidelines.pdf, cache/cyusb4013/fx10-datasheet.pdf` paths named in the layout contract; their hashes are recorded there.

No production qualification is claimed. Prototype source facts only; land patterns, assembly, electrical and thermal qualification remain open as recorded in the contracts.
