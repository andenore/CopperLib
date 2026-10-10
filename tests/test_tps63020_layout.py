"""Reusable asset contracts; these tests are not converter qualification."""
import importlib.util
import json
from pathlib import Path
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / "packages/circuits/ti/tps63020-buck-boost"
SPEC = importlib.util.spec_from_file_location("tps63020_layout", PACKAGE / "generate_layout.py")
GEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN)


class LayoutTests(unittest.TestCase):
    def test_deterministic_assets(self):
        for enabled, suffix in ((False, "always-on"), (True, "enabled-series-feedback")):
            expected = (json.dumps(GEN.generate(enabled), sort_keys=True, indent=2) + "\n").encode()
            self.assertEqual((PACKAGE / f"assets/tps63020-six-layer-{suffix}.json").read_bytes(), expected)

    def test_roles_ports_and_every_power_land(self):
        for enabled in (False, True):
            a = GEN.generate(enabled)
            roles = {(r, p): n for r, p, n in a["pad_nets"]}
            self.assertEqual(len(roles), len(a["pad_nets"]))
            self.assertEqual({p for r, p in roles if r == "U"}, {str(i) for i in range(1, 16)} - {"14"})
            self.assertEqual(a["isolated_pads"], [["U", "14"]])
            for p, net in ((4, "VOUT"), (5, "VOUT"), (6, "L2"), (7, "L2"),
                           (8, "L1"), (9, "L1"), (10, "VIN"), (11, "VIN")):
                entries = [t for t in a["tracks"] if t["net"] == net and {"pad": ["U", str(p)]} in t["points"]]
                self.assertEqual(len(entries), 1)
            for port in a["ports"]:
                self.assertEqual({tuple(p) for p in port["pads"]},
                                 {p for p, n in roles.items() if n == port["net"]})
                if port["net"] == "EN":
                    self.assertTrue(any(t["net"] == "EN" and t["layer"] == "F.Cu"
                        and t["points"] == [[8200000, -3000000], port["point"]] for t in a["tracks"]))
                    self.assertFalse(any(v["position_nm"] == port["point"] for v in a["vias"]))
                else:
                    self.assertTrue(any(v["net"] == port["net"] and v["position_nm"] == port["point"] for v in a["vias"]))
            self.assertEqual(len(a["members"]), 11 if enabled else 9)

    def test_ground_and_process_contract(self):
        for enabled in (False, True):
            a = GEN.generate(enabled)
            contacts = a["plane_returns"][0]["dedicated_contacts"]
            self.assertEqual(len(contacts), 6 if enabled else 5)
            self.assertEqual(len({tuple(c["via_position_nm"]) for c in contacts}), len(contacts))
            for c in contacts:
                self.assertTrue(any(v["net"] == "GND" and v["position_nm"] == c["via_position_nm"] for v in a["vias"]))
            self.assertTrue(all(v["size_nm"] == 600000 and v["drill_nm"] == 300000 and v["technology"] is None for v in a["vias"]))
            self.assertFalse(a["production_publishable"])
            self.assertTrue(a["unresolved"])
            self.assertEqual(a["allowed_rotations"], [0, 90, 180, 270])
            self.assertEqual({p["net"] for p in a["polygons"]}, {"VIN", "VOUT", "L1", "L2"})
            self.assertEqual(a["plane_returns"][0]["layers"], ["In1.Cu", "In4.Cu"])


    def test_explicit_branch_width_contracts(self):
        for enabled in (False, True):
            a = GEN.generate(enabled)
            self.assertEqual(a["schema"], "copperlib-physical-hard-macro/v0.4")
            rows = {c["track_index"]: c for c in a["width_contracts"]}
            self.assertEqual(len(rows), len(a["width_contracts"]))
            for i, t in enumerate(a["tracks"]):
                if t["width_nm"] < 800000 and t["net"] in {"VIN", "VOUT", "EN", "L1", "L2"}:
                    self.assertIn(i, rows)
                    self.assertEqual(rows[i]["minimum_width_nm"], t["width_nm"])
                    self.assertTrue(rows[i]["evidence"])
            self.assertTrue({"pin_entry", "control_supply", "output_sense", "enable"}.issubset({c["purpose"] for c in rows.values()}))


if __name__ == "__main__":
    unittest.main()
