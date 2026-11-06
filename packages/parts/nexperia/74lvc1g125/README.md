# 74lvc1g125

Exact reusable part interface and manufacturer package mapping for Nexperia 74LVC1G125GW (TSSOP5, SOT353-1). Source: [74LVC1G125 rev. 17.1, Table 1 ordering, Table 3 pin description, Table 4 function table; IOFF supports partial power down](https://assets.nexperia.com/documents/data-sheet/74LVC1G125.pdf). The source identity is in `evidence/source.json`; the PDF was read through the manufacturer site and is not cached here.

Pin order matches the SOT-23-5 SN74LVC1G125DBVR (OE 1, A 2, GND 3, Y 4, VCC 5), but the land pattern is SOT-353/SC-70-5, so it is not a drop-in on a DBV footprint. onsemi NC7SZ125P5X uses the same land and pin order; it is a procurement alternative to check against its own datasheet, not part of this definition.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
