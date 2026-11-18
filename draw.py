#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page as a 1024x1024 PNG.

Dense front page: masthead with the day named prominently, a large lead
story, then 30 further real stories grouped by region in two columns, plus
a footer of briefs. Dark text on white paper, clear hierarchy so the page
stays legible when shown small. All stories are real, verified news from
Tuesday, 17 November 2026. Headlines and summaries are kept to one line
each so the dense layout fits without overlap.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (15, 27, 61)
RED = (185, 28, 28)
INK = (25, 25, 25)
GRAY = (100, 100, 100)
RULE = (190, 190, 190)
WHITE = (255, 255, 255)
LEAD_BG = (246, 246, 242)


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


LEAD_HEAD = "US SINKS FIVE IRANIAN TANKERS AS WAR AT SEA ERUPTS"
LEAD_SUM = ("Tehran's forces twice targeted a US warship; Iran fired missiles at "
            "US troops in Jordan and 10 ships near Hormuz as oil topped $100.")

# (headline, one-line summary) — kept short so each fits on one line.
REGIONS_LEFT = [
    ("MIDDLE EAST", [
        ("US jets hit Qeshm Island missile site",
         "Iran hit a US base in Bahrain and claims it downed a US MQ-9 drone."),
        ("Trump: US 'looking into' Iran dirty-bomb report",
         "Trump takes a dirty-bomb plot report seriously; Iran denies the claim."),
        ("Houthis advance on Aden as army retreats",
         "Saudi named a new coalition chief as rebels neared the port city."),
        ("Israeli strike on Gaza tents kills three",
         "Settler attacks hit the West Bank as families returned to Sabra."),
        ("Four nations urge Israel to open Gaza aid",
         "The UK, Australia, Canada and Italy called the situation catastrophic."),
        ("Iraq vows to clear Kataib Hezbollah stronghold",
         "Baghdad threatened to retake Jurf al-Sakhar from the militia."),
    ]),
    ("AFRICA", [
        ("South Africa: 17 killed in two mass shootings",
         "Nine dead near Pretoria and eight near Pietermaritzburg in two attacks."),
        ("DR Congo Ebola 'out of control': 5,500 dead",
         "Africa CDC reported over 11,200 infections across eight provinces."),
        ("Ethiopia expels six Sudan diplomats",
         "Addis Ababa closed Sudan's consulate amid mutual accusations."),
        ("Amnesty: UN failed to stop S. Sudan massacre",
         "Peacekeepers ignored warnings before a village attack, Amnesty said."),
    ]),
    ("ASIA-PACIFIC", [
        ("APEC CEO Summit opens in Shenzhen",
         "Over 2,000 leaders from 21 economies gathered in Shenzhen, China."),
        ("India edge Pakistan in U19 Asia Cup thriller",
         "India won by one wicket off the last ball in the Oman final."),
        ("Pakistan cuts petrol, diesel prices by Rs2",
         "Petrol fell to Rs328 and diesel to Rs358 a litre from today."),
        ("ECO summit adopts Vision 2035 in Islamabad",
         "Ministers approved a ten-year roadmap for trade and connectivity."),
        ("Albanese in China as superpower talks loom",
         "Australia's PM prepared for Xi talks as the trilateral overshadowed APEC."),
    ]),
]

REGIONS_RIGHT = [
    ("EUROPE", [
        ("Ukraine hits Kerch Bridge for a second day",
         "A span fell into the strait; two killed as Russia closed the bridge."),
        ("Russian strike on Zaporizhzhia kills 40",
         "A strike on a school aid centre killed at least 26, Ukraine said."),
        ("Russia: French troops in Ukraine are targets",
         "Moscow warned Paris that sending troops would be direct involvement."),
        ("Japan scrambles jets as Russian planes intrude",
         "Two suspected Russian planes violated Japanese airspace early Tuesday."),
        ("COP31 draft: faster fossil-fuel exit, $120bn",
         "Antalya negotiators published a draft calling for more climate finance."),
        ("UK sanctions Israeli settlement firms",
         "London acted to protect the two-state solution as settler violence rose."),
        ("Le Pen vows earlier retirement if she wins",
         "France's far-right leader promised an earlier pension age for many."),
        ("EU charges Temu over illegal product sales",
         "Brussels said the platform did not do enough to stop unlawful goods."),
    ]),
    ("AMERICAS", [
        ("US loses measles-free status after 26 years",
         "Over 5,400 cases and 10 deaths in the worst outbreak in three decades."),
        ("Nvidia posts bumper results after Huang exit",
         "The AI chip giant reported strong earnings a day after its chief left."),
        ("US soldier held in UK on spying suspicion",
         "The serviceman was arrested by UK police and taken into US custody."),
        ("Major US banks hit by unexplained outages",
         "Customers were locked out in a wave of unexplained banking failures."),
        ("United Airlines outage strands passengers",
         "A system failure left travellers stuck on the tarmac across the US."),
        ("Trump in Asia ahead of talks with Putin, Xi",
         "Trump said he would be open to a one-on-one with Russia's leader."),
        ("Xi-Trump-Putin summit set for Thursday",
         "The first-ever trilateral of the three leaders will take place at APEC."),
        ("Epstein death was murder, expert claims",
         "A forensic expert said the examiner's file showed homicide, not suicide."),
    ]),
]

FOOTER = ("ALSO: Guinea arrests 1,200 in gold-mining crackdown  \u2022  "
          "Trump denies visa to Bethlehem priest  \u2022  "
          "FAA seeks $50bn more for air traffic control")


def draw_column(d, regions, x, col_w, top, bottom):
    """Draw region sections into one column. Returns the final y."""
    y = top
    f_label = font(BOLD, 19)
    f_head = font(BOLD, 17)
    f_sum = font(REG, 13)
    for name, stories in regions:
        # Region label: red name + thin rule.
        d.text((x, y), name, font=f_label, fill=RED)
        y += 24
        d.line([x, y, x + col_w, y], fill=RULE, width=1)
        y += 6
        for head, summ in stories:
            hl = wrap(head, f_head, col_w)
            sl = wrap(summ, f_sum, col_w)
            if len(hl) > 1 or len(sl) > 1:
                print("WARNING wraps to 2 lines: %r / %r" % (head, summ))
            for ln in hl:
                d.text((x, y), ln, font=f_head, fill=INK)
                y += 20
            for ln in sl:
                d.text((x, y), ln, font=f_sum, fill=GRAY)
                y += 16
            y += 3  # gap between stories
        y += 2  # gap after a region
    return y


def build_image():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Masthead -----------------------------------------------------
    f_title = font(BOLD, 56)
    f_date = font(BOLD, 27)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 6), title, font=f_title, fill=NAVY)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 64), date, font=f_date, fill=RED)
    d.line([24, 96, W - 24, 96], fill=NAVY, width=3)

    # ---- Lead story ---------------------------------------------------
    d.rectangle([24, 104, W - 24, 256], fill=LEAD_BG, outline=RULE, width=1)
    f_lead_tag = font(BOLD, 15)
    d.text((36, 112), "LEAD", font=f_lead_tag, fill=RED)
    f_lead_head = font(BOLD, 30)
    f_lead_sum = font(REG, 19)
    hl = wrap(LEAD_HEAD, f_lead_head, W - 72)
    y = 132
    for ln in hl:
        d.text((36, y), ln, font=f_lead_head, fill=NAVY)
        y += 35
    sl = wrap(LEAD_SUM, f_lead_sum, W - 72)
    for ln in sl:
        d.text((36, y), ln, font=f_lead_sum, fill=INK)
        y += 23

    # ---- Body: two columns --------------------------------------------
    body_top, body_bottom = 268, 980
    col_w = 476
    y_left = draw_column(d, REGIONS_LEFT, 24, col_w, body_top, body_bottom)
    y_right = draw_column(d, REGIONS_RIGHT, 524, col_w, body_top, body_bottom)

    # ---- Footer -------------------------------------------------------
    d.line([24, 984, W - 24, 984], fill=NAVY, width=2)
    f_foot = font(REG, 13)
    fw = d.textlength(FOOTER, font=f_foot)
    d.text(((W - fw) / 2, 996), FOOTER, font=f_foot, fill=GRAY)

    print("column end y: left=%d right=%d (body bottom=%d)" % (y_left, y_right, body_bottom))
    return img


def main():
    img = build_image()
    img.save("entry.png", format="PNG")
    print("saved entry.png", img.size, img.mode)


if __name__ == "__main__":
    main()
