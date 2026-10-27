"""STM32G0C1 I2C1/I2C2/I2C3 mux selectors from the data-sheet AF tables."""

import pytest

from copper_cli import check, compile_board


def _i2c_board(peripheral: str, scl: str, sda: str):
    return f'''
        board MuxFixture {{
            import st "github.com/andenore/CopperLib/packages/parts/st/stm32g0c1";
            component U: st.STM32G0C1RET6;
            configure U.{peripheral} as BUS {{ SCL = {scl}; SDA = {sda}; }}
            net V3V3 {{ U.VDD; U.VBAT; U.VREF_PLUS; }}
            net GND {{ U.VSS; }}
            supply V3V3 {{ voltage = 3.3V; external = true; }}
            supply GND {{ voltage = 0V; external = true; }}
        }}
    '''


# DS13564 Rev 5 Tables 13-16: AF6 rows for I2C1/I2C2/I2C3 on port B, and
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
def test_stm32g0c1_i2c_mux_selectors(peripheral, scl, sda, selector):
    source = _i2c_board(peripheral, scl, sda)
    selection = compile_board(source)["peripheral_selections"][0]
    assert selection["signals"]["SCL"]["selector"] == selector
    assert selection["signals"]["SDA"]["selector"] == selector
    assert check(source) == []


# DS13564 Rev 5 Table 12 lists USB_DM/USB_DP as PA11/PA12 additional
# functions; Table 14 has no AF8-AF15 entry for either pin.
def test_stm32g0c1_usb_is_additional_function():
    source = """
        board MuxFixture {
            import st "github.com/andenore/CopperLib/packages/parts/st/stm32g0c1";
            component U: st.STM32G0C1RET6;
            configure U.USB_FS as HOST { DP = PA12; DM = PA11; }
            net V3V3 { U.VDD; U.VBAT; U.VREF_PLUS; }
            net GND { U.VSS; }
            supply V3V3 { voltage = 3.3V; external = true; }
            supply GND { voltage = 0V; external = true; }
        }
    """
    selection = compile_board(source)["peripheral_selections"][0]
    assert selection["signals"]["DP"]["selector"] == "additional"
    assert selection["signals"]["DM"]["selector"] == "additional"
    assert check(source) == []
