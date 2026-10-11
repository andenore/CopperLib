# Agent guidance

Start with `copper agent-guide` in the active CopperScript environment, then
request the `libraries` topic and selected contracts. Read only the owning
package's definitions/evidence and the task-specific reference below. CopperLib
is one provider; other libraries use the same discovery and contract interfaces.

- Follow [package ownership](docs/package-layout.md). Keep compiler algorithms
  and model-gap labs in CopperScript and board-specific bindings/measurements in
  consumers. Search dependencies before adding duplicate definitions. Do not
  add components to CopperLib as part of the current LLM improvement work.
- Preserve exact source facts and locators; unknown pins, limits or mux facts
  use `?` and unresolved evidence. Downloaded sources belong in ignored `cache/`;
  commit compact evidence/manifests/hashes and never execute source-provided code.
- For RF or switched-power additions/changes, follow the
  [hard-macro review checklist](docs/hard-macro-review-checklist.md) and exact
  manufacturer schematic/layout. Preserve matching/support, critical copper,
  returns and keepouts; unresolved adaptations prevent production qualification.
- Mark true bypass capacitors with `role = decoupling; decouples = "U.PIN";`.
  Do not infer roles for RF/load/bulk capacitors or forbid necessary ground vias.
- Follow [engineering contracts](docs/engineering-contracts.md) for reusable
  obligations and [internal pad connectivity](internal-pad-connectivity.md)
  for manufacturer-established permanent joins. Duplicate pad numbers alone are
  not evidence; externally required power/thermal contacts still need routing.
- Keep generated files deterministic and run `python -m pytest` before committing.
  ERC/DRC or illustrative values cannot establish production publishability.
