#!/usr/bin/env python3
"""Build the 26 November 2026 one-page world-news newspaper.

Draws the full broadsheet page (1800x2853) and a 646x1024 entry
version, using only Pillow and fonts already on the system.
No network access, no external assets: every word is typed out
in the data tables below.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE_W, PAGE_H = 1800, 2853
MARGIN = 70
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (251, 248, 241)
INK = (18, 18, 18)
RED = (172, 28, 28)
NAVY = (28, 54, 96)
GREY = (112, 110, 105)
HAIR = (196, 193, 186)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


MASTHEAD = font(SERIF_BLACK, 104)
DATE_FONT = font(SANS_BOLD, 29)
KICKER = font(SANS_BOLD, 25)
LEAD_HEAD = font(SERIF_BOLD, 48)
LEAD_BODY = font(SERIF, 28)
LEAD_SRC = font(SANS, 24)
ALSO_HEAD = font(SANS_BOLD, 29)
ALSO_KICK = font(SANS_BOLD, 24)
ALSO_BODY = font(SERIF, 24)
BANNER = font(SANS_BOLD, 30)
NUM_FONT = font(SANS_BOLD, 27)
HEAD_FONT = font(SERIF_BOLD, 30)
DECK_FONT = font(SERIF, 23)
SRC_FONT = font(SANS, 20)
FOOT_FONT = font(SERIF, 22)
FOOT_BOLD = font(SANS_BOLD, 25)

LEADS = [
    {
        "kick": "MIDDLE EAST \u00b7 LEAD",
        "head": "Iranian drone strike in Kuwait kills two Italians as war widens",
        "deck": (
            "Two Italians were killed in an Iranian drone attack in Kuwait, "
            "Italy's foreign minister said. The victims were technicians "
            "working for the Italian unit of German defence group "
            "Rheinmetall, in a further widening of the regional war."
        ),
        "src": "\u2014 Reuters",
    },
    {
        "kick": "DIPLOMACY \u00b7 LEAD",
        "head": "Trump: Russia-Ukraine peace deal a 'strong possibility'",
        "deck": (
            "President Trump urged Vladimir Putin to end military aggression "
            "across Europe after talks in China, saying a deal between "
            "Russia and Ukraine was a strong possibility. He also met NATO "
            "chief Mark Rutte at Mar-a-Lago to brief him on the talks."
        ),
        "src": "\u2014 Truth Social / Free Press Journal",
    },
]

ALSO = [
    ("GENEVA",
     "A UN report says five women were killed every hour by lovers or "
     "close relatives in 2025."),
    ("SPORT",
     "Former IOC vice-president and trailblazer Anita DeFrantz dies at 74."),
    ("WASHINGTON",
     "Kushner praises Putin and says the Russian leader has shown "
     "restraint, including on nuclear weapons."),
    ("MINSK",
     "Belarus and Russia sign a 2027-2029 foreign policy program."),
]

# Each column: a list of ("banner", label) and ("story", num, head, deck, src).
COLUMNS = [
    [
        ("banner", "NORTH AMERICA"),
        ("story", "01", "Macy's Thanksgiving parade postponed in storm first",
         "Macy's 100th Thanksgiving Day parade in New York was postponed "
         "due to severe weather, the first postponement in 100 years, as a "
         "storm bore down on the East Coast.", "XINHUA / NDTV"),
        ("story", "02", "Trump uses Thanksgiving message to lash out at foes",
         "As Americans gathered for Thanksgiving, President Trump used the "
         "holiday to attack liberals, immigrants and a federal agency in a "
         "message on Truth Social.", "REUTERS"),
        ("story", "03", "US Army hails Iowa explosives detonation a success",
         "The US Army declared success in detonating a five-ton stockpile "
         "of lead azide explosives in Iowa, disposing of the ageing "
         "munitions in a controlled blast.", "REUTERS / NDTV"),
        ("story", "04", "New York court upholds Mamdani's rent freeze",
         "A New York court upheld Mayor Mamdani's rent freeze, handing the "
         "new mayor a win in one of his signature housing policies.",
         "REUTERS"),
        ("story", "05", "Airliner in emergency landing after door bid mid-air",
         "An American Airlines flight made an emergency landing after a "
         "passenger attempted to open a door mid-air, the airline said.",
         "NDTV"),
        ("banner", "AFRICA & LATIN AMERICA"),
        ("story", "06", "Kenyan cult leader convicted of terrorism charges",
         "A Kenyan court convicted cult leader Paul Mackenzie, serving 200 "
         "years for murdering nearly 200 children, of terrorism-related "
         "charges over one of the deadliest cult killings of modern times.",
         "REUTERS"),
        ("story", "07", "Guinea-Bissau delays elections by two years",
         "Guinea-Bissau's military leaders delayed presidential and "
         "legislative elections by roughly two years, to November 2028, "
         "saying conditions were not in place a year after the coup.",
         "REUTERS"),
        ("story", "08", "Rains kill at least eight in Brazil",
         "At least eight people were killed as heavy rains battered "
         "southern and southeastern Brazil, officials said.", "XINHUA"),
    ],
    [
        ("banner", "MIDDLE EAST"),
        ("story", "09", "Houthis say they hit two Saudi ports",
         "Yemen's Houthis said they attacked the Saudi ports of Jeddah and "
         "Jazan in response to coalition strikes on the Red Sea port of "
         "Hodeida.", "NDTV / XINHUA"),
        ("story", "10", "Saudi coalition intercepts three Houthi missiles",
         "The Saudi-led coalition intercepted three Houthi missiles, state "
         "media said, as the exchange of strikes across the Red Sea "
         "continued.", "XINHUA"),
        ("story", "11", "Israel kills Hamas security official in Gaza",
         "An Israeli strike killed Hamas security official Khaled Abu Nada "
         "along with his family in Gaza City, medics said.", "NDTV"),
        ("story", "12", "UN warns of meningitis surge in Gaza",
         "The UN warned of rising meningitis cases in Gaza and displacement "
         "in the West Bank as health conditions in the territory "
         "deteriorate.", "XINHUA"),
        ("story", "13", "Iraq shuts two Kurdistan border crossings",
         "Iraqi border forces closed two crossings with Syria and Iran "
         "administered by the Kurdistan Regional Government, as Baghdad "
         "moves to assert control over the region.", "REUTERS"),
        ("banner", "TECH, SCIENCE & MARKETS"),
        ("story", "14", "FCC clears SpaceX plan for a million orbital data-centre satellites",
         "The FCC gave SpaceX conditional approval to deploy up to one "
         "million satellites for an orbital data-centre network, despite "
         "objections from Amazon, Viasat and astronomers.",
         "NDTV / SEVEN LIGHTS"),
        ("story", "15", "Nvidia halts AI server shipments to four Asian states",
         "Nvidia told Dell and Supermicro to stop shipping AI servers to "
         "Malaysia, Singapore, Thailand and Indonesia, the FT reported, as "
         "US chip controls bite.", "NDTV / FT"),
        ("story", "16", "Asian tech stocks rebound",
         "Asian markets gained as tech stocks recovered from the Wall "
         "Street sell-off: Japan's Nikkei rose 1.3%, South Korea's Kospi "
         "1.2%, Taiwan's Taiex 2.6% and Hong Kong's Hang Seng 1.9%.", "AP"),
    ],
    [
        ("banner", "EUROPE"),
        ("story", "17", "Kremlin warns EU war funding could hit peace talks",
         "The Kremlin warned that increased European military funding for "
         "Ukraine could affect peace negotiations with Russia, spokesman "
         "Dmitry Peskov said, calling it 'not money for peace'.",
         "INFORMAT.RO / REUTERS"),
        ("story", "18", "34 nations and EU demand Russia stop chemical weapons",
         "Officials from 34 countries and the EU issued a joint statement "
         "calling on Russia to immediately stop using toxic chemicals and "
         "riot-control agents in Ukraine.", "REUTERS / IC BRIEF"),
        ("story", "19", "UK net migration falls to 77,000",
         "Net migration to the UK fell to 77,000, the lowest since 1997 "
         "apart from the Covid years, official figures showed.", "NDTV"),
        ("story", "20", "Russian refinery ablaze after drone attack",
         "Fire broke out at the Slavyansk ECO oil refinery in Russia's "
         "Krasnodar region after a drone attack, seriously damaging a "
         "crude distillation unit, the company said.", "REUTERS"),
        ("banner", "ASIA-PACIFIC"),
        ("story", "21", "Japan's JERA in talks with Anthropic, Meta on data centres",
         "Japan's largest power generator, JERA, entered talks with "
         "Anthropic, Meta and other US tech giants to build data centres "
         "near power plants in the Tokyo area, Nikkei reported.",
         "REUTERS / NIKKEI"),
        ("story", "22", "India asks Netflix not to air Pakistani show",
         "Prime Minister Modi's government asked Netflix not to air a "
         "Pakistani series in India, local media reported, after a film "
         "workers' union wrote to Modi seeking a ban.", "REUTERS"),
        ("story", "23", "Kim Jong Un urges wider use of tactical nuclear arms",
         "North Korea's Kim Jong Un called for diversified use of tactical "
         "nuclear weapons, state media reported.", "NDTV"),
        ("story", "24", "Bangladesh garment workers strike over wages",
         "Bangladeshi garment workers demanded a wage hike, forcing factory "
         "shutdowns in fresh protests over pay.", "REUTERS"),
    ],
]

FOOT_SOURCES = (
    "Sources: Reuters \u00b7 AP \u00b7 Xinhua \u00b7 NDTV \u00b7 Nikkei \u00b7 FT "
    "\u00b7 IC Brief \u00b7 Free Press Journal \u00b7 Seven Lights \u00b7 "
    "informat.ro (2026-11-26). Claims marked 'says / reported' are "
    "attributed and preliminary. All stories dated 26 November 2026."
)
FOOT_LINE = (
    "THE WORLD IN ONE PAGE \u00b7 26 NOVEMBER 2026 \u00b7 Generated by a "
    "program for the make.fun news-image bounty"
)


def wrap(dr, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if dr.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(dr, x, y, lines, fnt, leading, fill):
    for ln in lines:
        dr.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_lead(dr, x, y, width, lead):
    dr.text((x, y), lead["kick"], font=KICKER, fill=RED)
    y += 30
    y = para(dr, x, y, wrap(dr, lead["head"], LEAD_HEAD, width),
             LEAD_HEAD, 57, INK)
    y += 8
    y = para(dr, x, y, wrap(dr, lead["deck"], LEAD_BODY, width),
             LEAD_BODY, 35, INK)
    y += 6
    dr.text((x, y), lead["src"], font=LEAD_SRC, fill=GREY)
    return y + 24


def draw_story(dr, x, y, width, num, head, deck, src):
    dr.text((x, y), num, font=NUM_FONT, fill=RED)
    tx = x + 62
    tw = width - 62
    y = para(dr, tx, y, wrap(dr, head, HEAD_FONT, tw), HEAD_FONT, 34, INK)
    y += 4
    y = para(dr, tx, y, wrap(dr, deck, DECK_FONT, tw), DECK_FONT, 28, INK)
    y += 4
    dr.text((tx, y), src, font=SRC_FONT, fill=GREY)
    return y + 20 + 6


def draw_banner(dr, x, y, width, label):
    dr.rectangle([x, y, x + width, y + 48], fill=NAVY)
    dr.text((x + 16, y + 8), label, font=BANNER, fill=(255, 255, 255))
    return y + 48 + 10


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    dr = ImageDraw.Draw(img)
    y = 36

    # Masthead + dateline.
    dr.text((MARGIN, y), "THE WORLD IN ONE PAGE", font=MASTHEAD, fill=INK)
    y += 122
    dr.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 5], fill=INK)
    y += 17
    dr.text((MARGIN, y), "THURSDAY, 26 NOVEMBER 2026",
            font=DATE_FONT, fill=INK)
    right = "24 STORIES \u00b7 6 REGIONS"
    dr.text((PAGE_W - MARGIN - dr.textlength(right, font=DATE_FONT), y),
            right, font=DATE_FONT, fill=RED)
    y += 36
    dr.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 2], fill=INK)
    y += 22

    # Two lead stories, side by side.
    lead_w = (CONTENT_W - 36) // 2
    y1 = draw_lead(dr, MARGIN, y, lead_w, LEADS[0])
    y2 = draw_lead(dr, MARGIN + lead_w + 36, y, lead_w, LEADS[1])
    y = max(y1, y2) + 14
    dr.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 2], fill=INK)
    y += 16

    # "Also" strip: four short items.
    dr.text((MARGIN, y), "ALSO ON 26 NOVEMBER", font=ALSO_HEAD, fill=NAVY)
    y += 36
    also_w = (CONTENT_W - 3 * 28) // 4
    bottom = y
    for i, (kick, body) in enumerate(ALSO):
        ax = MARGIN + i * (also_w + 28)
        dr.text((ax, y), kick, font=ALSO_KICK, fill=RED)
        end = para(dr, ax, y + 32, wrap(dr, body, ALSO_BODY, also_w),
                   ALSO_BODY, 29, INK)
        bottom = max(bottom, end)
    y = bottom + 12
    dr.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 2], fill=INK)
    y += 22
    cols_top = y

    # Three columns of sections.
    gutter = 36
    col_w = (CONTENT_W - 2 * gutter) // 3
    col_xs = [MARGIN + i * (col_w + gutter) for i in range(3)]
    col_bottom = cols_top
    for ci, items in enumerate(COLUMNS):
        cy = cols_top
        for item in items:
            if item[0] == "banner":
                cy = draw_banner(dr, col_xs[ci], cy, col_w, item[1])
            else:
                _, num, head, deck, src = item
                cy = draw_story(dr, col_xs[ci], cy, col_w,
                                num, head, deck, src)
        col_bottom = max(col_bottom, cy)

    # Hairline dividers between columns.
    for gx in (col_xs[1] - gutter // 2, col_xs[2] - gutter // 2):
        dr.line([(gx, cols_top), (gx, col_bottom)], fill=HAIR, width=1)

    # Footer.
    y = col_bottom + 16
    dr.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 2], fill=INK)
    y += 14
    y = para(dr, MARGIN, y, wrap(dr, FOOT_SOURCES, FOOT_FONT, CONTENT_W),
             FOOT_FONT, 28, GREY)
    y += 8
    dr.text((MARGIN, y), FOOT_LINE, font=FOOT_BOLD, fill=INK)
    y += 24
    print("columns top:", cols_top, "columns bottom:", col_bottom,
          "page bottom used:", y, "of", PAGE_H)

    full_path = os.path.join(HERE, "world-news-26-nov-2026.png")
    img.save(full_path)
    small = img.resize((646, 1024), Image.LANCZOS)
    small.save(os.path.join(HERE, "entry.png"))
    print("saved", full_path, img.size)
    print("saved entry.png", small.size)


if __name__ == "__main__":
    build()
