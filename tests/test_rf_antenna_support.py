"""Physical DNP and reference topology are not RF signoff."""
from pathlib import Path
import json
from contracts import REQUIRED, load_contract
from copper_cli import assembly_snapshot, flat_components, flat_nets

ROOT = Path(__file__).parents[1]


def test_gnss_open_selector_model_preserves_current_operating_limits():
    package = ROOT / 'packages/parts/u-blox/max-m10s'
    source = (package / 'part.copper').read_text()
    vio = next(line for line in source.splitlines() if 'pin V_IO {' in line)
    selector = next(line for line in source.splitlines() if 'pin VIO_SEL {' in line)
    assert 'voltage_min = 2700mV;' in vio
    assert 'connection = do_not_connect;' in selector
    assert 'UBX-20035208 R08' in source
    review = json.loads((package / 'datasheet-review.json').read_text())
    contract = load_contract(package / 'qualification.json')
    assert review['source']['sha256'] == contract['sources'][0]['sha256']
    assert review['open_vio_sel_operating_limits']['vio_maximum_is_vcc']
    assert review['absolute_limits']['vio_rise_min_us_per_v'] == 25
    assert not review['production_publishable']


def test_lte_topology_retains_series_isolation_and_dnp():
    source = '''board Test {
        import support "github.com/andenore/CopperLib/packages/circuits/simcom/lte-antenna-support";
        module RF: support.LTE_ANTENNA_SUPPORT;
        net HOST { RF.HOST; }
        net ANT { RF.ANTENNA; }
        net GND { RF.GND; }
    }'''
    components = flat_components(source)
    assert len(components) == 5
    assert components['RF/C_DC']['value'] == '100 pF'
    assert components['RF/R_LINK']['value'] == '0 ohm'
    assert {s['reference'] for s in assembly_snapshot(source)['selections']} == {'RF/R_LINK', 'RF/C_DC', 'RF/D_ESD'}
    nets = list(flat_nets(source).values())
    assert {('RF/R_LINK', 'P2'), ('RF/C_DC', 'P1')} in nets
    assert {('RF/C_DC', 'P2'), ('RF/C_ANT', 'RF'), ('RF/D_ESD', 'IO')} in nets
    assert not any({('RF/R_LINK', 'P1'), ('RF/C_DC', 'P2')} <= n for n in nets)


def test_rf_support_keeps_required_external_review_gates():
    for path in ('parts/ti/tpd1e01b04', 'parts/semtech/rclamp1561pq', 'circuits/simcom/lte-antenna-support'):
        contract = load_contract(ROOT / 'packages' / path / 'qualification.json')
        assert not contract['production_publishable']
        assert REQUIRED['rf'] <= {r['id'] for r in contract['requirements']}
        assert all(r['algorithm'] == 'external' for r in contract['requirements'])
        assert all(len(s['sha256']) == 64 for s in contract['sources'])


def test_coexistence_sources_preserve_gain_and_filter_coverage_limits():
    receiver = json.loads((ROOT / 'packages/parts/u-blox/max-m10s/coexistence-limits.json').read_text())
    transmitter = json.loads((ROOT / 'packages/circuits/simcom/lte-antenna-support/reference-limits.json').read_text())
    saw = json.loads((ROOT / 'packages/parts/u-blox/max-m10s/filter-candidates/b4327-review.json').read_text())
    assert 'Low-gain' in receiver['conditions']
    assert transmitter['maximum_power_mdbm'] == transmitter['nominal_power_mdbm'] + transmitter['positive_tolerance_mdb'] == 25700
    assert len(receiver['samples']) == 9
    assert saw['status'] == 'not_implemented_not_qualified'
    assert not receiver['allow_interpolation'] and not saw['allow_interpolation']
    assert not any(r['lower_mhz'] <= 2350 <= r['upper_mhz'] for r in saw['rejection_minimum_ranges'])
    assert any('TVS alone' in r for r in saw['unresolved'])
    assert receiver['typical_not_guaranteed']


def test_passive_coexistence_options_never_approve_missing_filter_or_gain_evidence():
    data = json.loads((ROOT / 'packages/parts/u-blox/max-m10s/passive-coexistence-options.json').read_text())
    assert not data['production_publishable']
    assert data['receiver_configuration']['manufacturer_default_mode'] == 'low_gain'
    assert data['receiver_configuration']['configuration_key'] == 'CFG-HW-RF_LNA_MODE'
    baseline, filtered = data['options']
    assert not baseline['external_saw_populated']
    assert not baseline['approved_for_concurrent_lte']
    assert not filtered['implemented']
    assert 'not a solder-population option' in filtered['approval']
