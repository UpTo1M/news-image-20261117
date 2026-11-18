#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page as a 1024x1024 PNG.

Layout: newspaper masthead ("WORLD NEWS" + date band) on top, then six
story blocks in a 2x3 grid. Each block has a simple drawn icon, a bold
headline and one short factual line. Dark text on white paper, large type
so it stays legible when the image is shown small.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (15, 27, 61)
RED = (185, 28, 28)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
RULE = (190, 190, 190)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_radar(d, cx, cy, s, c):
    r = s // 2
    for frac in (1.0, 0.66, 0.33):
        rr = int(r * frac)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=c, width=4)
    d.line([cx, cy, cx + r, cy - r], fill=c, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=c)
    d.ellipse([cx + r // 2 - 5, cy - r // 2 - 5,
               cx + r // 2 + 5, cy - r // 2 + 5], fill=c)


def icon_bridge(d, cx, cy, s, c):
    hw = s // 2
    top, bot = cy - s // 3, cy + s // 3
    d.line([cx - hw, bot, cx + hw, bot], fill=c, width=5)  # deck
    for tx in (cx - hw + 8, cx + hw - 8):  # towers
        d.line([tx, top - 6, tx, bot], fill=c, width=5)
    d.arc([cx - hw, top - s // 2, cx + hw, top + s // 2], 0, 180,
          fill=c, width=4)  # main cable
    for fx in (-0.5, -0.25, 0.0, 0.25, 0.5):  # suspenders
        x = cx + int(hw * fx)
        d.line([x, top + 10, x, bot], fill=c, width=3)
    # crack in the deck
    d.line([cx, bot, cx + 8, bot - 12, cx - 4, bot - 20], fill=RED, width=4)


def icon_plane(d, cx, cy, s, c):
    hw = s // 2
    # fuselage pointing right, wings, tail
    d.polygon([(cx - hw, cy), (cx + hw - 8, cy - 8), (cx + hw, cy),
               (cx + hw - 8, cy + 8)], fill=c)
    d.polygon([(cx - 6, cy - 4), (cx - hw // 2, cy - s // 2),
               (cx + 4, cy - 4)], fill=c)
    d.polygon([(cx - 6, cy + 4), (cx - hw // 2, cy + s // 2),
               (cx + 4, cy + 4)], fill=c)
    d.polygon([(cx - hw + 2, cy - 4), (cx - hw + 14, cy - s // 3),
               (cx - hw + 18, cy - 4)], fill=c)


def icon_barrier(d, cx, cy, s, c):
    hw = s // 2
    top, bot = cy - s // 3, cy + s // 3
    for px in (cx - hw + 6, cx + hw - 6):  # posts
        d.line([px, top, px, bot], fill=c, width=6)
    # striped barrier arm
    d.line([cx - hw, top + 8, cx + hw, top + 8], fill=RED, width=10)
    for i in range(5):
        x0 = cx - hw + i * (2 * hw // 5)
        d.line([x0, top + 3, x0 + 10, top + 13], fill=WHITE, width=4)
    d.line([cx - hw, bot, cx + hw, bot], fill=c, width=4)


def icon_jet(d, cx, cy, s, c):
    hw = s // 2
    d.polygon([(cx + hw, cy), (cx - hw // 2, cy - 10),
               (cx - hw, cy), (cx - hw // 2, cy + 10)], fill=c)
    d.polygon([(cx - 4, cy - 6), (cx - hw // 3, cy - s // 2),
               (cx + hw // 4, cy - 6)], fill=c)
    d.polygon([(cx - 4, cy + 6), (cx - hw // 3, cy + s // 2),
               (cx + hw // 4, cy + 6)], fill=c)
    d.polygon([(cx - hw + 4, cy - 4), (cx - hw + 16, cy - s // 4),
               (cx - hw + 20, cy - 4)], fill=c)


def icon_drone(d, cx, cy, s, c):
    hw = s // 2
    d.rectangle([cx - 12, cy - 8, cx + 12, cy + 8], fill=c)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ax, ay = cx + sx * hw // 2, cy + sy * hw // 2
        d.line([cx, cy, ax, ay], fill=c, width=4)
        d.ellipse([ax - 14, ay - 5, ax + 14, ay + 5], outline=c, width=4)


# ---------------------------------------------------------------- page
STORIES = [
    ("IRAN STRIKES U.S. RADAR IN BAHRAIN",
     "Iran fired drones at a U.S. military radar site in Bahrain, its "
     "third attack on American targets there in days.",
     icon_radar),
    ("UKRAINE HITS KERCH BRIDGE",
     "Ukraine severely damaged the bridge linking Russia to Crimea; "
     "Russia struck Kyiv bridges in return.",
     icon_bridge),
    ("TRUMP HEADS TO ASIA",
     "Trump in Manila for the ASEAN summit, then trilateral nuclear "
     "talks with Xi Jinping and Vladimir Putin in Shenzhen.",
     icon_plane),
    ("ESTONIA CLOSES RUSSIA BORDER",
     "All crossings shut from 1 December after a foiled Russian "
     "sabotage plot.",
     icon_barrier),
    ("JAPAN SCRAMBLES JETS",
     "After suspected Russian aircraft violated its airspace.",
     icon_jet),
    ("HOUTHIS ADVANCE IN YEMEN",
     "Pushing toward Aden; drones fired at a Saudi oil pipeline.",
     icon_drone),
]


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    m = 32  # margin

    # ---- masthead
    d.line([m, 26, W - m, 26], fill=NAVY, width=4)
    mast = font(BOLD, 96)
    title = "WORLD NEWS"
    tw = mast.getlength(title)
    d.text(((W - tw) / 2, 38), title, font=mast, fill=NAVY)
    d.line([m, 152, W - m, 152], fill=NAVY, width=3)
    # date band
    d.rectangle([m, 166, W - m, 214], fill=NAVY)
    date_f = font(BOLD, 36)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = date_f.getlength(date)
    d.text(((W - dw) / 2, 172), date, font=date_f, fill=WHITE)

    # ---- story grid: 2 columns x 3 rows
    grid_top, grid_bottom = 238, 986
    row_gap, col_gap = 16, 24
    row_h = (grid_bottom - grid_top - 2 * row_gap) // 3
    col_w = (W - 2 * m - col_gap) // 2
    head_f = font(BOLD, 32)
    body_f = font(REG, 24)
    icon_s = 80

    for i, (headline, body, icon_fn) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = m + col * (col_w + col_gap)
        y = grid_top + row * (row_h + row_gap)

        # light dividers between blocks
        if row > 0:
            d.line([m, y - row_gap // 2, W - m, y - row_gap // 2],
                   fill=RULE, width=2)
        if col > 0:
            d.line([x - col_gap // 2, y, x - col_gap // 2, y + row_h],
                   fill=RULE, width=2)

        # icon, top-left of the block
        icon_fn(d, x + icon_s // 2, y + icon_s // 2 + 6, icon_s, RED)

        # text column to the right of the icon
        tx = x + icon_s + 16
        tw_max = col_w - icon_s - 16
        lines = wrap(headline, head_f, tw_max)
        ty = y + 4
        for ln in lines:
            d.text((tx, ty), ln, font=head_f, fill=NAVY)
            ty += 38
        ty += 8
        for ln in wrap(body, body_f, tw_max):
            d.text((tx, ty), ln, font=body_f, fill=INK)
            ty += 30

    # ---- footer
    d.line([m, 1000, W - m, 1000], fill=NAVY, width=2)
    foot_f = font(REG, 17)
    foot = "Six stories that defined Tuesday, 17 November 2026."
    fw = foot_f.getlength(foot)
    d.text(((W - fw) / 2, 1006), foot, font=foot_f, fill=GRAY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
