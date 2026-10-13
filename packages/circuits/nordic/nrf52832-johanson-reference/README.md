# nRF52832 and Johanson antenna reference circuit

Use the [CopperLib hard-macro review checklist](../../../../docs/hard-macro-review-checklist.md)
when revising its physical asset.

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

## Managed-footprint corner contract

`assets/nrf52832-johanson-managed-corner.json` is the reusable managed-provider
adaptation (KiCad revision `7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd`).
Generate it with the command above plus `--managed`; the default output then
selects this separate asset, preserving the older installed-footprint trial.
Its v0.5 contract requires edges 0 and 1 of `antenna-corner` to coincide fully
with the host's outer board perimeter. A closed island, one-edge-only opening
or a centred 45-degree placement on a rectangular host is rejected. The host
must place the entire macro accordingly; do not move only the radiator.

Johanson 36S0021A Rev. 4.0 page 3 provides the two-edge-open 6500 um square
ground-clearance reference. The managed adaptation changes no local copper,
matching returns, isolated pads or layer exclusions. CopperScript checks host
geometry, not antenna tuning; evaluation tee values, actual laminate/feed
impedance, ground shape/via fence and enclosure performance remain unresolved.

## Copper macro exports

Import this package normally and bind a named layout:

```copper
import rf_layout "github.com/andenore/CopperLib/packages/circuits/nordic/nrf52832-johanson-reference";
physical_macro RADIO: rf_layout.NRF52832_JOHANSON_SIX_LAYER_TRIAL {
    // Explicit member and net mappings for existing circuitry.
}
```

- `NRF52832_JOHANSON_SIX_LAYER_TRIAL` preserves the source-compatible trial
  footprint set used by the nRF antenna and coin-cell examples.
- `NRF52832_JOHANSON_MANAGED_SIX_LAYER` preserves the reviewed managed footprint
  adaptation used by full-vertical and the active asset-tracker source.
- `NRF52832_JOHANSON_MANAGED_CORNER` additionally retains the existing reviewed
  two-edge opening contract used by the RF-layout board revision.

The `.copper` files are the current declarative authoring inputs. Members name
exact managed footprint URLs, while consumer manifests pin provider revisions.
All fixed geometry, pad roles, isolated contacts, transformations and evidence
locators survive the JSON-to-source migration. Legacy JSON assets and extraction
scripts remain historical compatibility/reference inputs. These exports remain
unqualified; they do not instantiate the electrical circuit.
