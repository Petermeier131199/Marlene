"""Die Markensequenz: zwei Bänder laufen auf einen Punkt zu und fächern auf.

Aufbau in vier Abschnitten:

1. Zwei Partikelbänder ziehen herein - Blau von links oben, ihr Gelb von rechts
   unten. Beide werden vom Stroemungsfeld zu Faeden ausgezogen.
2. Sie laufen auf einen gemeinsamen Punkt zu und verdichten sich dort.
3. Aus diesem Punkt faechert alles nach oben auf. Die Strahlen sind nicht
   gleichmaessig verteilt, sondern in dreizehn Buendel gegliedert - so viele
   Blaetter hat der Faecher in ihrem Logo. Damit zeichnet die Bewegung ihr
   Zeichen, ohne dass ein Logo zu sehen ist.
4. Der Faecher zerfaellt, das Bild wird wieder cremeweiss.

Die Farben liegen additiv als Dichte vor und werden am Ende nach dem
Absorptionsgesetz auf den hellen Grund gerechnet: Tinte auf Papier schluckt
Licht, sie strahlt nicht. Nur dadurch mischen sich Blau und Gelb dort, wo sie
sich ueberlagern, so wie in echtem Wasser.
"""
import os, subprocess, sys
import numpy as np
import imageio_ffmpeg
from partikel import Stroemung, Wolke, auftragen, fertig
import brandkit as B

W, H = 1920, 1080
FPS, TEIL = 30, 6

CREME = np.array([249, 245, 236], np.float32)
# Absorptionskoeffizienten statt Farbwerte: Blau schluckt Rot, Gelb schluckt Blau
K_BLAU = np.array([2.05, 1.30, 0.22], np.float32)
K_GELB = np.array([0.10, 0.42, 2.10], np.float32)

# Zeitgeruest (Sekunden)
T_EIN, T_LAUF, T_FAECHER, T_ENDE = 0.30, 1.30, 1.95, 3.60
PUNKT = np.array([W * 0.57, H * 0.50], np.float32)
BLAETTER = 13                      # so viele Blaetter hat ihr Logo-Faecher


def _blattwinkel(rng, n, versatz):
    """Winkel im Faecher: nach oben geoeffnet, in Blaetter gegliedert.

    `versatz` waehlt jedes zweite Blatt aus. Die beiden Baender bekommen so
    ineinandergreifende Blaetter statt derselben Flaeche - sonst liegen Blau und
    Gelb uebereinander, und nach dem Absorptionsgesetz schlucken sie zusammen
    alles Licht: der Faecher wird schwarz.
    """
    paare = BLAETTER // 2 + 1
    blatt = np.minimum((rng.random(n) * paare).astype(np.int32), paare - 1) * 2 + versatz
    blatt = np.clip(blatt, 0, BLAETTER - 1)
    breite = np.pi / BLAETTER
    mitte = (blatt + 0.5) * breite
    # innerhalb des Blattes zur Mitte hin verdichtet
    return mitte + (rng.random(n) - 0.5) * breite * 0.78


class Faecher:
    """Der Ausbruch aus dem Punkt.

    Bewusst nicht aus den Baendern heraus entwickelt, sondern als eigener
    Ausbruch, der eingeblendet wird waehrend die Baender verschwinden. Grund:
    Tinte sieht nur deshalb nach Tinte aus, weil sie zerlaeuft - ein lesbarer
    Faecher braucht aber scharfe Strahlen. Transportiert man die Baender weiter,
    zerstreut die Diffusion den Faecher, bevor er zu sehen ist. Der Ausbruch
    ist schnell genug, um ihr davonzulaufen, und wird dann abgebremst.
    """

    def __init__(self, anzahl, versatz, saat):
        rng = np.random.default_rng(saat)
        self.w = Wolke(anzahl, W, H, saat=saat)
        self.w.saeen_fleck((PUNKT[0], PUNKT[1]), 26, anzahl=anzahl, streuung=0.8)
        n = self.w.x.size
        self.winkel = _blattwinkel(rng, n, versatz)
        # stark gestreute Geschwindigkeit: dadurch franst jedes Blatt aus
        self.v = (240 + 1350 * rng.random(n) ** 1.7).astype(np.float32)
        self.rng = rng

    def schritt(self, dt, bremse=3.0, zittern=1.7):
        self.v *= np.exp(-bremse * dt)
        self.w.x += np.cos(self.winkel) * self.v * dt
        self.w.y += -np.sin(self.winkel) * self.v * dt
        n = self.w.x.size
        self.w.x += self.rng.normal(0, zittern, n).astype(np.float32)
        self.w.y += self.rng.normal(0, zittern, n).astype(np.float32)


class Band:
    def __init__(self, start, ziel, anzahl, saat, versatz=0, radius=95, glieder=6):
        self.wolke = Wolke(anzahl, W, H, saat=saat)
        for k in range(glieder):
            f = k / (glieder - 1)
            p = start + (ziel - start) * f * 0.55
            self.wolke.saeen_fleck((p[0], p[1]), radius, anzahl=anzahl // glieder,
                                   streuung=0.6)
        self.richtung = (ziel - start)
        self.richtung = self.richtung / (np.linalg.norm(self.richtung) + 1e-6)
        rng = np.random.default_rng(saat + 40)
        n = self.wolke.x.size
        self.winkel = _blattwinkel(rng, n, versatz)
        self.tempo_aus = (0.55 + 0.9 * rng.random(n)).astype(np.float32)

    def schritt(self, feld, t, dt):
        w = self.wolke
        if t < T_LAUF:                              # hereinziehen
            zug = 7.6 * self.richtung
        elif t < T_FAECHER:                         # auf den Punkt zulaufen
            dx, dy = PUNKT[0] - w.x, PUNKT[1] - w.y
            r = np.hypot(dx, dy) + 1e-6
            p = (t - T_LAUF) / (T_FAECHER - T_LAUF)
            # Umrechnung: ein Schritt wirkt mit dt*3.4, davon sechs je Bild bei
            # 30 Bildern - ein Wert von 1 entspricht also gut 100 Pixeln je
            # Sekunde. Vorher stand hier 19, das waren 1900 Pixel je Sekunde,
            # und die Baender sind in einen Punkt geknallt.
            v = 1.2 + 4.2 * p
            # nicht bis auf null zusammenlaufen: ein Haufen im selben Pixel
            # treibt die Dichte ins Unendliche und die Farbe wird schwarz
            # nicht enger als 90 Pixel zusammenlaufen: dichter gedraengt steigt
            # die Dichte so stark, dass die Absorption ins Schwarze laeuft
            halten = np.clip((r - 90.0) / 60.0, 0.0, 1.0)
            w.x += dx / r * v * halten * dt * 3.4
            w.y += dy / r * v * halten * dt * 3.4
            zug = np.zeros(2, np.float32)
        else:                                       # nach dem Punkt nur noch treiben
            zug = np.zeros(2, np.float32)
        # waehrend des Faechers traegt das Stroemungsfeld kaum noch bei - sonst
        # verbiegt es die Strahlen, bevor sie ueberhaupt zu sehen sind
        tempo = 17.0 if t < T_FAECHER else 2.2
        zittern = 1.1 + 1.3 * max(0.0, (t - T_FAECHER) / 1.2)
        w.bewegen(feld, t * 0.8, tempo, drift=(zug[0], zug[1]), dt=dt * 3.4,
                  zittern=zittern)


def rendern(ziel, band_p=300000, faecher_p=220000, dauer=3.9):
    feld = Stroemung(W, H, ((13, 1.0), (6, 0.55), (3, 0.25)), saat=4)
    blau = Band(np.array([-W * 0.10, -H * 0.10]), PUNKT, band_p, 11, versatz=0)
    gelb = Band(np.array([W * 1.10, H * 1.12]), PUNKT, band_p, 23, versatz=1)
    fb = Faecher(faecher_p, 0, 5)
    fg = Faecher(faecher_p, 1, 9)

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    enc = subprocess.Popen(
        [ff, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
         "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", ziel],
        stdin=subprocess.PIPE)

    n = int(dauer * FPS)
    proben = {}
    for i in range(n):
        pb = np.zeros(H * W, np.float32)
        pg = np.zeros(H * W, np.float32)
        t = i / FPS
        # Uebergabe: Baender verschwinden, waehrend der Faecher aufgeht
        a_band = 1.0 if t < T_FAECHER else max(0.0, 1.0 - (t - T_FAECHER) / 0.30)
        a_fae = 0.0 if t < T_FAECHER else min(1.0, (t - T_FAECHER) / 0.16)
        a_fae *= max(0.0, min(1.0, (dauer - 0.35 - t) / 0.85))

        for k in range(TEIL):
            tk = (i + k / TEIL) / FPS
            if tk >= T_EIN and a_band > 0.002:
                blau.schritt(feld, tk, 1.0 / TEIL)
                gelb.schritt(feld, tk, 1.0 / TEIL)
                auftragen(pb, blau.wolke, W, H, a_band / TEIL)
                auftragen(pg, gelb.wolke, W, H, a_band / TEIL)
            if tk >= T_FAECHER:
                fb.schritt(1.0 / (FPS * TEIL))
                fg.schritt(1.0 / (FPS * TEIL))
                if a_fae > 0.002:
                    auftragen(pb, fb.w, W, H, a_fae / TEIL)
                    auftragen(pg, fg.w, W, H, a_fae / TEIL)

        db = fertig(pb, W, H, 0.5)
        dg = fertig(pg, W, H, 0.5)
        huelle = min(1.0, max(0.0, (t - T_EIN) / 0.35)) * \
                 min(1.0, max(0.0, (dauer - t) / 0.7))
        knoten = min(1.0, max(0.0, (t - (T_LAUF + 0.25)) / 0.45)) * \
                 (1.0 - min(1.0, max(0.0, (t - T_FAECHER) / 0.3)))
        s = (0.46 - 0.16 * knoten) * B.ease_in_out(huelle)
        tiefe = np.clip((db[..., None] * K_BLAU + dg[..., None] * K_GELB) * s, 0, 1.75)
        rgb = CREME * np.exp(-tiefe)
        rgb = rgb + np.random.default_rng(i).normal(0, 1.1, rgb.shape)
        rgb = np.clip(rgb, 0, 255).astype(np.uint8)
        enc.stdin.write(rgb.tobytes())
        if i in (14, 36, 54, 64, 78, 100):
            proben[i] = rgb.copy()
    enc.stdin.close()
    enc.wait()
    return proben


if __name__ == "__main__":
    from PIL import Image
    import time
    t0 = time.time()
    p = rendern(sys.argv[1] if len(sys.argv) > 1 else "/tmp/signatur.mp4")
    print("Lauf in %.0fs" % (time.time() - t0))
    bogen = Image.new("RGB", (1920, 540), (255, 255, 255))
    for i, (k, im) in enumerate(sorted(p.items())):
        bogen.paste(Image.fromarray(im).resize((640, 360), Image.LANCZOS)
                    .crop((0, 45, 640, 315)), ((i % 3) * 640, (i // 3) * 270))
    bogen.save("/tmp/signatur.png")
