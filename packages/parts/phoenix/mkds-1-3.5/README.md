# mkds-1-3.5

Exact reusable part interface for Phoenix Contact 1751248, MKDS 1/ 2-3,5 (2-position screw terminal, 3.5 mm pitch, horizontal wire entry). Source: [Phoenix catalog PDF for 1751248: 17.5 A / 200 V nominal, AWG 26-16 (0.14-1.5 mm2), body 7.5 x 7.3 mm, 8.5 mm installed height, 1.1 mm hole, drilling plan](https://www.phoenixcontact.com/us/products/1751248/pdf). Phoenix generates this PDF on request with a timestamp, so the SHA-256 in `evidence/source.json` identifies the 3 November 2026 copy only.

`footprints/Phoenix_MKDS_1_2_3_5.kicad_mod` follows the drilling plan: 1.1 mm drill at 3.5 mm pitch with the body 2.0 mm beyond each end pin, the pin row 3.6 mm behind the wire-entry face (local +y) and 3.7 mm from the back. Pads are authored 2.0 mm round (pin 1 square), the courtyard 0.5 mm beyond the body.

Both pins are typed power because the consumer assigns which side is supply and which is the switched return; the terminal itself is unpolarised.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
