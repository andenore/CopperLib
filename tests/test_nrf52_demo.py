from copper_cli import check, compile_board, part, pins


def test_demo_support_part_contracts():
    source = '''board SupportContract {
        import keystone "github.com/andenore/CopperLib/packages/parts/keystone/3034";
        component BT: keystone.KEYSTONE_3034;
        net V { BT.POS; }
        net GND { BT.NEG; }
        supply GND { voltage = 0V; external = true; }
    }'''
    assert check(source) == []
    board = compile_board(source)
    assert pins(board, "keystone.KEYSTONE_3034") == {"POS": "1", "NEG": "2"}
    assert part(board, "keystone.KEYSTONE_3034")["internal_pad_groups"] == [["1"]]


def test_button_internal_groups_do_not_short_signal_to_ground():
    source = '''board SwitchContract {
        import v "github.com/andenore/CopperLib/packages/generic/switch-button";
        component S: v.BUTTON;
        net BUTTON { S.A; }
        net GND { S.B; }
    }'''
    assert not check(source)
    button = part(compile_board(source), "v.BUTTON")
    assert button["internal_pad_groups"] == [["1"], ["2"]]
    assert button["source"]["checksum"] == "sha256:24633cbf6a2f784611d0986a0ca86333039d6dcf532db465342a1e659ab9ad6e"
