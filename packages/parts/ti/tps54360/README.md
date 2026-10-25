# tps54360

Exact reusable part interface and manufacturer package mapping. Source: [SLVSBB4G pins p4; DDA exposed-pad package addendum; six physical thermal drill lands retained](https://www.ti.com/lit/ds/symlink/tps54360.pdf). The source identity is in `evidence/source.json`; downloaded PDFs are in ignored `cache/organ-reva/`.

Use the exact named orderable part. Ratings and topology remain subject to the manufacturer operating conditions. This addition establishes pin/package source facts, not current capacity, thermal, transient, EMC, assembly or hardware qualification. The consumer owns operating conditions and procurement selection.

The pinned KiCad thermal-via footprint retains six 0.2 mm drilled contacts and the top exposed land/paste geometry. Its bottom-only copper rectangle was removed because CopperScript cannot import that bare SMD layer combination; the consumer must provide a bottom GND heat-spreading pour and independently verify the six drill contacts after export. This is a declared footprint adaptation, not an internal connection exemption.

The converter needs the complete input bypass, bootstrap, catch diode, inductor, output capacitors, compensation, feedback and RT network. Use the TPS54360EVM-182 schematic/layout (TI SLVU769B) as the reference. Local high-di/dt loop, switch-node area, thermal return and feedback isolation must be reviewed against that source; a freely placed IC alone is not a reusable power module. The current organ consumer uses fixed placement and routing-width constraints. It has no accepted immutable power macro or native current-path qualification yet.
