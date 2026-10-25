"""Regenerate the two sourced socket views and footprints; --check is read-only."""
from pathlib import Path
import json, sys, tempfile
real=Path(__file__).resolve().parent
facts=json.loads((real/'evidence/connector.json').read_text())
urls={k:v['url'] for k,v in facts['sources'].items()}
derived={'left':[], 'right':[]}
temporary=tempfile.TemporaryDirectory()
pkg=Path(temporary.name) if '--check' in sys.argv else real
(pkg/'footprints').mkdir(exist_ok=True)
left = [('G1',1),('G3',3),('G5',5),('G7',7),('G9',9),('GND',11),('VIN_5V',13),('G13',15),('G15',17)]
right = [('V3V3',28),('G43',26),('G44',24),('EN',22),('G0',20),('GND',18)]
for side, pins, count, y0 in [('left',left,9,-10.16),('right',right,6,-2.54)]:
 for n,(signal,mpad) in enumerate(pins,1):
  derived[side].append({'socket_pin':n,'module_pad':mpad,'signal':signal,'x_mm':'-7.62' if side=='left' else '7.62','y_mm':f'{y0+(n-1)*2.54:.2f}'})
 name=f'HCTL_PM254_1_{count:02}_Z_8_5'
 # HCTL Rev A specifies 1.02 mm finished holes, 2.54 mm pitch and 2.50 mm body width.
 # Copper annulus and courtyard are authored: 2.0 mm land, 0.25 mm courtyard beyond max body.
 last=(count-1)*2.54
 fp=[f'(footprint "{name}" (version 20240108) (generator "copperlib") (layer "F.Cu")',
     '  (attr through_hole)',
     f'  (fp_rect (start -1.25 -1.47) (end 1.25 {last+1.47:.2f}) (stroke (width 0.1) (type default)) (layer "F.Fab"))',
     f'  (fp_rect (start -1.60 -1.87) (end 1.60 {last+1.87:.2f}) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))',
     f'  (fp_rect (start -1.45 -1.67) (end 1.45 {last+1.67:.2f}) (stroke (width 0.12) (type default)) (layer "F.SilkS"))',
     '  (fp_line (start -1.45 -1.67) (end -1.45 0.8) (stroke (width 0.25) (type default)) (layer "F.SilkS"))']
 for n in range(1,count+1):
  fp.append(f'  (pad "{n}" thru_hole {"rect" if n==1 else "circle"} (at 0 {(n-1)*2.54:.2f}) (size 2 2) (drill 1.02) (layers "*.Cu" "*.Mask"))')
 fp.append(')')
 (pkg/f'footprints/{name}.kicad_mod').write_text('\n'.join(fp)+'\n')
 lines=[f'// Stamp-S3 carrier contact view of HCTL PM254-1-{count:02}-Z-8.5.',
        '// Socket numbering is top-to-bottom; not the module 1.27 mm pad numbering.',
        f'part STAMP_S3_SOCKET_{side.upper()} {{',
        '    category = "connector.module.stamp_s3";',
        '    manufacturer = "HCTL";',
        f'    footprint = "footprints/{name}.kicad_mod";',
        '    source_document = "M5StampS3 schematic v0.2, M1; HCTL PM254 Rev A";',
        '    source_location = "M1 pads 1,3,5,7,9,11,13,15,17 / 28,26,24,22,20,18; evidence/connector.json";',
        f'    source_url = "{urls["Stamp-S3-schematic.pdf"]}";',
        f'    source_checksum = "sha256:{facts["sources"]["Stamp-S3-schematic.pdf"]["sha256"]}";']
 for n,(sig,mpad) in enumerate(pins,1):
  domain='ground' if sig=='GND' else 'power' if sig in ('VIN_5V','V3V3') else 'digital'
  required='required' if sig in ('VIN_5V','GND') else 'optional'
  # Exact guaranteed 5V tolerance is not supplied by M5Stack; do not invent limits.
  lines.append(f'    pin {sig} {{ number = "{n}"; domains = "{domain}"; directions = "passive"; connection = "{required}"; }}')
 lines.append('}')
 (pkg/f'{side}.copper').write_text('\n'.join(lines)+'\n')

assert all(derived[s]==facts[s] for s in ('left','right'))
if '--check' in sys.argv:
    for p in pkg.rglob('*'):
        if p.is_file():
            assert p.read_bytes()==(real/p.relative_to(pkg)).read_bytes(), str(p)
    print('Stamp-S3 socket sources are current')
temporary.cleanup()
