# nRF52832 QFAA

The device model covers a subset of peripheral choices. TWIM0 currently exposes
SDA on P0.26 and SCL on P0.27; this is not a silicon restriction.
[Nordic Product Specification, TWIM](https://docs.nordicsemi.com/r/bundle/ps_nrf52832/page/twim.html),
"Master mode pin configuration", Table 1 and PSEL.SCL/PSEL.SDA register fields
document configurable GPIO selection and S0D1 drive. Select pins only while
TWIM is disabled. Provide pull-ups and avoid conflicting shared peripheral
instances in firmware. The CopperScript subset does not enforce shared-instance
ownership. No new RF or layout qualification is claimed by the mux addition.

SPI0 exposes SCK on P0.14 or P0.27, MOSI on P0.13 or P0.26, and MISO on P0.12
or P0.25 as a supported subset, with chip select handled by an ordinary GPIO. The
[SPI pin configuration](https://docs.nordicsemi.com/r/bundle/ps_nrf52832/page/spi.html)
(Product Specification v1.9, SPI master mode pin configuration) specifies output SCK/MOSI
and input MISO. Configure PSEL only with SPI disabled; firmware must arbitrate
the shared SPI0/SPIM0/SPIS0/TWI0/TWIM0/TWIS0 instance and isolate the pins before
removing power from an external peripheral.

These alternatives represent software-selectable GPIOs, not dedicated pin
assignments. P0.12-14 avoid the QFAA P0.22-31 group for which Nordic recommends
low drive and low-frequency I/O near the radio. The older P0.25-27 mux options
remain valid silicon capabilities, but their presence does not qualify them
for high-frequency use while the radio operates. See Nordic's
[pin usage recommendations](https://docs.nordicsemi.com/r/bundle/ps_nrf52832/page/pin.html)
and [GPIO near the radio](https://docs.nordicsemi.com/r/bundle/ps_nrf52832/page/gpio.html).
