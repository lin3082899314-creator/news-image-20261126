#!/usr/bin/env python3
"""Generate one newspaper front-page image summing up 26 November 2026 world news.

Entry for make.fun bounty "Sum up 26 November's world news in one image"
(news-image-20261126, $100, 50 places, closes 28 Nov 2026 08:00).

Run:  python3 generate_news_image.py
Out:   world-news-26-nov-2026.png  (1800 wide, cropped to content)
       entry.png                   (same page scaled to fit 1024x1024)

All 24 stories are dated 26 Nov 2026 in the cited reporting (Reuters, AP,
Xinhua, NDTV, Nikkei, FT, IC Brief, Free Press Journal, Seven Lights).
Preliminary/claimed items are attributed in the text ("says", "reports say",
"according to").
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1800, 3600  # cropped to content after drawing
M = 64  # margin
BG = (250, 248, 242)      # newsprint
INK = (18, 18, 18)
RED = (158, 27, 27)
GREY = (90, 86, 80)
RULE = (60, 58, 52)
ACCENT = (31, 58, 95)     # deep blue for section bars

F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (region, headline, summary, source)
LEADS = [
    ("MIDDLE EAST  ·  LEAD",
     "Iranian drone strike in Kuwait kills two Italians as war widens",
     "Two Italians were killed in an Iranian drone attack in Kuwait, Italy's "
     "foreign minister said. The victims were technicians working for the Italian "
     "unit of German defence group Rheinmetall, in a further widening of the "
     "regional war.",
     "Reuters"),
    ("DIPLOMACY  ·  LEAD",
     "Trump: Russia-Ukraine peace deal a 'strong possibility'",
     "President Trump urged Vladimir Putin to end military aggression across Europe "
     "after talks in China, saying a deal between Russia and Ukraine was a strong "
     "possibility. He also met NATO chief Mark Rutte at Mar-a-Lago to brief him "
     "on the talks.",
     "Truth Social / Free Press Journal"),
]

SECTIONS = [
    ("NORTH AMERICA", [
        ("Macy's Thanksgiving parade postponed in storm first",
         "Macy's 100th Thanksgiving Day parade in New York was postponed due to severe weather, the first postponement in 100 years, as a storm bore down on the East Coast.",
         "Xinhua / NDTV"),
        ("Trump uses Thanksgiving message to lash out at foes",
         "As Americans gathered for Thanksgiving, President Trump used the holiday to attack liberals, immigrants and a federal agency in a message on Truth Social.",
         "Reuters"),
        ("US Army hails Iowa explosives detonation a success",
         "The US Army declared success in detonating a five-ton stockpile of lead azide explosives in Iowa, disposing of the ageing munitions in a controlled blast.",
         "Reuters / NDTV"),
        ("New York court upholds Mamdani's rent freeze",
         "A New York court upheld Mayor Mamdani's rent freeze, handing the new mayor a win in one of his signature housing policies.",
         "Reuters"),
        ("Airliner in emergency landing after door bid mid-air",
         "An American Airlines flight made an emergency landing after a passenger attempted to open a door mid-air, the airline said.",
         "NDTV"),
    ]),
    ("EUROPE", [
        ("Kremlin warns EU war funding could hit peace talks",
         "The Kremlin warned that increased European military funding for Ukraine could affect peace negotiations with Russia, spokesman Dmitry Peskov said, calling it 'not money for peace'.",
         "informat.ro / Reuters"),
        ("34 nations and EU demand Russia stop chemical weapons",
         "Officials from 34 countries and the EU issued a joint statement calling on Russia to immediately stop using toxic chemicals and riot-control agents in Ukraine.",
         "Reuters / IC Brief"),
        ("UK net migration falls to 77,000",
         "Net migration to the UK fell to 77,000, the lowest since 1997 apart from the Covid years, official figures showed.",
         "NDTV"),
        ("Russian refinery ablaze after drone attack",
         "Fire broke out at the Slavyansk ECO oil refinery in Russia's Krasnodar region after a drone attack, seriously damaging a crude distillation unit, the company said.",
         "Reuters"),
    ]),
    ("MIDDLE EAST", [
        ("Houthis say they hit two Saudi ports",
         "Yemen's Houthis said they attacked the Saudi ports of Jeddah and Jazan in response to coalition strikes on the Red Sea port of Hodeida.",
         "NDTV / Xinhua"),
        ("Saudi coalition intercepts three Houthi missiles",
         "The Saudi-led coalition intercepted three Houthi missiles, state media said, as the exchange of strikes across the Red Sea continued.",
         "Xinhua"),
        ("Israel kills Hamas security official in Gaza",
         "An Israeli strike killed Hamas security official Khaled Abu Nada along with his family in Gaza City, medics said.",
         "NDTV"),
        ("UN warns of meningitis surge in Gaza",
         "The UN warned of rising meningitis cases in Gaza and displacement in the West Bank as health conditions in the territory deteriorate.",
         "Xinhua"),
        ("Iraq shuts two Kurdistan border crossings",
         "Iraqi border forces closed two crossings with Syria and Iran administered by the Kurdistan Regional Government, as Baghdad moves to assert control over the region.",
         "Reuters"),
    ]),
    ("ASIA-PACIFIC", [
        ("Japan's JERA in talks with Anthropic, Meta on data centres",
         "Japan's largest power generator, JERA, entered talks with Anthropic, Meta and other US tech giants to build data centres near power plants in the Tokyo area, Nikkei reported.",
         "Reuters / Nikkei"),
        ("India asks Netflix not to air Pakistani show",
         "Prime Minister Modi's government asked Netflix not to air a Pakistani series in India, local media reported, after a film workers' union wrote to Modi seeking a ban.",
         "Reuters"),
        ("Kim Jong Un urges wider use of tactical nuclear arms",
         "North Korea's Kim Jong Un called for diversified use of tactical nuclear weapons, state media reported.",
         "NDTV"),
        ("Bangladesh garment workers strike over wages",
         "Bangladeshi garment workers demanded a wage hike, forcing factory shutdowns in fresh protests over pay.",
         "Reuters"),
    ]),
    ("AFRICA & LATIN AMERICA", [
        ("Kenyan cult leader convicted of terrorism charges",
         "A Kenyan court convicted cult leader Paul Mackenzie, serving 200 years for murdering nearly 200 children, of terrorism-related charges over one of the deadliest cult killings of modern times.",
         "Reuters"),
        ("Guinea-Bissau delays elections by two years",
         "Guinea-Bissau's military leaders delayed presidential and legislative elections by roughly two years, to November 2028, saying conditions were not in place a year after the coup.",
         "Reuters"),
        ("Rains kill at least eight in Brazil",
         "At least eight people were killed as heavy rains battered southern and southeastern Brazil, officials said.",
         "Xinhua"),
    ]),
    ("TECH, SCIENCE & MARKETS", [
        ("FCC clears SpaceX plan for a million orbital data-centre satellites",
         "The FCC gave SpaceX conditional approval to deploy up to one million satellites for an orbital data-centre network, despite objections from Amazon, Viasat and astronomers.",
         "NDTV / Seven Lights"),
        ("Nvidia halts AI server shipments to four Asian states",
         "Nvidia told Dell and Supermicro to stop shipping AI servers to Malaysia, Singapore, Thailand and Indonesia, the FT reported, as US chip controls bite.",
         "NDTV / FT"),
        ("Asian tech stocks rebound",
         "Asian markets gained as tech stocks recovered from the Wall Street sell-off: Japan's Nikkei rose 1.3%, South Korea's Kospi 1.2%, Taiwan's Taiex 2.6% and Hong Kong's Hang Seng 1.9%.",
         "AP"),
    ]),
]

ALSO = [
    ("GENEVA", "A UN report says five women were killed every hour by lovers or close relatives in 2025."),
    ("SPORT", "Former IOC vice-president and trailblazer Anita DeFrantz dies at 74."),
    ("WASHINGTON", "Kushner praises Putin and says the Russian leader has shown restraint, including on nuclear weapons."),
    ("MINSK", "Belarus and Russia sign a 2027-2029 foreign policy program."),
]

SOURCES = ("Sources: Reuters · AP · Xinhua · NDTV · Nikkei · FT · IC Brief · "
           "Free Press Journal · Seven Lights · informat.ro (2026-11-26). Claims "
           "marked 'says / reported' are attributed and preliminary. All stories "
           "dated 26 November 2026.")

# ---------------------------------------------------------------- drawing
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- masthead
f_mast = font(F_SERIF_B, 96)
f_sub = font(F_SANS, 26)
f_date = font(F_SANS_B, 27)
y = 58
d.text((M, y), "THE WORLD IN ONE PAGE", font=f_mast, fill=INK)
y += 118
d.line([(M, y), (W - M, y)], fill=RULE, width=3)
y += 14
d.text((M, y), "THURSDAY, 26 NOVEMBER 2026", font=f_date, fill=INK)
right = "24 STORIES  ·  6 REGIONS"
d.text((W - M - d.textlength(right, font=f_date), y), right, font=f_date, fill=RED)
y += 44
d.line([(M, y), (W - M, y)], fill=RULE, width=3)
y += 26

# --- lead stories, two columns
col_w = (W - 2 * M - 48) // 2
f_kick = font(F_SANS_B, 24)
f_lead_h = font(F_SERIF_B, 40)
f_lead_b = font(F_SERIF, 26)
lead_top = y
lead_bottom = lead_top
for i, (kick, head, body, src) in enumerate(LEADS):
    x = M + i * (col_w + 48)
    yy = lead_top
    d.text((x, yy), kick, font=f_kick, fill=RED)
    yy += 38
    yy = draw_wrapped(d, x, yy, head, f_lead_h, col_w, leading=50)
    yy += 10
    yy = draw_wrapped(d, x, yy, body, f_lead_b, col_w, leading=35)
    yy += 8
    d.text((x, yy), "— " + src, font=font(F_SANS, 21), fill=GREY)
    lead_bottom = max(lead_bottom, yy + 30)
d.line([(M, lead_bottom), (W - M, lead_bottom)], fill=RULE, width=2)
y = lead_bottom + 22

# --- "also on 26 November" strip
f_also_h = font(F_SANS_B, 24)
d.text((M, y), "ALSO ON 26 NOVEMBER", font=f_also_h, fill=ACCENT)
y += 40
f_also_k = font(F_SANS_B, 22)
f_also_t = font(F_SERIF, 23)
also_bottom = y
for i, (k, t) in enumerate(ALSO):
    x = M + i * ((W - 2 * M) // 4)
    w = (W - 2 * M) // 4 - 28
    yy = y
    d.text((x, yy), k, font=f_also_k, fill=RED)
    yy += 32
    yy = draw_wrapped(d, x, yy, t, f_also_t, w, leading=30)
    also_bottom = max(also_bottom, yy)
y = also_bottom + 18
d.line([(M, y), (W - M, y)], fill=RULE, width=2)
y = y + 24

# --- body: 3 columns, sections assigned to balance height
# Measured section heights (bar top to next bar / last ink, px):
# NA 1025, MIDDLE EAST 998, ASIA-PACIFIC 827, EUROPE ~806, TECH ~730,
# AFRICA ~671. This pairing evens the columns (~1633-1728 px each);
# the old pairing left column 3 ~330 px shorter than column 1.
cols = [[0, 4], [2, 5], [1, 3]]  # section indices per column
f_sec = font(F_SANS_B, 28)
f_num = font(F_SANS_B, 26)
f_head = font(F_SERIF_B, 27)
f_body = font(F_SERIF, 22)
f_src = font(F_SANS, 19)
body_top = y
n = 1
col_x = [M, M + (W - 2 * M) // 3 + 16, M + 2 * (W - 2 * M) // 3 + 32]
col_wid = (W - 2 * M) // 3 - 32
body_bottom = body_top
for ci, sec_idx in enumerate(cols):
    x = col_x[ci]
    yy = body_top
    for si in sec_idx:
        sec, stories = SECTIONS[si]
        # section bar
        d.rectangle([x, yy, x + col_wid, yy + 44], fill=ACCENT)
        d.text((x + 14, yy + 6), sec, font=f_sec, fill=(255, 255, 255))
        yy += 44 + 14
        for head, body, src in stories:
            d.text((x, yy), f"{n:02d}", font=f_num, fill=RED)
            hx = x + 52
            hw = col_wid - 52
            yy2 = draw_wrapped(d, hx, yy, head, f_head, hw, leading=32)
            yy2 = draw_wrapped(d, hx, yy2 + 3, body, f_body, hw, leading=27)
            yy2 += 3
            d.text((hx, yy2), src.upper(), font=f_src, fill=GREY)
            yy = yy2 + 20
            n += 1
        yy += 4
    body_bottom = max(body_bottom, yy)
    # column rule
    if ci < 2:
        d.line([(x + col_wid + 16, body_top), (x + col_wid + 16, body_bottom)], fill=(200, 196, 188), width=1)

# --- footer, placed after the tallest column
fy = body_bottom + 26
d.line([(M, fy), (W - M, fy)], fill=RULE, width=2)
fy += 16
fy = draw_wrapped(d, M, fy, SOURCES, font(F_SANS, 20), W - 2 * M, fill=GREY, leading=27)
fy += 10
d.text((M, fy), "THE WORLD IN ONE PAGE  ·  26 NOVEMBER 2026  ·  Generated by a program for the make.fun news-image bounty",
       font=font(F_SANS_B, 20), fill=INK)
fy += 34

img = img.crop((0, 0, W, fy + 24))
img.save("world-news-26-nov-2026.png")
print("saved world-news-26-nov-2026.png", img.size, "stories:", n - 1)

# --- entry.png: same page scaled to fit inside 1024x1024, per bounty rules
entry = img.copy()
entry.thumbnail((1024, 1024), Image.LANCZOS)
entry.save("entry.png")
print("saved entry.png", entry.size)
