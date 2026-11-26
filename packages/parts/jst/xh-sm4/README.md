# SMT XH headers and contextual interfaces

This package owns both three- and four-pin SMT XH footprints. The existing
`JST_S3B_XH_SM4_TB` export is a battery/NTC view: P1=power, P2=ground, P3=analog;
MP mounting tabs are grounded. This is a selected harness convention, not an
intrinsic connector pinout. Verify actual harness numbering/polarity.

The CAN and UART conventions live separately in `packages/interfaces/can/jst-xh3`
and `packages/interfaces/uart/jst-xh4`; they reference these same footprints
rather than duplicate them. CAN: 1 CANH, 2 CANL, 3 GND. UART: 1 VREF, 2 TX,
3 RX, 4 GND. Each view grounds its mounting tabs.

JST XH catalogue, SMT body drawing page 6:
https://www.jst-mfg.com/product/pdf/eng/eXH.pdf
SHA256 `9426b136902f11900825077535e5c65032b7fbc31ffb59c5e9e1f463bb20fb90`.
Land data: JLCEDA/EasyEDA Official Library, https://lceda.cn/ and
https://easyeda.com/, exact C161860/C161861 packages; UUIDs
`339b3d311e1c4b379b2d8061c2d7ac48` and `2e6c2e3d58c5466fb09fd1d264c24934`.
The four-pin pattern has larger tab lands. Retain these credits.

Body drawings were visually checked; exact manufacturer land-pattern and
assembly signoff remain pending. Do not substitute a through-hole XH footprint.

## Three-pin body registration review (2026-11-25)

The three-pin land sizes match the catalogue p3 recommendation: signal
1.3 x 4.5 mm and mounting 1.8 x 3.9 mm. The 6.5/11 mm longitudinal
dimensions start at the mounting-pad outer edge, not the dashed plastic edge.
The plastic mating face is 0.2 mm inward. A nominal datum at local y=5.35 mm
places mounting-pad centres at y=3.40 mm and signal centres at y=-3.40 mm;
retained supplier lands at +/-3.40868 mm differ by +/-0.00868 mm. The
nominal x centres are signals -2.5/0/2.5 and mounts +/-5.7 mm; retained
coordinates differ by at most 0.00064 mm. Catalogue dimensions are reference
values, not a complete tolerance or solder-process qualification.

The 12.5 x 7 mm body therefore spans local x[-6.25,6.25], y[-1.85,5.15].
F.Fab is registered to that envelope; pads, courtyard and footprint origin
are unchanged. The nominal body-envelope centre is (0,1.65), not the
footprint origin. The mated housing reaches y=7.95 (2.8 mm beyond the face,
from p3's 12.8-3-7 dimensions). Height 6 mm is an assembled reference;
wire-axis z, insertion service space and cable bend radius remain separate.
This review does not qualify the four-pin package's different mounting lands.

CPL exports use the footprint origin; changing F.Fab does not shift the
assembly coordinate. Do not assume the body-envelope centre or a copper
centroid is the supplier's pick datum. Review C161860's exact placement,
pin 1 and rotation in the assembler preview before release. This package
has no verified supplier-specific placement-offset contract. If origin
recentring becomes necessary, rebase all footprint geometry and compensate
consumer placements together, then regenerate and validate; do not just
move the component or manually edit a generated CPL.
