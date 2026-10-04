# Exact assembly basics

Reusable exact identities, not generic placeholder parts. Nominal values remain
explicit on component instances; the compiler does not enforce a fixed value
against the part's MPN. Do not override these parts with incompatible values.
Procurement offers remain board-side assembly selections; no stock is implied.

| Part | Value/rating | Package | JLC candidate |
| --- | --- | --- | --- |
| UNIROYAL_0603WAF1002T5E | 10 kohm, 1%, 0.1 W, 75 V | 0603 | C25804 |
| SAMSUNG_CL05B104KO5NNNC | 100 nF, 10%, 16 V, X7R | 0402 | C1525 |
| FENGHUA_0402CG101J500NT | 100 pF, 5%, 50 V, C0G | 0402 | C1546 |
| SAMSUNG_CL10A105KB8NNNC | 1 uF, 10%, 50 V, X5R | 0603 | C15849 |
| SAMSUNG_CL10A475KO8NNNC | 4.7 uF, 10%, 16 V, X5R | 0603 | C19666 |
| KENTO_KT0603R | red LED, 1.8–2.4 V at 20 mA | 0603 | C2286 |

Manufacturer documents were inspected through official manufacturer product
pages and manufacturer-authored PDFs linked by the official supplier catalogue.
Do not redistribute downloaded PDFs; hashes and concise locators are recorded.
The KENTO PDF is identified by JLC's C2286 catalogue attachment; its cover calls
the product “0603-0.6 red”, rather than printing the commercial ordering code.

**KENTO numbering is A=1, K=2**, established by the signed-polarity drawing
on PDF page 2. The matching `LED_SMD:KENTO_KT0603R` footprint has cathode left
(pad 2) and anode right (pad 1). Its marked cathode and nominal IPC 0603 copper
lands preserve the standard KiCad land geometry; terminal numbers are reversed.
Never substitute KiCad's generic K=1 footprint without remapping the package.
The vendor also shows a smaller suggested land pattern; this footprint uses
the existing nominal IPC solder-fillet lands, not an exact copy of that drawing.
Do not claim manufacturer pins from supplier symbol numbering alone.

Brightness at very low coin-cell LED current is not guaranteed by the 20 mA
catalogue test. Board designers must choose current/brightness and battery
load budget explicitly. No firmware, light-output or battery-life validation
is implied by these part definitions.
# Generic CopperLib packages

This directory contains reusable, manufacturer-neutral geometry and interface
definitions. Exact orderable components live under `packages/parts/<vendor>/`;
generic definitions remain intentionally reference-level until a manufacturer
and source document are selected.

The `headers` package exports `HEADER_1X02`, `HEADER_1X04` and `HEADER_1X06`.
The individual connector, button, LED and debug header packages each export a
single part and can be imported independently.
