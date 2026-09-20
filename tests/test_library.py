import hashlib, json
from pathlib import Path
from copperscript_stm32g0 import core

def test_evidence_valid(): assert core.validate() == []
def test_generation_is_deterministic(tmp_path):
    core.generate(); before=hashlib.sha256((core.OUT/"pins.csv").read_bytes()).hexdigest(); core.generate(); after=hashlib.sha256((core.OUT/"pins.csv").read_bytes()).hexdigest(); assert before == after
def test_cross_reference_subjects():
    names={f["subject"] for f in core.facts()}; assert {"PA0","PA1","PC0","PC1"} <= names
def test_coverage_report():
    c=core.coverage(); assert c["verified_pins"] == 4; assert c["scope"] == "proof-of-concept"
def test_unresolved_blocks_publish(monkeypatch):
    original=core.facts
    monkeypatch.setattr(core, "facts", lambda: original()+[{"fact_id":"x","subject":"X","field":"package_pin","value":"?","status":"unresolved","source_id":"s","locator":"t"}])
    assert core.production_blocked()
