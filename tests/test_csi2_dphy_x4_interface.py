"""Four-lane CSI-2 (D-PHY) interface modules on the I-PEX CABLINE-CA 20525-040E-02.

Expected positions were transcribed independently from the 40-position pinout
table (function per position, source and sink sides), not copied from the
module files. Pairs follow a serializer/deserializer package edge (three data
pairs, clock, data pair); source and sink share the pair positions.
"""
import pytest

from copper_cli import CopperError, check, compile_board, endpoint, flat_components, part

LIB = "github.com/andenore/CopperLib/packages"
HARNESS = f"{LIB}/interfaces/mipi/csi2-dphy-x4-cabline-ca"
POSITIONS = [str(n) for n in range(1, 41)] + ["SH"]
LANE_PORTS = (
    "PAIR_A_P", "PAIR_A_N", "PAIR_B_P", "PAIR_B_N", "PAIR_C_P", "PAIR_C_N",
    "CLK_P", "CLK_N", "PAIR_D_P", "PAIR_D_N",
)

# Function column; None = reserved / not connected.
SOURCE_PINOUT = {
    "1": "GND", "2": None, "3": None, "4": "GND", "5": None, "6": None,
    "7": None, "8": "GND", "9": None, "10": None, "11": "GND", "12": "GND",
    "13": "GND", "14": "PAIR_A_P", "15": "PAIR_A_N", "16": "GND", "17": "PAIR_B_P",
    "18": "PAIR_B_N", "19": "GND", "20": "PAIR_C_P", "21": "PAIR_C_N", "22": "GND",
    "23": "CLK_P", "24": "CLK_N", "25": "GND", "26": "PAIR_D_P", "27": "PAIR_D_N",
    "28": "GND", "29": "GND", "30": "GND", "31": "SDA", "32": "SCL", "33": "GND",
    "34": "DUT_VIO", "35": None, "36": "VDUT_5V", "37": "VDUT_5V", "38": "VDUT_5V",
    "39": "VDUT_5V", "40": "GND", "SH": "GND",
}
# IN column: 5 V, I2C, VIO and reserved positions are "not connected".
SINK_PINOUT = {
    "1": "GND", "2": None, "3": None, "4": "GND", "5": None, "6": None, "7": None,
    "8": "GND", "9": None, "10": None, "11": "GND", "12": "GND", "13": "GND",
    "14": "PAIR_A_P", "15": "PAIR_A_N", "16": "GND", "17": "PAIR_B_P", "18": "PAIR_B_N",
    "19": "GND", "20": "PAIR_C_P", "21": "PAIR_C_N", "22": "GND", "23": "CLK_P",
    "24": "CLK_N", "25": "GND", "26": "PAIR_D_P", "27": "PAIR_D_N", "28": "GND",
    "29": "GND", "30": "GND", "31": None, "32": None, "33": "GND", "34": None,
    "35": None, "36": None, "37": None, "38": None, "39": None, "40": "GND", "SH": "GND",
}
# Example lane assignment: a deserializer port A (source) and a
# serializer CSI-2 input (sink) wired to the pair positions.
EXAMPLE_SOURCE_LANES = {
    "14": "DA2P", "15": "DA2N", "17": "DA3P", "18": "DA3N", "20": "DA0P", "21": "DA0N",
    "23": "CKAP", "24": "CKAN", "26": "DA1P", "27": "DA1N",
}
EXAMPLE_SINK_LANES = {
    "14": "D2P", "15": "D2N", "17": "D3P", "18": "D3N", "20": "D0P", "21": "D0N",
    "23": "CKP", "24": "CKN", "26": "D1P", "27": "D1N",
}
SOURCE_PORT_TYPES = {
    **{name: "passive" for name in LANE_PORTS},
    "VDUT_5V": "power_out", "SDA": "passive", "SCL": "passive",
    "DUT_VIO": "power_out", "GND": "power_in",
}
SINK_PORT_TYPES = {**{name: "passive" for name in LANE_PORTS}, "GND": "power_in"}


def _connector_only_board():
    lanes = "\n".join(
        f"            net {name} {{ J_OUT.{name}; J_IN.{name}; }}" for name in LANE_PORTS)
    return f'''
        board HarnessFixture {{
            import csi2 "{HARNESS}";
            module J_OUT: csi2.CSI2_DPHY_X4_SOURCE_PORT;
            module J_IN: csi2.CSI2_DPHY_X4_SINK_PORT;
            supply GND {{ voltage = 0V; external = true; }}
            supply VDUT_5V {{ voltage = 5V; external = true; }}
            supply DUT_VIO {{ voltage = 1.8V; external = true; }}
            net GND {{ J_OUT.GND; J_IN.GND; }}
            net VDUT_5V {{ J_OUT.VDUT_5V; }}
            net DUT_VIO {{ J_OUT.DUT_VIO; }}
            net SDA {{ J_OUT.SDA; }}
            net SCL {{ J_OUT.SCL; }}
{lanes}
        }}
    '''


def _definition(board, module: str) -> dict:
    (definition,) = [item for item in board["module_definitions"] if item["name"] == f"csi2.{module}"]
    return definition


def _module_position_map(board, module: str) -> dict[str, str | None]:
    """Connector land number -> module port, from the hierarchical IR."""
    definition = _definition(board, module)
    (connector,) = definition["components"]
    connector_part = part(definition, connector["part"])
    assert connector_part["name"].endswith("IPEX_20525_040E_02")
    mapping: dict[str, str | None] = {}
    for net in definition["nets"]:
        endpoints = [endpoint(item) for item in net["endpoints"]]
        ports = [pin for component, pin in endpoints if component == "port"]
        assert len(ports) == 1, net["name"]
        for component, pin in endpoints:
            if component == connector["ref"]:
                number = connector_part["pins"][pin]["number"]
                assert number not in mapping, number
                mapping[number] = ports[0]
    assert set(mapping) <= set(POSITIONS)
    return {position: mapping.get(position) for position in POSITIONS}


def _land_nets(source, refs) -> dict[tuple[str, str], list[str]]:
    """(flat connector reference, land number) -> nets, from the flat view."""
    components = flat_components(source)
    return {(ref, pin["number"]): pin["nets"] for ref in refs for pin in components[ref]["pin_list"]}


def _kind(port: str | None) -> tuple[str | None, str | None]:
    """Function class and polarity; data pairs are interchangeable lanes."""
    if port is None:
        return None, None
    if port.startswith("PAIR_"):
        return "DATA", port[-1]
    if port.startswith("CLK_"):
        return "CLOCK", port[-1]
    return port, None


@pytest.mark.parametrize(("module", "expected", "port_types"), [
    ("CSI2_DPHY_X4_SOURCE_PORT", SOURCE_PINOUT, SOURCE_PORT_TYPES),
    ("CSI2_DPHY_X4_SINK_PORT", SINK_PINOUT, SINK_PORT_TYPES),
])
def test_module_binds_the_pinout_exactly(module, expected, port_types):
    board = compile_board(_connector_only_board())
    assert _module_position_map(board, module) == expected
    assert _definition(board, module)["ports"] == port_types
    assert set(port_types) == {port for port in expected.values() if port is not None}


def test_flat_view_lands_every_position_on_the_parent_net():
    source = _connector_only_board()
    lands = _land_nets(source, ("J_OUT/J", "J_IN/J"))
    for ref, expected in (("J_OUT/J", SOURCE_PINOUT), ("J_IN/J", SINK_PINOUT)):
        actual = {}
        for position in POSITIONS:
            nets = lands.get((ref, position), [])
            assert len(nets) <= 1, (ref, position)
            actual[position] = nets[0] if nets else None
        assert actual == expected
    assert check(source) == []


@pytest.mark.parametrize("module", ["CSI2_DPHY_X4_SOURCE_PORT", "CSI2_DPHY_X4_SINK_PORT"])
def test_pairs_follow_package_edge_order_with_ground_between(module):
    mapping = _module_position_map(compile_board(_connector_only_board()), module)
    pairs = [mapping[str(n)] for n in range(13, 29)]
    assert pairs == ["GND", "PAIR_A_P", "PAIR_A_N", "GND", "PAIR_B_P", "PAIR_B_N", "GND",
                     "PAIR_C_P", "PAIR_C_N", "GND", "CLK_P", "CLK_N", "GND",
                     "PAIR_D_P", "PAIR_D_N", "GND"]


def test_straight_loopback_cable_keeps_lanes_and_isolates_dut_rails():
    board = compile_board(_connector_only_board())
    source = _module_position_map(board, "CSI2_DPHY_X4_SOURCE_PORT")
    sink = _module_position_map(board, "CSI2_DPHY_X4_SINK_PORT")
    for n in range(1, 41):
        near, far = source[str(n)], sink[str(n)]
        kind, _ = _kind(near)
        if kind in ("DATA", "CLOCK", "GND"):
            assert far == near, n  # same pair, same polarity, ground to ground
        else:  # DUT rails, I2C and reserved positions meet open sink contacts
            assert far is None, (n, near)


def test_sink_module_has_no_power_or_i2c_ports():
    with pytest.raises(CopperError, match="has no port 'VDUT_5V'"):
        compile_board(f'''
            board BadSink {{
                import csi2 "{HARNESS}";
                module J_IN: csi2.CSI2_DPHY_X4_SINK_PORT;
                net VDUT_5V {{ J_IN.VDUT_5V; }}
            }}
        ''')


def _two_port_board(dropped=frozenset()):
    def members(*items):
        return " ".join(f"{item};" for item in items if item not in dropped)
    source_nets = "\n".join(
        f"            net SRC_{pin} {{ {members(f'U_SRC.{pin}', f'J_OUT.{SOURCE_PINOUT[position]}')} }}"
        for position, pin in EXAMPLE_SOURCE_LANES.items())
    sink_nets = "\n".join(
        f"            net SNK_{pin} {{ {members(f'U_SNK.{pin}', f'J_IN.{SINK_PINOUT[position]}')} }}"
        for position, pin in EXAMPLE_SINK_LANES.items())
    return f'''
        board TwoPortLanes {{
            import csi2 "{HARNESS}";
            import adi92 "{LIB}/parts/adi/max96792a";
            import adi93 "{LIB}/parts/adi/max96793";
            module J_OUT: csi2.CSI2_DPHY_X4_SOURCE_PORT;
            module J_IN: csi2.CSI2_DPHY_X4_SINK_PORT;
            component U_SRC: adi92.MAX96792AGTM_VY;
            component U_SNK: adi93.MAX96793GTJ_VY;
            supply GND {{ voltage = 0V; external = true; }}
            supply V1V8 {{ voltage = 1.8V; external = true; }}
            supply V1V0 {{ voltage = 1.0V; external = true; }}
            supply V1V2 {{ voltage = 1.2V; external = true; }}
            supply VDUT_5V {{ voltage = 5V; external = true; }}
            supply DUT_VIO {{ voltage = 1.8V; external = true; }}
            net GND {{ U_SRC.EP; U_SNK.EP; J_OUT.GND; J_IN.GND; }}
            net V1V8 {{ U_SRC.VDD18_7; U_SRC.VDD18_16; U_SRC.VDDIO; U_SNK.VDD18; U_SNK.VDDIO; }}
            net V1V0 {{ U_SRC.VDD; U_SNK.VDD; }}
            net V1V2 {{ U_SRC.VTERM; }}
            net VDUT_5V {{ J_OUT.VDUT_5V; }}
            net DUT_VIO {{ J_OUT.DUT_VIO; }}
            net DUT_SDA {{ J_OUT.SDA; }}
            net DUT_SCL {{ J_OUT.SCL; }}
            net SRC_CAP_VDD {{ U_SRC.CAP_VDD; }}
            net SNK_CAP_VDD {{ U_SNK.CAP_VDD; }}
            net SRC_XRES {{ U_SRC.XRES; }}
            net SNK_XRES {{ U_SNK.XRES; }}
            net SRC_CFG0 {{ U_SRC.MFP2_CFG0; }}
            net SRC_CFG1 {{ U_SRC.MFP3_CFG1; }}
            net SNK_CFG0 {{ U_SNK.MFP1_CFG0; }}
            net SNK_CFG1 {{ U_SNK.MFP2_CFG1; }}
{source_nets}
{sink_nets}
        }}
    '''


def test_example_lane_assignment_through_the_modules_passes_erc():
    source = _two_port_board()
    assert check(source) == []
    components = flat_components(source)
    chips_on = {}
    for ref in ("U_SRC", "U_SNK"):
        for pin in components[ref]["pin_list"]:
            for net in pin["nets"]:
                chips_on.setdefault(net, set()).add(pin["pin"])
    chip_at_position: dict[tuple[str, str], str] = {}
    for (ref, position), nets in _land_nets(source, ("J_OUT/J", "J_IN/J")).items():
        for net in nets:
            if net in chips_on:
                (chip_at_position[(ref, position)],) = chips_on[net]
    # Lanes land on the documented chip pins; every ground land shares the chips' EP net.
    grounds = {position: "EP" for position, function in SOURCE_PINOUT.items() if function == "GND"}
    assert {position: pin for (ref, position), pin in chip_at_position.items()
            if ref == "J_OUT/J"} == {**EXAMPLE_SOURCE_LANES, **grounds}
    assert {position: pin for (ref, position), pin in chip_at_position.items()
            if ref == "J_IN/J"} == {**EXAMPLE_SINK_LANES, **grounds}


def test_half_connected_lane_through_the_module_is_reported():
    diagnostics = {(item["code"], item["subject"])
                   for item in check(_two_port_board(frozenset({"U_SRC.CKAN", "U_SNK.D0P"})))}
    assert ("INCOMPLETE_DIFFERENTIAL_PAIR", "U_SRC") in diagnostics
    assert ("INCOMPLETE_DIFFERENTIAL_PAIR", "U_SNK") in diagnostics
