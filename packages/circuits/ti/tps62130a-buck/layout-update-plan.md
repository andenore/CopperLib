# TPS62130A buck hard-macro layout update plan

Status: in progress. This is a six-layer layout revision of the existing electrical
module, not a claim that the result reproduces TI CAD or is production qualified.
Keep `production_publishable = false` through geometric acceptance. The 3.3 V
instance uses the always-on asset; the 1.8 V and 1.2 V instances share the
enabled asset. All three have the same local power-stage geometry. CopperVigo's
design-current target is below 0.5 A per output rail; DC current alone does not
bound the switching-loop or transient requirements.

## Evidence and baseline

- Use the pinned TPS62130A datasheet SLVSAG7F, section 11 and Figure 11-1, and
  EVM guide SLVU437B, section 4, as the layout comparison. Record separately
  which geometry is source-derived and which is an adaptation for the XAL4020,
  two output capacitors and the CopperVigo six-layer stack.
- Preserve the accepted CopperVigo route at
  `build/runs/20261007T210041Z-route/native-refill/board.kicad_pcb` as the
  baseline. Its zero KiCad DRC violations and opens establish connectivity and
  clearance only. Save cropped F.Cu, In1.Cu, In2.Cu and B.Cu plots for each
  regulator, alongside Figure 11-1 and the EVM top-layer drawing.
- Baseline local geometry, measured from `generate_layout.py`: the C_PVIN,
  C_OUT1 and C_OUT2 explicit ground-via-to-EP B.Cu spokes were approximately
  5.73, 5.59 and 10.48 mm. The drawn VOS connection from U.14 to C_OUT1.1 is about
  11.36 mm; its In2.Cu diagonal projects across the SW fanout vicinity. The
  SW merge-to-inductor section is about 1.67 mm, 0.8 mm wide and via-free.
  The inner GND plane offers parallel returns, so spoke length is a geometry
  warning rather than a measured current path. Recalculate the figures from
  each candidate's resolved footprint geometry.

## Progress, 2026-10-08

- Added a reusable CopperLib review checklist and linked it from the TPS62130A
  and Nordic RF physical-layout documentation. It recommends reference-layout
  hard macros for noise-generating and noise-sensitive circuits.
- Moved C_PVIN 0.6 mm toward U and placed its dedicated GND via on the IC-facing
  side. The C_PVIN VIN pad to U.12 center distance is 1.75 mm, its GND pad to via
  is 1.10 mm, and the via to its nearest EP thermal via is 3.05 mm. Choosing the
  nearest EP thermal via for each explicit B.Cu return reduces the C_OUT1 and
  C_OUT2 spokes to 5.11 and 9.75 mm without changing their capacitor positions.
- Tested moving C_OUT1 below the inductor in a disposable fixture. It shortened
  the VOS path but lengthened the divider pickup and output power trunk, so this
  candidate was rejected. The output loop, quiet-sense corridor and proposed
  v0.2 copper/plane-return support remain open.
- Both generated enable variants pass the isolated four-rotation native KiCad
  refill/DRC trial. In a disposable CopperVigo copy with a local dependency
  lock, ERC passes but `plan-layout` with one or three candidates finds no legal
  placement: `R_VDUT_BOT` is 12.58 mm from `U_MCU` against a 4 mm maximum.
  The original locked macro produces a legal one-candidate placement with the
  same board and compiler. Investigate this placement-search regression before
  changing CopperVigo's pinned scenes/lock or running a full route. This is a
  host-board integration failure, not evidence of a regulator copper DRC fault.
  Full-board routing and qualification remain pending.

## 1. Redraw the power stage around current loops

Work in the CopperLib generator and a disposable isolated trial first, leaving
the electrical module and CopperVigo placements unchanged. Keep all required
SW/PVIN/ground contacts and the four explicitly permitted filled/capped EP vias.

1. Bring C_PVIN's VIN and GND lands closer to the PVIN/PGND side of U. Place
   its dedicated ground via on the IC-facing side where clearance and assembly
   rules allow, then compare the complete input-capacitor/PVIN/EP loop against
   the baseline. Do not optimize pad-to-via distance alone while sending the
   via farther from the IC.
2. Place C_OUT1 as the primary switching-output capacitor beside the inductor
   and the IC return. Give its GND land its own short plane contact. Move
   C_OUT2 closer if feasible, but treat it as additional output storage rather
   than letting it determine the primary high-frequency loop.
3. Keep the SW connection on F.Cu, wide, short and via-free. Limit its copper
   area; do not create a broad SW pour merely to resemble the reference image.
   Retain individual legal necks from U.1/U.2/U.3 and U.11/U.12.
4. Replace avoidable zigzags and abrupt narrow-to-wide transitions after the
   component/loop geometry is settled. A 45-degree appearance is not an
   electrical acceptance criterion; short loops, legal copper width and
   clearance are.

Record per candidate the resolved component/pad coordinates, pad-to-via
distances, VIN/PVIN and L/C_OUT1 conductor lengths, return-via-to-EP distances,
SW extent and the relevant loop envelopes. Require an improvement in the
primary input/output paths without worsening the SW route or violating DRC.
If the desired broad local VIN, VOUT or GND copper cannot be represented
honestly by the v0.1 track/via asset, use phase 3 instead of imitating a pour
with many overlapping tracks.

## 2. Rework sensing and quiet support

- Connect VOS to the regulated node at C_OUT1 through the shortest legal quiet
  corridor that remains separate from the load-current path. Compare length
  and projected proximity to SW against the 11.36 mm baseline. If In2.Cu is
  retained, inspect the actual refilled In1.Cu GND shield along the whole path;
  a declared zone outline is not shielding evidence.
- Keep the FB divider close to U.5 and AGND, with its top pick-up at C_OUT1
  and its bottom return away from the switching-current return. Keep C_AVIN
  and C_SS close to their pins with individual ground contacts.
- Review the always-on EN-to-VIN branch separately from the power paths; it
  should not force a detour in C_PVIN placement. The enabled variant must keep
  its distinct EN port.

## 3. Add only the hard-macro support this layout proves necessary

The v0.1 macro asset contains immutable tracks/vias, ports and all-net zone
exclusions, but no macro-owned copper areas. Its pre-fill continuity proof
requires every private GND pad to reach a single explicit GND port. This is
why the current asset includes long B.Cu spokes even though CopperVigo has
In1.Cu and In4.Cu GND planes. Solve these as two bounded compiler features:

1. **Owned local copper areas.** Prefer the existing typed `CopperZone` model
   for local F.Cu VIN, VOUT and GND intent, with solid pad connections and
   explicit outline, priority, clearance and minimum width. Bind each zone's
   net, layers, geometry and owner to the asset digest and rigid transform.
   Reject a host-board zone that overlaps the private area on the same layer
   unless the export/fill semantics demonstrably preserve the intended owner
   shape. Keep the SW and quiet-sense corridors excluded. If KiCad zones cannot
   provide this owner isolation, design a fixed netted copper-area primitive
   instead; do not silently weaken the private-region contract.
2. **Plane-backed return proof.** Permit an explicitly declared private GND
   group to have separate pad-to-local-via roots before fill. Require a
   dedicated nearby contact for each capacitor GND land and direct, reviewed
   AGND/PGND-to-EP connections; every contact must reach the named GND plane.
   Mark the group pending, never connected merely because the zone outline exists.
   Independent native refill plus filled-copper connectivity must prove every
   pad/via reaches the declared plane and GND boundary. A missing/isolated
   plane, a lost local via, a wrong-net plane or any native open fails the
   complete route. Only then remove redundant B.Cu spokes from the regulator.

Make this a new explicit schema version; keep v0.1 assets and their existing
pre-fill proof unchanged. Preserve ownership through placement transforms,
routing, source recovery, KiCad export, native refill, board fingerprints and
manufacturing staging. Add synthetic negative tests before using either feature
in CopperLib. If the feature work is deferred, phase 1 can still improve the
macro using legal tracks/vias, but retain the current explicit GND proof and
label the copper-area/return limitations as unresolved.

## 4. Integrate and verify

1. Regenerate both deterministic CopperLib assets and update their package
   documentation. Rebind the three CopperVigo scenes with new SHA-256 values
   and refresh the locked dependency inventory. Never change an asset under an
   old digest or stretch a footprint to make it fit.
2. Run both enable variants at 0/90/180/270 degrees in the isolated trial.
   Require unchanged electrical pad roles, all required contacts, no SW via,
   immutable owner geometry, legal via process, zero native KiCad DRC
   violations and zero unconnected items after independent refill. Add
   targeted assertions for the measured loop/sense geometry and for absent
   or interrupted plane returns; current tests cover connectivity and width
   but do not bound switching-loop shape.
3. Route the complete CopperVigo board with all three instances and refill it
   independently. Require zero opens/violations, no hard-macro intrusion, the
   declared GND/VIN/VOUT zone contacts present, and no regression in CSI-2
   routing/reference planes. Compare per-layer regulator plots and the
   geometric metrics with the saved baseline. Inspect actual filled polygons,
   not only zone outlines.
4. Select real capacitor part numbers and verify effective capacitance under
   DC bias, voltage/temperature ratings, thermal-via assembly and the actual
   stackup. Bench-check regulation/transients, temperature and conducted/
   radiated noise before proposing a separate production-qualification path.
   The current compiler deliberately rejects `production_publishable = true`;
   these results cannot be inferred from DRC or the TI artwork.

## Reusable CopperLib and CopperScript guidance

- Add a short CopperLib hard-macro review checklist: authoritative source and
  exact revision/hash; extracted versus adapted geometry; pin and land mapping;
  switching/current-loop and quiet-sense paths; ground via/plane intent;
  exact component ratings; stackup/process assumptions; side-by-side layer
  images; native fill/DRC; unresolved electrical, thermal, EMI and assembly
  evidence. Link it from each physical-layout document.
- Extend CopperScript's `docs/physical-hard-macros.md` to distinguish
  **explicit pre-fill copper continuity** from **declared, pending plane-backed
  continuity** once the latter is implemented. Document macro-owned-zone
  collision/ownership rules and the native evidence required to close pending
  contacts. The current fail-closed wording is correct for v0.1 and should
  remain until the feature exists.
- Keep geometry-performance assertions local to this TPS62130A generator
  first. Extract a generic loop/sense audit helper only after another real
  CopperLib macro needs the same computation. Do not add a blanket
  angle-smoothing rule to the general router for this problem.
