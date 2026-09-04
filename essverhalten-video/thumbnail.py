"""YouTube-Thumbnails fuer "Ueber Essen und ueber mich".

1280x720 (YouTubes Vorgabe), gleiche Farbwelt wie die Einblender in cards.py.

Zwei Layouts:

  typo   nur Schrift auf cremefarbenem Grund - funktioniert ohne Standbild
  foto   Standbild formatfuellend, cremefarbener Verlauf ueber der Textseite

Auf YouTube schlaegt das Foto-Layout das reine Schrift-Layout deutlich: das
Thumbnail wird auf dem Handy briefmarkengross gesehen, und ein Gesicht liest
man dort sofort, einen Satz nicht. Die Schrift-Variante ist der Rueckfall,
wenn kein brauchbares Standbild da ist.

    python3 thumbnail.py                          # alle Schrift-Varianten
    python3 thumbnail.py --foto standbild.png     # alle Foto-Varianten
    python3 thumbnail.py --foto standbild.png --fokus 0.62 --seite rechts

--fokus verschiebt den Bildausschnitt waagerecht (0 = ganz links, 1 = ganz
rechts) und entscheidet, wo dein Gesicht landet. --seite sagt, auf welcher
Haelfte die Schrift steht; das Gesicht gehoert auf die andere.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from cards import GOLD, BURGUNDY, grotesk, serif, text_width, tracked_text

W, H = 1280, 720
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# Fuer das Thumbnail dunkler als in den Einblendern: es wird briefmarkengross
# gesehen, da traegt der zarte Braunton der Karten nicht mehr.
PAPER = (243, 238, 231)
INK = (43, 37, 32)
MUTED = (112, 100, 89)

# Die Varianten. Erste Zeile ist der Blickfang, deshalb kurz; die Unterzeile
# darf klein bleiben, sie wird ohnehin erst beim Draufklicken gelesen.
VARIANTEN = {
    "a-nackig": {
        "zeilen": [("SEELISCH", INK), ("NACKIG.", BURGUNDY)],
        "unter": "GESTÖRTES ESSVERHALTEN · 40 MINUTEN AM STÜCK",
    },
    "b-titel": {
        "zeilen": [("ÜBER ESSEN", INK), ("UND ÜBER MICH", INK)],
        "unter": "EIN GESPRÄCH OHNE DREHBUCH",
    },
    "c-ehrlich": {
        "zeilen": [("40 MINUTEN", INK), ("EHRLICH.", BURGUNDY)],
        "unter": "ÜBER KÖRPERBILD UND GESTÖRTES ESSVERHALTEN",
    },
}


def grund():
    """Cremefarbener Grund mit sehr weichem Lichtverlauf."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - 0.34 * W) / (1.05 * W)) ** 2 + ((yy - 0.28 * H) / (1.15 * H)) ** 2)
    lift = np.clip(1.0 - d, 0, 1) ** 1.4
    return np.clip(np.array(PAPER, np.float32)[None, None, :] * (0.955 + 0.055 * lift[:, :, None]), 0, 255)


def foto_grund(pfad, fokus, seite):
    """Standbild formatfuellend, darueber ein cremefarbener Verlauf auf der
    Textseite. Der Verlauf ist der eigentliche Trick: er nimmt der Schrift den
    unruhigen Untergrund, ohne das Foto zuzudecken."""
    im = Image.open(pfad).convert("RGB")
    bw, bh = im.size
    s = max(W / bw, H / bh)
    im = im.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.LANCZOS)
    ox = int((im.width - W) * min(1.0, max(0.0, fokus)))
    oy = int((im.height - H) * 0.5)
    arr = np.asarray(im.crop((ox, oy, ox + W, oy + H)), np.float32)

    x = np.linspace(0, 1, W, dtype=np.float32)
    if seite == "links":
        # deckend am linken Rand, offen ab etwa der Bildmitte
        a = np.clip((0.58 - x) / 0.34, 0, 1) ** 0.85
    else:
        a = np.clip((x - 0.42) / 0.34, 0, 1) ** 0.85
    a = a[None, :, None] * 0.94
    return np.clip(arr * (1 - a) + np.array(PAPER, np.float32)[None, None, :] * a, 0, 255)


def _cap(f):
    b = f.getbbox("H")
    return b[3] - b[1]


def zeile(d, text, f_serif, groesse, y_mitte, farbe, track=4, cx=None, links=None):
    """Zeichnet eine Versalzeile und setzt Ziffern in Montserrat.

    Cormorant hat Mediaevalziffern - eine 4 sitzt dort tiefer als ein H und
    reisst jede Versalzeile auseinander. Die Grotesk wird auf dieselbe
    Versalhoehe skaliert und auf derselben Grundlinie gesetzt, dann faellt der
    Wechsel nicht auf.
    """
    cap = _cap(f_serif)
    g = max(8, int(round(groesse * cap / max(1, _cap(grotesk(groesse, "Bold"))))))
    f_ziffer = grotesk(g, "Bold")

    def f_fuer(ch):
        return f_ziffer if ch.isdigit() else f_serif

    breite = sum(f_fuer(c).getlength(c) for c in text) + track * max(0, len(text) - 1)
    stift = (cx - breite / 2.0) if links is None else links
    grundlinie = y_mitte + cap / 2.0
    for ch in text:
        f = f_fuer(ch)
        d.text((stift, grundlinie), ch, font=f, fill=farbe, anchor="ls")
        stift += f.getlength(ch) + track
    return breite


def zeichne(basis, variante, seite="links", foto=False):
    img = Image.fromarray(basis.astype(np.uint8)).convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    zeilen = variante["zeilen"]
    unter = variante["unter"]

    if foto:
        # Schrift steht in ihrer Haelfte linksbuendig, das Gesicht bekommt die andere
        rand = 74
        cx = None
        links = rand if seite == "links" else W // 2 + 40
        breite = (W // 2 - 40) - rand if seite == "links" else W - rand - (W // 2 + 40)
    else:
        cx, links, breite = W / 2, None, W - 300

    # Schriftgrad so gross wie moeglich: ein Thumbnail wird briefmarkengross
    # gesehen, zu kleine Schrift ist dort schlicht nicht da. Bold statt Medium,
    # weil Cormorants duenne Striche beim Herunterskalieren verschwinden.
    def zeilenbreite(g):
        fs = serif(g, "Bold")
        cap = _cap(fs)
        gz = max(8, int(round(g * cap / max(1, _cap(grotesk(g, "Bold"))))))
        fz = grotesk(gz, "Bold")
        return max(sum((fz if c.isdigit() else fs).getlength(c) for c in t) + 4 * (len(t) - 1)
                   for t, _ in zeilen)

    groesse = 150
    while groesse > 40 and zeilenbreite(groesse) > breite:
        groesse -= 3
    f = serif(groesse, "Bold")

    zh = groesse * 0.95
    block = zh * (len(zeilen) - 1) + zh * 1.18     # Zeilen plus Linie und Unterzeile
    y0 = H * 0.47 - block / 2

    for i, (t, col) in enumerate(zeilen):
        zeile(d, t, f, groesse, y0 + i * zh, col + (255,), track=4, cx=cx, links=links)

    # Unterzeile in ihre Spalte zwingen - im Foto-Layout darf sie nicht in die
    # Bildhaelfte hineinlaufen, sonst steht sie auf dem Gesicht.
    gu = 20 if foto else 22
    while gu > 11 and text_width(unter, grotesk(gu, "Medium"), 5) > breite:
        gu -= 1
    fu = grotesk(gu, "Medium")
    yu = y0 + (len(zeilen) - 1) * zh + zh * 1.18
    if cx:
        d.line([(cx - 52, yu - zh * 0.52), (cx + 52, yu - zh * 0.52)], fill=GOLD + (225,), width=3)
        tracked_text(d, unter, fu, cx, yu, MUTED + (255,), track=5)
    else:
        d.line([(links, yu - zh * 0.52), (links + 96, yu - zh * 0.52)], fill=GOLD + (235,), width=3)
        tracked_text(d, unter, fu, 0, yu, MUTED + (255,), track=5, left=links)

    return Image.alpha_composite(img, layer).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--foto", help="Standbild aus dem Video (PNG/JPG)")
    ap.add_argument("--fokus", type=float, default=0.5,
                    help="waagerechter Bildausschnitt, 0=links … 1=rechts")
    ap.add_argument("--seite", choices=("links", "rechts"), default="links",
                    help="auf welcher Haelfte die Schrift steht")
    ap.add_argument("varianten", nargs="*", default=list(VARIANTEN))
    args = ap.parse_args()

    os.makedirs(OUTDIR, exist_ok=True)
    for name in args.varianten:
        v = VARIANTEN[name]
        if args.foto:
            basis = foto_grund(args.foto, args.fokus, args.seite)
            bild = zeichne(basis, v, args.seite, foto=True)
            ziel = os.path.join(OUTDIR, f"thumbnail-foto-{name}.jpg")
        else:
            bild = zeichne(grund(), v)
            ziel = os.path.join(OUTDIR, f"thumbnail-{name}.jpg")
        # JPG mit Qualitaet 92: YouTube nimmt bis 2 MB, das bleibt weit darunter
        bild.save(ziel, quality=92, subsampling=0)
        print("fertig:", ziel, f"({os.path.getsize(ziel) // 1024} kB)")


if __name__ == "__main__":
    main()
