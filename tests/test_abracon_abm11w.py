"""Abracon ABM11W 25 MHz crystal: terminals and source."""
from copper_cli import check, compile_board, part, pins

LIB = "github.com/andenore/CopperLib/packages"
NAME = "abracon.ABRACON_ABM11W_25_0000MHZ_8_D1X_T3"
SOURCE = f'''board CrystalFixture {{
    import abracon "{LIB}/parts/abracon/abm11w";
    component Y1: abracon.ABRACON_ABM11W_25_0000MHZ_8_D1X_T3;
    supply GND {{ voltage = 0V; external = true; }}
    net X1 {{ Y1.XTAL1; }}
    net X2 {{ Y1.XTAL2; }}
    net GND {{ Y1.GND_2; Y1.GND_4; }}
}}'''


def test_crystal_spans_the_diagonal_with_ground_on_the_other():
    board = compile_board(SOURCE)
    # Page 5: #1 and #3 are the crystal, #2 and #4 GND, as in KiCad's 2016 land.
    assert pins(board, NAME) == {"XTAL1": "1", "GND_2": "2", "XTAL2": "3", "GND_4": "4"}
    definition = part(board, NAME)
    assert definition["footprints"] == ["Crystal:Crystal_SMD_2016-4Pin_2.0x1.6mm"]
    assert definition["source"]["checksum"].startswith("sha256:8f1b6c4d")


def test_fixture_passes_erc():
    assert check(SOURCE) == []
