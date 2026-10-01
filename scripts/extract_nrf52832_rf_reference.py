"""Extract a bounded matching macro from the pinned Nordic QFAA LDO archive.

Reads data only; does not execute archived Altium/project code. The chip/land
coordinates are evidence, not a qualified transplant onto a different stackup.
"""
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

ARCHIVE_SHA256 = "21e37dcdd8e63d80825bb9e06462efdebe55b642f4e19c5f25c2d9a131e6e334"
ENTRY = "nRF52832-QFAx Reference Layout 1_1/Production files/nRF52832-QFAA/nrf52832_qfaa_pick_and_place.txt"
ENTRY_SHA256 = "3f0d7860f9bf2156a40210e9991017a0cbfb7bf51422411aead01212772e0ad2"
URL = "https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/reference-layouts/nrf52832qfaxreflayoutv11.zip"
DESTINATION = Path(__file__).resolve().parents[1] / "data/full-vertical/nrf52832-qfaa-rf-reference.json"


def extract(archive: Path) -> dict:
    if sha256(archive.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Nordic reference archive identity changed")
    with ZipFile(archive) as source:
        raw = source.read(ENTRY)
    if sha256(raw).hexdigest() != ENTRY_SHA256:
        raise ValueError("Nordic QFAA LDO placement entry identity changed")
    members = []
    for line in raw.decode("cp1252").splitlines():
        fields = line.split()
        if not fields or fields[0] not in {"U1", "C3", "L1"}:
            continue
        if len(fields) < 11 or fields[8] != "T":
            raise ValueError("unsupported reference placement row")
        def coordinate(value):
            if not re.fullmatch(r"-?\d+(?:\.\d+)?mil", value):
                raise ValueError("reference placement coordinate is not in mil")
            exact = Decimal(value[:-3]) * 25400
            return int(exact.to_integral_value(rounding=ROUND_HALF_UP))
        members.append({
            "reference": fields[0], "source_footprint": fields[1],
            "center_nm": [coordinate(fields[2]), -coordinate(fields[3])],
            "source_pad1_nm": [coordinate(fields[6]), -coordinate(fields[7])],
            "rotation_degrees": str(Decimal(fields[9]) % 360),
            "population": fields[10],
        })
    if {item["reference"] for item in members} != {"U1", "C3", "L1"} or len(members) != 3:
        raise ValueError("matching reference members are missing or duplicated")
    return {
        "schema": "copperlib-rigid-reference/v0.1",
        "source": {"url": URL, "revision": "QFAA LDO v1.1, 30 November 2016",
                   "archive_sha256": ARCHIVE_SHA256, "entry": ENTRY, "entry_sha256": ENTRY_SHA256},
        "coordinate_transform": "Altium top XY in mil -> integer nm, reflect Y; preserve top rotation modulo 360",
        "quantization": "nearest integer nanometre, Decimal ROUND_HALF_UP; source row precision is not exact land-pattern accuracy",
        "anchor": {"reference": "U1", "pad": "30"},
        "members": sorted(members, key=lambda item: item["reference"]),
        "pad_nets": [
            ["U1", "30", "raw"], ["U1", "31", "ground"],
            ["C3", "1", "ground"], ["C3", "2", "raw"],
            ["L1", "1", "raw"], ["L1", "2", "feed"],
        ],
        "pad_net_evidence": "QFAA LDO schematic sheet 1 and PCB PDF page 1 top copper; C3 upper land/first-pad coordinate is GND, lower land is ANT",
        "production_publishable": False,
        "unresolved": ["resolved footprint adaptation", "matching ground copper/vias",
                       "complete support/crystal circuit", "six-layer stackup/antenna matching"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=DESTINATION)
    args = parser.parse_args()
    document = extract(args.archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Raw-byte identities must survive generation and checkout on Windows/Linux.
    args.output.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
