"""Source-backed TI power-mux, charger, I2C-translator and ESD parts: pin/pad coverage and a compiling fixture."""
import os
from pathlib import Path

import pytest
from copper_cli import audit_footprints, check, compile_board, part, pins

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


def test_minimal_board_with_all_four_parts_checks_clean():
    assert check(BOARD) == []
    board = compile_board(BOARD)
    for key, expected in PARTS.items():
        definition = part(board, key)
        assert pins(board, key) == expected
        assert definition["manufacturer"] == "Texas Instruments"
        assert definition["source"]["checksum"] == "sha256:" + CHECKSUMS[key]
        assert definition["source"]["url"].startswith("https://www.ti.com/lit/ds/symlink/")
        assert not definition["internal_pad_groups"]


def test_pin_numbers_equal_footprint_pad_numbers():
    if not KICAD_FOOTPRINTS.is_dir():
        pytest.skip(f"KiCad footprint library not installed: {KICAD_FOOTPRINTS}")
    audit = audit_footprints(BOARD, KICAD_FOOTPRINTS)
    assert audit["passed"], [entry["errors"] for entry in audit["entries"]]
    assert audit["total"] == len(PARTS)


def test_datasheet_drive_and_connection_rules():
    board = compile_board(BOARD)
    mux, chg = part(board, "mux.TPS2121RUXR")["pins"], part(board, "chg.BQ24072RGTR")["pins"]
    assert "open_drain" in mux["ST"]["profile"]["drive_modes"]
    for name in ("CHG", "PGOOD"):
        assert "open_drain" in chg[name]["profile"]["drive_modes"]
    for name in ("CE", "EN1", "EN2", "TD", "VSS"):
        assert chg[name]["connection_policy"] == "required"
    assert chg["TMR"]["connection_policy"] == "optional"
    assert part(board, "esd.TPD4E1U06DBVR")["pins"]["NC"]["connection_policy"] == "optional"
    # One driver per multi-land output rail.
    assert mux["OUT_8"]["profile"]["directions"] == ["passive"]
    assert chg["OUT_11"]["profile"]["directions"] == ["passive"]


@pytest.mark.parametrize("edit,code", [
    (lambda t: t.replace(" U2.TD;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace(" U1.CP2;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (lambda t: t.replace("voltage = 5V", "voltage = 6.5V"), "SUPPLY_VOLTAGE_HIGH"),
    (lambda t: t.replace("voltage = 3.3V", "voltage = 3.7V"), "SUPPLY_VOLTAGE_HIGH"),
])
def test_source_limits_are_enforced(edit, code):
    assert code in {d["code"] for d in check(edit(BOARD))}
