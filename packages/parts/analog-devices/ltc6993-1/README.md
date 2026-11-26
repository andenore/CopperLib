# LTC6993IS6-1#TRMPBF

Exact I-grade TSOT-23-6 rising-edge, non-retriggerable one-shot. The -2 variant
is retriggerable and cannot be substituted for an independent pulse limiter.
Package-owned footprint `footprints/ADI_S6_TSOT23_6.kicad_mod` is authored from
the S6 drawing on p26, not vendor CAD: 0.95 mm pitch, 1.22 x 0.62 mm pads,
centers at +/-1.31 mm, 1.40 mm inner gap and 3.84 mm outer span. Body outline,
courtyard and silkscreen are authored annotations. Assembly process and paste
apertures still require consumer review; no 3D body is supplied.

Use 100 nF directly between VPLUS and GND. SET requires a 50–800 kohm resistor
to ground. Width is `NDIV * RSET / 50 kohm * 1 us`. For NDIV >= 512, the
full-temperature IC error bound is +/-3%, excluding resistor error; the
headline +/-2.3% applies at 25 C. I-grade operation is -40 to +85 C.
Keep SET/DIV wiring short and away from switch nodes. DIV is a ratiometric
input: derive it from the same supply, preserve the required code window,
use divider parallel resistance <=500 kohm and avoid >100 pF DIV capacitance.
Resistor tolerance, temperature coefficient, leakage and noise require review.

DIV codes 0–7 select positive pulses; 8–15 select negative pulses. OUT is held
low during startup; positive-pulse mode remains low afterward. Trigger events
during startup are ignored. Startup time is typically 500 master periods;
this typical value is not a guaranteed maximum. Provide an independent startup
inhibit/default-off power switch. A continuous high trigger does not retrigger.
An external inhibit applied only after OUT does not cancel an internal pulse:
releasing that inhibit can expose the remainder of an already-running pulse.
Consumers must review arming, fault recovery and trigger sequencing explicitly.

This is a pin/timing definition, not an actuator safety qualification. Switch
turnoff delay, output polarity, current-decay time, fault latch behavior and
single failures remain consumer obligations. No RF matching is applicable.

Primary source: [ADI Rev F datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc6993-6993-1-6993-2-6993-3-6993-4.pdf),
pp2, 4–5, 12–15 and S6 package drawing. The official PDF was reviewed through
the web reader. Direct binary download has not completed, so its byte hash is
unresolved; no hash or production-qualified source capture is claimed.
