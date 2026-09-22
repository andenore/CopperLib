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

The nRF52832-QFAA now has all 48 numbered QFN pins plus the exposed ground
pad bonded from the Nordic Product Specification v1.9 pin-assignment table.
This resolves its package-to-footprint number audit only; the board still lacks
the complete crystal/decoupling/reference circuit, so this is not a production
approval of the Bluetooth subsystem.

The STM32G0C1RET6 now has all 64 standard LQFP64-GP bonds from DS13564
Rev 5, Table 12. The board connects its VBAT and VREF+ supply pins, but the
MCU reference circuit, crystal/clock choice, and all vendor decoupling remain
to be completed and reviewed before production.

The nano-SIM connector is now the orderable GCT SIM8060-6-0-14-00-A (without
card detect), with I/O correctly on C7 and all four shell pads grounded. Its
installed KiCad 10 footprint includes embedded copper keepouts; CopperScript's
footprint importer must represent those keepouts before this asset can pass
the physical audit.

Import path:

```copper
import vertical "github.com/andenore/CopperLib/packages/full_vertical";
```

Before this package can be released, each orderable part must have complete
pin coverage, official-source evidence with precise revision/location, and a
verified footprint. The existing CopperLib publication gate remains the
authority for that transition.
