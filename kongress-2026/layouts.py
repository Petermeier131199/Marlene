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
        B.gesperrt(dd, "Medium  |  Mentorin  |  Autorin", f, 0, 0, 7,
                   B.GOLD_HELL + (int(255 * p_rolle),))
        lay.alpha_composite(txt, (x0 + 4, basis + 236))
    return lay


def _hintergrund_karte(mitte=0.5):
    """Warmer dunkler Grund fuer Titelkarten (Vollbild, nicht transparent).

    `mitte` ist die Bildhoehe, auf der das Licht sitzt. Es muss konzentrisch zu
    der Geometrie liegen, die darauf gezeichnet wird - sass das Licht tiefer als
    die Blume, lag deren obere Haelfte auf dunklerem Grund als die untere und
    das Auge las sie als nach oben verrutscht.
    """
    bg = Image.new("RGB", (B.W, B.H), (18, 15, 13))
    glow = B.verlauf_radial((B.W, B.H), (B.W * 0.5, B.H * mitte),
                            (B.W * 0.72, B.H * 0.78), (92, 54, 18), 210)
    bg = Image.alpha_composite(bg.convert("RGBA"), glow)
    warm = B.verlauf_radial((B.W, B.H), (B.W * 0.5, B.H * mitte),
                            (B.W * 0.34, B.H * 0.40), (150, 96, 30), 120)
    bg = Image.alpha_composite(bg, warm)
    return bg


def _zeile(bg, text, f, track, farbe, y, hoehe=320):
    """Gesperrte Zeile mittig aufs Bild setzen."""
    w = B.breite(text, f, track)
    lay = Image.new("RGBA", (B.W + 900, hoehe), (0, 0, 0, 0))
    B.gesperrt(ImageDraw.Draw(lay), text, f, 0, 0, track, farbe)
    bg.alpha_composite(lay.crop((0, 0, int(w) + 10, hoehe)), (int(B.W / 2 - w / 2), int(y)))
    return w


def titel_opener(thema="Erkenne deinen Seelenplan", p_geo=1.0, p_logo=1.0,
                 p_thema=1.0, p_gast=1.0):
    """Vorspann. Das Thema traegt die Karte, der Kongress ist der Absender.

    Termin und Anmeldehinweis fehlen bewusst: wer das Video sieht, ist bereits
    beim Kongress angemeldet.
    """
    MITTE = 0.545                      # optischer Schwerpunkt des Textblocks
    bg = _hintergrund_karte(MITTE)

    if p_geo > 0:
        s = int(1560 * (0.96 + 0.04 * p_geo))
        geo = B.einfaerben(B.blume_des_lebens(s, width=3), B.GOLD, 0.20 * p_geo)
        bg.alpha_composite(geo, (int(B.W / 2 - s / 2), int(B.H * MITTE - s / 2)))

    # Kongress-Logo klein oben: Absender, nicht Botschaft. Ohne Claim-Zeile,
    # weil der Claim bereits gross als Thema auf der Karte steht.
    lg = B.ck_logo(mit_claim=False)
    zb = 860
    lg = lg.resize((zb, int(lg.height * zb / lg.width)), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * p_logo)))
    bg.alpha_composite(lg, (int(B.W / 2 - zb / 2), int(B.H * 0.115)))

    _zeile(bg, thema, B.runalto(176), 12, B.CREAM + (int(252 * p_thema),), B.H * 0.415)

    y = int(B.H * 0.575)
    lw = int(560 * B.ease_out(p_gast))
    if lw > 2:
        ImageDraw.Draw(bg).rectangle([B.W / 2 - lw / 2, y, B.W / 2 + lw / 2, y + 3],
                                     fill=B.GOLD + (200,))
    if p_gast > 0:
        wort = wortmarke_in(B.CREAM, WORTMARKE.height * 1020 / WORTMARKE.width)
        wort.putalpha(wort.getchannel("A").point(lambda v: int(v * p_gast)))
        bg.alpha_composite(wort, (int(B.W / 2 - wort.width / 2), y + 74))
        _zeile(bg, "MEDIUM  |  MENTORIN  |  AUTORIN", B.grotesk(56, "Medium"), 11,
               (246, 228, 168) + (int(240 * p_gast),), y + 74 + wort.height + 46, 140)
    return bg.convert("RGB")


def nachklang(satz="Erkenne deinen Seelenplan.", p=1.0):
    """Schlusskarte eins: ein ruhiger Satz, der wirken darf."""
    MITTE = 0.50
    bg = _hintergrund_karte(MITTE)
    s = 1560
    geo = B.einfaerben(B.blume_des_lebens(s, width=3), B.GOLD, 0.18 * p)
    bg.alpha_composite(geo, (int(B.W / 2 - s / 2), int(B.H * MITTE - s / 2)))

    _zeile(bg, satz, B.runalto(168), 12, B.CREAM + (int(252 * p),), B.H * 0.425)

    y = int(B.H * 0.575)
    lw = int(440 * B.ease_out(p))
    if lw > 2:
        ImageDraw.Draw(bg).rectangle([B.W / 2 - lw / 2, y, B.W / 2 + lw / 2, y + 3],
                                     fill=B.GOLD + (190,))
    wort = wortmarke_in(B.CREAM, WORTMARKE.height * 840 / WORTMARKE.width)
    wort.putalpha(wort.getchannel("A").point(lambda v: int(v * p)))
    bg.alpha_composite(wort, (int(B.W / 2 - wort.width / 2), y + 70))
    return bg.convert("RGB")


def kontakt(eintraege=None, hinweis=True, p=1.0):
    """Schlusskarte zwei: wo man sie findet, plus ein leiser Hinweis.

    Der Workshop steht bewusst unterhalb einer Trennlinie und in kleinerer
    Schrift: Er wird im Video erwaehnt, soll aber nicht wie eine Werbeflaeche
    wirken - deshalb abgesetzt statt als vierte gleichwertige Zeile.
    """
    eintraege = eintraege or [
        "vanessa-spaleck.de",
        "@medium_vanessa_spaleck",
        "Buch »Ganz normal medial«",
    ]
    MITTE = 0.50
    bg = _hintergrund_karte(MITTE)
    s = 1520
    geo = B.einfaerben(B.blume_des_lebens(s, width=3), B.GOLD, 0.15 * p)
    bg.alpha_composite(geo, (int(B.W / 2 - s / 2), int(B.H * MITTE - s / 2)))

    fae = FAECHER.resize((int(FAECHER.width * 190 / FAECHER.height), 190), Image.LANCZOS)
    fae.putalpha(fae.getchannel("A").point(lambda v: int(v * p)))
    bg.alpha_composite(fae, (int(B.W / 2 - fae.width / 2), 300))

    wort = wortmarke_in(B.CREAM, WORTMARKE.height * 960 / WORTMARKE.width)
    wort.putalpha(wort.getchannel("A").point(lambda v: int(v * p)))
    bg.alpha_composite(wort, (int(B.W / 2 - wort.width / 2), 560))

    _zeile(bg, "WO DU MICH FINDEST", B.grotesk(52, "Medium"), 19,
           B.GOLD + (int(235 * p),), 730, 140)

    for i, e in enumerate(eintraege):
        _zeile(bg, e, B.grotesk(74, "Light"), 4, (243, 234, 218) + (int(248 * p),),
               880 + i * 140, 220)

    if hinweis:
        y = 1410
        lw = int(300 * B.ease_out(p))
        if lw > 2:
            ImageDraw.Draw(bg).rectangle([B.W / 2 - lw / 2, y, B.W / 2 + lw / 2, y + 2],
                                         fill=B.GOLD + (150,))
        _zeile(bg, "ONLINE-VIDEO-WORKSHOP", B.grotesk(44, "Medium"), 16,
               B.GOLD + (int(210 * p),), 1480, 120)
        # bewusst kleiner als die Kontaktzeilen darueber: der Hinweis soll
        # nachgeordnet wirken, nicht die Karte anfuehren
        _zeile(bg, "Geistführer & Geistiges Haus", B.runalto(82), 5,
               (238, 230, 214) + (int(232 * p),), 1585, 200)
        _zeile(bg, "vanessa-spaleck.de/geistfuehrer-und-geistiges-haus",
               B.grotesk(44, "Light"), 3, (214, 204, 188) + (int(190 * p),), 1735, 140)
    return bg.convert("RGB")
