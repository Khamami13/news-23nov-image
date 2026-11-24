#!/usr/bin/env python3
"""Draw the make.fun entry image: a one-page newspaper front page summing up
the world news of Monday 23 November 2026.

Output: entry.png next to the repo root (1024x1024, under 1 MiB).
Only Pillow (already installed) and the system Liberation/DejaVu fonts are used.
Every story on the page comes from the verified list in README.md; nothing
from any other day is included.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
MARGIN = 32
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (18, 69, 120)
PAPER = (252, 250, 244)
GREY = (90, 90, 90)
RULE = (150, 150, 150)
SEA = (196, 222, 240)
LAND = (232, 214, 170)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def para(draw, text, fnt, x, y, max_w, max_lines, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) <= max_lines, f"text overflows box: {text!r} -> {len(lines)} lines"
    return draw_lines(draw, lines, fnt, x, y, fill=fill)


def headline(draw, text, fnt, x, y, max_w, max_lines):
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) <= max_lines, f"headline overflows: {text!r}"
    return draw_lines(draw, lines, fnt, x, y, fill=INK)


def panel(draw, x, y, w, h, kicker, head, body, head_size=23, body_size=15):
    hf = font(SERIF_B, head_size)
    bf = font(SANS, body_size)
    head_lines = wrap(draw, head, hf, w - 28)
    body_lines = wrap(draw, body, bf, w - 28)
    need = 12 + 22 + len(head_lines) * int(head_size * 1.22) + 4 \
        + len(body_lines) * int(body_size * 1.22) + 10
    assert need <= h, (f"panel {kicker!r} needs {need}px > {h}px: "
                       f"{len(head_lines)} headline + {len(body_lines)} body lines")
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    px = x + 14
    inner = w - 28
    cy = y + 12
    draw.text((px, cy), kicker, font=font(SANS_B, 13), fill=RED)
    cy += 22
    cy = draw_lines(draw, head_lines, hf, px, cy, fill=INK)
    cy += 4
    draw_lines(draw, body_lines, bf, px, cy, fill=INK)
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top line -------------------------------------------------------
    d.line([(MARGIN, 22), (W - MARGIN, 22)], fill=INK, width=2)
    small = font(SANS, 13)
    d.text((MARGIN, 28), "THE WORLD IN ONE PAGE", font=font(SANS_B, 13), fill=GREY)
    right = "No. 327  •  ONE PAGE, ONE DAY"
    d.text((W - MARGIN - d.textlength(right, font=small), 28), right,
           font=small, fill=GREY)

    # ---- masthead -------------------------------------------------------
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 72)
    d.text(((W - d.textlength(title, font=tf)) / 2, 52), title, font=tf, fill=INK)
    d.line([(MARGIN, 138), (W - MARGIN, 138)], fill=INK, width=3)

    # ---- date band ------------------------------------------------------
    d.rectangle([MARGIN, 148, W - MARGIN, 194], fill=INK)
    date = "MONDAY, 23 NOVEMBER 2026"
    df = font(SANS_B, 30)
    d.text(((W - d.textlength(date, font=df)) / 2, 156), date, font=df,
           fill=(255, 255, 255))
    d.line([(MARGIN, 206), (W - MARGIN, 206)], fill=INK, width=2)

    # ---- lead story (left, wide) ---------------------------------------
    lx, ly, lw = MARGIN, 220, 600
    d.text((lx, ly), "LEAD STORY", font=font(SANS_B, 14), fill=RED)
    cy = ly + 24
    cy = headline(d, "Ukraine sinks Russian warship off Libya",
                  font(SERIF_B, 36), lx, cy, lw, 2)
    cy += 6
    cy = para(d, "Ukrainian naval drones sank the Russian corvette Merkury "
                 "off Libya and hit the cargo ship Angara, President "
                 "Zelenskyy confirmed. NATO held an emergency meeting "
                 "after Russian missile strikes in Poland.",
              font(SANS, 17), lx, cy, lw, 4)
    cy += 10

    # schematic map: Mediterranean sea, Libyan coast, the two ships
    mx0, my0, mx1, my1 = lx, cy, lx + lw, cy + 96
    d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=RULE, width=1)
    # Libyan landmass along the bottom
    d.polygon([(mx0, my1), (mx0, my1 - 34), (mx1 * 0.35, my1 - 44),
               (mx1 * 0.62, my1 - 30), (mx1, my1 - 40), (mx1, my1)],
              fill=LAND)
    d.text((mx0 + 12, my1 - 26), "LIBYA", font=font(SANS_B, 14), fill=(110, 85, 40))
    sea_label = "MEDITERRANEAN SEA"
    d.text((mx1 - 12 - d.textlength(sea_label, font=font(SANS_B, 13)), my0 + 8),
           sea_label, font=font(SANS_B, 13), fill=BLUE)

    def ship(cx, cy2, label, sunk):
        # simple side-view ship silhouette
        d.polygon([(cx - 26, cy2), (cx + 26, cy2), (cx + 18, cy2 + 12),
                   (cx - 18, cy2 + 12)], fill=INK)
        d.rectangle([cx - 8, cy2 - 12, cx + 8, cy2], fill=INK)
        d.line([(cx + 2, cy2 - 22), (cx + 2, cy2 - 12)], fill=INK, width=2)
        if sunk:
            d.line([(cx - 30, cy2 - 26), (cx - 12, cy2 - 8)], fill=RED, width=3)
            d.line([(cx - 12, cy2 - 26), (cx - 30, cy2 - 8)], fill=RED, width=3)
        d.text((cx - 30, cy2 + 16), label, font=font(SANS_B, 13),
               fill=RED if sunk else INK)

    ship(mx0 + 190, my0 + 38, "Merkury — sunk", True)
    ship(mx0 + 430, my0 + 46, "Angara — hit", False)
    lead_bottom = my1

    # ---- COP31 panel (right of lead) -----------------------------------
    rx, rw = lx + lw + 16, W - MARGIN - (lx + lw + 16)
    panel(d, rx, ly, rw, lead_bottom - ly, "CLIMATE  •  ANTALYA, TURKEY",
          "COP31 climate talks collapse with no deal",
          "The UN climate summit in Antalya, Turkey, ended with no "
          "agreement — the first failure since 2009 — after the EU "
          "rejected a final text that left out fossil fuels.",
          head_size=25, body_size=15)

    # ---- middle row: Nvidia / Iran / Indonesia -------------------------
    row2_y, row2_h = lead_bottom + 14, 200
    col_w = (W - 2 * MARGIN - 2 * 14) // 3
    x0 = MARGIN
    panel(d, x0, row2_y, col_w, row2_h, "TECH  •  SILICON VALLEY",
          "Nvidia brings back Jensen Huang as CEO",
          "Jensen Huang returns as chief executive after President "
          "Trump intervened with the board. Shares jumped about 30%.")
    panel(d, x0 + col_w + 14, row2_y, col_w, row2_h, "UNITED STATES  •  IRAN",
          "US hits Iran with new sanctions",
          "Washington sanctioned Iran's shadow-banking network: "
          "exchange houses, front companies, key personnel. Iran "
          "also flogged singer Parastoo Ahmadi and four band members.")
    panel(d, x0 + 2 * (col_w + 14), row2_y, col_w, row2_h, "INDONESIA  •  JAKARTA",
          "Factory fire in Jakarta kills 24",
          "A factory fire in Jakarta killed 24 people, with dozens "
          "more missing, officials said.")

    # ---- bottom row: Belgium / Nepal / Bitcoin -------------------------
    row3_y, row3_h = row2_y + row2_h + 14, 180
    panel(d, x0, row3_y, col_w, row3_h, "BELGIUM  •  BRUSSELS",
          "Belgium strike grounds almost all flights",
          "A national strike shut airports as air traffic controllers "
          "walked out; nearly all flights at Brussels and Charleroi "
          "were cancelled.")
    panel(d, x0 + col_w + 14, row3_y, col_w, row3_h, "SOUTH ASIA",
          "India gives $1.62bn aid to flood-hit Nepal",
          "India announced a $1.62 billion package for flood-hit Nepal.")
    panel(d, x0 + 2 * (col_w + 14), row3_y, col_w, row3_h, "MARKETS",
          "Bitcoin sinks to $55,100, then rebounds",
          "Bitcoin fell to about $55,100 — its lowest since September "
          "2024 — before recovering to around $61,000.")

    # ---- also-today strip ------------------------------------------------
    ay = row3_y + row3_h + 14
    d.rectangle([MARGIN, ay, W - MARGIN, ay + 44], fill=INK)
    strip = "ALSO TODAY:  EU proposes new Russia sanctions — 60 banks, " \
            "crypto platforms and shadow-fleet vessels."
    sf = font(SANS_B, 16)
    d.text((MARGIN + 14, ay + 12), strip, font=sf, fill=(255, 255, 255))

    # ---- footer ----------------------------------------------------------
    fy = ay + 56
    foot = "Sources: Reuters  •  AP  •  BBC  •  BusinessWorld  •  " \
           "Daily Summary of World"
    ff = font(SANS, 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy), foot, font=ff, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
