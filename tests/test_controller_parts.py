"""Pin/land identities and manufacturer package dimensions for controller parts."""
from pathlib import Path
import json
import pytest
from copper_cli import compile_board, part
ROOT=Path(__file__).resolve().parents[1]
PARTS=[
 ('diodes/dmn6075s','DMN6075S_7',{'G':'1','S':'2','D':'3'}),
 ('ti/sn74lvc1g125','SN74LVC1G125DBVR',{'OE':'1','A':'2','GND':'3','Y':'4','VCC':'5'}),
 ('diodes/ap2112','AP2112K_3V3',{'VIN':'1','GND':'2','EN':'3','NC':'4','VOUT':'5'}),
 ('ti/tps54360','TPS54360DDAR',dict(zip(('BOOT','VIN','EN','RT','FB','COMP','GND','SW','EP'),map(str,range(1,10))))),
 ('ti/sn74ahct541','SN74AHCT541PWR',{'OE1':'1','OE2':'19','VCC':'20','GND':'10',**{f'A{i}':str(i+1) for i in range(1,9)},**{f'Y{i}':str(19-i) for i in range(1,9)}}),
 ('hanrun/hr911130a','HR911130A',{**{f'P{i}':str(i) for i in range(1,15)},'SH':'15'}),
]
@pytest.mark.parametrize('path,symbol,pins',PARTS)
def test_source_bound_pin_contract(path,symbol,pins):
 b=compile_board(f'board Test {{ import p "github.com/andenore/CopperLib/packages/parts/{path}"; component U: p.{symbol}; }}')
 definition=part(b,'p.'+symbol)
 assert {k:v['number'] for k,v in definition['pins'].items()}==pins
 evidence=json.loads((ROOT/'packages/parts'/path/'evidence/source.json').read_text())
 assert definition['source']['checksum']=='sha256:'+evidence['sha256']
 assert not definition['internal_pad_groups']
