# LSM6DSOXTR Mode 1 integration

This definition covers the exact ST LSM6DSOXTR LGA-14 part in Mode 1 I2C use.
DS12814 Rev 4 (June 2024), Table 1 supplies pin identities, Table 3 operating
supplies, section 7.1 straps/bypasses, Figure 28 the 3.0 x 2.5 mm package and
0.86 mm maximum height. Source: https://www.st.com/resource/en/datasheet/lsm6dsox.pdf

VDD needs 1.71–3.6 V and VDDIO 1.62–3.6 V. Place one 100 nF bypass at each.
Tie CS to VDDIO for I2C, SA0 to a defined level (low selects 0x6A), SDx/SCx to
GND or VDDIO. Leave pin 10 electrically open; pin 11 can be open or VDDIO.
Unused interrupts may remain open. This subset does not advertise auxiliary
SPI, sensor hub or SPI-mode electrical direction contracts.

The package-local managed footprint uses 14 equal rectangular lands: pins 1–4
left, 5–7 bottom, 8–11 right, 12–14 top in top view. DS12814 Figure 28 gives
nominal 0.475 x 0.25 mm terminals and 0.5 mm pitch. TN0018 Rev 8 section 3.7
adds 0.1 mm to both dimensions for nominal terminal spacing above 0.2 mm,
giving 0.575 x 0.35 mm copper. Explicit mask apertures are 0.675 x 0.45 mm;
explicit paste apertures are 0.5175 x 0.315 mm (81% area), within section 3.3's
70–90% recommendation. This avoids unsupported custom-pad primitives or
fabrication modifiers without discarding mask/stencil requirements.

The terminal-width upper tolerance reaches 0.3 mm (0.2 mm spacing); the land
choice uses the nominal drawing dimensions. Factory tolerance/stencil review
remains required. Top-side copper pour and vias are excluded under the body;
the central region also excludes tracks. Route all pin escapes outward and
review the remaining perimeter strip for unrelated top-side tracks. Pads use
zone_connect=0 so ground must reach them through traces, per TN0018 section 3.8.

ST recommends 90–150 µm stencil thickness and balanced connections; assembly
process and sensor performance remain unqualified. Source:
https://www.st.com/resource/en/technical_note/CD00134799.pdf

Consumer owns orientation-to-enclosure transforms, mechanical stress isolation,
bus pullups, driver configuration and measurement qualification.
