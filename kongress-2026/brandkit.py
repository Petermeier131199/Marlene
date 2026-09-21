"""Designsystem fuer die Channeling-Kongress-Einblendungen (4K, 3840x2160)."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 3840, 2160
HERE = os.path.dirname(os.path.abspath(__file__))

# --- Farben: ihr Gold, sein Orange, warmes Schwarz -------------------------
# Ihr Gelb - im Logo abgetastet (#e0b020), im Stylesheet ihrer Website als
# #e7b428 hinterlegt. Der Abstand zwischen beiden betraegt 2,6 Prozent des
# Farbraums und ist auf einem Bildschirm nicht unterscheidbar; es ist dieselbe
# Farbe. Auf dunklem Grund wirkt sie wie Gold, auf hellem eindeutig wie Gelb -
# daher die alten Namen, die bleiben als Alias bestehen.
GELB_HELL = (232, 192, 80)
GELB      = (224, 176, 32)
GELB_WEB  = (231, 180, 40)
GOLD_HELL = GELB_HELL
GOLD      = GELB
ORANGE    = (196,  99,  18)     # Akzent des Kongress-Logos
ORANGE_HL = (217, 122,  30)
CREAM     = (247, 241, 230)
WEISS     = (255, 255, 255)
DUNKEL    = (20, 17, 15)

SAFE_X, SAFE_Y = 240, 160        # Sicherheitsrand


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, name), size)


def runalto(size):
    return font("Runalto.ttf", size)


def script(size):
    return font("AdornStoryScript.ttf", size)


def grotesk(size, schnitt="Medium"):
    """Kraeftige Groteske fuer kleine Zeilen.

    Runalto ist eine Display-Schrift mit sehr feinen Haarstrichen - unter etwa
    40 Pixeln Zeilenhoehe brechen die weg. Diese Groteske liegt ausserdem naeher
    an ihrer Logo-Wortmarke als Runalto selbst.
    """
    f = font("Montserrat.ttf", size)
    f.set_variation_by_name(schnitt)
    return f


# --- Bausteine -------------------------------------------------------------
def gesperrt(draw, text, f, x, y, track, fill):
    """Text mit fester Sperrung zeichnen; gibt die Gesamtbreite zurueck."""
    start = x
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + track
    return x - track - start


def breite(text, f, track):
    return sum(f.getlength(c) for c in text) + track * (len(text) - 1)


def saat_des_lebens(size, width=3):
    """Saat des Lebens: 7 Kreise (Mitte + 6) im Abstand r, plus Aussenring.

    Wie beim Kongress-Symbol; Mittelpunktsabstand = Radius, dadurch die Blueten.
    """
    ss = 3
    img = Image.new("L", (int(size * ss), int(size * ss)), 0)
    d = ImageDraw.Draw(img)
    c = size * ss / 2.0
    r = size * ss / 6.0
    lw = max(1, int(width * ss))
    pts = [(0.0, 0.0)] + [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
                          for a in range(0, 360, 60)]
    for x, y in pts:
        d.ellipse([c + x - r, c + y - r, c + x + r, c + y + r], outline=255, width=lw)
    for rr in (2.0 * r, 2.12 * r):
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=255, width=lw)
    return img.resize((int(size), int(size)), Image.LANCZOS)


def blume_des_lebens(size, width=3):
    """19 Kreise im Sechseckraster, Mittelpunktsabstand r, zwei Aussenringe."""
    ss = 3
    img = Image.new("L", (int(size * ss), int(size * ss)), 0)
    d = ImageDraw.Draw(img)
    c = size * ss / 2.0
    r = size * ss / 6.35
    lw = max(1, int(width * ss))
    for q in range(-4, 5):
        for p in range(-4, 5):
            x, y = r * (q + p * 0.5), r * (math.sqrt(3) / 2.0) * p
            if math.hypot(x, y) <= 2 * r + 1e-6:
                d.ellipse([c + x - r, c + y - r, c + x + r, c + y + r], outline=255, width=lw)
    for rr in (3.0 * r, 3.15 * r):
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=255, width=lw)
    return img.resize((int(size), int(size)), Image.LANCZOS)


def einfaerben(maske, farbe, alpha=1.0):
    """L-Maske zu RGBA einfaerben."""
    img = Image.new("RGBA", maske.size, farbe + (0,))
    a = maske if alpha >= 1.0 else maske.point(lambda v: int(v * alpha))
    img.putalpha(a)
    return img


def schein(rgba, radius, staerke=1.0):
    """Weichen Lichtschein unter ein Element legen."""
    g = rgba.filter(ImageFilter.GaussianBlur(radius))
    if staerke != 1.0:
        g.putalpha(g.getchannel("A").point(lambda v: min(255, int(v * staerke))))
    return g


def _asset(name):
    return Image.open(os.path.join(HERE, name)).convert("RGBA")


def vs_logo():
    return _asset("vs-logo.png")


def ck_logo(mit_claim=True):
    """Kongress-Logo. Ohne Claim, wenn der Claim schon als Thema auf der Karte steht.

    Die Originaldatei ist eine Sperrschrift-Sperre aus Wortmarke und Claim; die
    Leerzeile dazwischen liegt bei y = 296 bis 308. Geschnitten wird mittig in
    dieser Luecke, ergibt also die uebliche Variante ohne Zusatzzeile.
    """
    lg = _asset("ck26-logo.png")
    if mit_claim:
        return lg
    oben = lg.crop((0, 0, lg.width, 302))
    return oben.crop(oben.getchannel("A").getbbox())


def lotus_faecher():
    """Nur den goldenen Faecher aus ihrem Logo (ohne Wortmarke)."""
    lg = vs_logo()
    oben = lg.crop((0, 0, lg.width, 300))
    return oben.crop(oben.getchannel("A").getbbox())


def verlauf_radial(size, mitte, radius, farbe, max_alpha=255, schwelle=0):
    """Weicher radialer Verlauf als RGBA (fuer Lesbarkeit hinter Text)."""
    w, h = size
    klein = (max(2, w // 12), max(2, h // 12))
    m = Image.new("L", klein, 0)
    d = ImageDraw.Draw(m)
    cx, cy = mitte[0] / 12, mitte[1] / 12
    rx, ry = radius[0] / 12, radius[1] / 12
    schritte = 26
    for i in range(schritte, 0, -1):
        t = i / schritte
        v = int(max_alpha * (1 - t) ** 1.7)
        d.ellipse([cx - rx * t, cy - ry * t, cx + rx * t, cy + ry * t], fill=v)
    m = m.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(klein[0] // 3))
    if schwelle:
        # Restwerte auf glatte Null ziehen: sonst streut der Verlauf minimale
        # Alphawerte ueber die ganze Flaeche und die PNG-Kompression bricht ein
        m = m.point(lambda v: 0 if v < schwelle else v)
    img = Image.new("RGBA", size, farbe + (0,))
    img.putalpha(m)
    return img


def ease_out(t):
    return 1 - (1 - max(0.0, min(1.0, t))) ** 3


def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def fenster(t, start, ein, halt, aus):
    """Hoch-/Runterblenden: 0 vor start, 1 waehrend halt, 0 danach."""
    if t < start:
        return 0.0
    if t < start + ein:
        return ease_out((t - start) / ein)
    if t < start + ein + halt:
        return 1.0
    if t < start + ein + halt + aus:
        return 1.0 - ease_in_out((t - start - ein - halt) / aus)
    return 0.0
