"""Generate an explicitly unqualified RF assembly from pinned source evidence.

The Nordic matching strokes are verified against the QFAA LDO top Gerber.
The Johanson tee/corner and off-pad ground accesses are an adapted trial, NOT
a vendor CAD import or impedance-qualified copy. No fetching or CAD execution.
"""
from hashlib import sha256
from decimal import Decimal
import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

from extract_reference import ARCHIVE_SHA256, URL, extract

ROOT = Path(__file__).resolve().parent
ENTRY = "nRF52832-QFAx Reference Layout 1_1/Production files/nRF52832-QFAA/nrf52832_qfaa.GTL"
FOOTPRINTS = {
    "U1": ("Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.2x4.2mm", "cb810b0416966534962bcc4220c4f39bb8a6b22d45da13753297f20bf77ce078"),
    "C3": ("Capacitor_SMD:C_0402_1005Metric", "6626461e823efd255bfbdef7bdf64c8feb10fc410b0cacfd6353137e29252eda"),
    "L1": ("Inductor_SMD:L_0402_1005Metric", "5562c5cb01e540b6441fb2b3587074acffff71760023c276b03b69c374da1580"),
    "CA": ("Capacitor_SMD:C_0402_1005Metric", "6626461e823efd255bfbdef7bdf64c8feb10fc410b0cacfd6353137e29252eda"),
    "LA": ("Inductor_SMD:L_0402_1005Metric", "5562c5cb01e540b6441fb2b3587074acffff71760023c276b03b69c374da1580"),
    "LB": ("Inductor_SMD:L_0402_1005Metric", "5562c5cb01e540b6441fb2b3587074acffff71760023c276b03b69c374da1580"),
    "ANT": ("RF_Antenna:Johanson_2450AT18x100", "75af7637664284175ab59931a8ee60da88f9a34bedd40f84361e06c6604ccb62"),
}
LAYERS = ["F.Cu", "In1.Cu", "In2.Cu", "In3.Cu", "In4.Cu", "B.Cu"]


def gerber_strokes(text):
    """Bounded reader for this identity-pinned, linear RS274X 2.4-inch file.

    Only dark circular-aperture D01 strokes outside polygon regions are read.
    It is not a general Gerber importer and never infers an electrical net.
    """
    text = re.sub(r"\s+", "", text)
    if "%FSLAX24Y24*%" not in text or "%MOIN*%" not in text:
        raise ValueError("reference Gerber coordinate format changed")
    apertures = {int(a): int(Decimal(b) * 25400000) for a, b in re.findall(r"%ADD(\d+)C,([\d.]+)\*%", text)}
    x = y = 0
    aperture = None
    dark = True
    in_region = False
    strokes = set()
    for command in text.replace("%", "").split("*"):
        if command == "G36": in_region = True
        elif command == "G37": in_region = False
        elif command == "LPC": dark = False
        elif command == "LPD": dark = True
        elif re.fullmatch(r"D\d+", command) and int(command[1:]) >= 10:
            aperture = int(command[1:])
        else:
            match = re.fullmatch(r"(?:X(-?\d+))?(?:Y(-?\d+))?D0([123])", command)
            if match:
                nx = x if match[1] is None else int(match[1])
                ny = y if match[2] is None else int(match[2])
                if match[3] == "1" and not in_region and dark and aperture in apertures:
                    strokes.add(((x, y), (nx, ny), apertures[aperture]))
                x, y = nx, ny
    return strokes


def generate(archive):
    reference = extract(archive)  # verifies archive and pick-and-place identities
    with ZipFile(archive) as z:
        gerber = z.read(ENTRY)
    expected = [
        ((1191, -79), (1378, -79), 228600),
        ((1378, -79), (1500, -201), 228600),
        ((1500, -201), (1653, -201), 228600),
        ((243, 80), (1378, 80), 228600),
        ((1378, 80), (1491, 193), 228600),
        ((1491, 193), (1653, 193), 228600),
        ((1650, -199), (2003, -199), 508000),
    ]
    strokes = gerber_strokes(gerber.decode("ascii"))
    if not set(expected) <= strokes:
        raise ValueError("source-backed Nordic RF strokes changed or are missing")
    def track(net, points, width=228600, layer="F.Cu"):
        return dict(net=net, points=points, width_nm=width, layer=layer)
    def pad(ref, number): return {"pad": [ref, number]}
    def region(name, rectangle, layers, tracks=True, vias=True, zones=True):
        x0, y0, x1, y1 = rectangle
        return dict(id=name, layers=layers, vertices=[[x0,y0],[x1,y0],[x1,y1],[x0,y1]],
                    block_tracks=tracks, block_vias=vias, block_zones=zones)
    members = []
    poses = {m["reference"]: (m["center_nm"], m["rotation_degrees"]) for m in reference["members"]}
    poses.update(CA=([14500000,-1500000],"90"), LA=([13300000,-3000000],"0"),
                 LB=([14500000,-4500000],"90"), ANT=([14500000,-8750000],"90"))
    for ref, (position, rotation) in sorted(poses.items()):
        footprint, digest = FOOTPRINTS[ref]
        members.append(dict(reference=ref, footprint=footprint, footprint_digest=digest,
                            center_nm=position, rotation_degrees=rotation, edge_clearance_nm=250000))
    tracks = []
    for start, end, width in expected:
        tracks.append(track("ground" if start[1] > 0 else "raw",
                            [[start[0]*2540,-start[1]*2540], [end[0]*2540,-end[1]*2540]], width))
    # Ground extension starts inside the existing EP copper. The RF strokes
    # above are untouched; endpoint overlap with installed lands is DRC-tested.
    tracks += [
        track("ground", [pad("U1","49"), [617220,-203200]]),
        track("ground", [pad("U1","49"), [-1000000,-1000000], pad("U1","45"), [-1000000,-4300000]]),
        track("feed", [pad("L1","2"), [12972000,508000], pad("CA","1")], 250000),
        track("tee", [pad("CA","2"), [14500000,-3000000], pad("LB","1")], 250000),
        track("tee", [pad("LA","2"), [14500000,-3000000]], 250000),
        track("antenna", [pad("LB","2"), pad("ANT","1")], 250000),
        track("ground", [pad("LA","1"), [11500000,-3000000]], 250000),
        track("ground", [[-1000000,-4300000], [10200000,-4300000], [11500000,-3000000]], 250000, "B.Cu"),
    ]
    via = lambda position: dict(net="ground", position_nm=position, size_nm=600000, drill_nm=300000,
                                from_layer="F.Cu", to_layer="B.Cu", technology=None)
    return dict(schema="copperlib-physical-hard-macro/v0.1", anchor="U1", members=members,
        source={"nordic_url": URL, "archive_sha256": ARCHIVE_SHA256, "gerber_entry": ENTRY,
                "gerber_sha256": sha256(gerber).hexdigest(),
                "antenna_url": "https://www.johansontechnology.com/docs/3827/Antenna-2450AT18A0100001E-Rev4.0.pdf",
                "antenna_revision": "36S0021A Revision 4.0 (2024), page 3",
                "antenna_sha256": "c11a1866c9fd04bad6dcbbd40cfdfbec067c731e47ba83f4e58b56c0e4c9dfa0",
                "geometry_status": "Nordic matching strokes extracted; Johanson tee/corner and ground exits adapted, not vendor CAD"},
        pad_nets=[["U1","30","raw"],["U1","31","ground"],["U1","45","ground"],["U1","49","ground"],
                  ["C3","1","ground"],["C3","2","raw"],["L1","1","raw"],["L1","2","feed"],
                  ["CA","1","feed"],["CA","2","tee"],["LA","1","ground"],["LA","2","tee"],
                  ["LB","1","tee"],["LB","2","antenna"],["ANT","1","antenna"]],
        isolated_pads=[["ANT","2"]],
        tracks=tracks, vias=[via([-1000000,-4300000]),via([11500000,-3000000])],
        ports=[dict(name="ground", net="ground", point=[-1000000,-4300000], layer="B.Cu",
                    pads=[["U1","49"],["U1","31"],["U1","45"],["C3","1"],["LA","1"]])],
        # This is a router ownership envelope, not a vendor keepout. Its upper
        # edge leaves the DEC3 pad (-1 mm) an outward surface access corridor.
        # Source RF strokes and the separate no-pour/inner/via keepouts below
        # retain their original geometry. The nearest RF ground stroke remains
        # inside the envelope with >0.28 mm margin at the upper edge.
        protected_regions=[region("nordic-private", [3300000,-600000,6200000,1200000], ["F.Cu"], zones=False),
                           region("antenna-private", [12000000,-11700000,15500000,100000], ["F.Cu"], zones=False)],
        keepouts=[region("nordic-no-pour",[3300000,-1000000,6200000,1200000], ["F.Cu"], tracks=False),
                  region("nordic-inner-clear",[3300000,-1000000,6200000,1200000], LAYERS[1:]),
                  region("antenna-corner",[9500000,-12000000,16000000,-5500000],LAYERS,tracks=False),
                  region("tee-no-pour",[12000000,-5500000,15500000,100000],LAYERS,tracks=False)],
        required_layers=LAYERS, allowed_rotations=[0,45,90,135,180,225,270,315], internal_clearance_nm=0,
        production_publishable=False,
        unresolved=["complete powered MCU/crystal/decoupling circuit", "antenna tee values are evaluation-board values, not tuning",
                    "actual six-layer laminate and RF feed impedance", "reference ground/corner copper and via-fence qualification",
                    "whole-board macro boundary port allocation and placement feedback", "enclosure/antenna radiation verification"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "assets/nrf52832-johanson-six-layer-trial.json")
    args = parser.parse_args()
    document = generate(args.archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode())
    print(f"{args.output}: sha256:{sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__": main()
