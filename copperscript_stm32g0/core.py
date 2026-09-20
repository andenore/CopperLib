import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "data" / "evidence.jsonl"
OUT = ROOT / "generated" / "stm32g0b1cbt6-lqfp48-poc"

def facts():
    return [json.loads(line) for line in EVIDENCE.read_text(encoding="utf-8").splitlines() if line.strip()]

def validate():
    errors = []
    seen = set()
    for f in facts():
        for key in ("fact_id", "subject", "field", "status", "source_id", "locator"):
            if key not in f: errors.append(f"missing {key}: {f}")
        if f.get("fact_id") in seen: errors.append(f"duplicate fact_id: {f.get('fact_id')}")
        seen.add(f.get("fact_id"))
        if f.get("status") not in {"verified", "inferred", "unresolved", "illustrative"}: errors.append(f"bad status: {f}")
        if f.get("status") == "unresolved" and f.get("value") != "?": errors.append(f"unresolved value must be ?: {f}")
    return errors

def production_blocked():
    return any(f.get("status") == "unresolved" or f.get("value") == "?" for f in facts())

def generate():
    errors = validate()
    if errors: raise ValueError("; ".join(errors))
    OUT.mkdir(parents=True, exist_ok=True)
    fs = {f["subject"]: {} for f in facts() if f["field"] in {"package_pin", "alternate_functions"}}
    for f in facts():
        if f["subject"] in fs and f["status"] == "verified": fs[f["subject"]][f["field"]] = f["value"]
    (OUT / "device.json").write_text(json.dumps({"name":"STM32G0B1CBT6","family":"STM32G0B1","package":"LQFP48","scope":"proof-of-concept","production_publishable":not production_blocked()}, indent=2)+"\n", encoding="utf-8")
    with (OUT / "pins.csv").open("w", newline="", encoding="utf-8") as h:
        w=csv.writer(h); w.writerow(["name","package_pin","alternate_functions"])
        for name in sorted(fs): w.writerow([name, fs[name].get("package_pin","?"), "|".join(fs[name].get("alternate_functions",["?"]))])
    (OUT / "pads.csv").write_text("name,direction\nPA0,I/O\nPA1,I/O\nPC0,I/O\nPC1,I/O\n", encoding="utf-8")
    (OUT / "peripherals.csv").write_text("name\nGPIOA\nGPIOC\n", encoding="utf-8")
    (OUT / "mux.csv").write_text("pin,function\n"+"\n".join(f"{n},{af}" for n in sorted(fs) for af in fs[n].get("alternate_functions", []))+"\n", encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps({"generator":"copperscript-stm32g0-library","copperscript_revision":"ee63d69","evidence_sha256":hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),"files":sorted(p.name for p in OUT.iterdir() if p.is_file())}, indent=2)+"\n", encoding="utf-8")

def coverage():
    total = len({f["subject"] for f in facts() if f["field"] == "package_pin"})
    return {"orderable_part":"STM32G0B1CBT6","package":"LQFP48","verified_pins":total,"scope":"proof-of-concept","production_publishable":not production_blocked(),"unresolved_facts":sum(f.get("status")=="unresolved" for f in facts())}
