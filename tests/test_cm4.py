"""Real CM4 carrier contacts are not a fabricated active device model."""
from decimal import Decimal
from pathlib import Path
import json
import subprocess
import sys

import pytest
from copper_cli import check, compile_board, part

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "packages/profiles/raspberry_pi/cm4/evidence/pinout.json").read_text())


def source():
    grounds = []
    for row in DATA["pins"]:
        if row["signal"] == "GND":
            ref = "J1" if row["cm4_pin"] <= 100 else "J2"
            grounds.append(f'{ref}.GND_{row["cm4_pin"]};')
    return '''board Carrier {
        import cm4 "github.com/andenore/CopperLib/packages/profiles/raspberry_pi/cm4";
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


def test_socket_pin_table_is_complete_and_local_numbered():
    assert check(source()) == []
    board = compile_board(source())
    j1, j2 = (part(board, f"cm4.{name}") for name in ("CM4_GPIO_SOCKET", "CM4_HS_SOCKET"))
    for socket in (j1, j2):
        assert {p["number"] for p in socket["pins"].values()} == {str(n) for n in range(1, 101)}
        assert not socket["internal_pad_groups"]
        assert socket["manufacturer"] == "Hirose Electric"
        assert socket["source"]["checksum"] == "sha256:" + DATA["source"]["sha256"]
        for pin in socket["pins"].values():
            if "power" not in pin["profile"]["domains"]:
                assert pin["profile"]["directions"] == ["passive"]
    assert j1["pins"]["GPIO14"]["number"] == "55"
    assert j1["pins"]["GPIO15"]["number"] == "51"
    assert j1["pins"]["GPIO_VREF"]["connection_policy"] == "required"
    assert j2["pins"]["USB_N"]["number"] == "3"
    assert j2["pins"]["USB_P"]["number"] == "5"
    assert j2["pins"]["GND_107"]["number"] == "7"
    assert j2["pins"]["HDMI0_SCL"]["number"] == "100"


@pytest.mark.parametrize("edit,code", [
    (lambda t: t.replace("J2.GND_107;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("J1.V5_87;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("J1.GPIO_VREF;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("voltage = 5V", "voltage = 5.5V"), "SUPPLY_VOLTAGE_HIGH"),
    (lambda t: t.replace("net GND {", "net GND { J1.RESERVED_76;"), "DO_NOT_CONNECT"),
    (lambda t: t.replace("net GND {", "net GND { J2.RESERVED_104;"), "DO_NOT_CONNECT"),
])
def test_required_and_reserved_contacts_are_not_silently_waived(edit, code):
    assert code in {d["code"] for d in check(edit(source()))}


def test_profile_fragment_has_two_explicit_bindings_and_four_holes():
    mechanical = compile_board(source())["mechanical"]
    # The board owns the outline; the mounting profile contributes none.
    assert not any(feature["kind"] == "outline" and feature["instance"] == "cm"
                   for feature in mechanical["provenance"]["features"])
    assert len(mechanical["connectors"]) == 2
    assert len(mechanical["holes"]) == 4
    assert all(h["diameter_nm"] == 2700000 for h in mechanical["holes"])
    assert {(c["reference"], c["anchor_pad"]) for c in mechanical["connectors"]} == {("J1", "1"), ("J2", "1")}
    assert len(mechanical["keepouts"]) == 5
    assert all(k["maximum_height_nm"] is None for k in mechanical["keepouts"])


def test_cm4_generator_is_current():
    subprocess.run([sys.executable, str(ROOT / "packages/profiles/raspberry_pi/cm4/generate.py"), "--check"], check=True)


def test_rotated_mounting_is_a_rigid_transform_with_unchanged_contact_identity():
    original=compile_board(source())['mechanical']
    rotated=compile_board(source().replace('cm4.CM4Mounting as','cm4.CM4Mounting180 as'))['mechanical']
    assert len(original['connectors'])==len(rotated['connectors'])==2
    for a,b in zip(original['connectors'],rotated['connectors']):
        assert (a['reference'],a['anchor_pad'],a['footprint'],a['side'])==(b['reference'],b['anchor_pad'],b['footprint'],b['side'])
        assert a['position']['x_nm']+b['position']['x_nm']==60000000
        assert a['position']['y_nm']+b['position']['y_nm']==75000000
        assert (Decimal(a['rotation'])+180)%360==Decimal(b['rotation'])
    assert len(original['holes'])==len(rotated['holes'])==4
    for a,b in zip(original['holes'],rotated['holes']):
        assert a['position']['x_nm']+b['position']['x_nm']==60000000
        assert a['position']['y_nm']+b['position']['y_nm']==75000000
        assert a['diameter_nm']==b['diameter_nm']
    assert len(original['keepouts'])==len(rotated['keepouts'])==5
