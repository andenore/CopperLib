"""Voltage-TS variant and external hardware facts, not battery qualification."""
import json
from pathlib import Path

from pcbir import compile_source
from pcbir.elaborate import elaborate
from pcbir.engineering_qualification import load_contract

ROOT = Path(__file__).parents[1]


def test_t_variant_mapping_and_bias_connections(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module ts-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    board = compile_source('''board Test {
        import charger "github.com/andenore/CopperLib/packages/parts/ti/bq24072t";
        import bias "github.com/andenore/CopperLib/packages/circuits/ti/bq24072t-ts-43k-39k";
        component U: charger.BQ24072TRGTR;
        module TEMP: bias.BQ24072T_TS_43K_39K;
        net VIN { U.IN; TEMP.VIN; }
        net TS { U.TS; TEMP.TS; }
        net NTC { TEMP.NTC; }
        net GND { U.VSS; U.EP; TEMP.GND; }
    }''', str(tmp_path / "board.copper"), offline=True)
    flat = elaborate(board)
    part = board.library["charger.BQ24072TRGTR"]
    assert part.pins["TS"].number == "1"
    assert part.pins["TMR"].number == "14"
    assert part.pins["EP"].number == "17"
    assert len(part.pins) == 17
    nets = {n.name: {(e.component, e.pin) for e in n.endpoints} for n in flat.nets}
    assert nets["TS"] == {("U", "TS"), ("TEMP/R_ISOLATION", "P2")}
    assert nets["NTC"] == {("TEMP/R_TOP", "P2"), ("TEMP/R_SHUNT", "P1"), ("TEMP/R_ISOLATION", "P1")}
    assert ("TEMP/R_SHUNT", "P2") in nets["GND"]


def test_limits_do_not_inherit_non_t_voltage_or_invent_leakage():
    limits = json.loads((ROOT / "packages/parts/ti/bq24072t/charging-limits.json").read_text())
    assert limits["battery_regulation_max_mv"] == 4240
    assert limits["ts_type"] == "ratiometric_voltage_divider"
    assert limits["ts_maximum_input_leakage_na"] is None
    assert not limits["provides_cell_protection"]
    assert not limits["production_publishable"]
    assert load_contract(ROOT / "packages/parts/ti/bq24072t/qualification.json")["kind"] == "power"


def test_external_sensor_and_holder_keep_unknowns_explicit():
    sensor = json.loads((ROOT / "packages/sensors/semitec/103at-2/specification.json").read_text())
    holder = json.loads((ROOT / "packages/battery-holders/mpd/bh-18650-w/specification.json").read_text())
    assert sensor["nominal_resistance_by_temperature_c"]["40"] == 5827
    assert sensor["guaranteed_rt_envelope_percent"] is None
    assert sensor["cell_to_sensor_error_max_c"] is None
    assert holder["designed_for_protected_18650"]
    assert holder["lead_awg"] == 24
    assert holder["maximum_accepted_cell_length_um"] is None
    assert holder["current_rating_ma"] is None
    assert holder["contact_resistance_mohms"] is None
