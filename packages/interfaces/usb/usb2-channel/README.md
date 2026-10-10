# USB 2.0 channel qualification

Reusable companion contract for a complete endpoint-to-endpoint USB channel,
including every inline component and routed net section. No universal lengths,
component values or PCB impedance tolerances are invented here.

The [official USB-IF package](https://www.usb.org/document-library/usb-20-specification)
dated 2025-06-03 and its base-specification PDF are separately hash-pinned in
`qualification.json`. The base specification is Revision 2.0, 27-Apr-2000.
Downloaded ZIP/PDF bytes belong in ignored `cache/`; consult applicable errata,
ECNs and exact device/reference designs before accepting a consumer design.

Mandatory independent requirements cover operating mode, layout, impedance,
signal integrity and prototype results. Consumers bind their endpoints, net
sections, inline devices, stackup, operating states and reviewed external reports.
Algorithms/evidence validation live in CopperScript. Geometry inventories cannot
replace any mandatory external requirement or certify USB compliance.

Mode selection matters: Chapter 7 distinguishes full-speed and high-speed
signalling. The base specification's full-speed rise/fall section (§7.1.2.1,
printed p130 / PDF page 158, including Figures 7-8/7-9) was rendered and visually
inspected; the full-speed test load and measurement definition are not the
high-speed eye templates. §7.1.11 (printed p159 / PDF page 187) distinguishes
12 Mbit/s full-speed from 480 Mbit/s high-speed. Record endpoint capabilities
and actual negotiated mode before selecting limits or drawing conclusions
about length/skew.

Review VBUS detection and power availability separately from transceiver supply.
A working UART or a zero-open PCB does not establish that USB attaches on battery
power. Firmware roles, host clocking, device descriptors and driver availability
are consumer obligations, not a reusable guarantee.

## Battery-powered internal host links

Record required functional states explicitly: battery-only operation, charging
and charging-input removal where applicable. Also review safe shutdown,
undervoltage, power-source attachment and device-disabled states. Do not let an
external charging input become an accidental prerequisite for internal USB.

Establish exact device detect-input recommended voltage/current limits and
unpowered/sequencing tolerance separately from VBAT and absolute maximum ratings.
Evaluate regulator tolerance, load droop, startup/overshoot and shutdown at the
actual pin; a nominal voltage or powered UART is not evidence of USB attachment.
Keep internally generated detect power isolated from external input-only VBUS;
review reverse current, contention and phantom power through detect and data pins.

Select supply/control circuitry only after those limits are established. Reuse
existing rails when qualified over all required states; a new boost converter is
not universally necessary. Any new reusable circuit belongs in CopperLib with
source-backed switched-power macro/constraints. Consumer net/enable bindings and
measurements belong in the consumer. These are review obligations, not a claim
that the compiler simulates power states or that this contract approves a supply.
