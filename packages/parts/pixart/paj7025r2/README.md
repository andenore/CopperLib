# PAJ7025R2 vertical camera module

Original CopperLib definition and carrier land pattern derived from manufacturer facts, not copied from an external PCB design. Manufacturer PDF SHA-256 is recorded in part.copper. Pinout p5 and outline p6 were visually inspected; p9 specifies 10uF + 100nF close to VDDMA, and both grounds14/20 connected. All unused GPIO, CP and LED pins are left floating.

The module has no ordinary horizontal SMT package. Place this canonical footprint on the BACK at rotation0: its X coordinates are pre-mirrored so CopperScript places the hand-solder lands on B.Cu while the physical camera body is above F.Cu. The generic generated 3D body will not represent that unusual mounting; use the mechanical model for fit. The footprint supplies the slot and locating holes; host must honor the remaining mechanical contract:

- Slot centred at footprint origin, total12.5x1.2mm, long axisX.
- Two unplated locating holes diameter0.95mm at(-5.475,-3),(5.475,-3).
- Nominal1.6mm carrier thickness. Tail extends2.6mm below seating shoulder, leaving1.0mm below board for solder access.
- Lens faces -Y, front face nominalY=-3.5; optical axis X=0 and Z=4mm above seating shoulder.
- Body12.2±0.2 wide,9.85±0.2 totalheight,4.00±0.15 depth; PCB1.00±0.10 thick. Finger pitch1.15±0.05 and width0.65±0.05. Locating post pitch10.95±0.07, diameter0.80±0.03.

The pad numbering is manufacturer front/back mapping: from above, rear +Y row1..10 goes-X to+X; front-Y row11..20 goes+X to-X. All solder lands are on the underside; no paste apertures. Lands are0.65x1.1mm centredY=±1.55, leaving0.4mm copper clearance to slot. Solder must bridge the module finger to the land. This is an explicit hand-assembly engineering choice; neither a manufacturer-recommended land pattern nor a solder-process qualification. No 3D STEP is asserted.

The published trzy/PixArt carrier was inspected to cross-check orientation only; its source was not copied (no repository license established). Slot, land clearance and holes still require a physical sample fit/solder coupon before fabrication release. The general datasheet is version1.1; confirm purchased sample revision matches it. No reflow process is established for the optical module.

The underside courtyard bounds solder access (X±6.6,Y±2.3), not the upright body above the board. Front-side component exclusion and the physical camera envelope are separate host/mechanical obligations.
