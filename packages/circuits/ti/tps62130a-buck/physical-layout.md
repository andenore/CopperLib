# Provisional six-layer physical macro

Review this adaptation against the [CopperLib hard-macro checklist](../../../../docs/hard-macro-review-checklist.md).

The two JSON assets preserve nine component poses and their local copper for the
existing `TPS62130A_BUCK_2U2` circuit, including its board-owned feedback resistors.
The always-on variant joins EN to VIN locally. The enabled variant exposes a
separate EN port. Neither asset changes the electrical module or resistor values.
`production_publishable` remains false; geometric acceptance is not regulator,
thermal, EMI or assembly qualification.

## Evidence and adaptations

| Official source | Identity and use |
| --- | --- |
| [TPS62130A datasheet](https://www.ti.com/lit/ds/symlink/tps62130a.pdf) | SLVSAG7F Rev F, November 2021; SHA-256 `f9b1af285622c0cf1a5991f9641a6e64c5e6d899e52cc0b1632808742019579f`; Table 6-1 p. 3 establishes pins; sections 11.1–11.3 and Figure 11-1 pp. 28–29 establish layout and ground/sense requirements. |
| [Evaluation-board guide](https://www.ti.com/lit/pdf/SLVU437) | SLVU437B Rev B, June 2021; SHA-256 `b8e09708c6e866ee1c7f99993dd430967e1b3d1055678873452f3af0d8402237`; section 4 pp. 16–18 gives layout context, section 5 pp. 19–20 the circuit/BOM. |

Downloaded documents remain in ignored `cache/ti/tps62130a-layout/`. The official
SLVC394 ZIP short/direct URLs returned HTTP 401 on 2026-10-06. No archive or
Gerber entry was consumed, so there is no extracted-CAD claim or invented hash.

This authored adaptation uses a Coilcraft XAL4020-222MEC, two 0805 output
capacitors and a six-layer board. The output-capacitor arrangement, wide explicit
tracks, via banks and layer assignment differ from the TI drawings. No local
pours are approximated by a thin trace. The IC lands and short pin necks feed
0.8 mm power trunks; their electrical adequacy still requires application review.
Every VIN/VOUT segment, including AVIN, VOS, divider pick-up and the always-on
EN branch, is at least 0.25 mm wide to satisfy 0.25 mm rail routing rules. The
bounded fixtures enforce those same rail widths during materialization and routing.

AGND, PGND and all thermal-pad lands connect to one local ground system. Every
required SW and PVIN contact is individually routed. SW stays on F.Cu without
vias. VOS and the divider's output pick-up use a separate fixed In2.Cu path to
C_OUT1, with In1.Cu GND retained above it. Four 0.45/0.20 mm filled-capped thermal
vias sit inside EP. The regulator PG land remains present and unconnected.

C_PVIN is 0.6 mm closer to U than in the initial adaptation. Its individual GND
via is now on the IC-facing side of the capacitor, 1.10 mm from the GND pad and
3.05 mm from the nearest EP thermal via. The explicit B.Cu return for each local
GND via ends at its nearest EP via; the C_OUT1 and C_OUT2 return spokes are
5.11 and 9.75 mm respectively. These remain provisional drawn conductors, not
measured switching-current paths. A proposed move of C_OUT1 below the inductor
shortened VOS but lengthened the divider pickup and output power path, so the
output-capacitor placement was retained.

## Geometry and integration

The anchor is U at `(0, 0)`; only front-side 0/90/180/270-degree rotations are
allowed. Component-local coordinates, tracks, vias, ports and keepouts rotate
together. The private envelope is x = −10.6…6.6 mm, y = −3.9…5.1 mm. Owner
lead-ins extend to ports outside it; total copper extent is about 17.2 × 11.2 mm.

| Port | Local position (mm) | Exposed layer | Intended entry |
| --- | --- | --- | --- |
| VIN | (6.1, −4.5) | F.Cu; paired through-via bank also reaches B.Cu | Input-capacitor side |
| VOUT | (−6, 6) | F.Cu; paired through-via bank also reaches B.Cu | Output-capacitor side |
| GND | (0, 6) | B.Cu; through via exposes all copper layers | Common return |
| EN, enabled variant only | (2, −4.5) | F.Cu | Logic-control side |

Protection on F.Cu/In2.Cu/B.Cu prevents later same-net shortcuts as well as
foreign routing. Separate fill exclusions on F.Cu/In2.Cu/In3.Cu/B.Cu stop power
pours bypassing local sensing. In1.Cu and In4.Cu GND remain available to the
ground/thermal vias. Rail pours should land at the exposed access banks; use
surface-zone stitching and independent native refill to prove connectivity.

Each instance requires an explicit `via_in_pad(BUCK_x/U.EP)` filled-capped
permission, the JLCPCB six-layer profile, and declared inner GND zones. The asset
finish field alone grants no process permission. A macro binds all private pads
on a rail to its single logical port; two physical power vias are compatible
with that one-port contract. No internal-pad groups waive power contacts.

The five footprint geometries are digest-bound in `generate_layout.py`. The
KiCad footprints used for initial validation came from package
`10.0.6~ubuntu24.04.1`; the inductor uses CopperLib's own Coilcraft footprint.
Managed URL aliases retain the exact geometry check. A different installed
footprint fails binding and requires reviewed regeneration rather than stretching.

## Provisional DC conductor budget

Use **0.5 A per output rail** as the conservative design ceiling of the
target design. The following estimates assume 35 µm outer-layer copper, 25 µm via barrel
plating, 0.30 mm finished drill, 1.6 mm board thickness and copper resistivity
`1.724e−8 Ω·m` at 20 °C. They are explicit calculation assumptions, not a measured
stackup or current/temperature rating. `R = ρL/(wt)` for tracks and
`R ≈ ρL/(πdt)` for plated barrels.

| Conductor | Estimated resistance |
| --- | --- |
| VIN port to C_PVIN, 6.45 mm of 0.8 mm copper | 3.97 mΩ |
| C_PVIN to PVIN merge, 0.97 mm of 0.8 mm copper | 0.60 mΩ |
| Each PVIN pin neck, 0.7875 mm of 0.25 mm copper | 1.55 mΩ; two contacts share current |
| SW merge to L, 1.665 mm of 0.8 mm copper | 1.03 mΩ; pin necks are additional |
| L output to C_OUT1, 4.135 mm of 0.8 mm copper | 2.55 mΩ |
| C_OUT1 regulated node to VOUT port, 3.034 mm of 0.8 mm copper | 1.87 mΩ |
| One full through-via barrel; two in parallel at each rail port | 1.17 mΩ; pair approximately 0.59 mΩ |

At 0.5 A, the regulated output node to its B.Cu access bank drops approximately
1.23 mV from these conductors. The explicit return from C_OUT1 through its access
via, the 0.8 mm B.Cu return and the external GND port adds about 5.3 mV under a
conservative two-full-barrel model; continuous inner planes add parallel paths
but are not credited in that number. Together this is about 6.5 mV before
external board distribution, contacts and temperature effects. It consumes part
of the provisional 12 mV / 18 mV / 33 mV rail distribution budgets, not the whole
budget. Raise resistance approximately 20% at 70 °C under a linear copper model.
The inductor, IC switches and transient/AC effects are excluded; these estimates
do not establish loop inductance, stability, efficiency or thermal margin.

## Reproduction and acceptance

From CopperLib, with the sibling CopperScript checkout available:

```sh
python packages/circuits/ti/tps62130a-buck/generate_layout.py
macro_trial_dir=$(mktemp -d)
PYTHONPATH=../CopperScript ../CopperScript/.venv/bin/python \
  packages/circuits/ti/tps62130a-buck/layout_trial.py \
  --enabled --rotation 90 --output-dir "$macro_trial_dir"
kicad-cli pcb drc --refill-zones --format json \
  -o "$macro_trial_dir/native-drc.json" "$macro_trial_dir/buck.kicad_pcb"
COPPERSCRIPT_SOURCE=../CopperScript ../CopperScript/.venv/bin/python \
  -m pytest tests/test_tps62130a_hard_macro.py
```

`layout_trial.py` invokes CopperScript APIs; it does not duplicate compiler code.
Its generic test terminals exercise external access. It writes only to the
selected probe directory. Keep probes outside the CopperLib checkout: generated
JSON under `work/` can otherwise enter a local dependency's content inventory.
The bounded acceptance suite checks both enable
variants and all four rotations, external routing with owner preservation,
native refill/connectivity, surface power landing, changed footprint/rail
rejection, disconnected internal SS copper, removed owner copper and same-net
intrusion. Native KiCad 10.0.6 accepts the eight rotated/variant external-access
fixtures with zero violations and zero unconnected items. Full-board placement,
current distribution, assembly and powered hardware validation remain separate.
