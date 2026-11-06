# tps1h200a

Exact reusable part interface and manufacturer package mapping for TI TPS1H200AQDGNRQ1 (40 V, 200 mΩ single-channel smart high-side switch with adjustable current limit, HVSSOP-8 PowerPAD). Source: [SLVSEE0E, p3 pin functions, pp4-7 ratings, pp22-23 typical application, p28 land pattern](https://www.ti.com/lit/ds/symlink/tps1h200a-q1.pdf). The source identity is in `evidence/source.json`.

The footprint follows the DGN0008K example board layout: eight 1.4 x 0.45 mm pads on 4.4 mm row centres at 0.65 mm pitch and a 1.57 x 1.89 mm exposed pad with four paste windows. The exposed pad is unconnected inside the device; ground it or leave it floating.

Typical support: series resistors on IN/DIAG_EN, a pull-up on the open-drain FAULT output, R_CL = 0.8 V × 2500 / I_limit from CL to GND, and a DELAY capacitor (latch-off), a pull-up (auto-retry) or a short to GND (holding).

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
