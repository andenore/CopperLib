"""TI SBOS863D page 3 DCK pin contract, through the public package import."""
import pytest
from copper_cli import compile_board, part, pins

@pytest.mark.parametrize("variant", ["INA190A1IDCKR", "INA190A5IDCKR"])
def test_dck_pin_contract(variant):
    board = compile_board(
        'board Test { import sense "github.com/andenore/CopperLib/packages/parts/ti/ina190";'
        f' component U: sense.{variant};' + ' }')
    # DCK differs from enable-equipped DDF/RSW packages.
    assert pins(board, f"sense.{variant}") == {
        "REF": "1", "GND": "2", "VS": "3", "INP": "4", "INN": "5", "OUT": "6"}
    assert part(board, f"sense.{variant}")["footprints"][0] == "Package_TO_SOT_SMD:SOT-363_SC-70-6"
