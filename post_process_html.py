#!/usr/bin/env python3
import re, sys
from pathlib import Path

def process_html(html_path):
    content = Path(html_path).read_text(encoding='utf-8')

    pattern = re.compile(
        r'<img([^>]*?)alt="([^"]*)"([^>]*?)>',
        re.IGNORECASE | re.DOTALL
    )

    count = 0
    def replace_match(m):
        nonlocal count
        before = m.group(1)
        alt = m.group(2)
        after = m.group(3)

        if '.svg' not in (before + after):
            return m.group(0)

        if alt == "Diagram" or alt == "":
            alt = "Instruction encoding diagram"

        count += 1
        # Wrap in figure with visible caption
        return f'<figure><img{before}alt="{alt}"{after}><figcaption style="clip:rect(0 0 0 0);clip-path:inset(50%);height:1px;overflow:hidden;position:absolute;white-space:nowrap;width:1px">{alt}</figcaption></figure>'

    new_content = pattern.sub(replace_match, content)
    Path(html_path).write_text(new_content, encoding='utf-8')
    print(f"Fixed {count} diagrams in {html_path}")

if __name__ == '__main__':
    process_html(sys.argv[1])