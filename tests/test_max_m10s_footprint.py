from pathlib import Path
import importlib.util
import shutil
import subprocess

import pytest

from pcbir import (
    BoardOutline, KiCadPcbBackend, PadKind, PhysicalBoard, Placement, Point,
    load_kicad_mod,
)
_spec = importlib.util.spec_from_file_location(
    "max_m10s_generator", Path(__file__).resolve().parents[1] / "packages/parts/u-blox/max-m10s/generate_footprint.py"
)
_generator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_generator)
DESTINATION, render = _generator.DESTINATION, _generator.render


def test_source_backed_max_m10s_pattern_is_deterministic_and_complete():
    assert DESTINATION.read_text(encoding="utf-8") == render()
    footprint = load_kicad_mod(DESTINATION).footprint
    copper = {pad.number: pad for pad in footprint.pads if pad.number}
    apertures = [pad for pad in footprint.pads if pad.kind is PadKind.APERTURE]

    assert set(copper) == {str(number) for number in range(1, 19)}
    assert len(apertures) == 36  # wide outer + narrow inner stencil for 18 lands
    assert copper["1"].position == Point.mm(-4.4, 4.75)
    assert copper["9"].position == Point.mm(4.4, 4.75)
    assert copper["10"].position == Point.mm(4.4, -4.75)
    assert copper["18"].position == Point.mm(-4.4, -4.75)
    assert copper["1"].size.width_nm == 700_000
    assert copper["2"].size.width_nm == 800_000
    assert all(not pad.has_solder_paste for pad in copper.values())
    assert sum(pad.size.height_nm == 1_400_000 for pad in apertures) == 18
    assert sum(pad.size.height_nm == 900_000 for pad in apertures) == 18


def test_max_m10s_pattern_exports_through_installed_kicad(tmp_path: Path):
    cli = shutil.which("kicad-cli") or "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
    if not Path(cli).is_file():
        pytest.skip("KiCad 10 is not installed")
    footprint = load_kicad_mod(DESTINATION).footprint
    board = PhysicalBoard(
        name="MAX_M10S_LandPattern", outline=BoardOutline.rectangle(30, 30),
        footprints={footprint.name: footprint},
        placements=(Placement("U1", footprint.name, Point.mm(15, 15)),), nets=(),
    )
    pcb = tmp_path / "MAX_M10S_LandPattern.kicad_pcb"
    pcb.write_text(KiCadPcbBackend().generate(board).artifacts[0].content, encoding="utf-8")
    result = subprocess.run(
        [cli, "pcb", "export", "svg", "--mode-multi", "--layers", "F.Cu,F.Paste", "--output", str(tmp_path), str(pcb)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
