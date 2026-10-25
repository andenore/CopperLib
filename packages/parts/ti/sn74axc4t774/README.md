# SN74AXC4T774PWR

PW 16-pin package, SCES898C Table 4-1. Control inputs reference VCCA.
DIR high selects A to B. OE high disables all outputs. Pull OE high to VCCA
at boot and place one local 100 nF capacitor at each supply pin.
Both supplies and I/O are limited to their specified 3.6 V operating range.
Power isolation below 100 mV does not implement a 1.8 V VTref validity threshold;
consumers need a separate interlock. Firmware open-drain emulation requires
switching direction to input for the released state, not driving A high.
