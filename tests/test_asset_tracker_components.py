"""Migration contracts; these do not qualify RF, power or assembly behavior."""
import hashlib
from pathlib import Path

import pytest
from pcbir import compile_source
from pcbir.importers import load_kicad_mod
from pcbir.model import Direction

ROOT = Path(__file__).resolve().parents[1]
LIB = "github.com/andenore/CopperLib/packages"
EXPORTS = {
    "simcom": ("parts/simcom/sim7670g-lngv", ("SIM7670G_LNGV",)),
    "buck": ("parts/ti/tps63020", ("TPS63020DSJR",)),
    "bourns": ("parts/bourns/srp4020ta", ("SRP4020TA_1R5M",)),
    "jst": ("parts/jst/xh-sm4", ("JST_S3B_XH_SM4_TB",)),
    "level": ("parts/ti/sn74axc2t245", ("MODEM_UART_TRANSLATOR", "MODEM_STATUS_TRANSLATOR")),
    "fet": ("parts/onsemi/bss138", ("BSS138",)),
    "can": ("parts/ti/tcan334g", ("TCAN334GDR",)),
    "yxc": ("parts/yxc/ysx321sl", ("YXC_X322532MOB4SI",)),
    "button": ("parts/e-switch/tl3342", ("TL3342F160QG",)),
    "coax": ("parts/hirose/u-fl", ("U_FL_R_SMT_1",)),
    "can_header": ("interfaces/can/jst-xh3", ("CAN_HEADER",)),
    "uart_header": ("interfaces/uart/jst-xh4", ("DEBUG_HEADER",)),
}


@pytest.fixture(scope="module")
def board(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("extracted-components")
    (tmp / "copper.mod").write_text(
        "module extracted-components-test\n"
        "require github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n",
        encoding="utf-8")
    lines = ["board ExtractedComponents {"]
    for alias, (path, names) in EXPORTS.items():
        lines.append(f'import {alias} "{LIB}/{path}";')
        for i, name in enumerate(names):
            lines.append(f"component {alias.upper()}_{i}: {alias}.{name};")
    return compile_source("\n".join([*lines, "}"]), str(tmp / "board.copper"), offline=True)


def test_all_thirteen_exports_are_importable_with_provenance(board):
    assert len(board.components) == 13
    for alias, (_, names) in EXPORTS.items():
        for name in names:
            part = board.library[f"{alias}.{name}"]
            assert part.manufacturer and part.source and part.source.url
            assert part.footprints
            assert all("Tracker.pretty" not in f for f in part.footprints)


FOOTPRINTS = (
    ("parts/simcom/sim7670g-lngv/footprints/SIM7670G_LNGV.kicad_mod",
     {str(i) for i in range(1, 125)}, "59eb98f893d42b0fb78bad148e065ad7d4b3b4ae94fb2a8a547b04f2ba597823"),
    ("parts/ti/tps63020/footprints/TI_DSJ0014_TPS63020.kicad_mod",
     {str(i) for i in range(1, 16)}, "9653d152a188e181c08251c6da1d92f2ada12dcbbd70155c282573f3d7d9a8b7"),
    ("parts/bourns/srp4020ta/footprints/Bourns_SRP4020TA.kicad_mod",
     {"1", "2"}, "7e935df9b692778b3917f1a5af0c7e239f542ddad6f37b13a5b6a94731603cb8"),
    ("parts/jst/xh-sm4/footprints/JST_S3B_XH_SM4_TB.kicad_mod",
     {"1", "2", "3", "MP"}, "4e6035ec9b976bee0fd8117af3731dd427a3e945e104dab6418da488c203bc4c"),
    ("parts/jst/xh-sm4/footprints/JST_S4B_XH_SM4_TB.kicad_mod",
     {"1", "2", "3", "4", "MP"}, "4ae72bcb69bd23c7b925bc41b22672673e7daf6b3f40b4bfbce2245656cb7d83"),
)


@pytest.mark.parametrize("path,numbers,digest", FOOTPRINTS)
def test_moved_footprint_identity_and_land_coverage(path, numbers, digest):
    path = ROOT / "packages" / path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    footprint = load_kicad_mod(path).footprint
    assert {pad.number for pad in footprint.pads if pad.number} == numbers


def test_contextual_jst_interfaces_share_package_owned_land_patterns(board):
    battery = board.library["jst.JST_S3B_XH_SM4_TB"].footprints
    assert board.library["can_header.CAN_HEADER"].footprints == battery
    assert "parts/jst/xh-sm4/footprints/JST_S4B_XH_SM4_TB.kicad_mod" in (
        board.library["uart_header.DEBUG_HEADER"].footprints[0])


def test_modem_orientation_marker_does_not_overlay_pin_one():
    path = ROOT / "packages/parts/simcom/sim7670g-lngv/footprints/SIM7670G_LNGV.kicad_mod"
    assert '(center -10.5 -8)' in path.read_text()
    pad = next(p for p in load_kicad_mod(path).footprint.pads if p.number == "1")
    # Circle outer edge clears even the pad's rectangular envelope by >0.2 mm.
    pad_right = pad.position.x_nm + pad.size.width_nm // 2
    assert -10500000 - 260000 - pad_right > 200000


def test_configured_translation_and_existing_family_variants_remain_distinct(board):
    uart = board.library["level.MODEM_UART_TRANSLATOR"]
    status = board.library["level.MODEM_STATUS_TRANSLATOR"]
    assert uart.footprints == status.footprints
    assert {p.number for p in uart.pins.values()} == {str(i) for i in range(1, 11)}
    assert uart.pins["A_TX"].number == status.pins["A_STATUS"].number == "8"
    assert Direction.INPUT in uart.pins["A_TX"].profile.directions
    assert Direction.OUTPUT in status.pins["A_STATUS"].profile.directions
    assert "SOIC-8" in board.library["can.TCAN334GDR"].footprints[0]
    assert "VSSOP-8" in board.library["can.TCAN334G"].footprints[0]
    assert "yxc.YXC_X322525MOB4SI" in board.library
    assert "yxc.YXC_X322532MOB4SI" in board.library
