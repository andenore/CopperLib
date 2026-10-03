# Internal pad connectivity: part-generation checklist

These are electrical/package facts, not routing waivers. CopperScript's part
property `internal_pad_groups` lists semicolon-separated groups of footprint pad
numbers. Numbers within a group are comma/space separated. A singleton means
all distinct lands carrying that number are permanently connected inside the
installed component. For example:

```copper
internal_pad_groups = "1";       // Keystone 3034 positive retainer tabs
internal_pad_groups = "1; 2";    // TL3342: two separate permanent contact pairs
internal_pad_groups = "1, 3; 2, 4"; // only for a verified four-number mapping
```

Do not copy the last mapping into TL3342's KiCad footprint: it already collapses
the manufacturer's four terminals into two repeated pad numbers.

## Mandatory generation/review steps

1. Inspect the exact orderable variant's drawing/internal circuit, not a similar
   product photograph. Record manufacturer URL, revision, sheet and SHA-256 when
   evidence is available. Source fields remain optional in the language; an agent
   must not invent an internal connection without evidence.
2. Map manufacturer terminals to actual footprint lands, checking orientation
   and repeated numbers. Keep all solder lands, paste apertures and mechanics.
3. Declare only always-conductive paths. A switch's two contacts remain separate
   until actuated; do not merge them. Resistive/inductive paths and semiconductor
   junctions are not permanent shorts.
4. Do not exempt externally required power, parallel-current or thermal contacts
   merely because they appear electrically common inside a device. Absence of
   evidence means no group and ordinary all-land routing.
5. Compile/check a fixture. Validate unknown/overlapping groups and different-net
   assignments fail, and the desired group needs no redundant PCB bridge.
6. Normalized generation uses `part.json` with `"internal_pad_groups": [["1"],
   ["2"]]`; preserve this optional field through generation. Never hand-edit a
   generated package instead of its authoritative bundle.

CopperScript preserves internal groups in physical IR, routing closure and the
generated project-local footprint library. Exports using groups require KiCad
10 and use explicit jumper groups, not net ties or blanket DRC exclusions.
Bare-PCB copper remains physically disconnected where the component supplies
the connection; assembly-aware connectivity must be distinguished from bare
board continuity testing. Do not place fictitious copper in Gerbers.

## Verified examples

- Keystone 3034: conductive positive retainer joins the two KiCad pad-1 solder
  tabs. The negative PCB contact (pad 2) is separate and must reach GND.
  [Manufacturer catalogue, p9 figure 1 and 3034 row](https://www.keyelco.com/userAssets/file/M65p9.pdf).
  SHA-256: `58aa74ce778e2b3315b3388ff3feda6831b9b99ba4c1696358a7644b6d87c39a`.
- E-Switch TL3342F160QG: drawing P010632 rev J (2021-02-09), sheet 1 circuit
  shows terminals 1/2 permanently common and 3/4 permanently common, with SPST
  actuation between those groups. KiCad `SW_SPST_TL3342` numbers each pair 1 or
  2 (the drawing and footprint use different numbering conventions).
  [Manufacturer drawing](https://configured-product-images.s3.amazonaws.com/2D/specs/TL3342F160QG.pdf).
  SHA-256: `24633cbf6a2f784611d0986a0ca86333039d6dcf532db465342a1e659ab9ad6e`.

## Coin-cell negative contact / ground guidance

A PCB battery contact is not a soldered thermal pad. Inspect finish, mask,
mechanical contact height and via protection; an open drill is not a smooth
contact surface. Negative-contact geometry is manufacturer/footprint specific.

Read-only comparison of published PCB data (2026-10-03):

| Design | Negative contact | Connection observed |
| --- | --- | --- |
| [MVS adapter](https://github.com/bodgit/mvs-battery-holder) | 3.96 mm square | Surface trace to plated header; no vias in contact |
| [Redox wireless rev1](https://github.com/mattdibi/redox-keyboard/tree/master/redox-w/rev1.0W/pcb) | 3.96 mm square | Surface GND zones; no contact vias or dedicated contact track |
| [nRF52832 Morse Code Watch](https://github.com/bnezuld/MorseCodeWatchPCB) | 17.8 mm disc | Four GND vias centred inside the contact and another annulus overlapping its rim; surface GND traces/zones also present |

These are observed layouts, not manufacturing qualification or evidence that
many vias are required. CopperScript's nRF52 prototype retains one explicitly
approved filled/capped GND via-in-pad. Prefer a legal surface connection to GND
or an outside-contact via when available; add vias for a stated impedance,
current or redundancy requirement, not automatically based on pad area.
