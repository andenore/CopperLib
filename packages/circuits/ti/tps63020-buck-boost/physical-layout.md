# Physical contract and qualification boundary

## Official evidence

Layout guidance was visually compared with these official TI documents:

| Document | Locator | SHA-256 |
| --- | --- | --- |
| [TPS63020 datasheet](https://www.ti.com/lit/ds/symlink/tps63020.pdf), SLVS916I Rev I | Section 10.1, Figure 31, p23; DSJ land drawings pp31–33 | `d117773bb7370fd79377bc70ce987eec3469ea5979547a09df52fca5f95b2e69` |
| [TPS63020EVM-487 guide](https://www.ti.com/lit/ug/slvu365/slvu365.pdf), SLVU365 March 2010 | Figures 6–8, pp6–7 | `a164c060584f238a27553efe054ad47916d90fcf4ca5739bf0d01c8e35c5c221` |

Cached documents belong under ignored `cache/ti/tps63020-layout/`.
TI calls for short, wide power connections, close input/output capacitors and
inductor, feedback close to the IC, and quiet control ground joining power
ground near the IC. No source-backed universal width/current rating is claimed.

## Authored adaptations

This is not extracted, traced or manufacturer-approved TI CAD. It substitutes
the Bourns inductor and three 0805 outputs, uses six copper layers and off-pad
0.6/0.3 mm through vias. The local component arrangement and shielded inner
feedback route are authored. The low-current VINA feed and output sense use
B.Cu behind the In4 GND plane; FB and EN use In2.Cu behind In1 GND. These
differences need engineering review, including reference-plane continuity.

Fixed F.Cu polygons own the L1/L2 switch paths and VIN/VOUT capacitor lobes.
Every paired switching/input/output land has an explicit local entry. Pad 15's
central land and eight touching comb contacts are wired as real copper, not
an internal-pad exemption. Pad 14 (PG) is intentionally isolated. Control GND
joins exposed-pad GND directly near the IC. EP extensions reach two three-via
banks; capacitor grounds have separate declared off-pad contacts to the host
GND planes. Dedicated contacts are not substituted with nearby arbitrary vias.

The enabled variant terminates EN at a fixed F.Cu lead-in, not at its In2/F.Cu
transition via. The host must enter the free F.Cu endpoint. Both via layers are
therefore connected by owned copper even if host routing otherwise prefers
In2.Cu; this prevents a native dangling-via warning. This control-branch repair
does not change the switching, feedback or power-current paths.

Power port lead-ins are 0.8 mm; paired IC entries are 0.24 mm. Those dimensions
preserve this geometry, **not a proven peak/RMS current capacity**. The output
sense is taken from output-capacitor copper, with no autorouter-owned private
feedback/switching connections. Private routing protection covers F/In2/B;
fill exclusions cover In2/In3/B. In1/In4 remain the host ground references.
The owned top ground zone must not overlap another owner's top zone. The host
must leave room for the external port stubs as well as the protected rectangle.
Compatible HOST GND fill may overlap this owned top GND zone when its CopperScript
`copper_zone` explicitly sets `allow_same_net_hard_macro_overlap = true`.
This is not permission for foreign-net fill or new tracks/vias in the protected
region. Keep the specified fill exclusions and local conductor geometry intact;
verify actual native filled-copper continuity and DRC after integration. A remote
RF keepout remains effective but must not disable this compatible GND overlap.

## Scoped local widths

The v0.4 asset explicitly declares width contracts for individual 0.24 mm
package entries and 0.2 mm VINA/EN/output-sense branches. Main VIN/VOUT port
lead-ins remain 0.8 mm and have no width exception. These contracts bind exact
immutable owner segments, record purpose and evidence, preserve host routing
and fabrication minimums, and appear in CopperScript DRC audit findings. They
do not certify a neckdown's current capacity or authorize thinner host rails.

## Validation and release boundary

Asset tests cover deterministic generation, role/pad completeness, independent
ground contacts, port membership and process dimensions. CopperAssetTracker's
`scripts/probe_power_macros.py` binds its exact locked footprints, rigidly rotates
the macro and checks isolated copper acceptance plus native KiCad refill/DRC.
This cuts away the host circuitry for a geometry test only. Full-board placement,
external routing, ground fill and native DRC remain separate required checks.

Before production, resolve peak/RMS conductor and via capacity at actual copper
weight, pad neckdowns, MLCC bias derating, inductor saturation/temperature at
minimum battery voltage, feedback stability, modem load transients, EMI,
thermal behavior, paste/thermal-via assembly and actual six-layer stackup.
The selected host values and component voltage/current ratings also require
review. Keep `production_publishable=false` until these are resolved; neither
isolated connectivity nor native DRC constitutes production approval.
