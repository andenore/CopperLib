"""I-PEX CABLINE-CA receptacle 20525-040E-02: pin map, evidence and land coverage."""
import json
from pathlib import Path

from copper_cli import audit_footprints, check, compile_board, part

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/parts/i-pex/20525-040e-02"
EVIDENCE = PACKAGE / "evidence/footprint-audit.json"
IMPORT = "github.com/andenore/CopperLib/packages/parts/i-pex/20525-040e-02"


def test_footprint_evidence_keeps_cable_exit_and_harness_facts_unresolved():
    evidence = json.loads(EVIDENCE.read_text())
    assert evidence["production_publishable"] is False
    assert evidence["cable_exit_side"]["footprint_direction"] == "+Y"
    assert "41-n" in evidence["harness_pin_mapping"]["fact"]
    assert evidence["unresolved"]


def test_part_maps_every_land_and_compiles():
    nets = "\n".join(f"            net S{n} {{ J1.P{n}; J2.P{41 - n}; }}" for n in range(1, 41))
    source = f'''
        board CablineCaFixture {{
            import ipex "{IMPORT}";
            component J1: ipex.IPEX_20525_040E_02;
            component J2: ipex.IPEX_20525_040E_02;
{nets}
            net GND {{ J1.SHIELD; J2.SHIELD; }}
        }}
    '''
    connector = part(compile_board(source), "ipex.IPEX_20525_040E_02")
    pins = {name: pin["number"] for name, pin in connector["pins"].items()}
    assert pins == {**{f"P{n}": str(n) for n in range(1, 41)}, "SHIELD": "SH"}
    profiles = {name: (set(pin["profile"]["domains"]), set(pin["profile"]["directions"]))
                for name, pin in connector["pins"].items()}
    assert profiles.pop("SHIELD") == ({"ground"}, {"passive"})
    assert all(profile == ({"analog", "digital"}, {"passive"}) for profile in profiles.values())
    assert connector["internal_pad_groups"] == []
    evidence = json.loads(EVIDENCE.read_text())
    assert pins == evidence["semantic_pins"]
    assert connector["source"]["checksum"] == "sha256:" + evidence["sources"][0]["sha256"]
    assert connector["source"]["revision"] == "20525 rev 34"
    assert check(source) == []
    audit = audit_footprints(source)
    assert audit["passed"], [entry["errors"] for entry in audit["entries"]]
