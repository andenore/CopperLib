# r78k

Exact reusable part interface and manufacturer package mapping for RECOM R-78K12-1.0 (12 V, 1 A non-isolated switching regulator, 15-36 V input, SIP3). Source: [R-78K-1.0 datasheet Rev. 6-2025](https://recom-power.com/pdf/Innoline/R-78K-1.0.pdf): p1 selection guide, p2 ratings and UVLO, p5 protections, p7 dimensions and pinning. The source identity is in `evidence/source.json`.

Pins: 1 +VIN, 2 GND, 3 +VOUT, left to right in the top view with the embossed logo face toward the viewer. The footprint puts the pin row 2.0 mm behind the logo face (local +y), the body extending 5.55 mm behind it; 1.1 mm drills take the 0.64 ± 0.1 mm square pins (0.74 mm maximum, 1.05 mm diagonal).

The module has continuous short-circuit protection with automatic recovery. The datasheet asks for a 27 µF electrolytic across the input for hard plugging above 18 V.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
