# PH2 connector with local coil clamp

`COIL_CLAMP_PH2` owns three existing members: `J` is the reviewed JST
S2B-PH-SM4-TB header, `TVS` is SMBJ15A and `D` is B360A. Bind `PLUS` to coil
positive, `MINUS` to coil negative, `CLAMP` to their common cathodes and
`GROUND` to the connector mounting tabs. This preserves a series diode/TVS
flyback path from MINUS through D and reversed TVS to PLUS, independent of
the system ground. The copper-only common-cathode node has no external port.

J is the origin; TVS and D sit at (-2.6,-9.1) and (2.6,-9.1) mm, rotated
270 degrees. The connector mates toward local +Y; a whole-macro rotation of
270 degrees points the cable toward board -X. All clamp copper is 1 mm wide
on F.Cu with no vias. TVS-anode/J1 distance is about 4.40 mm and D-anode/J2
distance about 4.54 mm, satisfying a 5 mm host limit without crowding the
connector body. The aggregate footprint envelope is approximately 10 x 18 mm.
The host must reserve its actual mating plug, cable bend and strain relief
beyond the connector's local +Y edge; that volume is not in the macro.

This is an authored adaptation, not extracted manufacturer CAD. Sources are
the owning exact-part evidence for [JST PH](../../../parts/jst/ph-s2b-sm4/README.md),
[B360A](https://www.diodes.com/assets/Datasheets/ds13005.pdf) and
[SMBJ15A](https://www.vishay.com/docs/88392/smbj.pdf). Their current/pulse ratings
do not qualify this application. Verify conductor and connector capacity,
coil inductance, TVS energy/repetition, overshoot, FET SOA, cable current loop,
thermal behavior and actual current-decay timing before production.

