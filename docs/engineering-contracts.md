# Reusable RF, power and interface qualification contracts

Package-local `qualification.json` companion documents use CopperScript's
`copperscript-engineering-contract/v0.1` schema. They are data, not executable
agent skills or new Copper language syntax. Validation algorithms remain in
CopperScript (`engineering_qualification`, `rf_geometry`, `power_integrity`,
`cam_geometry`); do not copy them into this library or a board project.

The initial contracts cover the Nordic/Johanson reference circuit, TPS63020
buck-boost circuit, SIM7670G-LNGV, MAX-M10S and BQ24072. They retain mandatory
design, simulation and prototype evidence separately. Reuse does not imply
production approval. `production_publishable` remains false.

`packages/interfaces/usb/usb2-channel` adds a complete-channel `kind: interface`
contract. It identifies the protocol and preserves mandatory operating-mode,
layout, impedance, signal-integrity and prototype evidence. Pin the applicable
standard and review exact endpoints/inline components, firmware roles and VBUS
states. A USB 2.0 label does not establish high-speed operation. Board net/pad
selectors and operating requirements remain consumer-owned; graph/model code
stays in CopperScript. Do not treat a reviewed source catalog as a reviewed
consumer design or USB-IF certification.

Consumers bind scoped contracts to their own geometry/operating conditions.
Missing exact sources, matching review, stackup, effective capacitance/current
data or measurements remain incomplete. No guessed universal distances, trace
widths, antenna matching values or current ratings are supplied. The MAX-M10S
integration guide is pinned in its package's `integration-review.md`; datasheet
hash and consumer antenna/coexistence decisions remain unresolved, as does
exact-modem reference equivalence.
Nordic matching keepouts may deliberately exclude adjacent reference copper:
do not apply a generic solid-plane coverage rule to its chip matching network.

When adding a reusable RF or power component/circuit:

1. Follow `hard-macro-review-checklist.md` and the exact manufacturer references.
2. Add/update a package-local contract and source/revision/locator/hash evidence.
3. Preserve mandatory matching/impedance/prototype gates for RF and
   component-rating/current-capacity/layout/transient/prototype gates for power.
4. Put board-specific conditions, reference designators, coordinates, stackup and
   measurements in the consumer's engineering plan, never in this library.
5. Add schema/regression tests. Never replace a mandatory external qualification
   requirement with a simple arithmetic or component-centre-distance screen.

See CopperScript `docs/engineering-qualification.md` for commands, evidence and
qualification boundaries. Software verifies report identity and bindings, not
the truth of an external reviewer or laboratory attestation.
