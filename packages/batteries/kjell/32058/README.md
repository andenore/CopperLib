# Kjell article 32058 - external protected 18650

Reusable source catalogue, not an SMT part or a qualified assembled pack. Do not
invent a PCB footprint or put this external cell in a JLCPCB placement BOM.
The Norwegian retailer lists 2600 mAh and built-in overcharge/deep-discharge
protection. Its HTML marked the product in stock on 2026-10-10; local store stock
and quantity are not established and must be checked again when purchasing.

`specification.json` separates current retail facts from the older linked pack
datasheet. Use pack ratings, not the higher bare-cell currents in section 6.
The pack drawing allows 71,500 um length; a bare-18650 holder may not fit.
The empty protection section does not establish a trip threshold or pulse rating.
An external cell-mounted sensor and a reviewed harness remain host obligations.
Do not equate protection with a charger, or charge-temperature sensing with
discharge protection. Charging below the published minimum is not allowed.

Source applicability and production publication remain false. The companion
data are not Copper language syntax and are not automatically resolved by an
existing consumer package lock. Publish/pin/review them explicitly before use
as release inputs. Calculations and qualification algorithms belong in CopperScript.
