"""Exact protection lands, physical DNP and reference topology are not RF signoff."""
from pathlib import Path
import json
from pcbir import compile_source, load_kicad_mod, Point
from pcbir.assembly import snapshot
from pcbir.elaborate import elaborate
from pcbir.engineering_qualification import load_contract, REQUIRED

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


def test_exact_protection_lands():
    ti = load_kicad_mod(ROOT / 'packages/parts/ti/tpd1e01b04/footprints/TPD1E01B04_DPY.kicad_mod').footprint
    sem = load_kicad_mod(ROOT / 'packages/parts/semtech/rclamp1561pq/footprints/RClamp1561PQ_SLP1006P2.kicad_mod').footprint
    for footprint, half_pitch, width, height in ((ti, '0.35', 300000, 500000), (sem, '0.425', 550000, 600000)):
        pads = {p.number: p for p in footprint.pads if p.number}
        assert set(pads) == {'1', '2'}
        assert pads['1'].position == Point.mm('-' + half_pitch, 0)
        assert pads['2'].position == Point.mm(half_pitch, 0)
        assert all((p.size.width_nm, p.size.height_nm) == (width, height) for p in pads.values())


def test_lte_topology_retains_series_isolation_and_dnp(tmp_path):
    (tmp_path / 'copper.mod').write_text('module rf-test\nrequire github.com/andenore/CopperLib v0.1.0\n'
        f'replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n')
    design = compile_source('''board Test {
        import support "github.com/andenore/CopperLib/packages/circuits/simcom/lte-antenna-support";
        module RF: support.LTE_ANTENNA_SUPPORT;
        net HOST { RF.HOST; }
        net ANT { RF.ANTENNA; }
        net GND { RF.GND; }
    }''', str(tmp_path / 'board.copper'), offline=True)
    flat = elaborate(design)
    components = {c.ref: c for c in flat.components}
    assert len(components) == 5
    assert components['RF/C_DC'].value.in_unit('pF') == 100
    assert components['RF/R_LINK'].value.in_unit('ohm') == 0
    assert {s.reference for s in snapshot(design).selections} == {'RF/R_LINK', 'RF/C_DC', 'RF/D_ESD'}
    nets = [{(e.component, e.pin) for e in n.endpoints} for n in flat.nets]
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
