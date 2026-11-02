"""Pin contract for the Molex 73251-2200 right-angle SMA."""
from copper_cli import compile_board, part

SOURCE = ('board Test { import sma "github.com/andenore/CopperLib/packages/parts/molex/73251-2200"; '
          'component J1: sma.MOLEX_73251_2200; }')


def test_centre_contact_and_shared_ground_posts():
    connector = part(compile_board(SOURCE), "sma.MOLEX_73251_2200")
    assert connector["manufacturer"] == "Molex"
    assert {name: pin["number"] for name, pin in connector["pins"].items()} == {"SIGNAL": "1", "GND": "2"}
    assert not connector["internal_pad_groups"]

