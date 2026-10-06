"""MAX96792A deserializer and MAX96793 serializer: pin numbers, footprint
coverage, device models (D-PHY lane pairs, D-PHY/C-PHY modes, CSI-2 absolute
voltage limits) and ERC.

Expected numbers below were transcribed independently from the data sheets'
Pin Configuration drawings (MAX96792A 19-101426 Rev 1 p.23, MAX96793
19-101163 Rev 3 p.24), lane pairs and C-PHY trio names from the Pin
Descriptions (MAX96792A pp.23-24, MAX96793 pp.24-25), PHY selection from
MAX96792A p.56 / MAX96793 p.59 and CSI-2 limits from Absolute Maximum Ratings
(p.10 of both), not copied from the part or device files.
"""
import json
import re
from pathlib import Path

import pytest

from pcbir import RelativeVoltage, check, compile_source, load_kicad_mod
from pcbir.modes import active_bonded_pads, active_device_pads, condition_active, effective_modes
from pcbir.serializer import board_to_dict

ROOT = Path(__file__).resolve().parents[1]
KICAD_FOOTPRINTS = Path("/usr/share/kicad/footprints")
MODULE = "github.com/andenore/CopperLib/packages/parts/adi"

PARTS = {
    "max96792a": ("MAX96792AGTM_VY", "TQFN-48-1EP_7x7mm_P0.5mm_EP5.1x5.1mm", 48),
    "max96793": ("MAX96793GTJ_VY", "QFN-32-1EP_5x5mm_P0.5mm_EP3.1x3.1mm", 32),
}

SPOT_CHECKS = {
    "max96792a": {
        "PWDNB": "1", "SIOBN": "5", "SIOBP": "6", "VDD18_7": "7", "X1_OSC": "12",
        "RSVD": "14", "XRES": "15", "VDD18_16": "16", "SIOAP": "17", "SIOAN": "18",
        "CAP_VDD": "19", "VDD": "20", "VTERM": "23", "VDDIO": "24",
        "DA0P": "31", "DA0N": "32", "CKAP": "33", "CKAN": "34", "DA3N": "30",
        "CKBP": "39", "CKBN": "40", "DB3P": "47", "DB3N": "48",
    },
    "max96793": {
        "PWDNB": "1", "MFP1_CFG0": "3", "MFP2_CFG1": "4", "VREF": "7", "X1_OSC": "8",
        "XRES": "10", "VDD18": "11", "SIOP": "12", "SION": "13", "CAP_VDD": "14",
        "VDD": "15", "VDDIO": "16", "D2P": "19", "D3N": "24", "D0P": "25",
        "CKP": "27", "CKN": "28", "D1N": "30", "MFP8": "32",
    },
}
EP_NUMBERS = {"max96792a": "49", "max96793": "33"}
DEVICES = {"max96792a": "MAX96792A", "max96793": "MAX96793"}

# group -> (noninverted, inverted) pin, D-PHY data lanes and clock lanes.
DPHY_PAIRS = {
    "max96792a": {
        "DA0": ("DA0P", "DA0N"), "DA1": ("DA1P", "DA1N"), "DA2": ("DA2P", "DA2N"),
        "DA3": ("DA3P", "DA3N"), "CKA": ("CKAP", "CKAN"),
        "DB0": ("DB0P", "DB0N"), "DB1": ("DB1P", "DB1N"), "DB2": ("DB2P", "DB2N"),
        "DB3": ("DB3P", "DB3N"), "CKB": ("CKBP", "CKBN"),
    },
    "max96793": {
        "D0": ("D0P", "D0N"), "D1": ("D1P", "D1N"), "D2": ("D2P", "D2N"),
        "D3": ("D3P", "D3N"), "CK": ("CKP", "CKN"),
    },
}
# PHY mode group of each D-PHY pair: MAX96792A "Each port can be configured to
# use either D-PHY v1.2 or C-PHY v1.0" (p.56); MAX96793 has one port (p.59).
# D-PHY is the power-up default ((*) markers in the Pin Descriptions).
PAIR_MODE_GROUP = {
    "max96792a": {
        "DA0": "PHY_A", "DA1": "PHY_A", "DA2": "PHY_A", "DA3": "PHY_A", "CKA": "PHY_A",
        "DB0": "PHY_B", "DB1": "PHY_B", "DB2": "PHY_B", "DB3": "PHY_B", "CKB": "PHY_B",
    },
    "max96793": {"D0": "PHY", "D1": "PHY", "D2": "PHY", "D3": "PHY", "CK": "PHY"},
}
DEFAULT_MODES = {"max96792a": {"PHY_A": "DPHY", "PHY_B": "DPHY"}, "max96793": {"PHY": "DPHY"}}
# Package pin -> C-PHY trio function (Pin Descriptions): MAX96792A port A pins
# carry C-PHY port D, port B pins port E; MAX96793 pins 25-30 carry lanes 0/1.
CPHY_TRIOS = {
    "max96792a": {
        "DA0P": "DD0A", "DA0N": "DD0B", "CKAP": "DD0C", "CKAN": "DD1A", "DA1P": "DD1B", "DA1N": "DD1C",
        "DB0P": "DE0A", "DB0N": "DE0B", "CKBP": "DE0C", "CKBN": "DE1A", "DB1P": "DE1B", "DB1N": "DE1C",
    },
    "max96793": {"D0P": "D0A", "D0N": "D0B", "CKP": "D0C", "CKN": "D1A", "D1P": "D1B", "D1N": "D1C"},
}
# Absolute Maximum Ratings p.10: MAX96792A "D-PHY, C-PHY Pins -0.3V to
# (VTERM + 0.1V)" with "Note b: VTERM <= +1.26V", i.e. at most 1.36 V; MAX96793
# "D_P/N, CKP/N -0.3V to +1.35V". Neither gives an operating pin range.
CSI2_ABSOLUTE = {"max96792a": (-0.3, ("VTERM", 0.1, 1.36)), "max96793": (-0.3, 1.35)}

# Supplies and pins that must be wired for a clean ERC of a single chip U1.
REQUIRED_NETS = {
    "max96792a": """
            supply GND { voltage = 0V; external = true; }
            supply V1V8 { voltage = 1.8V; external = true; }
            supply V1V0 { voltage = 1.0V; external = true; }
            supply V1V2 { voltage = 1.2V; external = true; }
            net GND { U1.EP; }
            net V1V8 { U1.VDD18_7; U1.VDD18_16; U1.VDDIO; }
            net V1V0 { U1.VDD; }
            net V1V2 { U1.VTERM; }
            net CAP_VDD { U1.CAP_VDD; }
            net XRES { U1.XRES; }
            net CFG0 { U1.MFP2_CFG0; }
            net CFG1 { U1.MFP3_CFG1; }""",
    "max96793": """
            supply GND { voltage = 0V; external = true; }
            supply V1V8 { voltage = 1.8V; external = true; }
            supply V1V0 { voltage = 1.0V; external = true; }
            net GND { U1.EP; }
            net V1V8 { U1.VDD18; U1.VDDIO; }
            net V1V0 { U1.VDD; }
            net CAP_VDD { U1.CAP_VDD; }
            net XRES { U1.XRES; }
            net CFG0 { U1.MFP1_CFG0; }
            net CFG1 { U1.MFP2_CFG1; }""",
}

_PAD = re.compile(r'\(pad "([^"]*)" (\w+) (\w+)(.*?)\(layers ([^)]*)\)', re.S)


def _footprint_path(name: str) -> Path:
    path = KICAD_FOOTPRINTS / "Package_DFN_QFN.pretty" / f"{name}.kicad_mod"
    if not path.is_file():
        pytest.skip(f"KiCad footprint library not installed: {path}")
    return path


def _raw_copper_pad_numbers(path: Path) -> set[str]:
    """Copper pad numbers straight from the S-expression text."""
    return {
        number
        for number, _kind, _shape, _body, layers in _PAD.findall(path.read_text(encoding="utf-8"))
        if number and ("F.Cu" in layers or "*.Cu" in layers)
    }


def _compile(tmp_path, body: str):
    (tmp_path / "copper.mod").write_text(
        "module gmsl-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    return compile_source(body, str(tmp_path / "gmsl.copper"), offline=True)


def _selection(modes: str) -> str:
    return f' {{ modes = "{modes}"; }}' if modes else ";"


def _board(tmp_path, package: str, modes: str = ""):
    name, _, _ = PARTS[package]
    return _compile(tmp_path, f'''
        board PartOnly {{
            import adi "{MODULE}/{package}";
            component U1: adi.{name}{_selection(modes)}
        }}
    ''')


def _part(tmp_path, package: str):
    name, _, _ = PARTS[package]
    return _board(tmp_path, package).library[f"adi.{name}"]


def _device(tmp_path, package: str):
    board = _board(tmp_path, package)
    part = board.library[f"adi.{PARTS[package][0]}"]
    assert part.device == f"adi.{DEVICES[package]}"
    return part, board.devices[part.device]


def _pin_profile(part, device, pin_name: str):
    """The electrical profile a package pin gets from its unconditionally bonded pad."""
    pin = part.pins[pin_name]
    assert pin.profile is None, f"{pin_name} must not shadow its device pad"
    (bond,) = pin.bonds
    assert bond.when is None
    return device.pads[bond.pad].profile


def _active_pads(board, package: str) -> dict[str, tuple[str, ...]]:
    """Package pin -> device pads active for U1 in its effective modes."""
    (component,) = board.components
    part = board.library[f"adi.{PARTS[package][0]}"]
    device = board.devices[part.device]
    active = {name: active_bonded_pads(component, pin, device) for name, pin in part.pins.items()}
    # Bond conditions and pad `when` conditions must agree on every pin.
    assert active == {name: tuple(pad.name for pad in active_device_pads(component, pin, device))
                      for name, pin in part.pins.items()}
    return active


def _lane_pins(package: str) -> list[str]:
    return [pin for pair in DPHY_PAIRS[package].values() for pin in pair]


def _chip_board(tmp_path, package: str, extra: str = "", modes: str = ""):
    name, _, _ = PARTS[package]
    return _compile(tmp_path, f'''
        board ChipFixture {{
            import adi "{MODULE}/{package}";
            component U1: adi.{name}{_selection(modes)}
{REQUIRED_NETS[package]}
{extra}
        }}
    ''')


@pytest.mark.parametrize("package", sorted(PARTS))
def test_pin_numbers_match_kicad_footprint_pads_exactly(tmp_path, package):
    name, footprint, terminals = PARTS[package]
    part = _part(tmp_path, package)
    numbers = [pin.number for pin in part.pins.values()]
    assert part.footprints == (f"Package_DFN_QFN:{footprint}",)
    assert len(numbers) == len(set(numbers)) == terminals + 1
    path = _footprint_path(footprint)
    raw = _raw_copper_pad_numbers(path)
    assert set(numbers) == raw == {str(n) for n in range(1, terminals + 2)}
    # CopperScript's importer must accept the footprint and agree.
    imported = load_kicad_mod(path).footprint
    assert {pad.number for pad in imported.pads if pad.number} == set(numbers)


@pytest.mark.parametrize("package", sorted(PARTS))
def test_independent_pin_spot_checks_and_evidence(tmp_path, package):
    name, footprint, _ = PARTS[package]
    part, device = _device(tmp_path, package)
    pins = {pin_name: pin.number for pin_name, pin in part.pins.items()}
    for pin_name, number in SPOT_CHECKS[package].items():
        assert pins[pin_name] == number, pin_name
    assert pins["EP"] == EP_NUMBERS[package]
    ep = part.pins["EP"]
    assert {domain.value for domain in _pin_profile(part, device, "EP").domains} == {"ground"}
    assert ep.connection_policy.value == "required"

    evidence = json.loads(
        (ROOT / f"packages/parts/adi/{package}/evidence/package-audit.json").read_text())
    assert evidence["part"] == name
    assert evidence["production_publishable"] is False
    assert evidence["pins"] == pins
    assert evidence["footprint"]["id"] == f"Package_DFN_QFN:{footprint}"
    assert evidence["footprint"]["exposed_pad_number"] == EP_NUMBERS[package]
    assert part.source.checksum == "sha256:" + evidence["source"]["sha256"]
    assert device.source.checksum == part.source.checksum
    assert device.source.revision == part.source.revision
    unresolved = {item["item"] for item in evidence["unresolved"]}
    assert {"exposed_pad_and_land_pattern", "cphy_lane2_lane3_function", "cphy_trio_grouping"} <= unresolved
    assert "cphy_mode_not_modeled" not in unresolved
    if package == "max96792a":
        assert {"datasheet_rev2_recheck", "vterm_relative_csi2_limit"} <= unresolved
        assert part.pins["RSVD"].connection_policy.value == "do_not_connect"
        assert part.pins["RSVD"].bonds == ()


def _limits(part, device, pin_name):
    voltage = _pin_profile(part, device, pin_name).voltage
    return float(voltage.minimum.base_value), float(voltage.maximum.base_value)


def test_supply_limits_follow_table_2(tmp_path):
    def limits(model, pin_name):
        return _limits(*model, pin_name)

    deser = _device(tmp_path, "max96792a")
    assert limits(deser, "VTERM") == pytest.approx((1.14, 1.26))
    assert limits(deser, "VDD18_7") == limits(deser, "VDD18_16") == pytest.approx((1.7, 1.9))
    assert limits(deser, "VDD") == pytest.approx((0.95, 1.26))
    assert limits(deser, "VDDIO") == pytest.approx((1.7, 3.6))
    ser = _device(tmp_path, "max96793")
    assert limits(ser, "VDD18") == pytest.approx((1.7, 1.9))
    assert limits(ser, "VDD") == pytest.approx((0.95, 1.26))
    assert limits(ser, "VDDIO") == pytest.approx((1.7, 3.6))


def test_minimal_serializer_to_deserializer_board_passes_erc(tmp_path):
    board = _compile(tmp_path, f'''
        board GmslAudit {{
            import adi92 "{MODULE}/max96792a";
            import adi93 "{MODULE}/max96793";
            component U1: adi92.MAX96792AGTM_VY;
            component U2: adi93.MAX96793GTJ_VY;
            supply GND {{ voltage = 0V; external = true; }}
            supply V1V8 {{ voltage = 1.8V; external = true; }}
            supply V1V0 {{ voltage = 1.0V; external = true; }}
            supply V1V2 {{ voltage = 1.2V; external = true; }}
            net GND {{ U1.EP; U2.EP; }}
            net V1V8 {{ U1.VDD18_7; U1.VDD18_16; U1.VDDIO; U2.VDD18; U2.VDDIO; }}
            net V1V0 {{ U1.VDD; U2.VDD; }}
            net V1V2 {{ U1.VTERM; }}
            net U1_CAP_VDD {{ U1.CAP_VDD; }}
            net U2_CAP_VDD {{ U2.CAP_VDD; }}
            net U1_XRES {{ U1.XRES; }}
            net U2_XRES {{ U2.XRES; }}
            net U1_CFG0 {{ U1.MFP2_CFG0; }}
            net U1_CFG1 {{ U1.MFP3_CFG1; }}
            net U2_CFG0 {{ U2.MFP1_CFG0; }}
            net U2_CFG1 {{ U2.MFP2_CFG1; }}
            net CSI_CK_P {{ U1.CKAP; U2.CKP; }}
            net CSI_CK_N {{ U1.CKAN; U2.CKN; }}
            net CSI_D0_P {{ U1.DA0P; U2.D0P; }}
            net CSI_D0_N {{ U1.DA0N; U2.D0N; }}
        }}
    ''')
    assert check(board) == []


def test_reserved_and_required_pins_are_enforced(tmp_path):
    board = _compile(tmp_path, f'''
        board GmslMisuse {{
            import adi92 "{MODULE}/max96792a";
            component U1: adi92.MAX96792AGTM_VY;
            supply GND {{ voltage = 0V; external = true; }}
            supply V1V8 {{ voltage = 1.8V; external = true; }}
            net GND {{ U1.EP; U1.RSVD; }}
            net V1V8 {{ U1.VDD18_7; U1.VDD18_16; U1.VDDIO; U1.VTERM; U1.VDD; }}
        }}
    ''')
    codes = {(item.code, item.subject) for item in check(board)}
    assert ("DO_NOT_CONNECT", "U1.RSVD") in codes
    assert ("REQUIRED_PIN_UNCONNECTED", "U1.XRES") in codes
    assert ("SUPPLY_VOLTAGE_HIGH", "U1.VTERM") in codes


@pytest.mark.parametrize("package", sorted(PARTS))
def test_parts_bond_every_pin_to_its_own_device_pad(tmp_path, package):
    part, device = _device(tmp_path, package)
    lane_pins = set(_lane_pins(package))
    pin_group = {pin: PAIR_MODE_GROUP[package][group]
                 for group, pair in DPHY_PAIRS[package].items() for pin in pair}
    bonded = []
    for pin_name, pin in part.pins.items():
        if pin.connection_policy.value == "do_not_connect":
            assert pin.bonds == () and pin.profile is None
            continue
        if pin_name not in lane_pins:
            _pin_profile(part, device, pin_name)  # one unconditional bond, no shadowing profile
            assert pin.bonds[0].pad == pin_name
            bonded.append(pin_name)
            continue
        # CSI-2 pin: its own D-PHY pad in D-PHY mode, its C-PHY trio pad (if the
        # data sheet names one) in C-PHY mode, nothing else.
        assert pin.profile is None, pin_name
        group = pin_group[pin_name]
        expected = [(pin_name, {group: "DPHY"})]
        if pin_name in CPHY_TRIOS[package]:
            expected.append((CPHY_TRIOS[package][pin_name], {group: "CPHY"}))
        assert [(bond.pad, dict(bond.when.selections)) for bond in pin.bonds] == expected, pin_name
        bonded.extend(pad for pad, _ in expected)
    # Every pad is bonded exactly once: no pad is shared, so no internal connection is implied.
    assert len(bonded) == len(set(bonded))
    assert set(device.pads) == set(bonded)


@pytest.mark.parametrize("package", sorted(PARTS))
def test_every_dphy_lane_is_a_differential_pair_group(tmp_path, package):
    part, device = _device(tmp_path, package)
    pairs = DPHY_PAIRS[package]
    assert {name: (group.members["positive"], group.members["negative"])
            for name, group in device.signal_groups.items()} == pairs
    assert all(group.kind == "differential_pair" for group in device.signal_groups.values())
    # The pairs are D-PHY lanes: active only with their port in D-PHY mode.
    assert {name: dict(group.when.selections) for name, group in device.signal_groups.items()} == {
        name: {PAIR_MODE_GROUP[package][name]: "DPHY"} for name in pairs}
    positives = {positive for positive, _ in pairs.values()}
    negatives = {negative for _, negative in pairs.values()}
    pad_mode = {pin: {PAIR_MODE_GROUP[package][group]: "DPHY"}
                for group, pair in pairs.items() for pin in pair}
    pad_mode.update({pad: {PAIR_MODE_GROUP[package][group]: "CPHY"}
                     for group, pair in pairs.items() for pin in pair
                     for pad in [CPHY_TRIOS[package].get(pin)] if pad})
    for name, pad in device.pads.items():
        traits = set(pad.profile.traits) & {"differential_positive", "differential_negative"}
        expected = ({"differential_positive"} if name in positives
                    else {"differential_negative"} if name in negatives else set())
        assert traits == expected, name
        assert (dict(pad.when.selections) if pad.when else None) == pad_mode.get(name), name
    for pin_name in positives | negatives:
        # "Leave (pins) open if unused" (Pin Descriptions).
        assert part.pins[pin_name].connection_policy.value == "optional", pin_name


@pytest.mark.parametrize("package", sorted(PARTS))
def test_default_mode_keeps_dphy_bonding_and_pairs_without_a_modes_selection(tmp_path, package):
    board = _board(tmp_path, package)
    (component,) = board.components
    part = board.library[f"adi.{PARTS[package][0]}"]
    device = board.devices[part.device]
    assert component.modes == {}
    assert {name: (group.choices, group.default) for name, group in device.mode_groups.items()} == {
        name: (("DPHY", "CPHY"), "DPHY") for name in DEFAULT_MODES[package]}
    modes = effective_modes(component, device)
    assert dict(modes) == DEFAULT_MODES[package]
    active = _active_pads(board, package)
    # Exactly today's D-PHY bonding: every connectable pin on the pad of its own name.
    assert active == {name: (name,) for name, pin in part.pins.items() if pin.bonds} | {
        name: () for name, pin in part.pins.items() if not pin.bonds}
    assert all(condition_active(group.when, modes) for group in device.signal_groups.values())


@pytest.mark.parametrize(("package", "mode_group"),
                         [(package, group) for package in sorted(PARTS) for group in DEFAULT_MODES[package]])
def test_cphy_selection_bonds_trio_pads_and_deactivates_dphy_pairs(tmp_path, package, mode_group):
    board = _board(tmp_path, package, f"{mode_group}=CPHY")
    (component,) = board.components
    device = board.devices[board.library[f"adi.{PARTS[package][0]}"].device]
    active = _active_pads(board, package)
    port_pins = {pin for group, pair in DPHY_PAIRS[package].items()
                 if PAIR_MODE_GROUP[package][group] == mode_group for pin in pair}
    for pin_name in _lane_pins(package):
        if pin_name not in port_pins:
            assert active[pin_name] == (pin_name,), pin_name  # the other port stays D-PHY
        elif pin_name in CPHY_TRIOS[package]:
            assert active[pin_name] == (CPHY_TRIOS[package][pin_name],), pin_name
        else:
            assert active[pin_name] == (), pin_name  # lane 2/3: no C-PHY function
    modes = effective_modes(component, device)
    assert {name for name, group in device.signal_groups.items() if not condition_active(group.when, modes)} == {
        name for name, group in PAIR_MODE_GROUP[package].items() if group == mode_group}

    trio_pins = [pin for pin in CPHY_TRIOS[package] if pin in port_pins]
    lane_two_three = sorted(port_pins - set(CPHY_TRIOS[package]))
    # One wire of a trio is half of a D-PHY pair, but the pairs are inactive in C-PHY mode.
    single = _chip_board(tmp_path, package, f"            net TRIO {{ U1.{trio_pins[0]}; }}",
                         modes=f"{mode_group}=CPHY")
    assert check(single) == []
    every = "\n".join(f"            net T_{pin} {{ U1.{pin}; }}" for pin in trio_pins)
    assert check(_chip_board(tmp_path, package, every, modes=f"{mode_group}=CPHY")) == []
    unmodeled = _chip_board(tmp_path, package, f"            net L23 {{ U1.{lane_two_three[0]}; }}",
                            modes=f"{mode_group}=CPHY")
    assert [(item.code, item.subject) for item in check(unmodeled)] == [
        ("UNMODELED_PIN", f"U1.{lane_two_three[0]}")]


def _absolute(profile):
    absolute = profile.absolute_voltage
    assert absolute is not None and absolute.rating == "absolute"
    maximum = absolute.maximum
    if isinstance(maximum, RelativeVoltage):
        maximum = (maximum.reference, float(maximum.offset.base_value), float(maximum.limit.base_value))
    else:
        maximum = float(maximum.base_value)
    return float(absolute.minimum.base_value), maximum


@pytest.mark.parametrize("package", sorted(PARTS))
def test_csi2_pins_carry_absolute_maximum_limits(tmp_path, package):
    part, device = _device(tmp_path, package)
    csi2_pads = _lane_pins(package) + list(CPHY_TRIOS[package].values())
    for pad_name in csi2_pads:
        profile = device.pads[pad_name].profile
        assert _absolute(profile) == CSI2_ABSOLUTE[package], pad_name
        assert profile.voltage is None, pad_name  # no operating range is given
    evidence = json.loads(
        (ROOT / f"packages/parts/adi/{package}/evidence/package-audit.json").read_text())
    model = evidence["device_model"]
    assert model["device"] == DEVICES[package]
    assert model["csi2_pin_voltage_rating"] == "absolute_maximum"
    assert model["csi2_pin_operating_v"] is None
    assert {name: tuple(pair) for name, pair in model["differential_pairs"].items()} == DPHY_PAIRS[package]
    assert model["cphy_modeled"] is True
    assert model["cphy_alternates"] == CPHY_TRIOS[package]
    assert {name: (tuple(group["choices"]), group["default"]) for name, group in model["mode_groups"].items()} == {
        name: (("DPHY", "CPHY"), "DPHY") for name in DEFAULT_MODES[package]}
    assert set(model["dphy_only_pins"]) == set(_lane_pins(package)) - set(CPHY_TRIOS[package])


@pytest.mark.parametrize("package", sorted(PARTS))
def test_absolute_limits_lower_to_absolute_voltage_in_the_ir(tmp_path, package):
    document = board_to_dict(_board(tmp_path, package))
    (device,) = [item for item in document["devices"] if item["name"] == f"adi.{DEVICES[package]}"]
    pads = {pad["name"]: pad for pad in device["pads"]}
    minimum, maximum = CSI2_ABSOLUTE[package]
    for pad_name in _lane_pins(package) + list(CPHY_TRIOS[package].values()):
        profile = pads[pad_name]["profile"]
        assert profile["voltage"] is None, pad_name
        absolute = profile["absolute_voltage"]
        assert absolute["rating"] == "absolute", pad_name
        assert float(absolute["minimum"]["base_value"]) == pytest.approx(minimum), pad_name
        if isinstance(maximum, tuple):
            reference, offset, cap = maximum
            assert absolute["maximum"]["reference"] == reference, pad_name
            assert float(absolute["maximum"]["offset"]["base_value"]) == pytest.approx(offset)
            assert float(absolute["maximum"]["limit"]["base_value"]) == pytest.approx(cap)
        else:
            assert float(absolute["maximum"]["base_value"]) == pytest.approx(maximum), pad_name
    # Supplies keep their operating-only Table 2 ranges.
    assert "absolute_voltage" not in pads["VDD"]["profile"]
    assert {mode["name"]: mode["default"] for mode in device["mode_groups"]} == DEFAULT_MODES[package]


@pytest.mark.parametrize("package", sorted(PARTS))
def test_fully_connected_lanes_pass_erc(tmp_path, package):
    nets = "\n".join(f"            net {pin} {{ U1.{pin}; }}"
                     for pair in DPHY_PAIRS[package].values() for pin in pair)
    assert check(_chip_board(tmp_path, package, nets)) == []


@pytest.mark.parametrize(("package", "group"),
                         [(package, group) for package in sorted(PARTS) for group in DPHY_PAIRS[package]])
def test_half_connected_lane_is_an_erc_error(tmp_path, package, group):
    for connected in DPHY_PAIRS[package][group]:
        board = _chip_board(tmp_path, package, f"            net HALF {{ U1.{connected}; }}")
        diagnostics = check(board)
        assert [(item.code, item.subject) for item in diagnostics] == [
            ("INCOMPLETE_DIFFERENTIAL_PAIR", "U1")], connected
        assert f"group {group} " in diagnostics[0].message


# REQUIRED_NETS puts the MAX96792A VTERM on 1.2 V, so its CSI-2 absolute
# maximum resolves to min(1.2 V + 0.1 V, 1.36 V) = 1.3 V.
@pytest.mark.parametrize(("package", "voltage", "code"), [
    ("max96792a", "1.8V", "SUPPLY_VOLTAGE_ABSOLUTE_HIGH"),
    ("max96792a", "1.36V", "SUPPLY_VOLTAGE_ABSOLUTE_HIGH"),
    ("max96792a", "1.3V", None),
    ("max96792a", "-0.31V", "SUPPLY_VOLTAGE_ABSOLUTE_LOW"),
    ("max96793", "1.8V", "SUPPLY_VOLTAGE_ABSOLUTE_HIGH"),
    ("max96793", "1.36V", "SUPPLY_VOLTAGE_ABSOLUTE_HIGH"),
    ("max96793", "1.35V", None),
    ("max96793", "-0.3V", None),
    ("max96793", "-0.31V", "SUPPLY_VOLTAGE_ABSOLUTE_LOW"),
])
def test_csi2_pin_on_a_supply_rail_is_voltage_checked(tmp_path, package, voltage, code):
    lane_pins = _lane_pins(package)
    rails = "\n".join(
        f"            supply R_{pin} {{ voltage = {voltage}; external = true; }}\n"
        f"            net R_{pin} {{ U1.{pin}; }}" for pin in lane_pins)
    diagnostics = check(_chip_board(tmp_path, package, rails))
    codes = {(item.code, item.subject) for item in diagnostics}
    assert codes == ({(code, f"U1.{pin}") for pin in lane_pins} if code else set())
    assert all(item.severity.value == "error" for item in diagnostics)


@pytest.mark.parametrize(("package", "voltage"), [("max96792a", "1.31V"), ("max96793", "1.36V")])
def test_cphy_trio_pins_keep_the_absolute_maximum(tmp_path, package, voltage):
    trio_pins = list(CPHY_TRIOS[package])
    rails = "\n".join(
        f"            supply R_{pin} {{ voltage = {voltage}; external = true; }}\n"
        f"            net R_{pin} {{ U1.{pin}; }}" for pin in trio_pins)
    modes = ",".join(f"{group}=CPHY" for group in DEFAULT_MODES[package])
    codes = {(item.code, item.subject) for item in check(_chip_board(tmp_path, package, rails, modes=modes))}
    assert codes == {("SUPPLY_VOLTAGE_ABSOLUTE_HIGH", f"U1.{pin}") for pin in trio_pins}


def test_deserializer_csi2_limit_needs_vterm_on_a_declared_supply(tmp_path):
    def board(voltage):
        return _compile(tmp_path, f'''
            board VtermFloating {{
                import adi "{MODULE}/max96792a";
                component U1: adi.MAX96792AGTM_VY;
                supply R {{ voltage = {voltage}; external = true; }}
                net VTERM_FLOAT {{ U1.VTERM; }}
                net R {{ U1.DA0P; }}
            }}
        ''')

    def limit_codes(voltage):
        return {(item.code, item.subject) for item in check(board(voltage))
                if item.code.startswith(("VOLTAGE_LIMIT", "SUPPLY_VOLTAGE"))}

    # Without a VTERM supply only the 1.36 V cap of "VTERM+0.1V, 1.36V" applies.
    assert limit_codes("1.2V") == {("VOLTAGE_LIMIT_UNRESOLVED", "U1.DA0P")}
    assert limit_codes("1.4V") == {("VOLTAGE_LIMIT_UNRESOLVED", "U1.DA0P"),
                                   ("SUPPLY_VOLTAGE_ABSOLUTE_HIGH", "U1.DA0P")}
