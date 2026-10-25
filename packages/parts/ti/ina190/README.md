# INA190 SC70 current-sense amplifiers

Import `github.com/andenore/CopperLib/packages/parts/ti/ina190`.
Exports: `INA190A1IDCKR` (25 V/V), `INA190A5IDCKR` (500 V/V),
and their shared `INA190_DIE`. These DCK variants have no ENABLE pin.

TI SBOS863D page 3 establishes the pin map:

| Pin | Name |
|---|---|
| 1 | REF |
| 2 | GND |
| 3 | VS |
| 4 | IN+ (INP) |
| 5 | IN− (INN) |
| 6 | OUT |

Consumers must supply 1.7–5.5 V, use a low-impedance REF source, and place
100 nF directly between VS and GND. Connect differential inputs to the shunt
with Kelvin tracks. Follow page 27, Figure 46 for the SC70 reference layout.
These physical requirements are documented obligations, not verified macros.
Standard footprint: `Package_TO_SOT_SMD:SOT-363_SC-70-6`; consumers declare and
lock their KiCad footprint provider.

[Source manifest](evidence/manifest.json) pins the original datasheet hash.
Download source bytes to ignored `cache/ina190/` at the repository root from
[TI](https://www.ti.com/lit/ds/symlink/ina190.pdf).
The component declarations were migrated unchanged from CopperBenchParts.

No production qualification is claimed. Supply ranges, gain, pin identity and
footprint mapping do not establish accuracy, leakage, thermal behavior, ADC
settling or layout correctness. The CopperBench consumer retains its TI model
wrappers and unresolved ngspice convergence/absolute-output failures; those
board-specific simulation artifacts are not part of this reusable package.
