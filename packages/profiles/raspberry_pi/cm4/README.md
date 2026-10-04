# Raspberry Pi CM4 carrier interfaces

Source-backed **carrier connector and mechanical definitions**, not an active
BCM2711/device model or a qualified production bundle. Two Hirose
`DF40C-100DS-0.4V(51)` receptacles are separate soldered BOM items; the CM4 is a
separately purchased plug-in module. Do not substitute the 3 mm stacking variant.

```copper
import cm4 "github.com/andenore/CopperLib/packages/profiles/raspberry_pi/cm4";
component J1: cm4.CM4_GPIO_SOCKET { value = "DF40C-100DS-0.4V(51)"; }
component J2: cm4.CM4_HS_SOCKET { value = "DF40C-100DS-0.4V(51)"; }
mechanical {
    use cm4.CM4Mounting as module { gpio = J1; high_speed = J2; }
}
```

The profile intentionally has **no carrier outline**. It exports four NPTH
holes and two exact pad-1 poses. Its canonical board coordinates place the
40 x 55 mm module envelope at x=10..50, y=10..65 mm. No use-site transform is
implemented yet. Profile provenance identifies the imported feature owners.

## Electrical contract

- Each socket has exactly 100 distinct pins, locally numbered 1..100.
  CM4 pins 101..200 map to socket J2 numbers 1..100: USB_N=3, USB_P=5.
- Named signals follow current datasheet Table 6, not assumptions from similar
  Raspberry Pi headers. `GND_107`, for example, is CM4 pin 107 / J2 pad 7.
- All fitted grounds, all six 5 V contacts and GPIO_VREF are required.
  Reserved contacts 76, 104 and 106 are `do_not_connect`.
- Other contacts are optional. Signal contacts are passive because these parts
  are sockets, not the active CM4. ERC does not check GPIO mux, firmware,
  peripheral direction, timing, backfeed or rail sequencing through this model.
  5 V input limits 4.75..5.25 V are mated CM4 operating requirements.
- No `internal_pad_groups`: every required ground/power contact needs its own
  carrier connection, even though several join on the installed module.
- Tie GPIO_VREF to CM4's 3.3 V or 1.8 V output, never float it or use an
  independently powered rail. Do not power GPIO before the CM4's 5 V input.
- Hirose specifies 0.3 A/contact. Review current sharing and power routing;
  simply paralleling six power pins does not prove a safe total current.

`HEADER_1X02`, `HEADER_1X04` and `HEADER_1X06` are **reference pin-header
geometry**, not manufacturer-selected/orderable parts. Pin names are numbers;
the project assigns header functions. These are publication/assembly-selection
blockers for an orderable production bundle, not unresolved CM4 pin mappings.

## Mechanical contract and remaining checks

The 1.5 mm stacking option provides **zero spare component height under CM4**.
Five front-side placement keepouts reserve the module body, excluding the two
socket courtyard corridors plus a 0.3 mm allowance. Those corridors are only
for the sockets; do not place extra components in them. The current rectangle
keepout representation cannot express an owner-exempt solid body region.
Tracks under the body are allowed. Back-side components may be placed subject
to enclosure clearance, which is not modeled here.

M2.5 holes have 33 x 48 mm spacing; 2.7 mm carrier drills reproduce CM4IO v5.
The 3 mm screw-head clearance radius is a conservative carrier choice, not a
vendor requirement. Match the actual screws, spacers and enclosure in 3D.

For wireless CM4s the carrier owns an all-layer antenna copper/metal keepout.
Datasheet Fig. 4's minimum cutout is 6.5 x 11 mm, preferably 8 x 15 mm. In this
datum the minimum projection is x=20.5..31.5, y=58.5..65 mm. The CopperScript
example reserves x=18.5..33.5, y=55..70 mm on four layers. No RF performance or
enclosure qualification is implied. No CM5 compatibility claim is made.

## Evidence and regeneration

- [CM4 datasheet](https://datasheets.raspberrypi.com/cm4/cm4-datasheet.pdf):
  printed p13 Fig. 4; pp16-22 Table 6; p25 power sequence.
- [Official CM4IO KiCad reference](https://pip.raspberrypi.com/categories/1210-design-files):
  v5 combined carrier footprint establishes orientation and exact pad anchors.
- [Hirose exact connector](https://www.hirose.com/en/product/p/CL0684-4033-4-51):
  drawing EDC3-311352-00 sheet 1, spec ELC-311352-51-51 rev 3 sheet 1.
- KiCad `Connector_Hirose_DF40:Hirose_DF40C-100DS-0.4V_2x50_P0.4mm`:
  0.4 mm pitch, 3.08 mm land-centre separation, 0.2 x 0.7 mm pads;
  all 200 placed land centres checked against the official CM4IO footprint.

Compact verified facts and source hashes: `evidence/pinout.json` and
`evidence/mechanics.json`. Raw downloads remain in ignored `cache/cm4/`.
Do not redistribute the vendor reference project or execute anything in it.
Use these facts only for designs employing Raspberry Pi products, subject to
the vendor terms; this package grants no Raspberry Pi branding rights.

```sh
python packages/profiles/raspberry_pi/cm4/generate.py --check
python -m pytest tests/test_cm4.py
```

The deterministic generator renders the two contextual sockets from the
reviewed compact table. Production device generation still requires a separate
complete functional CM4 model; these sockets deliberately do not simulate one.
