"""Layouts: Bauchbinde, Titel-Opener, Kapitelkarte. Alles auf 3840x2160."""
from PIL import Image, ImageDraw, ImageFilter
import brandkit as B


def _teile_logo():
    """Faecher und Wortmarke trennen - ueber die Farbe, nicht ueber den Beschnitt.

    Im Original ueberlappen die unteren Bluetenblaetter die Schrift. Ein
    horizontaler Schnitt zieht deshalb Faecherreste in die Wortmarke. Der
    Faecher ist gold, die Wortmarke schwarz - das trennt sauber.
    """
    lg = B.vs_logo()
    px = lg.load()
    gold = Image.new("RGBA", lg.size, (0, 0, 0, 0))
    wort = Image.new("L", lg.size, 0)
    gp, wp = gold.load(), wort.load()
    for y in range(lg.height):
        for x in range(lg.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            if r > 120 and r > b + 40:          # goldener Faecher
                gp[x, y] = (r, g, b, a)
            elif r < 120 and g < 120 and b < 120:  # schwarze Wortmarke
                wp[x, y] = a
    bb = gold.getchannel("A").getbbox()
    # die untersten Bluetenblaetter lagen im Original hinter der Schrift und
    # haengen sonst als loser Rest unter dem Faecher
    faecher = gold.crop((bb[0], bb[1], bb[2], bb[1] + int((bb[3] - bb[1]) * 0.74)))
    wm = wort.crop(wort.getbbox())
    return faecher, wm


def wortmarke_in(farbe, hoehe):
    """Ihre Wortmarke in einer beliebigen Farbe, auf Hoehe skaliert."""
    m = WORTMARKE.resize((int(WORTMARKE.width * hoehe / WORTMARKE.height), int(hoehe)),
                         Image.LANCZOS)
    img = Image.new("RGBA", m.size, farbe + (0,))
    img.putalpha(m)
    return img
FAECHER, WORTMARKE = _teile_logo()


def bauchbinde(p_linie=1.0, p_text=1.0, p_rolle=1.0, versatz=0):
    """Namenseinblendung unten links. p_* = Fortschritt 0..1 je Element."""
    lay = Image.new("RGBA", (B.W, B.H), (0, 0, 0, 0))

    x0, basis = B.SAFE_X, 1660
    wort_h = 138
    wort = wortmarke_in(B.CREAM, wort_h)
    fae_h = 205
    fae = FAECHER.resize((int(FAECHER.width * fae_h / FAECHER.height), fae_h), Image.LANCZOS)

    breite_ges = fae.width + 48 + wort.width
    # Lesbarkeitsverlauf
    lay.alpha_composite(B.verlauf_radial(
        (B.W, B.H), (x0 + breite_ges * 0.5, basis + 130), (breite_ges * 1.05, 470),
        (8, 6, 5), int(150 * p_text)))

    # Goldlinie, zieht sich von links auf
    lw = int(breite_ges * B.ease_out(p_linie))
    if lw > 2:
        d = ImageDraw.Draw(lay)
        y = basis + 208
        d.rectangle([x0, y, x0 + lw, y + 3], fill=B.GOLD + (215,))

    def mit_alpha(img, a):
        out = img.copy()
        out.putalpha(out.getchannel("A").point(lambda v: int(v * a)))
        return out

    dx = int(versatz * (1 - B.ease_out(p_text)))
    if p_text > 0:
        lay.alpha_composite(mit_alpha(fae, p_text), (x0 - dx, basis - 62))
        lay.alpha_composite(mit_alpha(wort, p_text), (x0 + fae.width + 48 - dx, basis + 30))

    if p_rolle > 0:
        f = B.runalto(62)
        txt = Image.new("RGBA", (B.W, 140), (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        B.gesperrt(dd, "Medium  |  Speakerin  |  Coach", f, 0, 0, 7,
                   B.GOLD_HELL + (int(255 * p_rolle),))
        lay.alpha_composite(txt, (x0 + 4, basis + 236))
    return lay


def _hintergrund_karte(vignette=1.0):
    """Warmer dunkler Grund fuer Titelkarten (Vollbild, nicht transparent)."""
    bg = Image.new("RGB", (B.W, B.H), (18, 15, 13))
    glow = B.verlauf_radial((B.W, B.H), (B.W * 0.5, B.H * 0.52),
                            (B.W * 0.72, B.H * 0.78), (92, 54, 18), 210)
    bg = Image.alpha_composite(bg.convert("RGBA"), glow)
    warm = B.verlauf_radial((B.W, B.H), (B.W * 0.5, B.H * 0.56),
                            (B.W * 0.34, B.H * 0.40), (150, 96, 30), 120)
    bg = Image.alpha_composite(bg, warm)
    return bg


def titel_opener(p_geo=1.0, p_logo=1.0, p_datum=1.0, p_gast=1.0):
    bg = _hintergrund_karte()

    # Blume des Lebens ganz dezent hinter allem
    if p_geo > 0:
        s = int(1500 * (0.96 + 0.04 * p_geo))
        m = B.blume_des_lebens(s, width=3)
        geo = B.einfaerben(m, B.GOLD, 0.20 * p_geo)
        bg.alpha_composite(geo, (int(B.W / 2 - s / 2), int(B.H * 0.50 - s / 2)))

    # Kongress-Logo (Originaldatei, nur verkleinert)
    lg = B.ck_logo()
    zb = 1680
    lg = lg.resize((zb, int(lg.height * zb / lg.width)), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * p_logo)))
    bg.alpha_composite(lg, (int(B.W / 2 - zb / 2), int(B.H * 0.30)))

    d = ImageDraw.Draw(bg)
    if p_datum > 0:
        f = B.runalto(72)
        t = "DAS ONLINE-EVENT  ·  01. – 11. NOVEMBER 2026"
        w = B.breite(t, f, 11)
        lay = Image.new("RGBA", (B.W, 160), (0, 0, 0, 0))
        B.gesperrt(ImageDraw.Draw(lay), t, f, 0, 0, 11, B.CREAM + (int(230 * p_datum),))
        bg.alpha_composite(lay.crop((0, 0, int(w) + 10, 160)), (int(B.W / 2 - w / 2), int(B.H * 0.585)))

    if p_gast > 0:
        y = int(B.H * 0.70)
        lw = int(620 * B.ease_out(p_gast))
        if lw > 2:
            d.rectangle([B.W / 2 - lw / 2, y, B.W / 2 + lw / 2, y + 3], fill=B.GOLD + (200,))
        wort = wortmarke_in(B.CREAM, WORTMARKE.height * 980 / WORTMARKE.width)
        wort.putalpha(wort.getchannel("A").point(lambda v: int(v * p_gast)))
        bg.alpha_composite(wort, (int(B.W / 2 - wort.width / 2), y + 70))
        f2 = B.runalto(58)
        t2 = "Medium  |  Speakerin  |  Coach"
        w2 = B.breite(t2, f2, 7)
        lay2 = Image.new("RGBA", (B.W, 130), (0, 0, 0, 0))
        B.gesperrt(ImageDraw.Draw(lay2), t2, f2, 0, 0, 7, B.GOLD_HELL + (int(235 * p_gast),))
        bg.alpha_composite(lay2.crop((0, 0, int(w2) + 10, 130)),
                           (int(B.W / 2 - w2 / 2), y + 70 + wort.height + 34))
    return bg.convert("RGB")


def kapitelkarte(titel, nummer=None, p=1.0, p_titel=None):
    """Kapitel-Zwischentitel. Symbol oben, Nummer, Titel, Goldlinie."""
    p_titel = p if p_titel is None else p_titel
    bg = _hintergrund_karte()

    s = 340
    m = B.saat_des_lebens(s, width=3)
    sym = B.einfaerben(m, B.ORANGE_HL, 0.85 * p)
    bg.alpha_composite(B.schein(sym, 26, 0.7), (int(B.W / 2 - s / 2), int(B.H * 0.30 - s / 2)))
    bg.alpha_composite(sym, (int(B.W / 2 - s / 2), int(B.H * 0.30 - s / 2)))

    if nummer:
        f = B.runalto(62)
        t = nummer.upper()
        w = B.breite(t, f, 18)
        lay = Image.new("RGBA", (B.W, 140), (0, 0, 0, 0))
        B.gesperrt(ImageDraw.Draw(lay), t, f, 0, 0, 18, B.GOLD + (int(235 * p),))
        bg.alpha_composite(lay.crop((0, 0, int(w) + 10, 140)),
                           (int(B.W / 2 - w / 2), int(B.H * 0.435)))

    f = B.runalto(152)
    w = B.breite(titel, f, 12)
    lay = Image.new("RGBA", (B.W + 600, 320), (0, 0, 0, 0))
    B.gesperrt(ImageDraw.Draw(lay), titel, f, 0, 0, 12, B.CREAM + (int(252 * p_titel),))
    bg.alpha_composite(lay.crop((0, 0, int(w) + 10, 320)),
                       (int(B.W / 2 - w / 2), int(B.H * 0.505)))

    y = int(B.H * 0.655)
    lw = int(440 * B.ease_out(p))
    if lw > 2:
        ImageDraw.Draw(bg).rectangle([B.W / 2 - lw / 2, y, B.W / 2 + lw / 2, y + 3],
                                     fill=B.GOLD + (200,))
    return bg.convert("RGB")
