# Full-vertical acceptance package

This package contains the reusable CopperScript definitions currently needed
by CopperScript's `FullVerticalTracker` integration design. It is the canonical
home for those definitions; the compiler repository consumes the package by
its stable CopperLib import path.

The package is **not production-publishable**. Several definitions are bounded
electrical subsets, and generic support entries such as the regulator, UART
translator, choke, connectors, LED and button still require exact orderable
part selections and evidence-backed footprints. Every such file is labelled as
a prototype. Moving it here avoids duplicate models; it does not promote an
illustrative definition to verified status.

Import path:

```copper
import vertical "github.com/andenore/CopperLib/packages/full_vertical";
```

Before this package can be released, each orderable part must have complete
pin coverage, official-source evidence with precise revision/location, and a
verified footprint. The existing CopperLib publication gate remains the
authority for that transition.
