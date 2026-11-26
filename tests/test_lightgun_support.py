"""Public-CLI checks for camera power switching and nRF52 bus selection."""
import pytest

from copper_cli import check, compile_board, part, pins


SWITCH = '''board CameraPower {
    import sw "github.com/andenore/CopperLib/packages/parts/ti/tps22918";
    component U: sw.TPS22918DBVR;
    net VDD { U.VIN; U.ON; }
    net GND { U.GND; }
    net CAMERA { U.VOUT; U.QOD; }
    no_connect U.CT { reason = "default rise time"; }
    supply VDD { voltage = 3.3V; external = true; }
    supply GND { voltage = 0V; external = true; }
}'''


def test_tps22918_pin_map_and_legal_switch_topology():
    assert check(SWITCH) == []
    ir = compile_board(SWITCH)
    assert pins(ir, "sw.TPS22918DBVR") == {
        "VIN": "1", "GND": "2", "ON": "3", "CT": "4", "QOD": "5", "VOUT": "6",
    }
    assert part(ir, "sw.TPS22918DBVR")["source"]["checksum"] == (
        "sha256:1b28eb58003d28b18bf919a15734056f296a499bebee2bd493a1e4358c4dfb1c"
    )


@pytest.mark.parametrize("source, code", [
    (SWITCH.replace(" U.ON;", ""), "REQUIRED_PIN_UNCONNECTED"),
    (SWITCH.replace("voltage = 3.3V", "voltage = 6V"), "SUPPLY_VOLTAGE_HIGH"),
])
def test_tps22918_rejects_floating_enable_and_overvoltage(source, code):
    assert code in {d["code"] for d in check(source)}


def test_nrf_twim0_uses_register_selected_open_drain_pins():
    source = '''board CameraBus {
        import nordic "github.com/andenore/CopperLib/packages/parts/nordic/nrf52832";
        component U: nordic.NRF52832_QFAA;
        configure U.TWIM0 as CAMERA { SDA = P0_26; SCL = P0_27; }
        net VDD { U.VDD_1; U.VDD_2; U.VDD_3; }
        net GND { U.VSS_1; U.VSS_2; U.VSS_EP; }
        supply VDD { voltage = 3.3V; external = true; }
        supply GND { voltage = 0V; external = true; }
    }'''
    selection = compile_board(source)["peripheral_selections"][0]
    assert selection["signals"]["SDA"]["selector"] == "PSEL.SDA=26"
    assert selection["signals"]["SCL"]["selector"] == "PSEL.SCL=27"
    assert check(source) == []


@pytest.mark.parametrize("sck,mosi,miso", [(14, 13, 12), (27, 26, 25)])
def test_nrf_spi0_register_selected_pins_preserve_existing_alternative(sck, mosi, miso):
    source = f'''board PeripheralBus {{
        import nordic "github.com/andenore/CopperLib/packages/parts/nordic/nrf52832";
        component U: nordic.NRF52832_QFAA;
        configure U.SPI0 as SPI {{ SCK = P0_{sck:02}; MOSI = P0_{mosi:02}; MISO = P0_{miso:02}; }}
        net VDD {{ U.VDD_1; U.VDD_2; U.VDD_3; }}
        net GND {{ U.VSS_1; U.VSS_2; U.VSS_EP; }}
        supply VDD {{ voltage = 3.3V; external = true; }}
        supply GND {{ voltage = 0V; external = true; }}
    }}'''
    selection = compile_board(source)["peripheral_selections"][0]
    for signal, pin in (("SCK", sck), ("MOSI", mosi), ("MISO", miso)):
        assert selection["signals"][signal]["selector"] == f"PSEL.{signal}={pin}"
    assert check(source) == []
