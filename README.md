# CopperLib

**Reusable engineering definitions for PCB design as code.**

[CopperScript website](https://andenore.github.io/CopperScript/) ·
[Language and compiler](https://github.com/andenore/CopperScript) ·
[Complete board example](https://github.com/andenore/CopperAssetTracker)

CopperLib is the generic, provenance-first catalogue of reusable CopperScript
parts, interfaces, mechanical/stackup profiles and circuit modules. Board-specific examples and
device-model research live in the sibling CopperScript repository.

The repository contains source-backed definitions and compact evidence. Each
package documents its own unresolved items; incomplete definitions are not
silently presented as production-qualified parts.

## Part of the CopperScript workflow

[CopperScript](https://github.com/andenore/CopperScript) describes PCB connections,
electrical intent and physical constraints in typed source. CopperLib supplies
versioned building blocks; the compiler resolves their interfaces, footprints
and supported contracts into inspectable outputs and native KiCad boards.

[CopperAssetTracker](https://github.com/andenore/CopperAssetTracker) demonstrates
the composition of these definitions into a cellular, GNSS and Bluetooth board.
Its routed candidate remains a review design; see its
[current qualification status](https://github.com/andenore/CopperAssetTracker/blob/main/docs/validation.md).
Application configuration and board-specific measurements stay in the consumer
repository. Generic compiler algorithms stay in CopperScript.

## Mechanical profiles and physical contracts

CopperLib also supplies reusable mechanical definitions. The
[CM4 mounting profile](packages/profiles/raspberry_pi/cm4/README.md) contributes
four mounting holes, two connector pad-anchor poses and front-side placement
keepouts. A consumer binds its own connector components to the profile's roles
and supplies its carrier outline and application-specific clearance requirements.
The profile creates no electrical components or nets.

CopperScript expands these profiles into mechanical geometry with source
provenance, then uses supported constraints for placement and physical checks.
Its [mechanical editor](https://github.com/andenore/CopperScript/blob/main/docs/mechanical-editor.md)
lets the consumer review board-owned geometry and placement intent while imported
library definitions remain read-only. See
[profile syntax](https://github.com/andenore/CopperScript/blob/main/docs/mechanical-profiles.md)
and [placement/routing constraints](https://github.com/andenore/CopperScript/blob/main/docs/language-reference.md#constraints).
Package evidence and stated qualification limits still apply.

## Layout

```
packages/parts/        exact manufacturer parts grouped by vendor/family
packages/generic/      reference geometry and generic interfaces
packages/circuits/     reusable multi-part electrical assemblies
packages/interfaces/   debug, bus and harness interfaces
packages/profiles/     reusable board/profile geometry such as CM4
tools/generate/        package-local generation helpers and source readers
```

Packages are imported through stable URL-like paths rooted at
`github.com/andenore/CopperLib`. For example:

```copper
import nordic "github.com/andenore/CopperLib/packages/parts/nordic/nrf52832";
import rf "github.com/andenore/CopperLib/packages/circuits/nordic/nrf52832-johanson-reference";
component RADIO: rf.Nrf52832JohansonRf;
```

The nRF52832/Johanson package intentionally includes both the standalone
antenna part and the reusable antenna-inclusive RF circuit. Its physical trial
asset is kept beside that circuit under `assets/`, with explicit qualification
limits and source hashes.

The [TPS63020 buck-boost layout package](packages/circuits/ti/tps63020-buck-boost/README.md)
provides always-on and externally enabled six-layer physical hard macros with
owned switching/power copper, local feedback and explicit host ports. These
are source-backed authored adaptations, not production-qualified TI layouts.

The former STM32 model lab, board bundles and project support modules are not
part of this generic catalogue; CopperScript owns those examples and research
fixtures.

For contributions, start with [AGENTS.md](AGENTS.md) and
[package ownership](docs/package-layout.md), then read the owning package's
evidence and relevant [engineering contract](docs/engineering-contracts.md).
Modem, power, interface and connector definitions retain package-owned
footprints and provisional qualification status; application power policy
and selected board conditions remain consumer-owned.

Current package ownership and contracts are the guidance for new work;
completed migration narratives are recoverable from Git.