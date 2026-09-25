"""Schild fuer die magnetische Tafel, in ihrer Print-Sprache.

Vorbild ist ihr Briefpapier: weisser Grund, feines Punktraster, das goldene
Mandala mit Wortmarke oben, die Spirit-Akademie-Marke unten, alles in Grau und
Gold. Gesetzt wird in Millimetern und mit 300 dpi ausgegeben, damit es
massstabsgetreu gedruckt werden kann.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

DPI = 300
BREITE_MM, HOEHE_MM = 190.0, 265.0          # etwas kleiner als A4
MM = DPI / 25.4
W, H = int(BREITE_MM * MM), int(HOEHE_MM * MM)

WEISS   = (255, 255, 255)
GRAU    = (109, 106, 104)                    # Schriftgrau des Briefpapiers
GRAU_H  = (150, 147, 144)
PUNKT   = (214, 209, 204)
GOLD    = (224, 176, 32)


def mm(v):
    return v * MM


def f(name, size_mm, schnitt=None):
    font = ImageFont.truetype(name, int(mm(size_mm)))
    if schnitt:
        font.set_variation_by_name(schnitt)
    return font


def gesperrt(d, text, font, cx, y, track_mm, fill):
    track = mm(track_mm)
    breite = sum(font.getlength(c) for c in text) + track * (len(text) - 1)
    x = cx - breite / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + track
    return breite


def logo_oben(bild, breite_mm=58, oben_mm=15):
    lg = Image.open("vs-logo.png").convert("RGBA")
    b = int(mm(breite_mm))
    lg = lg.resize((b, int(lg.height * b / lg.width)), Image.LANCZOS)
    bild.alpha_composite(lg, (int(W / 2 - b / 2), int(mm(oben_mm))))
    # die Zeile unter der Wortmarke steht so auf ihrem Briefpapier
    gesperrt(ImageDraw.Draw(bild), "medium. coach. teacher.",
             f("Montserrat.ttf", 2.6, "Light"), W / 2,
             mm(oben_mm) + lg.height + mm(1.5), 1.0, GRAU_H + (255,))
    return mm(oben_mm) + lg.height


def spirit_marke(bild, y_mm, groesse_mm=17):
    """Die Spirit-Akademie-Marke wie unten rechts auf dem Briefpapier.

    "AKADEMIE" sitzt unter der rechten Haelfte des Schriftzugs, nicht mittig
    darunter - sonst laeuft es in die Unterlaengen der Schreibschrift hinein.
    """
    d = ImageDraw.Draw(bild)
    skript = f("AdornStoryScript.ttf", groesse_mm)
    wort = "Spirit"
    kasten = skript.getbbox(wort)
    b = kasten[2] - kasten[0]
    ak_font = f("Montserrat.ttf", 3.6, "Regular")
    ak_breite = sum(ak_font.getlength(c) for c in "AKADEMIE") + mm(1.6) * 7
    gesamt = b + ak_breite * 0.45
    x = W / 2 - gesamt / 2
    d.text((x - kasten[0], mm(y_mm)), wort, font=skript, fill=GRAU_H + (255,))
    ax = x + b - ak_breite * 0.55
    ay = mm(y_mm) + (kasten[3] - kasten[1]) * 1.06
    for ch in "AKADEMIE":
        d.text((ax, ay), ch, font=ak_font, fill=GRAU_H + (255,))
        ax += ak_font.getlength(ch) + mm(1.6)


def bauen(kopf, zeile2, jahr, unterzeile=None, datei="schild.png"):
    bild = Image.new("RGBA", (W, H), WEISS + (255,))
    unten = logo_oben(bild)
    d = ImageDraw.Draw(bild)

    y = mm(112)
    gesperrt(d, kopf, f("Montserrat.ttf", 13.5, "Light"), W / 2, y, 2.4, GRAU + (255,))
    if zeile2:
        gesperrt(d, zeile2, f("Montserrat.ttf", 13.5, "Light"), W / 2, y + mm(19.5), 2.4,
                 GRAU + (255,))
        y = y + mm(19.5)

    # Goldlinie und Jahr
    ly = y + mm(29)
    d.rectangle([W / 2 - mm(26), ly, W / 2 + mm(26), ly + max(2, int(mm(0.4)))], fill=GOLD)
    gesperrt(d, jahr, f("Montserrat.ttf", 9.5, "Light"), W / 2, ly + mm(8), 4.2,
             GOLD + (255,))

    if unterzeile:
        gesperrt(d, unterzeile, f("Runalto.ttf", 6.4), W / 2, ly + mm(28), 0.6,
                 GRAU_H + (255,))

    spirit_marke(bild, HOEHE_MM - 40)
    rgb = bild.convert("RGB")
    rgb.save(datei, dpi=(DPI, DPI))
    rgb.save(datei.replace(".png", ".pdf"), "PDF", resolution=DPI)
    return datei


if __name__ == "__main__":
    bauen("BASISAUSBILDUNG", "ZUM MEDIUM", "2026", None, "schild-a-2026.png")
    bauen("BASISAUSBILDUNG", "ZUM MEDIUM", "2026",
          "ohne Mystik und Märchen", "schild-b-2026.png")
    bauen("BASISAUSBILDUNG", "ZUM MEDIUM", "2027", None, "schild-a-2027.png")
    bauen("BASISAUSBILDUNG", "ZUM MEDIUM", "2027",
          "ohne Mystik und Märchen", "schild-b-2027.png")
    print("fertig", W, "x", H, "px")
