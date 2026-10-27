"""Regulator topology and immutable geometry of the generated hard-macro assets."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/circuits/ti/tps62130a-buck"


def load(name):
    spec = importlib.util.spec_from_file_location(name, PACKAGE/f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def path(enabled):
    return PACKAGE/"assets"/f"tps62130a-six-layer-{'enabled' if enabled else 'always-on'}.json"


@pytest.mark.parametrize("enabled", [False, True])
def test_assets_reproduce_and_bind_every_required_pad(enabled):
    asset = load("generate_layout").generate(enabled)
    assert (json.dumps(asset,sort_keys=True,indent=2)+"\n").encode() == path(enabled).read_bytes()
    assert asset["production_publishable"] is False and asset["unresolved"]
    assert asset["schema"] == "copperlib-physical-hard-macro/v0.3"
    assert {p["net"] for p in asset["polygons"]} == {"VIN", "SW", "VOUT"}
    assert all(p["layer"] == "F.Cu" for p in asset["polygons"])
    assert {zone["net"] for zone in asset["zones"]} == {"GND"}
    assert {zone["id"] for zone in asset["zones"]} == {"lower-return", "exposed-pad"}
    assert not any(track["net"] == "GND" and track["layer"] == "B.Cu" for track in asset["tracks"])
    assert asset["plane_returns"][0]["net"] == "GND"
    assert {tuple(p) for p in asset["plane_returns"][0]["pads"]} == {
        (r,p) for r,p,n in asset["pad_nets"] if n == "GND"}
    assert len({tuple(c["via_position_nm"]) for c in asset["plane_returns"][0]["dedicated_contacts"]}) == 6
    assert len(asset["members"]) == 9
    assert asset["isolated_pads"] == [["U","4"]]
    assert {p for r,p,n in asset["pad_nets"] if r == "U"} == {str(p) for p in range(1,18) if p != 4}
    assert {n for r,p,n in asset["pad_nets"] if r == "U" and p == "13"} == {"EN" if enabled else "VIN"}
    assert not any(v["net"] == "SW" for v in asset["vias"])
    assert all(t["layer"] == "F.Cu" for t in asset["tracks"] if t["net"] == "SW")
    assert all(t["width_nm"] >= 250000 for t in asset["tracks"] if t["net"] in {"VIN", "VOUT"})
    assert sum(v.get("finish") == "filled-capped" for v in asset["vias"]) == 4
    for port in asset["ports"]:
        assert {tuple(p) for p in port["pads"]} == {(r,p) for r,p,n in asset["pad_nets"] if n == port["net"]}
    assert len(asset["protected_regions"]) == 1
    assert asset["protected_regions"][0]["layers"] == ["F.Cu", "In2.Cu", "B.Cu"]
    assert len(asset["keepouts"]) == 1
    assert asset["keepouts"][0]["layers"] == ["In2.Cu", "In3.Cu", "B.Cu"]
    assert not asset["keepouts"][0]["block_tracks"]
    assert not asset["keepouts"][0]["block_vias"]
    assert asset["keepouts"][0]["block_zones"]


def test_cached_official_evidence_identity():
    asset = load("generate_layout").generate()
    for name, key in [("tps62130a.pdf","datasheet_sha256"),("slvu437b.pdf","evm_sha256")]:
        source = ROOT/"cache/ti/tps62130a-layout"/name
        if source.is_file(): assert sha256(source.read_bytes()).hexdigest() == asset["source"][key]
