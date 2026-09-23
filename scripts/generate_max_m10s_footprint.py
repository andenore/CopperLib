"""Deterministic MAX-M10S land pattern from u-blox UBX-20053088 R05, pp. 82-83.

Figure 30/Table 44 define copper and mask; Figure 31/Table 45 define the
recommended 150 um stencil. This is a mechanical transcription, not a source
of electrical pin facts. The source PDF belongs in ignored cache/.
"""

from __future__ import annotations

from pathlib import Path


DESTINATION = (
    Path(__file__).resolve().parents[1]
    / "footprints/RF_Module.pretty/u-blox_MAX-M10S.kicad_mod"
)


def render() -> str:
    lines = [
        '(footprint "u-blox_MAX-M10S"',
        '  (version 20240108)',
        '  (generator "copperlib")',
        '  (layer "F.Cu")',
        '  (descr "MAX-M10S-00B; u-blox UBX-20053088 R05 Figures 30-31, Tables 44-45")',
        '  (tags "ublox gnss MAX-M10S")',
        '  (attr smd)',
        '  (fp_rect (start -5.05 -4.85) (end 5.05 4.85)',
        '    (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))',
        # The manufacturer's 11.1 x 10.1 keepout is inside the paste extent.
        # Expand the assembly courtyard to include the whole 12.5 mm stencil.
        '  (fp_rect (start -5.7 -6.5) (end 5.7 6.5)',
        '    (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))',
        '  (fp_text reference "REF**" (at 0 -7.1) (layer "F.SilkS")',
        '    (effects (font (size 1 1) (thickness 0.15))))',
    ]
    # Figure 30: outer lands 0.7 wide, inner lands 0.8 wide; the outer
    # inter-pad gaps are 0.35 and the six inner gaps are 0.3. Pin 1 is at
    # bottom-left in the manufacturer's top-view drawing.
    x_positions = (-4.4, -3.3, -2.2, -1.1, 0.0, 1.1, 2.2, 3.3, 4.4)
    for row in (0, 1):
        y = 4.75 if row == 0 else -4.75
        for column, x in enumerate(x_positions):
            number = column + 1 if row == 0 else 18 - column
            width = 0.7 if column in (0, 8) else 0.8
            neck = 0.5 if column in (0, 8) else 0.6
            lines.extend((
                f'  (pad "{number}" smd rect (at {x:g} {y:g})'
                f' (size {width:g} 1.8) (layers "F.Cu" "F.Mask"))',
                # Figure 31: 1.4 mm full-width outer and 0.9 mm narrow inner
                # paste rectangles meet at the package edge to form a T.
                f'  (pad "" smd rect (at {x:g} {5.55 if row == 0 else -5.55:g})'
                f' (size {width:g} 1.4) (layers "F.Paste"))',
                f'  (pad "" smd rect (at {x:g} {4.4 if row == 0 else -4.4:g})'
                f' (size {neck:g} 0.9) (layers "F.Paste"))',
            ))
    lines.append(')')
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(render(), encoding="utf-8")
    print(DESTINATION)
