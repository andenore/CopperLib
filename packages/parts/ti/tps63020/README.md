# TPS63020DSJR (provisional component model)

Export `TPS63020DSJR`, with package-owned TI DSJ0014 land pattern. TI TPS6302x
datasheet SLVS916I, pin functions p4, section 8, mechanical drawings pp31-33:
https://www.ti.com/lit/ds/symlink/tps63020.pdf
SHA256 `d117773bb7370fd79377bc70ce987eec3469ea5979547a09df52fca5f95b2e69`.
Pins 1-14 remain separate; central/comb PGND contacts are pad 15. Six unnumbered
paste-only apertures are not electrical contacts. Review stencil and thermals.

This is a part, not a qualified converter circuit or physical hard macro.
Consumers must select/qualify inductors, effective input/output capacitance,
feedback and operating limits, and supply a source-backed reference layout macro
or strong placement **and conductor-width/current-path** constraints. Preserve
short switching/current-return loops, quiet feedback, local decoupling and
thermal/ground paths. Inspect pad neckdowns and via capacity.

The first tracker consumer's numerical proximity limits are provisional board
intent, not vendor-certified limits or a reusable layout contract. A reviewed
TPS63020 macro, route/current dimensions and low-battery transient/thermal
qualification remain open. Do not publish this model as production-qualified.
