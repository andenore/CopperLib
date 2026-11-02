"""Kingbright APTD1608 chip LEDs: polarity, sources and the package footprint."""
import json
import re
from pathlib import Path

import pytest
from copper_cli import audit_footprints, check, compile_board, part, pins

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/parts/kingbright/aptd1608"
LIB = "github.com/andenore/CopperLib/packages"
LEDS = (
    "KINGBRIGHT_APTD1608LSURCK",
    "KINGBRIGHT_APTD1608LSYCK",
    "KINGBRIGHT_APTD1608LZGCK",
    "KINGBRIGHT_APTD1608LVBC_D",
)

SOURCE = f'''board KingbrightFixture {{
    import passives "{LIB}/generic/passives";
    import kingbright "{LIB}/parts/kingbright/aptd1608";
{"".join(f"    component D{i}: kingbright.{name};{chr(10)}" for i, name in enumerate(LEDS))}    component R1: passives.RESISTOR {{ value = 470ohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }}
    supply V3V3 {{ voltage = 3.3V; external = true; }}
    supply GND {{ voltage = 0V; external = true; }}
    net V3V3 {{ R1.P1; }}
    net LED_A {{ R1.P2; {" ".join(f"D{i}.A;" for i in range(len(LEDS)))} }}
    net GND {{ {" ".join(f"D{i}.K;" for i in range(len(LEDS)))} }}
}}'''


@pytest.fixture(scope="module")
def board():
    return compile_board(SOURCE)


def _audit():
    return json.loads((PACKAGE / "evidence/aptd1608-audit.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", LEDS)
def test_cathode_is_terminal_1_with_sources_pinned(board, name):
    record = _audit()
    assert record["polarity"]["1"].startswith("cathode") and record["polarity"]["2"].startswith("anode")
    assert pins(board, f"kingbright.{name}") == {"K": "1", "A": "2"}
    definition = part(board, f"kingbright.{name}")
    assert definition["source"]["checksum"] == "sha256:" + record["parts"][name]["sha256"]
    assert definition["source"]["url"] == record["parts"][name]["url"]
    (footprint,) = definition["footprints"]
    assert footprint.endswith(record["footprint"])


def test_footprint_is_the_recommended_soldering_pattern():
    text = (PACKAGE / "footprints/Kingbright_APTD1608.kicad_mod").read_text()
    pads = {number: (float(x), float(w), float(h)) for number, x, w, h in
            re.findall(r'\(pad "(\d)" smd rect \(at (\S+) 0\) \(size (\S+) (\S+)\)', text)}
    assert pads == {"1": (-0.825, 0.8, 0.8), "2": (0.825, 0.8, 0.8)}  # 0.8 x 0.8 lands, 0.85 apart
    (entry,) = [e for e in audit_footprints(SOURCE)["entries"] if e["reference"].endswith("Kingbright_APTD1608.kicad_mod")]
    assert entry["passed"], entry["errors"]


def test_fixture_passes_erc():
    assert check(SOURCE) == []
