# TUSB320LAI RWB with local 0402 bypass

Bind `TUSB320LAI_RWB_0402_BYPASS` members `U` to TUSB320LAI and `C` to
its selected 0402 bypass capacitor; bind `SUPPLY` to VDD and `GROUND` to
system ground. Preserve the capacitor's decoupling role and `U.VDD` target.
Exact managed Texas_X2QFN-12_1.6x1.6mm_P0.4mm and C_0402_1005Metric
footprints are required.

U is the origin. C is at (-0.6,-2.81) mm, rotation 90 degrees. Its positive
land is 1.505 mm from VDD pin 12; the courtyards have 0.5 mm extra separation.
Owned 0.25 mm F.Cu copper joins C positive to VDD. The supply port is C
positive. C negative reaches a 0.6/0.3 mm through via at (-0.6,-4.06) mm;
the return contract requires ground planes on In1.Cu/In2.Cu. All four
quarter-turn rotations are permitted on a four-layer board.

The host owns IC ground pin 10, CC and control signals, operating mode,
VBUS detection, protection and the complete local return loop. Only VDD
and the bypass lands are bound. The supply lead carries controller supply
current; it is not a USB VBUS/load path. Review routing, ground continuity,
effective capacitance and electrical limits in the complete consumer.

This is an authored adaptation, not manufacturer CAD. The part identifies
TI SLLSEQ8D Rev D; the exact bypass/layout page and captured PDF hash remain
open in the qualification record. The 2 mm positive-pad limit is a consumer
criterion, not a universal datasheet distance.

The unchanged macro passes the source-bound combined camera/CC native
fixture: routing and requirements pass, zero native opens/violations, and
2/2 fixture bypasses are surface-connected. See `validation.json` for exact
inputs and run binding. This does not validate every rotation, whole-board
placement, USB behavior, assembly, EMI or production use. Production
qualification remains false; original temporary-fixture comments are retained
in the layout file to preserve the validated bytes.
