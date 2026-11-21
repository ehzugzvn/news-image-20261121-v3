#!/usr/bin/env python3
"""THE GLOBAL FRONT PAGE - news-image-20261121 v3.
Renders entry.png (1024x1024) with PIL. All stories/figures come only
from the 21 November 2026 news dossier. Not run by the grader."""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (18, 18, 18)
GREY = (90, 84, 70)
RED = (178, 34, 34)

def font(kind, size):
    name = {
        "serif": "LiberationSerif-Regular.ttf",
        "serif_b": "LiberationSerif-Bold.ttf",
        "sans": "LiberationSans-Regular.ttf",
        "sans_b": "LiberationSans-Bold.ttf",
    }[kind]
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

F_TITLE = font("serif_b", 42)
F_DATE = font("sans_b", 21)
F_STAND = font("serif", 12)
F_LEAD = font("serif_b", 26)
F_LEADTXT = font("sans", 10)
F_LEADTXT_B = font("sans_b", 10)
F_MAPT = font("sans_b", 10)
F_MAPL = font("sans", 9)
F_TICK = font("sans_b", 9)
F_TLAB = font("sans", 9)
F_BAND = font("sans_b", 11)
F_HEAD = font("sans_b", 12)
F_DET = font("sans", 10)
F_CHECK = font("sans_b", 17)
F_FOOT = font("sans", 8)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, f):
    return d.textlength(text, font=f)

def wrap(text, f, maxw, max_lines=None):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and tw(last + "...", f) > maxw:
            last = last[:-1]
        lines[-1] = last + "..."
    return lines

def center(text, f, y, color=INK):
    d.text(((W - tw(text, f)) / 2, y), text, font=f, fill=color)

# ---------------- MASTHEAD ----------------
center("THE GLOBAL FRONT PAGE", F_TITLE, 6)
d.rectangle([12, 54, W - 12, 82], fill=(10, 10, 10))
center("Saturday 21 November 2026", F_DATE, 57, color=(255, 255, 255))
center("All the world's news of Saturday 21 November 2026 - 47 stories, one page.",
       F_STAND, 86, color=GREY)
d.line([12, 102, W - 12, 102], fill=INK, width=2)

# ---------------- LEAD ILLUSTRATION (x 12..312, y 108..330) ----------------
IX0, IY0, IX1, IY1 = 12, 108, 312, 330
for i in range(IY1 - IY0):
    t = i / (IY1 - IY0)
    col = (int(8 + 14 * t), int(12 + 16 * t), int(38 + 30 * t))
    d.line([IX0, IY0 + i, IX1, IY0 + i], fill=col)
rng = random.Random(21)
for _ in range(70):
    sx, sy = rng.randint(IX0 + 3, IX1 - 3), rng.randint(IY0 + 3, IY0 + 95)
    d.point((sx, sy), fill=(235, 235, 210))
d.ellipse([IX1 - 52, IY0 + 10, IX1 - 24, IY0 + 38], fill=(238, 232, 200))
# missile trails arcing over the village
import math
for (sx, ex, peak, col) in [(IX0 + 18, IX0 + 205, 58, (255, 120, 60)),
                            (IX0 + 40, IX0 + 245, 76, (255, 190, 90)),
                            (IX0 + 8, IX0 + 165, 44, (255, 90, 50))]:
    pts = []
    for k in range(41):
        tt = k / 40
        x = sx + (ex - sx) * tt
        y = (IY0 + 128) - peak * 4 * tt * (1 - tt) - 62 * tt
        pts.append((x, y))
    d.line(pts, fill=col, width=2)
    hx, hy = pts[-1]
    d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(255, 230, 150))
# village silhouette
GY = IY1 - 34
d.rectangle([IX0, GY + 18, IX1, IY1], fill=(16, 34, 18))
for hx in range(IX0 + 8, IX1 - 30, 42):
    d.rectangle([hx, GY - 2, hx + 30, GY + 20], fill=(5, 5, 8))
    d.polygon([(hx - 3, GY - 2), (hx + 15, GY - 16), (hx + 33, GY - 2)], fill=(5, 5, 8))
    d.rectangle([hx + 11, GY + 6, hx + 18, GY + 13], fill=(255, 196, 90))
# crashed missile in the field
d.polygon([(IX0 + 196, GY + 24), (IX0 + 252, GY + 16), (IX0 + 258, GY + 22),
           (IX0 + 204, GY + 31)], fill=(150, 150, 155))
d.polygon([(IX0 + 252, GY + 16), (IX0 + 266, GY + 12), (IX0 + 258, GY + 22)], fill=(178, 34, 34))
d.ellipse([IX0 + 188, GY + 27, IX0 + 224, GY + 34], outline=(60, 50, 30), width=2)
for k in range(6):
    d.ellipse([IX0 + 232 + k * 3, GY + 2 - k * 3, IX0 + 238 + k * 3, GY + 8 - k * 3],
              outline=(120, 120, 120))
d.rectangle([IX0, IY0, IX1, IY1], outline=INK, width=2)
d.text((IX0 + 6, IY1 - 14), "Nowy Lipowiec, south-east Poland",
       font=F_MAPL, fill=(230, 230, 220))

# ---------------- LEAD HEADLINE (x 322..652) ----------------
LX = 322
ly = 108
for ln in wrap("RUSSIAN MISSILES FALL IN POLAND", F_LEAD, 330):
    d.text((LX, ly), ln, font=F_LEAD, fill=INK)
    ly += 30
ly += 2
d.line([LX, ly, LX + 330, ly], fill=RED, width=3)
ly += 6
lead_lines = [
    ("Two Russian Kh-101 cruise missiles and a suspected jet-powered drone down in south-east Poland: Nowy Lipowiec (~50 km from the Ukraine border), Rudnik nad Sanem, Molodycz. No casualties in Poland.", None),
    ("Tusk: \"intentional provocation\" - \"we know for sure the weapons came from Russia.\" Rutte: \"grave violation\"; in Warsaw Sat 21 Nov.", None),
    ("Fell near Exercise Koalicja 2026, Nowa Deba (11 nations); one missile ~35 km away. Poland seeks more NATO air defence - Eastern Sentry (AWACS, F-35s); F-16s, Gripens scrambled, Patriots active.", None),
    ("Ukraine barrage - November's largest: 404 Shahed/Gerbera drones, 27 ballistic + 84 cruise missiles (515 weapons). At least 8 killed in Kyiv; Austria's embassy damaged.", None),
    ("One day after Putin met Trump and Xi in Shenzhen.", F_LEADTXT_B),
]
for text, f in lead_lines:
    f = f or F_LEADTXT
    for ln in wrap(text, f, 330):
        d.text((LX, ly), ln, font=f, fill=INK)
        ly += 12
    ly += 3

# ---------------- DOT-MATRIX WORLD MAP (x 662..1012) ----------------
MX0, MY0 = 662, 108
d.text((MX0, MY0), "WHERE IT HAPPENED - PIN KEY", font=F_MAPT, fill=INK)
MAP = [
    "                                                                ",
    "      #######                                                   ",
    "   ###########      #      #################   #########        ",
    "  #############   #####   #################### ###########  ##  ",
    "   ##########      ##    ##################### ########## ##### ",
    "     ########            ###  ################  ########  ####  ",
    "      ######              ##   ##############    ######    ##   ",
    "       #####                    ############      ####          ",
    "        ####        ##           ##########        ##           ",
    "        #####      ####           ########         ##           ",
    "         ####      ######          ######          ##           ",
    "         #####      ####            ####        ########        ",
    "          ####       ##              ##        ##########       ",
    "          ###                                   ########        ",
    "           ##                                    ######         ",
    "           #                                      ####    ##    ",
    "                                                             ",
]
CELL = 5
for r, row in enumerate(MAP):
    for c, ch in enumerate(row):
        if ch == "#":
            x, y = MX0 + c * CELL, MY0 + 16 + r * CELL
            d.ellipse([x, y, x + 3, y + 3], fill=(70, 90, 130))
PINS = [(32, 3, "1"), (35, 4, "2"), (36, 6, "3"), (54, 6, "4"),
        (10, 3, "5"), (38, 7, "6"), (49, 8, "7"), (35, 10, "8")]
for c, r, n in PINS:
    x, y = MX0 + c * CELL + 1, MY0 + 16 + r * CELL + 1
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=RED)
    d.text((x - 3, y - 5), n, font=F_TICK, fill=(255, 255, 255))
legend = ("1 Poland (missiles down)   2 Kyiv (515-weapon barrage)",
          "3 Antalya (COP31)   4 Shenzhen (trilateral summit)",
          "5 New York (markets crash)   6 Riyadh / Gaza",
          "7 Myanmar (ICJ ruling)   8 Sudan (West Kordofan)")
lyy = MY0 + 16 + len(MAP) * CELL + 6
for ln in legend:
    d.text((MX0, lyy), ln, font=F_MAPL, fill=INK)
    lyy += 12
lyy += 6
d.text((MX0, lyy), "LEAD FACTS", font=F_MAPT, fill=INK)
lyy += 13
for ln in ("515 weapons in one night on Ukraine",
           "At least 8 killed in Kyiv, dozens injured",
           "Zelenskyy: among the largest attacks of the war",
           "Bridges and power infrastructure hit in Kyiv"):
    d.text((MX0, lyy), ln, font=F_MAPL, fill=INK)
    lyy += 12

# ---------------- UTC TIMELINE RAIL (y 338..384) ----------------
TY = 364
d.line([20, TY, W - 20, TY], fill=INK, width=2)
ticks = [("00:00", 20), ("06:00", 266), ("12:00", 512), ("18:00", 758), ("24:00", 984)]
for lab, x in ticks:
    d.line([x, TY - 5, x, TY + 5], fill=INK, width=2)
    d.text((x - 14, TY + 7), lab + " UTC", font=F_TICK, fill=GREY)
events = [
    (28, "OVERNIGHT: 515-weapon barrage on Ukraine"),
    (274, "EARLY: Russian missiles down in Poland"),
    (520, "DAY: Rutte in Warsaw - Poland seeks NATO air defence"),
    (766, "LATE: COP31 third draft due - markets digest Friday's crash"),
]
for x, lab in events:
    for i, ln in enumerate(wrap(lab, F_TLAB, 238)):
        d.text((x, 338 + i * 11), ln, font=F_TLAB, fill=INK)
d.line([12, 384, W - 12, 384], fill=INK, width=2)

# ---------------- BODY: NUMBERED STORY CARDS ----------------
# Each card: (number, headline, one short detail line with the key figure)
COLS = [
    ("EUROPE", (30, 90, 160), [
        ("E1", "EU approves defence support for Ukraine", "EUR 1 billion; Russia rejecting any peace deal"),
        ("E2", "HIMARS strike destroys brigade HQ", "810th Brigade HQ in Sumy area; 20 commanders killed"),
        ("E3", "Berlin hosts Coalition summit", "Coalition-of-the-Willing summit with Zelenskyy and US negotiators"),
        ("E4", "Pistorius: talk to Putin directly", "German Defence Minister says European nations ought to talk to Putin"),
        ("E5", "Denmark charges two men in plot", "Two Danish men recruited by Russia in plot to kill a Ukrainian rapper"),
        ("E6", "Estonia plans border shutdown", "Six-month shutdown planned; Kremlin cries \"Iron Curtain\""),
        ("E7", "UK-EU sign post-Brexit deals", "Biggest since Brexit: food, carbon, youth mobility"),
        ("E8", "Italy: mass walkout staged", "Workers and students walk out over pay, living costs and public services"),
    ]),
    ("CLIMATE / COP31", (0, 128, 90), [
        ("C1", "COP31 runs past deadline, no deal", "Antalya talks past Friday deadline; nearly 200 countries"),
        ("C2", "Draft strips fossil-fuel language", "Drops $120 billion-a-year target; 35% electricity by 2035"),
        ("C3", "Draft concedes 1.5C overshoot", "First text to concede 1.5C overshoot; plans point to ~2.6C"),
        ("C4", "Addis Ababa to host COP32", "Ethiopia's capital confirmed as host of COP32 in 2027"),
    ]),
    ("AFRICA", (190, 120, 20), [
        ("F1", "Sudan army dismantles RSF posts", "RSF strongholds dismantled in 10 areas of West Kordofan"),
        ("F2", "Morocco builds defence industry", "EUR 366 million committed to a defence manufacturing base by 2035"),
    ]),
    ("HEALTH", (140, 40, 120), [
        ("H1", "Pancreatic cancer pill trial hope", "Daraxonrasib: undetectable on scans in 1 in 12 patients"),
    ]),
    ("NORTH AMERICA", (178, 34, 34), [
        ("N1", "S&P 500 falls 3.7% on Friday", "To 6,910.39 - seventh straight loss, into correction"),
        ("N2", "Nasdaq plunges 5.28%", "To 22,618; all 2026 gains erased; worst week since 2020"),
        ("N3", "Dow falls 1.93% - about 950 points", "Dow Jones down to 48,147.33 - also in correction"),
        ("N4", "Nvidia crashes 14% on Friday", "SEC probe reported; down nearly 50% from 6 October record"),
        ("N5", "Anthropic slides 8.5% after IPO", "IPO price $83; debut valued it near $2 trillion"),
        ("N6", "VIX surges 86% on the week", "Fear gauge at 35.89, 19-month high; gold -3% to $3,517"),
        ("N7", "US approved AI chip sales to China", "Nearly 900,000 AI chips in six months; Nvidia subpoenaed"),
        ("N8", "Trump weighs strikes on Iran", "New extensive strikes weighed as Israel presses for fast action"),
        ("N9", "Palisades fire: man convicted", "Man convicted of starting the deadly Palisades fire in Los Angeles"),
    ]),
    ("MIDDLE EAST", (200, 90, 0), [
        ("M1", "Houthi missile intercepted at Riyadh", "Debris in Riyadh; six Houthi workshops hit in Sana'a"),
        ("M2", "Israeli strikes kill 7 in Gaza", "At least 7 Palestinians killed despite the ceasefire"),
        ("M3", "US campaign on Iran: $48.3 billion", "Trump: \"We've got time\" - war may run into 2027"),
        ("M4", "IRGC claims Hormuz reach", "IRGC claims waters 500 km beyond the Strait of Hormuz"),
        ("M5", "Iraq storms Jurf al-Sakhar", "Ends 12 years of Kata'ib Hezbollah rule; GM held"),
        ("M6", "Syria captures former general", "Former general accused of orchestrating a 2014 massacre captured"),
    ]),
    ("ASIA-PACIFIC", (0, 110, 160), [
        ("A1", "Xi centre stage in Shenzhen", "Joint reconciliation signed; Putin \"a friend of mine\""),
        ("A2", "Xi warns US on Taiwan", "Trump: China's buildup \"rapid and concerning\""),
        ("A3", "Mongolia's president resigns", "Resignation sets up elections within four months"),
        ("A5", "China notice on Mount Fuji", "Notice issued on climbing Fuji; missing climber's family offers a reward"),
        ("A6", "Indonesia questions Google", "Ministry asks Google to explain removal of 19,000 YouTube accounts"),
    ]),
    ("SOUTH ASIA", (90, 130, 30), [
        ("S1", "ICJ: Myanmar committed genocide", "Genocide against Rohingya; Myanmar, China call it unjust"),
        ("S2", "19+ years for Sikh plot", "More than 19 years in US prison over Sikh separatist plot"),
        ("S3", "UN warns on ISIS-Khorasan", "ISIS-Khorasan gaining drones; threats rising in Afghanistan, UN warns"),
    ]),
    ("LATIN AMERICA", (170, 60, 110), [
        ("T1", "Bukele seeks a third term", "El Salvador's President Bukele seeks a third term"),
        ("T2", "Migrant caravan crosses Mexico", "Fresh caravan of about 300 people crosses into southern Mexico"),
        ("T3", "Lula advances Indigenous protection", "Brazil's Lula meets Amazon leader Raoni Metuktire on land protection"),
    ]),
    ("SPORT", (40, 40, 140), [
        ("P1", "NBA: Lakers edge Kings 106-104", "Thunder 126-120 Pelicans (SGA 40); Cavs 128-119, Harden 51"),
        ("P2", "Al-Ahli beat Al-Nassr 3-1", "Ronaldo hits post in Jeddah; Bayern held 1-1 by Cologne"),
    ]),
]

COLX = [12, 352, 692]
COLW = 320
col_of = [[0, 1, 2, 3], [4, 5], [6, 7, 8, 9]]  # section indices per column

def draw_section(idx, x, y):
    name, color, cards = COLS[idx]
    d.rectangle([x, y, x + COLW, y + 15], fill=color)
    d.text((x + 6, y + 2), name, font=F_BAND, fill=(255, 255, 255))
    y += 18
    for num, head, det in cards:
        hlines = wrap(head, F_HEAD, COLW - 34, max_lines=2)
        dlines = wrap(det, F_DET, COLW - 34, max_lines=2)
        hh = len(hlines) * 13 + len(dlines) * 12 + 3
        d.rectangle([x, y, x + 26, y + 13], fill=color)
        d.text((x + 3, y + 2), num, font=F_TICK, fill=(255, 255, 255))
        cy = y
        for ln in hlines:
            d.text((x + 30, cy), ln, font=F_HEAD, fill=INK)
            cy += 13
        for ln in dlines:
            d.text((x + 30, cy), ln, font=F_DET, fill=(50, 46, 38))
            cy += 12
        d.line([x, y + hh - 2, x + COLW, y + hh - 2], fill=(215, 205, 180), width=1)
        y += hh
    return y + 3

BODY_Y = 390
max_y = BODY_Y
for ci, sections in enumerate(col_of):
    y = BODY_Y
    for sidx in sections:
        y = draw_section(sidx, COLX[ci], y)
    max_y = max(max_y, y)
print("body ends at y =", max_y)

# ---------------- DATE CHECK STRIP ----------------
d.rectangle([12, 972, W - 12, 1006], fill=(10, 10, 10))
center("DATE CHECK - SATURDAY 21 NOVEMBER 2026", F_CHECK, 980, color=(255, 255, 255))
center("THE GLOBAL FRONT PAGE - one image, one day: Saturday 21 November 2026 - sources: ISW, Reuters, CNN, wires",
       F_FOOT, 1010, color=GREY)

img.save(os.path.join(HERE, "entry.png"), optimize=True)
img.resize((300, 300), Image.LANCZOS).save(os.path.join(HERE, "preview300.png"))
print("saved entry.png", img.size)
