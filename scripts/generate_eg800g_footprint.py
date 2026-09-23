"""Transcribe the JLCPCB/EasyEDA EG800G-EU land pattern into KiCad.

Only physical PAD records are used. The associated EasyEDA schematic symbol
is *not* an electrical authority: it disagrees with Quectel's reference
design on several multifunction pins. The source shape digest pins the exact
upstream revision and makes an unexpected source change fail closed.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path
from urllib.request import Request, urlopen


PART_URL = "https://jlcpcb.com/partdetail/JLCPCBAssembly-EG800GEU/C9900097440"
API_URL = "https://easyeda.com/api/products/C9900097440/components?version=6.5.44"
SHAPE_SHA256 = "6686bd207dbc06407a6697d9fc83a60a8ab0ffb30703e12c92a4b390f4bcc08e"
DESTINATION = (
    Path(__file__).resolve().parents[1]
    / "footprints/RF_Module.pretty/Quectel_EG800G.kicad_mod"
)
MM_PER_EASYEDA_UNIT = Decimal("0.254")


def _mm(value: str | int | float, origin: str | int = 0) -> str:
    number = (Decimal(str(value)) - Decimal(str(origin))) * MM_PER_EASYEDA_UNIT
    return f"{number:.6f}".rstrip("0").rstrip(".") or "0"


def load_source() -> dict:
    request = Request(API_URL, headers={"User-Agent": "CopperLib footprint audit"})
    with urlopen(request, timeout=30) as response:
        document = json.load(response)
    if not document.get("success"):
        raise ValueError("EasyEDA did not return a successful component record")
    package = document["result"]["packageDetail"]["dataStr"]
    shapes = package["shape"]
    digest = hashlib.sha256(
        json.dumps(shapes, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    if digest != SHAPE_SHA256:
        raise ValueError(f"EasyEDA footprint changed: {digest}; review before updating")
    if package["head"]["c_para"]["package"] != "LCC-109_L17.7-W15.8-P1.10_EG800G-EU":
        raise ValueError("Unexpected EG800G-EU package identity")
    return package


def render(package: dict) -> str:
    head = package["head"]
    origin_x, origin_y = head["x"], head["y"]
    pads: dict[int, str] = {}
    for shape in package["shape"]:
        fields = shape.split("~")
        if fields[0] != "PAD":
            continue
        kind, x, y, width, height, layer, number = (
            fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[8]
        )
        angle = fields[11]
        if kind not in {"RECT", "OVAL"} or layer != "1" or angle not in {"0", "90"}:
            raise ValueError(f"Unsupported EG800G-EU pad: {shape}")
        pin = int(number)
        if pin in pads:
            raise ValueError(f"Duplicate EG800G-EU pad {pin}")
        pads[pin] = (
            f'  (pad "{pin}" smd {kind.lower()} '
            f'(at {_mm(x, origin_x)} {_mm(y, origin_y)} {angle}) '
            f'(size {_mm(width)} {_mm(height)}) '
            '(layers "F.Cu" "F.Paste" "F.Mask"))'
        )
    if set(pads) != set(range(1, 110)):
        raise ValueError("EG800G-EU footprint must have exactly pads 1–109")
    lines = [
        '(footprint "Quectel_EG800G"',
        '  (version 20240108)',
        '  (generator "copperlib")',
        '  (layer "F.Cu")',
        '  (descr "EG800G-EU; JLCPCB C9900097440 / EasyEDA LCC-109; verify against Quectel before fabrication")',
        '  (tags "Quectel EG800G-EU LTE LCC-109")',
        '  (attr smd)',
        '  (fp_rect (start -7.9 -8.85) (end 7.9 8.85)',
        '    (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))',
        '  (fp_rect (start -9.4 -10.35) (end 9.4 10.35)',
        '    (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))',
        '  (fp_text reference "REF**" (at 0 -10.85) (layer "F.SilkS")',
        '    (effects (font (size 1 1) (thickness 0.15))))',
        '  (fp_circle (center -7.2 -8.15) (end -7 -8.15)',
        '    (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))',
    ]
    lines.extend(pads[number] for number in sorted(pads))
    lines.append(')')
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(render(load_source()), encoding="utf-8")
    print(DESTINATION)
