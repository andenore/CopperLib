# Package ownership and contributions

CopperLib is one independently versioned CopperScript library provider. Each
reusable definition has one canonical home; search declared dependencies before
adding a duplicate. Keep the module identity `github.com/andenore/CopperLib`.

| Content | Owner |
| --- | --- |
| Exact manufacturer parts, package pin maps and terminal facts | `packages/parts/<vendor>/<family>/` |
| Honest generic passive/header templates | `packages/generic/` |
| Reusable circuit topology, matching/support and physical contracts | `packages/circuits/` |
| Standard protocol/harness interfaces | `packages/interfaces/` |
| Reusable board/mounting profiles | `packages/profiles/` |
| Source evidence, custom footprints, qualification and generated macro assets | Beside the owning package |
| Application GPIO assignments, operating configuration, power tree, placement, stackup, BOM/CPL, measurements | Consumer project |
| Compiler algorithms, model-gap research and parser fixtures | CopperScript |

Use stable lowercase package paths and one electrical definition per identity.
Related package variants may share a device model. Importable directories contain
only intended public definitions; evidence and alternative fixtures belong in
child directories. `catalog.json` indexes actual exports, scope and limitations;
it must not establish qualification through category or folder names.

Custom footprints resolve relative to their declaring source. Standard KiCad
assets use explicit managed providers. Consumers declare and lock required
providers; automatic transitive version selection is not established. Do not
create parallel canonical geometry under repository-wide footprint directories.
Generators and their outputs must be deterministic and reviewed together.

The standalone Johanson antenna and the nRF52832/Johanson RF circuit remain
separate reusable definitions with canonical dependencies. Preserve the RF
trial's six-layer contract, isolated antenna land, immutable copper, protected
returns and exact bindings. Layer/antenna/package changes require separately
reviewed adaptations; a renamed assembly is not a complete operational radio.
The library owns topology, reference facts and supported variants; the board
owns selected conditions, enclosure, tuning and measurement evidence.

Configured translator directions and connector harness pin meanings are
interface views, not universal silicon or connector facts. Package READMEs and
qualification contracts carry unresolved obligations after import or migration.

Version public imports through the consumer's `copper.mod` and `copper.lock`.
Old pinned revisions keep their old paths; do not assume transparent re-export
aliases. A package move must preserve electrical meaning, footprint geometry,
source hashes and contract limits, with deliberately updated identity bindings.
Run the full test suite before committing a library change. Follow
[engineering contracts](engineering-contracts.md),
[RF/power review](hard-macro-review-checklist.md) and
[internal pad connectivity](../internal-pad-connectivity.md) for relevant work.
