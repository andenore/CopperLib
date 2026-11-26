"""Deterministic TI RPW0010A and Q5B copper/assembly land patterns.

Manufacturer sources and adaptation boundaries are in the owning packages.
This does not generate a physical macro or certify current capacity.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pad(number, x, y, w, h, layers="F.Cu F.Mask", radius=0):
    shape = "roundrect" if radius else "rect"
    rr = f" (roundrect_rratio {radius / min(w, h):.9f})" if radius else ""
    return f'  (pad "{number}" smd {shape} (at {x:g} {y:g}) (size {w:g} {h:g}) (layers {layers}){rr})'


def outline(name, body, courtyard, description):
    lines = [f'(module {name} (layer F.Cu)', f'  (descr "{description}")', '  (attr smd)',
             f'  (fp_text reference REF** (at 0 {-courtyard[1]-0.7:g}) (layer F.SilkS) (effects (font (size 0.7 0.7) (thickness 0.12))))',
             f'  (fp_text value {name} (at 0 {courtyard[1]+0.7:g}) (layer F.Fab) (effects (font (size 0.7 0.7) (thickness 0.12))))']
    for (x, y), layer, width in [(body, "F.Fab", .1), (courtyard, "F.CrtYd", .05)]:
        for a,b in [((-x,-y),(x,-y)),((x,-y),(x,y)),((x,y),(-x,y)),((-x,y),(-x,-y))]:
            lines.append(f'  (fp_line (start {a[0]:g} {a[1]:g}) (end {b[0]:g} {b[1]:g}) (layer {layer}) (width {width:g}))')
    lines.append(f'  (fp_circle (center {-courtyard[0]-.2:g} {-body[1]:g}) (end {-courtyard[0]-.1:g} {-body[1]:g}) (layer F.SilkS) (width 0.1))')
    return lines


def tps25947():
    # TI 4225183/A 08/2019, PDF pp73-74, TOP (PCB) view.
    a=outline("TI_RPW0010A_TPS25947", (1,1), (1.45,1.45),
              "TI RPW0010A copper from 4225183/A; overlapping rounded rectangles preserve L terminals; no internal-pad routing waivers")
    for n,x,y in [(1,-.725,-.875),(4,-.725,.875),(7,.725,.875),(10,.725,-.875)]:
        a += [pad(n,x,y,.25,.65,radius=.05), pad(n, -.9 if x<0 else .9, -.7 if y<0 else .7,.6,.3,radius=.05)]
        # TI split corner apertures; two overlapping windows form the L.
        a += [pad("",-.7125 if x<0 else .7125,-.885 if y<0 else .885,.225,.63,"F.Paste",.05),
              pad("",-.9 if x<0 else .9,-.7125 if y<0 else .7125,.6,.275,"F.Paste",.05)]
    for n,x,y in [(2,-.9,-.225),(3,-.9,.225),(8,.9,.225),(9,.9,-.225)]:
        a.append(pad(n,x,y,.6,.25,"F.Cu F.Mask F.Paste",.05))
    for n,x in [(5,-.25),(6,.25)]:
        a.append(pad(n,x,0,.3,2.4,radius=.05))
        for y in [-.63,.63]:
            a.append(pad("",x,y,.28,1.06,"F.Paste",.05))
    return "\n".join(a+["", ")", ""])


def csd18540():
    # TI SLPS488B p9 copper, rotated 180 degrees to p1 top-view pinning.
    a=outline("TI_Q5B_CSD18540", (3,2.5), (3.71,2.75),
              "TI Q5B copper from SLPS488B p9; central D contact represented as pad9; all source/drain contacts require external copper; authored paste adaptation")
    for n,y in [(1,-1.905),(2,-.635),(3,.635),(4,1.905)]:
        a.append(pad(n,-2.77,y,1.372,.71))
        a.append(pad("",-2.77,y,1.072,.562,"F.Paste"))
    a.append(pad(9,.941,0,3.85,4.52))
    for n,y in [(5,1.905),(6,.635),(7,-.635),(8,-1.905)]:
        a.append(pad(n,3.161,y,.59,.71))
        a.append(pad("",3.12,y,.508,.508,"F.Paste"))
    # Eight 1.294 x .746 windows follow TI aperture sizes; symmetric positions
    # within the central rectangular contact are an authored assembly adaptation.
    for x in [.119,1.763]:
        for y in [-1.635,-.545,.545,1.635]:
            a.append(pad("",x,y,1.294,.746,"F.Paste"))
    return "\n".join(a+["", ")", ""])


def generate():
    for package,name,text in [("tps25947","TI_RPW0010A_TPS25947",tps25947()),
                              ("csd18540q5b","TI_Q5B_CSD18540",csd18540())]:
        path=ROOT / "packages/parts/ti" / package / "footprints" / (name+".kicad_mod")
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding="utf-8",newline="\n")


if __name__ == "__main__":
    generate()
