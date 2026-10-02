"""Pinned bounded RF asset, without claiming RF/manufacturing qualification."""
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "data/full-vertical/nrf-antenna-hard-macro.json"


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
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    extractor = importlib.import_module("extract_nrf_antenna_hard_macro")
    expected = (json.dumps(extractor.generate(archive),indent=2,sort_keys=True)+"\n").encode()
    assert expected == ASSET.read_bytes()


def test_generator_rejects_changed_archive_before_reading_geometry(tmp_path,monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    extractor = importlib.import_module("extract_nrf_antenna_hard_macro")
    source = tmp_path / "changed.zip"
    source.write_bytes(b"not the pinned archive")
    with pytest.raises(ValueError,match="archive identity changed"):
        extractor.generate(source)
