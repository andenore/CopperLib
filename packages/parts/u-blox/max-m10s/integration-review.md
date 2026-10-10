# MAX-M10S host integration obligations

Source: [u-blox integration manual](https://content.u-blox.com/sites/default/files/MAX-M10S_IntegrationManual_UBX-20053088.pdf),
UBX-20053088 **R05, 28-Apr-2026**, 102 pages, applicable to MAX-M10S-00B-01.
Reviewed cached PDF SHA-256:
`5a7510ef84f7e2757c57e362a25e3c16bcf8c80af5a4f70790c2e51032dbcd13`.
Pages 80, 81, 94 and 95 were rendered and visually inspected, including the
antenna-bias schematic, grounding example and typical supply connections.

The module front end is internally matched to 50 ohms and includes a DC block,
notch filter, LNA and SAW filter (§4.3, p77). This establishes **integrated module
matching**, not antenna matching, host-feed impedance or cellular coexistence.
Do not automatically add a generic pi network to this port or assume no support
network is needed.

Consumer decisions required:

- Specify passive, board-biased active or externally powered active antenna.
  A board-biased antenna needs the supply injection/filter/current-limiting
  network described in §4.3.4, pp79–80; supervisor designs are conditional.
- For cellular coexistence, assess coupling/isolation against receiver immunity
  and decide whether external SAW rejection is needed (§4.3.2–3, pp78–79).
  Internal filtering does not settle this decision.
- Review short 50-ohm RF geometry with surrounding ground/vias, solid underlying
  ground and coplanar-waveguide guidance (§4.4, pp80–81). Review antenna spacing,
  digital noise and thermal proximity. Do not turn qualitative advice into an
  invented universal maximum feed length or via pitch.
- Ground below the module on top/second layers and review crossings and ground
  stubs; an adjacent-plane coverage test alone is insufficient (p81).
- Review ESD handling/protection for the chosen antenna interface (§5.1.1).
- For the typical 3.3 V arrangement, VCC/V_IO share supply and VIO_SEL is open
  (B.1, pp93–94). Active-antenna supply and gain configuration are conditional.

This is reusable source guidance, not a reviewed consumer design. Datasheet
provenance, actual antenna, filter/protection decisions, impedance and bench
evidence must still be closed in the consumer qualification plan. No pins,
footprint, values or approval flags are changed by this review.
