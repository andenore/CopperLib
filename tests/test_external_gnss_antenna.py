import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT/'packages/antennas/taoglas/fxp611-07-0092c'


def test_passive_gnss_assembly_records_band_cable_and_real_clearance():
    facts = json.loads((PACKAGE/'specification.json').read_text())
    assert facts['mpn'] == 'FXP611.07.0092C'
    assert (facts['frequency_min_mhz'], facts['frequency_max_mhz']) == (1559, 1610)
    assert facts['nominal_impedance_ohms'] == 50
    assert facts['cable_length_um'] == 92000
    assert facts['required_mounting_space_um'] == [40000, 40000, 200]
    assert facts['minimum_metal_or_main_ground_plane_clearance_um'] == 10000
    assert facts['polarization'] == 'linear'
    assert not facts['requires_bias_power']
    assert not facts['production_publishable']
    assert not list(PACKAGE.glob('*.copper'))


def test_unresolved_host_obligations_are_not_inferred_from_nominal_impedance():
    facts = json.loads((PACKAGE/'specification.json').read_text())
    contract = json.loads((PACKAGE/'qualification.json').read_text())
    assert facts['additional_matching_required'] is None
    assert facts['integrated_rf_esd_protection'] is None
    assert facts['minimum_cable_bend_radius_um'] is None
    assert facts['drawing_body_dimensions_um'] != [facts['nominal_body_length_um'], facts['nominal_body_width_um']]
    assert contract['matching'] == 'unresolved'
    assert contract['sources'][0]['sha256'] == facts['sources'][0]['sha256']
    assert {r['id']: r['stage'] for r in contract['requirements']} == {
        'matching-review': 'design', 'reference-layout': 'design',
        'impedance': 'simulation', 'prototype-rf': 'bench'}


def test_cached_vendor_source_hash_when_available():
    import hashlib
    source = ROOT/'cache/taoglas-fxp611-review/FXP611.07.0092C.pdf'
    if source.exists():
        facts = json.loads((PACKAGE/'specification.json').read_text())
        assert hashlib.sha256(source.read_bytes()).hexdigest() == facts['sources'][0]['sha256']
