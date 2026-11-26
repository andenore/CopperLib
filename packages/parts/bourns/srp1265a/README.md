# SRP1265A-2R2M

Export `SRP1265A_2R2M`: 2.2 µH ±20%, 4.2 mΩ maximum DCR, 22 A Irms
(40°C temperature rise), 40 A Isat (20% inductance drop), at the datasheet's
stated test conditions. These figures are not a board-level current guarantee.
Review the L-versus-I curve and application temperature, copper, airflow and
switching losses. Host component value is `2.2uH`.

Source: Bourns SRP1265A datasheet Rev 06/24, p1 ratings/outline/recommended
land pattern, p2 L-versus-I, downloaded 2026-11-23:
https://www.bourns.com/docs/Product-Datasheets/SRP1265A.pdf
SHA256 `30b470999b737a6350ce5b09a917a5f12090c2e0895a78ddc15285e3d44ec649`.

The package-owned land pattern is derived directly from p1: 14.2 mm outside,
8.0 mm inner gap, 5.0 mm pad height => two 3.1 × 5.0 mm pads at ±5.55 mm.
Nominal body 13.5 × 12.5 mm; maximum body 14.0 × 12.8 × 6.5 mm.
Courtyard encloses maximum body and pads plus 0.25 mm; that added clearance is
library assembly policy, not a manufacturer dimension. No 3D model is qualified.
The symmetric unpolarized winding uses library pad numbers 1 and 2.

This is a bare inductor, not a converter qualification. Consumer power contract
must cover component ratings, current capacity, layout, transients and prototype
temperature. No generic short-loop geometry or trace-width guarantee is implied.
