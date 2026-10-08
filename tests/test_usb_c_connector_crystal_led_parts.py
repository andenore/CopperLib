"""USB-C and wire-to-board connectors, a crystal, indicator LEDs and the generic resistor."""
import json
import os
import re
from pathlib import Path

import pytest
from pcbir import check, compile_source
from pcbir.importers import load_kicad_mod

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "packages/parts"
KICAD_FOOTPRINTS = Path(os.environ.get("KICAD10_FOOTPRINT_DIR", "/usr/share/kicad/footprints"))
LIB = "github.com/andenore/CopperLib/packages"

LEDS = (
    "EVERLIGHT_19_217_GHC_YR1S2_6T",
    "EVERLIGHT_19_217_BHC_ZL1M2RY_6T",
    "EVERLIGHT_19_217_Y5C_AP1Q2_6T",
)


@pytest.fixture(scope="module")
def board(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("misc-parts")
    (tmp / "copper.mod").write_text(
        "module misc-parts-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n", encoding="utf-8")
    return compile_source(f'''board MiscPartsFixture {{
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
    }}''', str(tmp / "board.copper"), offline=True)


def _pins(board, name):
    return {pin.name: pin.number for pin in board.library[name].pins.values()}


def _evidence(path):
    return json.loads((PARTS / path).read_text(encoding="utf-8"))


def _pads(footprint_id, package_dir):
    """Load a part footprint; relative ids are package-local, others KiCad."""
    if footprint_id.endswith(".kicad_mod"):
        path = PARTS / package_dir / footprint_id.split(f"parts/{package_dir}/", 1)[-1]
    else:
        library, name = footprint_id.split(":", 1)
        path = KICAD_FOOTPRINTS / f"{library}.pretty" / f"{name}.kicad_mod"
        if not path.is_file():
            pytest.skip(f"KiCad footprint library not installed: {path}")
    return load_kicad_mod(path).footprint.pads


def _numbers(pads):
    return {pad.number for pad in pads if pad.number}


def test_board_with_all_parts_passes_erc(board):
    assert check(board) == []
    for component in board.components:
        part = board.library[component.part]
        if component.part.startswith("passives."):
            continue
        assert part.manufacturer and part.source and part.footprints
        assert part.source.checksum.startswith("sha256:") and part.source.url


def test_generic_resistor_matches_capacitor_abstraction(board):
    resistor = board.library["passives.RESISTOR"]
    capacitor = board.library["passives.CAPACITOR"]
    assert resistor.category == "passive.resistor"
    assert resistor.footprints == () and resistor.source is None
    assert _pins(board, "passives.RESISTOR") == _pins(board, "passives.CAPACITOR") == {"P1": "1", "P2": "2"}
    for name in ("P1", "P2"):
        assert resistor.pins[name].profile == capacitor.pins[name].profile


@pytest.mark.parametrize(("part", "package_dir", "evidence"), [
    ("gct.GCT_USB4105_GF_A", "gct/usb4105", "gct/usb4105/evidence/usb4105-audit.json"),
    ("jst.JST_S3B_PH_SM4_TB", "jst/ph-s3b-sm4", "jst/ph-s3b-sm4/evidence/s3b-ph-sm4-audit.json"),
    ("yxc.YXC_X322525MOB4SI", "yxc/ysx321sl", "yxc/ysx321sl/evidence/x322525mob4si-audit.json"),
    ("ndk.NDK_NX2016SA_25MHZ_STD_CZS_2", "ndk/nx2016sa", "ndk/nx2016sa/evidence/nx2016sa-25mhz-std-czs-2-audit.json"),
])
def test_connector_and_crystal_pins_cover_every_footprint_pad(board, part, package_dir, evidence):
    pins = _pins(board, part)
    record = _evidence(evidence)
    assert pins == record["semantic_pins"]
    assert len(set(pins.values())) == len(pins)  # one pin per pad number
    definition = board.library[part]
    assert definition.source.checksum == "sha256:" + record["source"]["sha256"]
    (footprint,) = definition.footprints
    assert footprint.endswith(record["footprint"])
    assert _numbers(_pads(footprint, package_dir)) == set(pins.values())


def test_usb4105_transcription_and_shared_lands(board):
    pins = _pins(board, "gct.GCT_USB4105_GF_A")
    record = _evidence("gct/usb4105/evidence/usb4105-audit.json")
    expected = {}
    for number, signal in record["signals"].items():
        if number == "SHELL":
            expected["SHIELD"] = "SH"
        elif signal in {"GND", "VBUS"}:
            expected[f"{signal}_{number}"] = number
        else:
            expected[signal.upper()] = number
    assert pins == expected
    assert (pins["CC1"], pins["CC2"]) == ("A5", "B5")
    assert (pins["DP1"], pins["DN1"], pins["DP2"], pins["DN2"]) == ("A6", "A7", "B6", "B7")
    part = board.library["gct.GCT_USB4105_GF_A"]
    assert part.internal_pad_groups == ()
    pads = _pads(part.footprints[0], "gct/usb4105")
    by_number = {}
    for pad in pads:
        by_number.setdefault(pad.number, []).append(pad)
    assert len(by_number["SH"]) == 4 and len(by_number[""]) == 6  # 2 NPTH pegs + 4 paste apertures
    function = {number: name.split("_")[0] for name, number in pins.items()}
    for first, second in record["shared_lands"]:
        (a,), (b,) = by_number[first], by_number[second]
        assert (a.position, a.size) == (b.position, b.size)
        assert function[first] == function[second] in {"GND", "VBUS"}
    assert len({pad.position for pad in pads if pad.number and pad.number != "SH"}) == 12


def test_usb4105_local_footprint_keeps_kicad_copper():
    original = KICAD_FOOTPRINTS / "Connector_USB.pretty/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod"
    if not original.is_file():
        pytest.skip(f"KiCad footprint library not installed: {original}")
    local = load_kicad_mod(PARTS / "gct/usb4105/footprints/Connector_USB.pretty/"
                           "USB_C_Receptacle_GCT_USB4105-GF-A_16P_TopMnt_Horizontal.kicad_mod").footprint.pads
    text = original.read_text(encoding="utf-8")
    assert text.count('(pad "SH" thru_hole oval') == 4 and text.count('"*.Cu" "*.Mask" "F.Paste"') == 4
    copper = sorted((p.number, p.position.x_nm, p.position.y_nm, p.size.width_nm, p.size.height_nm,
                     p.drill and (p.drill.width_nm, p.drill.height_nm)) for p in local if p.kind.value != "aperture")
    # Independently parsed lands from the KiCad file (positions/sizes in mm).
    expected = []
    for block in re.findall(r'\(pad "([^"]*)" (\w+) \w+\s+\(at ([-\d.]+) ([-\d.]+)\)\s+\(size ([\d.]+) ([\d.]+)\)(?:\s+\(drill (?:oval )?([\d.]+)(?: ([\d.]+))?\))?', text):
        number, _, x, y, w, h, dw, dh = block
        nm = lambda v: round(float(v) * 1_000_000)
        drill = (nm(dw), nm(dh or dw)) if dw else None
        expected.append((number, nm(x), nm(y), nm(w), nm(h), drill))
    assert copper == sorted(expected)
    apertures = [p for p in local if p.kind.value == "aperture"]
    shells = [p for p in local if p.number == "SH"]
    outline = lambda p: (p.position.x_nm, p.position.y_nm, p.size.width_nm, p.size.height_nm)
    assert sorted(map(outline, apertures)) == sorted(map(outline, shells))
    assert all(p.has_solder_paste for p in apertures)


def test_jst_circuit_one_is_left_of_the_mating_tabs():
    pads = _pads("Connector_JST:JST_PH_S3B-PH-SM4-TB_1x03-1MP_P2.00mm_Horizontal", "jst/ph-s3b-sm4")
    signal = {pad.number: pad for pad in pads if pad.number in {"1", "2", "3"}}
    mounting = [pad for pad in pads if pad.number == "MP"]
    assert [signal[n].position.x_nm for n in ("1", "2", "3")] == [-2_000_000, 0, 2_000_000]
    assert len(mounting) == 2
    assert sorted(pad.position.x_nm for pad in mounting) == [-4_350_000, 4_350_000]
    assert all(pad.size.width_nm == 1_500_000 and pad.size.height_nm == 3_400_000 for pad in mounting)
    # Reinforcement lands lie on the mating side (KiCad +y), signal lands opposite.
    assert all(pad.position.y_nm > 0 for pad in mounting)
    assert all(pad.position.y_nm < 0 for pad in signal.values())


def test_crystal_terminals_are_diagonal_and_match_yxc_layout(board):
    pins = _pins(board, "yxc.YXC_X322525MOB4SI")
    record = _evidence("yxc/ysx321sl/evidence/x322525mob4si-audit.json")
    assert {pins["XTAL1"], pins["XTAL2"]} == {n for n, f in record["terminals"].items() if f == "crystal"} == {"1", "3"}
    assert {pins["GND_2"], pins["GND_4"]} == {n for n, f in record["terminals"].items() if f == "GND"}
    part = board.library["yxc.YXC_X322525MOB4SI"]
    assert part.internal_pad_groups == ()
    pads = {pad.number: pad for pad in _pads(part.footprints[0], "yxc/ysx321sl")}
    for number, (x, y) in record["footprint_checks"]["pad_centres_mm"].items():
        assert (pads[number].position.x_nm, pads[number].position.y_nm) == (round(x * 1e6), round(y * 1e6))
        assert (pads[number].size.width_nm, pads[number].size.height_nm) == (1_400_000, 1_200_000)
    xtal = [pads[pins[name]].position for name in ("XTAL1", "XTAL2")]
    assert xtal[0].x_nm == -xtal[1].x_nm and xtal[0].y_nm == -xtal[1].y_nm  # diagonal pair
    assert "12 pF" in record["distributor_catalogue_C9006"]["load_capacitance"]
    assert any("load capacitance" in item for item in record["unresolved"])


def test_ndk_crystal_terminals_are_diagonal_and_its_cover_joins_the_ground_pads(board):
    name = "ndk.NDK_NX2016SA_25MHZ_STD_CZS_2"
    pins = _pins(board, name)
    record = _evidence("ndk/nx2016sa/evidence/nx2016sa-25mhz-std-czs-2-audit.json")
    assert {pins["XTAL1"], pins["XTAL2"]} == {n for n, f in record["terminals"].items() if f == "crystal"} == {"1", "3"}
    assert {pins["GND_2"], pins["GND_4"]} == {n for n, f in record["terminals"].items() if f == "GND"} == {"2", "4"}
    part = board.library[name]
    # The catalogue states #2 and #4 are connected through the cover.
    assert [sorted(group.numbers) for group in part.internal_pad_groups] == record["internal_pad_groups"]
    pads = {pad.number: pad for pad in _pads(part.footprints[0], "ndk/nx2016sa")}
    for number, (x, y) in record["footprint_checks"]["pad_centres_mm"].items():
        assert (pads[number].position.x_nm, pads[number].position.y_nm) == (round(x * 1e6), round(y * 1e6))
        assert (pads[number].size.width_nm, pads[number].size.height_nm) == (900_000, 800_000)
        # KiCad's land covers NDK's recommended 0.85 x 0.75 mm land at 1.35 x 1.05 mm pitch.
        assert abs(pads[number].position.x_nm) + 450_000 >= 675_000 + 425_000
        assert abs(pads[number].position.x_nm) - 450_000 <= 675_000 - 425_000
        assert abs(pads[number].position.y_nm) + 400_000 >= 525_000 + 375_000
        assert abs(pads[number].position.y_nm) - 400_000 <= 525_000 - 375_000
    xtal = [pads[pins[name]].position for name in ("XTAL1", "XTAL2")]
    assert xtal[0].x_nm == -xtal[1].x_nm and xtal[0].y_nm == -xtal[1].y_nm  # diagonal pair
    assert "8 pF" in record["distributor_catalogue_C843258"]["load_capacitance"]
    assert any("STD-CZS-2" in item for item in record["unresolved"])


@pytest.mark.parametrize("name", LEDS)
def test_everlight_led_polarity_follows_manufacturer_terminals(board, name):
    record = _evidence("everlight/19-217/evidence/19-217-audit.json")
    assert record["polarity"]["1"].startswith("anode") and record["polarity"]["2"].startswith("cathode")
    pins = _pins(board, f"everlight.{name}")
    assert pins == {"A": "1", "K": "2"}  # transcribed: terminal 1 "+", terminal 2 "-"
    part = board.library[f"everlight.{name}"]
    assert part.source.checksum == "sha256:" + record["parts"][name]["sha256"]
    assert part.source.url == record["parts"][name]["url"]
    (footprint,) = part.footprints
    assert footprint.endswith(record["footprint"])
    assert "LED_SMD:LED_0603_1608Metric" not in footprint  # KiCad generic is K=1, A=2
    pads = {pad.number: pad for pad in _pads(footprint, "everlight/19-217")}
    assert set(pads) == set(pins.values())
    cathode, anode = pads[pins["K"]], pads[pins["A"]]
    assert cathode.position.x_nm == -787_500 and anode.position.x_nm == 787_500
    assert cathode.size.width_nm == anode.size.width_nm == 875_000


def test_everlight_footprint_marks_the_cathode_side():
    footprint = load_kicad_mod(PARTS / "everlight/19-217/footprints/EVERLIGHT_19-217.kicad_mod").footprint
    pads = {pad.number: pad for pad in footprint.pads}
    assert pads["2"].position.x_nm < 0 < pads["1"].position.x_nm
    text = (PARTS / "everlight/19-217/footprints/EVERLIGHT_19-217.kicad_mod").read_text(encoding="utf-8")
    # The closed silkscreen end and the chamfered fab corner are on the cathode (-x) side.
    assert '(fp_line (start -1.485 -0.735) (end -1.485 0.735)' in text
    assert '(fp_line (start -0.5 -0.4) (end -0.8 -0.1)' in text
    generic = KICAD_FOOTPRINTS / "LED_SMD.pretty/LED_0603_1608Metric.kicad_mod"
    if generic.is_file():
        kicad = {pad.number: pad for pad in load_kicad_mod(generic).footprint.pads}
        assert kicad["1"].position == pads["2"].position  # same cathode land, swapped number
        assert kicad["2"].position == pads["1"].position
        assert kicad["1"].size == pads["2"].size
