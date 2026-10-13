# Taoglas FXUB16.07.0150AQ external LTE antenna

Reusable manufacturer facts for a passive cabled antenna, not a PCB-mounted
Copper part or a JLCPCB placement item. Consumers select this specification in
their external assembly manifest; do not add a fictional footprint or CPL row.

The [manufacturer specification](https://www.taoglas.com/datasheets/FXUB16.07.0150AQ.pdf)
is SPE-24-8-235-A, dated 2024-09-24. Relevant band, mounting, drawing and test
pages were rendered and inspected. Its hash and exact locators are in
`specification.json`; retain the PDF only in ignored cache.

Page 5 explicitly lists uplink/downlink coverage for LTE B1/B3/B7/B8/B20/B28,
and TDD B38/B40/B41. That is a suitable frequency-coverage candidate for these
EU bands, not approval for every EU allocation, operator or modem variant.
The factory assembly has a 150 mm, 1370 um diameter cable with MHF I/U.FL
compatible termination. Nominal input impedance is 50 ohm. Attach it to a
non-metal surface. Reserve 90400 by 15000 um for its body: the introduction
and drawing disagree slightly about length. Do not trim the cable.

The exact reference uses three cable directions and shows different efficiency
and return loss. It does not establish an installation-independent matching
guarantee, built-in TVS, required minimum metal spacing or minimum bend radius.
Keep those unknowns explicit; do not copy a different antenna's spacing rule.
Matching/ESD/DC-isolation adaptation, enclosure placement, certification gain
limits and RF/coexistence testing remain mandatory consumer obligations.

`qualification.json` keeps design, simulation and bench evidence separate.
This specification deliberately has `production_publishable=false`.
