"""Offline geometry checks for the pinned JLCPCB/EasyEDA EG800G-EU asset."""

from pathlib import Path
import importlib.util
import shutil
import subprocess

import pytest

from pcbir import BoardOutline, KiCadPcbBackend, PhysicalBoard, Placement, Point, load_kicad_mod
_spec = importlib.util.spec_from_file_location(
    "eg800g_generator", Path(__file__).resolve().parents[1] / "packages/parts/quectel/eg800g-eu/generate_footprint.py"
)
_generator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_generator)
DESTINATION, PART_URL, SHAPE_SHA256 = _generator.DESTINATION, _generator.PART_URL, _generator.SHAPE_SHA256


def test_eg800g_eu_footprint_has_all_109_distinct_lands():
    footprint = load_kicad_mod(DESTINATION).footprint
    pads = {pad.number: pad for pad in footprint.pads}

    assert PART_URL.endswith("C9900097440")
    assert len(SHAPE_SHA256) == 64
    assert len(footprint.pads) == 109
    assert set(pads) == {str(number) for number in range(1, 110)}
    assert all(pad.has_solder_mask and pad.has_solder_paste for pad in pads.values())
    # Values below are independent checks of the EasyEDA LCC-109 coordinates.
    assert abs(pads["1"].position.x_nm + 7_750_000) <= 100
    assert abs(pads["1"].position.y_nm + 6_600_000) <= 100
    assert abs(pads["35"].position.x_nm - 7_750_000) <= 100
    assert abs(pads["42"].position.y_nm + 8_700_000) <= 100
    assert abs(pads["1"].size.width_nm - 2_300_000) <= 100
    assert abs(pads["1"].size.height_nm - 600_000) <= 100


def test_eg800g_eu_footprint_exports_through_kicad(tmp_path: Path):
    cli = shutil.which("kicad-cli") or "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
    if not Path(cli).is_file():
        pytest.skip("KiCad 10 is not installed")
    footprint = load_kicad_mod(DESTINATION).footprint
    board = PhysicalBoard(
        name="EG800G_EU_LandPattern", outline=BoardOutline.rectangle(50, 50),
        footprints={footprint.name: footprint},
        placements=(Placement("U1", footprint.name, Point.mm(25, 25)),), nets=(),
    )
    pcb = tmp_path / "EG800G_EU_LandPattern.kicad_pcb"
    pcb.write_text(KiCadPcbBackend().generate(board).artifacts[0].content, encoding="utf-8")
    result = subprocess.run(
        [cli, "pcb", "export", "svg", "--mode-multi", "--layers", "F.Cu,F.Paste",
         "--output", str(tmp_path), str(pcb)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
