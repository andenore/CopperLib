from pathlib import Path
import json, subprocess, sys
from decimal import Decimal
from pcbir.importers.kicad_mod import load_kicad_mod
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'packages/profiles/m5stack/stamp-s3'

def test_source_generation_and_physical_header_geometry():
    subprocess.run([sys.executable,str(PKG/'generate.py'),'--check'],check=True)
    data=json.loads((PKG/'evidence/connector.json').read_text())
    for side,n in [('left',9),('right',6)]:
        fp=load_kicad_mod(PKG/f'footprints/HCTL_PM254_1_{n:02}_Z_8_5.kicad_mod').footprint
        assert len(fp.pads)==n
        for pad in fp.pads:
            assert pad.position.x_nm==0
            assert pad.position.y_nm==(int(pad.number)-1)*2540000
            assert pad.drill.width_nm==pad.drill.height_nm==1020000
        rows=data[side]
        assert len(rows)==n
        for a,b in zip(rows,rows[1:]):
            assert Decimal(b['y_mm'])-Decimal(a['y_mm'])==Decimal('2.54')
    assert [p['module_pad'] for p in data['left']]==list(range(1,18,2))
    assert [p['module_pad'] for p in data['right']]==list(range(28,17,-2))
    assert data['left'][6]['signal']=='VIN_5V'
    assert data['right'][0]['signal']=='V3V3'
