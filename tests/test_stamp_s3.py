from pathlib import Path
import json, re, subprocess, sys
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'packages/profiles/m5stack/stamp-s3'

def test_source_generation_and_header_rows():
    subprocess.run([sys.executable,str(PKG/'generate.py'),'--check'],check=True)
    data=json.loads((PKG/'evidence/connector.json').read_text())
    for side,n in [('left',9),('right',6)]:
        for name in (f'HCTL_PM254_1_{n:02}_Z_8_5', f'WE_6130{n:02}11821', f'Harwin_M20_782{n:02}42'):
            text=(PKG/f'footprints/{name}.kicad_mod').read_text()
            pads=re.findall(r'\(pad "(\d+)" thru_hole \w+ \(at 0 ([\d.]+)\) \(size 2 2\) \(drill 1\.02\)', text)
            assert [(int(p),Decimal(y)) for p,y in pads]==[(i,Decimal('2.54')*(i-1)) for i in range(1,n+1)], name
        rows=data[side]
        assert len(rows)==n
        for a,b in zip(rows,rows[1:]):
            assert Decimal(b['y_mm'])-Decimal(a['y_mm'])==Decimal('2.54')
    assert [p['module_pad'] for p in data['left']]==list(range(1,18,2))
    assert [p['module_pad'] for p in data['right']]==list(range(28,17,-2))
    assert data['left'][6]['signal']=='VIN_5V'
    assert data['right'][0]['signal']=='V3V3'
