# TPD1E01B04DPYR low-capacitance protection

Exact TI DPY 0402 model: bidirectional working voltage 3600 mV; either terminal
can be ground. SLVSDG3C specifies **200 fF typical / 230 fF maximum at zero bias**
for DPY, not the DPL package's smaller capacitance. TLP clamp is 7 V at 1 A,
9.2 V at 5 A and 15 V at 16 A; do not treat 7 V as a universal clamp limit.

Footprint follows DPY0002A 4224561/C example copper, 300 x 500 um lands on
700 um centers. This uses the illustrated NSMD alternative, not TI's preferred
solder-mask-defined implementation. Paste/mask/process and assembly approval
remain consumer gates. Keep near the external launch with short ground return;
evaluate the actual RF discontinuity and receiver ESD immunity.

TI JLCPCB candidate C779389 is distinct from other manufacturers' same-name
parts. Current assembly stock is not established by an indexed listing.
This part alone does not establish cellular coexistence or protect an arbitrary
added SAW filter. System ESD and RF tests remain required.
