# JST S6B-XH-A side-entry six-circuit header

Canonical physical connector; application signal assignments belong to the board.
Uses the consumer's managed KiCad Connector_JST footprint, without local KiCad
or a copied footprint. Select S6B-XH-A, not the shorter S6B-XH-A-1 variant.

Manufacturer facts from the JST XH catalogue (SHA-256 in part.copper), visually
checked on 2026-11-22:

- Six circuits, 2.5 mm pitch, 12.5 mm first-to-last pin span.
- Header width17.4 mm; height6.1 mm above PCB; nominal1.6 mm PCB.
- Side-entry C dimension9.2 mm for S6B-XH-A (7.6 mm is the -1 variant).
- Mate XHP-6 housing: width17.3 mm, depth7.5 mm, thickness5.7 mm (p4).
- Mated assembly overall length14.3 mm along mating axis (p2); wiring exits
  parallel to PCB. This length excludes cable bend allowance.
- SXH-001T-P0.6 contact accepts AWG28–22, insulation OD0.9–1.9 mm (p3).
  SXH-002T-P0.6 is an alternate for AWG30–26/OD0.9–1.3 mm. Match selected wire
  and manufacturer crimp tooling; do not infer cable rating from connector3A.
- SXH-001T-P0.6N is low insertion force and explicitly less vibration resistant;
  prefer ordinary SXH-001T-P0.6 for this recoil-equipped enclosure.

Managed footprint coordinates at front-side rotation0: pin1 at(0,0), pin6
at(12.5,0), mating direction+Y. BodyX[-2.45,14.95],Y[-2.3,9.2]; courtyard
X[-2.95,15.45],Y[-2.8,9.7]. The mated housing reaches nominalY12.0 relative
pin-row origin (14.3 minus rear2.3); no wire service loop included. An application
assembly-access rectangle can reserve X[-3,15.5],Y[9.2,19.2] for mate and initial
wire turn, but this10 mm allowance is a packaging choice, not a JST bend-radius
specification. Check the selected cable and insertion/removal access in3D.

No prototype crimp, mating-force or enclosure-clearance qualification is claimed.
No sensor/camera or battery pinout is implied by this reusable part definition.
