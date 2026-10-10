# Reusable components extracted from CopperAssetTracker

These definitions, five custom footprints and the SIMCom footprint converter
were moved out of CopperAssetTracker on 2026-10-09. They retain their provisional
qualification status; moving them into CopperLib does not approve them for
production. No new schematic topology or copper geometry was introduced.

| Public package (under `github.com/andenore/CopperLib/packages/`) | Exports / scope |
| --- | --- |
| `parts/simcom/sim7670g-lngv` | `SIM7670G_LNGV`, 124-land footprint and converter |
| `parts/ti/tps63020` | `TPS63020DSJR`, DSJ0014 footprint |
| `parts/bourns/srp4020ta` | `SRP4020TA_1R5M`, power-inductor footprint |
| `parts/ti/sn74axc2t245` | `MODEM_UART_TRANSLATOR`, `MODEM_STATUS_TRANSLATOR`: configured views of SN74AXC2T245RSWR |
| `parts/onsemi/bss138` | `BSS138`: low-current open-drain driver view |
| `parts/ti/tcan334g` | Added exact `TCAN334GDR` SOIC variant; existing VSSOP model unchanged |
| `parts/yxc/ysx321sl` | Added `YXC_X322532MOB4SI` 32 MHz variant; existing 25 MHz model unchanged |
| `parts/e-switch/tl3342` | `TL3342F160QG`, exact identity corresponding to the existing generic button template |
| `parts/hirose/u-fl` | `U_FL_R_SMT_1`, exact identity corresponding to the generic RF connector template |
| `parts/jst/xh-sm4` | `JST_S3B_XH_SM4_TB` battery/NTC view; owns three- and four-pin SMT XH footprints |
| `interfaces/can/jst-xh3` | `CAN_HEADER`: CANH/CANL/GND convention, using the shared three-pin footprint |
| `interfaces/uart/jst-xh4` | `DEBUG_HEADER`: VREF/TX/RX/GND convention, using the shared four-pin footprint |

The JST battery export preserves its existing P1=power, P2=ground, P3=analog
model convention. That is a selected harness interface, not an inherent
electrical property or universal pinout of an XH connector. Similarly the
translator directions and voltage annotations are configured interface views,
not a complete configurable silicon model. Review bindings before reuse.

The tracker keeps only its application-specific `AssetTrackerPowerTree` module:
chosen 3.3/3.8 V rails, charger settings, modem enable and pack wiring. It imports
the shared parts; board placement, routing constraints, BOM selections and
procurement history also remain project-owned.

Component evidence and host-layout obligations are in the owning package
READMEs. The modem's exact hardware-guide/matching review and TPS63020 reference
layout/hard macro remain open. Do not treat imported part definitions, successful
ERC or a package migration as RF or switched-power layout qualification.

The consuming project's `copper.mod` uses an explicit `../CopperLib` development
replacement and a refreshed content-inventory lock. The additions are not yet
published. Publish a reviewed library revision, then update its `require`, remove
the replacement and regenerate the project lock before claiming a standalone
remote build.
