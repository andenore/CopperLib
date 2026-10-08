# Hard-macro review checklist

Use this when adding or revising a physical hard macro in CopperLib. A passing
connectivity/DRC trial does not qualify electrical, thermal, EMI or assembly
performance.

- **Choose the right scope.** Identify components that generate noise or are
  sensitive to it. For switched regulators, RF circuits, precision analog
  front ends and similar layouts, prefer a hard macro derived from an official
  manufacturer reference layout when one exists. Preserve the electrically
  important placement, current/return loops, sense paths and keepouts; record
  every adaptation instead of claiming that an authored layout is vendor CAD.
- **Pin the evidence.** Record the exact official source URL, revision, page or
  figure, and content hash. Distinguish extracted copper from traced artwork,
  schematic-derived placement and wholly authored geometry. Keep source files
  in ignored `cache/`, not the package bundle.
- **Bind the real parts.** Check every physical land against the package data,
  including repeated numbers and isolated contacts. Pin member footprint
  identities and verify exact capacitor/inductor values, ratings, tolerance and
  effective capacitance under operating bias where relevant.
- **Review physical behavior.** Inspect the high-di/dt and high-dv/dt loops,
  switching-node extent, local ground vias and plane continuity, quiet sense/
  feedback routing, thermal path, port entry and the host-board stackup. For a
  layout adaptation, compare all relevant copper layers with the reference.
- **Keep ownership explicit.** Declare local copper, ports, protected routing
  regions and fill exclusions separately. Do not use a zone outline, shared
  logical pad number or net name as proof of physical connectivity. Confirm
  that host routing and fill cannot bypass a prescribed local return.
- **Test the contract.** Regenerate the asset deterministically; test permitted
  rotations and variants, lost or altered owner copper, wrong pad/net bindings,
  prohibited shortcuts, external port access, independent native refill and
  zero opens/violations. Add geometry checks for the actual loop/sense risk,
  rather than tests that merely restate the generator coordinates.
- **State the qualification boundary.** List unresolved current, control-loop,
  EMI, thermal, laminate, assembly and part-selection evidence. Keep an
  unqualified macro marked `production_publishable = false`; native DRC alone
  is not a release decision.
