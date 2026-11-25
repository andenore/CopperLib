# opa859

Import `github.com/andenore/CopperLib/packages/parts/ti/opa859`.
Exports: `OPA859IDSGR`.

- `OPA859IDSGR`: 1.8 GHz unity-gain-bandwidth FET-input amplifier in an 8-pin WSON
  (DSG, 2 x 2 mm), data sheet SBOS852A. 3.3 to 5.25 V supply, unity-gain stable
  with about 63 degrees of phase margin as a follower, 0.62 pF common-mode and
  0.2 pF differential input capacitance, 0.5 pA typical bias current. The
  OPA859IDSGT is the same device in 250-piece reels.
  Pins: 1 FB (internally the output; in a follower tie it to IN-), 2 NC (do not
  connect), 3 IN-, 4 IN+, 5 VS-, 6 OUT, 7 VS+, 8 PD (high = on), exposed pad to VS-.
  Footprint `Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm`
  (KiCad library; the consumer declares and locks its KiCad footprint provider).

Simulation: a built-in `sim opamp` macro model from the data sheet's 5 V figures
(derivations and gaps in `part.copper`). The input common-mode range is only
VS- + 0.4 V to VS- + 3.4 V (3.6 V typical): about -2.1 V to +0.9 V on a
+/-2.5 V supply, which a design with a +/-1 V signal must respect.

No production qualification is claimed.
