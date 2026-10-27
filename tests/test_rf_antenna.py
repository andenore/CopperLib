"""Source-backed antenna terminal audit, independent of placement/tuning."""
import json
from pathlib import Path

from copper_cli import check, compile_board, part

ROOT = Path(__file__).resolve().parents[1]


def _board(connect_anchor=False):
    return '''
        board AntennaAudit {
            import rf "github.com/andenore/CopperLib/packages/parts/johanson/2450at18a0100001e";
            component ANT: rf.JOHANSON_2450AT18A0100001E;
            net FEED { ANT.FEED; }
    ''' + ('net WRONG { ANT.NC; }' if connect_anchor else '') + '}'


def test_antenna_anchor_is_nc_with_source_evidence():
    antenna = part(compile_board(_board()), 'rf.JOHANSON_2450AT18A0100001E')
    assert {name: pin['number'] for name, pin in antenna['pins'].items()} == {'FEED': '1', 'NC': '2'}
    assert antenna['pins']['NC']['connection_policy'] == 'do_not_connect'
    assert antenna['pins']['NC']['profile'] is None
    assert antenna['footprints'] == ['RF_Antenna:Johanson_2450AT18x100']
    evidence = json.loads((ROOT / 'packages/parts/johanson/2450at18a0100001e/evidence/rf-audit.json').read_text())
    assert antenna['source']['checksum'] == 'sha256:' + evidence['source']['sha256']
    assert evidence['production_publishable'] is False
    assert check(_board()) == []


def test_erc_rejects_any_net_on_antenna_mechanical_anchor():
    assert any(d['code'] == 'DO_NOT_CONNECT' for d in check(_board(connect_anchor=True)))
