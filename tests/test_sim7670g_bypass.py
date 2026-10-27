"""Reusable pin-associated bank preserves modem contacts and evidence limits."""
from pathlib import Path
import re
from contracts import load_contract
from copper_cli import compile_board, flat_components, flat_nets, part

ROOT = Path(__file__).parents[1]


def test_bypass_bank_forwarding_and_intent():
    pins = re.findall(r'pin (\w+) \{(.*?)\}',
        (ROOT / 'packages/parts/simcom/sim7670g-lngv/part.copper').read_text())
    forwarded = [name for name, attributes in pins if 'do_not_connect' not in attributes]
    others = '\n'.join(f'net N_{name} {{ M.{name}; }}' for name in forwarded
        if name not in ('VBAT_1', 'VBAT_2', 'VBAT_3', 'GND'))
    source = '''board Test {
        import bank "github.com/andenore/CopperLib/packages/circuits/simcom/sim7670g-vbat-bypass";
        module M: bank.SIM7670G_VBAT_BYPASS;
        net VBAT { M.VBAT_1; M.VBAT_2; M.VBAT_3; }
        net GND { M.GND; }
    ''' + others + '}'
    components = flat_components(source)
    assert len(components) == 5
    expected = {'C_10P': ('10 pF', 'VBAT_1'), 'C_33N': ('33 nF', 'VBAT_1'),
                'C_100N': ('100 nF', 'VBAT_2'), 'C_1U': ('1 uF', 'VBAT_3')}
    for ref, (value, pin) in expected.items():
        capacitor = components['M/' + ref]
        assert capacitor['value'] == value
        assert capacitor['properties'] == {'role': 'decoupling', 'decouples': 'M/U.' + pin}
    endpoints = flat_nets(source)['VBAT']
    assert {('M/U', 'VBAT_1'), ('M/U', 'VBAT_2'), ('M/U', 'VBAT_3')} <= endpoints
    assert all(('M/' + ref, 'P1') in endpoints for ref in expected)
    modem = part(compile_board(source), components['M/U']['part'])
    assert len(modem['pins']) == 124
    assert not modem['internal_pad_groups']


def test_reference_boundaries_are_not_approval():
    readme = (ROOT / 'packages/circuits/simcom/sim7670g-vbat-bypass/README.md').read_text()
    assert 'production_publishable = false' in readme
    assert 'effective' in readme
    assert 'not manufacturer maximums' in readme
    contract = load_contract(ROOT / 'packages/circuits/simcom/sim7670g-vbat-bypass/qualification.json')
    assert contract['kind'] == 'power'
    assert not contract['production_publishable']
    assert {r['stage'] for r in contract['requirements']} == {'design', 'simulation', 'bench'}
