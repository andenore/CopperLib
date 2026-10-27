from pathlib import Path
import importlib.util
import shutil

from copper_cli import audit_footprints, compile_board, pins
_spec = importlib.util.spec_from_file_location(
    "max_m10s_generator", Path(__file__).resolve().parents[1] / "packages/parts/u-blox/max-m10s/generate_footprint.py"
)
_generator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_generator)
DESTINATION, render = _generator.DESTINATION, _generator.render
BOARD = 'board T { import u "github.com/andenore/CopperLib/packages/parts/u-blox/max-m10s"; component U: u.MAX_M10S_00B; }'


def test_source_backed_max_m10s_pattern_is_deterministic_and_complete(tmp_path):
    assert DESTINATION.read_text(encoding="utf-8") == render()
    assert set(pins(compile_board(BOARD), "u.MAX_M10S_00B").values()) == {str(n) for n in range(1, 19)}
    # The part names the footprint as MAX_M10S:u-blox_MAX-M10S; serve it from a library root.
    (tmp_path / "MAX_M10S.pretty").mkdir()
    shutil.copy(DESTINATION, tmp_path / "MAX_M10S.pretty" / DESTINATION.name)
    audit = audit_footprints(BOARD, tmp_path)
    assert audit["passed"], [entry["errors"] for entry in audit["entries"]]
