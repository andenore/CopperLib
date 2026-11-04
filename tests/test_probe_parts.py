"""Parts migrated from CopperProbeParts: pin maps and footprints match the recorded contracts."""
import hashlib
import json
from pathlib import Path

import pytest
from copper_cli import compile_board, part, pins

PARTS = Path(__file__).resolve().parents[1] / "packages/parts"
LIB = "github.com/andenore/CopperLib/packages/parts"
PACKAGES = ("abracon/abm8", "adi/ltc6268", "amphenol/12401610e4", "gct/usb4230", "infineon/cyusb4013",
            "murata/blm15px", "sitime/sit9121", "ti/ads4125", "ti/lm27761", "ti/ths4541", "ti/tlv757", "ti/tps7a20")
CASES = [(package, name, entry) for package in PACKAGES
         for name, entry in json.loads((PARTS / package / "evidence/contract.json").read_text()).items()]


@pytest.mark.parametrize("package,name,entry", CASES, ids=[name for _, name, _ in CASES])
def test_pins_and_footprint_match_contract(package, name, entry):
    board = compile_board(f'board Test {{ import p "{LIB}/{package}"; component U: p.{name}; }}')
    if "pins" in entry:
        assert pins(board, f"p.{name}") == entry["pins"]
    footprint = part(board, f"p.{name}")["footprints"][0]
    bundled = f"{LIB}/{package}/"
    if footprint.startswith(bundled):
        # Bundled lands keep the bytes CopperProbeParts recorded.
        land = PARTS / package / footprint.removeprefix(bundled)
        recorded = entry.get("footprint_inventory", {}).get("sha256")
        assert land.is_file()
        if recorded:
            assert hashlib.sha256(land.read_bytes()).hexdigest() == recorded
    else:
        assert footprint == entry["footprint"]
