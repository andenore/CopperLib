"""Pinned bounded RF asset, without claiming RF/manufacturing qualification."""
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "packages/circuits/nordic/nrf52832-johanson-reference/assets/nrf52832-johanson-six-layer-trial.json"


def test_rf_macro_is_explicitly_bounded_and_unqualified():
    data = json.loads(ASSET.read_bytes())
    assert data["schema"] == "copperlib-physical-hard-macro/v0.1"
    assert data["production_publishable"] is False and data["unresolved"]
    assert {m["reference"] for m in data["members"]} == {"U1","C3","L1","CA","LA","LB","ANT"}
    assert data["isolated_pads"] == [["ANT","2"]]
    assert ["C3","1","ground"] in data["pad_nets"]
    assert ["U1","31","ground"] in data["pad_nets"]
    assert all(v["position_nm"] not in ([0,0],[4191000,0]) for v in data["vias"])
    assert any(k["id"] == "antenna-corner" and k["block_zones"] for k in data["keepouts"])
    assert any(k["id"] == "nordic-inner-clear" and "In1.Cu" in k["layers"] for k in data["keepouts"])
    assert b"\r" not in ASSET.read_bytes()


def test_generator_reproduces_exact_asset_bytes(monkeypatch):
    archive = ROOT / "cache/rf-reference/nrf52832qfaxreflayoutv11.zip"
    if not archive.is_file(): pytest.skip("optional cached Nordic source")
    monkeypatch.syspath_prepend(str(ROOT / "packages/circuits/nordic/nrf52832-johanson-reference"))
    extractor = importlib.import_module("generate_trial")
    expected = (json.dumps(extractor.generate(archive),indent=2,sort_keys=True)+"\n").encode()
    assert expected == ASSET.read_bytes()


def test_dec3_access_envelope_does_not_relax_rf_fabrication_keepouts():
    data = json.loads(ASSET.read_bytes())
    private = next(r for r in data["protected_regions"] if r["id"] == "nordic-private")
    assert private["vertices"] == [[3300000,-600000],[6200000,-600000],
                                  [6200000,1200000],[3300000,1200000]]
    for name in ("nordic-no-pour", "nordic-inner-clear"):
        keepout = next(k for k in data["keepouts"] if k["id"] == name)
        assert keepout["vertices"] == [[3300000,-1000000],[6200000,-1000000],
                                      [6200000,1200000],[3300000,1200000]]
        assert keepout["block_vias"] and keepout["block_zones"]


def test_generator_rejects_changed_archive_before_reading_geometry(tmp_path,monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "packages/circuits/nordic/nrf52832-johanson-reference"))
    extractor = importlib.import_module("generate_trial")
    source = tmp_path / "changed.zip"
    source.write_bytes(b"not the pinned archive")
    with pytest.raises(ValueError,match="archive identity changed"):
        extractor.generate(source)
