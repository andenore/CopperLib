"""Source-backed TI power-mux, charger, I2C-translator and ESD parts: pin/pad coverage and a compiling fixture."""
import os
from pathlib import Path

import pytest
from pcbir import check, compile_source, load_kicad_mod
from pcbir.model import ConnectionPolicy, Direction, DriveMode

ROOT = Path(__file__).resolve().parents[1]
KICAD_FOOTPRINTS = Path(os.environ.get("KICAD10_FOOTPRINT_DIR", "/usr/share/kicad/footprints"))

PARTS = {
    "mux.TPS2121RUXR": {
        "OUT_1": "1", "IN2": "2", "CP2": "3", "OV2": "4", "OV1": "5", "PR1": "6",
        "IN1": "7", "OUT_8": "8", "ST": "9", "ILM": "10", "SS": "11", "GND": "12",
    },
    "chg.BQ24072RGTR": {
        "TS": "1", "BAT_2": "2", "BAT_3": "3", "CE": "4", "EN2": "5", "EN1": "6",
        "PGOOD": "7", "VSS": "8", "CHG": "9", "OUT_10": "10", "OUT_11": "11",
        "ILIM": "12", "IN": "13", "TMR": "14", "TD": "15", "ISET": "16", "EP": "17",
    },
    "lvl.TCA9406DCUR": {
        "SDA_B": "1", "GND": "2", "VCCA": "3", "SDA_A": "4", "SCL_A": "5", "OE": "6",
        "VCCB": "7", "SCL_B": "8",
    },
    "esd.TPD4E1U06DBVR": {
        "D1_P": "1", "GND": "2", "D2_P": "3", "D2_N": "4", "NC": "5", "D1_N": "6",
    },
}

CHECKSUMS = {
    "mux.TPS2121RUXR": "b2f5950f596dc2c4ca33e4ebac27fd35e4dcc68ea63e173466123e1118e91a06",
    "chg.BQ24072RGTR": "4fe4e4f9855501f83b400c6932e3098439e51c50539e40dc45b44a8d509e8db1",
    "lvl.TCA9406DCUR": "fdb80d682fbacd5ef18cbafc57e4d9375a295daa38da33721af6e055f8a7da61",
    "esd.TPD4E1U06DBVR": "f2cf0c3dcadf31c762a88e2b140df7ab3538082e7e3d7bccf0ef52afedf23f3e",
}

BOARD = '''board TiPartsFixture {
    import mux "github.com/andenore/CopperLib/packages/parts/ti/tps2121";
    import chg "github.com/andenore/CopperLib/packages/parts/ti/bq24072";
    import lvl "github.com/andenore/CopperLib/packages/parts/ti/tca9406";
    import esd "github.com/andenore/CopperLib/packages/parts/ti/tpd4e1u06";
    component U1: mux.TPS2121RUXR;
    component U2: chg.BQ24072RGTR;
    component U3: lvl.TCA9406DCUR;
    component U4: esd.TPD4E1U06DBVR;
    net GND { U1.GND; U1.CP2; U1.OV1; U1.OV2; U1.ST; U2.VSS; U2.EP; U2.CE;
              U2.EN1; U2.EN2; U2.TD; U3.GND; U4.GND; }
    net VBUS { U2.IN; U1.IN1; U3.VCCB; }
    net V3V3 { U1.PR1; U3.VCCA; U3.OE; }
    net SYS { U2.OUT_10; U2.OUT_11; U1.IN2; }
    net VOUT { U1.OUT_1; U1.OUT_8; }
    net VBAT { U2.BAT_2; U2.BAT_3; }
    net SDA_5V { U3.SDA_B; U4.D1_P; }
    net SCL_5V { U3.SCL_B; U4.D1_N; }
    supply GND { voltage = 0V; external = true; }
    supply VBUS { voltage = 5V; external = true; }
    supply V3V3 { voltage = 3.3V; external = true; }
}'''


def compile_board(tmp_path, change=lambda text: text):
    (tmp_path / "copper.mod").write_text(
        "module ti-parts-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n", encoding="utf-8")
    return compile_source(change(BOARD), str(tmp_path / "board.copper"), offline=True)


def footprint_file(footprint_id: str) -> Path:
    library, _, name = footprint_id.partition(":")
    return KICAD_FOOTPRINTS / f"{library}.pretty" / f"{name}.kicad_mod"


def test_minimal_board_with_all_four_parts_checks_clean(tmp_path):
    board = compile_board(tmp_path)
    assert check(board) == []
    for key, pins in PARTS.items():
        part = board.library[key]
        assert {name: pin.number for name, pin in part.pins.items()} == pins
        assert part.manufacturer == "Texas Instruments"
        assert part.source.checksum == "sha256:" + CHECKSUMS[key]
        assert part.source.url.startswith("https://www.ti.com/lit/ds/symlink/")
        assert not part.internal_pad_groups


@pytest.mark.parametrize("key", sorted(PARTS))
def test_pin_numbers_equal_footprint_pad_numbers(tmp_path, key):
    part = compile_board(tmp_path).library[key]
    (footprint_id,) = part.footprints
    path = footprint_file(footprint_id)
    if not path.is_file():
        pytest.skip(f"KiCad footprint library not installed: {path}")
    pads = {pad.number for pad in load_kicad_mod(path).footprint.pads if pad.number}
    assert {pin.number for pin in part.pins.values()} == pads


def test_tps2121_rux_land_pattern_matches_ti_example(tmp_path):
    part = compile_board(tmp_path).library["mux.TPS2121RUXR"]
    path = footprint_file(part.footprints[0])
    if not path.is_file():
        pytest.skip("KiCad footprint library not installed")
    pads = {pad.number: pad for pad in load_kicad_mod(path).footprint.pads}
    # SLVSEA3F p. 39 (RUX0012A land pattern example), KiCad y axis points down.
    expected = {"1": (-675_000, -350_000, 1_050_000, 400_000),
                "2": (-675_000, 350_000, 1_050_000, 400_000),
                "7": (675_000, 350_000, 1_050_000, 400_000),
                "8": (675_000, -350_000, 1_050_000, 400_000),
                "3": (-750_000, 1_150_000, 200_000, 600_000),
                "6": (750_000, 1_150_000, 200_000, 600_000),
                "9": (750_000, -1_150_000, 200_000, 600_000),
                "12": (-750_000, -1_150_000, 200_000, 600_000)}
    for number, (x, y, width, height) in expected.items():
        pad = pads[number]
        assert (pad.position.x_nm, pad.position.y_nm) == (x, y)
        assert (pad.size.width_nm, pad.size.height_nm) == (width, height)


def test_bq24072_exposed_pad_matches_rgt0016c(tmp_path):
    part = compile_board(tmp_path).library["chg.BQ24072RGTR"]
    path = footprint_file(part.footprints[0])
    if not path.is_file():
        pytest.skip("KiCad footprint library not installed")
    pad = {pad.number: pad for pad in load_kicad_mod(path).footprint.pads}["17"]
    assert (pad.size.width_nm, pad.size.height_nm) == (1_680_000, 1_680_000)


def test_datasheet_drive_and_connection_rules(tmp_path):
    library = compile_board(tmp_path).library
    mux, chg = library["mux.TPS2121RUXR"], library["chg.BQ24072RGTR"]
    assert DriveMode.OPEN_DRAIN in mux.pins["ST"].profile.drive_modes
    for name in ("CHG", "PGOOD"):
        assert DriveMode.OPEN_DRAIN in chg.pins[name].profile.drive_modes
    for name in ("CE", "EN1", "EN2", "TD", "VSS"):
        assert chg.pins[name].connection_policy is ConnectionPolicy.REQUIRED
    assert chg.pins["TMR"].connection_policy is ConnectionPolicy.OPTIONAL
    assert library["esd.TPD4E1U06DBVR"].pins["NC"].connection_policy is ConnectionPolicy.OPTIONAL
    # One driver per multi-land output rail.
    assert mux.pins["OUT_8"].profile.directions == {Direction.PASSIVE}
    assert chg.pins["OUT_11"].profile.directions == {Direction.PASSIVE}


@pytest.mark.parametrize("edit,code", [
    (lambda t: t.replace(" U2.TD;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace(" U1.CP2;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("voltage = 5V", "voltage = 6.5V"), "SUPPLY_VOLTAGE_HIGH"),
    (lambda t: t.replace("voltage = 3.3V", "voltage = 3.7V"), "SUPPLY_VOLTAGE_HIGH"),
])
def test_source_limits_are_enforced(tmp_path, edit, code):
    assert code in {d.code for d in check(compile_board(tmp_path, edit))}
