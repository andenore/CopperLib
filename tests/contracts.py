"""Read package engineering contracts as data; no compiler loader is involved."""
import json
from pathlib import Path

SCHEMA = "copperscript-engineering-contract/v0.1"
# Requirements every contract of a kind must name; each needs reviewed external evidence.
REQUIRED = {
    "rf": {"matching-review", "impedance", "prototype-rf"},
    "power": {"component-ratings", "current-capacity", "layout-review", "transient", "prototype-power"},
    "interface": {"operating-mode", "layout-review", "impedance", "signal-integrity", "prototype-interface"},
}


def load_contract(path: Path) -> dict:
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    assert contract["schema"] == SCHEMA and contract["kind"] in REQUIRED, path
    ids = [item["id"] for item in contract["requirements"]]
    assert len(ids) == len(set(ids)) and REQUIRED[contract["kind"]] <= set(ids), path
    for item in contract["requirements"]:
        assert item["stage"] in {"design", "simulation", "bench"} and item["description"].strip(), item
        if item["id"] in REQUIRED[contract["kind"]]:
            assert item["algorithm"] == "external", item
    return contract
