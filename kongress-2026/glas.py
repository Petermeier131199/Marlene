"""Markensequenz: Tinte im klaren Wasser. Gelb als Farbe, Blau nur als Licht."""
import sys, os
sys.path.insert(0, ".")
import numpy as np
from PIL import Image
import render_ck as R
import brandkit as B
from tinte import Tinte

W, H = B.W, B.H
GW, GH = 960, 540
GELB      = np.array([231, 180,  40], np.float32)   # ihr Gelb
GELB_HELL = np.array([250, 231, 176], np.float32)
BLAU      = np.array([ 82, 122, 186], np.float32)   # ihr Blau, nur als Licht


def sequenz(dauer=5.0, name="uebergang-tinte-im-wasser.mov", deckend=True):
    sim = Tinte(GW, GH)
    EIN_VON, EIN_BIS = 0.35, 1.75          # solange beruehrt der Pinsel das Wasser
    MITTE = dauer * 0.5
    zustand = {"t": -1.0}

    # Blau als Licht: ein ruhiger, kuehler Schimmer, kein Farbauftrag
    yy, xx = np.mgrid[0:GH, 0:GW].astype(np.float32)
    licht = np.exp(-(((xx - GW * 0.42) / (GW * 0.78)) ** 2
                     + ((yy - GH * 0.22) / (GH * 0.85)) ** 2))

    def frame(t):
        while zustand["t"] < t - 1e-6:
            zustand["t"] += 1.0 / (R.FPS * 2)
            tt = zustand["t"]
            if EIN_VON <= tt <= EIN_BIS:
                staerke = 0.26 * B.ease_in_out(min(1.0, (tt - EIN_VON) / 0.35))
                sim.eintauchen([(0.33, 1.0), (0.47, 0.5), (0.63, 0.75)], staerke)
            # das Sinken wird nach dem Eintauchen langsamer - die Farbe verteilt
            # sich, statt weiter durchzufallen
            nach = max(0.0, (tt - EIN_BIS) / max(dauer - EIN_BIS, 1e-6))
            sim.schritt(sinken=3.6 * (1 - 0.70 * nach),
                        seitlich=0.45 + 0.7 * nach,
                        wirbel=0.55 + 0.9 * nach,
                        verlaufen=0.45 + 2.1 * nach,
                        zerfall=0.9965)

        d = sim.farbe
        a = np.clip(d * 0.95, 0, 1) ** 1.0

        t1 = np.clip((d - 0.35) * 1.8, 0, 1)[..., None]
        rgb = GELB * (1 - t1) + GELB_HELL * t1

        # Blau nur als Licht: leichter kuehler Schimmer im klaren Wasser
        blau_a = licht * 0.26 * B.ease_in_out(max(0.0, 1.0 - abs(t - MITTE) / (dauer * 0.55)))
        rgb = rgb * (1 - blau_a[..., None] * 0.55) + BLAU * blau_a[..., None] * 0.55
        a = np.clip(a + blau_a, 0, 1)

        if deckend:
            deck = B.ease_in_out(max(0.0, 1.0 - abs(t - MITTE) / 0.55)) ** 1.1
            rgb = rgb * (1 - deck * 0.85) + np.array([246, 226, 166], np.float32) * deck * 0.85
            a = np.clip(a + deck * 1.35, 0, 1)

        huelle = min(1.0, t / 0.5) * min(1.0, max(0.0, (dauer - t) / 0.9))
        a = a * B.ease_in_out(huelle)

        out = np.empty((GH, GW, 4), np.uint8)
        out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
        out[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
        return Image.fromarray(out, "RGBA").resize((W, H), Image.BICUBIC)

    R.encode(name, frame, True, dauer)


if __name__ == "__main__":
    R.OUT = sys.argv[1] if len(sys.argv) > 1 else "muster"
    os.makedirs(R.OUT, exist_ok=True)
    sequenz()
