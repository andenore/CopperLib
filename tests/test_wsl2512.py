"""Vishay 30100 p2: exact resistance-dependent land pattern."""
from pathlib import Path
from pcbir import compile_source
from pcbir.importers import load_kicad_mod

ROOT=Path(__file__).parents[1]
PACKAGE=ROOT/"packages/parts/vishay/wsl2512"

def test_wsl_public_terminal_contract(tmp_path):
    (tmp_path/"copper.mod").write_text(
        "module wsl-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    board=compile_source(
        'board Test { import shunts "github.com/andenore/CopperLib/packages/parts/vishay/wsl2512";'
        ' component R: shunts.WSL2512R0500FEA { value = 0.05 ohm; } }',
        str(tmp_path/"board.copper"),offline=True)
    part=board.library["shunts.WSL2512R0500FEA"]
    assert {n:p.number for n,p in part.pins.items()}=={"P1":"1","P2":"2"}

def test_wsl_resistance_specific_lands():
    fp=load_kicad_mod(PACKAGE/"footprints/WSL2512_7m_to_500m.kicad_mod").footprint
    assert len(fp.pads)==2
    pads=sorted(fp.pads,key=lambda p:p.number)
    assert [p.position.x_nm for p in pads]==[-2855000,2855000]
    assert all(p.size.width_nm==1650000 and p.size.height_nm==3680000 for p in pads)
    assert pads[1].position.x_nm-pads[0].position.x_nm-pads[0].size.width_nm==4060000
