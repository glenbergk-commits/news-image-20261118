#!/usr/bin/env python3
"""Draw the front page for 18 November 2026 (make.fun news-image-20261118).

The page is typeset programmatically with Pillow: headlines and body
copy are rendered from real fonts so every word stays crisp at
1024x1024, and each panel's picture is a flat editorial illustration
drawn with PIL shapes in this file. The output is deterministic:
no randomness, no timestamps, no network.

Run locally to (re)build the shipped image:
    python3 layout.py            # writes entry.png beside this file
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 24, 20)
MUTED = (96, 88, 74)
RULE = (26, 24, 20)
RED = (178, 34, 44)
BLUE = (36, 74, 140)
GOLD = (198, 148, 42)
TEAL = (28, 110, 110)
SKY = (214, 228, 238)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-{}.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"


def serif(size, bold=True):
    return ImageFont.truetype(SERIF.format("Bold" if bold else "Regular"), size)


def sans(size, bold=False):
    return ImageFont.truetype(SANS.format("Bold" if bold else "Regular"), size)


def wrap(draw, text, font, max_width):
    """Word-wrap text to a pixel width, returning a list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, font, fill, max_width, leading):
    """Draw wrapped text; return the y just below it."""
    x, y = xy
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def kicker(draw, xy, text, fill=RED):
    draw.text(xy, text.upper(), font=sans(15, bold=True), fill=fill)


# ---------------------------------------------------------------- header

def header(draw):
    draw.text((28, 18), "ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
              font=sans(16, bold=True), fill=MUTED)
    draw.text((W - 28, 18), "make.fun daily", font=sans(16), fill=MUTED,
              anchor="ra")
    draw.line([(28, 48), (W - 28, 48)], fill=RULE, width=3)
    draw.text((W // 2, 58), "The World on Wednesday",
              font=serif(40), fill=INK, anchor="ma")
    draw.text((W // 2, 104), "NOVEMBER 18, 2026",
              font=serif(46), fill=RED, anchor="ma")
    draw.line([(28, 162), (W - 28, 162)], fill=RULE, width=1)
    draw.line([(28, 166), (W - 28, 166)], fill=RULE, width=3)


# ------------------------------------------------------- lead illustration

def lead_art(draw, box):
    """APEC Shenzhen: skyline, three flags, a summit table."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    draw.ellipse([x1 - 92, y0 + 14, x1 - 30, y0 + 76], fill=GOLD)
    # skyline
    towers = [(0, 80, 34, 132), (40, 52, 70, 132), (78, 96, 108, 132),
              (116, 38, 150, 132), (158, 74, 190, 132), (198, 56, 228, 132),
              (236, 90, 262, 132), (270, 44, 300, 132), (308, 80, 336, 132)]
    for tx, ty, bx, by in towers:
        draw.rectangle([x0 + tx, y0 + ty, x0 + bx, y0 + by], fill=(120, 140, 165))
        for wy in range(y0 + ty + 10, y0 + by - 8, 14):
            draw.line([(x0 + tx + 5, wy), (x0 + bx - 5, wy)],
                      fill=(225, 232, 240), width=2)
    base = y0 + 132
    draw.rectangle([x0, base, x1, y1], fill=(232, 222, 198))
    # three flags on poles
    for i, colour in enumerate((RED, GOLD, BLUE)):
        fx = x0 + 52 + i * 118
        draw.line([(fx, base + 2), (fx, base + 52)], fill=INK, width=3)
        draw.rectangle([fx, base + 4, fx + 62, base + 30], fill=colour)
        draw.polygon([(fx + 62, base + 4), (fx + 74, base + 17),
                      (fx + 62, base + 30)], fill=colour)
    # summit table and three seats
    draw.rectangle([x0 + 30, base + 72, x1 - 30, base + 84], fill=(90, 62, 40))
    for i in range(3):
        cx = x0 + 92 + i * 118
        draw.ellipse([cx - 11, base + 48, cx + 11, base + 70], fill=INK)
        draw.rectangle([cx - 14, base + 68, cx + 14, base + 82], fill=INK)


def lead(draw):
    x0, y0, x1, y1 = 28, 182, W - 28, 462
    kicker(draw, (x0, y0), "Lead story  •  APEC summit, Shenzhen")
    y = block(draw, (x0, y0 + 22),
              "Xi & Putin Meet in Shenzhen as Trump Arrives for "
              "First-Ever Trilateral", serif(37), INK, 560, 42)
    y = block(draw, (x0, y + 6),
              "China's Xi Jinping and Russia's Vladimir Putin met at "
              "the APEC summit a day before the first US-China-Russia "
              "leaders' talks. Ukraine, Iran and arms control top the "
              "agenda. En route, Trump stopped in Manila, where Quad "
              "leaders met for the first time in over two years.",
              sans(19), (52, 48, 42), 560, 25)
    lead_art(draw, (612, y0 + 22, x1, y0 + 216))
    draw.text((612, y0 + 246), "SHENZHEN, CHINA — APEC LEADERS' WEEK",
              font=sans(13, bold=True), fill=MUTED)
    draw.line([(x0, y1), (x1, y1)], fill=RULE, width=2)


# ------------------------------------------------------------ mid panels

def art_gulf(draw, box):
    """Strait, a tanker, two drones."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(168, 205, 224))
    draw.rectangle([x0, y0 + 62, x1, y1], fill=(64, 118, 168))
    draw.polygon([(x0, y0 + 62), (x0 + 70, y0 + 30), (x0 + 128, y0 + 62)],
                 fill=(196, 172, 120))
    draw.polygon([(x1, y0 + 62), (x1 - 62, y0 + 38), (x1 - 110, y0 + 62)],
                 fill=(196, 172, 120))
    # tanker
    draw.polygon([(x0 + 88, y0 + 84), (x0 + 218, y0 + 84), (x0 + 204, y0 + 102),
                  (x0 + 100, y0 + 102)], fill=(40, 40, 44))
    draw.rectangle([x0 + 128, y0 + 70, x0 + 178, y0 + 84], fill=RED)
    # drones
    for dx, dy in ((52, 22), (238, 14)):
        draw.line([(x0 + dx - 14, y0 + dy), (x0 + dx + 14, y0 + dy)], fill=INK, width=3)
        draw.line([(x0 + dx, y0 + dy - 8), (x0 + dx, y0 + dy + 8)], fill=INK, width=3)
        draw.ellipse([x0 + dx - 4, y0 + dy - 4, x0 + dx + 4, y0 + dy + 4], fill=INK)


def art_gta(draw, box):
    """Vice City sunset, palms, a big VI."""
    x0, y0, x1, y1 = box
    bands = [(250, 150, 90), (248, 120, 110), (196, 84, 130),
             (120, 64, 140), (60, 44, 100)]
    band_h = (y1 - y0) // len(bands)
    for i, colour in enumerate(bands):
        draw.rectangle([x0, y0 + i * band_h, x1, y0 + (i + 1) * band_h + 1],
                       fill=colour)
    draw.ellipse([x0 + 118, y0 + 26, x0 + 182, y0 + 90], fill=(255, 214, 120))
    for px, flip in ((52, 1), (252, -1)):
        top = (x0 + px + 6 * flip, y0 + 56)
        draw.line([(x0 + px, y1), top], fill=(20, 30, 24), width=5)
        for dx, dy in ((-30, 12), (-18, 2), (0, -6), (18, 2), (30, 12)):
            draw.line([top, (top[0] + dx, top[1] + dy)],
                      fill=(20, 30, 24), width=3)
            draw.line([(top[0] + dx, top[1] + dy),
                       (top[0] + dx + (6 if dx >= 0 else -6), top[1] + dy + 10)],
                      fill=(20, 30, 24), width=2)
    draw.text(((x0 + x1) // 2, y1 - 8), "VI", font=serif(64),
              fill=(255, 240, 210), anchor="ms")


def art_ai(draw, box):
    """A chip and a rising bar chart."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(30, 36, 52))
    for i, hgt in enumerate((28, 44, 66, 96)):
        bx = x0 + 22 + i * 44
        draw.rectangle([bx, y1 - 14 - hgt, bx + 30, y1 - 14],
                       fill=(86, 200, 160) if i == 3 else (70, 130, 180))
    cx, cy = x0 + 218, y0 + 52
    draw.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], outline=GOLD, width=4)
    draw.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], outline=GOLD, width=2)
    for d in range(-20, 21, 10):
        draw.line([(cx + d, cy - 42), (cx + d, cy - 30)], fill=GOLD, width=3)
        draw.line([(cx + d, cy + 30), (cx + d, cy + 42)], fill=GOLD, width=3)
        draw.line([(cx - 42, cy + d), (cx - 30, cy + d)], fill=GOLD, width=3)
        draw.line([(cx + 30, cy + d), (cx + 42, cy + d)], fill=GOLD, width=3)
    draw.text((x0 + 18, y0 + 10), "$83", font=sans(30, bold=True),
              fill=(255, 220, 130))


MID = [
    ("War  •  Middle East", "Iran War Escalates in the Gulf",
     "US jets strike a missile site on Qeshm Island. Iran's drones "
     "target US bases in Kuwait and Bahrain; a tanker is hit near "
     "the Strait of Hormuz.", art_gulf),
    ("Culture  •  Games", "GTA VI Is Finally Here",
     "After a 13-year wait, the game unlocks first in New Zealand "
     "at midnight and rolls out worldwide on PS5 and Xbox Series.",
     art_gta),
    ("Business  •  AI", "Nvidia Soars, Anthropic at $83",
     "Nvidia posts record Q3 revenue of $115.8bn, up 103%. "
     "Anthropic prices its IPO at $83, above its range, to debut "
     "on Nasdaq as ANT.", art_ai),
]


def mid_row(draw):
    y0, y1 = 478, 756
    col_w, gap = 309, 24
    for i, (tag, head, body, art) in enumerate(MID):
        x0 = 28 + i * (col_w + gap)
        art(draw, (x0, y0, x0 + col_w, y0 + 104))
        kicker(draw, (x0, y0 + 112), tag, fill=TEAL if i else RED)
        y = block(draw, (x0, y0 + 134), head, serif(23), INK, col_w, 27)
        block(draw, (x0, y + 4), body, sans(15), (52, 48, 42), col_w, 20)
        if i:
            draw.line([(x0 - gap // 2, y0), (x0 - gap // 2, y1)],
                      fill=(200, 192, 172), width=1)
    draw.line([(28, y1), (W - 28, y1)], fill=RULE, width=2)


# ----------------------------------------------------------- small items

SMALL = [
    ("US POLITICS", "Peltola Wins Alaska",
     "Democrat Mary Peltola beats Sen. Dan Sullivan; Democrats are "
     "projected to hold the US Senate 56-44."),
    ("UKRAINE", "Kerch Bridge Hit Again",
     "Ukraine strikes the Crimea bridge for a second day; part of "
     "the road span falls into the strait."),
    ("WEATHER  •  INDIA", "Cyclone Akvan Nears Land",
     "A severe storm in the Bay of Bengal, winds near 100 km/h, "
     "heads for Odisha and Andhra Pradesh on Nov 20."),
    ("GAZA  •  UK", "Gaza Operation, UK Sanctions",
     "Israel opens a concentrated operation in central Gaza; the UK "
     "sanctions 8 settlement firms and group Tzav 9."),
]


def small_grid(draw):
    y0 = 772
    col_w, gap = 474, 24
    for i, (tag, head, body) in enumerate(SMALL):
        x0 = 28 + (i % 2) * (col_w + gap)
        yy = y0 + (i // 2) * 70
        kicker(draw, (x0, yy), tag, fill=MUTED)
        draw.text((x0 + 158, yy - 3), head, font=serif(19), fill=INK)
        block(draw, (x0, yy + 20), body, sans(14), (52, 48, 42), col_w, 18)


# ------------------------------------------------------------------- map

MAP_ROWS = [
    "        ___  _                                                  ",
    "  _____/   \\/ \\__      _.-\"\"\"-._   _                            ",
    " /  Americas     \\    /  Europe \\_/ \\_   Asia                    ",
    "|  *Alaska        \\__/  *Kerch  \\    \\___  *Shenzhen             ",
    " \\_  *Florida       *Gaza  *Hormuz    \\_/    \\                   ",
    "   \\   (Vice City) /   \\      *Bay of Bengal  \\  *NZ: GTA VI     ",
    "    \\____  ______/  Africa \\______  Australia  \\_/               ",
    "          \\/               \\      \\/                             ",
]

MARKERS = [(4, 3), (25, 4), (33, 3), (38, 4), (44, 4), (52, 3), (46, 5), (58, 5)]


CONTINENTS = [
    # very coarse continent silhouettes inside the strip, (x, y) pairs
    # with y kept inside the band (title row, then 22..58)
    [(30, 26), (120, 22), (146, 32), (122, 42), (102, 52), (80, 40),
     (36, 40)],                                             # North America
    [(96, 46), (116, 44), (118, 56), (104, 62), (96, 54)],   # South America
    [(300, 24), (356, 22), (366, 32), (336, 38), (304, 36)],  # Europe
    [(310, 40), (354, 38), (362, 50), (344, 62), (320, 60),
     (308, 50)],                                             # Africa
    [(386, 24), (560, 20), (624, 30), (590, 44), (510, 42),
     (452, 48), (412, 42), (390, 34)],                        # Asia
    [(520, 46), (548, 44), (552, 54), (528, 58), (516, 52)],  # SE Asia arc
    [(640, 48), (694, 46), (700, 58), (660, 62), (638, 56)],  # Australia
    [(742, 56), (758, 54), (760, 62), (746, 63)],             # New Zealand
]


def map_band(draw):
    y0 = 916
    draw.rectangle([28, y0, W - 28, 984], fill=(38, 52, 74))
    draw.text((44, y0 + 5), "WHERE IT HAPPENED — NOV 18 AROUND THE WORLD",
              font=sans(13, bold=True), fill=(255, 220, 130))
    land = (122, 148, 120)
    for poly in CONTINENTS:
        draw.polygon([(x + 28, y + y0) for x, y in poly], fill=land)
    labels = [("ALASKA", 52, 26), ("FLORIDA", 128, 38), ("GAZA", 330, 38),
              ("KERCH", 376, 24), ("HORMUZ", 452, 38),
              ("BAY OF BENGAL", 520, 44), ("SHENZHEN", 606, 26),
              ("AUCKLAND", 748, 50)]
    for name, lx, ly in labels:
        draw.ellipse([lx, y0 + ly, lx + 8, y0 + ly + 8], fill=(255, 120, 90),
                     outline=(255, 240, 220), width=1)
        draw.text((lx + 11, y0 + ly - 2), name, font=sans(10, bold=True),
                  fill=(225, 234, 246))


def footer(draw):
    draw.line([(28, 994), (W - 28, 994)], fill=RULE, width=1)
    draw.text((28, 1000),
              "All stories reported on 18 November 2026, in some time zone. "
              "Illustrations are editorial artwork, not photographs.",
              font=sans(12), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    header(draw)
    lead(draw)
    mid_row(draw)
    small_grid(draw)
    map_band(draw)
    footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
