"""Real CM4 carrier contacts are not a fabricated active device model."""
from pathlib import Path
import json
import subprocess
import sys

import pytest
from pcbir import check, compile_source
from pcbir.compiler import compile_design_source
from pcbir.model import ConnectionPolicy, Direction, SignalDomain

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/cm4/pinout.json").read_text())


def source(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module cm4-test\nrequire github.com/andenore/CopperLib workspace\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    grounds = []
    for row in DATA["pins"]:
        if row["signal"] == "GND":
            ref = "J1" if row["cm4_pin"] <= 100 else "J2"
            grounds.append(f'{ref}.GND_{row["cm4_pin"]};')
    return '''board Carrier {
        import cm4 "github.com/andenore/CopperLib/packages/raspberry_pi_cm4";
        component J1: cm4.CM4_GPIO_SOCKET;
        component J2: cm4.CM4_HS_SOCKET;
        net GND { ''' + " ".join(grounds) + ''' }
        net V5 { J1.V5_77; J1.V5_79; J1.V5_81; J1.V5_83; J1.V5_85; J1.V5_87; }
        net V3V3 { J1.V3V3_84; J1.V3V3_86; J1.GPIO_VREF; }
        supply GND { voltage = 0V; external = true; }
        supply V5 { voltage = 5V; external = true; }
        supply V3V3 { voltage = 3.3V; external = true; }
        mechanical { outline rectangle { width = 70mm; height = 70mm; }
            use cm4.CM4Mounting as cm { gpio = J1; high_speed = J2; } }
    }'''


def compile_board(tmp_path, change=lambda text: text):
    return compile_source(change(source(tmp_path)), str(tmp_path / "board.copper"), offline=True)


def test_socket_pin_table_is_complete_and_local_numbered(tmp_path):
    board = compile_board(tmp_path)
    assert check(board) == []
    j1, j2 = (board.library[f"cm4.{name}"] for name in ("CM4_GPIO_SOCKET", "CM4_HS_SOCKET"))
    for part in (j1, j2):
        assert {p.number for p in part.pins.values()} == {str(n) for n in range(1, 101)}
        assert not part.internal_pad_groups
        assert part.manufacturer == "Hirose Electric"
        assert part.source.checksum == "sha256:" + DATA["source"]["sha256"]
        for pin in part.pins.values():
            if pin.profile.domains.isdisjoint({SignalDomain.POWER}):
                assert pin.profile.directions == {Direction.PASSIVE}
    assert j1.pins["GPIO14"].number == "55"
    assert j1.pins["GPIO15"].number == "51"
    assert j1.pins["GPIO_VREF"].connection_policy is ConnectionPolicy.REQUIRED
    assert j2.pins["USB_N"].number == "3"
    assert j2.pins["USB_P"].number == "5"
    assert j2.pins["GND_107"].number == "7"
    assert j2.pins["HDMI0_SCL"].number == "100"


@pytest.mark.parametrize("edit,code", [
    (lambda t: t.replace("J2.GND_107;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("J1.V5_87;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("J1.GPIO_VREF;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("voltage = 5V", "voltage = 5.5V"), "SUPPLY_VOLTAGE_HIGH"),
    (lambda t: t.replace("net GND {", "net GND { J1.RESERVED_76;"), "DO_NOT_CONNECT"),
    (lambda t: t.replace("net GND {", "net GND { J2.RESERVED_104;"), "DO_NOT_CONNECT"),
])
def test_required_and_reserved_contacts_are_not_silently_waived(tmp_path, edit, code):
    assert code in {d.code for d in check(compile_board(tmp_path, edit))}


def test_profile_fragment_has_two_explicit_bindings_and_four_holes(tmp_path):
    design = compile_design_source(source(tmp_path), str(tmp_path / "board.copper"), offline=True)
    from pcbir.parser import parse
    profile = parse((ROOT / "packages/raspberry_pi_cm4/mounting.copper").read_text())
    assert not any(getattr(d, "kind", None) == "outline" for d in profile.declarations)
    assert len(design.mechanical.connectors) == 2
    assert len(design.mechanical.holes) == 4
    assert all(h.diameter_nm == 2700000 for h in design.mechanical.holes)
    assert {(c.reference, c.anchor_pad) for c in design.mechanical.connectors} == {("J1", "1"), ("J2", "1")}
    assert len(design.mechanical.keepouts) == 5
    assert all(k.maximum_component_height_nm is None for k in design.mechanical.keepouts)


def test_cm4_generator_is_current():
    subprocess.run([sys.executable, str(ROOT / "scripts/generate_cm4.py"), "--check"], check=True)
