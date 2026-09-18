"""Rendert alle Einblendungen und Uebergaenge in 4K/60 fps.

Overlays (Bauchbinde, Uebergaenge) gehen als MOV mit PNG-Codec raus: verlustfrei,
echter Alphakanal, importiert in Premiere, DaVinci und Final Cut. Vollbildkarten
als H.264 mit hoher Datenrate.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg
import brandkit as B
import layouts as L

FPS = 30            # 60 / 30 geht glatt auf: keine ungleichmaessige
                    # Bildverdopplung in einer 60p-Timeline
AUSGABE = (1920, 1080)
W, H = B.W, B.H
FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)


def encode(name, frames, alpha, dauer):
    """frames: Generator von PIL-Bildern. alpha=True -> MOV/PNG RGBA."""
    pfad = os.path.join(OUT, name)
    if alpha:
        # PNG im MOV: verlustfrei, echter Alphakanal, importiert in Premiere,
        # DaVinci und Final Cut. Bei diesen Inhalten kleiner als ProRes 4444
        # (gemessen: 22 statt 29 MB bei gleichem Testclip).
        args = ["-c:v", "png", "-pix_fmt", "rgba"]
        pix_in = "rgba"
    else:
        args = ["-c:v", "libx264", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
        pix_in = "rgb24"
    # Aufgebaut wird in 4K, ausgegeben in 1080p: das Herunterrechnen wirkt wie
    # achtfaches Antialiasing, Schrift und Goldlinien bleiben dadurch sauber.
    skala = ["-vf", f"scale={AUSGABE[0]}:{AUSGABE[1]}:flags=lanczos"]
    cmd = [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", pix_in,
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *skala, *args, pfad]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dauer * FPS))
    for i in range(n):
        img = frames(i / FPS)
        p.stdin.write(img.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg fehlgeschlagen: " + name)
    mb = os.path.getsize(pfad) / 1e6
    print(f"  {name}  {dauer:.2f}s  {n} Frames  {mb:.0f} MB")


# --------------------------------------------------------------- Bauchbinde
def _schatten(img, radius=14, staerke=1.0, farbe=(0, 0, 0)):
    """Weicher dunkler Schatten unter einem Element - traegt die Lesbarkeit
    auch dort, wo der Abdunkler allein nicht reicht (helle Wand, Lampe)."""
    sch = Image.new("RGBA", img.size, farbe + (0,))
    sch.putalpha(img.getchannel("A"))
    sch = sch.filter(ImageFilter.GaussianBlur(radius))
    if staerke != 1.0:
        sch.putalpha(sch.getchannel("A").point(lambda v: min(255, int(v * staerke))))
    return sch


def _mit_schatten(img, radius=14, staerke=1.6, versatz=(0, 6)):
    """Element auf transparenter Flaeche, Schatten inklusive."""
    pad = radius * 3
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sch = _schatten(img, radius, staerke)
    out.alpha_composite(sch, (pad + versatz[0], pad + versatz[1]))
    out.alpha_composite(sch, (pad + versatz[0], pad + versatz[1]))   # zweifach = dichter
    out.alpha_composite(img, (pad, pad))
    return out, pad


def _bauchbinde_frame():
    x0, basis = B.SAFE_X, 1660
    wort_r, pad_w = _mit_schatten(L.wortmarke_in(B.CREAM, 138), 16, 1.5)
    fae = L.FAECHER.resize((int(L.FAECHER.width * 205 / L.FAECHER.height), 205), Image.LANCZOS)
    fae_r, pad_f = _mit_schatten(fae, 14, 1.4)
    breite = fae.width + 48 + L.wortmarke_in(B.CREAM, 138).width

    rt = "MEDIUM  |  SPEAKERIN  |  COACH"
    rf = B.grotesk(58, "Medium")
    rolle = Image.new("RGBA", (int(B.breite(rt, rf, 11)) + 20, 130), (0, 0, 0, 0))
    B.gesperrt(ImageDraw.Draw(rolle), rt, rf, 0, 0, 11, (246, 228, 168) + (255,))
    rolle_r, pad_r = _mit_schatten(rolle, 12, 1.7)

    # Abdunkler: deutlich kraeftiger und grosszuegiger als zuvor, von der
    # unteren linken Ecke ausgehend und nach rechts oben auslaufend
    gw, gh = int(breite * 2.6), 1500
    gx, gy = int(x0 + breite * 0.5 - gw / 2), int(basis + 150 - gh / 2)
    grund = B.verlauf_radial((gw, gh), (gw / 2, gh / 2), (breite * 1.25, 660),
                             (10, 7, 5), 215, schwelle=4)
    # zweiter, engerer Abdunkler direkt hinter dem Schriftblock: die weite
    # Flaeche allein reicht gegen eine helle Wand mit Lampe nicht aus
    eng = B.verlauf_radial((gw, gh), (gw / 2, gh / 2 + 40), (breite * 0.72, 330),
                           (12, 8, 5), 170, schwelle=4)
    grund = Image.alpha_composite(grund, eng)
    grund_a = grund.getchannel("A")

    def frame(t):
        aus = 1.0 if t < 6.6 else max(0.0, 1.0 - B.ease_in_out((t - 6.6) / 1.0))
        p_linie = min(1.0, max(0.0, (t - 0.00) / 0.55))
        p_text = min(1.0, max(0.0, (t - 0.25) / 0.80))
        p_rolle = min(1.0, max(0.0, (t - 0.75) / 0.60))

        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_g = 0.95 * B.ease_out(p_text) * aus
        if a_g > 0.004:
            g = grund.copy()
            g.putalpha(grund_a.point(lambda v: int(v * a_g)))
            lay.alpha_composite(g, (gx, gy))

        lw = int(breite * B.ease_out(p_linie))
        if lw > 2 and aus > 0:
            linie = Image.new("RGBA", (max(lw, 1), 5), B.GOLD + (int(235 * aus),))
            lay.alpha_composite(_schatten(linie, 8, 1.6), (x0, basis + 212))
            lay.alpha_composite(linie, (x0, basis + 208))

        def mit(img, a):
            if a <= 0.003:
                return None
            o = img.copy()
            o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
            return o

        dx = int(70 * (1 - B.ease_out(p_text)))
        s = mit(fae_r, p_text * aus)
        if s: lay.alpha_composite(s, (x0 - dx - pad_f, basis - 62 - pad_f))
        s = mit(wort_r, p_text * aus)
        if s: lay.alpha_composite(s, (x0 + fae.width + 48 - dx - pad_w, basis + 30 - pad_w))
        s = mit(rolle_r, p_rolle * aus)
        if s: lay.alpha_composite(s, (x0 + 4 - pad_r, basis + 244 - pad_r))
        return lay

    return frame


def bauchbinde(dauer=8.0):
    encode("bauchbinde-vanessa-spaleck.mov", _bauchbinde_frame(), True, dauer)


# --------------------------------------------------------------- Uebergaenge
_yy, _xx = np.mgrid[0:H, 0:W]
_dist = np.sqrt(((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2)
_dist_n = _dist / _dist.max()


def _bloom_rgba(staerke, warm=(255, 214, 150), kern=(255, 246, 232)):
    """Radialer Lichtschwall; staerke 0..1, bei 1 deckt er das Bild vollstaendig."""
    a = np.clip((1.35 * staerke - _dist_n * (1.0 - staerke) * 1.6), 0, 1)
    a = a ** 1.25
    if staerke >= 0.999:
        a = np.ones_like(a)
    mix = np.clip(staerke * 1.15 - _dist_n * 0.35, 0, 1)[..., None]
    col = np.array(warm, np.float32) * (1 - mix) + np.array(kern, np.float32) * mix
    rgba = np.empty((H, W, 4), np.uint8)
    rgba[..., :3] = col.astype(np.uint8)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def lichtbluete(dauer=1.0):
    """Saat des Lebens blueht auf und deckt in der Mitte komplett ab."""
    basis = 2600
    sym = B.saat_des_lebens(basis, width=7)

    def frame(t):
        p = t / dauer
        s = 0.22 + 1.55 * B.ease_in_out(min(1.0, p * 1.12))
        deck = 1 - abs(p - 0.5) * 2
        deck = B.ease_in_out(deck) ** 0.75
        lay = _bloom_rgba(deck)
        gs = max(40, int(basis * s))
        g = sym.resize((gs, gs), Image.BILINEAR)
        a_geo = (0.95 if p < 0.5 else max(0.0, 1 - (p - 0.5) * 2.4)) * min(1.0, p * 5)
        geo = B.einfaerben(g, B.ORANGE_HL if p < 0.45 else B.GOLD_HELL, a_geo)
        geo = Image.alpha_composite(B.schein(geo, 14, 0.7), geo)
        lay.alpha_composite(geo, (int(W / 2 - gs / 2), int(H / 2 - gs / 2)))
        return lay

    encode("uebergang-lichtbluete.mov", frame, True, dauer)


def atemblende(dauer=0.6):
    """Weicher Lichtatem fuer Schnitte innerhalb eines Kapitels."""
    def frame(t):
        p = t / dauer
        deck = B.ease_in_out(1 - abs(p - 0.5) * 2) ** 0.8
        return _bloom_rgba(deck, warm=(255, 206, 140), kern=(255, 244, 226))

    encode("uebergang-atemblende.mov", frame, True, dauer)


def faecher(dauer=1.2):
    """Ihr Lotus-Faecher oeffnet sich durchs Bild."""
    f = L.FAECHER
    gross = f.resize((int(f.width * 1500 / f.height), 1500), Image.LANCZOS)

    def frame(t):
        p = t / dauer
        deck = B.ease_in_out(1 - abs(p - 0.5) * 2) ** 0.85
        lay = _bloom_rgba(deck, warm=(250, 196, 120), kern=(255, 242, 224))
        sk = 0.55 + 1.15 * B.ease_in_out(p)
        gw, gh = int(gross.width * sk), int(gross.height * sk)
        g = gross.resize((gw, gh), Image.BILINEAR).rotate(
            -22 + 44 * B.ease_in_out(p), resample=Image.BILINEAR, expand=True)
        a = min(1.0, p * 4) * (1.0 if p < 0.55 else max(0.0, 1 - (p - 0.55) * 2.6))
        g.putalpha(g.getchannel("A").point(lambda v: int(v * a * 0.95)))
        g = Image.alpha_composite(B.schein(g, 12, 0.55), g)
        lay.alpha_composite(g, (int(W / 2 - g.width / 2), int(H * 0.60 - g.height / 2)))
        return lay

    encode("uebergang-faecher.mov", frame, True, dauer)


# ------------------------------------------------------------ Vollbildkarten
_NOISE = None


def _koernung(img, staerke=1.6):
    """Feines Dither gegen Streifenbildung in den dunklen Verlaeufen.

    Bewusst EIN feststehendes Rauschfeld fuer alle Frames. Streifenbildung ist
    ein raeumliches Problem, kein zeitliches - und Rauschen, das sich je Bild
    aendert, kostet bei 4K/60 ein Vielfaches an Datenrate, weil der Encoder
    zwischen den Bildern nichts mehr fortschreiben kann.
    """
    global _NOISE
    if _NOISE is None:
        _NOISE = np.random.default_rng(7).normal(0, staerke, (H, W, 1)).astype(np.float32)
    return Image.fromarray(
        np.clip(np.asarray(img, np.float32) + _NOISE, 0, 255).astype(np.uint8), "RGB")


def _karte_clip(name, bauen, dauer, ein=1.3, aus=1.0):
    """Statische Karte mit sanfter Auf- und Abblende plus leichtem Heranfahren."""
    voll = bauen()
    zoom = 1.035

    def frame(t):
        p = t / dauer
        sk = zoom - (zoom - 1.0) * B.ease_out(min(1.0, t / dauer))
        nw, nh = int(W * sk), int(H * sk)
        img = voll.resize((nw, nh), Image.BILINEAR).crop(
            ((nw - W) // 2, (nh - H) // 2, (nw - W) // 2 + W, (nh - H) // 2 + H))
        a = 1.0
        if t < ein:
            a = B.ease_in_out(t / ein)
        elif t > dauer - aus:
            a = B.ease_in_out(max(0.0, (dauer - t) / aus))
        if a < 0.999:
            img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, a)
        return _koernung(img)

    encode(name, frame, False, dauer)


def opener(dauer=6.5):
    _karte_clip("titel-opener.mp4", lambda: L.titel_opener(), dauer, ein=1.5, aus=1.2)


def kapitel(titel, nummer, name, dauer=4.5):
    _karte_clip(name, lambda: L.kapitelkarte(titel, nummer), dauer, ein=1.2, aus=1.0)


def outro(dauer=8.0):
    def bauen():
        bg = L._hintergrund_karte()
        s = 1500
        bg.alpha_composite(B.einfaerben(B.blume_des_lebens(s, 3), B.GOLD, 0.18),
                           (int(W / 2 - s / 2), int(H * 0.5 - s / 2)))
        lg = B.ck_logo()
        zb = 1560
        lg = lg.resize((zb, int(lg.height * zb / lg.width)), Image.LANCZOS)
        bg.alpha_composite(lg, (int(W / 2 - zb / 2), int(H * 0.27)))
        for txt, size, track, farbe, y in [
            ("01. – 11. NOVEMBER 2026", 84, 14, B.CREAM + (240,), 0.555),
            ("Jetzt kostenfrei anmelden", 76, 6, B.GOLD_HELL + (245,), 0.665),
            ("channeling-portal.de", 66, 10, B.CREAM + (210,), 0.745),
        ]:
            f = B.runalto(size)
            w = B.breite(txt, f, track)
            lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
            B.gesperrt(ImageDraw.Draw(lay), txt, f, 0, 0, track, farbe)
            bg.alpha_composite(lay.crop((0, 0, int(w) + 10, 200)), (int(W / 2 - w / 2), int(H * y)))
        return bg.convert("RGB")

    _karte_clip("outro-anmeldung.mp4", bauen, dauer, ein=1.4, aus=1.4)


def logo_eck():
    """Dezente Dauereinblendung: ihr Zeichen oben rechts, als PNG mit Alpha."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wort = L.wortmarke_in(B.CREAM, 62)
    fae = L.FAECHER.resize((int(L.FAECHER.width * 96 / L.FAECHER.height), 96), Image.LANCZOS)
    x = W - B.SAFE_X - wort.width
    lay.alpha_composite(fae, (x - fae.width - 26, 118))
    lay.alpha_composite(wort, (x, 150))
    a = lay.getchannel("A").point(lambda v: int(v * 0.82))
    lay.putalpha(a)
    lay.resize(AUSGABE, Image.LANCZOS).save(os.path.join(OUT, "logo-eck.png"))
    print("  logo-eck.png")


if __name__ == "__main__":
    print("Rendere nach", OUT)
    for fn in (bauchbinde, lichtbluete, atemblende, faecher, opener, outro, logo_eck):
        fn()
    kapitel("Was dein Seelenplan dir zeigt", "Kapitel 2", "kapitelkarte-beispiel.mp4")
