# SN74LVC1G14DBVR

TI SCES218AA, October 2025, DBV five-pin SOT-23. The package pin map is
NC=1, A=2, GND=3, Y=4, VCC=5. The model conservatively leaves NC disconnected;
TI permits connection but does not require it. No RF matching network exists.

Use a local 100 nF supply bypass and review the managed SOT-23-5 lands against
the DBV drawing. Host owns routing, power sequencing and logic margins.
Schmitt hysteresis accepts slow/noisy signals; use supply-specific thresholds
from Table 5.5, not a generic CMOS threshold. Supply range is 1.65–5.5 V.
The maximum power-off Ioff is ±10 µA; external loads determine the unpowered
output voltage. Operation during the supply ramp is not established by the
Ioff specification at zero volts. This definition does not qualify a consumer
power-sequencing or fault-interlock design.

[TI datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf), source hash
`3d59568b16a2b7abb63d33ebe6f8ddd37e12dd3ca2616dd803872c509a583283`.

No production qualification, fitted-board test or supplier allocation is claimed.
