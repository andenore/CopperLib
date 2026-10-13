"""Current Copper exports preserve every historical geometry/evidence contract."""
from decimal import Decimal
import json
from pathlib import Path
import pytest
from pcbir.parser import parse
from pcbir.packages import PackageResolver
from pcbir.macro_definitions import lower_macro
from pcbir.quantities import decimal_text

ROOT = Path(__file__).resolve().parents[1]
JOBS = [
    ('nordic/nrf52832-johanson-reference', 'trial-layout.copper', 'nrf52832-johanson-six-layer-trial.json'),
    ('nordic/nrf52832-johanson-reference', 'managed-layout.copper', 'nrf52832-johanson-six-layer-trial.json'),
    ('nordic/nrf52832-johanson-reference', 'corner-layout.copper', 'nrf52832-johanson-managed-corner.json'),
    ('ti/tps62130a-buck', 'managed-always-on.copper', 'tps62130a-six-layer-always-on.json'),
    ('ti/tps62130a-buck', 'managed-enabled.copper', 'tps62130a-six-layer-enabled.json'),
    *[('ti/tps63020-buck-boost', v + '-layout.copper', 'tps63020-six-layer-' + v + '.json')
      for v in ('always-on', 'enabled-series-feedback', 'enabled-power-output')],
]

@pytest.mark.parametrize('package,source,asset', JOBS)
def test_copper_export_preserves_fixed_geometry_and_source_facts(package, source, asset):
    root = ROOT / 'packages/circuits' / package
    path = root / source
    doc = parse(path.read_text(encoding='utf-8'), str(path))
    resolver = PackageResolver.for_source(path, doc.location, locked=True, offline=True)
    actual, inputs = lower_macro(doc, resolver, resolve_footprints=False)
    assert inputs == {}  # This structural test never fetches a provider.
    prior = json.loads((root / 'assets' / asset).read_bytes())
    prior['vias'] = [{'finish': 'standard', **v} for v in prior['vias']]
    for key in prior.keys() - {'schema', 'source', 'members'}:
        assert actual[key] == prior[key], key
    for before, after in zip(prior['members'], actual['members'], strict=True):
        before = {**before, 'rotation_degrees': decimal_text(Decimal(str(before['rotation_degrees'])))}
        assert {k:v for k,v in before.items() if k not in {'footprint', 'footprint_digest'}} == {
            k:v for k,v in after.items() if k not in {'footprint', 'footprint_digest'}}
        assert after['footprint'].startswith(('github.com/andenore/CopperLib/', 'github.com/KiCad/kicad-footprints/'))
    for key, value in prior['source'].items():
        assert actual['source'][key] == value
    assert actual['production_publishable'] is False
    assert actual['unresolved'] == prior['unresolved']
