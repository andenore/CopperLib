"""Vishay 30100 p2: exact resistance-dependent land pattern."""
from copper_cli import compile_board, pins

def test_wsl_public_terminal_contract():
    board=compile_board(
        'board Test { import shunts "github.com/andenore/CopperLib/packages/parts/vishay/wsl2512";'
        ' component R: shunts.WSL2512R0500FEA { value = 0.05 ohm; } }')
    assert pins(board,"shunts.WSL2512R0500FEA")=={"P1":"1","P2":"2"}
