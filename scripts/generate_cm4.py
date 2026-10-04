"""Deterministically render passive CM4 carrier sockets from reviewed pin facts.

No download, PDF heuristics or inferred firmware/mux behavior in generation.
The source PDF and reference ZIP stay in ignored cache/cm4; pinout.json is the
authoritative compact table. This is not an active Compute Module device model.
"""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
FOOTPRINT = "Connector_Hirose_DF40:Hirose_DF40C-100DS-0.4V_2x50_P0.4mm"


def render(data, offset, name):
    rows = data["pins"]
    if [row["cm4_pin"] for row in rows] != list(range(1, 201)):
        raise ValueError("CM4 pin table must contain every pin 1..200 exactly once")
    source = data["source"]
    lines = [
        "// Generated from data/cm4/pinout.json by scripts/generate_cm4.py.",
        "// Carrier socket, not an active CM4 device model; signal contacts are passive.",
        "// MPN: Hirose DF40C-100DS-0.4V(51). Local socket numbers always run 1..100.",
        f"part {name} {{",
        '    category = "connector.compute_module.cm4";',
        '    manufacturer = "Hirose Electric";',
        f'    footprint = "{FOOTPRINT}";',
        '    source_document = "Raspberry Pi Compute Module 4 datasheet";',
        '    source_location = "Table 6, printed pages 16-22; CM4IO v5 PCB establishes socket orientation";',
        f'    source_url = "{source["url"]}";',
        f'    source_checksum = "sha256:{source["sha256"]}";',
    ]
    for row in rows[offset:offset + 100]:
        n, signal = row["cm4_pin"], row["signal"]
        prefix = {"GND": "GND", "+5V": "V5", "CM4_3.3V": "V3V3",
                  "CM4_1.8V": "V1V8", "Reserved": "RESERVED"}.get(signal)
        pin = f"{prefix}_{n}" if prefix else signal
        power = signal in {"+5V", "GPIO_VREF", "CM4_3.3V", "CM4_1.8V"}
        domain = "ground" if signal == "GND" else "power" if power else (
            "analog" if signal.startswith("Analog") or signal == "VDAC_COMP" else "digital")
        direction = "input" if signal in {"+5V", "GPIO_VREF"} else "passive"
        required = signal in {"GND", "+5V", "GPIO_VREF"}
        policy = "do_not_connect" if signal == "Reserved" else "required" if required else "optional"
        voltage = ' voltage_min = 4.75V; voltage_max = 5.25V;' if signal == "+5V" else ""
        lines.append(f'    pin {pin} {{ number = "{n-offset}"; domains = "{domain}"; '
                     f'directions = "{direction}"; connection = "{policy}";{voltage} }}')
    return "\n".join([*lines, "}", ""])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on stale generated files; never write")
    args = parser.parse_args()
    data = json.loads((ROOT / "data/cm4/pinout.json").read_text(encoding="utf-8"))
    for offset, name, filename in [(0, "CM4_GPIO_SOCKET", "gpio_socket.copper"),
                                   (100, "CM4_HS_SOCKET", "high_speed_socket.copper")]:
        target = ROOT / "packages/raspberry_pi_cm4" / filename
        text = render(data, offset, name)
        if args.check:
            if target.read_text(encoding="utf-8") != text:
                raise SystemExit(f"stale generated file: {target}")
        else:
            target.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
