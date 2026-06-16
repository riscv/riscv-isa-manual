#!/usr/bin/env python3
"""Check rendered HTML for cross-reference fallback text (e.g., <a href="#ref">[ref]</a>)."""

import sys
from html.parser import HTMLParser
from pathlib import Path


class LinkTextParser(HTMLParser):
    """Extract href/text pairs from anchor elements."""

    def __init__(self):
        """Initialize parser."""
        super().__init__()
        self.in_a = False
        self.href = None
        self.text_parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        """Start collecting text when entering an anchor."""
        if tag == "a":
            self.in_a = True
            self.href = dict(attrs).get("href", "")
            self.text_parts = []

    def handle_data(self, data):
        """Collect visible text while inside an anchor."""
        if self.in_a:
            self.text_parts.append(data)

    def handle_endtag(self, tag):
        """Store the completed link when leaving an anchor."""
        if tag == "a" and self.in_a:
            text = "".join(self.text_parts).strip()
            self.links.append((self.href, text))
            self.in_a = False
            self.href = None
            self.text_parts = []


def is_fallback(text):
    """Return True when link text is fully wrapped in brackets."""
    return bool(text) and text.startswith("[") and text.endswith("]")


def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("usage: check_xref_fallbacks.py <html-files>", file=sys.stderr)
        sys.exit(22)

    found_fallback = False

    for filename in sys.argv[1:]:
        path = Path(filename)
        html = path.read_text(encoding="utf-8", errors="replace")

        parser = LinkTextParser()
        parser.feed(html)

        bad = []
        for href, text in parser.links:
            if href.startswith("#") and is_fallback(text):
                bad.append((href[1:], text))

        if bad:
            found_fallback = True
            print(f"Fallback xrefs found in {path.name}:")
            for href, text in bad:
                print(f"  {href} -> {text}")

    if found_fallback:
        sys.exit(1)


if __name__ == "__main__":
    main()
