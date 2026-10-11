# TPS62130A layout qualification backlog

The current always-on and enabled assets use v0.3 fixed VIN/SW/VOUT polygons,
owned local GND zones and pending plane-backed returns. Geometry, provenance,
ports, process assumptions and reproduction are in [physical layout](physical-layout.md).
Both variants pass isolated native rotation/external-access checks; this is an
authored adaptation of TI Figure 11-1, not extracted CAD or production approval.
The conductor target is below 0.5 A per output rail.

- [ ] Extract actual filled copper, stackup and via plating for resistance/drop,
  current density and input/output loop metrics; obsolete trace-only budgets
  cannot qualify filled zones. Check SW extent and quiet VOS/FB pickup separately.
- [ ] Add generator-local loop/sense geometry bounds and negative plane-return
  assertions. Preserve each required power contact and dedicated capacitor GND via.
- [ ] Select exact capacitors and verify biased capacitance, voltage/temperature
  ratings, inductor saturation, thermal-via assembly and process.
- [ ] Validate stability/transients, temperature and conducted/radiated EMI on hardware.
- [ ] For a host integration, refresh reviewed scene/dependency identities, route
  every instance, refill independently and check native closure, owner geometry,
  filled returns and every host critical interface. Isolated fixtures are insufficient.

Keep `production_publishable=false` until an explicit qualified path exists.
Follow the [hard-macro review checklist](../../../../docs/hard-macro-review-checklist.md).
Do not weaken host constraints or add example-specific repair selectors.
