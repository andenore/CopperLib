from pathlib import Path

from pcbir import check, compile_source
from pcbir.importers import load_kicad_mod

ROOT = Path(__file__).resolve().parents[1]


def test_exact_parts_have_manufacturer_and_polarity_correct_footprint(tmp_path):
    (tmp_path / "copper.mod").write_text(
        "module assembly-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n", encoding="utf-8")
    board = compile_source('''board ExactParts {
        import kento "github.com/andenore/CopperLib/packages/parts/kento/kt0603r";
        import uniroyal "github.com/andenore/CopperLib/packages/parts/uniroyal/0603waf";
        import samsung "github.com/andenore/CopperLib/packages/parts/samsung/cl05";
        import fenghua "github.com/andenore/CopperLib/packages/parts/fenghua/0402cg";
        import samsung_cl10 "github.com/andenore/CopperLib/packages/parts/samsung/cl10";
        component D: kento.KENTO_KT0603R;
        component R: uniroyal.UNIROYAL_0603WAF1002T5E { value = 10kohm; }
        component C1: samsung.SAMSUNG_CL05B104KO5NNNC { value = 100nF; }
        component C2: fenghua.FENGHUA_0402CG101J500NT { value = 100pF; }
        component C3: samsung_cl10.SAMSUNG_CL10A105KB8NNNC { value = 1uF; }
        component C4: samsung_cl10.SAMSUNG_CL10A475KO8NNNC { value = 4.7uF; }
        net A { D.A; R.1; C1.1; C2.1; C3.1; C4.1; }
        net B { D.K; R.2; C1.2; C2.2; C3.2; C4.2; }
    }''', str(tmp_path / "board.copper"), offline=True)
    assert not check(board)
    part = board.library["kento.KENTO_KT0603R"]
    assert {name: pin.number for name, pin in part.pins.items()} == {"A":"1", "K":"2"}
    assert part.source.checksum == "sha256:a3bac1cc9c59cb306ad03512945cce12c87bb54252abc223b796e1d20d41d4a1"
    footprint = load_kicad_mod(ROOT / "packages/parts/kento/kt0603r/footprints/KENTO_KT0603R.kicad_mod").footprint
    pads = {pad.number: pad for pad in footprint.pads}
    assert pads["2"].position.x_nm == -787500
    assert pads["1"].position.x_nm == 787500
    assert pads["1"].size.width_nm == 875000
    assert pads["1"].size.height_nm == 950000
    for component in board.components:
        part = board.library[component.part]
        assert part.manufacturer and part.source and part.footprints
