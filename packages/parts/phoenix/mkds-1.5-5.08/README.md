# mkds-1.5-5.08

Exact reusable part interface for Phoenix Contact 1715721, MKDS 1,5/ 2-5,08 (2-position screw terminal, 5.08 mm pitch). Source: [Phoenix catalog PDF for 1715721: pitch 5.08 mm, 1.3 mm hole, 0.9 x 0.9 mm pins, 17.5 A / 400 V nominal, drilling plan](https://www.phoenixcontact.com/us/products/1715721/pdf). Phoenix generates this PDF on request with a timestamp, so the SHA-256 in `evidence/source.json` identifies the 2 November 2026 copy only.

`footprints/Phoenix_MKDS_1_5_2_5_08.kicad_mod` follows the drilling plan: 1.3 mm drill at 5.08 mm pitch, 2.6 mm pads, body 10.16 mm wide by 9.8 mm deep with the pin row 4.6 mm behind the wire-entry face (local +y). Pad, body and courtyard coordinates match KiCad's TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal; it is authored here because that library footprint uses legacy angle-based arcs. P1 and P2 use the same 5.08 mm spacing as the Kefa KF128 view, but the body outline differs.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
