"""Run the CopperScript CLI on fixture boards and read its public JSON output.

Tests assert package facts on what `copper compile`, `copper check` and
`copper query` print, never on compiler internals. COPPER overrides the
command (for example `COPPER=copper` or a Rust build); COPPERSCRIPT_SOURCE
points the default `python -m copperscript` at a source checkout.
"""
import atexit
import functools
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMAND = shlex.split(os.environ["COPPER"]) if os.environ.get("COPPER") else [sys.executable, "-m", "copperscript"]


class CopperError(Exception):
    """The CLI rejected a fixture; the message is what it printed."""


def _environment():
    environment = {**os.environ, "PYTHONUTF8": "1"}
    source = os.environ.get("COPPERSCRIPT_SOURCE")
    if source:
        environment["PYTHONPATH"] = os.pathsep.join(filter(None, (source, os.environ.get("PYTHONPATH"))))
    return environment


@functools.cache
def _workspace() -> Path:
    directory = Path(tempfile.mkdtemp(prefix="copperlib-tests-"))
    atexit.register(shutil.rmtree, directory, True)
    (directory / "copper.mod").write_text(
        "module copperlib-test\nrequire github.com/andenore/CopperLib v0.1.0\n"
        f"replace github.com/andenore/CopperLib => {ROOT.as_posix()}\n", encoding="utf-8")
    return directory


def board_file(source: str) -> Path:
    """Write a fixture board into a workspace that resolves CopperLib to this checkout."""
    path = _workspace() / f"{hashlib.sha256(source.encode()).hexdigest()[:16]}.copper"
    if not path.exists():
        path.write_text(source, encoding="utf-8")
    return path


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([*COMMAND, *args], cwd=_workspace(), env=_environment(),
                          capture_output=True, text=True, encoding="utf-8", check=False)


def _failure(result: subprocess.CompletedProcess) -> CopperError:
    return CopperError("\n".join(filter(None, (result.stdout.strip(), result.stderr.strip()))))


def _json(result: subprocess.CompletedProcess):
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise _failure(result) from None


@functools.cache
def _compile(source: str) -> str:
    board = board_file(source)
    output = board.with_suffix(".json")
    result = run("compile", str(board), "--no-check", "--offline", "-o", str(output))
    if result.returncode:
        raise _failure(result)
    return output.read_text(encoding="utf-8")


def compile_board(source: str) -> dict:
    """`copper compile` JSON IR, emitted even when ERC fails."""
    return json.loads(_compile(source))


@functools.cache
def _check(source: str, pins: str) -> str:
    return json.dumps(_json(run("check", str(board_file(source)), "--json", "--offline", "--pins", pins)))


def check(source: str, pins: str = "off") -> list[dict]:
    """`copper check --json` diagnostics; unmarked pins are off unless asked for."""
    return json.loads(_check(source, pins))["diagnostics"]


def codes(diagnostics) -> set[tuple[str, str]]:
    return {(item["code"], item["subject"]) for item in diagnostics}


@functools.cache
def _query(source: str, *args: str) -> str:
    return json.dumps(_json(run("query", str(board_file(source)), *args, "--json", "--offline")))


def query(source: str, *args: str) -> dict:
    return json.loads(_query(source, *args))


def flat_components(source: str) -> dict[str, dict]:
    """Flattened components by hierarchical reference, each with its `pin_list`."""
    return {item["ref"]: query(source, "component", item["ref"])["component"]
            for item in query(source, "components")["components"]}


def flat_nets(source: str) -> dict[str, set[tuple[str, str]]]:
    """Flattened net name -> {(component, pin)} endpoints."""
    nets: dict[str, set[tuple[str, str]]] = {}
    for ref, component in flat_components(source).items():
        for pin in component["pin_list"]:
            for net in pin["nets"]:
                nets.setdefault(net, set()).add((ref, pin["pin"]))
    return nets


def part(design: dict, name: str) -> dict:
    """A compiled part with its pins keyed by name."""
    (item,) = [item for item in design["parts"] if item["name"] == name]
    return {**item, "pins": {pin["name"]: pin for pin in item["pins"]}}


def device(design: dict, name: str) -> dict:
    """A compiled device with its pads and groups keyed by name."""
    (item,) = [item for item in design["devices"] if item["name"] == name]
    return {**item, "pads": {pad["name"]: pad for pad in item["pads"]},
            "signal_groups": {group["name"]: group for group in item["signal_groups"]},
            "mode_groups": {group["name"]: group for group in item["mode_groups"]}}


def pins(design: dict, name: str) -> dict[str, str]:
    """Pin name -> pad number of a compiled part."""
    return {pin["name"]: pin["number"] for pin in part(design, name)["pins"].values()}


def endpoint(text: str) -> tuple[str, str]:
    component, _, pin = text.rpartition(".")
    return component, pin


@functools.cache
def _audit(source: str, roots: tuple[str, ...], strict: bool) -> str:
    arguments = [argument for root in roots for argument in ("--footprint-root", root)]
    return json.dumps(_json(run("audit-footprints", str(board_file(source)), *(["--strict"] if strict else []),
                                "--offline", "--json", *arguments)))


def audit_footprints(source: str, *roots: Path, strict: bool = True) -> dict:
    """`copper audit-footprints --json`: each selected footprint resolves and its
    numbered pads equal its part's pin numbers. Installed KiCad library
    footprints carry lossy-import warnings (ignored user text), so audit them
    with strict=False."""
    return json.loads(_audit(source, tuple(str(root) for root in roots), strict))


@functools.cache
def _snapshot(source: str) -> str:
    board = board_file(source)
    output = board.with_suffix(".assembly.lock")
    output.unlink(missing_ok=True)
    result = run("assembly", "snapshot", str(board), "--offline", "-o", str(output))
    if result.returncode:
        raise _failure(result)
    return output.read_text(encoding="utf-8")


def assembly_snapshot(source: str) -> dict:
    """`copper assembly snapshot`: the assembly lock a board would start from."""
    return json.loads(_snapshot(source))
