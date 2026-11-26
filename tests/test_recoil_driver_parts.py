"""Manufacturer pinout regressions and mandatory power qualification gates."""
from pathlib import Path
from copper_cli import compile_board, pins
from contracts import load_contract

ROOT = Path(__file__).resolve().parents[1]

def test_recoil_parts_use_exact_package_pinouts():
    ir = compile_board('''board DriverParts {
        import amp "github.com/andenore/CopperLib/packages/parts/ti/ina180";
        import drv "github.com/andenore/CopperLib/packages/parts/ti/ucc27517";
        import pfet "github.com/andenore/CopperLib/packages/parts/diodes/dmp6023le";
        import npn "github.com/andenore/CopperLib/packages/parts/nexperia/mmbt3904";
        import tvs "github.com/andenore/CopperLib/packages/parts/vishay/smbj";
        component A: amp.INA180A1IDBVR;
        component D: drv.UCC27517DBVR;
        component P: pfet.DMP6023LE_13;
        component N: npn.MMBT3904;
        component T: tvs.SMBJ15A;
    }''')
    # TI INA180 SBOS741H p4: A pinout, not B.
    assert pins(ir, "amp.INA180A1IDBVR") == {
        "OUT":"1", "GND":"2", "IN_P":"3", "IN_N":"4", "VS":"5"}
    # TI SLUSAY4D pin table: supply is pin1, not pin5.
    assert pins(ir, "drv.UCC27517DBVR") == {
        "VDD":"1", "GND":"2", "IN_P":"3", "IN_N":"4", "OUT":"5"}
    # DS37199 p1; Nexperia 8-Apr-2026 p1; Vishay 88392 polarity.
    assert pins(ir, "pfet.DMP6023LE_13") == {"G":"1", "D":"2", "S":"3"}
    assert pins(ir, "npn.MMBT3904") == {"B":"1", "E":"2", "C":"3"}
    assert pins(ir, "tvs.SMBJ15A") == {"K":"1", "A":"2"}

def test_new_power_parts_retain_all_external_qualification_gates():
    for package in ("ti/ina180", "ti/ucc27517", "diodes/dmp6023le", "vishay/smbj", "nexperia/mmbt3904"):
        c = load_contract(ROOT / "packages/parts" / package / "qualification.json")
        assert c["production_publishable"] is False
        assert all(r["algorithm"] == "external" for r in c["requirements"])

