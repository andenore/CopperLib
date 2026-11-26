# SN74LVC1G11 DBV with local 0402 bypass

Bind `LVC1G11_0402_BYPASS` members `U` to SN74LVC1G11DBVR and `C` to its
100 nF 0402 bypass. Bind nets `SUPPLY` to VCC and `GROUND` to system ground.
The macro pins exact managed SOT-23-6 and C_0402_1005Metric footprints.
The host capacitor should retain `role = decoupling` and `decouples` pointing
to the IC's VCC pin. All four quarter-turn rotations are permitted.

U is the origin. C is at (3.5,0) mm, rotation zero. Its positive land is
1.8825 mm from U pin 5, inside a 2 mm consumer limit. The exact courtyards
have a 0.54 mm gap, including the usual additional 0.5 mm assembly spacing.
Owned 0.25 mm F.Cu copper connects U pin 5 directly to C positive; the supply
port is at C positive. C negative has a separate 0.25 mm lead to an owned
0.6 mm / 0.3 mm through via at (4.8,0) mm. A plane-return contract requires
the capacitor to reach consumer ground planes on In1.Cu/In2.Cu.
Approximate envelope, including that via, is 7.15 x 3.4 mm.

Only U pin 5 is bound. **The host still owns U pin 2 ground, every logic
signal, and the ground connection between IC and bypass via.** Provide a
short IC ground connection to continuous planes and review the complete
decoupling loop. The macro does not claim a self-contained ground loop.
No switch/load current may be deliberately routed through the bypass branch.

This is an authored adaptation of TI SCES487J p13, not manufacturer CAD.
Native fixture routing verifies local copper and both bypass supply paths;
it does not qualify whole-board supply integrity, EMI or assembly. See
`qualification.json` and `validation.json`; production qualification remains
false. The 2 mm limit is the consumer design criterion, not a universal
datasheet distance requirement. The part's source manifest retains the
exact primary PDF hash and pin-map evidence.
