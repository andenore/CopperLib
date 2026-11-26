# TPS61088 four-layer local layout — authored adaptation

Export `TPS61088_FOUR_LAYER_LOCAL_CONTROL`. This physical macro binds existing
electrical components; it does not create circuitry or select operating values.
It owns 15 components, the inductor switching connection, first input/output
capacitors, local control wiring, quiet feedback, six external PGND return vias,
other local returns and protected routing regions. The approximate occupied
envelope is 30.4 × 13.4 mm, before additional host assembly clearance.

Reference: TI TPS61088EVM-677 SLVUAF2, June 2015, Figure 7 p7 schematic and
Figures 8–11 pp9–10 layout, https://www.ti.com/lit/ug/slvuaf2/slvuaf2.pdf,
SHA256 `a957c5e8842e86d83037f8da9ccfcbebce7c61cfae7981ff1f6e63f3c00bf46a`.
This is authored geometry with changed inductor, passives and layer allocation,
not extracted vendor CAD or a manufacturer-qualified reference implementation.

## Bindings

The anchor is `U`, the TPS61088RHLR. Rotations 0/90/180/270° are permitted.
Layers are F.Cu, In1.Cu, In2.Cu and B.Cu. Internal additional courtyard spacing
is 0.15 mm; actual copper clearances remain independently checked.

| Member | Required footprint / role |
| --- | --- |
| U | Package-owned TI_RHL0020A_TPS61088 |
| L | Package-owned Bourns_SRP1265A, SRP1265A-2R2M |
| C_INPUT1 | 0805 input bulk, beside L input terminal |
| C_OUTPUT1 | 1210 output bulk |
| C_VCC, C_OUTPUT_HF | 0603 |
| C_BOOT, C_INPUT_HF, C_SS, C_COMP | 0402 capacitors |
| R_FSW, R_ILIM, R_FB_TOP, R_FB_BOTTOM, R_COMP | 0402 resistors |

Net roles: `VIN`, `VOUT`, `GND`, `VCC`, `BOOT`, `SW`, `SS`, `FSW`, `ILIM`,
`FB`, `COMP`, `COMP_RC`, `EN`. Ground includes NC11/NC12 for thermal continuity
and MODE13 for forced PWM. Do not bind this variant to floating MODE/PFM.

External ports, in the unrotated U-centered coordinate frame:

| Port | Net | Position, mm |
| --- | --- | --- |
| INPUT | VIN | (-20.8, 2.6) |
| OUTPUT | VOUT | (1.5, 6.7) |
| ENABLE | EN | (-2.2, -6.6) |

SW is private, including L.2 and all four switch contacts. The main input and
switch trunks are 2 mm wide, without switching-node vias. Local pad joins use
collectors matched to the narrow terminals. Output collector-to-capacitor and bulk-to-port main power feeds are 1 mm. These are
authored conductor dimensions, not ampacity guarantees. Review peak/RMS current,
minimum copper thickness, pad neckdowns, drop and temperature in the consumer.

The owned 1 mm output tail extends to local y=6.7 mm, 0.8 mm beyond the
local-support region's y=5.9 mm boundary. This leaves space for a 1 mm host
track plus 0.15 mm clearance at the connection point. It replaces the earlier
y=6.2 mm endpoint, whose 0.3 mm center margin blocked a full-width host route.
Only the final tail and port move; the output capacitor bank, chip connections,
protected region and conductor widths are unchanged. This extension is an
authored host-access adaptation, not a TI reference dimension. Wider host
routes or larger clearances require a separate access review. Any host ground
pour beside the extension must clear VOUT normally; the port grants no access
through protected regions or foreign copper.

The input IC bypass is a separate low-current branch on B.Cu, returning through
two vias; it is not the inductor input-current path. Input bulk proximity must
be measured to **L.1**, not to the IC's VIN control-supply pin. Probe constraints
verify 4 mm to L.1, 4 mm output bulk to VOUT15, 5.5 mm L.2 to SW4 and 2 mm local
BOOT/VCC/input-HF/output-HF/FB bounds. These bounds describe this authored
adaptation, not vendor-prescribed universal limits.

The `input_sense_width` contract applies only to the two 0.2 mm B.Cu segments
feeding the chip's VIN branch. The `input_main` path remains 2 mm; its power
current obligation is unchanged. TI SLVUAF2 section 2.1 and Figure 7 explicitly
separate the IC supply through JP1 from the power-stage input. This supports the
branch classification, not a manufacturer-specified trace width. The branch
must remain dedicated to the IC supply and its local bypass.

TI TPS61088 datasheet SLVSCM8D, August 2021, pin table p3 and section 9.2.2.6
p17 identify VIN pin9 as the IC supply and recommend a local 100 nF ceramic
bypass. Bind `C_INPUT_HF` accordingly, close to VIN with a short ground return;
the remote input bulk does not replace it. Section 7.5 p5 lists VIN quiescent
current as 1 uA typical / 3 uA maximum under its stated enabled, no-load,
12 V output conditions. Those figures do not bound startup or switching
transients. Source: https://www.ti.com/lit/ds/symlink/tps61088.pdf.
The exact Rev D PDF archival requirement in `qualification.json` remains open.
Local supply ripple, return impedance and startup remain host qualification
items; no capacitor value or power-path dimension changes with this contract.

## Four-layer return and assembly boundary

Six owned 0.6/0.3 mm standard through-vias lie outside the exposed pad, north and
south. All four PGND fingers have explicit local copper; north/south branches
provide parallel connections to continuous In1/In2 ground. The thermal pad and
paste apertures are unchanged. The native compiler currently supports filled,
capped via-in-pad only with its six-layer GND process. This four-layer variant
does not put unqualified open holes under the soldered pad or waive that check.
External vias and necks need thermal/current measurements; they are not claimed
equivalent to the EVM's thermal-via arrangement. No switch or thermal operating
limit is qualified by a passing copper check.

The consumer must supply continuous internal ground planes, the remaining input
and output banks, rated source/harness/load paths, compensation verification and
complete EMI/thermal review. Host routes attach at the named ports. Preserve
the macro's owner regions and inspect exported fill exclusions. Where an
exporter cannot retain a region's fill prohibition, the consumer must add a
pose-bound zone-only exclusion and independently check the resulting fill.

Native probe builds exercise actual port connections, exact footprints,
component courtyard legality, source distance constraints, immutable owner
copper, full routing and saved ground fills. Passing native checks does not
cover silkscreen, mask bridges, process capability, loop stability, EMI or
prototype power behavior. `qualification.json` keeps those gates open.

Current-source validation is pending for the output-port extension to local
y=6.7 mm and the input-supply branch width contract. Earlier probe passes do
not validate this revision or host power-net widths they did not exercise.
No package `validation.json` is present; fresh source-bound native validation
must be recorded by the consuming project before claiming routing closure.

The local-support protected polygon steps inward from x=7.9 mm to x=6.8 mm
at y=2.0 mm. The output-bulk courtyard ends at x=7.0 mm. Its two external
GND return branches and vias remain immutable owned copper outside that
stepped boundary, subject to ordinary clearance checks. This releases unused
placement space without removing switching or quiet-control protection. The
ground-side edge of the output land remains governed by normal copper rules;
the extra 0.2 mm trim avoids reserving space around an adjacent ground via.
Consumers must check adjacent pad/via solder-mask separation and assembly
clearance; same-net electrical clearance alone does not qualify solder wicking.

The output-bulk return vias lie at (7.4,3.2) and (7.4,2.2) mm. The second
return branches upward to preserve space beside the lower-right edge for
adjacent components while retaining two parallel ground returns.
