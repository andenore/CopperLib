"""Deterministic cross-vendor compatibility report for CopperScript ee63d69."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "data" / "case-studies"
REPORTS = ROOT / "reports"


def _read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _facts(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_report() -> dict[str, object]:
    index = _read(CASES / "index.json")
    definitions = {item["id"]: item for item in _read(CASES / "cases.json")["cases"]}
    result_cases = []
    for case_id in index["cases"]:
        case = definitions[case_id]
        sources = _read(CASES / case_id / "sources.json")["sources"]
        source_ids = {source["id"] for source in sources}
        facts = _facts(CASES / case_id / "evidence.jsonl")
        errors = []
        for fact in facts:
            if fact.get("source_id") not in source_ids:
                errors.append(f"{fact.get('fact_id')}: unknown source {fact.get('source_id')}")
        for concept in case["concepts"]:
            if concept["classification"] not in {"represented", "lossy", "unrepresentable", "expansion-risk"}:
                errors.append(f"{case_id}: invalid classification {concept['classification']}")
        result_cases.append({
            "id": case_id,
            "vendor": case["vendor"],
            "orderable_part": case["orderable_part"],
            "package": case["package"],
            "fixture": case["fixture"],
            "scope": case["scope"],
            "sources": sources,
            "production_publishable": False,
            "source_count": len(sources),
            "fact_count": len(facts),
            "concepts": case["concepts"],
            "validation_errors": errors,
        })
    return {"schema": "copperscript-device-model-compatibility/v0.1", "copperscript_revision": index["copperscript_revision"], "cases": result_cases}


def markdown(report: dict[str, object]) -> str:
    lines = ["# CopperScript device-model compatibility lab", "", f"CopperScript revision: `{report['copperscript_revision']}`", "", "All four cases are deliberately non-publishable bounded fixtures.", ""]
    for case in report["cases"]:
        lines.extend([f"## {case['orderable_part']} ({case['vendor']})", "", f"Package: {case['package']}; scope: {case['scope']}", "", "| Concept | Classification | Finding |", "|---|---|---|"])
        for concept in case["concepts"]:
            lines.append(f"| `{concept['id']}` | **{concept['classification']}** | {concept['note']} |")
        lines.extend(["", f"Evidence facts: {case['fact_count']}; sources: {case['source_count']}; production publishable: `false`.", ""])
        for source in case["sources"]:
            lines.append(f"Source: [{source['document']}]({source['url']}) — {source['revision']}; {source['locator']}")
        lines.append("")
    return "\n".join(lines)


def write_reports() -> dict[str, object]:
    report = build_report()
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "compatibility.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (REPORTS / "compatibility.md").write_text(markdown(report), encoding="utf-8")
    return report
