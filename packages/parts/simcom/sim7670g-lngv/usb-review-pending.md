# USB host obligations - exact-model confirmation pending

Related-family source: SIMCom-authored SIM7672X Series Hardware Design V1.01,
[retained mirror](https://files.waveshare.com/wiki/SIM7670G-LTE-Cat-1-GNSS-HAT/SIM7672X_Series_Hardware_Design_V1.01.pdf),
SHA-256 `bd198ceb5eecddbafd3d438782cf35c89208e40a8c4b3b1eb19097fdb363706d`.
This does **not** establish complete SIM7670G-LNGV applicability. Do not update
this part's electrical limits or add mandatory component values from this
document without exact-model confirmation.

## Consumer-authorized document assumptions

A consumer may explicitly accept this document's applicability as a design
assumption. Record that decision with the consumer; it is not manufacturer
confirmation and does not globally qualify this catalogue part. CopperAssetTracker
does so on 2026-10-10. Its design can proceed under that assumption while bench
qualification and unsupplied limits remain open.

Reusable source facts under **SIM7672X V1.01 applicability**:

- Table 17 (p36) / Table 51 (p61): pad 24 USB detection has a recommended range
  3.6-5.2 V, nominal 5.0 V. Table 50's -0.3 to 5.4 V is absolute maximum only.
- The input detects USB; it does not supply module charging or host power. A
  regulated shared VBAT rail is a possible design choice only if the actual
  detect pin remains within its own, stricter lower voltage bound. VBAT's 3.4 V
  minimum alone does not meet the 3.6 V USB bound.
- A shared switched rail avoids independently applying detect power while VBAT
  is absent, but does not by itself qualify host DP/DM power-off tolerance.
- Table 12/Figure 10 (p30): USB readiness delay is typical 470 ms, not a maximum
  or guaranteed firmware timeout. Table 13/Figure 11 (p31): shut down through
  PWRKEY/AT+CPOF before removing VBAT; power cycling requires VBAT below 1.3 V
  and at least 2 s off/on buffer. Verify actual discharge and readiness.
- Section 5.3.2 (p63): USB must be unplugged for the described sleep mode.
  Permanently asserting detect while VBAT remains enabled cannot be assumed to
  support that mode; separate attach control may be needed for low-power USB sleep.

The guide does not establish a USB-detect input-current maximum or complete
unpowered pin tolerance. Do not invent them or claim tested enumeration/data
transfer from a nominal supply connection. Rendered pages 30/31/36/61 and the
already reviewed USB reference schematic underpin these obligations.

Review triggers from the related guide:

- §3.4, p36: module is a USB peripheral, supports full/high-speed modes, and has
  a separate active-high USB detection input. Confirm the exact module's detect
  range and behaviour in every required power state; transceiver/module power
  alone is not proof of USB availability.
- Figure 17, p37, was rendered and visually inspected. It prescribes module-side
  series components, switchable short test branches, protection and ground-backed
  controlled-impedance routing. Verify which support topology applies to an
  internal host link versus an exposed connector, and retain the exact layout
  requirements. Do not blindly add generic ESD or resistors to a different model.
- Table 51, p61, distinguishes recommended USB_VBUS operation from absolute
  maximum ratings. An absolute maximum is not a usable operating threshold.

Consumers must confirm exact module/full-speed compatibility, firmware drivers,
VBUS/attach behaviour, support topology and reference layout. Apply the reusable
USB channel contract in addition to the module's RF/power obligations. Missing
manufacturer confirmation remains incomplete, not a passing design attestation.

## Supplier brief checked 2026-10-10

The exact C45935408 supplier-linked
[SIM7670X product brief](https://datasheet.lcsc.com/datasheet/pdf/ee03db1eecfc7b8f7e60fb0421704843.pdf?productCode=C45935408),
revision 2024.05, SHA-256
`12d00aae02bc600ac678f8d478d86e099f3339f9a9a7e2837773e5d9489acb11`,
contains only two pages. Both pages were rendered and visually reviewed. It
lists USB and module supply information, but does not establish USB_VBUS detect
range/current, unpowered tolerance, sequencing or exact full-speed behaviour.
Do not reinterpret its module supply range as a detect-input range.

The public SIMCom SIM7670X product listing and carrier documentation were also
checked. The LilyGO SIM7670G hardware-guide link resolves to SIM7672X V1.02,
not an exact LNGV guide. Exact manufacturer confirmation remains necessary;
no pin limits or mandatory component values were changed from this search.
