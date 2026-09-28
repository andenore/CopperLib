"""Pin and land checks for the fitted Cortex Debug SMD header."""

from pathlib import Path

from pcbir import load_kicad_mod


FOOTPRINT = (
    Path(__file__).resolve().parents[1]
    / "footprints/Connector_Debug.pretty/FTSH-105-01-L-DV-007-K.kicad_mod"
)


def test_keyed_smd_cortex_header_has_nine_separate_lands() -> None:
    footprint = load_kicad_mod(FOOTPRINT).footprint
    pads = {pad.number: pad for pad in footprint.pads}

    assert set(pads) == {"1", "2", "3", "4", "5", "6", "8", "9", "10"}
    assert all(pad.has_solder_mask and pad.has_solder_paste for pad in pads.values())
    assert pads["1"].position.x_nm == -1_715_000
    assert pads["1"].position.y_nm == -2_540_000
    assert pads["1"].size.width_nm == 2_790_000
    assert pads["1"].size.height_nm == 740_000
    assert pads["9"].position.y_nm == 2_540_000
