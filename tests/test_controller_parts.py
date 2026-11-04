"""Pin/land identities and manufacturer package dimensions for controller parts."""
from pathlib import Path
import json, re
import pytest
from copper_cli import compile_board, part
ROOT=Path(__file__).resolve().parents[1]
PARTS=[
 ('diodes/dmn6075s','DMN6075S_7',{'G':'1','S':'2','D':'3'}),
 ('ti/sn74lvc1g125','SN74LVC1G125DBVR',{'OE':'1','A':'2','GND':'3','Y':'4','VCC':'5'}),
 ('nexperia/74lvc1g125','NEXPERIA_74LVC1G125GW',{'OE':'1','A':'2','GND':'3','Y':'4','VCC':'5'}),
 ('mcc/sk36a','SK36A_LTP',{'K':'1','A':'2'}),
 ('diodes/b360a','B360A_13_F',{'K':'1','A':'2'}),
 ('littelfuse/smbj30a','SMBJ30A',{'K':'1','A':'2'}),
 ('phoenix/mkds-1.5-5.08','MKDS_1_5_2_5_08',{'P1':'1','P2':'2'}),
 ('phoenix/mkds-1-3.5','MKDS_1_2_3_5',{'P1':'1','P2':'2'}),
 ('ti/sn74cb3t3306','SN74CB3T3306DCUR',{'OE1':'1','A1':'2','B1':'3','GND':'4','A2':'5','B2':'6','OE2':'7','VCC':'8'}),
 ('diodes/ap2112','AP2112K_3V3',{'VIN':'1','GND':'2','EN':'3','NC':'4','VOUT':'5'}),
 ('ti/tps54360','TPS54360DDAR',dict(zip(('BOOT','VIN','EN','RT','FB','COMP','GND','SW','EP'),map(str,range(1,10))))),
 ('ti/tps1h200a','TPS1H200AQDGNRQ1',dict(zip(('IN','DIAG_EN','FAULT','CL','DELAY','GND','OUT','VS','EP'),map(str,range(1,10))))),
 ('recom/r78k','R78K12_1A',{'VIN':'1','GND':'2','VOUT':'3'}),
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

def lands(path):
 """Numbered pads of a CopperLib footprint as (number, x, y, width, height, drill) in mm."""
 text=(ROOT/'packages/parts'/path).read_text()
 found=re.findall(r'\(pad "(\w+)" \w+ \w+ \(at (\S+) (\S+)\) \(size (\S+) (\S+)\)(?: \(drill (\S+)\))?',text)
 return [(n,*(float(v) for v in values[:4]),float(values[4]) if values[4] else None) for n,*values in found]

def test_phoenix_terminal_land_pattern_matches_drilling_plan():
 assert lands('phoenix/mkds-1.5-5.08/footprints/Phoenix_MKDS_1_5_2_5_08.kicad_mod')==[('1',0,0,2.6,2.6,1.3),('2',5.08,0,2.6,2.6,1.3)]

def test_phoenix_mkds1_land_pattern_matches_drilling_plan():
 assert lands('phoenix/mkds-1-3.5/footprints/Phoenix_MKDS_1_2_3_5.kicad_mod')==[('1',0,0,2,2,1.1),('2',3.5,0,2,2,1.1)]

def test_high_side_switch_land_pattern_matches_dgn0008k():
 pads={n:rest for n,*rest in lands('ti/tps1h200a/footprints/HVSSOP-8-1EP_3x3mm_P0.65mm_EP1.57x1.89mm.kicad_mod')}
 assert pads['1']==[-2.2,-0.975,1.4,0.45,None] and pads['8']==[2.2,-0.975,1.4,0.45,None]
 assert pads['4']==[-2.2,0.975,1.4,0.45,None] and pads['5']==[2.2,0.975,1.4,0.45,None]
 assert pads['9'][:4]==[0,0,1.57,1.89]

def test_r78k_land_pattern_matches_pinning():
 assert [(n,x,y,d) for n,x,y,_,_,d in lands('recom/r78k/footprints/RECOM_R78K_1A.kicad_mod')]==[('1',-2.54,0,1.1),('2',0,0,1.1),('3',2.54,0,1.1)]
