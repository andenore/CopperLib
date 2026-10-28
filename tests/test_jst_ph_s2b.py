"""Manufacturer circuit numbering and mechanical-tab audit for the two-way PH."""
from pathlib import Path
import hashlib, json
from copper_cli import compile_board, part

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'packages/parts/jst/ph-s2b-sm4'

def test_source_bound_pin_contract_and_no_invented_tab_continuity():
    board=compile_board('board Test { import j "github.com/andenore/CopperLib/packages/parts/jst/ph-s2b-sm4"; component J1: j.JST_S2B_PH_SM4_TB; }')
    connector=part(board,'j.JST_S2B_PH_SM4_TB')
    assert {name: pin['number'] for name,pin in connector['pins'].items()} == {'P1':'1','P2':'2','MP':'MP'}
    assert not connector['internal_pad_groups']
    audit=json.loads((PKG/'evidence/s2b-ph-sm4-audit.json').read_text())
    path=PKG/audit['footprint']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==audit['footprint_source']['sha256']
