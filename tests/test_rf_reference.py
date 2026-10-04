from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rf_extract", ROOT / "packages/circuits/nordic/nrf52832-johanson-reference/extract_reference.py")
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)


def test_checked_reference_is_bounded_and_unqualified():
    document = json.loads(extractor.DESTINATION.read_text())
    members = {item["reference"]: item for item in document["members"]}
    assert set(members) == {"U1", "C3", "L1"}
    assert members["U1"]["center_nm"] == [0, 0]
    assert members["C3"]["center_nm"] == [4191000, 0]
    assert members["L1"]["center_nm"] == [5613400, 508000]
    assert members["C3"]["rotation_degrees"] == "270.00"
    assert ["C3", "1", "ground"] in document["pad_nets"]
    assert ["C3", "2", "raw"] in document["pad_nets"]
    assert document["production_publishable"] is False
    assert document["unresolved"]


def test_cached_vendor_extraction_is_reproducible():
    archive = ROOT / "cache/rf-reference/nrf52832qfaxreflayoutv11.zip"
    if not archive.is_file():
        pytest.skip("optional source reproducibility check requires local Nordic archive")
    rendered = json.dumps(extractor.extract(archive), indent=2, sort_keys=True) + "\n"
    assert rendered.encode("utf-8") == extractor.DESTINATION.read_bytes()


def test_generation_uses_portable_lf_bytes(tmp_path, monkeypatch):
    output = tmp_path / "reference.json"
    monkeypatch.setattr("sys.argv", ["extract", "unused.zip", "--output", str(output)])
    monkeypatch.setattr(extractor, "extract", lambda archive: {"fixture": True})
    extractor.main()
    assert output.read_bytes() == b'{\n  "fixture": true\n}\n'
    assert b"\r" not in extractor.DESTINATION.read_bytes()


def test_changed_source_identity_is_rejected(tmp_path):
    archive = tmp_path / "changed.zip"
    archive.write_bytes(b"not the pinned Nordic archive")
    with pytest.raises(ValueError, match="archive identity"):
        extractor.extract(archive)


def test_missing_rows_fail_even_when_test_source_is_pinned(tmp_path, monkeypatch):
    archive = tmp_path / "fixture.zip"
    rows = b"U1 QFN 0mil 0mil 0mil 0mil 0mil 0mil T 360.00 MCU\n"
    with ZipFile(archive, "w") as output:
        output.writestr(extractor.ENTRY, rows)
    monkeypatch.setattr(extractor, "ARCHIVE_SHA256", sha256(archive.read_bytes()).hexdigest())
    monkeypatch.setattr(extractor, "ENTRY_SHA256", sha256(rows).hexdigest())
    with pytest.raises(ValueError, match="missing or duplicated"):
        extractor.extract(archive)
