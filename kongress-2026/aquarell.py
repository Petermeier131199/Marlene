"""Tinte-im-Wasser-Simulation fuer den langen Kapiteluebergang.

Die Saat des Lebens wird als Farbe in ein Stroemungsfeld gegeben und laeuft
darin auseinander. Das Feld besteht aus zwei Anteilen:

* einer radialen Ausbreitung nach aussen, die mit der Zeit nachlaesst - das ist
  der Druck des Tropfens,
* einem Wirbelfeld aus Rauschen, das die Faeden macht. Es wird als Rotation
  eines Potentialfeldes gebildet und ist dadurch quellenfrei; ohne diese
  Eigenschaft entstehen Quellen und Senken, in denen die Farbe unnatuerlich
  verschwindet oder aufplatzt.

Gerechnet wird auf halber Aufloesung und am Ende hochskaliert - Tinte hat keine
harten Kanten, der Unterschied ist unsichtbar, die Rechenzeit ein Viertel.
"""
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter


class Aquarell:
    def __init__(self, breite, hoehe, saat=7):
        self.w, self.h = breite, hoehe
        self.rng = np.random.default_rng(saat)
        yy, xx = np.mgrid[0:hoehe, 0:breite].astype(np.float32)
        self.xx, self.yy = xx, yy
        cx, cy = breite / 2.0, hoehe / 2.0
        dx, dy = xx - cx, yy - cy
        r = np.hypot(dx, dy) + 1e-6
        self.rn = r / np.hypot(cx, cy)          # normierter Radius
        self.ux_rad, self.uy_rad = dx / r, dy / r
        self._wirbel_felder = [self._potentialfeld(sk) for sk in (86, 42, 20)]
        self.farbe = np.zeros((hoehe, breite), np.float32)

    def _potentialfeld(self, skala):
        """Glattes Rauschpotential; seine Rotation ergibt ein quellenfreies Feld."""
        klein = self.rng.normal(0, 1, (max(4, self.h // skala), max(4, self.w // skala)))
        gross = np.array(
            map_coordinates(
                klein,
                [np.clip(self.yy / skala, 0, klein.shape[0] - 1),
                 np.clip(self.xx / skala, 0, klein.shape[1] - 1)],
                order=3, mode="reflect"),
            np.float32)
        return gaussian_filter(gross, skala * 0.35)

    def geschwindigkeit(self, t, stiftung=1.0):
        """Stroemungsfeld zum Zeitpunkt t (0..1 ueber die Sequenz)."""
        vx = np.zeros_like(self.farbe)
        vy = np.zeros_like(self.farbe)
        for i, pot in enumerate(self._wirbel_felder):
            gy, gx = np.gradient(pot)
            gew = (1.0, 0.40, 0.13)[i] * (1.0 + 0.35 * np.sin(t * 2.0 + i))
            vx += gy * gew
            vy += -gx * gew
        norm = np.abs(vx).max() + 1e-6
        vx, vy = vx / norm, vy / norm
        # radialer Druck, faellt ueber die Zeit ab und nach aussen hin auch
        druck = stiftung * (1.0 - self.rn * 0.55)
        vx = vx * 1.7 + self.ux_rad * druck
        vy = vy * 1.7 + self.uy_rad * druck
        return vx.astype(np.float32), vy.astype(np.float32)

    def einbringen(self, maske, menge=1.0):
        """Farbe hinzufuegen (Maske 0..1 in Gittergroesse)."""
        self.farbe = np.clip(self.farbe + maske * menge, 0, 1.6)

    def schritt(self, t, dt=1.0, stiftung=1.0, diffusion=0.7, zerfall=0.997):
        """Ein Simulationsschritt: transportieren, leicht verlaufen, abklingen."""
        vx, vy = self.geschwindigkeit(t, stiftung)
        # semi-lagrangesch: nachschauen, woher die Farbe kam
        qx = np.clip(self.xx - vx * dt, 0, self.w - 1)
        qy = np.clip(self.yy - vy * dt, 0, self.h - 1)
        self.farbe = np.array(
            map_coordinates(self.farbe, [qy, qx], order=1, mode="constant", cval=0.0),
            np.float32)
        if diffusion:
            self.farbe = gaussian_filter(self.farbe, diffusion)
        self.farbe *= zerfall
