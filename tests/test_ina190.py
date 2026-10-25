"""TI SBOS863D page 3 DCK pin contract, through the public package import."""
from pathlib import Path
import pytest
from pcbir import compile_source

ROOT = Path(__file__).parents[1]

@pytest.mark.parametrize("variant", ["INA190A1IDCKR", "INA190A5IDCKR"])
def test_dck_pin_contract(tmp_path, variant):
    (tmp_path / "copper.mod").write_text(
        "module ina190-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    board = compile_source(
        'board Test { import sense "github.com/andenore/CopperLib/packages/parts/ti/ina190";'
        f' component U: sense.{variant};' + ' }',
        str(tmp_path / "board.copper"), offline=True)
    part = board.library[f"sense.{variant}"]
    # DCK differs from enable-equipped DDF/RSW packages.
    assert {name: pin.number for name, pin in part.pins.items()} == {
        "REF": "1", "GND": "2", "VS": "3", "INP": "4", "INN": "5", "OUT": "6"}
    assert part.footprints[0] == "Package_TO_SOT_SMD:SOT-363_SC-70-6"

