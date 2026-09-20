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
from aquarell import Aquarell
from wasser import Wasser

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


def aquarell(dauer=3.0, name="uebergang-aquarell.mov", gitter=(960, 540)):
    """Langer Kapiteluebergang: die Saat des Lebens laeuft aus wie Tinte im Wasser.

    Ablauf: die Geometrie steht zuerst als klare Goldzeichnung, faengt dann an zu
    bluten und wird zu Farbe im Wasser; zur Mitte hin deckt ein warmer Schwall
    das Bild vollstaendig ab - nur dadurch passt der Uebergang auf jeden Schnitt -
    danach treiben die Schlieren auseinander und geben das neue Bild frei.
    """
    gw, gh = gitter
    sim = Aquarell(gw, gh)

    # Saat des Lebens als Ausgangsfarbe, in Gittergroesse
    GEO = 2500
    geo_maske = B.saat_des_lebens(GEO, width=6)
    voll = Image.new("L", (W, H), 0)
    voll.paste(geo_maske, (int(W / 2 - GEO / 2), int(H / 2 - GEO / 2)))
    sim.einbringen(np.asarray(voll.resize((gw, gh), Image.LANCZOS), np.float32) / 255.0, 0.62)

    # klare Zeichnung fuer die erste Phase
    klar = B.einfaerben(geo_maske, B.GOLD_HELL, 1.0)
    klar = Image.alpha_composite(B.schein(klar, 16, 0.8), klar)

    T_BLUTEN, T_MITTE = 0.70, dauer / 2.0

    def farbe_zu_rgba(d, deckung):
        """Farbdichte in Bild umsetzen: aussen Bernstein, innen Gold bis Creme."""
        d = np.clip(d, 0, 1.6)
        a = np.clip(d * 1.05, 0, 1) ** 0.9
        t1 = np.clip(d * 1.5, 0, 1)[..., None]
        t2 = np.clip((d - 0.85) * 1.6, 0, 1)[..., None]
        c = (np.array([132, 68, 16], np.float32) * (1 - t1)
             + np.array([226, 168, 60], np.float32) * t1)
        c = c * (1 - t2) + np.array([250, 234, 196], np.float32) * t2
        # bei voller Deckung Richtung warmes Licht mischen - sonst deckt der
        # duenne Farbsaum das Bild in einem schmutzigen Braun ab
        if deckung > 0.001:
            c = c * (1 - deckung * 0.92) + np.array([250, 226, 180], np.float32) * deckung * 0.92
        rgba = np.empty((gh, gw, 4), np.uint8)
        rgba[..., :3] = np.clip(c, 0, 255).astype(np.uint8)
        rgba[..., 3] = (np.clip(a + deckung * 1.5, 0, 1) * 255).astype(np.uint8)
        return Image.fromarray(rgba, "RGBA").resize((W, H), Image.BICUBIC)

    zustand = {"t": -1.0}

    def frame(t):
        # Simulation nachziehen (zwei Teilschritte je Bild, ruhigerer Transport)
        while zustand["t"] < t - 1e-6:
            zustand["t"] += 1.0 / (FPS * 2)
            tn = max(0.0, (zustand["t"] - T_BLUTEN) / max(dauer - T_BLUTEN, 1e-6))
            if zustand["t"] >= T_BLUTEN:
                # Anlauf: erst kriecht die Farbe nur in die Flaeche, dann setzt
                # der Druck ein. Ohne das ist das Ausbluten der Linien - der
                # eigentliche Moment - nach zwei Zehnteln vorbei.
                anlauf = min(1.0, (zustand["t"] - T_BLUTEN) / 0.5) ** 1.6
                sim.schritt(tn, dt=1.2, stiftung=3.6 * anlauf * (1 - tn) ** 1.1,
                            diffusion=0.5 + 1.4 * tn, zerfall=0.988)

        # Volldeckung genau in der Mitte, damit der Uebergang auf jeden Schnitt passt
        deck = max(0.0, 1.0 - abs(t - T_MITTE) / 0.38)
        deck = B.ease_in_out(deck) ** 0.8

        lay = farbe_zu_rgba(sim.farbe, deck)

        # erste Phase: klare Zeichnung, die in die Farbe uebergeht
        p_klar = 1.0 if t < T_BLUTEN else max(0.0, 1.0 - (t - T_BLUTEN) / 0.62)
        if p_klar > 0.004:
            sk = 1.0 + 0.06 * min(1.0, t / T_BLUTEN)
            gs = int(GEO * sk)
            k = klar.resize((gs, gs), Image.BILINEAR)
            k.putalpha(k.getchannel("A").point(lambda v: int(v * p_klar)))
            lay.alpha_composite(k, (int(W / 2 - gs / 2), int(H / 2 - gs / 2)))

        # letzte Phase: alles sanft ausblenden
        if t > dauer - 0.55:
            a = max(0.0, (dauer - t) / 0.55)
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * B.ease_in_out(a))))
        return lay

    encode(name, frame, True, dauer)


def wasserfarben(dauer=3.5, name="uebergang-wasserfarben.mov", gitter=(960, 540)):
    """Kurzer Atemzug: Farbschleier im Wasser, die ineinander verlaufen.

    Einatmen - die Schleier treiben zueinander und mischen sich. Halten - sie
    decken das Bild. Ausatmen - sie sinken wieder auseinander und duennen aus.

    Kein Druck aus der Mitte und keine Geometrie: beides machte den ersten
    Versuch unruhig. Die Bewegung besteht nur aus grossen, traegen Wirbeln und
    einem leichten Zu- und Auseinanderdriften im Atemrhythmus.
    """
    gw, gh = gitter
    sim = Wasser(gw, gh)
    # vier Schleier, ausserhalb der Mitte und teils ausserhalb des Bildes
    sim.schleier(B.GOLD,            (gw * 0.30, gh * 0.32), (gw * 0.30, gh * 0.34), 0.95)
    sim.schleier(B.ORANGE,          (gw * 0.74, gh * 0.66), (gw * 0.32, gh * 0.32), 0.90)
    sim.schleier((242, 221, 176),   (gw * 0.60, gh * 0.22), (gw * 0.26, gh * 0.24), 0.75)
    # kein dunkles Braun: gemittelt mit dem Gold ergibt es ein stumpfes Oliv.
    # Alle vier Schleier bleiben in der warmen Gold-Bernstein-Familie und
    # unterscheiden sich nur in der Helligkeit.
    sim.schleier((168,  90,  26),   (gw * 0.24, gh * 0.78), (gw * 0.28, gh * 0.28), 0.70)

    EIN, HALT = 1.4, 1.9
    MITTE = (EIN + HALT) / 2.0

    zustand = {"t": -1.0}

    def atemwert(t):
        if t < EIN:
            return 0.95 * B.ease_in_out(t / EIN)
        if t < HALT:
            return 0.12
        return -0.75 * B.ease_in_out(min(1.0, (t - HALT) / 1.0))

    def frame(t):
        while zustand["t"] < t - 1e-6:
            zustand["t"] += 1.0 / (FPS * 2)
            sim.schritt(zustand["t"], atemwert(zustand["t"]), dt=1.05,
                        verlaufen=0.85, zerfall=0.9985)

        rgb, dichte = sim.bild()
        # Dichtehuelle: der Atemzug fuellt sich erst auf. Ohne sie deckt die
        # Farbe von der ersten Sekunde an und es gibt keinen Verlauf zu sehen.
        if t < EIN:
            hd = 0.18 + 0.82 * B.ease_in_out(t / EIN) ** 1.3
        elif t < HALT:
            hd = 1.0
        else:
            hd = max(0.0, 1.0 - B.ease_in_out(min(1.0, (t - HALT) / 1.45)) * 0.92)
        a = np.clip(dichte * 1.15 * hd, 0, 1) ** 0.95

        # Volldeckung in der Mitte des Atemzugs - im Farbton der Mischung, nicht
        # als heller Blitz, sonst wirkt es wieder wie ein Effekt
        deck = max(0.0, 1.0 - abs(t - MITTE) / 0.42)
        deck = B.ease_in_out(deck) ** 0.9
        if deck > 0.001:
            rgb = rgb * (1 - deck * 0.8) + np.array([226, 182, 104], np.float32) * deck * 0.8
            a = np.clip(a + deck * 1.35, 0, 1)

        # Anfang und Ende sauber bei null
        huelle = min(1.0, t / 0.8) * min(1.0, max(0.0, (dauer - t) / 0.8))
        a = a * B.ease_in_out(huelle)

        rgba = np.empty((gh, gw, 4), np.uint8)
        rgba[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
        rgba[..., 3] = (a * 255).astype(np.uint8)
        return Image.fromarray(rgba, "RGBA").resize((W, H), Image.BICUBIC)

    encode(name, frame, True, dauer)


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


def kapitel(titel, kennzeichen, name, unterzeile=None, dauer=4.5):
    _karte_clip(name, lambda: L.kapitelkarte(titel, kennzeichen, unterzeile),
                dauer, ein=1.2, aus=1.0)


def themen_bauchbinde(titel, kennzeichen, name, dauer=6.0):
    """Kleine Themeneinblendung unten links fuer das laufende Bild.

    Bewusst anders aufgebaut als die Namens-Bauchbinde - Saat des Lebens statt
    Lotus-Faecher, Titel in Runalto - damit der Zuschauer beide nicht verwechselt.
    """
    x0, basis = B.SAFE_X, 1680
    kf = B.grotesk(52, "Medium")
    kz = Image.new("RGBA", (int(B.breite(kennzeichen.upper(), kf, 18)) + 20, 110), (0, 0, 0, 0))
    B.gesperrt(ImageDraw.Draw(kz), kennzeichen.upper(), kf, 0, 0, 18, B.GOLD + (255,))
    kz_r, pad_k = _mit_schatten(kz, 12, 1.7)

    tf = B.runalto(112)
    tw = int(B.breite(titel, tf, 8))
    tt = Image.new("RGBA", (tw + 20, 210), (0, 0, 0, 0))
    B.gesperrt(ImageDraw.Draw(tt), titel, tf, 0, 0, 8, B.CREAM + (255,))
    tt_r, pad_t = _mit_schatten(tt, 16, 1.5)

    sym = B.einfaerben(B.saat_des_lebens(150, width=3), B.ORANGE_HL, 0.95)
    sym_r, pad_s = _mit_schatten(sym, 12, 1.5)

    breite = max(tw, 1500) + 220
    gw, gh = int(breite * 2.0), 1100
    gx, gy = int(x0 + breite * 0.5 - gw / 2), int(basis + 90 - gh / 2)
    grund = B.verlauf_radial((gw, gh), (gw / 2, gh / 2), (breite * 0.78, 400),
                             (10, 7, 5), 215, schwelle=5)
    grund_a = grund.getchannel("A")

    def frame(t):
        aus = 1.0 if t < dauer - 1.4 else max(0.0, 1.0 - B.ease_in_out((t - (dauer - 1.4)) / 1.0))
        p_k = min(1.0, max(0.0, (t - 0.00) / 0.55))
        p_t = min(1.0, max(0.0, (t - 0.30) / 0.75))

        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_g = 0.95 * B.ease_out(p_k) * aus
        if a_g > 0.004:
            g = grund.copy()
            g.putalpha(grund_a.point(lambda v: int(v * a_g)))
            lay.alpha_composite(g, (gx, gy))

        def mit(img, a):
            if a <= 0.003:
                return None
            o = img.copy()
            o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
            return o

        s = mit(sym_r, p_k * aus)
        if s: lay.alpha_composite(s, (x0 - pad_s, basis - 4 - pad_s))
        s = mit(kz_r, p_k * aus)
        if s: lay.alpha_composite(s, (x0 + 200 - pad_k, basis - pad_k))
        dx = int(60 * (1 - B.ease_out(p_t)))
        s = mit(tt_r, p_t * aus)
        if s: lay.alpha_composite(s, (x0 + 200 - dx - pad_t, basis + 92 - pad_t))
        return lay

    encode(name, frame, True, dauer)


def nachklang(satz="Erkenne deinen Seelenplan.", dauer=6.0):
    """Schlusskarte eins: ein ruhiger Satz, der nachwirken darf."""
    _karte_clip("schluss-1-nachklang.mp4", lambda: L.nachklang(satz), dauer,
                ein=1.6, aus=1.6)


def kontakt(eintraege=None, dauer=7.0):
    """Schlusskarte zwei: wo man sie findet."""
    _karte_clip("schluss-2-kontakt.mp4", lambda: L.kontakt(eintraege), dauer,
                ein=1.4, aus=1.4)


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
    for fn in (bauchbinde, lichtbluete, atemblende, faecher, opener, nachklang,
               kontakt, logo_eck):
        fn()
    kapitel("Was dein Seelenplan dir zeigt", "Kapitel 2", "kapitelkarte-beispiel.mp4")
