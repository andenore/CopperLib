# Provisional six-layer physical macro

Review this adaptation against the [CopperLib hard-macro checklist](../../../../docs/hard-macro-review-checklist.md).

The two v0.3 JSON assets preserve nine component poses and their local copper for the
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
capacitors and a six-layer board. It follows the arrangement in datasheet
Figure 11-1: viewed at 180° in the probe, VIN and its input capacitor are to
the left of U; the inductor is to the right with SW above VOUT; C_OUT1 is below
and between U and L; and the second output capacitor extends the VOUT edge.
Three fixed, netted F.Cu polygons form the broad VIN and VOUT lobes and the
bounded SW island. The VOUT lobe contacts the inductor's lower land, both output
capacitors and the side access lead. Two locked F.Cu GND zones form the lower
return field and the exposed-pad area. The lower field extends well below the
output capacitors; every capacitor also retains its own nearby GND via.

The extra capacitor, larger inductor, side via banks and layer assignment are
adaptations, not literal TI geometry. The XAL4020 courtyard forces more space
between U and L than in the drawing, so the SW polygon has a narrow contoured
neck; it remains local and has no SW via or broad SW pour. The IC lands and short
pin necks feed the polygons and 0.8 mm access tracks. Their electrical adequacy
still requires application review. Every VIN/VOUT track, including AVIN, VOS,
divider pick-up and the always-on EN branch, is at least 0.25 mm wide to
satisfy the rail routing rules.

AGND, PGND and all thermal-pad lands connect directly to the EP region. Every
required SW and PVIN contact is individually routed. SW stays on F.Cu without
vias. VOS and the divider's output pick-up use a separate fixed In2.Cu path to
C_OUT1, with In1.Cu GND retained above it. Four 0.45/0.20 mm filled-capped thermal
vias sit inside EP. The regulator PG land remains present and unconnected.

C_PVIN's individual GND via is on the IC-facing side of the capacitor, 1.10 mm
from its GND pad and 3.05 mm from the nearest EP thermal via. Every capacitor
ground has its own nearby through via; none shares another component's return
contact. The former long B.Cu spokes to EP remain removed. Their continuity
depends on actual filled In1.Cu/In4.Cu GND planes. C_OUT1's power land is the
quiet VOS/divider pickup point on shielded In2.Cu, separate from the SW island.

## Geometry and integration

The anchor is U at `(0, 0)`; only front-side 0/90/180/270-degree rotations are
allowed. Component-local coordinates, tracks, vias, ports, polygons, zones and
keepouts rotate together. The private envelope is x = −10.6…6.6 mm,
y = −6…5.1 mm. Side access and the enabled EN lead extend to ports outside it;
the power-port span is 18.4 mm.

| Port | Local position (mm) | Exposed layer | Intended entry |
| --- | --- | --- | --- |
| VIN | (7.2, −0.95) | F.Cu; paired through-via bank also reaches B.Cu | Input side |
| VOUT | (−11.2, 0) | F.Cu; paired through-via bank also reaches B.Cu | Output side |
| EN, enabled variant only | (2, −6.5) | F.Cu | Logic-control side |

Protection on F.Cu/In2.Cu/B.Cu prevents later same-net shortcuts as well as
foreign routing. Fill exclusions on In2.Cu/In3.Cu/B.Cu keep host pours out of
the quiet-sense and lower-layer corridors. On F.Cu, host zones overlapping the
private region are rejected so the two owned zones can fill as drawn. In1.Cu
and In4.Cu GND planes contact the individual ground/thermal vias. Native refill
and zero unconnected items are required to prove those plane-backed returns;
an unfilled zone outline is not accepted as a connection. A board may
explicitly set `allow_same_net_hard_macro_overlap = true` on a same-net F.Cu
GND zone to let its native fill connect to these local GND zones; the macro's
B.Cu/In2.Cu/In3.Cu fill exclusions and all foreign-net clearances remain active.

`required_layers` names the six-layer stackup contract; it does not reserve
every layer beneath the macro. The macro permits tracks beneath its envelope
on In1.Cu, In3.Cu and In4.Cu. Its In3.Cu keepout excludes pours only. Vigo's
board-wide GND zones separately reserve In1.Cu and In4.Cu for plane return;
they are not hard-macro track keepouts. Through-vias still occupy their actual
six-layer spans and need normal copper clearance.

Each instance requires an explicit `via_in_pad(BUCK_x/U.EP)` filled-capped
permission, the JLCPCB six-layer profile, and declared inner GND zones. The asset
finish field alone grants no process permission. VIN and VOUT each have one
external logical port; GND uses the declared plane-return contract and has no
fictional pre-fill common port. No internal-pad groups waive power contacts.

The five footprint geometries are digest-bound in `generate_layout.py`. The
KiCad footprints used for initial validation came from package
`10.0.6~ubuntu24.04.1`; the inductor uses CopperLib's own Coilcraft footprint.
Managed URL aliases retain the exact geometry check. A different installed
footprint fails binding and requires reviewed regeneration rather than stretching.

## Conductor budget still needed

The target is below **0.5 A per output rail**. The old trace-only DC resistance
table no longer models the filled local copper and plane returns, so it has
been withdrawn. Extract the actual filled copper, stackup and via plating to
recalculate DC drop and current density; then review switching-loop inductance,
stability, temperature and EMI. Native DRC cannot establish these quantities.

## Reproduction and acceptance

For the minimal one-regulator inspection board, from CopperScript with a sibling
CopperLib checkout:

```sh
.venv/bin/python -m examples.tps62130a_macro.trial
```

For all rotation and external-access checks, from CopperLib:

```sh
../CopperScript/.venv/bin/python packages/circuits/ti/tps62130a-buck/generate_layout.py
PYTHONPATH=../CopperScript ../CopperScript/.venv/bin/python \
  -m pytest tests/test_tps62130a_hard_macro.py
```

`layout_trial.py` invokes CopperScript APIs; it does not duplicate compiler code.
Its generic test terminals exercise external access. It writes only to the
selected probe directory. Keep probes outside the CopperLib checkout: generated
JSON under `work/` can otherwise enter a local dependency's content inventory.
The bounded acceptance suite checks both enable
variants and all four rotations, external routing with owner preservation,
native refill/connectivity including both filled owner zones and all three
fixed polygons, surface power landing, a missing dedicated GND via, changed footprint/rail rejection,
disconnected internal SS copper, removed owner copper and same-net intrusion.
Native KiCad 10.0.6 accepts the eight rotated/variant external-access
fixtures with zero violations and zero unconnected items. Full-board placement,
current distribution, assembly and powered hardware validation remain separate.
