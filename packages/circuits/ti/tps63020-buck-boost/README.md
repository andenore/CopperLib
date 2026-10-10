# TPS63020 six-layer physical hard macros

Reusable **unqualified authored adaptations** for the TI DSJ TPS63020 with
Bourns SRP4020TA, one 0805 input capacitor, a local 0402 VINA capacitor,
three 0805 output capacitors and 0402 feedback resistors. These assets bind
explicit host circuit members; they do not select component ratings or replace
an electrical circuit. Use the existing TPS63020 and SRP4020TA part packages.

- `assets/tps63020-six-layer-always-on.json`: nine members, EN tied to VIN.
- `assets/tps63020-six-layer-enabled-series-feedback.json`: eleven members,
  external EN with pull-down and two series top feedback resistors.

The output voltage is determined by the host resistor values, not this geometry.
Check the full allowed output window, including resistor/reference tolerance,
line/load regulation, power-save offset, ripple and transient droop/overshoot.
SLVS916I p6 distinguishes PWM feedback limits from the upward power-save offset;
these macros tie PS_SYNC low. A nominal output matching a USB-detect or RF supply
range does not qualify the actual pin voltage. CopperScript provides the generic
`divider_voltage_window` static corner screen; dynamic and temperature margins
remain consumer simulation/bench obligations. Shutdown disconnects input from
load but does not establish guaranteed active discharge or a safe reset interval.
The v0.4 assets require CopperScript's scoped immutable track-width contracts.
These identify local control/sense/enable branches and individual pin entries
without lowering the host's distribution-width rule or fabrication minimum.
The enabled variant's `FB_SERIES` is a private intermediate feedback node.
Both variants require F.Cu/In1.Cu/In2.Cu/In3.Cu/In4.Cu/B.Cu, with continuous
GND host planes on In1.Cu and In4.Cu. They permit cardinal rotations only.
Bind VIN/VOUT (and enabled EN) through the declared external ports. Supply
all members with the exact footprint identities/digests; do not substitute
another inductor or package merely because its pad count matches.

Regenerate deterministically:

```sh
python packages/circuits/ti/tps63020-buck-boost/generate_layout.py
```

See [physical layout and evidence](physical-layout.md). Both assets deliberately
have `production_publishable=false`. Passing geometry checks does not qualify
current capacity, converter performance, EMI, thermal behavior or assembly.
