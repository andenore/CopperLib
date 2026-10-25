# SN74CB3Q3306ADCUR

Reusable TI dual bidirectional FET switch, DCU VSSOP-8. Exact pin map and
power-off behavior: SCDS113F (September 2026), pages 1 and 3. Download SHA-256
is in part.copper; ignored cache/ti/sn74cb3q3306a holds the source PDF.

A1/B1 and A2/B2 connect only while their respective active-low OE is low.
The definition uses passive pins because these are conditional conductive
paths, not logic drivers. ERC does not model the switched connection or prove
power-sequencing isolation. There are no permanent internal pad joins.

Supply VCC at 2.3 V to 3.6 V. Put a local bypass between VCC and GND, tagged
against VCC. Pull each OE to VCC to maintain isolation during power transitions
(TI p1). Ioff and power-off isolation are specified; this is not galvanic
isolation. The host must control enable safely, avoid competing drivers and
verify signal integrity and all independently powered states. No universal
signal rate or trace-length qualification is implied.

Use KiCad Package_SO:VSSOP-8_2.3x2mm_P0.5mm (TI DCU0008A, 0.5 mm pitch).
JLCPCB C2653266 lists SN74CB3Q3306ADCUR in VSSOP-8 for assembly; the live
2026-10-23 listing returned 69 stock units and 28 presale units. Recheck before
ordering; no stock reserved. No production qualification is claimed.
