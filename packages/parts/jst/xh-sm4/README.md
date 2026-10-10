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
