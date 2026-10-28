"""USB-C and wire-to-board connectors, a crystal, indicator LEDs and the generic resistor."""
import json
import os
from pathlib import Path

import pytest
from copper_cli import audit_footprints, check, compile_board, part, pins

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "packages/parts"
KICAD_FOOTPRINTS = Path(os.environ.get("KICAD10_FOOTPRINT_DIR", "/usr/share/kicad/footprints"))
LIB = "github.com/andenore/CopperLib/packages"

LEDS = (
    "EVERLIGHT_19_217_GHC_YR1S2_6T",
    "EVERLIGHT_19_217_BHC_ZL1M2RY_6T",
    "EVERLIGHT_19_217_Y5C_AP1Q2_6T",
)

SOURCE = f'''board MiscPartsFixture {{
    import passives "{LIB}/generic/passives";
    import gct "{LIB}/parts/gct/usb4105";
    import jst "{LIB}/parts/jst/ph-s3b-sm4";
    import yxc "{LIB}/parts/yxc/ysx321sl";
    import ndk "{LIB}/parts/ndk/nx2016sa";
    import everlight "{LIB}/parts/everlight/19-217";
    component J_USB: gct.GCT_USB4105_GF_A;
    component J_BAT: jst.JST_S3B_PH_SM4_TB;
    component Y1: yxc.YXC_X322525MOB4SI;
    component Y2: ndk.NDK_NX2016SA_25MHZ_STD_CZS_2;
    component D_G: everlight.EVERLIGHT_19_217_GHC_YR1S2_6T;
    component D_B: everlight.EVERLIGHT_19_217_BHC_ZL1M2RY_6T;
    component D_Y: everlight.EVERLIGHT_19_217_Y5C_AP1Q2_6T;
    component R_CC1: passives.RESISTOR {{ value = 5.1kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }}
    component R_CC2: passives.RESISTOR {{ value = 5.1kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }}
    component R_LED: passives.RESISTOR {{ value = 1kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }}
    net VBUS {{ J_USB.VBUS_A4; J_USB.VBUS_A9; J_USB.VBUS_B4; J_USB.VBUS_B9; R_LED.P1; }}
    net LED_A {{ R_LED.P2; D_G.A; D_B.A; D_Y.A; }}
    net USB_DP {{ J_USB.DP1; J_USB.DP2; }}
    net USB_DN {{ J_USB.DN1; J_USB.DN2; }}
    net CC1 {{ J_USB.CC1; R_CC1.P1; }}
    net CC2 {{ J_USB.CC2; R_CC2.P1; }}
    net VBAT {{ J_BAT.P1; }}
    net NTC {{ J_BAT.P3; }}
    net XTAL_1 {{ Y1.XTAL1; }}
    net XTAL_2 {{ Y1.XTAL2; }}
    net XTAL_3 {{ Y2.XTAL1; }}
    net XTAL_4 {{ Y2.XTAL2; }}
    net GND {{
        J_USB.GND_A1; J_USB.GND_A12; J_USB.GND_B1; J_USB.GND_B12; J_USB.SHIELD;
        J_BAT.P2; J_BAT.MP; Y1.GND_2; Y1.GND_4; Y2.GND_2; Y2.GND_4; R_CC1.P2; R_CC2.P2;
        D_G.K; D_B.K; D_Y.K;
    }}
}}'''


@pytest.fixture(scope="module")
def board():
    return compile_board(SOURCE)


def _evidence(path):
    return json.loads((PARTS / path).read_text(encoding="utf-8"))


def _assert_footprint_covers_pins(footprint_id):
    """The audit resolves the footprint and its numbered pads equal the part's pin numbers.

    Package-local footprints always resolve and are audited strictly; KiCad library ids
    need an installed library."""
    if footprint_id.endswith(".kicad_mod"):
        audit = audit_footprints(SOURCE)
    else:
        if not KICAD_FOOTPRINTS.is_dir():
            pytest.skip(f"KiCad footprint library not installed: {KICAD_FOOTPRINTS}")
        audit = audit_footprints(SOURCE, KICAD_FOOTPRINTS, strict=False)
    (entry,) = [entry for entry in audit["entries"] if entry["reference"] == footprint_id]
    assert entry["passed"], entry["errors"]


def test_board_with_all_parts_passes_erc(board):
    assert check(SOURCE) == []
    for component in board["components"]:
        definition = part(board, component["part"])
        if component["part"].startswith("passives."):
            continue
        assert definition["manufacturer"] and definition["source"] and definition["footprints"]
        assert definition["source"]["checksum"].startswith("sha256:") and definition["source"]["url"]


def test_generic_resistor_matches_capacitor_abstraction(board):
    resistor = part(board, "passives.RESISTOR")
    capacitor = part(board, "passives.CAPACITOR")
    assert resistor["category"] == "passive.resistor"
    assert resistor["footprints"] == [] and resistor["source"] is None
    assert pins(board, "passives.RESISTOR") == pins(board, "passives.CAPACITOR") == {"P1": "1", "P2": "2"}
    for name in ("P1", "P2"):
        assert resistor["pins"][name]["profile"] == capacitor["pins"][name]["profile"]


@pytest.mark.parametrize(("name", "evidence"), [
    ("gct.GCT_USB4105_GF_A", "gct/usb4105/evidence/usb4105-audit.json"),
    ("jst.JST_S3B_PH_SM4_TB", "jst/ph-s3b-sm4/evidence/s3b-ph-sm4-audit.json"),
    ("yxc.YXC_X322525MOB4SI", "yxc/ysx321sl/evidence/x322525mob4si-audit.json"),
    ("ndk.NDK_NX2016SA_25MHZ_STD_CZS_2", "ndk/nx2016sa/evidence/nx2016sa-25mhz-std-czs-2-audit.json"),
])
def test_connector_and_crystal_pins_cover_every_footprint_pad(board, name, evidence):
    numbers = pins(board, name)
    record = _evidence(evidence)
    assert numbers == record["semantic_pins"]
    assert len(set(numbers.values())) == len(numbers)  # one pin per pad number
    definition = part(board, name)
    assert definition["source"]["checksum"] == "sha256:" + record["source"]["sha256"]
    (footprint,) = definition["footprints"]
    assert footprint.endswith(record["footprint"])
    _assert_footprint_covers_pins(footprint)


def test_usb4105_transcription_and_shared_lands(board):
    numbers = pins(board, "gct.GCT_USB4105_GF_A")
    record = _evidence("gct/usb4105/evidence/usb4105-audit.json")
    expected = {}
    for number, signal in record["signals"].items():
        if number == "SHELL":
            expected["SHIELD"] = "SH"
        elif signal in {"GND", "VBUS"}:
            expected[f"{signal}_{number}"] = number
        else:
            expected[signal.upper()] = number
    assert numbers == expected
    assert (numbers["CC1"], numbers["CC2"]) == ("A5", "B5")
    assert (numbers["DP1"], numbers["DN1"], numbers["DP2"], numbers["DN2"]) == ("A6", "A7", "B6", "B7")
    assert part(board, "gct.GCT_USB4105_GF_A")["internal_pad_groups"] == []
    function = {number: name.split("_")[0] for name, number in numbers.items()}
    for first, second in record["shared_lands"]:
        assert function[first] == function[second] in {"GND", "VBUS"}


def test_crystal_terminals_match_yxc_layout(board):
    numbers = pins(board, "yxc.YXC_X322525MOB4SI")
    record = _evidence("yxc/ysx321sl/evidence/x322525mob4si-audit.json")
    assert {numbers["XTAL1"], numbers["XTAL2"]} == {n for n, f in record["terminals"].items() if f == "crystal"} == {"1", "3"}
    assert {numbers["GND_2"], numbers["GND_4"]} == {n for n, f in record["terminals"].items() if f == "GND"}
    assert part(board, "yxc.YXC_X322525MOB4SI")["internal_pad_groups"] == []
    assert "12 pF" in record["distributor_catalogue_C9006"]["load_capacitance"]
    assert any("load capacitance" in item for item in record["unresolved"])


def test_ndk_crystal_cover_joins_the_ground_pads(board):
    name = "ndk.NDK_NX2016SA_25MHZ_STD_CZS_2"
    numbers = pins(board, name)
    record = _evidence("ndk/nx2016sa/evidence/nx2016sa-25mhz-std-czs-2-audit.json")
    assert {numbers["XTAL1"], numbers["XTAL2"]} == {n for n, f in record["terminals"].items() if f == "crystal"} == {"1", "3"}
    assert {numbers["GND_2"], numbers["GND_4"]} == {n for n, f in record["terminals"].items() if f == "GND"} == {"2", "4"}
    # The catalogue states #2 and #4 are connected through the cover.
    assert [sorted(group) for group in part(board, name)["internal_pad_groups"]] == record["internal_pad_groups"]
    assert "8 pF" in record["distributor_catalogue_C843258"]["load_capacitance"]
    assert any("STD-CZS-2" in item for item in record["unresolved"])


@pytest.mark.parametrize("name", LEDS)
def test_everlight_led_polarity_follows_manufacturer_terminals(board, name):
    record = _evidence("everlight/19-217/evidence/19-217-audit.json")
    assert record["polarity"]["1"].startswith("anode") and record["polarity"]["2"].startswith("cathode")
    assert pins(board, f"everlight.{name}") == {"A": "1", "K": "2"}  # transcribed: terminal 1 "+", terminal 2 "-"
    definition = part(board, f"everlight.{name}")
    assert definition["source"]["checksum"] == "sha256:" + record["parts"][name]["sha256"]
    assert definition["source"]["url"] == record["parts"][name]["url"]
    (footprint,) = definition["footprints"]
    assert footprint.endswith(record["footprint"])
    assert "LED_SMD:LED_0603_1608Metric" not in footprint  # KiCad generic is K=1, A=2
    _assert_footprint_covers_pins(footprint)
