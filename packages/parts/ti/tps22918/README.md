# TPS22918DBVR

Import `github.com/andenore/CopperLib/packages/parts/ti/tps22918`, symbol
`TPS22918DBVR`. Managed footprint: `Package_TO_SOT_SMD:SOT-23-6`.

Source: [TI SLVSD76C](https://www.ti.com/lit/ds/symlink/tps22918.pdf),
section 5, sections 6.3 and 8.3, sections 10-11 / Figure 32. Download SHA-256:
`1b28eb58003d28b18bf919a15734056f296a499bebee2bd493a1e4358c4dfb1c`.

Use a local 1 uF ceramic VIN bypass; tag its `role = decoupling` and
`decouples = "U.VIN"`. Drive ON explicitly, including reset. CT selects
rise time and may be open. QOD may connect to VOUT directly or through
a discharge resistor, or remain open. Neither auxiliary pin is a supply
source; the model marks these passive to avoid false driver conflicts.

This load switch is not an inductive-load driver or current-limiting eFuse.
Review capacitor inrush, reverse-current paths, thermal/current limits and
discharge energy for the chosen load. Compare physical implementation to
Figure 32; keep bypass and power paths compact. No numerical placement
distance is invented here. Managed generic footprint land-pattern comparison,
layout and bench validation remain host obligations. The package provides
electrical pin facts, not qualified copper.
