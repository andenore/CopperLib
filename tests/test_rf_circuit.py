from copper_cli import check, compile_board


BOARD = """board Radio {
    import rf "github.com/andenore/CopperLib/packages/circuits/nordic/nrf52832-johanson-reference";
    module RADIO: rf.Nrf52832JohansonRf;
    net VDD { RADIO.VDD; }
    net GND { RADIO.GND; }
    net SWDIO { RADIO.SWDIO; }
    net SWDCLK { RADIO.SWDCLK; }
    net RESET { RADIO.RESET; }
    net ANT { RADIO.RF_OUT; }
    supply VDD { voltage = 3V; external = true; }
    supply GND { voltage = 0V; external = true; }
}"""


def test_nrf_johanson_reference_circuit_is_reusable():
    assert not check(BOARD)
    assert "rf.Nrf52832JohansonRf" in {item["name"] for item in compile_board(BOARD)["module_definitions"]}
