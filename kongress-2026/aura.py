"""Aura-Lichtfelder: ruhige, ineinanderliegende Farbschleier.

Bewusst keine Stroemungssimulation. Transport erzeugt Wirbel, und Wirbel lesen
sich als Unruhe - der Grund, warum die beiden Vorversuche nicht getragen haben.
Hier bewegt sich nichts durch das Bild; es sind grosse, weiche Lichtfelder, die
langsam atmen, ihre Mittelpunkte kaum merklich verschieben und ihre Farbe
schimmern lassen. Das ist optisch fast Stillstand und trotzdem lebendig.
"""
import numpy as np
from scipy.ndimage import gaussian_filter

# Aura-Palette: gedeckt gehalten, damit es edel bleibt und nicht bunt wird
GOLD      = (232, 194,  90)
ROSE      = (200, 122, 158)
VIOLETT   = (138, 114, 196)
TUERKIS   = ( 98, 184, 176)
LICHT     = (246, 236, 217)


class Aura:
    def __init__(self, breite, hoehe, saat=5):
        self.w, self.h = breite, hoehe
        self.rng = np.random.default_rng(saat)
        self.yy, self.xx = np.mgrid[0:hoehe, 0:breite].astype(np.float32)
        # eine einzige, sehr grobe Stoerung bricht die perfekte Ellipsenform auf
        stoer = self.rng.normal(0, 1, (max(4, hoehe // 90), max(4, breite // 90)))
        from scipy.ndimage import zoom
        self.stoer = gaussian_filter(
            zoom(stoer, (hoehe / stoer.shape[0], breite / stoer.shape[1]), order=3), 40)
        self.stoer /= np.abs(self.stoer).max() + 1e-6
        self.felder = []

    def feld(self, farbe, mitte, groesse, phase=0.0, wandern=(0.0, 0.0), staerke=1.0):
        """Ein weiches Lichtfeld. `wandern` ist der Weg seines Mittelpunkts
        ueber die gesamte Sequenz - in Bildanteilen, absichtlich winzig."""
        self.felder.append(dict(farbe=np.array(farbe, np.float32), mitte=mitte,
                                groesse=groesse, phase=phase, wandern=wandern,
                                staerke=staerke))

    def _lobe(self, f, tn, atem):
        cx = (f["mitte"][0] + f["wandern"][0] * tn) * self.w
        cy = (f["mitte"][1] + f["wandern"][1] * tn) * self.h
        rx = f["groesse"][0] * self.w * (0.88 + 0.22 * atem)
        ry = f["groesse"][1] * self.h * (0.88 + 0.22 * atem)
        d = (((self.xx - cx) / rx) ** 2 + ((self.yy - cy) / ry) ** 2)
        d = d * (1.0 + 0.30 * self.stoer)        # weiche, unregelmaessige Kante
        return np.exp(-d * 1.15) * f["staerke"]

    def bild(self, tn, atem, schimmer=0.0):
        """Farben additiv wie Licht mischen; gibt (rgb, intensitaet)."""
        summe = np.zeros((self.h, self.w), np.float32)
        rgb = np.zeros((self.h, self.w, 3), np.float32)
        for i, f in enumerate(self.felder):
            g = self._lobe(f, tn, atem)
            # Schimmern: jedes Feld pulsiert in eigener Phase
            g = g * (1.0 + schimmer * np.sin(tn * 5.0 + f["phase"]))
            summe += g
            rgb += g[..., None] * f["farbe"]
        rgb /= (summe[..., None] + 1e-6)
        return rgb, summe
