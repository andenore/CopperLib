"""Manufacturer circuit numbering and mechanical-tab audit for the two-way PH."""
from pathlib import Path
import hashlib, json
from pcbir import compile_source
from pcbir.importers import load_kicad_mod

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'packages/parts/jst/ph-s2b-sm4'

def test_source_bound_land_pattern_and_no_invented_tab_continuity(tmp_path):
    (tmp_path/'copper.mod').write_text('module jst-test\nrequire github.com/andenore/CopperLib v0.1.0\n'+f'replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n')
    board=compile_source('board Test { import j "github.com/andenore/CopperLib/packages/parts/jst/ph-s2b-sm4"; component J1: j.JST_S2B_PH_SM4_TB; }',str(tmp_path/'board.copper'),offline=True)
    part=board.library['j.JST_S2B_PH_SM4_TB']
    assert {name: pin.number for name,pin in part.pins.items()} == {'P1':'1','P2':'2','MP':'MP'}
    assert not part.internal_pad_groups
    audit=json.loads((PKG/'evidence/s2b-ph-sm4-audit.json').read_text())
    path=PKG/audit['footprint']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==audit['footprint_source']['sha256']
    pads=load_kicad_mod(path).footprint.pads
    signals={p.number:p for p in pads if p.number in {'1','2'}}
    assert [(signals[n].position.x_nm,signals[n].position.y_nm) for n in ('1','2')]==[(-1000000,-2850000),(1000000,-2850000)]
    tabs=[p for p in pads if p.number=='MP']
    assert sorted(p.position.x_nm for p in tabs)==[-3350000,3350000]
    assert all(p.position.y_nm==2900000 and p.size.width_nm==1500000 and p.size.height_nm==3400000 for p in tabs)
