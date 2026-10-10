"""Convert the complete exact C45935408 EasyEDA package, never its symbol.

Input is downloaded data, not executable code. Retains all 124 numbered lands.
Source: JLCEDA/EasyEDA Official Library, https://lceda.cn/ https://easyeda.com.
Run: python packages/parts/simcom/sim7670g-lngv/import_footprint.py cache/modem-easyeda.json
"""
import hashlib
import json
import sys
from pathlib import Path

source = Path(sys.argv[1])
data = json.loads(source.read_text(encoding="utf-8"))
assert data["success"] and data["result"]["lcsc"]["number"] == "C45935408"
package = data["result"]["packageDetail"]
assert package["uuid"] == "2be3f51bf5e54bc28cbf6586caa12048"
geometry = package["dataStr"]
if isinstance(geometry, str):
    geometry = json.loads(geometry)
ox, oy = float(geometry["head"]["x"]), float(geometry["head"]["y"])
lines = [
    '(footprint "SIM7670G_LNGV" (version 20240108) (generator "CopperAssetTracker") (layer "F.Cu")',
    '  (descr "SIM7670G-LNGV C45935408; JLCEDA/EasyEDA Official Library; https://lceda.cn/ https://easyeda.com")',
    '  (attr smd)',
    '  (fp_text reference "REF**" (at 0 -13.5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',
    '  (fp_text value "SIM7670G-LNGV" (at 0 13.5) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))',
]
seen = set()
for shape in geometry["shape"]:
    fields = shape.split("~")
    if fields[0] != "PAD":
        continue
    kind, x, y, width, height, layer, net, number, hole = fields[1:10]
    assert layer == "1" and float(hole) == 0 and kind in {"RECT", "OVAL"}
    assert number.isdecimal() and number not in seen
    seen.add(number)
    x, y = (float(x) - ox) * 0.254, (float(y) - oy) * 0.254
    width, height = float(width) * 0.254, float(height) * 0.254
    angle = float(fields[11])
    lines.append(f'  (pad "{number}" smd {"rect" if kind == "RECT" else "oval"} (at {x:.6f} {y:.6f} {angle:g}) (size {width:.6f} {height:.6f}) (layers "F.Cu" "F.Paste" "F.Mask"))')
assert seen == {str(n) for n in range(1, 125)}, "Incomplete modem footprint"
lines += [
    '  (fp_rect (start -12 -12) (end 12 12) (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))',
    '  (fp_rect (start -13 -13) (end 13 13) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))',
    # Authored orientation marker beside pad 1, inside the body outline.
    # The former marker overlaid pad 1's exposed solder-mask opening.
    '  (fp_circle (center -10.5 -8) (end -10.3 -8) (stroke (width 0.12) (type default)) (fill solid) (layer "F.SilkS"))',
    ')',
]
output = Path(__file__).resolve().parent / "footprints/SIM7670G_LNGV.kicad_mod"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {len(seen)} pads; input SHA256 {hashlib.sha256(source.read_bytes()).hexdigest()}")
