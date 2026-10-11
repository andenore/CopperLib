# BQ24072T voltage-based battery temperature input

Export `BQ24072TRGTR`; JLCPCB lists exact part C129319 for SMT assembly.
This is not the non-T BQ24072: TS uses a VIN-referenced divider, its maximum
charge-regulation voltage is 4240 mV, and timer tolerance differs. Verify all
limits when substituting it. Listing is not live-stock or assembly approval.

`charging-limits.json` records source facts with integer units; unknown TS
leakage stays null. `qualification.json` requires independent evidence rather
than allowing an ideal divider calculation to approve a battery.

TI SLUS937C pp4-5 and appended RGT0016C confirm the same pin numbers/package
as the non-T variant. The KiCad land pattern is compatible in package size,
pitch and exposed pad, but differs from TI's example perimeter lands; final
stencil, thermal vias and assembly review remain required. VSS and EP both
need ground connections. Small-signal TS/programming returns must avoid load
current paths. Keep IN/BAT/OUT capacitors local per Figure37, with appropriately
sized power conductors and exposed-pad thermal copper/vias.

Use `packages/circuits/ti/bq24072t-ts-43k-39k` for a reusable conservative
starting network with a cell-mounted Semitec 103AT-2. The 100 kohm isolation
resistor follows Figure18/p26; it is not a substitute for protection of the
external harness. Neither this part nor that module provides cell protection.

Source: [TI datasheet](https://www.ti.com/lit/ds/symlink/bq24072t.pdf), SLUS937C,
SHA256 `6f09e139e13a7bca407b4e8608ed0c387e43ba8c1d3705b4f9872b82495ea71c`.
