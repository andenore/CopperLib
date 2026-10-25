# AD7606C 18 serial support

Reusable electrical support for software mode, single DOUTA and external 2.5 V
reference. Based on Rev B Figure 123 and pages 57–59. VDRIVE is board-selected
3.3 V. ADC input negative terminals share GND for single-ended operation.
Firmware must set CONFIG DOUT_FORMAT to one line: the reset default is two.

Individual 100 nF AVCC capacitors, 100 nF VDRIVE, separate 1 µF REGCAPs,
100 nF REFIN, joined REFCAPA/B with 10 µF, and 10 µF source bulk are present.
The 2 mm proximity constraints are engineering placement targets, not a
dimension stated by ADI. They do not guarantee low-inductance loops.

Before routing: inspect ADI evaluation-board layout, preserve a continuous
ground plane and dedicated ground connections, keep digital traces out from
under the ADC and away from analog inputs. A qualified physical macro has not
yet been supplied. Exact capacitor MPNs/DC bias and reference drive stability
are unresolved. No board release or analog performance is implied.
