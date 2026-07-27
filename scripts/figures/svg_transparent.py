#!/usr/bin/env python3
"""Strip opaque white background plates from converted SVG figures.

pdf2svg keeps matplotlib's white canvas and per-axes plates as large white
paths. Removing them leaves the ink on a transparent background, so a figure
sits on whatever the page background is — which is what lets one asset serve
both the light and the dark theme (dark mode inverts the ink with a CSS filter;
inversion leaves alpha=0 areas alone).

Only *large* white shapes go: small white fills are usually marker faces or
label halos and must stay.

Usage: svg_transparent.py FILE...   (edits in place)
"""
import re
import sys

# Two dialects: pdf2svg writes percentage rgb() fills, matplotlib's own SVG
# writer emits a style attribute. The style form is matched only when white is
# the whole declaration, so stroked white shapes (legend frames, marker faces)
# are never candidates.
WHITE = re.compile(
    r'fill="rgb\(100%,\s*100%,\s*100%\)"|style="fill: ?#ffffff"'
)
NUM = re.compile(r'-?\d+(?:\.\d+)?')
AREA_FRACTION = 0.03  # drop white shapes covering >=3% of the canvas


def canvas_area(svg: str) -> float:
    m = re.search(r'viewBox="([\d.\s-]+)"', svg)
    if not m:
        return 0.0
    _, _, w, h = (float(v) for v in m.group(1).split())
    return w * h


def strip(path: str) -> tuple[int, int]:
    svg = open(path).read()
    total = canvas_area(svg)
    if not total:
        return 0, 0

    removed = kept = 0
    out = []
    for element in re.split(r'(<path[^>]*/>)', svg):
        if element.startswith('<path') and WHITE.search(element):
            d = re.search(r'\sd="([^"]*)"', element)
            coords = [float(v) for v in NUM.findall(d.group(1))] if d else []
            xs, ys = coords[0::2], coords[1::2]
            area = (max(xs) - min(xs)) * (max(ys) - min(ys)) if xs and ys else 0.0
            if area >= AREA_FRACTION * total:
                removed += 1
                continue
            kept += 1
        out.append(element)

    open(path, 'w').write(''.join(out))
    return removed, kept


if __name__ == '__main__':
    for f in sys.argv[1:]:
        r, k = strip(f)
        print(f'{f.split("/")[-1]:<26} removed {r} plate(s), kept {k} small white fill(s)')
