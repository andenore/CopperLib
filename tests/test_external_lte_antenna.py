import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT / 'packages/antennas/taoglas/fxub16-07-0150aq'


def test_external_antenna_records_exact_eu_band_intervals_not_marketing_range():
    data = json.loads((PACKAGE/'specification.json').read_text())
    assert data['assembly_type'] == 'external_passive_cabled_flex_antenna'
    assert data['mpn'] == 'FXUB16.07.0150AQ'
    assert data['nominal_impedance_ohms'] == 50
    assert data['cable_length_um'] == 150000
    assert not data['requires_bias_power']
    bands = {b['band']: b for b in data['eu_lte_band_intervals_mhz']}
    assert bands[20]['downlink'] == [791, 821]
    assert bands[28]['uplink'] == [703, 748]
    assert {1, 3, 7, 8, 20, 28, 38, 40, 41} <= set(bands) <= set(data['lte_bands_from_page5'])
    assert data['minimum_metal_clearance_um'] is None
    assert data['integrated_rf_esd_protection'] is None
    assert data['additional_matching_required'] is None
    assert not data['production_publishable']
    assert not list(PACKAGE.glob('*.copper'))
    assert len(data['sources'][0]['sha256']) == 64


def test_antenna_contract_does_not_approve_host_matching_or_simulation():
    contract = json.loads((PACKAGE/'qualification.json').read_text())
    assert contract['matching'] == 'unresolved'
    assert not contract['production_publishable']
    assert {r['id']: r['stage'] for r in contract['requirements']} == {
        'matching-review': 'design', 'reference-layout': 'design',
        'impedance': 'simulation', 'prototype-rf': 'bench'}


def test_selected_stackup_keeps_calculator_and_construction_models_separate():
    package = ROOT/'packages/profiles/jlcpcb/jlc06161h-3313'
    model = json.loads((package/'calculator-model.json').read_text())
    stackup = json.loads((package/'stackup.json').read_text())
    assert model['selected_profile'] == stackup['selected_profile']
    assert model['material'] == 'Nan Ya Plastics NP-155F'
    assert model['outer_copper_model_thickness_nm'] == 40640
    assert stackup['physical_layers'][0]['thickness_nm'] == 35000
    assert stackup['physical_layers'][1]['thickness_nm'] == 99400
    assert model['loss_tangent'] is None
    assert not model['production_publishable']
