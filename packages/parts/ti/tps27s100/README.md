# tps27s100

Exact reusable part interface and manufacturer package mapping for TI TPS27S100APWPR (40 V, 80 mΩ, 4 A single-channel industrial high-side switch with adjustable current limit and open-drain status, HTSSOP-14 PowerPAD). Source: [SLVSE42B, p3 pin functions, pp4-7 ratings, p17 current limit, p25 typical application, pp35-36 land pattern](https://www.ti.com/lit/ds/symlink/tps27s100.pdf). The source identity is in `evidence/source.json`.

The footprint follows the PWP0014K example board layout: fourteen 1.5 x 0.45 mm pads on 5.8 mm row centres at 0.65 mm pitch and a 3.4 x 5 mm thermal land with a 2.6 x 2.59 mm solder-mask-defined opening and four paste windows. No thermal vias are included. The thermal pad may be grounded or left floating.

Typical support: series resistors on EN/DIAG_EN, a pull-up on the open-drain FLT output, R_ILIM = 1.233 V × 2000 / I_limit from ILIM to GND (ILIM to device GND when a GND network is used), and input and output capacitors. Faults recover automatically; there is no latch-off input. The B version (TPS27S100BPWPR) has a current-monitor output in place of FLT and is not modelled here.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
