# UCC27517DBVR with local 0402 bypass

Bind `UCC27517_DBV_0402_BYPASS` member `U` to UCC27517DBVR and `C` to a suitable
0402 bypass. Bind `SUPPLY` to VDD and `GROUND` to system ground.
Retain the capacitor's decoupling role and consumer positive-pad distance limit.
This macro requires F.Cu, In1.Cu, In2.Cu and B.Cu and permits quarter-turn rotations.

U is the origin with exact managed SOT-23-5 geometry. C is at
(-3.5, -0.95) mm, rotation 180 degrees. The positive-pad
distance is 1.8825 mm; the managed courtyards have a 0.54 mm gap.
Owned 0.25 mm F.Cu copper connects U pin 1 to C positive,
where the host supply port attaches. C negative reaches a separate
0.6/0.3 mm through via at (-4.8, -0.95) mm, with an inner-ground-plane return contract.

The host owns IC ground pin 2, all functional signals and the complete
IC-to-capacitor return loop. No other load or switch current may be deliberately
carried through these local bypass branches. Host must provide the additional bulk capacitor, short driver-ground/gate-current return, output/gate wiring and pulse-current, ripple, transient and thermal qualification.

This is authored geometry, not manufacturer CAD. The staged file is byte-identical
to the isolated fixture and current integration probe. Native review of the
retained fixture reports passes routing, requirements, filled DRC and all three
fixture surface bypasses. Its historical per-file input binding is incomplete;
see `validation.json`. A fresh source-bound consumer build is required before
claiming current integration acceptance. No production qualification is claimed.
Source locators and unresolved captures remain explicit in `qualification.json`
and `layout.copper`; the 2 mm limit is a consumer criterion, not a universal
manufacturer distance requirement.
