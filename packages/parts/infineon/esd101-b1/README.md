# esd101-b1

Import `github.com/andenore/CopperLib/packages/parts/infineon/esd101-b1`.
Exports: `ESD101_B1_02EL`.

- `ESD101_B1_02EL`: one-line bidirectional ESD diode in PG-TSLP-2-20
  (1.0 x 0.6 mm), from the ESD101-B1-02 Series data sheet revision 1.4
  (2017-10-26): ±5.5 V working voltage, 0.2 pF maximum at 1 MHz (0.1 pF
  typical at 1 GHz), leakage under 0.1 nA typical and 20 nA maximum at 5.5 V,
  ±12 kV IEC 61000-4-2 contact. The holding voltage (6.1 V minimum) is above
  the working voltage. Clamping is high for a low-capacitance part (18 V at 8 A,
  30 V at 16 A TLP), so a sensitive input behind it may need a second stage.

Footprint `footprints/Infineon_TSLP-2-20.kicad_mod` follows the data sheet's
Figure 15 (TSLP-2-19, -20-FP V01): 0.6 x 0.35 mm copper pads 0.3 mm apart,
0.45 x 0.28 mm paste apertures as separate paste pads. The solder mask comes
from the board's mask expansion; Figure 15's mask outline was not reproduced.
Pin 1 is at +y, beside the silkscreen bar (the package's pin-1 marking side).

No production qualification is claimed: land pattern, assembly and system ESD
performance remain open.
