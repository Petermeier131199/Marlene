"""Einblender fuer das Video "Ueber Essen und ueber mich".

Rendert vier Elemente als Videodateien:

  titelkarte      Vollbild, kommt nach dem gesprochenen Einstieg
  triggerwarnung  Bauchbinde mit Alphakanal, liegt ueber dem Material
  zwischenblende  Vollbild, ueberbrueckt die Luecke in der Aufnahme
  abbinder        Vollbild mit Anlaufstellen, ganz am Schluss

Die Farbwelt ist aus einem Standbild des Videos abgeleitet: helle Wand,
helle Eiche, Goldrahmen, brauner Ledersessel, Burgunder im Blumenstrauss.
Deshalb helle Karten - eine dunkle Tafel risse mitten im Video ein Loch.

    python3 cards.py [name ...]      # ohne Argument: alle vier

Ergebnis liegt in out/ - je Element eine ProRes-.mov fuer Final Cut Pro und
eine .mp4 zur schnellen Ansicht.
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FPS = int(os.environ.get("FPS", 25))
FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# --- Palette (aus dem Standbild) ---------------------------------------------
PAPER = (241, 235, 227)      # cremiges Off-White, Grund der Karten
INK = (59, 52, 46)           # tiefes Warmbraun, Schrift
GOLD = (176, 138, 74)        # Goldrahmen im Hintergrund
BURGUNDY = (140, 58, 56)     # Blumenstrauss, sparsamster Akzent
MUTED = (124, 112, 100)      # zurueckgenommene Nebenzeilen


def font(name, variation, size):
    f = ImageFont.truetype(os.path.join(FONTDIR, name), size)
    f.set_variation_by_name(variation)
    return f


def serif(size, weight="Light"):
    return font("CormorantGaramond.ttf", weight, size)


def grotesk(size, weight="Light"):
    return font("Montserrat.ttf", weight, size)


# --- Zeichenhilfen ------------------------------------------------------------
def tracked_text(draw, text, f, cx, y, color, track=0.0, anchor="mm", left=None):
    """Text mit einstellbarer Sperrung. Gibt die Gesamtbreite zurueck."""
    widths = [f.getlength(ch) for ch in text]
    total = sum(widths) + track * max(0, len(text) - 1)
    pen = (cx - total / 2.0) if left is None else left
    for ch, w in zip(text, widths):
        draw.text((pen, y), ch, font=f, fill=color, anchor="l" + anchor[1])
        pen += w + track
    return total


def text_width(text, f, track=0.0):
    return sum(f.getlength(ch) for ch in text) + track * max(0, len(text) - 1)


def hairline(draw, cx, y, halfwidth, color, width=2, alpha=255):
    draw.line([(cx - halfwidth, y), (cx + halfwidth, y)],
              fill=color + (alpha,) if len(color) == 3 else color, width=width)


def paper_ground():
    """Grund der Vollbildkarten: warmes Off-White mit ganz weichem Lichtverlauf.

    Der Verlauf ist bewusst kaum sichtbar - er verhindert nur, dass die Flaeche
    tot wirkt, und nimmt das Tageslicht aus dem Raum auf.
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # Licht kommt im Video von links vorn
    d = np.sqrt(((xx - 0.36 * W) / (1.05 * W)) ** 2 + ((yy - 0.30 * H) / (1.15 * H)) ** 2)
    lift = np.clip(1.0 - d, 0, 1) ** 1.4
    base = np.array(PAPER, dtype=np.float32)
    img = base[None, None, :] * (0.955 + 0.055 * lift[:, :, None])
    return np.clip(img, 0, 255)


GROUND = paper_ground()


def grain(seed, strength=2.6):
    """Feine Koernung. Bewusst pro Karte konstant, nicht pro Bild neu gewuerfelt:
    stehende Koernung liest sich wie Papier, flimmert nicht und laesst die
    Datei um ein Vielfaches kleiner werden als rieselndes Filmkorn."""
    rng = np.random.default_rng(seed)
    n = rng.normal(0.0, strength, (H // 2, W // 2, 1)).astype(np.float32)
    n = np.repeat(np.repeat(n, 2, axis=0), 2, axis=1)
    return n


GRAIN = None   # wird nach der Definition von grain() gesetzt


def clamp01(x):
    return 0.0 if x < 0 else (1.0 if x > 1 else x)


def ease_in_out(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ease_out_cubic(x):
    return 1 - (1 - clamp01(x)) ** 3


def fade(t, dur, fin=0.55, fout=0.55):
    """Deckkraft der ganzen Karte: sanft auf, halten, sanft ab."""
    return min(ease_in_out(t / fin), ease_in_out((dur - t) / fout))


GRAIN = grain(11, 1.8)


# --- Karten -------------------------------------------------------------------
def card_titel(t, dur):
    """Titelkarte. Zeilen steigen minimal auf, Goldlinie zieht nach aussen."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    f1 = serif(118, "Light")
    fsub = grotesk(24, "Light")

    p1 = ease_out_cubic((t - 0.35) / 1.10)
    p2 = ease_out_cubic((t - 0.60) / 1.10)
    pr = ease_out_cubic((t - 1.15) / 0.90)
    ps = ease_out_cubic((t - 1.45) / 0.95)

    for p, line, y0 in ((p1, "ÜBER ESSEN", 0.385), (p2, "UND ÜBER MICH", 0.505)):
        if p <= 0.002:
            continue
        col = INK + (int(255 * p),)
        tracked_text(d, line, f1, W / 2, y0 * H + 14 * (1 - p) ** 1.5, col, track=9 + 6 * (1 - p))

    if pr > 0.002:
        hairline(d, W / 2, 0.588 * H, 150 * pr, GOLD, width=2, alpha=int(210 * pr))

    if ps > 0.002:
        tracked_text(d, "SEELISCH. NICHT KÖRPERLICH.", fsub, W / 2,
                     0.648 * H + 8 * (1 - ps) ** 1.5, MUTED + (int(235 * ps),), track=8 + 4 * (1 - ps))

    return layer, fade(t, dur, 0.5, 0.7)


def card_zwischenblende(t, dur):
    """Ueberbrueckt die Luecke. Benennt sie, statt sie zu verstecken -
    ein stummer Schnitt an dieser Stelle laese die Zuschauer ratlos zurueck."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    f1 = serif(64, "Light")
    f2 = serif(64, "Light")

    p1 = ease_out_cubic((t - 0.30) / 0.95)
    p2 = ease_out_cubic((t - 0.95) / 0.95)
    pr = ease_out_cubic((t - 0.70) / 0.80)

    if p1 > 0.002:
        tracked_text(d, "Hier haben mich ein paar Sekunden verlassen.", f1, W / 2,
                     0.452 * H + 10 * (1 - p1) ** 1.5, INK + (int(255 * p1),), track=1.5)
    if pr > 0.002:
        hairline(d, W / 2, 0.512 * H, 60 * pr, GOLD, width=2, alpha=int(180 * pr))
    if p2 > 0.002:
        tracked_text(d, "Die Kamera, meine ich.", f2, W / 2,
                     0.572 * H + 10 * (1 - p2) ** 1.5, MUTED + (int(255 * p2),), track=1.5)

    return layer, fade(t, dur, 0.45, 0.55)


def card_abbinder(t, dur):
    """Anlaufstellen. Steht am Ende ruhig und lange genug zum Mitschreiben."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    fk = grotesk(22, "Light")
    fh = serif(58, "Light")
    fname = grotesk(27, "Medium")
    fnum = grotesk(40, "Regular")   # Grotesk wegen der Versalziffern
    fnote = grotesk(19, "Light")

    p = ease_out_cubic((t - 0.30) / 1.20)
    if p <= 0.002:
        return layer, fade(t, dur, 0.5, 0.8)
    a = int(255 * p)
    dy = 12 * (1 - p) ** 1.5

    tracked_text(d, "WENN DICH DAS GERADE SELBST BETRIFFT", fk, W / 2, 0.185 * H + dy,
                 GOLD + (a,), track=7)
    hairline(d, W / 2, 0.228 * H + dy, 120 * p, GOLD, width=2, alpha=int(160 * p))

    tracked_text(d, "Du musst damit nicht allein bleiben.", fh, W / 2, 0.305 * H + dy,
                 INK + (a,), track=1.5)

    rows = [
        ("Beratungstelefon Essstörungen", "0221 892031",
         "Mo–Do 10–22 Uhr · Fr–So 10–18 Uhr · anonym und kostenfrei"),
        ("TelefonSeelsorge", "0800 111 0 111  ·  116 123",
         "rund um die Uhr · anonym und kostenfrei"),
    ]
    y = 0.435 * H
    for name, num, note in rows:
        tracked_text(d, name.upper(), fname, W / 2, y + dy, INK + (a,), track=4)
        tracked_text(d, num, fnum, W / 2, y + 0.056 * H + dy, BURGUNDY + (a,), track=5)
        tracked_text(d, note, fnote, W / 2, y + 0.103 * H + dy, MUTED + (int(a * 0.9),), track=2)
        y += 0.175 * H

    tracked_text(d, "IM NOTFALL: 112", fk, W / 2, 0.845 * H + dy, MUTED + (int(a * 0.85),), track=7)

    return layer, fade(t, dur, 0.6, 0.9)


def lower_third(t, dur):
    """Bauchbinde mit Alphakanal, laeuft ueber das laufende Bild.

    Liegt unten links ueber der hellen Tischzone. Eine weiche Off-White-Flaeche
    traegt die Schrift, ohne das Bild zu verdecken; links eine Goldkante.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    fl = grotesk(21, "Medium")
    ft = serif(48, "Light")

    label = "TRIGGERWARNUNG"
    body = "Körperbild · gestörtes Essverhalten"

    padx, pady = 46, 34
    wl = text_width(label, fl, 6)
    wt = text_width(body, ft, 1.5)
    bw = int(max(wl, wt) + 2 * padx)
    bh = int(pady * 2 + 30 + 58)
    bx, by = 110, int(H - 150 - bh)

    # Panel: weiche Flaeche mit abgerundeten Ecken und leichtem Schlagschatten
    panel = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(panel).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=6, fill=255)

    slide = 1.0 - ease_out_cubic((t - 0.15) / 0.85)
    wipe = ease_out_cubic((t - 0.15) / 0.95)
    ox = int(-26 * slide)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sm = Image.new("L", (W, H), 0)
    sm.paste(panel, (bx + ox, by + 10))
    shadow.paste((40, 34, 28, 255), (0, 0), sm.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.30)))
    layer = Image.alpha_composite(layer, shadow)

    body_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    body_layer.paste(PAPER + (238,), (0, 0), _mask_at(panel, bx + ox, by))
    # Goldkante links, faehrt mit auf
    edge = Image.new("L", (3, int(bh * wipe)), 255)
    body_layer.paste(GOLD + (255,), (0, 0), _mask_at(edge, bx + ox, by))

    d = ImageDraw.Draw(body_layer)
    pl = ease_out_cubic((t - 0.35) / 0.70)
    pb = ease_out_cubic((t - 0.50) / 0.70)
    if pl > 0.002:
        tracked_text(d, label, fl, 0, by + pady + 8, BURGUNDY + (int(255 * pl),),
                     track=6, left=bx + ox + padx)
    if pb > 0.002:
        tracked_text(d, body, ft, 0, by + pady + 62, INK + (int(255 * pb),),
                     track=1.5, left=bx + ox + padx)

    layer = Image.alpha_composite(layer, body_layer)
    return layer, fade(t, dur, 0.05, 0.75)


def _mask_at(mask, x, y):
    m = Image.new("L", (W, H), 0)
    m.paste(mask, (x, y))
    return m


# --- Rendering ----------------------------------------------------------------
def render(name, fn, dur, alpha=False, seed=7):
    n = int(round(dur * FPS))
    os.makedirs(OUTDIR, exist_ok=True)
    mov = os.path.join(OUTDIR, f"{name}.mov")
    mp4 = os.path.join(OUTDIR, f"{name}.mp4")

    import imageio_ffmpeg
    exe = imageio_ffmpeg.get_ffmpeg_exe()

    pix = "rgba" if alpha else "rgb24"
    # ProRes nur, wo es gebraucht wird: der Alphakanal geht in H.264 verloren.
    # Fuer die flaechigen Vollbildkarten ist H.264 visuell gleichwertig und
    # rund 25x kleiner. PRORES=1 erzwingt .mov fuer alle.
    want_mov = alpha or os.environ.get("PRORES") == "1"
    # ProRes 4444 traegt den Alphakanal, ProRes 422 HQ reicht fuer Vollbild
    prores = (["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "8"]
              if alpha else ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"])

    enc = subprocess.Popen(
        [exe, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", pix,
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *prores, mov],
        stdin=subprocess.PIPE) if want_mov else None

    frames = []
    for i in range(n):
        t = i / FPS
        layer, opacity = fn(t, dur)
        opacity = max(0.0, min(1.0, opacity))

        if alpha:
            arr = np.asarray(layer, dtype=np.float32).copy()
            arr[:, :, 3] *= opacity
            out = np.clip(arr, 0, 255).astype(np.uint8)
        else:
            base = GROUND + GRAIN
            fg = np.asarray(layer, dtype=np.float32)
            a = (fg[:, :, 3:4] / 255.0) * opacity
            rgb = base * (1 - a) + fg[:, :, :3] * a
            out = np.clip(rgb, 0, 255).astype(np.uint8)

        frames.append(out)
        if enc:
            enc.stdin.write(out.tobytes())

    if enc:
        enc.stdin.close()
        enc.wait()

    # Ansichtskopie
    mp4args = (["-c:v", "libx264", "-preset", "slow", "-crf", "16",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart"])
    p = subprocess.Popen([exe, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          *mp4args, mp4], stdin=subprocess.PIPE)
    for f in frames:
        if alpha:
            # fuer die Ansichtskopie auf hellem Grund zusammenrechnen
            a = f[:, :, 3:4].astype(np.float32) / 255.0
            comp = GROUND * (1 - a) + f[:, :, :3].astype(np.float32) * a
            p.stdin.write(np.clip(comp, 0, 255).astype(np.uint8).tobytes())
        else:
            p.stdin.write(f.tobytes())
    p.stdin.close()
    p.wait()

    # Standbild aus der Mitte, zum schnellen Draufschauen
    mid = frames[int(n * 0.72)]
    if alpha:
        a = mid[:, :, 3:4].astype(np.float32) / 255.0
        mid = np.clip(GROUND * (1 - a) + mid[:, :, :3].astype(np.float32) * a, 0, 255).astype(np.uint8)
    Image.fromarray(mid).save(os.path.join(OUTDIR, f"{name}-vorschau.png"))
    print("fertig:", (mov + " / " if want_mov else "") + mp4)


CARDS = {
    "titelkarte": (card_titel, 4.0, False),
    "zwischenblende": (card_zwischenblende, 3.6, False),
    "abbinder": (card_abbinder, 11.0, False),
    "triggerwarnung": (lower_third, 6.0, True),
}


def main():
    names = sys.argv[1:] or list(CARDS)
    for name in names:
        fn, dur, alpha = CARDS[name]
        render(name, fn, dur, alpha)


if __name__ == "__main__":
    main()
