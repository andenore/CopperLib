# Full-vertical acceptance package

This package contains the reusable CopperScript definitions currently needed
by CopperScript's `FullVerticalTracker` integration design. It is the canonical
home for those definitions; the compiler repository consumes the package by
its stable CopperLib import path.

The package is **not production-publishable**. Several definitions are bounded
electrical subsets, and generic support entries such as the 3.3 V regulator, UART
translator, several connectors, LED and button still require exact orderable
part selections and evidence-backed footprints. Every such file is labelled as
a prototype. Moving it here avoids duplicate models; it does not promote an
illustrative definition to verified status.

The nRF52832-QFAA now has all 48 numbered QFN pins plus the exposed ground
pad bonded from the Nordic Product Specification v1.9 pin-assignment table.
This resolves its package-to-footprint number audit only; the board still lacks
the complete crystal/decoupling/reference circuit, so this is not a production
approval of the Bluetooth subsystem.

The STM32G0C1RET6 now has all 64 standard LQFP64-GP bonds from DS13564
Rev 5, Table 12. The board connects its VBAT and VREF+ supply pins, but the
MCU reference circuit, crystal/clock choice, and all vendor decoupling remain
to be completed and reviewed before production.

The nano-SIM connector is now the orderable GCT SIM8060-6-0-14-00-A (without
card detect), with I/O correctly on C7 and all four shell pads grounded. Its
installed KiCad 10 footprint includes embedded copper keepouts; CopperScript's
footprint importer now preserves those keepouts through routing, DRC, and
KiCad export. The asset passes the physical pad/footprint audit; SIM ESD and
modem reference-circuit checks remain outstanding.

The USB data-line choke is now the Coilcraft 0603USB-601MLC, matched to the
installed KiCad 0603USB land pattern and its 1-4 / 2-3 winding pairs. This
resolves its footprint mismatch; SI/EMC performance still needs board-level
measurement or qualified analysis.

The 5 V input uses the orderable GCT USB4135-GF-A power-only USB-C
receptacle. Both VBUS/GND contacts and the shield are modelled. A TUSB320LAI
sink CC controller provides the dead-battery CC pull-downs and source-current
classification; separate 5.1 kOhm CC resistors are **not** fitted. Its OUT1
and OUT2 open-drain status signals go to the MCU with 10 kOhm pull-ups.
Only the attached 3 A source code (OUT1/OUT2 both low) may permit modem power.
The connector's 3 A contact rating is not permission for the board to draw
3 A. Firmware implementing this gate and 2 A input budget, along with
overvoltage/inrush protection, remain necessary before production release.
The board-level input target is 5 V at no more than 2 A. That is distinct from
Quectel's requirement that the modem *3.8 V rail* supply 2 A. The modem rail
now uses a TI TPS62130ARGTR 3 A synchronous buck and a Coilcraft
XAL4020-222MEC 2.2 uH inductor; a 750 kOhm / 200 kOhm divider programs
3.8 V from the regulator's 0.8 V reference. A 100 kOhm pull-down holds its
enable low until firmware authorizes the modem. The regulator selection does
not establish that the complete board fits inside a 10 W input budget;
efficiency, thermal behavior, 2 A load transients, input losses and other
loads require measurement. The user's successful TLV76701DRV-family modem
implementation remains a useful prototype comparison, but TI rates that LDO
for only 1 A and it cannot substantiate the 2 A rail target.

The MAX-M10S-00B footprint is generated at
`footprints/RF_Module.pretty/u-blox_MAX-M10S.kicad_mod` from the official
[u-blox MAX-M10S integration manual](https://content.u-blox.com/sites/default/files/MAX-M10S_IntegrationManual_UBX-20053088.pdf),
UBX-20053088 R05 Figures 30-31 / Tables 44-45 (pages 82-83). It has all 18
numbered copper/mask lands and the separate recommended T-shaped 150-um
stencil apertures. Run `python scripts/generate_max_m10s_footprint.py` to
recreate it byte-for-byte. The expanded courtyard includes the stencil; this
is a conservative assembly choice, not a vendor dimension. RF layout and the
fabricator's stencil process still need review before release.

The EG800G-EU land pattern at
`footprints/RF_Module.pretty/Quectel_EG800G.kicad_mod` is transcribed from the
[JLCPCB C9900097440 listing](https://jlcpcb.com/partdetail/JLCPCBAssembly-EG800GEU/C9900097440)
and its EasyEDA LCC-109 geometry by
`scripts/generate_eg800g_footprint.py`. The generator pins the EasyEDA shape
digest and refuses changed upstream data; the checked-in result has numbered
pads 1–109 and passes a KiCad 10 export test. This is a third-party footprint,
not a Quectel-approved production land pattern. The EasyEDA *symbol* is not
used as electrical evidence: it labels some pads reserved that Quectel's
[QuecOpen Reference Design V1.1](https://developer.quectel.com/wp-content/uploads/2025/01/Quectel_EG800G_Series_QuecOpen_Reference_Design_V1.1.pdf)
uses for functions (for example pad 44 VRTC and pads 49–58). The part definition
therefore declares all physical pads, connects the Quectel-identified ground
lands, and leaves the other not-yet-reconciled pads as unmodeled placeholders.
Those placeholders cannot be connected without an electrical profile. The
complete EG800G-EU pinout and Quectel mechanical/stencil review still block
production release.

The Bluetooth antenna is now the explicit Johanson
`JOHANSON_2450AT18A0100001E` (legacy 2450AT18A100), not a generic grounded
two-pin antenna. [Doc# 36S0021A Revision 4.0](https://www.johansontechnology.com/docs/3827/Antenna-2450AT18A0100001E-Rev4.0.pdf),
page 2, identifies terminal 1 as feed and terminal 2 as an NC mechanical
anchor. Keep its second solder land isolated; ERC rejects any net on it.
The source hash and bounded facts are in `data/full-vertical/rf-audit.json`.
Page 3's corner mounting, ground-clearance and board-specific matching must
still be implemented and reviewed. Matching values from the vendor evaluation
board are not qualified values for this six-layer tracker. The Nordic support
circuit/reference layout and antenna qualification remain production blockers.
The same audit records Nordic QFAA reference v1.1, sheet 1: C3 0.8 pF
shunts the chip-side ANT node before L1 3.9 nH. The tracker example is corrected
upstream; this does not complete its crystal/decoupling/reference-ground circuit.

Import path:

```copper
import vertical "github.com/andenore/CopperLib/packages/full_vertical";
```

Before this package can be released, each orderable part must have complete
pin coverage, official-source evidence with precise revision/location, and a
verified footprint. The existing CopperLib publication gate remains the
authority for that transition.
