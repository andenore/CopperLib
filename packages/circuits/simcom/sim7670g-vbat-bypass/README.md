# Conditional SIM7670G local VBAT bypass bank

Wraps the exact SIM7670G-LNGV part, preserving every supported external pin,
with the four ceramic values recommended by SIM7672X Hardware Design V1.01,
page 26, Figure 6. Applicability must be accepted by the consumer; this is not
manufacturer-confirmed equivalence. Source SHA256:
`bd198ceb5eecddbafd3d438782cf35c89208e40a8c4b3b1eb19097fdb363706d`.

The 3 mm pad-relative limits are authored implementation bounds for the guide's
"near VBAT" intent, not manufacturer maximums. Each capacitor has explicit
decoupling intent to a real VBAT pad, enabling CopperScript's direct surface
feed reservation. Ground contacts may use legal nearby return vias. All three
VBAT contacts still require external copper; none is internally exempted.

The host must connect every forwarded ground and power port and provide at
least 100 uF **effective** local reservoir capacitance. Nominal ceramic values
do not prove this. Select exact capacitors for voltage, tolerance, bias, RF
behavior and assembly; no generic supplier identity is assumed by the circuit.
The host owns high-current distribution (guide recommends at least 2 mm), pad
neckdowns, via arrays, ground return, transient and thermal verification.
Optional ferrite and surge protection require whole-supply review and are not
silently inserted. Preserve the part's RF/power qualification obligations.

This is a reusable electrical module, not an RF/power-qualified hard macro.
`production_publishable = false`.
The companion `qualification.json` retains mandatory power design, simulation
and bench evidence. Bind it alongside the underlying part's RF contract; it
does not replace RF matching, impedance or prototype requirements.
