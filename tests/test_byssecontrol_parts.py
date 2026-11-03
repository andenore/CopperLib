"""Pin/land identities and manufacturer package dimensions for controller parts."""
from pathlib import Path
import json
import pytest
from pcbir import compile_source, load_kicad_mod
ROOT=Path(__file__).resolve().parents[1]
PARTS=[
 ('diodes/dmn6075s','DMN6075S_7',{'G':'1','S':'2','D':'3'}),
 ('ti/sn74lvc1g125','SN74LVC1G125DBVR',{'OE':'1','A':'2','GND':'3','Y':'4','VCC':'5'}),
 ('nexperia/74lvc1g125','NEXPERIA_74LVC1G125GW',{'OE':'1','A':'2','GND':'3','Y':'4','VCC':'5'}),
 ('mcc/sk36a','SK36A_LTP',{'K':'1','A':'2'}),
 ('littelfuse/smbj30a','SMBJ30A',{'K':'1','A':'2'}),
 ('phoenix/mkds-1.5-5.08','MKDS_1_5_2_5_08',{'P1':'1','P2':'2'}),
 ('phoenix/mkds-1-3.5','MKDS_1_2_3_5',{'P1':'1','P2':'2'}),
 ('ti/sn74cb3t3306','SN74CB3T3306DCUR',{'OE1':'1','A1':'2','B1':'3','GND':'4','A2':'5','B2':'6','OE2':'7','VCC':'8'}),
 ('diodes/ap2112','AP2112K_3V3',{'VIN':'1','GND':'2','EN':'3','NC':'4','VOUT':'5'}),
 ('ti/tps54360','TPS54360DDAR',dict(zip(('BOOT','VIN','EN','RT','FB','COMP','GND','SW','EP'),map(str,range(1,10))))),
 ('ti/tps1h200a','TPS1H200AQDGNRQ1',dict(zip(('IN','DIAG_EN','FAULT','CL','DELAY','GND','OUT','VS','EP'),map(str,range(1,10))))),
 ('recom/r78k','R78K12_1A',{'VIN':'1','GND':'2','VOUT':'3'}),
 ('ti/sn74ahct541','SN74AHCT541PWR',{'OE1':'1','OE2':'19','VCC':'20','GND':'10',**{f'A{i}':str(i+1) for i in range(1,9)},**{f'Y{i}':str(19-i) for i in range(1,9)}}),
]
@pytest.mark.parametrize('path,symbol,pins',PARTS)
def test_source_bound_pin_contract(tmp_path,path,symbol,pins):
 (tmp_path/'copper.mod').write_text('module parts-test\nrequire github.com/andenore/CopperLib workspace\n'+f'replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n')
 b=compile_source(f'board Test {{ import p "github.com/andenore/CopperLib/packages/parts/{path}"; component U: p.{symbol}; }}',str(tmp_path/'board.copper'),offline=True)
 part=b.library['p.'+symbol]
 assert {k:v.number for k,v in part.pins.items()}==pins
 evidence=json.loads((ROOT/'packages/parts'/path/'evidence/source.json').read_text())
 assert part.source.checksum=='sha256:'+evidence['sha256']
 assert not part.internal_pad_groups

def test_custom_land_patterns_have_correct_polarity_drills_and_spacing():
 base=ROOT/'packages/parts'
 ind=load_kicad_mod(base/'wurth/7447797820/footprints/WE_PDF_1045.kicad_mod').footprint
 assert [(p.position.y_nm,p.size.width_nm,p.size.height_nm) for p in ind.pads]==[(-4100000,3400000,2400000),(4100000,3400000,2400000)]
 power=load_kicad_mod(base/'kefa/kf128/footprints/KEFA_KF128_2P.kicad_mod').footprint
 assert [p.position.x_nm for p in power.pads]==[0,5080000]
 assert all(p.drill.width_nm==1400000 for p in power.pads)
 buck=load_kicad_mod(base/'ti/tps54360/footprints/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.71x3.7mm_ThermalVias.kicad_mod').footprint
 drills=[p for p in buck.pads if p.number=='9' and p.drill is not None]
 assert len(drills)==6 and all(p.drill.width_nm==200000 for p in drills)

def test_phoenix_terminal_land_pattern_matches_drilling_plan():
 fp=load_kicad_mod(ROOT/'packages/parts/phoenix/mkds-1.5-5.08/footprints/Phoenix_MKDS_1_5_2_5_08.kicad_mod').footprint
 assert [(p.number,p.position.x_nm,p.position.y_nm) for p in fp.pads]==[('1',0,0),('2',5080000,0)]
 assert all(p.drill.width_nm==1300000 and p.size.width_nm==2600000 for p in fp.pads)

def test_phoenix_mkds1_land_pattern_matches_drilling_plan():
 fp=load_kicad_mod(ROOT/'packages/parts/phoenix/mkds-1-3.5/footprints/Phoenix_MKDS_1_2_3_5.kicad_mod').footprint
 assert [(p.number,p.position.x_nm,p.position.y_nm) for p in fp.pads]==[('1',0,0),('2',3500000,0)]
 assert all(p.drill.width_nm==1100000 and p.size.width_nm==2000000 for p in fp.pads)

def test_high_side_switch_land_pattern_matches_dgn0008k():
 fp=load_kicad_mod(ROOT/'packages/parts/ti/tps1h200a/footprints/HVSSOP-8-1EP_3x3mm_P0.65mm_EP1.57x1.89mm.kicad_mod').footprint
 lands={p.number:(p.position.x_nm,p.position.y_nm,p.size.width_nm,p.size.height_nm) for p in fp.pads if p.number}
 assert lands['1']==(-2200000,-975000,1400000,450000) and lands['8']==(2200000,-975000,1400000,450000)
 assert lands['4']==(-2200000,975000,1400000,450000) and lands['5']==(2200000,975000,1400000,450000)
 assert lands['9']==(0,0,1570000,1890000)

def test_r78k_land_pattern_matches_pinning():
 fp=load_kicad_mod(ROOT/'packages/parts/recom/r78k/footprints/RECOM_R78K_1A.kicad_mod').footprint
 assert [(p.number,p.position.x_nm,p.position.y_nm) for p in fp.pads]==[('1',-2540000,0),('2',0,0),('3',2540000,0)]
 assert all(p.drill.width_nm==1100000 for p in fp.pads)
