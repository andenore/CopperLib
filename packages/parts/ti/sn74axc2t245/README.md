# SN74AXC2T245RSWR configured interface views

Both exports represent the same orderable device and UQFN-10 footprint:

- `MODEM_UART_TRANSLATOR`: channel 1 A->B, channel 2 B->A; A-side 3.3 V and
  B-side 1.8 V interface annotations. DIR1 must be high, DIR2 low, OE_N low.
- `MODEM_STATUS_TRANSLATOR`: both channels B->A; DIR1/DIR2 low, OE_N low.
  Ground the unused B input; its A output can remain unconnected.

These are reusable direction-specific views, not different physical parts or a
complete runtime-configurable device model. Names are retained for compatibility
with the original consumer. Do not wire direction controls inconsistently with
the selected view. Provide local decoupling on both supplies and review power
sequencing/voltage limits against TI SN74AXC2T245 SCES879A, Table 4-1 and truth
tables: https://www.ti.com/lit/ds/symlink/sn74axc2t245.pdf

The views are provisional and do not certify all timing, startup or isolation
behavior. Exact assembly rotation and package review remain required.
