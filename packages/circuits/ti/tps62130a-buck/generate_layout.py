"""Deterministic, provisional six-layer TPS62130A physical adaptation.

Uses the documented circuit and layout principles, not extracted vendor CAD.
No compiler implementation or fetching is included in this generator.
"""
from hashlib import sha256
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAYERS = ["F.Cu", "In1.Cu", "In2.Cu", "In3.Cu", "In4.Cu", "B.Cu"]
FOOTPRINTS = {
    "U": ("Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm", "2cd7a54456461aff937a78ba0d02a90302e6000c2b7eb618b82920a55a5bda6b"),
    "L": ("Inductor_SMD:L_Coilcraft_XAL4020-XXX", "676cea6505e0b24c6ab5f94a07d9492d504f7f7d7bccffa3f1542e2455c2ded5"),
    "C_PVIN": ("Capacitor_SMD:C_0805_2012Metric", "89bba70c2d465045c058445d23f9626bb02341f69c6d5c44043a8621be2112ce"),
    "C_OUT1": ("Capacitor_SMD:C_0805_2012Metric", "89bba70c2d465045c058445d23f9626bb02341f69c6d5c44043a8621be2112ce"),
    "C_OUT2": ("Capacitor_SMD:C_0805_2012Metric", "89bba70c2d465045c058445d23f9626bb02341f69c6d5c44043a8621be2112ce"),
    "C_AVIN": ("Capacitor_SMD:C_0402_1005Metric", "6626461e823efd255bfbdef7bdf64c8feb10fc410b0cacfd6353137e29252eda"),
    "C_SS": ("Capacitor_SMD:C_0402_1005Metric", "6626461e823efd255bfbdef7bdf64c8feb10fc410b0cacfd6353137e29252eda"),
    "R_FB_TOP": ("Resistor_SMD:R_0402_1005Metric", "66db65bc75ecc968fdec69997097d224d9fb5d1d7ae2517c82faa8042d3e127e"),
    "R_FB_BOT": ("Resistor_SMD:R_0402_1005Metric", "66db65bc75ecc968fdec69997097d224d9fb5d1d7ae2517c82faa8042d3e127e"),
}
POSES = {"U": (0, 0, 0), "L": (-5.1, 1.05, 90), "C_PVIN": (3.2, -1.9, 90),
         "C_AVIN": (3.4, .9, 0), "C_SS": (2.9, 2.6, 180),
         "C_OUT1": (-4.2, -2.7, 0), "C_OUT2": (-8, -2.7, 180),
         "R_FB_TOP": (-1.6, 3, 0), "R_FB_BOT": (.3, 3, 0)}


def nm(value): return round(value * 1_000_000)
def point(x, y): return [nm(x), nm(y)]
def pad(ref, number): return {"pad": [ref, str(number)]}


def generate(enabled=False):
    """The variant changes only the explicit EN role and its local connection."""
    tracks, vias = [], []
    def track(net, vertices, width=.25, layer="F.Cu"):
        tracks.append(dict(net=net, points=[v if isinstance(v, dict) else point(*v) for v in vertices],
                           width_nm=nm(width), layer=layer))
    def via(net, xy, thermal=False):
        data = dict(net=net, position_nm=point(*xy), size_nm=450000 if thermal else 600000,
                    drill_nm=200000 if thermal else 300000, from_layer="F.Cu", to_layer="B.Cu", technology=None)
        if thermal: data["finish"] = "filled-capped"
        vias.append(data)
    pad_nets = []
    def assign(ref, numbers, net):
        pad_nets.extend([ref, str(number), net] for number in numbers)
    for numbers, net in [([1,2,3],"SW"),([5],"FB"),([6,7,8,15,16,17],"GND"),([9],"SS"),
                         ([10,11,12],"VIN"),([13],"EN" if enabled else "VIN"),([14],"VOUT")]:
        assign("U", numbers, net)
    assign("L",[1],"SW"); assign("L",[2],"VOUT")
    for ref, net in [("C_PVIN","VIN"),("C_AVIN","VIN"),("C_SS","SS"),("C_OUT1","VOUT"),("C_OUT2","VOUT")]:
        assign(ref,[1],net); assign(ref,[2],"GND")
    assign("R_FB_TOP",[1],"VOUT"); assign("R_FB_TOP",[2],"FB")
    assign("R_FB_BOT",[1],"FB"); assign("R_FB_BOT",[2],"GND")

    # Every power contact is individually wired; none is an internal-pad exemption.
    for n in (1,2,3): track("SW", [pad("U",n),(-2.25,(-.75,-.25,.25)[n-1])], .25)
    # Fixed, contoured power copper follows TI Figure 11-1's VIN/SW/VOUT
    # arrangement. The second output capacitor extends the reference's VOUT
    # edge without enlarging the switching island.
    def polygon(name, net, vertices):
        return dict(id=name, net=net, layer="F.Cu", vertices=[point(*p) for p in vertices])
    polygons = [
        polygon("switch-island", "SW", [(-3.1,-1.1),(-1.9,-1.1),
                (-1.9,.35),(-2.3,.35),(-2.3,2.4),(-5.3,2.4),
                (-5.3,1.8),(-3.1,1.8)]),
        polygon("input-lobe", "VIN", [(1.8,-1),(2.3,-1),(2.3,-1.55),
                (6.3,-1.55),(6.3,-.35),(2.3,-.35),(2.3,-.05),(1.8,-.05)]),
        polygon("output-lobe", "VOUT", [(-9.2,.8),(-7.4,.8),(-7.4,.5),
                (-5.75,.5),(-5.75,-1.9),(-3.9,-1.9),(-3.9,-3.3),
                (-7.4,-3.3),(-7.4,-1.6),(-9.2,-1.6)]),
    ]
    for n, y in ((11,-.25),(12,-.75)):
        track("VIN", [pad("U",n),(2.25,y)], .25)
    track("VIN", [pad("U",10),(2.1,.25),(2.75,.9),pad("C_AVIN",1)], .25)
    track("VIN", [pad("C_AVIN",1),(2.92,-.95),pad("C_PVIN",1)], .25)
    track("VIN", [pad("C_PVIN",1),(7.2,-.95)], .8)
    for xy in ((7.2,-.95),(7.2,-.15)):
        via("VIN", xy)
    track("VIN", [(7.2,-.95),(7.2,-.15)], .8)
    track("VIN", [(7.2,-.95),(7.2,-.15)], .8,"B.Cu")
    track("VOUT", [(-8.3,0),(-11.2,0)], .8)
    for xy in ((-11.2,0),(-11.2,.8)):
        via("VOUT", xy)
    track("VOUT", [(-11.2,0),(-11.2,.8)], .8)
    track("VOUT", [(-11.2,0),(-11.2,.8)], .8,"B.Cu")
    # Quiet sense geometry is owner copper on In2, shielded from SW by In1 GND.
    track("VOUT", [pad("U",14),(.25,-2.6)], .25)
    track("VOUT", [pad("C_OUT1",1),(-5.2,-1.55)], .25)
    track("VOUT", [pad("R_FB_TOP",1),(-2.11,4.25)], .25)
    for xy in ((.25,-2.6),(-5.2,-1.55),(-2.11,4.25)):
        via("VOUT",xy)
    track("VOUT", [(.25,-2.6),(.25,-1.85),(-5.2,-1.55),(-5.2,5),(-2.11,5),(-2.11,4.25)], .25,"In2.Cu")
    track("FB", [pad("U",5),(-.75,2.3),(-1.09,2.64),pad("R_FB_TOP",2),pad("R_FB_BOT",1)], .2)
    track("SS", [pad("U",9),(2,.75),(2,1.6),pad("C_SS",1)], .2)
    for n, xy in ((6,(-.25,.65)),(7,(.25,.65)),(8,(.75,.65)),(15,(-.25,-.65)),(16,(-.75,-.65))):
        track("GND", [pad("U",n),xy], .25)
    ep_vias = ((-.35,-.35),(.35,-.35),(-.35,.35),(.35,.35))
    for xy in ep_vias:
        via("GND",xy,thermal=True)
    grounds = [("C_PVIN",(2.1,-2.85)),("C_AVIN",(4.8,.9)),("C_SS",(1.4,2.6)),
               ("C_OUT1",(-2.2,-2.7)),("C_OUT2",(-9.85,-2.7)),("R_FB_BOT",(.81,4))]
    for ref, xy in grounds:
        track("GND",[pad(ref,2),xy],.5 if ref in {"C_PVIN","C_OUT1","C_OUT2"} else .25)
        via("GND",xy)
    if enabled:
        track("EN",[pad("U",13),(1,-1.7125),(1,-6.5),(2,-6.5)],.2)
    else:
        track("VIN",[pad("U",13),(1,-1.7125),(1,-3.8),(4.3,-3.8),(4.3,-1.55)],.25)

    # One broad lower GND return complements the fixed VIN/VOUT conductors;
    # refill clears it around the output lobe and makes the ground contacts.
    def zone(name, net, vertices):
        return dict(id=name, net=net, layers=["F.Cu"], vertices=[point(*p) for p in vertices],
                    priority=2, clearance_nm=200000, minimum_width_nm=200000,
                    pad_connection="solid")
    zones = [
        zone("lower-return", "GND", [(-10.3,-5.7),(5.9,-5.7),(5.9,-1.8),
             (1.3,-1.8),(1.3,-.7),(-3.3,-.7),(-3.3,-1.8),(-10.3,-1.8)]),
        zone("exposed-pad", "GND", [(-.6,-.6),(.6,-.6),(.6,.6),(-.6,.6)]),
    ]

    def region(name,layers,tracks,vias,zones):
        return dict(id=name,layers=layers,vertices=[point(-10.6,-6),point(6.6,-6),point(6.6,5.1),point(-10.6,5.1)],
                    block_tracks=tracks,block_vias=vias,block_zones=zones)
    ports = []
    for role, xy, layer in [("VIN",(7.2,-.95),"F.Cu"),("VOUT",(-11.2,0),"F.Cu")]+([("EN",(2,-6.5),"F.Cu")] if enabled else []):
        ports.append(dict(name=role,net=role,point=point(*xy),layer=layer,pads=[[r,p] for r,p,n in pad_nets if n==role]))
    plane_returns = [dict(net="GND", layers=["In1.Cu","In4.Cu"],
                          pads=[[r,p] for r,p,n in pad_nets if n=="GND"],
                          dedicated_contacts=[dict(pad=[ref,"2"],via_position_nm=point(*xy))
                                              for ref,xy in grounds])]
    return dict(schema="copperlib-physical-hard-macro/v0.3", production_publishable=False,
        source={"datasheet_url":"https://www.ti.com/lit/ds/symlink/tps62130a.pdf",
                "datasheet_sha256":"f9b1af285622c0cf1a5991f9641a6e64c5e6d899e52cc0b1632808742019579f",
                "datasheet_locator":"SLVSAG7F Rev F, Table 6-1, sections 11.1–11.3, Figure 11-1, pages 3 and 28–29",
                "evm_url":"https://www.ti.com/lit/pdf/SLVU437",
                "evm_sha256":"b8e09708c6e866ee1c7f99993dd430967e1b3d1055678873452f3af0d8402237",
                "evm_locator":"SLVU437B Rev B, sections 4–5, pages 16–20",
                "geometry_status":"authored adaptation; different inductor, two output capacitors and six-layer stack; not extracted TI CAD",
                "gerber_status":"SLVC394 public URLs returned HTTP 401 on 2026-10-06; archive not consumed"},
        anchor="U",members=[dict(reference=r,footprint=FOOTPRINTS[r][0],footprint_digest=FOOTPRINTS[r][1],
                                 center_nm=point(x,y),rotation_degrees=str(angle),edge_clearance_nm=250000)
                              for r,(x,y,angle) in sorted(POSES.items())],
        pad_nets=pad_nets,isolated_pads=[["U","4"]],tracks=tracks,vias=vias,ports=ports,zones=zones,polygons=polygons,
        plane_returns=plane_returns,
        protected_regions=[region("regulator-private",["F.Cu","In2.Cu","B.Cu"],True,True,False)],
        keepouts=[region("regulator-fill-exclusion",["In2.Cu","In3.Cu","B.Cu"],False,False,True)],
        required_layers=LAYERS,allowed_rotations=[0,90,180,270],internal_clearance_nm=0,
        unresolved=["rail current and thermal qualification including access-neck and via-bank capacity",
                    "assembly review of filled-capped thermal vias and solder paste",
                    "six-layer laminate and control-loop/EMI bench validation",
                    "TI Gerber archive unavailable without authentication; authored adaptation rather than CAD reproduction"])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=ROOT/"assets")
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    for enabled in (False,True):
        path=args.output_dir/f"tps62130a-six-layer-{'enabled' if enabled else 'always-on'}.json"
        path.write_bytes((json.dumps(generate(enabled),sort_keys=True,indent=2)+"\n").encode())
        print(f"{path.name}: sha256:{sha256(path.read_bytes()).hexdigest()}")


if __name__=="__main__":main()
