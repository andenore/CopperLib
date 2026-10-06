"""STM32G0C1 I2C1/I2C2/I2C3 mux selectors from the data-sheet AF tables."""

from pathlib import Path

import pytest

from pcbir import check, compile_source

ROOT = Path(__file__).resolve().parents[1]


def _compile(tmp_path, body: str):
    (tmp_path / "copper.mod").write_text(
        "module stm32g0c1-i2c-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    return compile_source(body, str(tmp_path / "board.copper"), offline=True)


def _i2c_board(tmp_path, peripheral: str, scl: str, sda: str):
    return _compile(tmp_path, f'''
        board MuxFixture {{
            import st "github.com/andenore/CopperLib/packages/parts/st/stm32g0c1";
            component U: st.STM32G0C1RET6;
            configure U.{peripheral} as BUS {{ SCL = {scl}; SDA = {sda}; }}
            net V3V3 {{ U.VDD; U.VBAT; U.VREF_PLUS; }}
            net GND {{ U.VSS; }}
            supply V3V3 {{ voltage = 3.3V; external = true; }}
            supply GND {{ voltage = 0V; external = true; }}
        }}
    ''')


# DS13564 Rev 2 Tables 13-16: AF6 rows for I2C1/I2C2/I2C3 on port B, and
# PA6/PA7 carrying I2C2 on AF8 and I2C3 on AF9 (AF6 there is not I2C).
@pytest.mark.parametrize(("peripheral", "scl", "sda", "selector"), [
    ("I2C1", "PB8", "PB9", "AF6"),
    ("I2C1", "PB6", "PB7", "AF6"),
    ("I2C2", "PB10", "PB11", "AF6"),
    ("I2C2", "PB13", "PB14", "AF6"),
    ("I2C2", "PA7", "PA6", "AF8"),
    ("I2C3", "PB3", "PB4", "AF6"),
    ("I2C3", "PA7", "PA6", "AF9"),
])
def test_stm32g0c1_i2c_mux_selectors(tmp_path, peripheral, scl, sda, selector):
    board = _i2c_board(tmp_path, peripheral, scl, sda)
    selection = board.peripheral_selections[0]
    assert selection.signals["SCL"].selector == selector
    assert selection.signals["SDA"].selector == selector
    assert check(board) == []
