from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "data" / "bundles" / "stm32g0b1"
OUTPUT = ROOT / "generated"
REQUESTS = ROOT / "data" / "requests.json"
EVIDENCE = ROOT / "data" / "evidence.jsonl"


def devicegen_env() -> dict[str, str]:
    env = os.environ.copy()
    source = env.get("COPPERSCRIPT_SOURCE")
    if source:
        env["PYTHONPATH"] = str(Path(source)) + os.pathsep + env.get("PYTHONPATH", "")
    return env


def devicegen(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pcbir.devicegen", *args],
        cwd=ROOT,
        env=devicegen_env(),
        text=True,
        capture_output=capture,
        check=False,
    )


def validate() -> None:
    result = devicegen("validate", str(BUNDLE), capture=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def generate() -> None:
    validate()
    result = devicegen("generate", str(BUNDLE), "--out-dir", str(OUTPUT), capture=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def check() -> None:
    result = devicegen("check", str(BUNDLE), "--out-dir", str(OUTPUT), capture=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def coverage() -> dict[str, object]:
    request = json.loads(REQUESTS.read_text(encoding="utf-8"))["requests"][0]
    facts = [json.loads(line) for line in EVIDENCE.read_text(encoding="utf-8").splitlines() if line]
    return {
        "orderable_part": request["orderable_part"],
        "package": request["package"],
        "verified_package_pins": sum(f["field"] == "package_pin" and f["status"] == "verified" for f in facts),
        "covered_pads": 4,
        "peripheral_signals": 0,
        "mux_options": 0,
        "scope": request["scope"],
        "complete_coverage": request["complete_coverage"],
        "production_publishable": False,
        "unresolved_facts": sum(f["status"] == "unresolved" for f in facts),
        "illustrative_facts": sum(f["status"] == "illustrative" for f in facts),
    }
