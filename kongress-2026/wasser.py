"""Farbschleier im Wasser - mehrere Farben, die ineinander verlaufen.

Der Unterschied zum ersten Versuch liegt in zwei Punkten:

* Es gibt mehrere Farbfelder statt einem. Eine einzige Dichte, die durch einen
  Farbverlauf gejagt wird, sieht immer nach Feuer aus - Farben mischen sich erst
  dann sichtbar, wenn sie getrennt transportiert und am Ende gewichtet
  zusammengerechnet werden.
* Es gibt keinen radialen Druck aus der Mitte. Der war die schnelle, unruhige
  Geste. Stattdessen treiben die Schleier in grossen, traegen Wirbeln und
  bewegen sich auf dem Einatmen leicht zueinander, auf dem Ausatmen auseinander.
"""
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter


class Wasser:
    def __init__(self, breite, hoehe, saat=11):
        self.w, self.h = breite, hoehe
        self.rng = np.random.default_rng(saat)
        yy, xx = np.mgrid[0:hoehe, 0:breite].astype(np.float32)
        self.xx, self.yy = xx, yy
        cx, cy = breite / 2.0, hoehe / 2.0
        dx, dy = xx - cx, yy - cy
        r = np.hypot(dx, dy) + 1e-6
        self.ux, self.uy = dx / r, dy / r
        self.rn = (r / np.hypot(cx, cy)).astype(np.float32)
        # nur grosse Skalen: kleine Wirbel wirken sofort hektisch
        self.pot = [self._potential(sk) for sk in (150, 78)]
        self.felder = []          # Liste (farbe, dichtefeld)

    def _potential(self, skala):
        klein = self.rng.normal(0, 1, (max(4, self.h // skala), max(4, self.w // skala)))
        gross = np.array(map_coordinates(
            klein,
            [np.clip(self.yy / skala, 0, klein.shape[0] - 1),
             np.clip(self.xx / skala, 0, klein.shape[1] - 1)],
            order=3, mode="reflect"), np.float32)
        return gaussian_filter(gross, skala * 0.4)

    def schleier(self, farbe, mitte, groesse, dichte=1.0, unruhe=0.55):
        """Weicher Farbschleier: eine Wolke, kein Tropfen."""
        cx, cy = mitte
        rx, ry = groesse
        d = np.exp(-(((self.xx - cx) / rx) ** 2 + ((self.yy - cy) / ry) ** 2))
        if unruhe:
            stoer = gaussian_filter(self.rng.normal(0, 1, (self.h, self.w)).astype(np.float32), 26)
            stoer /= np.abs(stoer).max() + 1e-6
            d = d * (1.0 + unruhe * stoer)
        self.felder.append([np.array(farbe, np.float32), np.clip(d, 0, None) * dichte])

    def _geschwindigkeit(self, t, atem):
        vx = np.zeros((self.h, self.w), np.float32)
        vy = np.zeros((self.h, self.w), np.float32)
        for i, pot in enumerate(self.pot):
            gy, gx = np.gradient(pot)
            gew = (1.0, 0.42)[i] * (1.0 + 0.25 * np.sin(t * 1.4 + i * 2.0))
            vx += gy * gew
            vy += -gx * gew
        vx /= np.abs(vx).max() + 1e-6
        vy /= np.abs(vy).max() + 1e-6
        # Atem: leicht zur Mitte (einatmen) bzw. nach aussen (ausatmen)
        vx = vx * 1.45 - self.ux * atem * (0.35 + 0.65 * self.rn)
        vy = vy * 1.45 - self.uy * atem * (0.35 + 0.65 * self.rn)
        return vx, vy

    def schritt(self, t, atem, dt=1.0, verlaufen=0.9, zerfall=0.998):
        vx, vy = self._geschwindigkeit(t, atem)
        qx = np.clip(self.xx - vx * dt, 0, self.w - 1)
        qy = np.clip(self.yy - vy * dt, 0, self.h - 1)
        for eintrag in self.felder:
            f = np.array(map_coordinates(eintrag[1], [qy, qx], order=1,
                                         mode="nearest"), np.float32)
            eintrag[1] = gaussian_filter(f, verlaufen) * zerfall

    def bild(self):
        """Farben gewichtet mischen; gibt (rgb, dichte) zurueck."""
        summe = np.zeros((self.h, self.w), np.float32)
        rgb = np.zeros((self.h, self.w, 3), np.float32)
        for farbe, d in self.felder:
            summe += d
            rgb += d[..., None] * farbe
        rgb /= (summe[..., None] + 1e-6)
        return rgb, summe
