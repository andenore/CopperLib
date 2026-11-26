# TPS61088RHLR — provisional bare part

Export `TPS61088RHLR`. Package-owned footprint
`footprints/TI_RHL0020A_TPS61088.kicad_mod` carries TI package identifier RHL0020A.
All SW and VOUT
pins are separate terminals and must be externally joined with reviewed copper.
Pad 21 has overlapping rectangular copper shapes and perimeter ground contacts; inspect
each physical contact, paste aperture and thermal path, not only pad numbering.

The pin map was checked against TI's EVM schematic, Figure 7 p7, SLVUAF2
(June 2015), https://www.ti.com/lit/ug/slvuaf2/slvuaf2.pdf, SHA256
`a957c5e8842e86d83037f8da9ccfcbebce7c61cfae7981ff1f6e63f3c00bf46a`.
Reference assembly/layout is Figures 8–11, pp9–10. The datasheet electrical
ranges were cross-checked against TI's indexed SLVSCM8D (August 2021),
https://www.ti.com/lit/ds/symlink/tps61088.pdf. The full Rev D PDF download
returned HTTP 404 during this review; an archived datasheet hash remains a
qualification gate. The package drawing was separately verified as below.
Do not claim the EVM hash is a
hash of the datasheet. Distributor summaries are not authoritative output-current
ratings: the advertised 10 A figure concerns switch current.

The package-owned footprint preserves the copper/mask/paste of managed KiCad
`Texas_VQFN-RHL-20` at provider revision
`7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd`, file SHA256
`ff36ff57cc668f1503bf51779b62571c8c61cc4113dd3eaca7f63f5a9fd9e2f3`.
That asset's twelve-vertex custom pad 21 is exactly the union of a
2.05 × 3.05 mm rectangle and a 0.75 × 3.85 mm rectangle, both centered at zero.
Using those supported primitives leaves every copper point unchanged. Four
0.2 × 0.6 mm perimeter PGND fingers, all twenty signal pads, and all eight
paste-only apertures are retained. The display-only 3D reference and duplicate
user-reference text are omitted; all fabrication and silkscreen graphics remain.
KiCad source: https://gitlab.com/kicad/libraries/kicad-footprints/ (CC-BY-SA-4.0
with KiCad library exception). This adaptation changes representation, not lands.

Dimensions were visually compared with TI RHL0020A drawing 4219071/A, May 2017,
land/stencil examples on PDF pp41–42 of BQ51050B SLUSB42F:
https://www.ti.com/lit/ds/symlink/bq51050b.pdf, SHA256
`6caa339988c57bbf8f787cea348546b9dd9463726ace4d1a6d97bf5bb375b36b`.
This is the same package drawing, not a substitution of the BQ51050B pin map.
Package drawing lists 0.05 mm typical corner radii; the managed central polygon
has square corners, retained here rather than silently changing copper.
Thermal vias remain consumer-owned and required for application qualification.

This boost converter has no true output disconnect. EN low does not isolate the
input from the output through the inductor/rectifier path. Applications requiring
load disconnection need an independently reviewed switch/protection stage.

The consumer owns frequency, mode, current-limit, soft-start, feedback divider,
compensation, inductor and effective capacitors. FSW resistor returns to SW;
BOOT capacitor returns to SW; VCC needs local decoupling. Floating MODE permits
PFM; ground selects forced PWM. Mode affects feedback reference and current-limit
calibration. NC pins may follow the EVM's ground connection and are not ground
current terminals. Keep compensation/feedback and AGND away from SW current.

No reusable layout macro is qualified. Consumers must supply strong placement
AND conductor/current-path constraints derived from the reference, minimize the
boost output-capacitor switching loop, join all power terminals, and review
ground/thermal vias, neckdowns and copper after routing. No universal distance,
frequency or current is asserted by this part. The three VOUT contacts carry
`emi_role = hot_supply`; PGND is `hot_return`, and SW contacts remain `switch`.
VIN (pad 9) is not the boost hot-supply terminal. TI application report SLVA790A,
July 2016 revised November 2019, sections 2.1-2.2 / Figures 1-3 (pp2-3), identifies
the output-capacitor switching loop and the local high-frequency output bypass:
https://www.ti.com/lit/an/slva790a/slva790a.pdf. This additional source was reviewed
online; its exact PDF archive/hash remains to be recorded before qualification.

These labels enable the compiler's representative boost hot-loop geometry check
on actual routed copper. Review the selected output capacitor and all external
power contacts; representative-pad screening does not establish current sharing.
This metadata supplies no switching waveform, universal operating frequency or
current. Numerical boost PEEC/full-wave adapter support is separate from these
terminal facts; do not claim such extraction or EMC compliance from the labels.

Required evidence remains component/DC-bias/current-limit review, loop stability,
load transients, minimum-source operation, startup/shutdown including pass-through,
input wiring/pack limits, thermal measurement, EMI and prototype qualification.
See `qualification.json`; this package is not production-qualified.
