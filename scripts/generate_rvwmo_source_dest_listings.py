#!/usr/bin/env python3
"""Generate RVWMO source/destination listings include from a canonical text source.

This is a transitional generator: today the canonical input is a text snapshot
that can be replaced by UnifiedDB-derived content in a follow-up.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

HEADER = [
    "// This file is generated. Do not edit directly.",
    "// Source: src/unpriv/rvwmo-source-dest-listings.src.adoc",
    "",
]


def generate(src: Path, out: Path) -> None:
    body = src.read_text(encoding="utf-8")
    text = "\n".join(HEADER) + body
    if not text.endswith("\n"):
        text += "\n"
    out.write_text(text, encoding="utf-8")


def check(src: Path, out: Path) -> int:
    expected = "\n".join(HEADER) + src.read_text(encoding="utf-8")
    if not expected.endswith("\n"):
        expected += "\n"

    actual = out.read_text(encoding="utf-8") if out.exists() else ""
    if actual != expected:
        print(
            "RVWMO listing include is out of date. Run:\n"
            "  python3 scripts/generate_rvwmo_source_dest_listings.py",
            file=sys.stderr,
        )
        return 1
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--src",
        default="src/unpriv/rvwmo-source-dest-listings.src.adoc",
        help="Canonical source input file",
    )
    p.add_argument(
        "--out",
        default="src/unpriv/rvwmo-source-dest-listings.adoc",
        help="Generated include output file",
    )
    p.add_argument("--check", action="store_true", help="Check output is up to date")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    src = Path(args.src)
    out = Path(args.out)
    if args.check:
        raise SystemExit(check(src, out))
    generate(src, out)
