# Hard-macro review checklist

Use this when adding or revising a physical hard macro in CopperLib. A passing
connectivity/DRC trial does not qualify electrical, thermal, EMI or assembly
performance.

## Required review when adding components

These checks apply before deciding whether to create a hard macro, including
standalone part additions. A standalone part can leave board-specific geometry
to its host, but must document the required support circuit and physical layout
obligations. Do not hide missing layout work behind a valid pin map or ERC pass.

- **RF matching and reference layout.** For every RF-capable component, inspect
  the exact manufacturer reference schematic and layout for its package,
  operating band and intended antenna/interface. Explicitly record whether
  chip-side matching, a balun, antenna tuning, filters or other support are
  required or integrated. A nominal 50-ohm module port is not evidence that the
  board antenna needs no matching. If no external network is needed, record
  the source-backed reason; unknown requirements remain unresolved.
- **Constrain RF-critical geometry.** Preserve matching topology and prescribed
  ground returns. Encode reference-backed pin-to-component distances, relative
  poses/orientations, short routes, layer/impedance requirements, return vias
  and antenna copper/component keepouts. Prefer a reviewed hard macro when
  placement alone cannot preserve the required copper. Do not invent universal
  distance limits or copy matching values to a different package, antenna or
  stackup without review.
- **Switching supplies: macro first.** For switching regulators, converters and
  switching chargers, ideally generate a hard macro from the applicable
  manufacturer reference layout, preserving critical placement and copper.
  Include local capacitors, inductor and other topology-specific support,
  high-di/dt current/return loops, switching-node geometry, quiet feedback/sense
  paths and thermal/ground connections. Record package, topology and operating
  conditions, and distinguish authored adaptations from extracted vendor CAD.
- **Strong fallback contract.** If a macro is unavailable or unsuitable,
  require explicit, source-backed placement/orientation and pin-relative
  distance limits plus trace widths or conductor geometry for each critical
  power/current path. Review peak/RMS current, copper thickness, temperature
  rise, voltage drop, pad-entry neckdowns and via capacity; do not apply one
  arbitrary wide trace to every net. Bound critical route/loop geometry and
  isolate feedback from switching copper. Soft placement groups, component
  centre distances alone, or board-default widths do not satisfy this contract.
- **Enforcement and evidence.** Check generated placement and routed geometry
  against the contract. Add regression checks for enforceable requirements;
  explicitly list unsupported constraints and require manual review of those
  gaps before qualification. Never silently weaken a limit to make placement
  or routing pass. Retain manufacturer revision/page/figure locators and
  hashes with the part/circuit evidence.

## Macro asset review

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
  that host routing and fill cannot bypass a prescribed local return. Use
  fixed netted polygons for prescribed conductor shapes and zones for copper
  that must refill around neighboring objects; inspect both after native DRC.
- **Test the contract.** Regenerate the asset deterministically; test permitted
  rotations and variants, lost or altered owner copper, wrong pad/net bindings,
  prohibited shortcuts, external port access, independent native refill and
  zero opens/violations. Add geometry checks for the actual loop/sense risk,
  rather than tests that merely restate the generator coordinates.
- **State the qualification boundary.** List unresolved current, control-loop,
  EMI, thermal, laminate, assembly and part-selection evidence. Keep an
  unqualified macro marked `production_publishable = false`; native DRC alone
  is not a release decision.
