# TPS22918 DBV with local 0603 input bypass

Bind `TPS22918_DBV_0603_BYPASS` members `U` to TPS22918DBVR and `C` to
its selected 0603 input capacitor, and nets `SUPPLY`/`GROUND` to the input
rail/system ground. Preserve the capacitor's decoupling role and `U.VIN`
target. Exact managed SOT-23-6 and C_0603_1608Metric footprints are required.

U is the origin. C is at (-1.1375,-3.68) mm, rotation 90 degrees. Its positive
land is 1.955 mm from VIN pin 1; the courtyards have 0.5 mm extra separation.
Owned 0.25 mm F.Cu copper joins C positive to VIN. The supply port is C
positive. C negative reaches a 0.6/0.3 mm through via at (-1.1375,-5.23) mm;
the return contract requires ground planes on In1.Cu/In2.Cu. The macro
permits four quarter-turn rotations on a four-layer board.

**The VIN lead carries the switched load current as well as input-bypass
current.** Its 0.25 mm width is not qualified for the part's full current
rating. The host must establish load/inrush current, copper thickness,
voltage drop and temperature rise before using this geometry. The temporary
macro's `control_supply` width-contract classification does not establish a
load-current rating. Do not use it as a generic high-current load-switch layout.

The host owns IC ground pin 2, VOUT and its output capacitor, ON/CT/QOD,
all remaining support, and the complete load/return loop. Only VIN and the
input-capacitor lands are bound. Verify effective input capacitance and
stability/inrush behavior at the selected operating point.

This is an authored adaptation, not manufacturer CAD. TI SLVSD76C Rev C,
sections 10-11 and Figure 32 provide the source layout intent; the source
hash is retained by the part and qualification record. The 2 mm positive-pad
limit is a fixture/consumer criterion, not a universal datasheet distance.

The unchanged macro passes the source-bound combined camera/CC native
fixture: routing and requirements pass, zero native opens/violations, and
2/2 fixture bypasses are surface-connected. See `validation.json` for exact
inputs and run binding. This does not validate every rotation, whole-board
placement, current, assembly, EMI or production use. Production qualification
remains false; the layout file retains its original temporary-fixture comments
to preserve the exact validated bytes.
