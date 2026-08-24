"""Titel-Layer fuer das Innerself-Detox-Intro: Glyphen, Goldlinien, Blume des Lebens."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONTDIR = "fonts"   # Cormorant Garamond + Montserrat (Google Fonts, variabel)

CREAM = (245, 237, 224)
GOLD = (201, 164, 92)
GOLD_TEXT = (236, 205, 148)   # Subline etwas heller, damit sie ueber dem Fenster traegt

TITLE = "INNERSELF DETOX"
SUB = "ZURÜCK ZU DIR SELBST"

TITLE_SIZE = 150
TITLE_TRACK = 6          # Grundsperrung in px
SUB_SIZE = 27
SUB_TRACK = 15

TITLE_CY = 0.505 * H     # optische Mitte der Versalien
RULE_TOP_Y = 0.415 * H
RULE_BOT_Y = 0.598 * H
SUB_CY = 0.641 * H
RULE_HALFW = 0.366 * W


def _font(name, variation, size):
    f = ImageFont.truetype(f"{FONTDIR}/{name}", size)
    f.set_variation_by_name(variation)
    return f


def title_font():
    return _font("CormorantGaramond.ttf", "Regular", TITLE_SIZE)


def sub_font():
    return _font("Montserrat.ttf", "Light", SUB_SIZE)


def layout(text, font, track, cx, cy):
    """Gibt je Zeichen (glyph-image, x, y, mitte-x) zurueck, zentriert auf cx/cy."""
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    # Versalhoehe fuer optische Zentrierung
    asc = font.getbbox("H")
    cap_h = asc[3] - asc[1]
    pen = cx - total / 2.0
    out = []
    for ch, w in zip(text, widths):
        if ch != " ":
            pad = int(TITLE_SIZE * 0.6)
            box = font.getbbox(ch)
            gw, gh = int(box[2] - box[0]) + 2 * pad, int(box[3] - box[1]) + 2 * pad
            g = Image.new("L", (max(gw, 1), max(gh, 1)), 0)
            ImageDraw.Draw(g).text((pad - box[0], pad - box[1]), ch, font=font, fill=255)
            gx = pen + box[0] - pad
            gy = cy - cap_h / 2.0 + (box[1] - asc[1]) - pad
            out.append({"img": g, "x": gx, "y": gy, "cx": pen + w / 2.0})
        pen += w + track
    return out, total


def flower_of_life(size, r, width=2):
    """Blume des Lebens als weiche Linienzeichnung (L-Maske), 19 Kreise + Rahmen."""
    ss = 3  # Supersampling fuer saubere Kanten
    img = Image.new("L", (size * ss, size * ss), 0)
    d = ImageDraw.Draw(img)
    c = size * ss / 2.0
    R = r * ss
    lw = max(1, int(width * ss))
    pts = []
    for q in range(-3, 4):
        for s in range(-3, 4):
            x = R * 1.5 * q
            y = R * math.sqrt(3) * (s + q / 2.0)
            if math.hypot(x, y) <= 2 * R + 1:
                pts.append((x, y))
    for x, y in pts:
        d.ellipse([c + x - R, c + y - R, c + x + R, c + y + R], outline=255, width=lw)
    for rr in (2.62 * R, 2.78 * R):
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=255, width=lw)
    img = img.resize((size, size), Image.LANCZOS)
    # weiche Vignette, damit die Linien nach aussen ausfransen
    return img
