#!/usr/bin/env python3
"""Reject normative-rule tags inside admonition blocks (NOTE, TIP, IMPORTANT, WARNING, CAUTION).

Admonitions are non-normative, so a ``norm:`` tag must not appear inside one, nor as an anchor
on the line just before one (which would tag the admonition itself).
"""

import re
import sys
from pathlib import Path

ADMONITIONS = "NOTE|TIP|IMPORTANT|WARNING|CAUTION"
STYLE_LINE = re.compile(rf"^\[(?:{ADMONITIONS})(?:[,\]])")
PARAGRAPH = re.compile(rf"^(?:{ADMONITIONS}):\s")
ATTRIBUTE_LINE = re.compile(r"^\[[^\]]*\]\s*$")
DELIMITER = re.compile(r"^(={4,}|\*{4,}|-{4,}|_{4,}|\.{4,}|--)\s*$")
TAG = re.compile(r"norm:([A-Za-z0-9_.-]+)")
ANCHOR_ONLY = re.compile(r"^\s*(?:\[\[norm:[^\]]+\]\]|\[#norm:[^\]]+\])\s*$")


def check(path):
    """Return (line, tag) pairs for norm tags inside or attached to admonitions."""
    lines = path.read_text(encoding="utf-8").splitlines()
    found = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if STYLE_LINE.match(line) or PARAGRAPH.match(line):
            # An anchor on the line just before the admonition tags the admonition.
            j = i - 1
            while j >= 0 and ATTRIBUTE_LINE.match(lines[j]) and not ANCHOR_ONLY.match(lines[j]):
                j -= 1
            if j >= 0 and ANCHOR_ONLY.match(lines[j]):
                found += [(j + 1, t) for t in TAG.findall(lines[j])]
        if PARAGRAPH.match(line):
            start = i
            while i < len(lines) and lines[i].strip():
                i += 1
            found += [(k + 1, t) for k in range(start, i) for t in TAG.findall(lines[k])]
            continue
        if STYLE_LINE.match(line):
            i += 1
            while i < len(lines) and ATTRIBUTE_LINE.match(lines[i]):
                i += 1
            if i < len(lines) and DELIMITER.match(lines[i]):
                delim = lines[i].strip()
                i += 1
                start = i
                while i < len(lines) and lines[i].strip() != delim:
                    i += 1
            else:  # style applied to the next paragraph
                start = i
                while i < len(lines) and lines[i].strip():
                    i += 1
            found += [(k + 1, t) for k in range(start, min(i, len(lines))) for t in TAG.findall(lines[k])]
        i += 1
    return found


def main(argv):
    """Check the given AsciiDoc files and report every offending tag."""
    errors = 0
    for name in argv:
        for line, tag in check(Path(name)):
            print(f"{name}:{line}: normative-rule tag norm:{tag} is inside or on an admonition block")
            errors += 1
    if errors:
        print(f"{errors} normative-rule tag(s) in admonition blocks; move the text out or drop the tag.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
