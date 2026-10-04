from pathlib import Path

from pcbir import check, compile_source


ROOT = Path(__file__).resolve().parents[1]


def test_nrf_johanson_reference_circuit_is_reusable(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module rf-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n",
        encoding="utf-8",
    )
    board = compile_source(
        """board Radio {
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
        }""",
        str(tmp_path / "board.copper"),
        offline=True,
    )
    assert not check(board)
    assert "rf.Nrf52832JohansonRf" in board.module_definitions
