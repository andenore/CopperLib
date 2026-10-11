"""External pack facts must not be mistaken for a reviewed PCB/pack design."""
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_external_cell_keeps_pack_and_retail_facts_separate():
    data = json.loads((ROOT / "packages/batteries/kjell/32058/specification.json").read_text())
    assert data["assembly_type"] == "external_removable_cell"
    assert data["retail_protection_present"] is True
    assert data["integrated_ntc"] is None
    assert data["connector"] is None
    assert data["datasheet_pack"]["maximum_continuous_discharge_current_ma"] == 3000
    assert data["datasheet_pack"]["maximum_pack_length_um"] == 71500
    assert data["datasheet_pack"]["protection_trip_current_ma"] is None
    assert not data["source_applicability_reviewed"]
    assert not data["production_publishable"]
    assert all(len(source["sha256"]) == 64 for source in data["sources"])


def test_charger_does_not_guarantee_pack_temperature_or_protection():
    data = json.loads((ROOT / "packages/parts/ti/bq24072/charging-limits.json").read_text())
    assert data["battery_regulation_max_mv"] == 4230
    assert data["floating_tmr_fast_charge_min_s"] == 14400
    assert not data["nominal_ntc_window_is_guaranteed"]
    assert not data["provides_cell_protection"]
    assert not data["production_publishable"]
