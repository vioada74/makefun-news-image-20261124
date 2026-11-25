#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024).

Reads the eight AI illustrations in assets/ (hero.webp, block1.webp ..
block7.webp) and composes a newspaper front page with PIL + DejaVu fonts.
Writes entry.png next to this script. PNG is tried first; if the result is
over the 1 MiB limit it falls back to JPEG bytes (still named entry.png,
which the competition rules allow).
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
OUT = os.path.join(BASE, "entry.png")

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968

PAPER = (251, 248, 241)
INK = (20, 20, 20)
GREY = (90, 86, 80)
RED = (140, 29, 24)
DARK = (22, 22, 26)
PHOTO_EDGE = (120, 115, 108)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, cx=W // 2):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def photo(path, w, h):
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, (w, h), Image.LANCZOS)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    mast = font(SERIF_B, 62)
    draw_centered(d, 16, "WORLD NEWS ROUNDUP", mast, INK)
    d.line([(MARGIN, 88), (W - MARGIN, 88)], fill=INK, width=3)
    d.line([(MARGIN, 94), (W - MARGIN, 94)], fill=INK, width=1)

    # ---- Date ribbon ----------------------------------------------------
    d.rectangle([MARGIN, 102, W - MARGIN, 134], fill=RED)
    date_f = font(SANS_B, 20)
    draw_centered(d, 108, "TUESDAY, 24 NOVEMBER 2026", date_f, (255, 255, 255))

    # ---- Hero -----------------------------------------------------------
    hero = photo(os.path.join(ASSETS, "hero.webp"), CW, 190)
    page.paste(hero, (MARGIN, 144))
    d.rectangle([MARGIN, 144, W - MARGIN - 1, 144 + 190 - 1],
                outline=PHOTO_EDGE, width=1)
    tag_f = font(SANS_B, 15)
    d.text((MARGIN, 342), "TOP STORY", font=tag_f, fill=RED)
    hero_head = font(SERIF_B, 37)
    d.text((MARGIN, 360), "SANOFI BUYS INSMED FOR $41 BILLION",
           font=hero_head, fill=INK)
    hero_sum = font(SANS, 21)
    d.text((MARGIN, 404), "Sanofi agrees $41 billion cash deal for US biotech Insmed.",
           font=hero_sum, fill=(50, 48, 44))
    d.line([(MARGIN, 440), (W - MARGIN, 440)], fill=INK, width=2)

    # ---- Photo blocks ---------------------------------------------------
    blocks = [
        ("block1.webp", "ISRAEL KILLS HAMAS SECURITY CHIEF IN GAZA",
         "Airstrike kills Hamas security chief Abu Nahel; six others dead."),
        ("block2.webp", "RUSSIAN STRIKE HITS ZAPORIZHZHIA HOMES",
         "Overnight strike kills two, wounds 40, including four children."),
        ("block3.webp", "47,000 WOMEN KILLED BY PARTNERS IN 2025",
         "UN: partners or family killed 47,000 women last year."),
        ("block4.webp", "GERMANY FIRST TO GET UKRAINE'S DELTA SYSTEM",
         "Germany first ally to access Ukraine's Delta battlefield system."),
        ("block5.webp", "RUSSIAN JETS SPARK KOREA AIR ALERT",
         "Russian jets enter Korea defence zone; Seoul scrambles fighters."),
        ("block6.webp", "EBOLA TEAMS TRAPPED BY CONGO FIGHTING",
         "Fighting traps Ebola responders in Ituri hospital ward."),
        ("block7.webp", "IRAQ PM SEIZES KURDISH OILFIELDS",
         "Baghdad orders takeover of Kurdish oilfields and crossings."),
    ]
    head_f = font(SERIF_B, 18)
    sum_f = font(SANS, 16)
    gap = 10
    row1_y, row2_y = 452, 710
    row_h = 228
    for i, (img, headline, summary) in enumerate(blocks):
        if i < 4:
            cols, row_y = 4, row1_y
        else:
            cols, row_y = 3, row2_y
            i2 = i - 4
            bw = (CW - gap * (cols - 1)) // cols
            x = MARGIN + i2 * (bw + gap)
            _draw_block(d, page, x, row_y, bw, img, headline, summary,
                        head_f, sum_f)
            continue
        bw = (CW - gap * (cols - 1)) // cols
        x = MARGIN + i * (bw + gap)
        _draw_block(d, page, x, row_y, bw, img, headline, summary,
                    head_f, sum_f)

    # ---- Footer ticker --------------------------------------------------
    d.rectangle([MARGIN, 968, W - MARGIN, 1014], fill=DARK)
    tick_f = font(SANS_B, 15)
    ticker = ("ASIAN CHIP STOCKS SOAR: TAIEX +9.0%, KOSPI +6.3%, NIKKEI +3.9%"
              "  \u25cf  DOW TOPS 50,000 AS NASDAQ SLIDES 1.5%"
              "  \u25cf  EUCLID FINDS MOST DISTANT QUASAR, 630M YEARS AFTER BIG BANG")
    lines = wrap(d, ticker, tick_f, CW - 24)
    ly = 972
    for line in lines[:2]:
        draw_centered(d, ly, line, tick_f, (245, 245, 240))
        ly += 21

    page.save(OUT, format="PNG", optimize=True)
    if os.path.getsize(OUT) > 1048576:
        page.save(OUT, format="JPEG", quality=88, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


def _draw_block(d, page, x, y, w, img, headline, summary, head_f, sum_f):
    im = photo(os.path.join(ASSETS, img), w, 112)
    page.paste(im, (x, y))
    d.rectangle([x, y, x + w - 1, y + 112 - 1], outline=PHOTO_EDGE, width=1)
    ty = y + 120
    for line in wrap(d, headline, head_f, w)[:3]:
        d.text((x, ty), line, font=head_f, fill=INK)
        ty += 22
    ty += 3
    for line in wrap(d, summary, sum_f, w)[:3]:
        d.text((x, ty), line, font=sum_f, fill=(50, 48, 44))
        ty += 20


if __name__ == "__main__":
    main()
