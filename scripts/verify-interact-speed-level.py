#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED = {
    "1x": 100,
    "1.5x": 150,
    "2x": 200,
    "3x": 300,
    "4x": 400,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an openFPGA interact.json Speed Level menu.")
    parser.add_argument("interact_json", type=Path)
    args = parser.parse_args()

    data = json.loads(args.interact_json.read_text(encoding="utf-8-sig"))
    variables = data.get("interact", {}).get("variables", [])
    speed = next((item for item in variables if isinstance(item, dict) and item.get("name") == "Speed Level"), None)
    if speed is None:
        print("error: missing Speed Level variable")
        return 1

    actual = {str(option.get("name")): option.get("value") for option in speed.get("options", []) if isinstance(option, dict)}
    missing = {name: value for name, value in EXPECTED.items() if actual.get(name) != value}
    if missing:
        print(f"error: unexpected Speed Level options: {actual}")
        return 1

    if speed.get("type") != "list":
        print(f"error: Speed Level type should be list, got {speed.get('type')!r}")
        return 1

    if not speed.get("persist"):
        print("error: Speed Level should be persistent")
        return 1

    formatted = ", ".join(f"{name}={value}" for name, value in EXPECTED.items())
    print(f"ok: Speed Level has options {formatted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
