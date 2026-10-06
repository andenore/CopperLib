"""I-PEX CABLINE-CA receptacle 20525-040E-02: land pattern, pin 1 and ground lands.

Expected geometry was transcribed independently from I-PEX drawing 20525 rev 34,
sheet 5/7 (recommended footprint pattern, 40P row: A=17.40, B=15.60, E=12.00,
G=20.18, H=21.60, J=23.60, K=2.40), not copied from the footprint file.
"""
import json
from pathlib import Path

from pcbir import FootprintResolver, audit_resolved_footprints, check, compile_source, load_kicad_mod

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/parts/i-pex/20525-040e-02"
FOOTPRINT = PACKAGE / "footprints/Connector_I-PEX.pretty/I-PEX_20525-040E-02.kicad_mod"
EVIDENCE = PACKAGE / "evidence/footprint-audit.json"
IMPORT = "github.com/andenore/CopperLib/packages/parts/i-pex/20525-040e-02"
NM = 1_000_000
SIGNALS = {str(n) for n in range(1, 41)}


def _pads():
    return load_kicad_mod(FOOTPRINT, strict=True).footprint.pads


def _size(pad):
    return pad.size.width_nm, pad.size.height_nm


def test_land_pattern_matches_sheet5_40p_row():
    pads = _pads()
    signal = {pad.number: pad for pad in pads if pad.number in SIGNALS}
    shield = [pad for pad in pads if pad.number == "SH"]

    assert {pad.number for pad in pads} == SIGNALS | {"SH"}
    assert len(signal) == 40 and len(pads) == 52
    assert all(pad.has_solder_mask and pad.has_solder_paste for pad in pads)
    # Pin 1 at the datum-mark end: left in top view with the signal row toward -Y.
    assert signal["1"].position.x_nm == -7_800_000
    assert signal["40"].position.x_nm == 7_800_000
    for n in range(1, 40):
        assert signal[str(n + 1)].position.x_nm - signal[str(n)].position.x_nm == 400_000
    assert {_size(pad) for pad in signal.values()} == {(200_000, 800_000)}
    signal_top = {pad.position.y_nm - pad.size.height_nm // 2 for pad in signal.values()}
    assert len(signal_top) == 1
    top = signal_top.pop()

    # 12 non-signal lands: 2 end tails, E/K+1 = 6 ground contacts, 4 shell tabs.
    assert len(shield) == 12
    by_size = {}
    for pad in shield:
        by_size.setdefault(_size(pad), []).append(pad)
    assert {size: len(group) for size, group in by_size.items()} == {
        (550_000, 900_000): 2, (550_000, 550_000): 6, (710_000, 1_300_000): 2, (710_000, 1_850_000): 2,
    }
    ends = by_size[(550_000, 900_000)]
    assert sorted(pad.position.x_nm for pad in ends) == [-8_700_000, 8_700_000]  # A = 17.40
    assert {pad.position.y_nm - 450_000 for pad in ends} == {top}
    grounds = by_size[(550_000, 550_000)]
    assert sorted(pad.position.x_nm for pad in grounds) == [
        -6_000_000, -3_600_000, -1_200_000, 1_200_000, 3_600_000, 6_000_000]
    assert {pad.position.y_nm - 275_000 for pad in grounds} == {top + 800_000 + 250_000}
    for size, top_offset in (((710_000, 1_300_000), 550_000), ((710_000, 1_850_000), 2_600_000)):
        tabs = by_size[size]
        assert sorted(pad.position.x_nm for pad in tabs) == [-10_445_000, 10_445_000]  # G/H edges
        assert {pad.position.y_nm - size[1] // 2 for pad in tabs} == {top + top_offset}
    # Origin: centre of the copper extents.
    assert top == -2_225_000
    assert max(pad.position.y_nm + pad.size.height_nm // 2 for pad in pads) == 2_225_000


def test_courtyard_is_note1_area_and_cable_exits_away_from_signal_row():
    footprint = load_kicad_mod(FOOTPRINT, strict=True).footprint
    xs = [point.x_nm for point in footprint.courtyard]
    ys = [point.y_nm for point in footprint.courtyard]
    assert (min(xs), max(xs)) == (-11_800_000, 11_800_000)  # J = 23.60
    assert min(ys) == -2_225_000 + 2_600_000 - 3_420_000  # 3.42 MIN. above lower shell pads
    assert max(ys) == 2_225_000 + 1_500_000

    evidence = json.loads(EVIDENCE.read_text())
    assert evidence["production_publishable"] is False
    assert evidence["cable_exit_side"]["footprint_direction"] == "+Y"
    signal_y = {pad.position.y_nm for pad in footprint.pads if pad.number in SIGNALS}
    assert max(signal_y) < min(pad.position.y_nm for pad in footprint.pads if pad.number == "SH"
                               and pad.size.width_nm == 550_000 and pad.size.height_nm == 550_000)
    assert "41-n" in evidence["harness_pin_mapping"]["fact"]
    assert evidence["unresolved"]


def test_part_maps_every_land_and_compiles(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module ipex-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    nets = "\n".join(f"            net S{n} {{ J1.P{n}; J2.P{41 - n}; }}" for n in range(1, 41))
    board = compile_source(f'''
        board CablineCaFixture {{
            import ipex "{IMPORT}";
            component J1: ipex.IPEX_20525_040E_02;
            component J2: ipex.IPEX_20525_040E_02;
{nets}
            net GND {{ J1.SHIELD; J2.SHIELD; }}
        }}
    ''', str(tmp_path / "board.copper"), offline=True)
    part = board.library["ipex.IPEX_20525_040E_02"]
    pins = {name: pin.number for name, pin in part.pins.items()}
    assert pins == {**{f"P{n}": str(n) for n in range(1, 41)}, "SHIELD": "SH"}
    profiles = {name: ({d.value for d in pin.profile.domains}, {d.value for d in pin.profile.directions})
                for name, pin in part.pins.items()}
    assert profiles.pop("SHIELD") == ({"ground"}, {"passive"})
    assert all(profile == ({"analog", "digital"}, {"passive"}) for profile in profiles.values())
    assert part.internal_pad_groups == ()
    evidence = json.loads(EVIDENCE.read_text())
    assert pins == evidence["semantic_pins"]
    assert part.source.checksum == "sha256:" + evidence["sources"][0]["sha256"]
    assert part.source.revision == "20525 rev 34"
    assert check(board) == []
    audit = audit_resolved_footprints(
        board, FootprintResolver(base_directory=tmp_path, strict=True, offline=True))
    assert audit.passed, [entry.errors for entry in audit.entries]
