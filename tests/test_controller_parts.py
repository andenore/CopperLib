"""Pin/land identities and manufacturer package dimensions for controller parts."""
from pathlib import Path
import json
import pytest
from pcbir import compile_source, load_kicad_mod
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
 jack=load_kicad_mod(base/'hanrun/hr911130a/footprints/Hanrun_HR911130A.kicad_mod').footprint
 pads={p.number:p for p in jack.pads if p.number and p.number!='15'}
 assert (pads['1'].position.x_nm,pads['1'].position.y_nm)==(5715000,8890000)
 assert (pads['10'].position.x_nm,pads['10'].position.y_nm)==(-5715000,6350000)
 assert [pads[str(i)].position.x_nm for i in range(11,15)]==[6625000,4085000,-4085000,-6625000]
 assert len([p for p in jack.pads if p.number=='15'])==2
 assert sorted(p.drill.width_nm for p in jack.pads if not p.number)==[3250000,3250000]
 ind=load_kicad_mod(base/'wurth/7447797820/footprints/WE_PDF_1045.kicad_mod').footprint
 assert [(p.position.y_nm,p.size.width_nm,p.size.height_nm) for p in ind.pads]==[(-4100000,3400000,2400000),(4100000,3400000,2400000)]
 power=load_kicad_mod(base/'kefa/kf128/footprints/KEFA_KF128_2P.kicad_mod').footprint
 assert [p.position.x_nm for p in power.pads]==[0,5080000]
 assert all(p.drill.width_nm==1400000 for p in power.pads)
 buck=load_kicad_mod(base/'ti/tps54360/footprints/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.71x3.7mm_ThermalVias.kicad_mod').footprint
 drills=[p for p in buck.pads if p.number=='9' and p.drill is not None]
 assert len(drills)==6 and all(p.drill.width_nm==200000 for p in drills)
