"""Public-CLI geometry checks; managed footprint cache is an explicit input."""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from copper_cli import COMMAND, ROOT


PACKAGE = ROOT / "packages/circuits/nordic/nrf52832-qfaa-ground-escape"
FOOTPRINT = "github.com/KiCad/kicad-footprints/Package_DFN_QFN.pretty/QFN-48-1EP_6x6mm_P0.4mm_EP4.2x4.2mm.kicad_mod"


@pytest.fixture(scope="module")
def fixture(tmp_path_factory):
    cache = os.environ.get("COPPER_MACRO_FOOTPRINTS")
    if not cache:
        pytest.skip("set COPPER_MACRO_FOOTPRINTS to the managed KiCad footprint provider cache")
    directory = tmp_path_factory.mktemp("nrf-ground-escape")
    (directory / "layouts").mkdir()
    shutil.copyfile(PACKAGE / "layout.copper", directory / "layouts/layout.copper")
    (directory / "copper.mod").write_text(
        "module nrf-ground-escape-test\n"
        "require github.com/KiCad/kicad-footprints 7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd\n"
        f"replace github.com/KiCad/kicad-footprints => {Path(cache).as_posix()}\n",
        encoding="utf-8",
    )
    (directory / "parts").mkdir()
    # A mechanical test vehicle: all real lands, two connected contacts.
    other_pins = " ".join(
        f'pin P{i} {{ number = "{i}"; domains = "analog"; directions = "passive"; }}'
        for i in range(1, 50) if i not in (45, 49))
    (directory / "parts/part.copper").write_text(
        f'part GroundTest {{ footprint = "{FOOTPRINT}"; '
        'pin EP { number = "49"; domains = "ground"; directions = "passive"; } '
        'pin G { number = "45"; domains = "ground"; directions = "passive"; } '
        + other_pins + ' }', encoding="utf-8")
    return directory


def call(directory, *arguments):
    return subprocess.run([*COMMAND, *arguments], cwd=directory, capture_output=True,
                          text=True, encoding="utf-8", timeout=120)


def source(wrong_net=False):
    connections = 'net GND { U.EP; } net WRONG { U.G; }' if wrong_net else 'net GND { U.EP; U.G; }'
    unused = ', '.join(f'U.P{i}' for i in range(1, 50) if i not in (45, 49))
    return '''board GroundEscapeTest {
        build { fab_profile = "jlcpcb-four-layer"; }
        import parts "./parts";
        import layouts "./layouts";
        component U: parts.GroundTest;
        CONNECTIONS
        no_connect UNUSED { reason = "Unconnected physical clearance obstacles in a ground-only fixture"; }
        supply GROUND { net = GND; voltage = 0V; external = true; }
        constraint fixed_placement(U) { x = 15mm; y = 15mm; rotation = 90; }
        physical_macro GROUND_EXIT: layouts.NRF52832_QFAA_EP_GROUND_ESCAPE {
            member U = U; net ground = GND;
        }
    }'''.replace("CONNECTIONS", connections).replace("UNUSED", unused)


def test_compiled_contract_needs_no_via_process_or_internal_plane(fixture):
    result = call(fixture, "compile-macro", "layouts/layout.copper", "--offline", "-o", "layout.json")
    assert result.returncode == 0, result.stdout + result.stderr
    asset = json.loads((fixture / "layout.json").read_text())
    assert asset["required_layers"] == ["F.Cu"]
    assert asset["vias"] == [] and asset["plane_returns"] == []
    assert not asset["production_publishable"]


def test_rotated_four_layer_host_closes_ground_without_via_in_pad(fixture):
    (fixture / "board.copper").write_text(source(), encoding="utf-8")
    result = call(fixture, "route-board", "board.copper", "--offline", "--layers", "4",
                  "--routing-profile", "quick", "--report", "route-report.json", "-o", "board.kicad_pcb")
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((fixture / "route-report.json").read_text())
    assert report["routing_complete"] is True


def test_host_cannot_bind_ground_exit_across_different_nets(fixture):
    (fixture / "wrong.copper").write_text(source(wrong_net=True), encoding="utf-8")
    result = call(fixture, "route-board", "wrong.copper", "--offline", "--layers", "4",
                  "--stop-after", "placement", "--report", "wrong-report.json", "-o", "wrong.kicad_pcb")
    assert result.returncode != 0
    assert "hard-macro pad/net mismatch" in result.stdout + result.stderr
    assert not (fixture / "wrong.kicad_pcb").exists()
