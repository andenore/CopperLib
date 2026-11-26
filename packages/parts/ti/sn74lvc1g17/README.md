# SN74LVC1G17DBVR

Non-inverting Schmitt buffer, DBV five-pin SOT-23. Supply 1.65–5.5 V; input
range 0–5.5 V. Use the supply-specific positive/negative thresholds and
hysteresis in TI Table 5-1. Its Schmitt input supports slow resistor-pullup
fault signals before ordinary CMOS gates. Output is push-pull; do not join
it directly to open-drain fault sources.

Use local 100 nF VCC bypass; tie input to a defined level and conservatively
leave NC open. Review the managed SOT-23-5 lands against DBV0005A. Ioff at
VCC=0 does not establish safe output throughout the supply ramp; default-off
actuator bias and startup supervision remain host obligations. No RF matching
applies. Host routing, logic margins and prototype verification remain open.

Source: [TI SCES351Y Rev Y, October 2025](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf),
pp3, 5–7, 12, DBV drawing; SHA256
`ade19853307838593bd60d27ae4f6a026fc8a52935de8d5f487457b8214e050f`.
