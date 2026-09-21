"""Nur der Faecher-Moment, isoliert und schnell.

Neuer Ansatz: Die Strahlen schiessen schnell heraus und werden dann gebremst -
ein Ausbruch, kein gleichmaessiges Auseinanderdriften. Schnell genug, um der
Diffusion davonzulaufen, gebremst genug, um im Bild zu bleiben.
"""
import sys
sys.path.insert(0, ".")
import numpy as np
from PIL import Image
from partikel import Wolke, auftragen, fertig

W, H = 1920, 1080
CREME = np.array([249, 245, 236], np.float32)
K_BLAU = np.array([2.05, 1.30, 0.22], np.float32)
K_GELB = np.array([0.10, 0.42, 2.10], np.float32)
BLAETTER = 13
PUNKT = (W * 0.57, H * 0.52)


def blattwinkel(rng, n, versatz):
    paare = BLAETTER // 2 + 1
    blatt = np.clip((rng.random(n) * paare).astype(np.int32) * 2 + versatz, 0, BLAETTER - 1)
    breite = np.pi / BLAETTER
    # Blattbreite leicht streuen, sonst wirken die Strahlen mechanisch
    streu = (rng.random(n) - 0.5) * breite * (0.55 + 0.7 * rng.random(n))
    return (blatt + 0.5) * breite + streu


class Strahlen:
    def __init__(self, anzahl, versatz, saat):
        rng = np.random.default_rng(saat)
        self.w = Wolke(anzahl, W, H, saat=saat)
        self.w.saeen_fleck(PUNKT, 26, anzahl=anzahl, streuung=0.8)
        n = self.w.x.size
        self.winkel = blattwinkel(rng, n, versatz)
        # sehr unterschiedliche Geschwindigkeiten: dadurch franst jedes Blatt
        # an der Spitze aus, statt als geschlossener Balken zu enden
        self.v = (240 + 1500 * rng.random(n) ** 1.7).astype(np.float32)
        self.rng = rng

    def schritt(self, dt, bremse=2.1, zittern=1.7):
        self.v *= np.exp(-bremse * dt)          # Ausbruch, dann abbremsen
        self.w.x += np.cos(self.winkel) * self.v * dt
        self.w.y += -np.sin(self.winkel) * self.v * dt
        n = self.w.x.size
        self.w.x += self.rng.normal(0, zittern, n).astype(np.float32)
        self.w.y += self.rng.normal(0, zittern, n).astype(np.float32)


def lauf(bremse=2.1, zittern=1.7, dichte=0.16, partikel=260000):
    a = Strahlen(partikel, 0, 5)
    b = Strahlen(partikel, 1, 9)
    bilder = {}
    FPS, TEIL = 30, 6
    for i in range(40):
        pa = np.zeros(H * W, np.float32); pb = np.zeros(H * W, np.float32)
        for k in range(TEIL):
            a.schritt(1.0 / (FPS * TEIL), bremse, zittern)
            b.schritt(1.0 / (FPS * TEIL), bremse, zittern)
            auftragen(pa, a.w, W, H, 1.0 / TEIL)
            auftragen(pb, b.w, W, H, 1.0 / TEIL)
        if i in (4, 10, 18, 32):
            da, db = fertig(pa, W, H, 0.5), fertig(pb, W, H, 0.5)
            tiefe = np.clip((da[..., None] * K_BLAU + db[..., None] * K_GELB) * dichte, 0, 1.9)
            bilder[i] = np.clip(CREME * np.exp(-tiefe), 0, 255).astype(np.uint8)
    return bilder


if __name__ == "__main__":
    b = lauf()
    bogen = Image.new("RGB", (1920, 270), (255, 255, 255))
    for i, (k, im) in enumerate(sorted(b.items())):
        bogen.paste(Image.fromarray(im).resize((480, 270), Image.LANCZOS), (i * 480, 0))
    bogen.save("/tmp/faecher.png")
    print("fertig")
