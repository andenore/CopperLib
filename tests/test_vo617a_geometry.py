"""Vishay 83430 Rev 2.8 Fig. 17, Option 7 land pattern and assembly envelope."""
from pathlib import Path
from pcbir import load_kicad_mod

PATH = Path(__file__).resolve().parents[1] / 'packages/parts/vishay/vo617a/footprints/VO617A_OPTION7.kicad_mod'


def test_option7_land_pattern_and_top_view_pin_order():
    footprint = load_kicad_mod(PATH, strict=True).footprint
    pads = {p.number:p for p in footprint.pads}
    assert set(pads) == {'1', '2', '3', '4'}
    assert all((p.size.width_nm, p.size.height_nm) == (1520000, 1780000) for p in pads.values())
    assert pads['1'].position.x_nm == pads['2'].position.x_nm == -4765000
    assert pads['3'].position.x_nm == pads['4'].position.x_nm == 4765000
    assert pads['1'].position.y_nm == pads['4'].position.y_nm == -1270000
    assert pads['2'].position.y_nm == pads['3'].position.y_nm == 1270000
    assert pads['4'].position.x_nm - pads['1'].position.x_nm - 1520000 == 8010000


def test_courtyard_encloses_every_terminal_land_with_assembly_margin():
    footprint = load_kicad_mod(PATH, strict=True).footprint
    left = min(p.x_nm for p in footprint.courtyard)
    right = max(p.x_nm for p in footprint.courtyard)
    top = min(p.y_nm for p in footprint.courtyard)
    bottom = max(p.y_nm for p in footprint.courtyard)
    for pad in footprint.pads:
        assert pad.position.x_nm - pad.size.width_nm // 2 >= left + 250000
        assert pad.position.x_nm + pad.size.width_nm // 2 <= right - 250000
        assert pad.position.y_nm - pad.size.height_nm // 2 >= top + 250000
        assert pad.position.y_nm + pad.size.height_nm // 2 <= bottom - 250000
    # Also encloses maximum 6.5 +/-0.5 by 4.58 +/-0.3 mm molded body.
    assert left < -3500000 and right > 3500000
    assert top < -2440000 and bottom > 2440000
