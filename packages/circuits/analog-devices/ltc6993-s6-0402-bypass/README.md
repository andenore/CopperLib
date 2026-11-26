# LTC6993 S6 with local 0402 bypass

Bind `LTC6993_S6_0402_BYPASS` members `U` to LTC6993IS6-1#TRMPBF and `C` to
its 100 nF 0402 bypass. Bind nets `SUPPLY` to VPLUS and `GROUND` to system
ground. The IC footprint is the package-owned ADI S6 land pattern; it is
not interchangeable with the managed generic SOT-23-6 footprint. The host
capacitor should retain `role = decoupling` and `decouples` pointing to
the IC's VPLUS pin. All four quarter-turn rotations are permitted.

U is the origin. C is at (3.65,0) mm, rotation zero. Its positive land is
1.86 mm from U pin 5, inside a 2 mm consumer limit. The exact courtyards
have a 0.54 mm gap, including the usual additional 0.5 mm assembly spacing.
Owned 0.25 mm F.Cu copper connects U pin 5 directly to C positive; the supply
port is at C positive. C negative has a separate 0.25 mm lead to an owned
0.6 mm / 0.3 mm through via at (4.95,0) mm. A plane-return contract requires
the capacitor to reach consumer ground planes on In1.Cu/In2.Cu.
Approximate envelope, including that via, is 7.45 x 3.5 mm.

Only U pin 5 is bound. **The host still owns U pin 2 ground, SET and DIV
resistors, trigger/output wiring, and the ground connection between IC and
bypass via.** Keep the complete ground loop short and review SET/DIV wiring
against switching interference. This does not qualify timing limits,
startup behavior, pulse sequencing or a safety cutoff.

This is an authored adaptation of LTC6993 Rev F, not manufacturer CAD.
Native fixture routing verifies local copper and both bypass supply paths;
it does not qualify whole-board supply integrity, EMI or assembly. See
`qualification.json` and `validation.json`; production qualification remains
false. The 2 mm limit is the consumer design criterion, not a universal
datasheet distance requirement. As recorded by the owning part, the primary
PDF was read but its binary hash is still unresolved; no hash is invented.
