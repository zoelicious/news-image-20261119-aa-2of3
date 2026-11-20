#!/usr/bin/env python3
"""Render entry.png for news-image-20261119, Aa 2/3 (zoelicious4843).

Concept "Anthropic Hero": classic cream front page, giant serif date,
3 scene hero panels (APEC / ICJ / Anthropic), COP31 featured banner,
10 scene cards, small flat world map, 21 one-line briefs, DATE CHECK box.
35 stories, all verified 19 November 2026. Deterministic: no randomness,
no timestamps, no network. Pillow only, build time.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14
CW = W - 2 * M
PAPER = (247, 241, 222)
INK = (20, 20, 20)
GREY = (90, 90, 85)
RED = (179, 39, 30)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
TEAL = (18, 72, 66)
SKY = (205, 222, 230)
SEA = (214, 230, 231)
LAND = (238, 228, 192)
CREAM_CARD = (252, 248, 236)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_DATE = font("DejaVuSerif-Bold.ttf", 54)
F_SUB = font("DejaVuSerif-Italic.ttf", 15)
F_NUM = font("DejaVuSerif-Bold.ttf", 24)
F_HERO_HEAD = font("DejaVuSerif-Bold.ttf", 16)
F_BANNER_HEAD = font("DejaVuSerif-Bold.ttf", 19)
F_CARD_HEAD = font("DejaVuSerif-Bold.ttf", 12)
F_SERIF_B = font("DejaVuSerif-Bold.ttf", 11)
F_KICK = font("DejaVuSans-Bold.ttf", 10)
F_KICK_S = font("DejaVuSans-Bold.ttf", 9)
F_DECK = font("DejaVuSans.ttf", 10)
F_DECK_S = font("DejaVuSans.ttf", 9)
F_BRIEF = font("DejaVuSans.ttf", 9)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 9)
F_FOOT = font("DejaVuSans.ttf", 9)
F_TAG = font("DejaVuSans-Bold.ttf", 7)
F_PIN = font("DejaVuSans-Bold.ttf", 9)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(d, x, y, text, fnt, fill, spacing=1.2):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += fnt.getlength(ch) + (spacing if ch != " " else 2.2)
    return cx - x


def tag_pill(d, x, y, text, fill=RED):
    w = int(F_TAG.getlength(text)) + 8
    d.rectangle([x, y, x + w, y + 11], outline=fill, width=1)
    d.text((x + 4, y + 1), text, font=F_TAG, fill=fill)
    return w


def num_circle(d, cx, cy, n, r=9):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    s = str(n)
    d.text((cx - F_PIN.getlength(s) / 2, cy - 6), s, font=F_PIN, fill=(255, 255, 255))


def flag_us(d, x, y, w=34, h=20):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(60, 59, 110))


def flag_cn(d, x, y, w=34, h=20):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    d.text((x + 3, y + 2), "*", font=font("DejaVuSans-Bold.ttf", 12), fill=(255, 222, 0))
    d.text((x + 15, y + 1), "*", font=font("DejaVuSans-Bold.ttf", 7), fill=(255, 222, 0))
    d.text((x + 19, y + 6), "*", font=font("DejaVuSans-Bold.ttf", 7), fill=(255, 222, 0))
    d.text((x + 15, y + 11), "*", font=font("DejaVuSans-Bold.ttf", 7), fill=(255, 222, 0))


def flag_ru(d, x, y, w=34, h=20):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x, y, x + w, y + h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def figure(d, cx, base_y, hair, suit, tie):
    # head + hair + shoulders, simple flat face
    d.ellipse([cx - 13, base_y - 52, cx + 13, base_y - 26], fill=(235, 192, 150), outline=INK, width=1)
    d.pieslice([cx - 13, base_y - 52, cx + 13, base_y - 32], 180, 360, fill=hair)
    d.ellipse([cx - 4, base_y - 44, cx - 1, base_y - 41], fill=INK)
    d.ellipse([cx + 1, base_y - 44, cx + 4, base_y - 41], fill=INK)
    d.arc([cx - 5, base_y - 38, cx + 5, base_y - 32], 0, 180, fill=INK, width=1)
    d.polygon([(cx - 22, base_y), (cx - 16, base_y - 28), (cx + 16, base_y - 28),
               (cx + 22, base_y)], fill=suit, outline=INK)
    d.polygon([(cx - 4, base_y - 27), (cx + 4, base_y - 27), (cx, base_y - 6)], fill=tie)


def scene_apec(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x, y, x + w, y + 16], fill=GOLD)
    d.text((x + 6, y + 3), "FIRST US-CHINA-RUSSIA SUMMIT", font=F_KICK_S, fill=INK)
    flag_us(d, x + 22, y + 24)
    flag_cn(d, x + w // 2 - 17, y + 24)
    flag_ru(d, x + w - 56, y + 24)
    figure(d, x + 39, y + h - 4, (210, 180, 60), (30, 30, 34), RED)
    figure(d, x + w // 2, y + h - 4, (20, 20, 20), (30, 30, 34), RED)
    figure(d, x + w - 39, y + h - 4, (225, 225, 225), (30, 30, 34), (40, 80, 160))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(240, 232, 210))
    for cx, name in ((x + 39, "TRUMP"), (x + w // 2, "XI"), (x + w - 39, "PUTIN")):
        tw = F_KICK_S.getlength(name)
        d.rectangle([cx - tw / 2 - 4, y + h - 13, cx + tw / 2 + 4, y + h - 2],
                    fill=(255, 255, 255), outline=INK, width=1)
        d.text((cx - tw / 2, y + h - 12), name, font=F_KICK_S, fill=INK)


def scene_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # court building
    bx, by, bw, bh = x + 18, y + 34, w - 110, h - 34
    d.rectangle([bx, by, bx + bw, by + bh], fill=(172, 102, 62), outline=INK, width=1)
    d.polygon([(bx - 6, by), (bx + bw // 2, by - 18), (bx + bw + 6, by)], fill=(140, 75, 45), outline=INK)
    for i in range(5):
        cx = bx + 12 + i * (bw - 24) // 4
        d.rectangle([cx - 4, by + 8, cx + 4, by + bh - 12], fill=(240, 232, 210), outline=INK, width=1)
    d.rectangle([bx + 8, by + bh - 12, bx + bw - 8, by + bh], fill=(120, 60, 35))
    # towers
    d.rectangle([x + 8, y + 18, x + 20, y + h], fill=(150, 85, 55), outline=INK, width=1)
    d.polygon([(x + 6, y + 18), (x + 14, y + 6), (x + 22, y + 18)], fill=(120, 60, 35), outline=INK)
    # scales
    sx = x + w - 48
    d.line([sx, y + 22, sx, y + 62], fill=GOLD, width=3)
    d.line([sx - 18, y + 28, sx + 18, y + 28], fill=GOLD, width=3)
    d.arc([sx - 18, y + 28, sx - 2, y + 48], 0, 180, fill=GOLD, width=2)
    d.arc([sx + 2, y + 28, sx + 18, y + 48], 0, 180, fill=GOLD, width=2)
    d.ellipse([sx - 4, y + 16, sx + 4, y + 24], fill=GOLD, outline=INK, width=1)
    # 9-6 badge
    d.rectangle([x + w - 62, y + 6, x + w - 8, y + 26], fill=RED)
    d.text((x + w - 52, y + 9), "9-6", font=font("DejaVuSans-Bold.ttf", 13), fill=(255, 255, 255))


def scene_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 46, 58))
    for gy in (y + 22, y + 44, y + 66):
        d.line([x + 8, gy, x + w - 8, gy], fill=(60, 100, 110), width=1)
    pts = [(x + 14, y + 74), (x + 60, y + 62), (x + 105, y + 66), (x + 150, y + 48),
           (x + 200, y + 50), (x + 250, y + 30), (x + w - 14, y + 16)]
    d.line(pts, fill=(120, 220, 130), width=3, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(120, 220, 130))
    d.polygon([(x + w - 26, y + 8), (x + w - 14, y + 24), (x + w - 14, y + 8)], fill=(120, 220, 130))
    d.rectangle([x + 10, y + 8, x + 62, y + 28], fill=(255, 255, 255))
    d.text((x + 15, y + 11), "ANT", font=font("DejaVuSans-Bold.ttf", 13), fill=(16, 46, 58))
    d.text((x + 70, y + 8), "NASDAQ", font=F_KICK_S, fill=(200, 220, 225))
    d.text((x + 10, y + 30), "$81.3bn", font=font("DejaVuSerif-Bold.ttf", 22), fill=(255, 255, 255))
    d.rectangle([x + w - 78, y + h - 22, x + w - 8, y + h - 8], fill=GOLD)
    d.text((x + w - 72, y + h - 19), "FIRST DAY", font=F_KICK_S, fill=INK)


def hero_panel(d, x, y, w, h, num, kicker, headline, deck, source, scene):
    d.rectangle([x, y, x + w, y + h], fill=CREAM_CARD, outline=INK, width=1)
    scene(d, x + 1, y + 1, w - 2, 88)
    ty = y + 94
    num_circle(d, x + 14, ty + 5, num, r=9)
    d.text((x + 28, ty), kicker, font=F_KICK, fill=RED)
    ty += 17
    for line in wrap(headline, F_HERO_HEAD, w - 16):
        d.text((x + 8, ty), line, font=F_HERO_HEAD, fill=INK)
        ty += 19
    ty += 2
    for line in wrap(deck, F_DECK, w - 16):
        d.text((x + 8, ty), line, font=F_DECK, fill=(40, 40, 40))
        ty += 12
    ty += 2
    d.text((x + 8, ty), source, font=F_DECK_S, fill=GREY)
    tag_pill(d, x + w - 62, ty - 1, "REPORTED")


def draw_masthead(d):
    draw_spaced(d, M, 6, "THE WORLD IN ONE DAY", F_KICK, INK)
    right = "35 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY"
    d.text((W - M - F_KICK.getlength(right), 6), right, font=F_KICK, fill=RED)
    d.text((M, 18), "Thursday 19 November 2026", font=F_DATE, fill=INK)
    d.line([M, 80, W - M, 80], fill=INK, width=3)
    d.line([M, 84, W - M, 84], fill=INK, width=1)
    d.text((M, 88), "Trump, Xi and Putin share one table \u00b7 The World Court finds genocide in Myanmar \u00b7 Anthropic\u2019s record IPO",
           font=F_SUB, fill=RED)


def draw_numbers(d):
    stats = [
        ("3", "presidents at one table"),
        ("9\u20136", "World Court genocide vote"),
        ("$81.3bn", "Anthropic\u2019s record IPO"),
        ("109\u20130", "Danish vote on Arctic pact"),
        ("4.9%", "Australian jobless rate"),
        ("$120bn", "aid goal cut at COP31"),
    ]
    cw = CW // 6
    y = 110
    d.line([M, y - 2, W - M, y - 2], fill=INK, width=1)
    for i, (num, label) in enumerate(stats):
        x = M + i * cw
        d.text((x + 4, y + 2), num, font=F_NUM, fill=RED if i in (0, 2, 4) else INK)
        for j, line in enumerate(wrap(label, F_DECK_S, cw - 10)):
            d.text((x + 4, y + 30 + j * 11), line, font=F_DECK_S, fill=(60, 60, 60))
    d.line([M, y + 52, W - M, y + 52], fill=INK, width=1)


def draw_regions(d):
    regions = [
        ("ASIA", 8, (179, 39, 30)), ("MIDDLE EAST", 3, (176, 106, 26)),
        ("EUROPE", 9, (22, 35, 63)), ("AFRICA", 5, (46, 110, 60)),
        ("AMERICAS", 4, (96, 60, 140)), ("OCEANIA", 4, (18, 110, 110)),
        ("GLOBAL", 2, (100, 100, 100)),
    ]
    y = 168
    x = M
    for name, count, color in regions:
        d.rectangle([x, y, x + 12, y + 12], fill=color)
        label = f"{name} {count}"
        d.text((x + 15, y + 1), label, font=F_KICK_S, fill=INK)
        x += 15 + F_KICK_S.getlength(label) + 26


# ---------- COP31 featured banner ----------
def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    # globe
    d.ellipse([x + 12, y + 8, x + 66, y + 62], fill=(70, 140, 190), outline=(255, 255, 255), width=2)
    d.ellipse([x + 24, y + 18, x + 44, y + 34], fill=(90, 170, 90))
    d.ellipse([x + 40, y + 40, x + 58, y + 54], fill=(90, 170, 90))
    # thermometer
    d.rectangle([x + 76, y + 10, x + 86, y + 46], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x + 78, y + 26, x + 84, y + 44], fill=RED)
    d.ellipse([x + 72, y + 42, x + 90, y + 60], fill=RED, outline=INK, width=1)
    # document with FOSSIL FUELS crossed out
    d.rectangle([x + 100, y + 8, x + w - 8, y + 62], fill=(255, 255, 255), outline=INK, width=1)
    d.text((x + 108, y + 12), "DRAFT DEAL \u00b7 19 NOV", font=F_KICK_S, fill=INK)
    d.text((x + 108, y + 26), "FOSSIL FUELS", font=font("DejaVuSans-Bold.ttf", 13), fill=INK)
    d.line([x + 106, y + 33, x + 196, y + 33], fill=RED, width=3)
    d.text((x + 108, y + 42), "$120BN ADAPTATION AID", font=font("DejaVuSans-Bold.ttf", 11), fill=RED)


def draw_cop31(d, y):
    h = 84
    d.rectangle([M, y, W - M, y + h], fill=CREAM_CARD, outline=INK, width=1)
    scene_cop31(d, M + 1, y + 1, 300, h - 2)
    tx = M + 316
    num_circle(d, tx + 8, y + 14, 4, r=9)
    d.text((tx + 22, y + 9), "ANTALYA \u00b7 CLIMATE", font=F_KICK, fill=RED)
    d.text((tx + 8, y + 28), "COP31 draft drops fossil fuels and $120bn aid goal",
           font=F_BANNER_HEAD, fill=INK)
    d.text((tx + 8, y + 52), "The slimmer text has no figure for adaptation aid. Talks are due to end on Friday.",
           font=F_DECK, fill=(40, 40, 40))
    d.text((tx + 8, y + 68), "\u2014 Reuters \u00b7 AFP", font=F_DECK_S, fill=GREY)
    tag_pill(d, W - M - 66, y + 66, "REPORTED")
    return y + h


# ---------- secondary grid scenes ----------
def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 210, 225))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 130, 170))
    d.arc([x + w // 2 - 40, y + 6, x + w // 2 + 40, y + h], 0, 180, fill=INK, width=3)
    d.line([x + 6, y + h - 18, x + w - 6, y + h - 18], fill=INK, width=3)
    for dx, dy in ((w - 34, 8), (w - 26, 14), (w - 40, 16)):
        d.polygon([(x + dx, y + dy - 8), (x + dx + 5, y + dy), (x + dx - 5, y + dy)], fill=(255, 140, 0))
    d.ellipse([x + w - 36, y + 4, x + w - 18, y + 20], fill=(255, 200, 60))


def scene_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 40, 70))
    for i, bh in enumerate((26, 34, 20, 30, 24)):
        bx = x + 8 + i * 30
        d.rectangle([bx, y + h - bh, bx + 22, y + h], fill=(70, 80, 110), outline=(150, 160, 190), width=1)
    d.line([x + 20, y + h - 10, x + w - 30, y + 10], fill=(255, 200, 60), width=2)
    d.line([x + 40, y + h - 6, x + w - 50, y + 16], fill=(255, 120, 40), width=2)
    d.ellipse([x + w - 44, y + 4, x + w - 28, y + 18], fill=(255, 220, 90))
    for dx, dy in ((w - 38, 12), (w - 30, 18)):
        d.polygon([(x + dx, y + dy - 5), (x + dx + 4, y + dy + 3), (x + dx - 4, y + dy + 3)], fill=(255, 140, 0))


def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 225, 235))
    cx, cy = x + w // 2 - 10, y + h // 2
    for r in (8, 15, 22):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(22, 35, 63), width=3)
    d.line([cx + 24, cy - 8, cx + 44, cy - 18], fill=RED, width=3)
    d.polygon([(cx + 44, cy - 18), (cx + 34, cy - 18), (cx + 42, cy - 8)], fill=RED)
    d.text((x + w - 52, y + 4), "ODISHA", font=F_KICK_S, fill=RED)


def scene_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 200))
    d.rectangle([x + 26, y + 30, x + 78, y + 38], fill=(120, 70, 30), outline=INK, width=1)
    d.rectangle([x + 82, y + 8, x + 106, y + 30], fill=(150, 95, 40), outline=INK, width=1)
    d.line([x + 82, y + 10, x + 106, y + 28], fill=INK, width=1)
    d.rectangle([x + w - 92, y + 6, x + w - 8, y + 22], outline=RED, width=2)
    d.text((x + w - 88, y + 9), "OVERTURNED", font=F_KICK_S, fill=RED)


def scene_greenland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 215, 230))
    d.polygon([(x, y + h), (x + 45, y + 8), (x + 90, y + h)], fill=(255, 255, 255), outline=INK)
    d.polygon([(x + 60, y + h), (x + 110, y + 2), (x + 160, y + h)], fill=(230, 235, 240), outline=INK)
    d.rectangle([x + 8, y + 6, x + 30, y + 18], fill=RED)
    d.text((x + 10, y + 8), "DK", font=F_KICK_S, fill=(255, 255, 255))
    d.rectangle([x + 34, y + 6, x + 56, y + 18], fill=(60, 59, 110))
    d.text((x + 36, y + 8), "US", font=F_KICK_S, fill=(255, 255, 255))
    d.rectangle([x + w - 52, y + 4, x + w - 6, y + 20], fill=RED)
    d.text((x + w - 48, y + 7), "109-0", font=F_KICK_S, fill=(255, 255, 255))


def scene_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 30, 110))
    d.ellipse([x + 30, y + 10, x + 90, y + 36], fill=(40, 40, 40), outline=(255, 255, 255), width=2)
    d.ellipse([x + w - 90, y + 10, x + w - 30, y + 36], fill=(40, 40, 40), outline=(255, 255, 255), width=2)
    d.rectangle([x + 60, y + 14, x + w - 60, y + 30], fill=(40, 40, 40), outline=(255, 255, 255), width=2)
    d.text((x + w // 2 - 14, y + 8), "VI", font=font("DejaVuSerif-Bold.ttf", 22), fill=GOLD)


def scene_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 200))
    for i, cx in enumerate(range(20, w - 10, 26)):
        d.ellipse([x + cx, y + 12, x + cx + 14, y + 26], fill=(235, 192, 150), outline=INK, width=1)
        d.rectangle([x + cx - 2, y + 28, x + cx + 16, y + h - 4], fill=(150, 60, 50) if i % 3 == 0 else (60, 90, 140))
    d.rectangle([x + w - 70, y + 2, x + w - 4, y + 14], fill=(255, 205, 0))
    d.rectangle([x + w - 70, y + 14, x + w - 4, y + 20], fill=(0, 56, 147))
    d.rectangle([x + w - 70, y + 20, x + w - 4, y + 26], fill=(206, 17, 38))


def scene_runner(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 220))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(200, 60, 40))
    d.ellipse([x + 40, y + 8, x + 54, y + 22], fill=(120, 70, 40), outline=INK, width=1)
    d.line([x + 47, y + 22, x + 47, y + 34], fill=INK, width=3)
    d.line([x + 47, y + 26, x + 62, y + 18], fill=INK, width=2)
    d.line([x + 47, y + 34, x + 62, y + h - 12], fill=INK, width=3)
    d.line([x + 47, y + 34, x + 32, y + h - 12], fill=INK, width=3)
    d.rectangle([x + w - 66, y + 6, x + w - 6, y + 22], fill=RED)
    d.text((x + w - 62, y + 9), "BANNED", font=F_KICK_S, fill=(255, 255, 255))


def scene_jobs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + 6), "4.9%", font=font("DejaVuSerif-Bold.ttf", 24), fill=(255, 255, 255))
    d.line([x + 110, y + 10, x + 150, y + 30], fill=(255, 90, 70), width=3)
    d.polygon([(x + 150, y + 30), (x + 138, y + 28), (x + 148, y + 40)], fill=(255, 90, 70))
    for i, cx in enumerate((x + w - 60, x + w - 42, x + w - 24)):
        d.ellipse([cx, y + h - 24, cx + 12, y + h - 12], fill=(235, 192, 150), outline=(255, 255, 255), width=1)
        d.rectangle([cx - 2, y + h - 12, cx + 14, y + h - 2], fill=(150, 60, 50) if i % 2 else (60, 90, 140))


def scene_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 230))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(90, 130, 170))
    d.polygon([(x + 20, y + h - 12), (x + 30, y + 16), (x + 150, y + 16), (x + 160, y + h - 12)], fill=(120, 40, 30), outline=INK, width=1)
    d.rectangle([x + 120, y + 4, x + 140, y + 16], fill=(200, 200, 200), outline=INK, width=1)
    for fx in (60, 90, 120):
        d.polygon([(x + fx, y + 16), (x + fx + 7, y + 2), (x + fx + 14, y + 16)], fill=(255, 140, 0))
    d.text((x + 8, y + 4), "CLAIM", font=F_KICK_S, fill=RED)


CARDS = [
    (5, "KERCH BRIDGE \u00b7 WAR", "Ukraine hits Crimea bridge again",
     "Third strike in a week halts trains to Russia.", "Euronews", "REPORTED", scene_bridge),
    (6, "OVER RIYADH \u00b7 WAR", "Saudis shoot down Houthi missiles",
     "Debris fell on the capital; no casualties reported.", "Reuters", "REPORTED", scene_riyadh),
    (7, "CYCLONE AKVAN \u00b7 STORM", "Cyclone Akvan nears India\u2019s coast",
     "Over 100,000 in shelters before Friday\u2019s landfall.", "IMD", "REPORTED", scene_cyclone),
    (8, "SEOUL \u00b7 JUSTICE", "Korea\u2019s top court clears ex-PM Han",
     "Han Duck-soo\u2019s martial law conviction is overturned.", "AP", "REPORTED", scene_gavel),
    (9, "GREENLAND \u00b7 SECURITY", "Denmark backs Arctic pact with US",
     "Parliament approves the Greenland security deal 109\u20130.", "AP", "REPORTED", scene_greenland),
    (10, "GTA VI \u00b7 GAMES", "GTA VI goes on sale after 13 years",
     "The midnight launch draws rave reviews.", "ABC", "REPORTED", scene_gta),
    (11, "PARO NACIONAL \u00b7 LABOUR", "Colombia\u2019s unions hold national strike",
     "Marches in three cities against an economic law.", "Infobae", "REPORTED", scene_strike),
    (12, "DOPING \u00b7 3 YEARS \u00b7 SPORT", "Marathon champion banned for doping",
     "Kenya\u2019s Peres Jepchirchir gets three years.", "ABC", "REPORTED", scene_runner),
    (13, "JOBLESS RATE \u00b7 ECONOMY", "Australia\u2019s jobless rate hits 4.9%",
     "Highest since 2024; shares and the dollar slide.", "ABC", "REPORTED", scene_jobs),
    (14, "HORMUZ \u00b7 CLAIM", "Iran says mines set 3 tankers ablaze",
     "Tehran\u2019s claim could not be independently verified.", "Al Jazeera", "CLAIM", scene_tanker),
]


def draw_card(d, x, y, w, h, num, kicker, headline, deck, source, tag, scene):
    d.rectangle([x, y, x + w, y + h], fill=CREAM_CARD, outline=INK, width=1)
    scene(d, x + 1, y + 1, w - 2, 46)
    ty = y + 50
    num_circle(d, x + 12, ty + 5, num, r=8)
    d.text((x + 23, ty), kicker, font=F_KICK_S, fill=RED)
    ty += 14
    for line in wrap(headline, F_CARD_HEAD, w - 12):
        d.text((x + 6, ty), line, font=F_CARD_HEAD, fill=INK)
        ty += 14
    for line in wrap(deck, F_DECK_S, w - 12):
        d.text((x + 6, ty), line, font=F_DECK_S, fill=(40, 40, 40))
        ty += 11
    d.text((x + 6, y + h - 13), "\u2014 " + source, font=F_DECK_S, fill=GREY)
    tag_pill(d, x + w - 58, y + h - 14, tag, RED if tag == "CLAIM" else (46, 110, 60))


# ---------- small flat world map ----------
EURASIA = [(-10, 36), (-9, 44), (-2, 49), (2, 51), (7, 54), (8, 58), (12, 56), (18, 56),
           (21, 55), (24, 59), (30, 60), (28, 65), (25, 70), (35, 68), (45, 68), (55, 70),
           (65, 72), (75, 73), (90, 75), (110, 76), (130, 72), (150, 70), (170, 67),
           (178, 65), (170, 60), (162, 58), (158, 52), (142, 50), (140, 40), (135, 35),
           (127, 35), (122, 30), (115, 23), (108, 20), (105, 10), (100, 8), (97, 15),
           (92, 20), (88, 22), (80, 15), (77, 8), (75, 20), (70, 22), (65, 25),
           (58, 25), (52, 27), (48, 30), (44, 29), (40, 35), (35, 36), (30, 36),
           (27, 37), (22, 37), (18, 40), (12, 42), (8, 44), (3, 43), (-2, 37), (-6, 36)]
N_AMERICA = [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 60),
             (-70, 45), (-80, 32), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
             (-125, 40), (-125, 49), (-145, 60)]
GREENLAND_P = [(-58, 64), (-45, 60), (-32, 68), (-25, 70), (-35, 76), (-55, 76)]
S_AMERICA = [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
             (-45, -20), (-55, -30), (-65, -40), (-70, -50), (-73, -40), (-75, -25),
             (-80, -15)]
AFRICA = [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
          (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35),
          (15, -25), (12, -10), (9, 0), (-8, 5)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (120, -34), (129, -32), (135, -35),
             (140, -38), (145, -38), (150, -37), (153, -27), (146, -19), (142, -11),
             (136, -12), (132, -11), (126, -14), (122, -17)]
# (num, lon, lat, dx, dy) — dx/dy nudge the pin so labels never overlap
PINS = [
    (1, 114, 22, 0, 0), (2, 4, 52, 0, 0), (3, -74, 41, 0, 0), (4, 30, 37, 0, 0),
    (5, 34, 45, 6, -4), (6, 47, 25, -6, -2), (7, 85, 20, 0, 0), (8, 127, 37, 0, 0),
    (9, -42, 72, 0, 0), (10, -80, 26, 0, 0), (11, -74, 5, 0, 0), (12, 37, -1, 0, 0),
    (13, 149, -35, 0, 0), (14, 56, 26, 6, 4),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (75 - lat) / 130 * h)

    for poly in (EURASIA, N_AMERICA, GREENLAND_P, S_AMERICA, AFRICA, AUSTRALIA):
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=(150, 135, 95))
    for lon, lat in ((10, 41), (139, 36), (147, -41), (174, -41), (100, 13), (103, 1)):
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=LAND, outline=(150, 135, 95))
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        num_circle(d, px + dx, py + dy, num, r=8)


BRIEFS = [
    (15, "Shenzhen", "Xi urges ban on all nuclear arms.", "Al Jazeera"),
    (16, "APEC", "Albanese to Putin: \u201cEnd your war, end it now.\u201d", "ABC"),
    (17, "Seoul", "Half a million sit college entrance exam.", "Sedaily"),
    (18, "Jakarta", "Asset-seizure law passes after 18 years.", "Kompas"),
    (19, "Gaza", "Israel ends tank raid past truce line.", "BBC"),
    (20, "Krasnodar", "Kyiv says it hit two oil refineries.", "Euronews"),
    (21, "Brussels", "EU delays methane rules two years.", "Euronews"),
    (22, "UK", "Inquiry: yacht Bayesian was vulnerable to wind.", "RNZ"),
    (23, "Zurich", "Two rivals to challenge FIFA\u2019s Infantino.", "ABC"),
    (24, "Rome", "Author Corrado Augias dies at 91.", "Euronews"),
    (25, "Mogadishu", "Somalia expels UAE ambassador.", "Al Jazeera"),
    (26, "Sudan", "Court sentences absent RSF chief to death.", "AP"),
    (27, "Pretoria", "Central bank holds rate at 7.25%.", "SABC"),
    (28, "Canaries", "Record 11,000 migrants in 15 days.", "Africanews"),
    (29, "Florida", "Floods shut Broward, Miami schools again.", "CBS"),
    (30, "Wellington", "Court: pay equity cuts broke rights law.", "RNZ"),
    (31, "Tonga", "Drought emergency takes effect.", "RNZ"),
    (32, "Cook Islands", "Cyclone Xavier weakens to category 4.", "RNZ"),
    (33, "Space", "Red giant seen eating a Sun-sized star.", "Nature"),
    (34, "Finland", "Approves first nuclear waste store.", "Euronews"),
    (35, "Germany", "Russian held for spying on Palantir.", "Euronews"),
]


def draw_bottom(d, y):
    h = 168
    # map (left)
    d.text((M, y), "WHERE IT HAPPENED", font=F_KICK, fill=INK)
    d.text((M + 150, y), "numbers match the stories", font=F_DECK_S, fill=GREY)
    draw_map(d, M, y + 16, 380, h - 16)
    # briefs (right)
    bx = M + 396
    d.text((bx, y), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=F_KICK, fill=INK)
    d.text((bx + 268, y), "place \u00b7 what happened \u00b7 source", font=F_DECK_S, fill=GREY)
    col_w = (W - M - bx - 8) // 2
    for i, (num, place, text, source) in enumerate(BRIEFS):
        col = 0 if i < 11 else 1
        row = i if i < 11 else i - 11
        x = bx + col * (col_w + 8)
        yy = y + 16 + row * 14
        d.text((x, yy), str(num), font=F_BRIEF_B, fill=RED)
        d.text((x + 18, yy), place, font=F_BRIEF_B, fill=INK)
        d.text((x + 18 + F_BRIEF_B.getlength(place) + 4, yy),
               text + " " + source, font=F_BRIEF, fill=(40, 40, 40))
    return y + h


def draw_datecheck(d, y):
    h = 62
    d.rectangle([M, y, W - M, y + h], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK \u2713  Every story on this page happened, or was first reported, on Thursday 19 November 2026.",
           font=F_BRIEF_B, fill=INK)
    left = ("LEFT OUT AS OTHER DAYS\u2019 NEWS:  18 NOV: EU\u2019s \u20ac45bn Ukraine loan plan \u00b7 Iran fires on Kuwait and Bahrain "
            "\u00b7 Nvidia results \u00b7 Jeffries named for US speaker \u00b7 Carney on China ties \u00b7 Van Gogh $190.4m "
            "\u00b7 Voyager 1 one light-day \u00b7 Pew 2035 \u00b7 Anthropic IPO pricing ($83) \u00b7 Gaza push began  |  "
            "20 NOV: COP31\u2019s scheduled close \u00b7 Cyclone Akvan\u2019s landfall")
    ty = y + 22
    for line in wrap(left, F_FOOT, CW - 16):
        d.text((M + 8, ty), line, font=F_FOOT, fill=(60, 60, 60))
        ty += 12
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_numbers(d)
    draw_regions(d)
    # hero: 3 panels
    hy = 190
    ph = 200
    pw = (CW - 18) // 3
    hero = [
        (1, "APEC 2026 \u00b7 SHENZHEN", "Trump, Xi and Putin hold first three-way summit",
         "The three leaders met for 90 minutes and issued a \u201cDeclaration on Peace\u201d on nuclear risk and UN reform.",
         "\u2014 Reuters \u00b7 AP \u00b7 Xinhua", scene_apec),
        (2, "WORLD COURT \u00b7 THE HAGUE", "World Court: Myanmar committed genocide",
         "By 9 votes to 6 the ICJ found Myanmar guilty of genocide against the Rohingya and ordered reparations.",
         "\u2014 Al Jazeera \u00b7 UN News", scene_icj),
        (3, "ANT \u00b7 NASDAQ", "Anthropic shares surge 17% on first day of trading",
         "The AI firm\u2019s shares jumped on their Nasdaq debut, closing the largest listing ever.",
         "\u2014 AP", scene_anthropic),
    ]
    for i, (num, kicker, head, deck, src, scene) in enumerate(hero):
        hero_panel(d, M + i * (pw + 9), hy, pw, ph, num, kicker, head, deck, src, scene)
    y = draw_cop31(d, hy + ph + 6)
    # secondary grid 2x5
    gy = y + 6
    gh = 132
    gw = (CW - 4 * 6) // 5
    for i, card in enumerate(CARDS):
        row, col = divmod(i, 5)
        draw_card(d, M + col * (gw + 6), gy + row * (gh + 6), gw, gh, *card)
    y = draw_bottom(d, gy + 2 * gh + 10)
    y = draw_datecheck(d, y + 4)
    fty = y + 4
    for line in wrap("Claims are attributed, not stated as fact \u00b7 Pictures and map: original, drawn in code \u00b7 Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature, Kompas, Infobae, IMD, SABC, CBS, Africanews \u00b7 2026-11-19",
                     F_FOOT, CW):
        d.text((M, fty), line, font=F_FOOT, fill=GREY)
        fty += 11
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
