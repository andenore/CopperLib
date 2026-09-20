import argparse, json
from .core import coverage, generate, validate

def main():
    p=argparse.ArgumentParser(); p.add_argument("command", choices=["validate","generate","coverage"]); a=p.parse_args()
    if a.command == "validate":
        e=validate()
        if e: raise SystemExit("\n".join(e))
        print("valid")
    elif a.command == "generate": generate(); print("generated")
    else: print(json.dumps(coverage(), indent=2))
