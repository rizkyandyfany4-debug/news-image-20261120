#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page as a 1024x1024 PNG.

Everything is drawn from code with Pillow: no photographs, no network,
no timestamps, no randomness -- the same input always renders the same bytes.

Layout budget (1024 tall): masthead to 130, lead 146-472, middle row
488-780, ICJ band 794-912, ALSO strip 924-964, footer 984.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 236)
INK = (20, 20, 20)
RED = (158, 27, 27)
GREY = (90, 86, 76)
LIGHT_RULE = (180, 172, 150)
NAVY = (16, 28, 54)
GOLD = (212, 160, 44)

FONT_DIR = Path("/usr/share/fonts/truetype/noto")
SERIF_BLACK = str(FONT_DIR / "NotoSerif-Black.ttf")
SERIF = str(FONT_DIR / "NotoSerif-Regular.ttf")
SANS_BOLD = str(FONT_DIR / "NotoSans-Bold.ttf")
SANS = str(FONT_DIR / "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_calendar(draw, x0, y0, x1, y1):
    """A wall calendar page: red 2027 header, big JAN 1 circled in red."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=3)
    draw.rectangle([x0, y0, x1, y0 + 52], fill=RED)
    f = font(SANS_BOLD, 30)
    draw.text((x0 + 18, y0 + 10), "2027", font=f, fill=(255, 255, 255))
    f = font(SANS_BOLD, 22)
    draw.text((x1 - 118, y0 + 14), "JANUARY", font=f, fill=(255, 255, 255))
    # faint calendar grid
    for gx in range(x0 + 44, x1, 44):
        draw.line([(gx, y0 + 52), (gx, y1 - 10)], fill=(225, 220, 205), width=1)
    for gy in range(y0 + 96, y1, 44):
        draw.line([(x0 + 10, gy), (x1 - 10, gy)], fill=(225, 220, 205), width=1)
    # big "1" centred in a red circle
    f = font(SERIF_BLACK, 120)
    one_w = draw.textlength("1", font=f)
    cx = x0 + 118
    draw.text((cx - one_w / 2, y0 + 84), "1", font=f, fill=INK)
    draw.ellipse([cx - 60, y0 + 78, cx + 60, y0 + 218], outline=RED, width=6)
    f = font(SANS_BOLD, 18)
    draw.text((x0 + 192, y0 + 104), "NEW YEAR", font=f, fill=INK)
    draw.text((x0 + 192, y0 + 130), "DAY", font=f, fill=INK)
    f = font(SANS, 17)
    draw.text((x0 + 14, y1 - 34), "No decision before then.", font=f, fill=GREY)


def draw_probe(draw, x0, y0, x1, y1):
    """A starfield strip with a small deep-space probe and its signal."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    stars = [
        (12, 10), (48, 26), (90, 8), (140, 30), (190, 12), (235, 24),
        (280, 9), (330, 28), (370, 14), (420, 26), (30, 44), (110, 50),
        (170, 42), (250, 48), (310, 44), (400, 50), (70, 60), (200, 62),
        (350, 62), (440, 58),
    ]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(255, 255, 255))
    # dotted trajectory from the left edge to the probe
    for tx in range(x0 + 6, x0 + 300, 14):
        draw.ellipse([tx, y0 + 36, tx + 3, y0 + 39], fill=GOLD)
    # probe body: gold box, dish, antenna
    px, py = x0 + 330, y0 + 22
    draw.rectangle([px, py, px + 46, py + 26], fill=GOLD, outline=(255, 255, 255))
    draw.line([(px + 46, py + 8), (px + 66, py - 6)], fill=(255, 255, 255), width=2)
    draw.ellipse([px + 62, py - 12, px + 74, py + 0], outline=(255, 255, 255), width=2)
    draw.line([(px + 10, py + 26), (px + 10, py + 44)], fill=(255, 255, 255), width=2)
    draw.line([(px + 36, py + 26), (px + 36, py + 44)], fill=(255, 255, 255), width=2)


def draw_cyclone(draw, x0, y0, x1, y1):
    """A spiral storm, sized to fit a short strip, with rain ticks."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, start, end in [(44, 200, 500), (34, 140, 440), (24, 80, 380),
                          (14, 20, 320), (6, 300, 260)]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start, end=end,
                 fill=INK, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    # rain ticks around the spiral
    for rx, ry in [(x0 + 8, y0 + 6), (x0 + 34, y0 + 30), (x1 - 34, y0 + 10),
                   (x1 - 12, y0 + 34), (x0 + 16, y1 - 18), (x1 - 22, y1 - 12)]:
        draw.line([(rx, ry), (rx - 5, ry + 10)], fill=GREY, width=2)


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 40
    rx = W - mx

    # ---- masthead ----
    f = font(SERIF_BLACK, 32)
    title = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=f)) / 2, 24), title, font=f, fill=INK)
    f = font(SANS_BOLD, 42)
    date = "FRIDAY 20 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f)) / 2, 66), date, font=f, fill=INK)
    rule(d, mx, rx, 122, width=4)
    rule(d, mx, rx, 130, width=1)

    # ---- lead story: Trump puts the Iran decision off to 2027 ----
    y = 146
    f = font(SANS_BOLD, 17)
    d.text((mx, y), "WASHINGTON  ·  THE GULF", font=f, fill=RED)
    y += 30
    f = font(SERIF_BLACK, 56)
    y = draw_lines(d, mx, y,
                   wrap(d, "TRUMP PUTS IRAN CALL OFF TO 2027", f, 600),
                   f, leading=60)
    y += 6
    f = font(SERIF, 21)
    y = draw_lines(d, mx, y,
                   wrap(d, "“We’ll see what happens after January 1,” he says "
                           "aboard Air Force One — no new strikes this year.",
                        f, 600),
                   f, leading=27)
    y += 8
    f = font(SERIF, 19)
    y = draw_lines(d, mx, y,
                   wrap(d, "President Donald Trump said on Thursday he will not "
                           "decide on renewed strikes against Iran until next "
                           "year, pushing back a timeline he had tied to the "
                           "midterms. He told Reuters, Fox News and Axios: "
                           "“I’m not rushing to make any decisions.”",
                        f, 600),
                   f, leading=25)
    draw_calendar(d, 688, 148, 984, 428)

    rule(d, mx, rx, 472, width=2)

    # ---- middle row: two columns ----
    y = 488
    mid = W // 2
    # left: Voyager 1
    f = font(SANS_BOLD, 16)
    d.text((mx, y), "SPACE  ·  NASA", font=f, fill=RED)
    f = font(SERIF_BLACK, 33)
    draw_lines(d, mx, y + 26,
               wrap(d, "VOYAGER 1 PASSES ONE LIGHT-DAY OUT", f, 452),
               f, leading=38)
    f = font(SERIF, 18)
    draw_lines(d, mx, y + 108,
               wrap(d, "NASA confirms the farthest human-made object is now "
                       "more than a light-day from Earth — some 25 billion "
                       "km — still phoning home.",
                    f, 452),
               f, leading=23)
    draw_probe(d, mx, 674, 492, 764)
    # right: Cyclone Akvan
    f = font(SANS_BOLD, 16)
    d.text((mid + 12, y), "INDIA  ·  WEATHER", font=f, fill=RED)
    f = font(SERIF_BLACK, 33)
    draw_lines(d, mid + 12, y + 26,
               wrap(d, "CYCLONE AKVAN HITS EAST COAST", f, 452),
               f, leading=38)
    f = font(SERIF, 18)
    draw_lines(d, mid + 12, y + 108,
               wrap(d, "Severe Cyclone Akvan is due to cross the Andhra "
                       "Pradesh–Odisha coast around noon, winds 90–100 "
                       "km/h. Tens of thousands have moved to safety. (IMD)",
                    f, 452),
               f, leading=23)
    draw_cyclone(d, mid + 180, 674, mid + 320, 764)
    # vertical divider between the columns
    d.line([(mid, 488), (mid, 764)], fill=LIGHT_RULE, width=1)

    rule(d, mx, rx, 780, width=2)

    # ---- ICJ band ----
    y = 794
    f = font(SANS_BOLD, 16)
    d.text((mx, y), "THE HAGUE  ·  JUSTICE", font=f, fill=RED)
    f = font(SERIF_BLACK, 30)
    d.text((mx, y + 26), "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
           font=f, fill=INK)
    f = font(SERIF, 18)
    draw_lines(d, mx, y + 64,
               wrap(d, "The International Court of Justice ruled on Thursday "
                       "that Myanmar committed genocide against the Rohingya "
                       "in 2017 — 9 votes to 6, the first time a state has "
                       "been found guilty of genocide.",
                    f, 944),
               f, leading=23)

    rule(d, mx, rx, 912, width=2)

    # ---- ALSO strip ----
    y = 924
    f = font(SANS_BOLD, 16)
    d.text((mx, y), "ALSO", font=f, fill=RED)
    f = font(SERIF, 16)
    draw_lines(d, mx + 62, y,
               wrap(d, "Anthropic +17% on debut after the record $81.3bn IPO  ·  "
                       "GTA VI sales pass $1.8bn  ·  Europe ready for Ukraine "
                       "talks with Russia  ·  South Korea’s exports top $1trn  ·  "
                       "Hayabusa2 scraps asteroid landing",
                    f, 944 - 62),
               f, leading=20)

    # ---- footer ----
    f = font(SANS, 14)
    foot = "Sources: Reuters · BBC · NASA · IMD · AP — Drawn from code; no photographs."
    d.text(((W - d.textlength(foot, font=f)) / 2, 984), foot, font=f, fill=GREY)

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out)
