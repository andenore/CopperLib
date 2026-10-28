"""Raspberry Pi 22-pin camera interface modules (camera end and host port).

The expected pin table was transcribed from the Raspberry Pi camera pinout
(Raspberry Pi pin -> signal), not copied from the module files. The camera end
numbers its connector like Raspberry Pi pins; the host port is mirrored (pin k
on standard pad 23 - k), so a flat cable between them joins like signals.
"""
from copper_cli import check, compile_board, endpoint, part

INTERFACE = "github.com/andenore/CopperLib/packages/interfaces/raspberry-pi/camera-22pin"
PI_PINOUT = {
    1: "GND", 2: "D0_N", 3: "D0_P", 4: "GND", 5: "D1_N", 6: "D1_P", 7: "GND",
    8: "CLK_N", 9: "CLK_P", 10: "GND", 11: "D2_N", 12: "D2_P", 13: "GND",
    14: "D3_N", 15: "D3_P", 16: "GND", 17: "IO0", 18: "IO1", 19: "GND",
    20: "SCL", 21: "SDA", 22: "V3V3",
}
SIGNALS = sorted({name for name in PI_PINOUT.values() if name != "GND"})


def _board() -> str:
    nets = "\n".join(f"            net {name} {{ CAM.{name}; HOST.{name}; }}" for name in SIGNALS)
    return f'''
        board CameraLoop {{
            import rpi "{INTERFACE}";
            module CAM: rpi.RPI_CAMERA_22PIN_CAMERA_END;
            module HOST: rpi.RPI_CAMERA_22PIN_HOST_PORT;
            supply GND {{ voltage = 0V; external = true; }}
            supply V3V3 {{ voltage = 3.3V; external = true; }}
            net GND {{ CAM.GND; HOST.GND; }}
{nets}
        }}
    '''


def _pad_map(module: str, part_suffix: str) -> dict[str, str]:
    """Connector land number -> module port, from the hierarchical IR."""
    (definition,) = [item for item in compile_board(_board())["module_definitions"]
                     if item["name"] == f"rpi.{module}"]
    (connector,) = definition["components"]
    connector_part = part(definition, connector["part"])
    assert connector_part["name"].endswith(part_suffix)
    mapping: dict[str, str] = {}
    for net in definition["nets"]:
        endpoints = [endpoint(item) for item in net["endpoints"]]
        (port,) = [pin for component, pin in endpoints if component == "port"]
        for component, pin in endpoints:
            if component == connector["ref"]:
                number = connector_part["pins"][pin]["number"]
                assert number not in mapping, number
                mapping[number] = port
    return mapping


def test_camera_end_numbers_its_connector_like_raspberry_pi_pins():
    pads = _pad_map("RPI_CAMERA_22PIN_CAMERA_END", "GUOCONN_0_5K_GX_22PWB_R")
    assert pads == {**{str(pin): name for pin, name in PI_PINOUT.items()}, "MP": "GND"}


def test_host_port_mirrors_raspberry_pi_pins_onto_standard_pads():
    pads = _pad_map("RPI_CAMERA_22PIN_HOST_PORT", "HIROSE_FH12_22S_0_5SH")
    assert pads == {**{str(23 - pin): name for pin, name in PI_PINOUT.items()}, "MP": "GND"}


def test_flat_cable_joins_camera_end_to_host_port_signal_for_signal():
    # A flat, untwisted FFC between two boards both component side up joins
    # pad j at one end to the pad in the mirrored position (23 - j) at the other.
    camera = _pad_map("RPI_CAMERA_22PIN_CAMERA_END", "GUOCONN_0_5K_GX_22PWB_R")
    host = _pad_map("RPI_CAMERA_22PIN_HOST_PORT", "HIROSE_FH12_22S_0_5SH")
    assert all(camera[str(j)] == host[str(23 - j)] for j in range(1, 23))
    assert check(_board()) == []
