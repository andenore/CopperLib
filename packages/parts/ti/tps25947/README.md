# TPS259470LRPWR

Exact active-current-limit, FLT-output, thermal-latch variant. The L suffix does
not mean every initial short immediately latches: Table7-3 leaves FLT high at
initial fast trip; sustained limiting asserts FLT. UVLO/OVLO do not assert FLT.
EN below VSD resets an internally latched fault. Hosts must analyze sequencing
and independent firing/restart policy rather than treating FLT as power-good.

Source: TI SLVSFC9C (May2026), Table5-1, Table7-3, sections7.3.5/8.3/8.4;
RPW0010A drawing4225183/A. SHA256 and exact URL are in part.copper.

The package-local footprint preserves the ten contacts, including L-shaped
corners and full-length IN/OUT copper. The generator decomposes each L into
overlapping rounded rectangles. No internal-pad connectivity waiver is used.
Stencil positions follow TI's example; assembly process remains unqualified.

Mandatory host obligations: local input bypass, output transient clamp and
capacitance, short/wide power copper, quiet ILM with parasitics below50pF,
thermal/current/fault-energy review. Bulk capacitors downstream bypass electronic
current protection during their own discharge. The published500ns response is
typical, with a specified test condition; it is not a guaranteed bound.

No physical macro or production qualification is supplied. The exact topology,
current/voltage settings, capacitance and interruption transients belong to the
consumer. Regenerate with tools/generate/recoil_protection_parts.py.
