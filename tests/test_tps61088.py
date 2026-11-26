"""Source-backed pin map and qualification gates for the boost supply parts."""
from pathlib import Path

from copper_cli import audit_footprints, compile_board, part, pins
from contracts import REQUIRED, load_contract

ROOT = Path(__file__).resolve().parents[1]


def test_boost_pin_map_keeps_power_contacts_separate():
    ir = compile_board('''board BoostPart {
        import boost "github.com/andenore/CopperLib/packages/parts/ti/tps61088";
        import coil "github.com/andenore/CopperLib/packages/parts/bourns/srp1265a";
        component U: boost.TPS61088RHLR;
        component L: coil.SRP1265A_2R2M;
    }''')
    # TI SLVUAF2 Figure 7, including exposed PGND as pad 21.
    assert pins(ir, "boost.TPS61088RHLR") == {
        "VCC":"1", "EN":"2", "FSW":"3", "SW_4":"4", "SW_5":"5",
        "SW_6":"6", "SW_7":"7", "BOOT":"8", "VIN":"9", "SS":"10",
        "NC_11":"11", "NC_12":"12", "MODE":"13", "VOUT_14":"14",
        "VOUT_15":"15", "VOUT_16":"16", "FB":"17", "COMP":"18",
        "ILIM":"19", "AGND":"20", "PGND":"21",
    }
    assert pins(ir, "coil.SRP1265A_2R2M") == {"A":"1", "B":"2"}


def test_boost_preserves_external_qualification_gates():
    contract = load_contract(ROOT / "packages/parts/ti/tps61088/qualification.json")
    assert contract["production_publishable"] is False
    assert REQUIRED["power"] <= {r["id"] for r in contract["requirements"]}
    assert all(r["algorithm"] == "external" for r in contract["requirements"])
    assert "datasheet-package-review" in {r["id"] for r in contract["requirements"]}
    inductor = load_contract(ROOT / "packages/parts/bourns/srp1265a/qualification.json")
    assert inductor["production_publishable"] is False


def test_rhl_land_pattern_supported_without_losing_contacts():
    source = '''board RhlFootprint {
        import b "github.com/andenore/CopperLib/packages/parts/ti/tps61088";
        component U: b.TPS61088RHLR;
    }'''
    assert audit_footprints(source, strict=True)["passed"]
    import re
    text = (ROOT / "packages/parts/ti/tps61088/footprints/TI_RHL0020A_TPS61088.kicad_mod").read_text()
    # TI 4219071/A: twenty signal contacts, four ground fingers, eight stencil apertures.
    assert set(re.findall(r'\(pad (\d+) smd', text)) == {str(n) for n in range(1, 22)}
    assert text.count('(pad 21 smd roundrect') == 4
    assert text.count('(pad "" smd rect') == 8
    assert 'smd custom' not in text
    # The two overlapping rectangles preserve the exact stepped central copper.
    shapes = re.findall(r'\(pad 21 smd rect \(at ([\d.-]+) ([\d.-]+)\) \(size ([\d.]+) ([\d.]+)\)', text)
    assert {tuple(map(float, s)) for s in shapes} == {(0, 0, 2.05, 3.05), (0, 0, .75, 3.85)}
    # Central area 2.05*3.05 plus two .75*.4 extensions (not its bounding box).
    area = 2.05*3.05 + .75*3.85 - .75*3.05
    assert abs(area - 6.8525) < 1e-12


def test_boost_hot_loop_uses_output_contacts_not_control_supply():
    # TI SLVA790A sections 2.1-2.2 / Figures 1-3: output switching loop.
    ir = compile_board('''board BoostEmiTerminals {
        import boost "github.com/andenore/CopperLib/packages/parts/ti/tps61088";
        component U: boost.TPS61088RHLR;
    }''')
    definition = part(ir, "boost.TPS61088RHLR")
    roles = {name: pin["profile"].get("emi", {}).get("role")
             for name, pin in definition["pins"].items()}
    assert {name for name, role in roles.items() if role == "hot_supply"} == {
        "VOUT_14", "VOUT_15", "VOUT_16",
    }
    assert {name for name, role in roles.items() if role == "hot_return"} == {"PGND"}
    assert {name for name, role in roles.items() if role == "switch"} == {
        "SW_4", "SW_5", "SW_6", "SW_7",
    }
    assert roles["VIN"] is None
    assert roles["FB"] == "feedback"
