# lp5907

Import `github.com/andenore/CopperLib/packages/parts/ti/lp5907`.
Exports: `LP5907MFX_2V5`.

- `LP5907MFX_2V5`: LP5907MFX-2.5/NOPB, a 250 mA ultra-low-noise fixed 2.5 V LDO in
  SOT-23-5, data sheet SNVS798 revision Q. 2.2 to 5.5 V input, 6.5 uVRMS noise
  (10 Hz to 100 kHz, 250 mA), PSRR 82 dB at 1 kHz and 60 dB at 100 kHz, EN high above
  1.2 V. Pins: 1 IN, 2 GND, 3 EN, 4 N/C, 5 OUT, the same as TI's TPS7A2025PDBVR, so it
  can replace that part on the same footprint. Output capacitor 0.7 to 10 uF with
  5 to 500 mohm ESR; input capacitor 0.7 uF minimum.

Simulation: a built-in `sim regulator` macro model from the data sheet (derivations in
`part.copper`). The fixed 2.5 V option is confirmed by the Mouser listing, not by the
data sheet pages read.

No production qualification is claimed.
