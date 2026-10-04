# CopperLib reorganization plan

Status: proposed; implementation has not started.

## 1. Objective and agreed scope

CopperLib is a generic, reusable hardware library. Organize its public packages
by component identity, reusable circuit function, and standard interface/profile.
A project name must not determine where a generally reusable component lives.
Keep the module identity `github.com/andenore/CopperLib`.

**The antenna stays in CopperLib.** Retain both the standalone Johanson
2450AT18A0100001E component and the reusable nRF52832/Johanson RF assembly,
including its matching components, placement reference, physical hard macro,
source evidence, generator and checks. The assembly imports the canonical chip
and antenna definitions; it does not maintain another copy of either part.

The existing RF assembly remains explicitly experimental. Its current file
records adapted Johanson geometry, six required copper layers, incomplete MCU
support, and unresolved impedance/tuning assumptions. Reorganization preserves
those facts. It does not establish that its matching values or layout work on
arbitrary boards.

This work covers package organization, ownership, documentation, generators,
validation and migration of current CopperScript consumers. New radio design,
RF qualification, completion of device models and new compiler features are
separate engineering work.

## 2. Ownership rules

| Content | Owner |
| --- | --- |
| Chip/device capabilities, orderable package pin maps, terminal identities | CopperLib component package |
| Genuine generic passive/header templates | CopperLib generic package |
| Custom footprint, source hashes/locators, concise evidence, reusable simulation model | The relevant CopperLib part/circuit package |
| Reusable matching network, antenna assembly, manufacturer reference circuit and its physical contract | CopperLib circuit package |
| Standard SWD pin assignment or CM4 socket/mounting contract | CopperLib interface/profile package |
| Tracker-specific power-tree composition, board outline, chosen carrier cutout, application GPIO assignment, BOM offers | Consuming board project |
| Application-specific circuit binding, placement scene, routing output, simulation plan and results | Consuming board project |
| Compiler model-gap studies, bounded generation proofs and parser fixtures | CopperScript development/test tooling |

Application bindings belong to the project; the reusable RF assembly and its
antenna geometry belong to CopperLib. A project may select an explicit library
variant or supply supported overrides, while satisfying that variant's contract.

Each component identity has one canonical electrical definition. Related package
variants may share a device definition in one family package. Contextual standard
interfaces are separate from the underlying connector's manufacturer identity.
Evidence/coverage determines model status independently of the folder name.

## 3. Target layout

```text
CopperLib/
  copper.mod
  README.md
  AGENTS.md
  catalog.json
  packages/
    parts/
      nordic/nrf52832/
        device.copper
        nrf52832_qfaa.copper
        evidence/
      st/stm32g0c1/
      ti/tps62130/
      ti/tusb320/
      ti/tcan334/
      st/lis2dw12/
      quectel/eg800g/
        footprints/
        evidence/
      u_blox/max_m10s/
      johanson/2450at18a0100001e/
      keystone/3034/
      samtec/ftsh_105_01_l_dv_007_k/
      gct/usb4135/
      gct/sim8060/
      coilcraft/0603usb/
      coilcraft/xal4020/
      samsung/cl05/
      samsung/cl10/
      fenghua/0402cg/
      uniroyal/0603waf/
      kento/kt0603r/
    generic/
      passives/
      headers/
    circuits/
      nordic/nrf52832_johanson_reference/
        README.md
        # Reusable electrical definitions as supported by the current compiler.
        assets/
          nordic_qfaa_ldo_reference.json
          nrf52832_johanson_six_layer_trial.json
        evidence/
      ti/tps62130_reference/
    interfaces/
      arm/swd_10pin/
    profiles/
      raspberry_pi/cm4/
  tools/
    generate/
    acquire/
  tests/
    parts/
    circuits/
    profiles/
    fixtures/
  docs/
    contributing.md
    package-layout.md
    reorganization-plan.md
```

Directory names are lowercase and stable. Public imports continue to select
packages; `copper.mod` selects the module revision. An example future import is:

```copper
import nordic "github.com/andenore/CopperLib/packages/parts/nordic/nrf52832";
import antenna "github.com/andenore/CopperLib/packages/parts/johanson/2450at18a0100001e";
```

Every importable directory contains only its intended public definitions. Keep
evidence and non-source assets in child directories, so the compiler does not
mistake a fixture or alternative circuit for a public export.

Custom geometry belongs beside its owning part and uses declaring-file-relative
footprint paths. Standard KiCad geometry uses explicit managed providers. Document
provider requirements and bind them in consumer manifests; the current resolver
does not automatically select transitive provider versions from CopperLib.
Avoid parallel canonical copies in a repository-wide `footprints/` directory.

`catalog.json` is a proposed library index, not a new CopperScript language
feature. Initially record public import paths, exported identities, categories,
model coverage/limitations, evidence locations and footprint dependencies.
Validate that entries match actual exports and retain explicit provisional,
template or experimental-reference status where appropriate. Category browsing
should come from this index rather than duplicating files under category trees.

## 4. Concrete migration map

| Current area | Destination/action |
| --- | --- |
| `packages/full_vertical/nrf52832_*` | `packages/parts/nordic/nrf52832` |
| `packages/full_vertical/stm32g0c1*` | `packages/parts/st/stm32g0c1` |
| TI regulators/controllers/transceivers, LIS2DW12, EG800G, MAX-M10S, GCT connectors, Coilcraft parts | Their manufacturer/family packages |
| `packages/full_vertical/rf_antenna.copper` | Canonical Johanson antenna package; preserve FEED=1 and isolated NC=2 |
| `packages/nrf52_demo/cr2032_holder.copper` | `packages/parts/keystone/3034`; preserve permanent positive-tab connectivity |
| Exact parts in `packages/assembly_basics` | Manufacturer/family packages; preserve KENTO A=1/K=2 and its custom footprint |
| `packages/full_vertical/power_tree.copper` | CopperScript's full-vertical example modules; extract reusable regulator reference circuitry separately |
| Prototype UART translator and open-drain driver | Project/example fixtures until real, evidence-backed devices are selected |
| Reference LED/crystal and application-labelled generic connectors | Move placeholders into example fixtures; retain only honest, reusable templates in `packages/generic` |
| `SWD_HEADER` and Samtec custom geometry | Component identity under Samtec; standard protocol mapping under `interfaces/arm/swd_10pin` |
| `packages/raspberry_pi_cm4` | Reusable CM4 mappings/mounting under `profiles/raspberry_pi/cm4`; separate generic header definitions |
| `data/full-vertical/rf-audit.json` | Split/relocate evidence to the Nordic circuit and Johanson part, preserving original sources/locators |
| `data/full-vertical/usb-choke-audit.json` | Coilcraft choke evidence; preserve verified winding pairs and polarity |
| `nrf52832-qfaa-rf-reference.json` | Nordic circuit `assets/nordic_qfaa_ldo_reference.json` |
| `nrf-antenna-hard-macro.json` and its README/generator | Nordic/Johanson circuit `assets/nrf52832_johanson_six_layer_trial.json`, documentation and generator |
| `data/cm4` and CM4 generator | CM4 profile evidence and shared generation tools |
| `copperscript_stm32g0`, `data/case-studies`, compatibility reports, proof work packets and incomplete `generated/stm32g0b1*` | CopperScript development/test tooling, with its own fixtures and deterministic checks |

Move concise part evidence with the part even when it was originally gathered
for a particular board. Preserve all referenced checksums and source locations.
Raw vendor downloads remain ignored local cache content. Move model-gap tooling
only after its destination tests and reports reproduce the existing results.

The first structural pass may retain existing contextual CM4/SWD exports in
their new interface/profile packages. Sharing underlying manufacturer facts must
not require invented alias/re-export syntax or unsupported compiler composition.
Any necessary language work needs a separate explicit proposal.

## 5. nRF52832 and antenna assembly contract

The circuit package must be useful from both the coin-cell and tracker examples.
It includes:

1. The canonical nRF52832-QFAA and Johanson antenna dependencies.
2. The existing chip-side matching network and antenna-side matching network,
   with component roles and electrical connectivity recorded explicitly.
3. The manufacturer reference placement packet and the existing seven-member
   physical trial, retaining footprint digests, protected copper, keepouts,
   pad/net bindings, allowed transforms and source evidence.
4. A documented binding contract for a consuming board. The initial migration
   may preserve explicit component bindings; introducing a combined electrical
   wrapper must avoid creating a second chip or antenna instance.
5. Tests proving the antenna NC land stays isolated, RF pad/net mapping remains
   correct, and binding/materialization preserve the retained copper.

Keep the existing six-layer physical trial as a named variant. Do not advertise
it as layer-independent or silently adapt its vias/plane references to a
2-layer or 4-layer board. A new variant requires its own evidence and checks.

### Library-owned versus board-owned choices

The library owns reusable topology, terminal facts, reference values, physical
assets and each variant's required placement/clearance/layer assumptions. The
board owns the selected variant, global placement, board outline, actual
stackup/laminate, enclosure, application pin configuration and resulting tuning.
A reference value can remain in the library with its provenance and limitation;
it must not be presented as an already tuned value for every board.

A binding must validate every requirement representable by today's compiler
and fail explicitly on known mismatches. Document RF requirements that still
need engineering review. Do not invent an automatic impedance/tuning validator
as part of this file reorganization.

The initial package describes the retained RF assembly. Complete power,
clock/crystal and decoupling support remains a separately visible completion
item wherever existing facts are incomplete; its name/docs must not imply a
complete operational radio or a production-qualified module.

## 6. Implementation phases

### Phase A — Inventory and freeze the migration contract

- [ ] List every public export, consumer, footprint and hashed physical asset.
- [ ] Record one destination per definition and identify actual duplicates.
- [ ] Capture baseline electrical connectivity, pin/bond maps, internal contact
      groups, pad geometry and RF trial outputs.
- [ ] Record compatible compiler/library revisions and all provider pins.
- [ ] Define catalog coverage/status fields and the public package naming rules.

### Phase B — Establish canonical components

- [ ] Move manufacturer parts and shared device definitions into family packages.
- [ ] Relocate concise evidence, custom footprints and component generators.
- [ ] Update declaring-file-relative paths and generator output destinations.
- [ ] Separate genuine generic templates from illustrative example fixtures.
- [ ] Populate and validate the catalog; add part-level import/geometry tests.

### Phase C — Retain reusable circuits, including the antenna

- [ ] Publish the Nordic/Johanson circuit package with both reference and trial
      assets, documented electrical/physical roles and explicit variant limits.
- [ ] Move its generator and RF checks; preserve deterministic retained geometry.
- [ ] Keep the standalone antenna and chip importable independently.
- [ ] Separate reusable TPS62130 reference circuitry from tracker power policy.
- [ ] Organize SWD and CM4 standard contracts and their shared component facts.
- [ ] Verify antenna-containing consumers instantiate one chip and one antenna
      and preserve their original electrical and macro bindings.

### Phase D — Migrate consumers and research tooling

- [ ] Update full-vertical tracker, nRF antenna probe, nRF coin-cell, LED ring,
      mechanical-profile and CM4 examples to canonical imports/assets.
- [ ] Keep project modules, example placeholders and use-site scenes with their
      boards. Adopt library circuit exports where their supported API suffices.
- [ ] Update generator scripts, tests, Make configuration and current guides.
- [ ] Move compatibility research/proofs into CopperScript development tooling;
      run the old compatibility checks until the replacement reproduces them.
- [ ] Update CopperLib CI around catalog, component, circuit/profile and
      deterministic generation checks, using a compatible pinned compiler.

### Phase E — Validate, publish and remove obsolete paths

- [ ] Run the complete CopperLib suite and deterministic generators.
- [ ] Verify representative library imports and physical exports in fresh
      consumer projects, including managed footprint dependencies.
- [ ] Confirm cache preparation, `--locked` and `--locked --offline` behavior.
- [ ] Publish the new CopperLib revision before pinning it in CopperScript.
- [ ] Regenerate both the root CopperScript lock and the independent CM4 lock;
      update affected scene/asset digests deliberately.
- [ ] Run affected CopperScript checks and its full suite against the new pin.
- [ ] Inspect native KiCad RF exports for retained copper/keepouts and isolated
      antenna land, without treating DRC as RF qualification.
- [ ] Remove old `full_vertical`, `nrf52_demo` and `assembly_basics` bundles after
      all active consumers have migrated; rewrite the library README.

Use incremental commits: canonical components, retained circuits/profiles,
consumer migration, research-tool migration, then obsolete-path removal.
Reorganization changes import identities and therefore some provenance/digests.
Compare electrical meaning and physical geometry after normalizing intended
namespace/path changes; do not silently bless unexpected model changes.

## 7. Compatibility and completion criteria

Existing consumers pinned to an earlier Git revision keep using that revision.
New public paths ship in a new immutable revision. Do not assume CopperScript
supports transparent re-export aliases. If a temporary old package is necessary,
generate it from canonical sources, test equivalence, assign a removal milestone,
and avoid independently maintained duplicate models.

Cleanup is complete when:

- [ ] Each reusable part has one canonical home independent of its first board.
- [ ] No public component package is named after the tracker or demo project.
- [ ] The Johanson antenna and the antenna-inclusive nRF52832 RF circuit are
      both available, with clear dependencies and preserved evidence/geometry.
- [ ] Manufacturer facts, generic templates and experimental circuit variants
      have explicit, accurate coverage/status descriptions.
- [ ] Custom footprints resolve from their owning packages; external geometry
      uses documented pinned providers and fresh consumers need no sibling repo.
- [ ] Project-specific policy/outputs and compiler research fixtures have their
      intended owners; generators and tests remain deterministic.
- [ ] Current consumers pass electrical, footprint, macro and applicable native
      checks against the published library revision.
- [ ] README/catalog/docs describe the generic library and its public imports.

**RF tuning and production qualification remain separate from cleanup
completion.** Preserve the existing unresolved work rather than deleting it or
promoting the experimental assembly through a rename.
