# AD7606C 18 serial interface view

Exact device: AD7606C-18BSTZ, LQFP-64 ST-64-2. The public export
AD7606C18BSTZ_SERIAL_EXTERNAL_REF fixes serial software mode and external
reference semantics. It must not be used as a parallel-mode or internal-reference
view. Source: Rev B Table 9 pages 15–17, Table 23 and Figure 123.

All 64 package contacts are represented separately. REGCAP 36 and 39 must
each receive their own 1 µF capacitor; never short the regulators together.
REFCAPA/B require an external connection and 10 µF capacitor; this is not an
internal electrical short. REFIN needs external 2.5 V and local 100 nF.
AVCC pins need individual 100 nF and source bulk capacitance.

The standard KiCad land pattern is a selected candidate, not manufacturer
assembly approval. Physical support placement, per-ground-pin vias, signal
return and source-backed macro remain pending. See the serial support circuit.
