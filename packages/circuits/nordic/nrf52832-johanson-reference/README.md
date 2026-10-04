# nRF52832 and Johanson antenna reference circuit

This package keeps the reusable electrical assembly and its physical evidence
together without making either one a production-qualified radio module. The
`Nrf52832JohansonRf` module contains the Nordic QFAA, matching network and
Johanson 2450AT18A0100001E antenna:

```copper
import rf "github.com/andenore/CopperLib/packages/circuits/nordic/nrf52832-johanson-reference";
module RadioSection { component RADIO: rf.Nrf52832JohansonRf; }
```

`assets/nrf52832-johanson-six-layer-trial.json` is a pinned data-only physical
asset for CopperScript's `pcbir.hard_macro_trial` probe. It does not replace
the electrical part/device definitions and is not a production-qualified radio
module.

The seven-member trial retains Nordic QFAA LDO v1.1 matching Gerber strokes and
adds an adapted Johanson evaluation-style tee/corner arrangement. Its footprint
digests bind the installed KiCad assets. The antenna's mechanical NC land stays
isolated; ground contacts use off-pad vias, never implicit via-in-pad permission.
It remains unqualified for impedance, actual laminate/reference-ground geometry,
antenna tuning/enclosure and the complete powered Nordic support circuit.

Generate the physical trial from the locally cached identity-pinned Nordic
archive:

```powershell
python packages/circuits/nordic/nrf52832-johanson-reference/generate_trial.py \
  cache/rf-reference/nrf52832qfaxreflayoutv11.zip
```

The script verifies the archive and pick-and-place identities and selected
linear dark top-Gerber strokes. It never executes CAD files, fetches sources or
infers connectivity from unnamed Gerber artwork. Its bounded reader is not a
general Gerber importer. Electrical roles come from the reviewed reference
schematic/terminal definitions; unresolved adaptations are explicit in the JSON.

CopperScript's design contract, acceptance tests and limitations are documented
in `docs/physical-hard-macros.md` in the sibling compiler repository. The
matching reference extraction is written to
`assets/nordic-qfaa-ldo-reference.json`; it is evidence for the trial, not a
claim that the complete support circuit has been qualified.
