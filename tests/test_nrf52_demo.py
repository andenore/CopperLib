from pathlib import Path

from pcbir import check, compile_source

ROOT = Path(__file__).resolve().parents[1]


def test_demo_support_part_contracts(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module demo-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n", encoding="utf-8")
    board = compile_source('''board SupportContract {
        import demo "github.com/andenore/CopperLib/packages/nrf52_demo";
        component BT: demo.KEYSTONE_3034;
        component X: demo.REFERENCE_XTAL_2016;
        component D: demo.REFERENCE_LED_0603;
        net V { BT.POS; }
        net GND { BT.NEG; X.CASE_2; X.CASE_4; D.K; }
        supply GND { voltage = 0V; external = true; }
    }''', str(tmp_path / "board.copper"), offline=True)
    assert check(board) == []
    def pins(name):
        return {p.name: p.number for p in board.library["demo." + name].pins.values()}
    assert pins("KEYSTONE_3034") == {"POS": "1", "NEG": "2"}
    assert tuple(g.numbers for g in board.library["demo.KEYSTONE_3034"].internal_pad_groups) == (("1",),)
    assert pins("REFERENCE_XTAL_2016") == {"X1": "1", "X2": "3", "CASE_2": "2", "CASE_4": "4"}
    assert pins("REFERENCE_LED_0603") == {"K": "1", "A": "2"}


def test_button_internal_groups_do_not_short_signal_to_ground(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module switch-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n", encoding="utf-8")
    board = compile_source('''board SwitchContract {
        import v "github.com/andenore/CopperLib/packages/full_vertical";
        component S: v.BUTTON;
        net BUTTON { S.A; }
        net GND { S.B; }
    }''', str(tmp_path / "board.copper"), offline=True)
    assert not check(board)
    part = board.library["v.BUTTON"]
    assert tuple(g.numbers for g in part.internal_pad_groups) == (("1",), ("2",))
    assert part.source.checksum == "sha256:24633cbf6a2f784611d0986a0ca86333039d6dcf532db465342a1e659ab9ad6e"
