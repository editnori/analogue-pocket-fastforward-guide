#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


REVERSE_TABLE = bytes(int(f"{byte:08b}"[::-1], 2) for byte in range(256))


def reverse_bits_per_byte(source: Path, target: Path) -> None:
    data = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data.translate(REVERSE_TABLE))


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a Quartus .rbf to an Analogue Pocket .rbf_r by reversing bits in each byte.")
    parser.add_argument("source", type=Path, help="Quartus .rbf input")
    parser.add_argument("target", type=Path, help="Pocket .rbf_r output")
    args = parser.parse_args()
    reverse_bits_per_byte(args.source, args.target)
    print(f"wrote {args.target} ({args.target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
