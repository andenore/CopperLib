"""Bounded physical macro probe using CopperScript's public integration APIs.

The test terminals exercise external access; this is not a powered bench board.
Run with CopperScript on PYTHONPATH and explicit installed KiCad footprints.
"""
import argparse
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path

from pcbir import compile_source, resolved_physicalize, FootprintResolver, PrototypePhysicalOptions
from pcbir.clusters import cluster_placements
from pcbir.drc import PhysicalDrcPolicy, run_physical_drc
from pcbir.hard_macros import bind_hard_macro, materialize_hard_macros
from pcbir.physical import Point
from pcbir.placement import transformed_local_point

ROOT = Path(__file__).resolve().parent
LIBRARY = ROOT.parents[3]


def make_trial(directory, *, enabled=False, rotation=0, footprint_root=Path("/usr/share/kicad/footprints"),
               external=True, asset_path=None):
    """Compile real electrical membership, bind exact footprints, then materialize."""
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "copper.mod").write_text(
        "module tps62130a-layout-trial\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {LIBRARY.as_posix()}\n", encoding="utf-8")
    roles = ["VIN", "VOUT", "GND"] + (["EN"] if enabled else [])
    terminal_part = """
        part TestTerminal {
            footprint = "TestPoint:TestPoint_Pad_D1.0mm";
            pin P { number = "1"; domains = "digital,power,ground"; directions = "passive"; }
        }
    """
    (directory / "terminal").mkdir(exist_ok=True)
    (directory / "terminal/part.copper").write_text(terminal_part, encoding="utf-8")
    terminals = 'import probe "./terminal";\n' + "\n".join(f"component J_{role}: probe.TestTerminal;" for role in roles) if external else ""
    def terminal(role): return f"J_{role}.P;" if external else ""
    source = '''board BuckLayoutTrial {
        import buck "github.com/andenore/CopperLib/packages/circuits/ti/tps62130a-buck";
        import passives "github.com/andenore/CopperLib/packages/generic/passives";
        module B: buck.TPS62130A_BUCK_2U2;
        component R_TOP: passives.RESISTOR { value = 49.9kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }
        component R_BOT: passives.RESISTOR { value = 100kohm; footprint = "Resistor_SMD:R_0402_1005Metric"; }
    ''' + terminals + f'''
        net VIN {{ B.VIN; {'' if enabled else 'B.EN;'} {terminal('VIN')} }}
        {f'net ENABLE {{ B.EN; {terminal("EN")} }}' if enabled else ''}
        net FB {{ B.FB; R_TOP.P2; R_BOT.P1; }}
        net VOUT {{ B.VOUT; R_TOP.P1; {terminal('VOUT')} }}
        net GND {{ B.GND; R_BOT.P2; {terminal('GND')} }}
        supply VIN {{ voltage = 5V; external = true; }}
        supply VOUT {{ voltage = 1.2V; source = B.VOUT; }}
        supply GND {{ voltage = 0V; external = true; }}
        constraint copper_zone(GND) {{ layers = "In1.Cu,In4.Cu"; pad_connection = solid; }}
        constraint via_in_pad(B/U.EP) {{ process = "filled-capped"; }}
        constraint routing(VIN) {{ width = 0.25mm; }}
        constraint routing(VOUT) {{ width = 0.25mm; }}
    }}'''
    path = directory / "board.copper"
    path.write_text(source, encoding="utf-8")
    electrical = compile_source(source, str(path), offline=True)
    board = resolved_physicalize(electrical, FootprintResolver(directory, (Path(footprint_root),), offline=True),
        PrototypePhysicalOptions(board_width_mm=40, board_height_mm=40, copper_layers=6,
                                 fabrication_profile="jlcpcb-six-layer"))
    asset_path = asset_path or ROOT / "assets" / f"tps62130a-six-layer-{'enabled' if enabled else 'always-on'}.json"
    data = json.loads(asset_path.read_bytes())
    bindings = {m["reference"]: ("R_TOP" if m["reference"] == "R_FB_TOP" else
                 "R_BOT" if m["reference"] == "R_FB_BOT" else "B/" + m["reference"]) for m in data["members"]}
    nets = {role: role for role in ("VIN", "VOUT", "GND", "FB")}
    nets.update(SW="B/SW", SS="B/SS")
    if enabled: nets["EN"] = "ENABLE"
    board = bind_hard_macro(board, asset_path, expected_sha256=sha256(asset_path.read_bytes()).hexdigest(),
                           name="regulator", bindings=bindings, net_bindings=nets)
    poses = {p.reference:p for p in board.placements}
    anchor = replace(poses["B/U"], position=Point.mm(20,20), rotation_degrees=rotation)
    poses.update(cluster_placements(board, board.rigid_clusters[0], anchor))
    if external:
        for role, xy in {"VIN":(6.1,-7), "VOUT":(-6,8.5), "GND":(0,8.5), "EN":(2,-7)}.items():
            ref = "J_" + role
            if ref in poses:
                poses[ref] = replace(poses[ref], position=transformed_local_point(anchor, Point.mm(*xy)),
                                     rotation_degrees=rotation)
    board = replace(board, placements=tuple(poses.values()),
                    metadata={**board.metadata,"prototype_placement":"false","fabrication_ready":"false"})
    return materialize_hard_macros(board)


def route_trial(board):
    from pcbir.routing import GlobalRouterOptions, route_global
    from pcbir.detailed import DetailedRouterOptions, route_detailed
    from pcbir.plane import stitch_zone_pads
    guides = route_global(board, GlobalRouterOptions(maximum_iterations=2, tile_size_nm=1000000))
    board = stitch_zone_pads(board).board
    result = route_detailed(board, guides, DetailedRouterOptions(maximum_passes=1,
        maximum_search_states=20000))
    zone_nets = {zone.net for zone in board.zones}
    if any(not net.connected and net.net not in zone_nets for net in result.nets):
        raise ValueError("external macro access failed: " + str([(n.net,n.diagnostics) for n in result.nets if not n.connected]))
    return result.board


def main():
    from pcbir.backends.kicad_pcb import KiCadPcbBackend
    from pcbir.backends.kicad_project import write_kicad_project
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="probe directory outside CopperLib (keeps generated JSON out of dependency locks)")
    parser.add_argument("--footprint-root", type=Path, default=Path("/usr/share/kicad/footprints"))
    parser.add_argument("--enabled", action="store_true")
    parser.add_argument("--rotation", type=int, choices=(0,90,180,270), default=0)
    args = parser.parse_args()
    board = route_trial(make_trial(args.output_dir, enabled=args.enabled, rotation=args.rotation,
                                   footprint_root=args.footprint_root))
    report = run_physical_drc(board, policy=PhysicalDrcPolicy(False))
    (args.output_dir/"physical-drc.json").write_text(report.to_json(),encoding="utf-8")
    write_kicad_project(KiCadPcbBackend().generate(board),args.output_dir/"buck.kicad_pcb")
    print(f"{len(board.tracks)} tracks, {len(board.vias)} vias; physical findings: {len(report.findings)}")
    print("Provisional geometry probe; current, thermal, assembly and control-loop qualification remain open.")


if __name__ == "__main__": main()
