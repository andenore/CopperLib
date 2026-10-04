"""Source-backed antenna terminal audit, independent of placement/tuning."""
import json
from pathlib import Path

from pcbir import ConnectionPolicy, check, compile_source

ROOT = Path(__file__).resolve().parents[1]


def _board(tmp_path, connect_anchor=False):
    (tmp_path / 'copper.mod').write_text(
        'module antenna-test\nrequire github.com/andenore/CopperLib v0.1.0\n'
        f'replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n')
    return compile_source('''
        board AntennaAudit {
            import rf "github.com/andenore/CopperLib/packages/parts/johanson/2450at18a0100001e";
            component ANT: rf.JOHANSON_2450AT18A0100001E;
            net FEED { ANT.FEED; }
    ''' + ('net WRONG { ANT.NC; }' if connect_anchor else '') + '}',
        str(tmp_path / 'rf-audit-smoke.copper'), offline=True)


def test_antenna_anchor_is_nc_with_source_evidence(tmp_path):
    board = _board(tmp_path)
    part = board.library['rf.JOHANSON_2450AT18A0100001E']
    assert {name: pin.number for name, pin in part.pins.items()} == {'FEED': '1', 'NC': '2'}
    assert part.pins['NC'].connection_policy is ConnectionPolicy.DO_NOT_CONNECT
    assert part.pins['NC'].profile is None
    assert part.footprints == ('RF_Antenna:Johanson_2450AT18x100',)
    evidence = json.loads((ROOT / 'packages/parts/johanson/2450at18a0100001e/evidence/rf-audit.json').read_text())
    assert part.source.checksum == 'sha256:' + evidence['source']['sha256']
    assert evidence['production_publishable'] is False
    assert check(board) == []


def test_erc_rejects_any_net_on_antenna_mechanical_anchor(tmp_path):
    assert any(d.code == 'DO_NOT_CONNECT' for d in check(_board(tmp_path, connect_anchor=True)))
