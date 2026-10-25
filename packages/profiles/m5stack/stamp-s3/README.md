# Stamp-S3 removable carrier sockets

Two real BOM items: `STAMP_S3_SOCKET_LEFT` is HCTL PM254-1-09-Z-8.5
(JLCPCB C2897372); `STAMP_S3_SOCKET_RIGHT` is PM254-1-06-Z-8.5 (C2897369).
Both are listed for wave-soldered PCBA. The separately purchased M5Stack S007
module and its supplied 9/6-pin male headers are installed after carrier assembly.
These are configured contact views, not a silicon model or a soldered module.

Top view: antenna up, USB down. Left socket pin 1 is module pad 1 (G1);
right socket pin 1 is module pad 28 (3V3). Rows are 15.24 mm apart; right pin 1
is 7.62 mm below left pin 1. The 2.54 mm mounting uses alternating module pads;
it does not expose all 23 GPIOs. See evidence/connector.json for exact mapping.
Do not copy the official DIP footprint's 0.55 mm holes for these carrier sockets.
Those describe module pads. HCTL's recommended carrier hole is 1.02 mm.

Footprints use the HCTL Rev A drawing: 2.54 mm pitch, 2.50 +/- 0.15 mm body
width, length 2.54*N+0.40 +/- 0.30 mm, 8.5 +/- 0.15 mm body height.
Land diameter 2 mm and 0.25 mm courtyard beyond maximum body are authored.
The module footprint's coordinate rounding (up to 7 nm) is normalized to the
dimensioned 2.54 mm grid. Sources and hashes are in evidence/connector.json;
downloaded originals are in ignored cache/m5stack/stamp-s3.

The host owns absolute socket poses, a module/body exclusion, USB cable access
and antenna clearance. Preserve these relative coordinates as a rigid pair.
Only populated 2.54 mm male-header positions are supported; do not install
additional 1.27 mm headers. Check header engagement, parallelism, underside
clearance and actual fit on a sample before assembly release.

Supply VIN_5V with nominal 5 V and connect both GND sockets. Guaranteed input
tolerance and spare 3V3 output capacity are unspecified here. 3V3 is the module
regulator output, not an invitation to parallel the host regulator. The v0.2
schematic connects USB VBUS to VIN_5V through F1 (PTC); it does not provide
source isolation. The host must isolate its 5 V supply for USB programming.
G0 is the boot button and EN resets/disables the module. Leave them unloaded
unless deliberately controlled. G43 has a module-side 510 ohm series resistor.
GPIO3 is a strapping signal; the carrier must not impose an unintended boot level.

The module schematic integrates PROANT440 antenna, L1/C1/C2 matching,
crystal, decoupling and DC/DC conversion. The host does not recreate that RF
network. Manufacturer host-board antenna keepout dimensions were not found;
host copper/enclosure adaptations and RF performance remain unqualified.
The passive socket view does not enforce GPIO mux, voltage limits, boot straps,
USB power states or power-off behavior. Firmware, antenna performance, fit,
current capacity and PCBA review are required separately. Not production qualified.
