#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news poster and save it as entry.png.

One newspaper front page for Thursday 19 November 2026. The lead story is
the first three-way summit of Trump, Xi and Putin in Shenzhen, and five
shorter stories cover the Crimean Bridge strike, Iran's widened Gulf
attacks, the ICJ ruling on Myanmar and the Rohingya, Anthropic's record
stock-market debut, and North Korea's expanded uranium enrichment.
Every picture on the page is drawn here from plain shapes: no photos,
no downloaded art, no network. Flat colours keep the PNG small and the
text readable when the picture is shown small.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"
M = 36  # page margin

PAPER = (252, 250, 243)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (30, 80, 200)
TEAL = (15, 118, 110)
GOLD = (176, 124, 28)
GREEN = (22, 125, 60)
GREY = (96, 96, 96)
LIGHT = (236, 232, 220)
SKY = (214, 232, 248)
SAND = (248, 230, 196)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Split text into lines that fit inside max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, fill, gap=5):
    """Draw wrapped text starting at (x, y); return y below the last line."""
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def centred(d, cx, y, text, font, fill):
    """Draw text centred on cx at height y; return y below the line."""
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + font.size


def rule(d, x0, x1, y, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def pic_summit(d, x, y, w, h):
    """Three flags over a round table: the Shenzhen summit."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=SKY)
    # three flag poles with pennants
    cols = [RED, BLUE, GOLD]
    for i, col in enumerate(cols):
        px = x + w * (0.22 + i * 0.28)
        d.line([(px, y + 18), (px, y + h - 62)], fill=INK, width=5)
        d.polygon([(px, y + 18), (px + 62, y + 32), (px, y + 48)], fill=col)
    # round table
    d.ellipse([x + 30, y + h - 62, x + w - 30, y + h - 26], fill=(120, 72, 20))
    d.rectangle([x + w // 2 - 6, y + h - 30, x + w // 2 + 6, y + h - 6],
                fill=INK)
    d.rectangle([x + w // 2 - 44, y + h - 10, x + w // 2 + 44, y + h - 4],
                fill=INK)


def pic_bridge(d, x, y, w, h):
    """A bridge deck broken in the middle, over water."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=(254, 228, 228))
    mid = x + w // 2
    # towers
    for tx in (x + w * 0.24, x + w * 0.76):
        d.line([(tx, y + 16), (tx, y + h * 0.62)], fill=INK, width=7)
        d.line([(tx - 18, y + 16), (tx + 18, y + 16)], fill=INK, width=7)
    # deck, two pieces with a gap
    d.line([(x + 8, y + h * 0.62), (mid - 18, y + h * 0.62)], fill=INK, width=9)
    d.line([(mid + 18, y + h * 0.62), (x + w - 8, y + h * 0.62)], fill=INK, width=9)
    # falling pieces and cracks
    d.line([(mid - 18, y + h * 0.62), (mid - 2, y + h * 0.88)], fill=RED, width=6)
    d.line([(mid + 18, y + h * 0.62), (mid + 2, y + h * 0.88)], fill=RED, width=6)
    # cables sagging from the towers
    d.arc([x + w * 0.24 - 60, y - 30, x + w * 0.24 + 60, y + h * 0.62],
          20, 160, fill=GREY, width=3)
    d.arc([x + w * 0.76 - 60, y - 30, x + w * 0.76 + 60, y + h * 0.62],
          20, 160, fill=GREY, width=3)
    # water
    for i in range(3):
        yy = y + h - 26 + i * 8
        pts = []
        for px in range(x + 8, x + w - 7, 10):
            pts.append((px, yy + 3 * ((px // 10) % 2)))
        d.line(pts, fill=BLUE, width=3)


def pic_gulf(d, x, y, w, h):
    """Missile arcs over a ship at sea: the Gulf escalation."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=(16, 32, 64))
    # sea
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(24, 68, 140))
    for i in range(3):
        yy = y + h * 0.76 + i * 12
        d.line([(x + 10, yy), (x + w - 10, yy)], fill=(140, 190, 240), width=3)
    # ship: hull, funnel, mast
    d.polygon([(x + w * 0.12, y + h * 0.66), (x + w * 0.88, y + h * 0.66),
               (x + w * 0.78, y + h * 0.80), (x + w * 0.22, y + h * 0.80)],
              fill=(200, 200, 200))
    d.rectangle([x + w * 0.40, y + h * 0.50, x + w * 0.58, y + h * 0.66],
                fill=RED)
    d.line([(x + w * 0.49, y + h * 0.38), (x + w * 0.49, y + h * 0.50)],
           fill=(200, 200, 200), width=4)
    # missile trails: two curves arcing down from the top right to the
    # burst point, drawn as quadratic bezier polylines inside the box
    bx, by = x + w * 0.72, y + h * 0.42
    import math

    def bezier(p0, p1, p2, steps=24):
        pts = []
        for i in range(steps + 1):
            t = i / steps
            px = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            py = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            pts.append((px, py))
        return pts

    d.line(bezier((x + w - 8, y + 8), (x + w * 0.86, y + h * 0.18),
                  (bx + 14, by - 6)), fill=GOLD, width=5)
    d.line(bezier((x + w * 0.62, y + 6), (x + w * 0.62, y + h * 0.20),
                  (bx - 4, by - 14)), fill=(240, 240, 240), width=4)
    # burst where a trail meets the ship
    for k in range(8):
        ang = k * 0.785
        ex = bx + 22 * math.cos(ang)
        ey = by + 22 * math.sin(ang)
        d.line([(bx, by), (ex, ey)], fill=GOLD, width=4)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=GOLD)


def pic_scales(d, x, y, w, h):
    """Scales of justice: the ICJ ruling."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=(220, 252, 231))
    cx = x + w // 2
    # post and base
    d.line([(cx, y + 16), (cx, y + h - 26)], fill=INK, width=6)
    d.rectangle([cx - 52, y + h - 26, cx + 52, y + h - 12], fill=INK)
    # beam
    d.line([(cx - 78, y + 34), (cx + 78, y + 34)], fill=INK, width=6)
    # pans
    for side in (-1, 1):
        px = cx + side * 78
        d.line([(px, y + 34), (px - 30, y + 78)], fill=INK, width=3)
        d.line([(px, y + 34), (px + 30, y + 78)], fill=INK, width=3)
        d.arc([px - 30, y + 62, px + 30, y + 94], 0, 180, fill=GOLD, width=5)
        d.line([(px - 30, y + 78), (px + 30, y + 78)], fill=GOLD, width=5)
    # small gavel resting at the foot, left of centre
    d.rectangle([x + 10, y + h - 44, x + 44, y + h - 32], fill=(120, 72, 20))
    d.line([(x + 27, y + h - 38), (x + 62, y + h - 50)], fill=(120, 72, 20),
           width=5)


def pic_chart(d, x, y, w, h):
    """Rising bars and an arrow: a record market debut."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=(255, 255, 255))
    # axes
    d.line([(x + 22, y + 14), (x + 22, y + h - 22)], fill=INK, width=3)
    d.line([(x + 22, y + h - 22), (x + w - 14, y + h - 22)], fill=INK, width=3)
    # bars rising left to right
    heights = [0.30, 0.45, 0.42, 0.62, 0.85]
    bw = (w - 60) // len(heights)
    for i, frac in enumerate(heights):
        bx = x + 34 + i * bw
        top = y + h - 22 - int(frac * (h - 50))
        d.rectangle([bx, top, bx + bw - 10, y + h - 22], fill=TEAL)
    # arrow over the bars
    pts = [(x + 34, y + h - 40), (x + w * 0.42, y + h * 0.52),
           (x + w * 0.68, y + h * 0.34), (x + w - 22, y + 22)]
    d.line(pts, fill=RED, width=5)
    d.polygon([(x + w - 22, y + 22), (x + w - 46, y + 20),
               (x + w - 26, y + 44)], fill=RED)


def pic_atom(d, x, y, w, h):
    """An atom: nucleus with three orbits, for the enrichment story."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=SKY)
    cx, cy = x + w // 2, y + h // 2
    # orbits: wide, tall and diagonal-ish ellipses
    d.ellipse([cx - 84, cy - 26, cx + 84, cy + 26], outline=BLUE, width=4)
    d.ellipse([cx - 26, cy - 84, cx + 26, cy + 84], outline=RED, width=4)
    d.ellipse([cx - 66, cy - 66, cx + 66, cy + 66], outline=TEAL, width=4)
    # nucleus and electrons
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=INK)
    d.ellipse([cx + 72, cy - 32, cx + 84, cy - 20], fill=BLUE)
    d.ellipse([cx - 32, cy + 72, cx - 20, cy + 84], fill=RED)
    d.ellipse([cx - 72, cy - 72, cx - 60, cy - 60], fill=TEAL)


def story_card(d, x, y, w, pic, kicker, head, body, head_size=23,
               body_size=17, pic_h=118):
    """One small story: kicker, picture, headline, body text."""
    d.text((x, y), kicker, font=fnt(SANS_B, 15), fill=RED)
    y += 22
    pic(d, x, y, w, pic_h)
    y += pic_h + 10
    y = para(d, x, y, head, fnt(SERIF_B, head_size), w, INK, gap=2)
    y = para(d, x, y + 2, body, fnt(SANS, body_size), w, INK, gap=4)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    right = W - M

    # --- masthead ---
    y = 26
    y = centred(d, W // 2, y, "THE WORLD TODAY", fnt(SERIF_B, 82), INK)
    y += 8
    y = centred(d, W // 2, y, "THURSDAY  19  NOVEMBER  2026",
                fnt(SANS_B, 27), RED)
    y += 12
    rule(d, M, right, y, width=3)
    rule(d, M, right, y + 6, width=1)

    # --- lead story ---
    y += 18
    lead_pic_w = 348
    lead_pic_h = 236
    lead_x = right - lead_pic_w
    d.text((M, y), "THE LEAD  •  SHENZHEN", font=fnt(SANS_B, 16), fill=RED)
    y += 26
    head_y = y
    y = para(d, M, y, "Trump, Xi and Putin meet in Shenzhen",
             fnt(SERIF_B, 45), lead_x - M - 24, INK, gap=2)
    y += 6
    y = para(d, M, y,
             "The three leaders hold their first three-way talks on the "
             "sidelines of the APEC forum, as the world watches for any "
             "sign of a thaw.",
             fnt(SANS, 21), lead_x - M - 24, INK, gap=5)
    pic_summit(d, lead_x, head_y, lead_pic_w, lead_pic_h)
    y = max(y, head_y + lead_pic_h) + 10
    rule(d, M, right, y, width=2)

    # --- row A: three stories ---
    y += 16
    gap = 16
    cw = (W - 2 * M - 2 * gap) // 3
    x0, x1, x2 = M, M + cw + gap, M + 2 * (cw + gap)
    story_card(d, x0, y, cw, pic_bridge, "UKRAINE",
               "Bridge hit for the third time this week",
               "Ukraine strikes the Crimean Bridge again as talks go on.",
               pic_h=104)
    story_card(d, x1, y, cw, pic_gulf, "THE GULF",
               "Iran widens attacks on Gulf states",
               "Tehran hits Gulf targets after US jets struck a site on "
               "Qeshm Island.",
               pic_h=104)
    story_card(d, x2, y, cw, pic_scales, "THE HAGUE",
               "World court rules on Myanmar case",
               "The ICJ delivers its long-awaited judgment on the "
               "Rohingya genocide case.",
               pic_h=104)
    y += 258
    rule(d, M, right, y, width=2)

    # --- row B: two stories ---
    y += 14
    cw2 = (W - 2 * M - gap) // 2
    story_card(d, M, y, cw2, pic_chart, "MARKETS",
               "Anthropic's record market debut",
               "The AI lab raises a record sum in its first day of "
               "trading, the biggest debut of its kind.",
               head_size=25, body_size=18, pic_h=112)
    story_card(d, M + cw2 + gap, y, cw2, pic_atom, "NORTH KOREA",
               "Pyongyang expands enrichment",
               "The IAEA says North Korea has expanded uranium "
               "enrichment at Yongbyon, raising fresh concern.",
               head_size=25, body_size=18, pic_h=112)

    # --- footer ---
    rule(d, M, right, H - 30, width=1)
    centred(d, W // 2, H - 24,
            "The World Today  •  19 November 2026  •  All pictures drawn "
            "from simple shapes",
            fnt(SANS, 15), GREY)

    img.save(OUT, "PNG")
    print(f"Wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
