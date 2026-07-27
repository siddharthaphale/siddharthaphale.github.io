"""
Generate the 1200x630 link-preview card (public/assets/images/og-card.png).

Social platforms crop or letterbox anything that is not roughly 1.91:1, and the
only other image on the site is a 600x800 portrait, so the card is drawn here
instead. It follows the site's own vocabulary: paper background, monospace
wordmark, a cardinal hairline, sans subtitle. Menlo stands in for Space Mono and
Helvetica for Source Sans 3, since those two are webfonts and this file has to be
a static PNG.

Run:  python3 scripts/og_card.py
Out:  public/assets/images/og-card.png
"""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "public", "assets", "images", "og-card.png")

W, H = 1200, 630
PAPER = "#ffffff"
INK = "#1a1a1a"
SECONDARY = "#555555"
CARDINAL = "#8c1515"
RULE = "#e0ded8"

MONO = "/System/Library/Fonts/Menlo.ttc"
SANS = "/System/Library/Fonts/Helvetica.ttc"


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    wordmark = ImageFont.truetype(MONO, 68, index=1)   # Menlo Bold
    subtitle = ImageFont.truetype(SANS, 30)
    body = ImageFont.truetype(SANS, 27)
    label = ImageFont.truetype(MONO, 22)

    left, top = 96, 150

    d.text((left, top), "Siddharth Aphale", font=wordmark, fill=INK)

    d.text((left, top + 104), "Data Scientist · Probabilistic ML · Embodied AI",
           font=subtitle, fill=SECONDARY)

    d.line([(left, top + 172), (left + 190, top + 172)], fill=CARDINAL, width=3)

    for i, line in enumerate([
        "Post-training and test-time compute for LLMs and VLAs:",
        "what curricula make tasks learnable, whether our objectives",
        "measure what we intend, and how to spend a fixed budget.",
    ]):
        d.text((left, top + 214 + i * 40), line, font=body, fill=INK)

    d.line([(left, H - 108), (W - left, H - 108)], fill=RULE, width=2)
    d.text((left, H - 84), "siddharthaphale.github.io", font=label, fill=SECONDARY)

    im.save(OUT, optimize=True)
    print(f"wrote {OUT} ({im.size[0]}x{im.size[1]})")


if __name__ == "__main__":
    main()
