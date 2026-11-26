# SN74LVC1G11DBVR

TI three-input positive AND gate, DBV six-pin SOT-23. Supply 1.65–5.5 V;
inputs tolerate 5.5 V. Output is push-pull and must not be wired to another
push-pull output. Tie every unused input to a defined level. Use local 100 nF
supply bypass and inspect managed SOT-23-6 lands against DBV0006A.

This is not a Schmitt input. At VCC 3.0–3.6 V, VIH is 2.0 V minimum and VIL
0.8 V maximum; input transition rate is limited to 10 ns/V. Open-drain fault
lines with slow resistor pullups need a Schmitt buffer before this gate.
The Ioff +/-10 uA limit at VCC=0 does not guarantee a safe output throughout
the supply ramp. Use passive downstream default-off bias and a supervisor
where power sequencing matters. No RF matching is applicable.

Source: [TI SCES487J Rev J, November 2026](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf),
pp3–6 and 13, DBV drawing; SHA256
`05464c6cc1df6867150f87b4ce274f41f34e1f7135fc81174f5b9cef70e3d561`.
No host fault-interlock, assembly sourcing or prototype qualification is claimed.
