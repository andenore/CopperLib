# CSD18540Q5B

Exact60V N-channel Q5B package, ±20V gate absolute maximum. This is not a
3.3V-qualified gate-drive selection. TI SLPS488B p1 establishes pinning; pp8-9
establish the package and recommended copper. Hash and URL are in part.copper.

The exposed drain is locally numbered9; terminals5-8 overlap its continuous
copper through the manufacturer's four tabs. All three source terminals and
all drain contacts remain required: there are no routing waivers. The footprint
uses the p1 top-view orientation. Copper follows the p9 pattern; the central
paste windows use its dimensions with authored symmetric placement, requiring
stencil/assembly review. This adaptation is explicitly not extracted vendor CAD.

The host owns gate/source return locality, ringing control, thermal copper,
parallel-contact routing, short-circuit SOA and repetitive-energy validation.
The headline pulse-current and avalanche ratings alone do not establish a
consumer's short-circuit survival. No physical macro or production approval is
supplied. Regenerate with tools/generate/recoil_protection_parts.py.
