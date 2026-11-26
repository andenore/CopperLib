# Printed-antenna feed anchor

`AntennaFeed` is an authored 1.0 × 0.6 mm bare copper land with a 1.5 × 0.9 mm
courtyard. It has no paste, assembly or purchasing requirement. It factors the
existing CopperAssetTracker feed-anchor geometry into a reusable package; the
generator label changes to CopperLib. It is not a manufacturer's component or
a tuned antenna. The library does not assign a frequency or impedance to it.

Bind `constraint antenna(ANT.FEED)` in the consumer. CopperScript owns the
radiator geometry, fixed feed pose and all-layer antenna region exclusions.
The host must supply the actual stackup, ground zones, radio matching network,
antenna matching, source-bound synthesis and enclosure/battery/metal review.
Preserve the radio manufacturer's chip-side matching and return geometry.
Keep copper, screws, other components and external metal out of the required
antenna region, and verify after placement/routing. Synthesis is simulation,
not electrical, RF, EMC, fabrication or regulatory qualification.
