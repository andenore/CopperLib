# Taoglas FXP611.07.0092C external passive GNSS antenna

Reusable companion facts, not a PCB component/footprint or a qualified RF macro.
The factory assembly has a 92 mm cable, U.FL-compatible plug, 50 ohm nominal
interface and 1559-1610 MHz L1 coverage for GPS/Galileo/GLONASS/BeiDou. No antenna
bias supply is needed. It is linearly polarized; this is not an RHCP patch.

Mount the radiator on plastic. Reserve **40 x 40 mm**, with **200 um** mounting
height allowance, and at least **10 mm** clearance to metal or the main device
ground plane (datasheet p3). Battery cans also count as metal. This radiator
clearance is not permission to remove ground beneath the host's RF trace.
The reference measurement used a 300 x 300 mm ABS panel, not an arbitrary small
consumer enclosure. Preserve factory cable and verify bend/retention constraints.

The p10 drawing dimensions and connector BOM differ in detail from the nominal
specification; record both and confirm the delivered assembly before mechanical
release. Do not copy one headline VSWR/gain into an installed performance pass.

See specification.json for integer-valued dimensions and exact source hash;
qualification.json keeps host matching/protection, layout, modelling and bench
evidence mandatory. The receiver may have integrated matching/DC isolation, but
this does not settle transmitter isolation, antenna tuning or extra SAW filtering.
Consumer reference designators, enclosure coordinates and measurements belong
outside this package. Production publishability remains false.
