"""Independent manufacturer terminal/land checks for the short protection path."""
from pathlib import Path
import importlib.util
import re
from copper_cli import compile_board, pins, part, audit_footprints
from contracts import REQUIRED, load_contract

ROOT=Path(__file__).resolve().parents[1]
FIXTURE='''board ProtectionParts {
 import e "github.com/andenore/CopperLib/packages/parts/ti/tps25947";
 import q "github.com/andenore/CopperLib/packages/parts/ti/csd18540q5b";
 import f "github.com/andenore/CopperLib/packages/parts/littelfuse/0451";
 import b "github.com/andenore/CopperLib/packages/parts/vishay/wsl2512";
 component E: e.TPS259470LRPWR;
 component Q: q.CSD18540Q5B;
 component F: f.FUSE_0451002_MRL;
 component B: b.WSL2512R5000FEA { value = 0.5ohm; }
}'''

def test_exact_terminals_and_open_drain_fault():
    ir=compile_board(FIXTURE)
    assert pins(ir,"e.TPS259470LRPWR")==dict(zip(
        ["EN_UVLO","OVLO","AUXOFF","FLT_N","IN","OUT","DVDT","GND","ILM","ITIMER"],map(str,range(1,11))))
    assert pins(ir,"q.CSD18540Q5B")==dict(zip(
        ["S1","S2","S3","G","D5","D6","D7","D8","D_PAD"],map(str,range(1,10))))
    assert "open_drain" in part(ir,"e.TPS259470LRPWR")["pins"]["FLT_N"]["profile"]["drive_modes"]
    assert pins(ir,"f.FUSE_0451002_MRL")=={"P1":"1","P2":"2"}
    assert pins(ir,"b.WSL2512R5000FEA")=={"P1":"1","P2":"2"}

def test_strict_managed_footprint_audit():
    assert audit_footprints(FIXTURE,strict=True)["passed"]

def test_land_patterns_preserve_power_area_and_contact_count():
    ep=(ROOT/"packages/parts/ti/tps25947/footprints/TI_RPW0010A_TPS25947.kicad_mod").read_text()
    qp=(ROOT/"packages/parts/ti/csd18540q5b/footprints/TI_Q5B_CSD18540.kicad_mod").read_text()
    assert set(re.findall(r'\(pad "(\d+)"',ep))==set(map(str,range(1,11)))
    for n in [1,4,7,10]:
        assert ep.count(f'(pad "{n}"')==2
    # TI RPW p73: both current-carrying lands are .3x2.4, not small signal lands.
    assert ep.count('(size 0.3 2.4)')==2
    assert set(re.findall(r'\(pad "(\d+)"',qp))==set(map(str,range(1,10)))
    # TI Q5B p9 full drain rectangle plus four .59x.71 tabs.
    assert '(size 3.85 4.52)' in qp and qp.count('(size 0.59 0.71)')==4
    assert qp.count('(size 1.372 0.71)')==4
    for pkg in ['tps25947','csd18540q5b']:
        assert 'internal_pad_groups' not in (ROOT/f'packages/parts/ti/{pkg}/part.copper').read_text()

def test_reproducible_land_patterns_and_unresolved_contracts():
    spec=importlib.util.spec_from_file_location('recoil_gen',ROOT/'tools/generate/recoil_protection_parts.py')
    gen=importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
    for pkg,name,expected in [('tps25947','TI_RPW0010A_TPS25947',gen.tps25947()),('csd18540q5b','TI_Q5B_CSD18540',gen.csd18540())]:
        assert (ROOT/f'packages/parts/ti/{pkg}/footprints/{name}.kicad_mod').read_text()==expected
        c=load_contract(ROOT/f'packages/parts/ti/{pkg}/qualification.json')
        assert c['production_publishable'] is False
        assert REQUIRED['power'] <= {r['id'] for r in c['requirements']}
        assert all(r['algorithm']=='external' for r in c['requirements'])
