"""Deterministic six-layer TPS63020 layout adaptations, not extracted TI CAD.

The assets bind an explicit component set without changing its electrical IR.
Lengths and widths are authored geometry, not current/thermal qualification.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = "github.com/andenore/CopperLib/packages/parts/"
LAYERS = ["F.Cu", "In1.Cu", "In2.Cu", "In3.Cu", "In4.Cu", "B.Cu"]
FOOTPRINTS = {
    "U": (LIB + "ti/tps63020/footprints/TI_DSJ0014_TPS63020.kicad_mod", "868d75b61d43b61e5e92f5d118d4ac8bb28cb590d8bccda128789cd399c2d80d"),
    "L": (LIB + "bourns/srp4020ta/footprints/Bourns_SRP4020TA.kicad_mod", "2d3625ed24b82fd9bea8f1468539474a40f6026b87c13ca1a44dc91fc41dc03e"),
    "C_IN": ("Capacitor_SMD:C_0805_2012Metric", "10029d0eef91812b8b2cbffa7695a033370cbca3ee988ba1426b632cf6609662"),
    "C_VINA": ("Capacitor_SMD:C_0402_1005Metric", "86575c98c1bd84414ad1626d2f1a649749c0fb10743c56ba8f2c3fdee795a0ff"),
    "R_TOP": ("Resistor_SMD:R_0402_1005Metric", "e907cca3732f063d1d109c709b5962d31caeb59bfff68284fb04effdb7351e12"),
}
for name in ("C_OUT1", "C_OUT2", "C_OUT3"):
    FOOTPRINTS[name] = FOOTPRINTS["C_IN"]
for name in ("R_TOP2", "R_BOT", "R_EN_PD"):
    FOOTPRINTS[name] = FOOTPRINTS["R_TOP"]


def nm(value):
    return round(value * 1_000_000)


def point(x, y):
    return [nm(x), nm(y)]


def pad(ref, number):
    return {"pad": [ref, str(number)]}


def generate(enabled=False):
    poses = {"U": (0, 0, 0), "L": (0, 5, 180),
             "C_IN": (3.55, -.1, 90), "C_VINA": (-3, -2, 180),
             "C_OUT1": (-3.55, .2, 90), "C_OUT2": (-5.75, .2, 90),
             "C_OUT3": (-8.05, .2, 90), "R_TOP": (-2.6, -3.9, 0),
             "R_BOT": (-.7, -3.9, 0)}
    if enabled:
        poses.update(R_TOP=(-4.5, -3.9, 0), R_TOP2=(-2.6, -3.9, 0),
                     R_EN_PD=(5, -4.5, 0))
    tracks, vias, pad_nets = [], [], []

    def track(net, vertices, width=.2, layer="F.Cu"):
        tracks.append(dict(net=net, points=[p if isinstance(p, dict) else point(*p) for p in vertices],
                           width_nm=nm(width), layer=layer))

    def via(net, xy):
        vias.append(dict(net=net, position_nm=point(*xy), size_nm=600000,
                         drill_nm=300000, from_layer="F.Cu", to_layer="B.Cu", technology=None))

    def assign(ref, numbers, net):
        pad_nets.extend([ref, str(p), net] for p in numbers)

    for numbers, net in [([1, 10, 11], "VIN"), ([2, 13, 15], "GND"),
                         ([3], "FB"), ([4, 5], "VOUT"), ([6, 7], "L2"),
                         ([8, 9], "L1"), ([12], "EN" if enabled else "VIN")]:
        assign("U", numbers, net)
    assign("L", [1], "L1")
    assign("L", [2], "L2")
    for ref, net in [("C_IN", "VIN"), ("C_VINA", "VIN"),
                     ("C_OUT1", "VOUT"), ("C_OUT2", "VOUT"), ("C_OUT3", "VOUT")]:
        assign(ref, [1], net)
        assign(ref, [2], "GND")
    assign("R_TOP", [1], "VOUT")
    assign("R_TOP", [2], "FB_SERIES" if enabled else "FB")
    if enabled:
        assign("R_TOP2", [1], "FB_SERIES")
        assign("R_TOP2", [2], "FB")
        assign("R_EN_PD", [1], "EN")
        assign("R_EN_PD", [2], "GND")
        track("FB_SERIES", [pad("R_TOP", 2), pad("R_TOP2", 1)])
    assign("R_BOT", [1], "FB")
    assign("R_BOT", [2], "GND")

    def polygon(name, net, vertices):
        return dict(id=name, net=net, layer="F.Cu", vertices=[point(*p) for p in vertices])

    # Separately contact both switch lands and both VIN/VOUT lands. These are
    # not internal-pad exemptions or a claim that one power pin is sufficient.
    for number, y in ((8, 1.5), (9, 1)):
        track("L1", [pad("U", number), (2.25, y)], .24)
    for number, y in ((6, 1), (7, 1.5)):
        track("L2", [pad("U", number), (-2.25, y)], .24)
    for role, pins, x in (("VIN", (10, 11), 2.1), ("VOUT", (4, 5), -2.1)):
        for number in pins:
            track(role, [pad("U", number), (x, .5 if number in (5, 10) else 0)], .24)
    switch_right = [(1.9, .85), (2.65, .85), (2.65, 6.2),
                    (.95, 6.2), (.95, 3.8), (1.9, 3.8)]
    polygons = [polygon("switch-l1", "L1", switch_right),
                polygon("switch-l2", "L2", [(-x, y) for x, y in reversed(switch_right)]),
                polygon("input-lobe", "VIN", [(1.8, -.12), (2.3, -.12), (2.3, .3),
                        (6, .3), (6, 1.55), (2.85, 1.55), (2.85, .62), (1.8, .62)]),
                polygon("output-lobe", "VOUT", [(-1.8, -.12), (-2.3, -.12), (-2.3, .3),
                        (-9, .3), (-9, 1.85), (-2.85, 1.85), (-2.85, .62), (-1.8, .62)])]
    track("VIN", [(5.7, .85), (8.2, .85)], .8)
    track("VOUT", [(-8.7, 1.15), (-10.2, 1.15)], .8)
    for role, xy in (("VIN", (8.2, .85)), ("VOUT", (-10.2, 1.15))):
        via(role, xy)

    # VINA decoupling is local on F.Cu. Its low-current feed is behind the
    # In4 ground reference, separate from the main power and switch copper.
    track("VIN", [pad("U", 1), pad("C_VINA", 1), (-2.49, -2.5), (-3, -3)])
    via("VIN", (-3, -3))
    track("VIN", [(-3, -3), (-2.6, -3), (-2.6, -5.8), (9.4, -5.8), (9.4, .85), (8.2, .85)], .2, "B.Cu")

    # Kelvin sense from output-capacitor copper; shielded low-current feed and
    # feedback are owner routes, never long ordinary autorouter nets.
    sense_x = -5.01 if enabled else -3.6
    track("VOUT", [pad("R_TOP", 1), (sense_x, -5)])
    via("VOUT", (sense_x, -5))
    via("VOUT", (-4.6, 1.15))
    track("VOUT", [(-10.2, 1.15), (-4.6, 1.15)], .8, "B.Cu")
    track("VOUT", [(-4.6, 1.15), (-4.6, -5), (sense_x, -5)], .2, "B.Cu")
    track("FB", [pad("U", 3), (-2.4, -.55)])
    via("FB", (-2.4, -.55))
    via("FB", (-1.95, -3.2))
    track("FB", [(-2.4, -.55), (-1.35, -.55), (-1.35, -3.2), (-1.95, -3.2)], .2, "In2.Cu")
    track("FB", [(-1.95, -3.2), pad("R_TOP2" if enabled else "R_TOP", 2), pad("R_BOT", 1)])

    en = "EN" if enabled else "VIN"
    track(en, [pad("U", 12), (2.35, -.6)])
    via(en, (2.35, -.6))
    via(en, (8.2, -3))
    track(en, [(2.35, -.6), (6, -.6), (8.2, -3)], .2, "In2.Cu")
    if enabled:
        # A defined F.Cu lead-in makes this an unambiguous surface port.
        # The prior bare via terminal could be entered on In2.Cu only, leaving
        # an owner via connected on just one layer in native DRC.
        track("EN", [(8.2, -3), (8.8, -3)])
        track("EN", [pad("R_EN_PD", 1), (4.49, -5.15)])
        via("EN", (4.49, -5.15))
        track("EN", [(4.49, -5.15), (4.49, -.6)], .2, "In2.Cu")
    else:
        track("VIN", [(8.2, -3), (8.2, .85)], .2, "B.Cu")

    # Off-pad standard vias avoid silently requiring filled/capped assembly.
    # All PGND comb lands physically touch the central copper in the footprint;
    # the common copper is wired, with no internal-pad connectivity exemption.
    # Pad 15 has nine physical lands; use its explicit central copper point,
    # never the ambiguous unique-land endpoint shorthand.
    track("GND", [(0, 0), (0, -2.75)], .6)
    track("GND", [(0, 0), (0, 2.75)], .6)
    for xy in ((0, -2.75), (.6, -2.75), (-.6, -2.75), (0, 2.75), (.6, 2.75), (-.6, 2.75)):
        via("GND", xy)
    track("GND", [(-.6, -2.75), (.6, -2.75)], .6)
    track("GND", [(-.6, 2.75), (.6, 2.75)], .6)
    # Join quiet control ground directly to the exposed-pad copper near the IC.
    track("GND", [pad("U", 2), (0, -1), (0, 0)])
    track("GND", [pad("R_BOT", 2), (0, -2.75)])
    track("GND", [pad("U", 13), (2.1, -1.3), (2.7, -2)])
    via("GND", (2.7, -2))
    ground_contacts = [("C_IN", (3.55, -2.4)), ("C_VINA", (-4, -2.4)),
                       ("C_OUT1", (-3.75, -3)), ("C_OUT2", (-5.75, -1.95)),
                       ("C_OUT3", (-8.05, -1.95))]
    if enabled:
        ground_contacts.append(("R_EN_PD", (6.4, -4.5)))
    for ref, xy in ground_contacts:
        track("GND", [pad(ref, 2), xy], .4 if ref.startswith("C_OUT") or ref == "C_IN" else .2)
        via("GND", xy)

    boundary = [point(-9.3, -6.2), point(7.3, -6.2), point(7.3, 7.5), point(-9.3, 7.5)]
    def region(name, layers, tracks=False, vias=False, zones=False):
        return dict(id=name, layers=layers, vertices=boundary,
                    block_tracks=tracks, block_vias=vias, block_zones=zones)
    ports = []
    for role, xy in [("VIN", (8.2, .85)), ("VOUT", (-10.2, 1.15))] + ([("EN", (8.8, -3))] if enabled else []):
        ports.append(dict(name=role, net=role, point=point(*xy), layer="F.Cu",
                          pads=[[r, p] for r, p, net in pad_nets if net == role]))
    width_contracts = []
    for index, t in enumerate(tracks):
        if t["width_nm"] >= nm(.8) or t["net"] not in {"VIN", "VOUT", "EN", "L1", "L2"}:
            continue
        first = t["points"][0]
        pin = first.get("pad") if isinstance(first, dict) else None
        if pin and pin[0] == "U" and pin[1] in {str(i) for i in range(4, 12)}:
            purpose = "pin_entry"
            evidence = "Authored 0.24 mm individual DSJ land entry into owned power/switch polygon; see physical-layout.md. Peak/RMS neckdown capacity remains unresolved."
        elif t["net"] == "VOUT":
            purpose = "output_sense"
            evidence = "Authored 0.2 mm low-current Kelvin feedback sense from output-capacitor copper, not load-current distribution; TI SLVS916I section 10.1 intent, adaptation in physical-layout.md."
        elif t["net"] == "EN" or (pin == ["U", "12"]) or first in (point(2.35, -.6), point(8.2, -3)):
            purpose = "enable"
            evidence = "Authored 0.2 mm EN control branch, not the VIN main current path; physical-layout.md and TI SLVS916I pin functions."
        else:
            purpose = "control_supply"
            evidence = "Authored 0.2 mm VINA control supply/decoupler feed, not VIN main current distribution; TI SLVS916I section 10.1 intent, adaptation in physical-layout.md."
        width_contracts.append(dict(track_index=index, minimum_width_nm=t["width_nm"], purpose=purpose, evidence=evidence))
    return dict(schema="copperlib-physical-hard-macro/v0.4", production_publishable=False,
        source=dict(datasheet_url="https://www.ti.com/lit/ds/symlink/tps63020.pdf",
                    datasheet_sha256="d117773bb7370fd79377bc70ce987eec3469ea5979547a09df52fca5f95b2e69",
                    datasheet_locator="SLVS916I Rev I, section 10.1, Figure 31, p23; DSJ land drawings pp31-33",
                    evm_url="https://www.ti.com/lit/ug/slvu365/slvu365.pdf",
                    evm_sha256="a164c060584f238a27553efe054ad47916d90fcf4ca5739bf0d01c8e35c5c221",
                    evm_locator="SLVU365 March 2010, Figures 6-8, pp6-7",
                    geometry_status="authored adaptation, not digitized/extracted TI CAD; Bourns inductor, 0805 outputs, six layers, off-pad vias and shielded feedback"),
        anchor="U", members=[dict(reference=r, footprint=FOOTPRINTS[r][0], footprint_digest=FOOTPRINTS[r][1],
            center_nm=point(x, y), rotation_degrees=str(a), edge_clearance_nm=250000)
            for r, (x, y, a) in sorted(poses.items())],
        pad_nets=pad_nets, isolated_pads=[["U", "14"]], tracks=tracks, vias=vias, polygons=polygons,
        width_contracts=width_contracts,
        zones=[dict(id="local-ground-return", net="GND", layers=["F.Cu"], vertices=boundary,
                    priority=2, clearance_nm=90000, minimum_width_nm=150000, pad_connection="solid")],
        plane_returns=[dict(net="GND", layers=["In1.Cu", "In4.Cu"],
            pads=[[r, p] for r, p, n in pad_nets if n == "GND"],
            dedicated_contacts=[dict(pad=[r, "2"], via_position_nm=point(*xy)) for r, xy in ground_contacts])],
        ports=ports, protected_regions=[region("converter-private", ["F.Cu", "In2.Cu", "B.Cu"], True, True)],
        keepouts=[region("converter-fill-exclusion", ["In2.Cu", "In3.Cu", "B.Cu"], zones=True)],
        required_layers=LAYERS, allowed_rotations=[0, 90, 180, 270], internal_clearance_nm=0,
        unresolved=["input/output conductor, neckdown and via current capacity at actual copper weight",
                    "MLCC effective capacitance and inductor saturation/temperature at minimum battery voltage",
                    "loop stability, EMI, thermal and modem-transient bench qualification",
                    "six-layer stackup, assembly paste and off-pad thermal-via suitability",
                    "author adaptation differs from TI CAD; native geometry checks are not production approval"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for enabled in (False, True):
        target = args.output_dir / f"tps63020-six-layer-{'enabled-series-feedback' if enabled else 'always-on'}.json"
        target.write_bytes((json.dumps(generate(enabled), sort_keys=True, indent=2) + "\n").encode())
        print(f"{target.name}: sha256:{sha256(target.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
