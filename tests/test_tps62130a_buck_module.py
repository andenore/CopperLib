"""TPS62130A buck circuit module: a sourced rail with parent-set feedback."""

from pathlib import Path

from pcbir import check, compile_source

ROOT = Path(__file__).resolve().parents[1]


def _compile(tmp_path, body: str):
    (tmp_path / "copper.mod").write_text(
        "module buck-module-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n")
    return compile_source(body, str(tmp_path / "board.copper"), offline=True)


def test_buck_module_is_a_sourced_rail_with_parent_feedback(tmp_path):
    board = _compile(tmp_path, '''
        board BuckFixture {
            import buck "github.com/andenore/CopperLib/packages/circuits/ti/tps62130a-buck";
            import passives "github.com/andenore/CopperLib/packages/generic/passives";
            module B: buck.TPS62130A_BUCK_2U2;
            component R_TOP: passives.RESISTOR { value = 49.9kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }
            component R_BOT: passives.RESISTOR { value = 100kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }
            net VIN { B.VIN; B.EN; }
            net FB { B.FB; R_TOP.P2; R_BOT.P1; }
            net V1V2 { B.VOUT; R_TOP.P1; }
            net GND { B.GND; R_BOT.P2; }
            supply VIN { voltage = 5V; external = true; }
            supply V1V2 { voltage = 1.2V; source = B.VOUT; }
            supply GND { voltage = 0V; external = true; }
        }
    ''')
    assert check(board) == []
