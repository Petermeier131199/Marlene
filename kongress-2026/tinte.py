"""Tinte, die in klarem Wasser nach unten sinkt.

Der Unterschied zu den verworfenen Versuchen ist die Art der Stroemung, nicht
die Tatsache, dass gestroemt wird. Vorher war das Feld wirbelig - Farbe wurde
im Kreis getragen, und das liest sich als Unruhe. Hier dominiert die
Schwerkraft: eine einzige, gleichbleibende Richtung nach unten, dazu nur eine
sehr schwache, grossskalige seitliche Stoerung, die die Faeden auffaechert.
Solche Stroemung heisst laminar und ist von sich aus ruhig.
"""
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter, zoom


class Tinte:
    def __init__(self, breite, hoehe, saat=3):
        self.w, self.h = breite, hoehe
        self.rng = np.random.default_rng(saat)
        self.yy, self.xx = np.mgrid[0:hoehe, 0:breite].astype(np.float32)
        self.farbe = np.zeros((hoehe, breite), np.float32)
        self.seit = [self._grob(sk) for sk in (150, 70)]   # seitliche Stoerung
        self.sink = self._grob(190)                        # Sinkgeschwindigkeit
        # schwaches Wirbelfeld: sinkende Tinte rollt sich an ihrer Spitze ein,
        # ohne das bleiben glatte Saeulen statt Faeden. Quellenfrei gebildet und
        # so schwach gehalten, dass die Schwerkraft klar dominiert.
        p = self._grob(60)
        gy, gx = np.gradient(p)
        self.wx, self.wy = gy / (np.abs(gy).max() + 1e-6), -gx / (np.abs(gx).max() + 1e-6)

    def _grob(self, skala):
        k = self.rng.normal(0, 1, (max(4, self.h // skala), max(4, self.w // skala)))
        g = zoom(k, (self.h / k.shape[0], self.w / k.shape[1]), order=3)
        g = gaussian_filter(g, skala * 0.42).astype(np.float32)
        return g / (np.abs(g).max() + 1e-6)

    def eintauchen(self, stellen, staerke=1.0, breite_px=None):
        """Farbe an der Oberflaeche zufuehren - dort, wo der Pinsel eintaucht."""
        breite_px = breite_px or self.w * 0.016
        for x_anteil, gew in stellen:
            cx = x_anteil * self.w
            cy = self.h * 0.035
            d = np.exp(-(((self.xx - cx) / breite_px) ** 2
                         + ((self.yy - cy) / (self.h * 0.030)) ** 2))
            self.farbe = np.clip(self.farbe + d * staerke * gew, 0, 1.4)

    def schritt(self, sinken=3.2, seitlich=0.85, wirbel=0.7, verlaufen=0.85,
                zerfall=0.997):
        # Schwerkraft dominiert; die Stoerung faechert die Faeden nur auf
        vy = sinken * (1.0 + 0.30 * self.sink)
        vx = seitlich * (self.seit[0] + 0.45 * self.seit[1]) + wirbel * self.wx
        vy = vy + wirbel * self.wy
        qx = np.clip(self.xx - vx, 0, self.w - 1)
        qy = np.clip(self.yy - vy, 0, self.h - 1)
        self.farbe = np.array(
            map_coordinates(self.farbe, [qy, qx], order=1, mode="constant", cval=0.0),
            np.float32)
        self.farbe = gaussian_filter(self.farbe, verlaufen) * zerfall
