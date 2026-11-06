# 3D model coverage

Audit of 2026-11-06 against `kicad-footprints` 7ebfa6b (the provider revision
consumers lock) and `kicad-packages3D` 10.0.8. A part has a real body when its
`model` field, or the `(model ...)` of an imported stock KiCad footprint, names a
file that library ships; anything else gets the compiler's generated body (see
[package layout](package-layout.md)). A consumer still has to require
`kicad-packages3D` in its `copper.mod` for either to resolve.

Of 158 concrete parts (plus 3 footprint-less passive templates), 104 have a real
body: 30 through their own `model`, 74 through their footprint's own `(model ...)`. One of the 26,
`LM27761DSGR`, also depends on its footprint resolving (below).
The Stamp-S3 socket models are emitted by `packages/profiles/m5stack/stamp-s3/generate.py`.

`model` carries no offset or rotation, so a model was added only when the part's
footprint has the same origin and pad positions as the KiCad footprint the model
was made for (every lead and terminal pad within 0.15 mm), and the body matches the
package or its outline (noted beside the field).

## No usable KiCad model: needs a manufacturer STEP

The model would be added beside the part and named with a relative `model`.

| Part | Package | Why there is none |
|---|---|---|
| `JST_S2B_PH_SM4_TB`, `JST_S3B_PH_SM4_TB` | JST PH SM4-TB | KiCad's footprints name models the 3D library does not ship |
| `JST_S3B_XH_SM4_TB`, `CAN_HEADER`, `DEBUG_HEADER` | JST XH SM4-TB (3/4 pin) | as above |
| `SIM8060_6_0_14_00_A` | GCT SIM8060 nano-SIM | as above |
| `CM4_GPIO_SOCKET`, `CM4_HS_SOCKET` | Hirose DF40C-100DS-0.4V | as above |
| `GCT_USB4230_03_A` | GCT USB4230 | not in KiCad |
| `HIROSE_FH34SRJ_22S_0_5SH`, `GUOCONN_0_5K_GX_22PWB_R` | 22-pin 0.5 mm FPC | not in KiCad |
| `IPEX_20525_040E_02` | I-PEX 20525 | not in KiCad |
| `HR911130A` | Hanrun RJ45 with magnetics | not in KiCad (only HR911105A) |
| `MKDS_1_2_3_5`, `KF128_5_08_2P_AA` | Phoenix MKDS 1/2-3.5, KEFA KF128 | not in KiCad |
| `SWD_HEADER` | Samtec FTSH-105-01-L-DV-K | KiCad's generic 2x05 1.27 mm SMD header has different pads |
| `TS_1187A_B_A_B` | XKB TS-1187A | no model; its footprint is also not in the locked provider |
| `KENTO_KT0603R`, `KENTO_KT0603Y` | 0603 chip LED | no recorded height; KiCad's 0603 LED model is 1.1 mm tall |
| `KINGBRIGHT_APTD1608*` (4) | 1.6 x 0.8 x 0.95 mm LED | KiCad's 1.1 mm model is taller; `height` is set instead |
| `EVERLIGHT_19_217_*` (3) | 1.6 x 0.8 x 0.4 mm LED | as above, `height` set |
| `SRP4020TA_1R5M` | Bourns SRP4020TA | not in KiCad |
| `EG800G_EU`, `SIM7670G_LNGV`, `MAX_M10S_00B` | LTE / GNSS modules | not in KiCad |
| `Ag59624_LPB` | Silvertel Ag59600 PoE module | not in KiCad |
| `R78B6V5_1A`, `R78E3V3_1A` | RECOM R-78B/R-78E SIP-3 | KiCad's R-78B-2.0/R-78E-0.5 footprints use another origin |
| `R78K12_1A` | RECOM R-78K | not in KiCad |
| `CYUSB4013_FCAXI` | Infineon FX10 FCA169 | KiCad's BGA-169 11 x 11 mm model has a different ball layout |
| `NRF52832_QFAA` | QFN-48 6 x 6 mm, 0.4 mm | KiCad 10 ships only the thinner UQFN-48 |
| `MAX96793GTJ_VY` | 32-TQFN 5 x 5 mm | KiCad ships only the thicker QFN-32 |
| `TUSB320LAI` | X2QFN-12 1.6 x 1.6 mm | not in KiCad 10 |
| `COILCRAFT_0603USB_601MLC` | Coilcraft 0603USB | KiCad's footprint names a model the library does not ship |
| `TPS2121RUXR` | VQFN-HR-12 | no model; its footprint is also not in the locked provider |
| `TPS63710DRRR`, `TPS63020DSJR` | WSON-12 3 x 3, VSON-14 3 x 4 | not in KiCad |
| `OPA547T`, `OPA548T` | TO-220-7 (KVT) | KiCad's TO-220-7 footprints use another origin and lead form |
| `VO617A_3X017T`, `AQV252GAZ` | SMD optocoupler / PhotoMOS | KiCad's SMDIP-4/6 pads differ |
| `RCLAMP1561PQTCT`, `TPD1E01B04DPYR` | 1.0 x 0.6 mm two-pad DFN | not in KiCad |
| `SIT9121AI_1C2_33S125` | SiTime 5032 6-pin | KiCad's 6-pin 5.0 x 3.2 mm oscillator has different pads |
| `FUSE_0451010_MRL` | Littelfuse 0451 NANO2 | KiCad has the footprint, not a model |
| `WE_7447797820`, `WE7499511420` | Wurth parts | not in KiCad |

The 10 parts with an existing model reference that resolved to nothing are now
either given a same-outline model (`MAX96792AGTM_VY`, `TPS62130ARGTR`,
`BQ24072RGTR`, `BQ24072TRGTR`) or listed above; their references are dropped
with a warning, as before.

## Generic model fits, dimensions unconfirmed

`TSW10207GS` lines up with KiCad's `PinHeader_1x02_P2.54mm_Vertical`, but no
recorded dimension shows the TSW `-07` lead style matches its post lengths, so
no `model` was added.

## Footprints that do not resolve against the locked provider

`TS_1187A_B_A_B`, `ADS4125IRGZT`, `LM27761DSGR` and `TPS2121RUXR` name KiCad
footprints that exist in KiCad 10 but not at 7ebfa6b. If a consumer requires a newer
provider, `ADS4125IRGZT` gets its body from the footprint and `LM27761DSGR` from
its `model` field.
