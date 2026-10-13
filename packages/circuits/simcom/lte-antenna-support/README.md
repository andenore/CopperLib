# LTE direct-coax support, conditional reference adaptation

HOST -> 0 ohm link -> 100 pF DC block -> ANTENNA, with two unpopulated
0402 shunt tuning lands and connector-side RClamp1561PQTCT protection.
The series defaults follow SIM7672X Hardware Design V1.01 Figure30,
pp58-59, under the consumer's explicit applicability assumption. The figure
includes an RF test connector; this direct-coax topology is an adaptation,
not a verbatim reference layout. The 100 pF value is an initial setting, not
proof of antenna match. Select a C0G/NP0 RF capacitor with reviewed voltage,
loss and self-resonance, then tune the complete installed path.

Pin-relative placement bounds are authored compactness goals, not vendor
numerical limits. Consumers must keep each signal segment surface-only over
continuous reference ground, constrain total host-to-connector length, put
the TVS at the connector launch with a short ground return, and verify the
actual pad transitions. Importing the module does not establish those facts.

RClamp1561PQ Rev2.1 has a bidirectional 15 V working rating. Its 250 fF typical
and 300 fF maximum capacitances are specified at **15 V bias**, not at zero
bias. The unbiased feed requires S-parameter/nonlinearity review. Its transient
clamp can exceed the modem's permissible input: a diode rating alone does not
qualify system ESD protection. Verify RF peaks under mismatch and ESD response.

Generic DNP lands are absent from assembled BOM selections, but remain in the
physical design. Verify CPL/DNP handling independently before ordering. Exact
Semtech candidate JLCPCB C20336388 is not a similarly named clone; live assembly
stock must be checked at order time. External antennas are installed after PCBA.

Source hashes and unclosed RF obligations are in qualification.json.
production_publishable = false; no installed matching or ESD test is implied.
