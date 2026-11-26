# nRF52832 QFAA exposed-pad ground escape

`NRF52832_QFAA_EP_GROUND_ESCAPE` preserves an explicit F.Cu connection from
the QFAA exposed pad 49 to peripheral ground pad 45. It imports the managed
KiCad QFN-48/4.2 mm exposed-pad footprint and supports orthogonal rotations.
Its only required layer is F.Cu, so it is compatible with a four-layer host.

```copper
import ground_layout "github.com/andenore/CopperLib/packages/circuits/nordic/nrf52832-qfaa-ground-escape";
physical_macro NRF_GROUND: ground_layout.NRF52832_QFAA_EP_GROUND_ESCAPE {
    member U = U_NRF;
    net ground = GND;
}
```

This is the first portion of `track_8` in the sibling
[managed Nordic/Johanson layout](../nrf52832-johanson-reference/managed-layout.copper):
pad 49, local (-1,-1) mm, pad 45, with 0.2286 mm width. The ground exit is an
authored adaptation, not a claim that this fragment reproduces Nordic's complete
reference artwork. The original source is Nordic QFAx Reference Layout 1.1,
QFAA LDO; its official archive URL and verified historical hash are retained
in the macro's source record. Chip RF matching and other reference copper are
outside this fragment's scope.

The host must route pad 45 to its real ground network and establish native
filled-plane continuity. No via, plane, keepout, antenna, paste aperture or
fabrication-process permission is added. In particular this macro neither
requires nor permits a via inside the exposed pad. It does not establish a
thermal-via array, package thermal performance or assembly suitability.
Source-owned copper is immutable after binding; changes must be made here
and revalidated rather than patched into an exported PCB.

The footprint provider must be declared and locked by the consumer. Compilation
validates the definition; host binding, all-pad clearance, native refill and
zero GND opens remain required. This macro is not production qualified.
