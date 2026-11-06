# smbj30a

Exact reusable part interface and manufacturer package mapping for Littelfuse SMBJ30A (uni-directional 600 W TVS, DO-214AA/SMB). Source: [SMBJ series datasheet rev JC.07/04/25 v4: electrical table, physical specifications and solder pads](https://www.littelfuse.com/assetdocs/tvs-diodes-smbj-series-datasheet?assetguid=ba555e99-a12d-4f72-a0b6-86b06c67171e). The PDF was read through the manufacturer site; its identity is in `evidence/source.json`.

Pin 1 is the cathode (band) and pin 2 the anode, matching KiCad Diode_SMD:D_SMB. The anode pin is typed ground for an input clamp; use another definition when the anode is not at ground.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.
