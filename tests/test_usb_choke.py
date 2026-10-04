"""Coilcraft schematic winding topology, not just pad-name coverage."""
import json
from pathlib import Path

from pcbir import check, compile_source

ROOT = Path(__file__).resolve().parents[1]


def test_usb_lanes_traverse_distinct_windings_with_matching_dot_polarity(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module choke-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    board = compile_source('''
        board ChokeAudit {
            import filter "github.com/andenore/CopperLib/packages/parts/coilcraft/0603usb";
            component FL: filter.COILCRAFT_0603USB_601MLC;
            net DP_IN { FL.DP_IN; }
            net DM_IN { FL.DM_IN; }
            net DP_OUT { FL.DP_OUT; }
            net DM_OUT { FL.DM_OUT; }
        }
    ''', str(tmp_path / "choke.copper"), offline=True)
    part = board.library["filter.COILCRAFT_0603USB_601MLC"]
    pins = {name: pin.number for name, pin in part.pins.items()}
    # Independently transcribed physical topology from page 1's schematic.
    windings = {frozenset({"1", "2"}), frozenset({"4", "3"})}
    lanes = {frozenset({pins[f"{lane}_IN"], pins[f"{lane}_OUT"]}) for lane in ("DP", "DM")}
    assert lanes == windings
    assert {pins["DP_IN"], pins["DM_IN"]} == {"1", "4"}  # dotted ends
    assert frozenset({pins["DP_IN"], pins["DM_IN"]}) not in windings
    assert frozenset({pins["DP_OUT"], pins["DM_OUT"]}) not in windings
    evidence = json.loads((ROOT / "packages/parts/coilcraft/0603usb/evidence/usb-choke-audit.json").read_text())
    assert pins == evidence["semantic_pins"]
    assert {frozenset(pair) for pair in evidence["windings"]} == windings
    assert set(evidence["dotted_ends"]) == {"1", "4"}
    assert part.source.checksum == "sha256:" + evidence["source"]["sha256"]
    assert part.footprints == (evidence["footprint"],)
    assert evidence["production_publishable"] is False
    assert check(board) == []
