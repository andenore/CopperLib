"""Offline checks for the pinned JLCPCB/EasyEDA EG800G-EU asset."""

from pathlib import Path
import importlib.util
import shutil

from copper_cli import audit_footprints, compile_board, pins
_spec = importlib.util.spec_from_file_location(
    "eg800g_generator", Path(__file__).resolve().parents[1] / "packages/parts/quectel/eg800g-eu/generate_footprint.py"
)
_generator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_generator)
DESTINATION, PART_URL, SHAPE_SHA256 = _generator.DESTINATION, _generator.PART_URL, _generator.SHAPE_SHA256
BOARD = 'board T { import q "github.com/andenore/CopperLib/packages/parts/quectel/eg800g-eu"; component U: q.EG800G_EU; }'


def test_eg800g_eu_footprint_lands_cover_all_109_pins(tmp_path):
    assert PART_URL.endswith("C9900097440")
    assert len(SHAPE_SHA256) == 64
    assert set(pins(compile_board(BOARD), "q.EG800G_EU").values()) == {str(n) for n in range(1, 110)}
    # The part names the footprint as EG800G:Quectel_EG800G; serve it from a library root.
    (tmp_path / "EG800G.pretty").mkdir()
    shutil.copy(DESTINATION, tmp_path / "EG800G.pretty" / DESTINATION.name)
    audit = audit_footprints(BOARD, tmp_path)
    assert audit["passed"], [entry["errors"] for entry in audit["entries"]]
