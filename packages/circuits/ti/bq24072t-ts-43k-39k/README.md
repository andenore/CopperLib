# Conservative BQ24072T TS bias network

Reusable electrical module; not a routed or qualified hard macro. Use 1%
resistors: upper 43 kohm (0603), NTC shunt 39 kohm (0402), TS isolation
100 kohm (0402). Source topology is TI SLUS937C Figure18; R8 is required when
the upper resistor is below 100 kohm. Use only with the voltage-based T variant.

Connect VIN to charger IN, GND to a quiet common charger/cell negative return,
NTC to a cell-mounted Semitec 103AT-2 (other lead to protected cell negative),
TS to charger TS. Keep isolation-to-TS short, ideally direct F.Cu, away from
switch nodes. Consumer must constrain that actual charger endpoint and review
ground voltage errors, connector/harness faults and protection. An onboard
thermistor measuring the PCB is not an equivalent cell sensor.

Design target: roughly 5-35 degC nominal. Screening against guaranteed charger
thresholds uses sensor values at 0 degC and 40 degC, not a claim that these are
guaranteed trip temperatures. Use CopperScript `ratiometric_ntc_divider` with
explicit R/T bounds and TS input leakage. Catalogue R25/B tolerances alone
do not establish a guaranteed full R/T envelope. Ideal NTC open/short screening
does not establish safety for every harness or isolation-resistor fault.

Candidate upper resistor: UNI-ROYAL 0603WAF4302T5E, LCSC C23172; shunt:
0402WGF3902TCE, C25783. Confirm current JLC assembly availability, exact ratings
and temperature drift in each consumer BOM. No consumer approval is inherited.
