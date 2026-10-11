# Conditional SIM7672X RF and power reference facts

These are facts from SIMCom's SIM7672X Series Hardware Design V1.01, not
manufacturer-confirmed equivalence to SIM7670G-LNGV. A consumer must explicitly
accept applicability before using them; a consumer's assumption does not qualify
this shared part. Source [retained mirror](https://files.waveshare.com/wiki/SIM7670G-LTE-Cat-1-GNSS-HAT/SIM7672X_Series_Hardware_Design_V1.01.pdf),
SHA256 `bd198ceb5eecddbafd3d438782cf35c89208e40a8c4b3b1eb19097fdb363706d`.
Complete relevant pages and figures were rendered and visually inspected.

## Antenna integration: pp58-60, Figures 30-32

- Page 60 limits the module ANT-to-connector PCB trace to 20 mm, with impedance
  design and separation from power/clock interference. Determine the actual
  rotated land location; a footprint-origin proximity estimate is insufficient.
- Figure 30 reserves antenna matching elements; p59 describes initial series
  values of 0 ohm and 100 pF, with shunt capacitors unpopulated by default.
  Values ultimately depend on antenna tuning. The drawing places the matching
  block on the antenna side of the RF test connector: do not blindly transplant
  that whole block onto an internal module-to-coax feed or assume the external
  antenna assembly already supplies it. Record the chosen system boundary.
- The guide recommends bidirectional low-capacitance RF ESD protection. Review
  clamp characteristics, RF loading, exposed connectors and antenna implementation
  before selecting a device. A generic logic TVS is not an RF substitute.
- Active GNSS antennas require the appropriate bias/filter/protection network;
  do not apply the modem's GNSS diagram to a separate receiver without reviewing
  that receiver's integration guide. Antenna and enclosure choices stay consumer-owned.

## VBAT integration: pp25-27, Figure 6

- All three VBAT contacts are required. The guide's test setup uses a 100 uF
  tantalum capacitor and it recommends at least 100 uF external reservoir
  capacitance when the supply can support the peak demand. Nominal ceramic
  capacitance does not establish effective capacitance under DC bias.
- It recommends nearby 10 pF, 33 nF, 100 nF and 1 uF ceramic capacitors and at
  least 2 mm supply routing from regulator to module. Review actual pad neckdowns,
  distribution copper, via barrels and current-sharing; minimum track width alone
  cannot certify a plane-fed or mixed-layer path.
- Ferrite filtering is conditional on interference; surge/overvoltage protection
  is recommended with attention to the stated clamp requirement. Do not add a
  ferrite without assessing DC drop and transient effects on the actual supply.
- The peak-current entry in Table 9 is TBD: this guide does not justify inventing
  a modem peak load or using a converter's headline current rating as delivered load.

Consumers should encode source-backed route lengths/placement/width intent and
review whole-system implementation. CopperScript already provides length/width
screens and routing constraints; a numerical pass never replaces impedance,
transient, thermal or prototype evidence. Shared support circuits/components
belong in CopperLib when a topology and exact parts are established.
