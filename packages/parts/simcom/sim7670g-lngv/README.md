# SIM7670G-LNGV (provisional used-pin model)

Export `SIM7670G_LNGV`; exact JLCPCB identity C45935408. The 124-land footprint
and `import_footprint.py` are package-owned. The model preserves the previously
checked used pins; unused multifunction pins remain `do_not_connect`. It is not
a complete or production-qualified device definition.

See [pending USB integration review](usb-review-pending.md) for source-backed
related-family review triggers. Exact-model applicability remains unconfirmed.

- SIMCom supplier-linked specification:
  https://datasheet.lcsc.com/datasheet/pdf/ee03db1eecfc7b8f7e60fb0421704843.pdf?productCode=C45935408
  SHA256 `12d00aae02bc600ac678f8d478d86e099f3339f9a9a7e2837773e5d9489acb11`.
- Used pins were cross-checked against the exact CAD symbol and SIMCom-authored
  SIM7672X Hardware Design V1.01 Tables 4/5:
  https://files.waveshare.com/wiki/SIM7670G-LTE-Cat-1-GNSS-HAT/SIM7672X_Series_Hardware_Design_V1.01.pdf
  This does not establish complete exact-variant equivalence.
- Package data: JLCEDA/EasyEDA Official Library, https://lceda.cn/ and
  https://easyeda.com/; API
  https://easyeda.com/api/products/C45935408/components?version=6.5.44
  UUID `2be3f51bf5e54bc28cbf6586caa12048`, title LCC-124_L24.0-W24.0-P1.0-TL.
  Input JSON SHA256 `bde713d456f592968facd909ba03b4e3736ff7edb684c97ac55bf3d7429e3df6`.

Retain those credits when redistributing converted land data. The converter
validates exact identity and preserves all 124 lands; it never executes source
code. Keep downloaded input in ignored `cache/`. Run from the repository root:

```console
python packages/parts/simcom/sim7670g-lngv/import_footprint.py cache/modem-easyeda.json
```

Host obligations: connect every required power/ground contact, qualify burst
delivery, provide the required logic translation and PWRKEY driver, and review
SIM/USB/ESD support. Audit the exact-model reference schematic and layout for
antenna matching/tuning, feed impedance/reference planes, ground returns and
short-distance constraints before reuse. External matching requirements are
**unresolved**, not assumed absent because a coax connector is used. No RF
matching hard macro or qualified stackup is provided. The authored pin-one
silkscreen marker is moved beside pad 1, inside the body outline, to avoid
its solder-mask opening. It is an assembly orientation aid, covered after
mounting; all 124 source lands and the courtyard are unchanged. This cosmetic
repair does not resolve matching, exact-variant or hardware qualification.
