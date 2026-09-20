"""Drei Muster fuer den langen Uebergang - gleiche Aura-Farbwelt, andere Bewegung."""
import sys, os
sys.path.insert(0, ".")
import numpy as np
from PIL import Image
import render_ck as R
import brandkit as B
from aura import Aura, GOLD, ROSE, VIOLETT, TUERKIS, LICHT

W, H = B.W, B.H
GW, GH = 960, 540
OUT = sys.argv[1] if len(sys.argv) > 1 else "muster"
R.OUT = OUT
os.makedirs(OUT, exist_ok=True)


def _huelle(t, dauer, ein, aus):
    return B.ease_in_out(min(1.0, t / ein) * min(1.0, max(0.0, (dauer - t) / aus)))


def _rgba(rgb, a):
    out = np.empty((GH, GW, 4), np.uint8)
    out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA").resize((W, H), Image.BICUBIC)


def muster_a(dauer=4.5):
    """A - Aura-Atem: das Licht blueht aus der Flaeche auf, haelt, geht zurueck."""
    au = Aura(GW, GH, 5)
    au.feld(GOLD,    (0.44, 0.46), (0.44, 0.52), 0.0, (0.030, -0.020), 1.00)
    au.feld(ROSE,    (0.62, 0.56), (0.40, 0.46), 1.7, (-0.020, 0.020), 0.80)
    au.feld(VIOLETT, (0.48, 0.66), (0.48, 0.42), 3.1, (0.010, -0.030), 0.70)
    au.feld(LICHT,   (0.52, 0.48), (0.30, 0.34), 4.4, (0.000, 0.010), 0.85)
    mitte = dauer / 2.0

    def frame(t):
        tn = t / dauer
        atem = B.ease_in_out(max(0.0, 1.0 - abs(t - mitte) / mitte))
        rgb, inten = au.bild(tn, atem, 0.03)
        a = np.clip(inten * (0.35 + 1.5 * atem), 0, 1) ** 0.9
        deck = max(0.0, 1.0 - abs(t - mitte) / 0.55)
        a = np.clip(a + B.ease_in_out(deck) * 1.3, 0, 1)
        return _rgba(rgb, a * _huelle(t, dauer, 1.0, 1.0))

    R.encode("muster-a-aura-atem.mov", frame, True, dauer)


def muster_b(dauer=4.5):
    """B - Aurasaum: das Licht kommt vom Rand herein und schliesst sich."""
    au = Aura(GW, GH, 9)
    for farbe, mitte, gr, ph in [
        (GOLD,    (0.06, 0.34), (0.40, 0.55), 0.0),
        (ROSE,    (0.96, 0.60), (0.40, 0.55), 1.4),
        (VIOLETT, (0.40, 1.02), (0.55, 0.38), 2.8),
        (TUERKIS, (0.66, -0.04), (0.50, 0.36), 4.2),
    ]:
        au.feld(farbe, mitte, gr, ph, (0.0, 0.0), 0.95)
    mitte_t = dauer / 2.0

    def frame(t):
        tn = t / dauer
        schliessen = B.ease_in_out(max(0.0, 1.0 - abs(t - mitte_t) / mitte_t))
        # die Felder wachsen zur Mitte hin, statt sich zu bewegen
        for f in au.felder:
            f["groesse"] = (f.get("_g0", f["groesse"])[0] * (1.0 + 1.5 * schliessen),
                            f.get("_g0", f["groesse"])[1] * (1.0 + 1.5 * schliessen))
            f.setdefault("_g0", f["groesse"])
        rgb, inten = au.bild(tn, schliessen * 0.6, 0.03)
        a = np.clip(inten * (0.5 + 1.3 * schliessen), 0, 1) ** 0.9
        deck = max(0.0, 1.0 - abs(t - mitte_t) / 0.5)
        a = np.clip(a + B.ease_in_out(deck) * 1.3, 0, 1)
        return _rgba(rgb, a * _huelle(t, dauer, 1.0, 1.0))

    R.encode("muster-b-aurasaum.mov", frame, True, dauer)


def muster_c(dauer=4.5):
    """C - Aurazug: ein Lichtschleier zieht sehr langsam von unten nach oben."""
    au = Aura(GW, GH, 14)
    au.feld(VIOLETT, (0.35, 1.30), (0.70, 0.40), 0.0, (0.02, -1.70), 0.85)
    au.feld(ROSE,    (0.60, 1.55), (0.62, 0.36), 1.6, (-0.02, -1.75), 0.85)
    au.feld(GOLD,    (0.48, 1.80), (0.75, 0.42), 3.0, (0.01, -1.80), 1.00)
    au.feld(LICHT,   (0.52, 1.95), (0.45, 0.30), 4.5, (0.00, -1.85), 0.75)
    mitte = dauer / 2.0

    def frame(t):
        tn = t / dauer
        rgb, inten = au.bild(tn, 0.5, 0.03)
        a = np.clip(inten * 1.35, 0, 1) ** 0.9
        deck = max(0.0, 1.0 - abs(t - mitte) / 0.5)
        a = np.clip(a + B.ease_in_out(deck) * 1.3, 0, 1)
        return _rgba(rgb, a * _huelle(t, dauer, 0.9, 0.9))

    R.encode("muster-c-aurazug.mov", frame, True, dauer)


if __name__ == "__main__":
    muster_a(); muster_b(); muster_c()
