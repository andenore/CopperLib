from pathlib import Path
import json, subprocess, sys
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'packages/profiles/m5stack/stamp-s3'

def test_source_generation_and_header_rows():
    subprocess.run([sys.executable,str(PKG/'generate.py'),'--check'],check=True)
    data=json.loads((PKG/'evidence/connector.json').read_text())
    for side,n in [('left',9),('right',6)]:
        assert (PKG/f'footprints/HCTL_PM254_1_{n:02}_Z_8_5.kicad_mod').is_file()
        rows=data[side]
        assert len(rows)==n
        for a,b in zip(rows,rows[1:]):
            assert Decimal(b['y_mm'])-Decimal(a['y_mm'])==Decimal('2.54')
    assert [p['module_pad'] for p in data['left']]==list(range(1,18,2))
    assert [p['module_pad'] for p in data['right']]==list(range(28,17,-2))
    assert data['left'][6]['signal']=='VIN_5V'
    assert data['right'][0]['signal']=='V3V3'
