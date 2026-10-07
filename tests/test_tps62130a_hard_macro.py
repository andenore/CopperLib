"""Regulator topology, immutable geometry and independent refill acceptance."""
from dataclasses import replace
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/circuits/ti/tps62130a-buck"
FOOTPRINT_ROOT = Path(os.environ.get("KICAD_FOOTPRINT_ROOT", "/usr/share/kicad/footprints"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, PACKAGE/f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def path(enabled):
    return PACKAGE/"assets"/f"tps62130a-six-layer-{'enabled' if enabled else 'always-on'}.json"


@pytest.mark.parametrize("enabled", [False, True])
def test_assets_reproduce_and_bind_every_required_pad(enabled):
    asset = load("generate_layout").generate(enabled)
    assert (json.dumps(asset,sort_keys=True,indent=2)+"\n").encode() == path(enabled).read_bytes()
    assert asset["production_publishable"] is False and asset["unresolved"]
    assert len(asset["members"]) == 9
    assert asset["isolated_pads"] == [["U","4"]]
    assert {p for r,p,n in asset["pad_nets"] if r == "U"} == {str(p) for p in range(1,18) if p != 4}
    assert {n for r,p,n in asset["pad_nets"] if r == "U" and p == "13"} == {"EN" if enabled else "VIN"}
    assert not any(v["net"] == "SW" for v in asset["vias"])
    assert all(t["layer"] == "F.Cu" for t in asset["tracks"] if t["net"] == "SW")
    assert all(t["width_nm"] >= 250000 for t in asset["tracks"] if t["net"] in {"VIN", "VOUT"})
    assert sum(v.get("finish") == "filled-capped" for v in asset["vias"]) == 4
    for port in asset["ports"]:
        assert {tuple(p) for p in port["pads"]} == {(r,p) for r,p,n in asset["pad_nets"] if n == port["net"]}
    assert all("In1.Cu" not in k["layers"] and "In4.Cu" not in k["layers"] for k in asset["keepouts"])


def test_cached_official_evidence_identity():
    asset = load("generate_layout").generate()
    for name, key in [("tps62130a.pdf","datasheet_sha256"),("slvu437b.pdf","evm_sha256")]:
        source = ROOT/"cache/ti/tps62130a-layout"/name
        if source.is_file(): assert sha256(source.read_bytes()).hexdigest() == asset["source"][key]


@pytest.mark.skipif(not FOOTPRINT_ROOT.is_dir(), reason="explicit KiCad footprint installation required")
@pytest.mark.parametrize("enabled", [False, True])
@pytest.mark.parametrize("rotation", [0,90,180,270])
def test_materialization_rotates_and_independent_refill_accepts_external_routes(tmp_path,enabled,rotation):
    from pcbir.hard_macros import materialize_hard_macros, validate_hard_macros
    from pcbir.backends.kicad_pcb import KiCadPcbBackend
    from pcbir.backends.kicad_project import write_kicad_project
    trial = load("layout_trial")
    board = trial.make_trial(tmp_path,enabled=enabled,rotation=rotation,footprint_root=FOOTPRINT_ROOT)
    assert materialize_hard_macros(board) is board
    routed = trial.route_trial(board)
    assert routed.tracks[:len(board.tracks)] == board.tracks
    assert routed.vias[:len(board.vias)] == board.vias
    validate_hard_macros(routed)
    cli = shutil.which("kicad-cli")
    if cli is None: pytest.skip("native KiCad CLI required for independent fill acceptance")
    target = tmp_path/"buck.kicad_pcb"
    write_kicad_project(KiCadPcbBackend().generate(routed),target)
    subprocess.run([cli,"pcb","drc","--refill-zones","--format","json","-o",str(tmp_path/"native.json"),str(target)],
                   check=True,capture_output=True,text=True)
    result = json.loads((tmp_path/"native.json").read_bytes())
    assert not result["violations"], result["violations"]
    assert not result["unconnected_items"], result["unconnected_items"]


@pytest.mark.skipif(not FOOTPRINT_ROOT.is_dir(), reason="explicit KiCad footprint installation required")
def test_broken_internal_owner_copper_and_same_net_intrusion_are_rejected(tmp_path):
    from pcbir.hard_macros import validate_hard_macros
    from pcbir.physical import CopperLayer, Point, TrackSegment
    trial = load("layout_trial")
    damaged = json.loads(path(False).read_bytes())
    damaged["tracks"] = [t for t in damaged["tracks"] if t["net"] != "SS"]
    asset = tmp_path/"broken.json"
    asset.write_text(json.dumps(damaged),encoding="utf-8")
    with pytest.raises(ValueError,match="internal net.*not connected"):
        trial.make_trial(tmp_path/"broken",footprint_root=FOOTPRINT_ROOT,asset_path=asset)
    board = trial.make_trial(tmp_path/"original",footprint_root=FOOTPRINT_ROOT)
    shortcut = TrackSegment("GND",Point.mm(19.9,20),Point.mm(20.1,20),150000,CopperLayer.FRONT)
    with pytest.raises(ValueError,match="new copper intrudes"):
        validate_hard_macros(replace(board,tracks=(*board.tracks,shortcut)))
    with pytest.raises(ValueError,match="immutable hard-macro copper"):
        validate_hard_macros(replace(board,tracks=board.tracks[1:]))


@pytest.mark.skipif(not FOOTPRINT_ROOT.is_dir(), reason="explicit KiCad footprint installation required")
@pytest.mark.parametrize("fault", ["footprint", "rail"])
def test_changed_real_footprint_or_rail_assignment_is_rejected(tmp_path,fault):
    data = json.loads(path(False).read_bytes())
    if fault == "footprint": data["members"][0]["footprint_digest"] = "0"*64
    else: next(p for p in data["pad_nets"] if p[:2] == ["U","11"])[2] = "VOUT"
    asset = tmp_path/"changed.json"
    asset.write_text(json.dumps(data),encoding="utf-8")
    with pytest.raises(ValueError,match="footprint identity mismatch" if fault == "footprint" else "pad/net mismatch"):
        load("layout_trial").make_trial(tmp_path/"probe",footprint_root=FOOTPRINT_ROOT,asset_path=asset)


@pytest.mark.skipif(not FOOTPRINT_ROOT.is_dir() or shutil.which("kicad-cli") is None,
                    reason="native KiCad plus explicit footprint installation required")
def test_surface_power_fill_connects_at_owner_via_banks(tmp_path):
    from pcbir.physical import CopperLayer, CopperZone, Point, PolygonRing, PolygonWithHoles, ZoneConnection
    from pcbir.plane import PlaneStitchOptions, stitch_zone_pads
    from pcbir.backends.kicad_pcb import KiCadPcbBackend
    from pcbir.backends.kicad_project import write_kicad_project
    from pcbir.hard_macros import validate_hard_macros
    trial = load("layout_trial")
    board = trial.make_trial(tmp_path,enabled=True,footprint_root=FOOTPRINT_ROOT)
    def zone(name,net,y0,y1):
        return CopperZone(name,net,(CopperLayer.BACK,),PolygonWithHoles(PolygonRing(tuple(
            Point.mm(x,y) for x,y in ((.5,y0),(39.5,y0),(39.5,y1),(.5,y1))))),
            pad_connection=ZoneConnection.SOLID)
    board = replace(board,zones=(*board.zones,zone("vin-access","VIN",.5,16),zone("vout-access","VOUT",25.2,39.5)))
    # Ordinary routing first has enough endpoint contacts; explicit surface
    # stitching then proves that no private-pad shortcut is needed for a pour.
    routed = trial.route_trial(board)
    stitched = stitch_zone_pads(routed,PlaneStitchOptions(include_surface_zones=True)).board
    assert stitched.tracks[:len(board.tracks)] == board.tracks
    assert stitched.vias[:len(board.vias)] == board.vias
    validate_hard_macros(stitched)
    target = tmp_path/"power-filled.kicad_pcb"
    write_kicad_project(KiCadPcbBackend().generate(stitched),target)
    subprocess.run([shutil.which("kicad-cli"),"pcb","drc","--refill-zones","--format","json",
                    "-o",str(tmp_path/"native.json"),str(target)],check=True,capture_output=True,text=True)
    result = json.loads((tmp_path/"native.json").read_bytes())
    assert not result["violations"], result["violations"]
    assert not result["unconnected_items"], result["unconnected_items"]
