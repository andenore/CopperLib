# SN74CB3T3306DCUR

Reusable TI dual bidirectional FET switch with voltage translation, DCU
VSSOP-8. Exact pin map and power-off behavior: SCDS119C (December 2015),
pages 1 and 3. Download SHA-256 is in part.copper.

Pin-for-pin with SN74CB3Q3306ADCUR (1OE, 1A, 1B, GND, 2A, 2B, 2OE, VCC) and
the same active-low OE. Unlike the CB3Q, the CB3T output level tracks VCC:
inputs above VCC pass as roughly VCC-level outputs. That suits 3.3 V on both
sides; check the actual signal levels for anything else.

A1/B1 and A2/B2 connect only while their OE is low. The definition uses
passive pins because these are conditional conductive paths, not logic
drivers. Supply VCC at 2.3 V to 3.6 V with a local bypass tagged against VCC.
Ioff supports partial power down; this is not galvanic isolation. The host
must control enable safely and verify every independently powered state.
No production qualification is claimed.
