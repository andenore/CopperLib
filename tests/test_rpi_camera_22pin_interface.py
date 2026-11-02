"""Raspberry Pi 22-pin camera interface modules (camera end and host port).

The expected pin table was transcribed from the Raspberry Pi camera pinout
(Raspberry Pi pin -> signal), not copied from the module files. The camera end
numbers its connector like Raspberry Pi pins; the host port is mirrored (pin k
on standard pad 23 - k), so a flat cable between them joins like signals.
The FH34 camera end numbers its contacts from the right, so it carries Raspberry
Pi pin k on contact 23 - k, in the same place as the GUOCONN end.
"""
import re

from copper_cli import ROOT, check, compile_board, endpoint, part

INTERFACE = "github.com/andenore/CopperLib/packages/interfaces/raspberry-pi/camera-22pin"
PI_PINOUT = {
    1: "GND", 2: "D0_N", 3: "D0_P", 4: "GND", 5: "D1_N", 6: "D1_P", 7: "GND",
    8: "CLK_N", 9: "CLK_P", 10: "GND", 11: "D2_N", 12: "D2_P", 13: "GND",
    14: "D3_N", 15: "D3_P", 16: "GND", 17: "IO0", 18: "IO1", 19: "GND",
    20: "SCL", 21: "SDA", 22: "V3V3",
}
SIGNALS = sorted({name for name in PI_PINOUT.values() if name != "GND"})


def _board(camera: str = "RPI_CAMERA_22PIN_CAMERA_END") -> str:
    nets = "\n".join(f"            net {name} {{ CAM.{name}; HOST.{name}; }}" for name in SIGNALS)
    return f'''
        board CameraLoop {{
            import rpi "{INTERFACE}";
            module CAM: rpi.{camera};
            module HOST: rpi.RPI_CAMERA_22PIN_HOST_PORT;
            supply GND {{ voltage = 0V; external = true; }}
            supply V3V3 {{ voltage = 3.3V; external = true; }}
            net GND {{ CAM.GND; HOST.GND; }}
{nets}
        }}
    '''


def _pad_map(module: str, part_suffix: str, camera: str = "RPI_CAMERA_22PIN_CAMERA_END") -> dict[str, str]:
    """Connector land number -> module port, from the hierarchical IR."""
    (definition,) = [item for item in compile_board(_board(camera))["module_definitions"]
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


FH34 = "RPI_CAMERA_22PIN_CAMERA_END_FH34"


def _pad_x(footprint: str) -> dict[str, float]:
    """Signal pad number -> x position in a CopperLib footprint file."""
    text = (ROOT / "packages/parts" / footprint).read_text()
    return {number: float(x) for number, x in re.findall(r'\(pad "(\d+)" smd rect \(at (\S+) ', text)}


def test_fh34_footprint_numbers_contacts_from_the_right():
    guoconn = _pad_x("guoconn/0.5k-gx-22pwb-r/footprints/Connector_GUOCONN.pretty/GUOCONN_0.5K-GX-22PWB-R.kicad_mod")
    fh34 = _pad_x("hirose/fh34srj-22s-0.5sh/footprints/Connector_Hirose.pretty/"
                  "Hirose_FH34SRJ-22S-0.5SH_1x22-1MP_P0.50mm_Horizontal.kicad_mod")
    assert all(fh34[str(j)] == guoconn[str(23 - j)] for j in range(1, 23))


def test_fh34_camera_end_carries_raspberry_pi_pin_k_on_contact_23_minus_k():
    pads = _pad_map(FH34, "HIROSE_FH34SRJ_22S_0_5SH", FH34)
    assert pads == {**{str(23 - pin): name for pin, name in PI_PINOUT.items()}, "MP": "GND"}


def test_fh34_camera_end_puts_each_signal_where_the_guoconn_end_does():
    guoconn = _pad_map("RPI_CAMERA_22PIN_CAMERA_END", "GUOCONN_0_5K_GX_22PWB_R")
    fh34 = _pad_map(FH34, "HIROSE_FH34SRJ_22S_0_5SH", FH34)
    assert all(fh34[str(23 - j)] == guoconn[str(j)] for j in range(1, 23))
    assert check(_board(FH34)) == []
