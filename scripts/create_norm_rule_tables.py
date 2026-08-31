#!/usr/bin/env python3
"""Generate an AsciiDoc appendix listing normative rules and linking back to the
specification text that defines them.

Inputs are the normative tag JSON produced by the "tags" Asciidoctor backend
(docs-resources/converters/tags.rb) and the normative rule definition YAML files
in normative_rule_defs/.  The tag JSON supplies both the tag text and the section
tree, which is what lets every row carry an xref back to the tagged text and to
its enclosing section.

Because the generated appendix contains only xrefs and defines no new "norm:"
tags, adding it to the manual does not change the tag JSON: the two-pass build
(tags -> appendix -> pdf/html) reaches a fixed point after one regeneration.

Usage:
    python3 scripts/create_norm_rule_tables.py \
        -t build/riscv-spec-norm-tags.json \
        -d normative_rule_defs/rv64.yaml \
        --rule-table scripts/default_norm_rule_table.yaml \
        --output-dir build/norm-rule-appendix
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    sys.exit("create_norm_rule_tables.py: ERROR: PyYAML is required")

PN = "create_norm_rule_tables.py"

# Rule name -> anchor prefix for the appendix row itself.  Deliberately distinct
# from the "norm:" prefix used for tags in the manual body so that the tags
# backend does not pick these up as normative tags.
RULE_ANCHOR_PREFIX = "nr:"

KNOWN_COLUMNS = {"RULE_NAME", "KIND", "SUMMARY", "CHAPTER", "LOCATION"}

_errors = 0
_warnings_only = False


def fatal(msg: str) -> None:
    sys.exit(f"{PN}: ERROR: {msg}")


def error(msg: str) -> None:
    """Report a recoverable problem, counted so main() can fail the build.

    Labelled WARNING rather than ERROR under -w, which is how a chapter that is
    still being tagged gets an appendix without failing the build.
    """
    global _errors
    _errors += 1
    label = "WARNING" if _warnings_only else "ERROR"
    print(f"{PN}: {label}: {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"{PN}: {msg}")


def safe_filename(name: str) -> str:
    """Map a rule name to a safe output filename stem."""
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)


def load_json_object(pathname: str) -> Dict[str, Any]:
    try:
        with open(pathname, encoding="utf-8") as f:
            obj = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        fatal(f"Can't load JSON file {pathname}: {exc}")
    if not isinstance(obj, dict):
        fatal(f"Expected a JSON object at the top level of {pathname}")
    return obj


def load_yaml_object(pathname: str) -> Dict[str, Any]:
    try:
        with open(pathname, encoding="utf-8") as f:
            obj = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as exc:
        fatal(f"Can't load YAML file {pathname}: {exc}")
    if not isinstance(obj, dict):
        fatal(f"Expected a YAML mapping at the top level of {pathname}")
    return obj


# ---------------------------------------------------------------------------
# Tag index
# ---------------------------------------------------------------------------


def build_tag_index(tag_fnames: List[str]) -> Dict[str, Dict[str, Any]]:
    """Return tag name -> {text, section_id, section_title, chapter_title, breadcrumb}.

    The section tree emitted by tags.rb nests volume -> part -> chapter -> section,
    with the document root as an untitled outermost node.  The "chapter" is taken
    to be the outermost titled ancestor below the volume, which is the level the
    normative rule definition files are organized around.
    """
    index: Dict[str, Dict[str, Any]] = {}

    for fname in tag_fnames:
        doc = load_json_object(fname)
        tags = doc.get("tags")
        sections = doc.get("sections")
        if not isinstance(tags, dict):
            fatal(f"{fname}: expected a 'tags' object")
        if not isinstance(sections, dict):
            fatal(f"{fname}: expected a 'sections' object")

        def walk(section: Dict[str, Any], ancestors: List[Dict[str, Any]]) -> None:
            chain = ancestors + [section]
            titled = [s for s in chain if s.get("title")]
            for tag_name in section.get("tags", []):
                if tag_name in index:
                    error(
                        f"Tag {tag_name!r} appears in more than one tag file; "
                        f"first in {index[tag_name]['tag_filename']}, again in {fname}"
                    )
                    continue
                section_id = section.get("id")
                if not section_id:
                    error(
                        f"Tag {tag_name!r} is in section {section.get('title')!r} "
                        "which has no id, so it cannot be linked to"
                    )
                    continue
                index[tag_name] = {
                    "text": tags.get(tag_name, ""),
                    "section_id": section_id,
                    "section_title": section.get("title") or "",
                    "volume_title": titled[0]["title"] if titled else "",
                    "chapter_title": titled[2]["title"] if len(titled) > 2 else "",
                    "breadcrumb": [s["title"] for s in titled],
                    "tag_filename": fname,
                }
            for child in section.get("children", []):
                walk(child, chain)

        walk(sections, [])

        for tag_name in tags:
            if tag_name not in index:
                error(f"{fname}: tag {tag_name!r} has no enclosing section")

    return index


# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------


def load_rules(def_fnames: List[str]) -> List[Dict[str, Any]]:
    """Flatten rule definition files into one rule per name.

    A definition entry may name several rules (`names:`) that share one set of
    tags, and may reference several tags (`tags:`) that together make up one
    self-contained rule.  Both are expanded here so that each output row is
    exactly one normative rule.
    """
    rules: List[Dict[str, Any]] = []
    seen: Dict[str, str] = {}

    for fname in def_fnames:
        doc = load_yaml_object(fname)
        chapter_name = doc.get("chapter_name")
        if not isinstance(chapter_name, str) or not chapter_name.strip():
            fatal(f"{fname}: expected a non-empty 'chapter_name'")

        defs = doc.get("normative_rule_definitions")
        if not isinstance(defs, list):
            fatal(f"{fname}: expected a 'normative_rule_definitions' list")

        for entry in defs:
            if not isinstance(entry, dict):
                fatal(f"{fname}: expected each normative rule definition to be a mapping")

            names = entry.get("names")
            if names is None:
                single = entry.get("name")
                if not isinstance(single, str):
                    fatal(f"{fname}: rule definition needs a 'name' or 'names'")
                names = [single]
            if not isinstance(names, list) or not names:
                fatal(f"{fname}: 'names' must be a non-empty list")

            tags = entry.get("tags")
            if tags is None:
                single_tag = entry.get("tag")
                tags = [single_tag] if isinstance(single_tag, str) else []
            if not isinstance(tags, list):
                fatal(f"{fname}: 'tags' must be a list")
            if not tags:
                error(f"{fname}: rule {names[0]!r} references no tags")

            instances = entry.get("instances")
            if instances is None:
                single_instance = entry.get("instance")
                instances = [single_instance] if isinstance(single_instance, str) else []

            for name in names:
                if name in seen:
                    error(
                        f"Duplicate normative rule name {name!r} in {fname}; "
                        f"already defined in {seen[name]}"
                    )
                    continue
                seen[name] = fname
                rules.append(
                    {
                        "name": name,
                        "tags": list(tags),
                        "summary": entry.get("summary"),
                        "description": entry.get("description"),
                        "kind": entry.get("kind"),
                        "instances": instances,
                        "impl_def_behavior": bool(entry.get("impl-def-behavior")),
                        "impl_def_category": entry.get("impl-def-category"),
                        "def_filename": fname,
                        "chapter_name": chapter_name,
                    }
                )

    return rules


# ---------------------------------------------------------------------------
# Cell rendering
# ---------------------------------------------------------------------------


def literal(text: str) -> str:
    """Render text as an AsciiDoc monospace literal, immune to inline substitutions."""
    delim = "+"
    while delim in text:
        delim += "+"
    return f"`{delim}{text}{delim}`"


def inline_text(text: str) -> str:
    """Collapse whitespace and escape the cell separator."""
    return re.sub(r"\s+", " ", text.strip()).replace("|", "\\|")


def render_rule_name_cell(rule: Dict[str, Any]) -> str:
    name = rule["name"]
    anchor = f"{RULE_ANCHOR_PREFIX}{name}"
    lines = ["a|", f"[#{anchor}]#{literal(name)}#"]
    if rule["impl_def_behavior"]:
        category = rule["impl_def_category"]
        suffix = f" ({category})" if isinstance(category, str) and category else ""
        lines += ["", f"[.small]#Implementation-defined behavior{suffix}#"]
    return "\n".join(lines)


def render_kind_cell(rule: Dict[str, Any]) -> str:
    kind = rule["kind"]
    if not isinstance(kind, str) or not kind:
        return "|"
    parts = [kind.replace("_", " ")]
    instances = [i for i in rule["instances"] if isinstance(i, str) and i]
    if instances:
        parts.append(", ".join(literal(i) for i in instances))
    return "a|\n" + "\n\n".join(parts)


def render_summary_cell(rule: Dict[str, Any]) -> str:
    for key in ("summary", "description"):
        value = rule[key]
        if isinstance(value, str) and value.strip():
            return "| " + inline_text(value)
    return "| See linked specification text"


def render_chapter_cell(rule: Dict[str, Any]) -> str:
    return "| " + inline_text(rule["chapter_name"])


def render_location_cell(rule: Dict[str, Any], tag_index: Dict[str, Dict[str, Any]]) -> str:
    """One bullet per tag: an xref to the tagged text, then one to its section.

    Link text is always supplied explicitly for the tag xref.  A bare <<norm:x>>
    would render as the fallback "[norm:x]", which scripts/check_xref_fallbacks.py
    treats as a build failure.  Section xrefs are left bare on purpose so that
    :xrefstyle: short renders them as "Section N.N".
    """
    lines = ["a|"]
    for tag_name in rule["tags"]:
        entry = tag_index.get(tag_name)
        if entry is None:
            error(f"Rule {rule['name']!r} references unknown tag {tag_name!r}")
            lines.append(f"* {literal(tag_name)} (tag not found)")
            continue
        lines.append(
            f"* <<{tag_name},{literal(tag_name)}>> in <<{entry['section_id']}>>"
        )
    if len(lines) == 1:
        lines.append("* (no tags)")
    return "\n".join(lines)


def render_row(
    rule: Dict[str, Any],
    columns: List[Dict[str, Any]],
    tag_index: Dict[str, Dict[str, Any]],
) -> str:
    renderers = {
        "RULE_NAME": lambda: render_rule_name_cell(rule),
        "KIND": lambda: render_kind_cell(rule),
        "SUMMARY": lambda: render_summary_cell(rule),
        "CHAPTER": lambda: render_chapter_cell(rule),
        "LOCATION": lambda: render_location_cell(rule, tag_index),
    }
    cells = []
    for col in columns:
        col_id = col["column"]
        renderer = renderers.get(col_id)
        if renderer is None:
            fatal(f"Internal error: unsupported column identifier {col_id!r}")
        cells.append(renderer())
    return "\n".join(cells) + "\n"


# ---------------------------------------------------------------------------
# Table layout config
# ---------------------------------------------------------------------------


def load_table_config(pathname: str) -> List[Dict[str, Any]]:
    doc = load_yaml_object(pathname)
    columns = doc.get("columns")
    if not isinstance(columns, list) or not columns:
        fatal(f"{pathname}: expected a non-empty 'columns' list")
    total = 0
    for col in columns:
        if not isinstance(col, dict):
            fatal(f"{pathname}: each column must be a mapping")
        for key in ("name", "column", "width_pct"):
            if key not in col:
                fatal(f"{pathname}: column is missing required key {key!r}")
        if col["column"] not in KNOWN_COLUMNS:
            fatal(
                f"{pathname}: unknown column identifier {col['column']!r}; "
                f"expected one of {', '.join(sorted(KNOWN_COLUMNS))}"
            )
        total += int(col["width_pct"])
    if total != 100:
        fatal(f"{pathname}: column width_pct values total {total}, expected 100")
    return columns


def render_cols_spec(columns: List[Dict[str, Any]]) -> str:
    return ",".join(f"{col['width_pct']}%" for col in columns)


def render_header_row(columns: List[Dict[str, Any]]) -> str:
    return "| " + " | ".join(str(col["name"]) for col in columns)


def table_open(columns: List[Dict[str, Any]], title: Optional[str] = None) -> List[str]:
    lines = []
    if title:
        lines.append(f".{title}")
    lines += [
        f'[cols="{render_cols_spec(columns)}",options="header"]',
        "|===",
        render_header_row(columns),
        "",
    ]
    return lines


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def write_file(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def write_outputs(
    rules: List[Dict[str, Any]],
    columns: List[Dict[str, Any]],
    tag_index: Dict[str, Dict[str, Any]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # Per-rule row fragments, grouped into a directory per definition file.
    chapter_rules: Dict[str, List[Tuple[str, Dict[str, Any]]]] = {}
    chapter_titles: Dict[str, str] = {}
    seen_stems: Dict[str, str] = {}

    for rule in rules:
        stem = safe_filename(rule["name"])
        chapter_dir_name = Path(rule["def_filename"]).stem
        key = f"{chapter_dir_name}/{stem}"
        if key in seen_stems:
            fatal(
                f"Rule names {seen_stems[key]!r} and {rule['name']!r} collide after "
                "filename sanitization"
            )
        seen_stems[key] = rule["name"]

        existing = chapter_titles.get(chapter_dir_name)
        if existing is not None and existing != rule["chapter_name"]:
            fatal(
                f"Conflicting chapter_name for {rule['def_filename']}: "
                f"{existing!r} vs {rule['chapter_name']!r}"
            )
        chapter_titles[chapter_dir_name] = rule["chapter_name"]

        write_file(
            output_dir / chapter_dir_name / "rules" / f"{stem}.adoc",
            [render_row(rule, columns, tag_index)],
        )
        chapter_rules.setdefault(chapter_dir_name, []).append((stem, rule))

    # Per-chapter include of that chapter's rows, in definition-file order.
    for chapter_dir_name, entries in chapter_rules.items():
        write_file(
            output_dir / chapter_dir_name / "rules" / "all_norm_rules.adoc",
            [f"include::{stem}.adoc[]" for stem, _ in entries],
        )

    # Chapter-organized appendix body: one table per chapter.
    by_chapter: List[str] = []
    for chapter_dir_name, entries in chapter_rules.items():
        title = chapter_titles[chapter_dir_name]
        by_chapter.append(f"=== {title}")
        by_chapter.append("")
        by_chapter += table_open(columns, f"Normative rules for {title}")
        by_chapter.append(f"include::{chapter_dir_name}/rules/all_norm_rules.adoc[]")
        by_chapter.append("|===")
        by_chapter.append("")
    write_file(output_dir / "all_norm_rules_by_chapter.adoc", by_chapter)

    # One A-Z table across every chapter.
    a_to_z: List[str] = table_open(columns, "Normative rules, A to Z")
    for stem, rule in sorted(
        ((stem, rule) for entries in chapter_rules.values() for stem, rule in entries),
        key=lambda pair: pair[1]["name"].lower(),
    ):
        chapter_dir_name = Path(rule["def_filename"]).stem
        a_to_z.append(f"include::{chapter_dir_name}/rules/{stem}.adoc[]")
    a_to_z.append("|===")
    write_file(output_dir / "all_norm_rules_a_to_z.adoc", a_to_z)

    info(
        f"Wrote {len(rules)} normative rules across {len(chapter_rules)} chapter(s) "
        f"to {output_dir}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=PN,
        description="Generate an AsciiDoc appendix of normative rules that links "
        "back to the specification text defining each rule.",
    )
    parser.add_argument(
        "-t",
        "--tags",
        required=True,
        action="append",
        metavar="FILE",
        help="normative tag JSON file (repeatable)",
    )
    parser.add_argument(
        "-d",
        "--rule-def",
        required=True,
        action="append",
        metavar="FILE",
        help="normative rule definition YAML file (repeatable)",
    )
    parser.add_argument(
        "--rule-table",
        default=str(Path(__file__).with_name("default_norm_rule_table.yaml")),
        metavar="FILE",
        help="table layout YAML file (default: scripts/default_norm_rule_table.yaml)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        metavar="DIR",
        help="directory to write the generated .adoc files into",
    )
    parser.add_argument(
        "-w",
        "--warnings-only",
        action="store_true",
        help="report unresolved tags and duplicate names as warnings instead of "
        "failing; useful while a chapter is still being tagged",
    )
    return parser.parse_args()


def main() -> int:
    global _warnings_only
    args = parse_args()
    _warnings_only = args.warnings_only

    columns = load_table_config(args.rule_table)
    tag_index = build_tag_index(args.tags)
    rules = load_rules(args.rule_def)

    write_outputs(rules, columns, tag_index, Path(args.output_dir))

    if _errors and not _warnings_only:
        print(f"{PN}: {_errors} error(s); rerun with -w to downgrade to warnings",
              file=sys.stderr)
        return 1
    if _errors:
        info(f"{_errors} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
