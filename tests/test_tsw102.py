from pathlib import Path
from pcbir.importers import load_kicad_mod

def test_tsw_manufacturer_hole_pattern():
    path=Path(__file__).parents[1]/"packages/parts/samtec/tsw-102-07-g-s/footprints/TSW102_1.02mm.kicad_mod"
    pads=sorted(load_kicad_mod(path).footprint.pads,key=lambda p:p.number)
    assert len(pads)==2
    assert [p.position.y_nm for p in pads]==[0,2540000]
    assert all(p.drill.width_nm==1020000 and p.drill.height_nm==1020000 for p in pads)
    assert all(p.size.width_nm==1700000 for p in pads)
