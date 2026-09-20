import shutil

from copperscript_stm32g0 import core
from pcbir.devicegen import check_generated, load_bundle, render_bundle, validate_bundle


def test_exact_upstream_validation_and_cross_references():
    bundle = load_bundle(core.BUNDLE)
    assert validate_bundle(bundle) == ()
    assert [row["name"] for row in bundle.pads] == ["PA0", "PA1", "PC0", "PC1"]
    assert [row["bond"] for row in bundle.parts[0].pins] == ["PA0", "PA1", "PC0", "PC1"]


def test_deterministic_upstream_copper_output():
    expected = render_bundle(load_bundle(core.BUNDLE))
    assert expected == {path.name: path.read_text(encoding="utf-8") for path in core.OUTPUT.glob("*.copper")}


def test_incomplete_scope_blocks_publication():
    report = core.coverage()
    assert report["complete_coverage"] is False
    assert report["production_publishable"] is False


def test_unresolved_blocks_upstream_validation(tmp_path):
    bundle_dir = tmp_path / "bundle"
    shutil.copytree(core.BUNDLE, bundle_dir)
    pads = bundle_dir / "pads.csv"
    pads.write_text(pads.read_text(encoding="utf-8").replace("PA0,digital_input", "PA0,?"), encoding="utf-8")
    assert validate_bundle(load_bundle(bundle_dir))


def test_upstream_check_matches_committed_outputs():
    assert check_generated(load_bundle(core.BUNDLE), core.OUTPUT) == ()


def test_coverage_is_conspicuous():
    assert core.coverage() == {
        "orderable_part": "STM32G0B1CBT6",
        "package": "LQFP48",
        "verified_package_pins": 4,
        "covered_pads": 4,
        "peripheral_signals": 0,
        "mux_options": 0,
        "scope": "proof-of-concept",
        "complete_coverage": False,
        "production_publishable": False,
        "unresolved_facts": 0,
        "illustrative_facts": 0,
    }
