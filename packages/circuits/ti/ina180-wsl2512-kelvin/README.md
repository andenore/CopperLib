# INA180 / WSL2512 local Kelvin layout

`INA180_WSL2512_KELVIN` fixes three existing electrical members: `R` is
WSL2512R0500FEA, `U` is INA180A1IDBVR, and `C` is its 100 nF 0402 bypass.
Bind nets `HIGH`, `GROUND`, `SUPPLY`, `OUT` to shunt high, shunt low/system
ground, amplifier supply and amplifier output respectively. It changes no
electrical topology. The macro requires four copper layers and permits quarter
turns. Approximate envelope is 10 x 8.4 mm including power-entry copper.

The shunt anchor is (0,0); U is (0,-4.1) mm and C is (3.25,-5.5) mm.
Opposite, separate 1 mm power entries feed the outer shunt lands. Matched
0.18 mm sensing traces leave the inner top of each land for the input pair.
The amplifier and bypass ground share the quiet negative-sense branch. Host
power wiring must attach at the HIGH port and outer ground-via bank; no load or plane
current may be intentionally routed through either narrow sensing trace.
Review filled copper and via stitching to preserve that arrangement.
Two owned 0.6 mm / 0.3 mm through vias at (4.2,0) and (4.2,1) mm join the
1 mm outer ground entry to the consumer's In1/In2 ground planes. The explicit
plane-return contract requires all private ground pads to reach that bank; the consumer must provide
and verify the filled planes and their heavy battery-return connection.
The compact bank leaves 0.22 mm between each via's copper edge and the
shunt land's outer edge at x=3.68 mm; the drilled holes are outside the land.

Geometry explains the necessary proximity limit. The exact shunt courtyard
extends 2.09 mm toward U and the SOT-23 courtyard extends 1.7 mm toward R.
The 4.1 mm separation leaves 0.31 mm between those courtyards. Shunt land
centers are +/-2.855 mm; amplifier input centers are +/-1.1375 mm and 0.95 mm
toward R. Their pairwise straight distances are 3.588 mm, fitting a 3.6 mm
consumer limit. A symmetric 3 mm limit cannot fit these footprints even at
zero courtyard gap. These are footprint-derived dimensions, not a universal
electrical recommendation.

This authored adaptation follows [TI INA180 Rev H, section9.4 pp27–28](https://www.ti.com/lit/ds/symlink/ina180.pdf)
and the package-owned [Vishay WSL lands](../../../parts/vishay/wsl2512/README.md).
It is not vendor CAD. Two-terminal shunt pad/contact resistance, actual
current distribution, pulse ampacity, short-circuit SOA, thermal rise and
prototype calibration remain unqualified. The 1 mm conductor is a physical
design choice; it is not a proven 2 A or hard-short rating.
