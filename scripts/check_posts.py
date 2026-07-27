#!/usr/bin/env python3
"""
Structural checks over the MDX posts. Two things that are easy to break by
editing and invisible until someone reads the page:

  adjacency  Two figures or tables with nothing between them make the reader
             context-switch twice with no verbal bridge, and force the second
             caption to re-establish what the first already said. Prose between
             them should say what the second visual adds; if there is nothing to
             say, one of the two is not earning its place, so merge or cut
             rather than padding. A figure right after a heading, or after a
             callout, is fine and not reported.

  citations  Every [[n]] resolves to an entry in the reference list, the list
             has no orphans, and numbering follows first appearance. Moving a
             section silently invalidates all three.

Run:  python3 scripts/check_posts.py       (exit 1 if anything is reported)
"""

import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTS = sorted(glob.glob(os.path.join(ROOT, "src", "posts", "*.mdx")))


def visual_blocks(lines):
    """(kind, first_line, last_line) for each figure, markdown table and caption."""
    out, i = [], 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("<figure"):
            j = i
            while j < len(lines) and "</figure>" not in lines[j]:
                j += 1
            out.append(("figure", i, j))
            i = j + 1
        elif stripped.startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(("table", i, j - 1))
            i = j
        elif stripped.startswith('<p className="table-caption"'):
            out.append(("caption", i, i))
            i += 1
        else:
            i += 1
    return out


def check_adjacency(path, text):
    lines = text.split("\n")
    blocks = visual_blocks(lines)
    problems = []
    for first, second in zip(blocks, blocks[1:]):
        if "caption" in (first[0], second[0]):
            continue
        between = [
            l for l in lines[first[2] + 1:second[1]]
            if l.strip() and not l.strip().startswith('<p className="table-caption"')
        ]
        if not between:
            problems.append(
                f"  {os.path.basename(path)}:{first[1] + 1}: "
                f"{first[0]} followed by {second[0]} with nothing between"
            )
    return problems


def check_citations(path, text):
    name = os.path.basename(path)
    body, _, tail = text.partition('<ol className="references">')
    if not tail:
        return []
    listed = tail.count("<li>")
    order = []
    for m in re.finditer(r"\[\[(\d+)\]\]", body):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
    problems = []
    missing = [n for n in order if n > listed]
    if missing:
        problems.append(f"  {name}: cites {missing} but the list has {listed} entries")
    orphans = [n for n in range(1, listed + 1) if n not in order]
    if orphans:
        problems.append(f"  {name}: reference {orphans} listed but never cited")
    if order != sorted(order):
        problems.append(f"  {name}: not numbered by first appearance: {order}")
    return problems


def main():
    failures = []
    for path in POSTS:
        text = open(path).read()
        failures += check_adjacency(path, text)
        failures += check_citations(path, text)

    if failures:
        print(f"{len(failures)} problem(s):")
        print("\n".join(failures))
        return 1
    print(f"{len(POSTS)} posts: no adjacent visuals, citations resolve and are ordered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
