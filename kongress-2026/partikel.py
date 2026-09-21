"""Partikelstroemung fuer seidige Faeden.

Warum ueberhaupt ein anderes Verfahren: Auf einem Gitter transportierte
Farbdichte muss in jedem Schritt weichgezeichnet werden, sonst zerfaellt sie in
Treppen. Genau diese Weichzeichnung frisst die feinen Faeden weg - mit dieser
Technik entstehen zwangslaeufig Wolken, nie Filigranes.

Hier bewegen sich stattdessen hunderttausende einzelne Punkte durch ein
Stroemungsfeld und werden additiv aufgezeichnet. Ein Faden ist dann die Spur
vieler Punkte, die fast denselben Weg nehmen. Die Feinheit kommt aus der
Partikelzahl, nicht aus der Aufloesung des Feldes - das Feld darf und soll
glatt sein, sonst wird es unruhig.
"""
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter, zoom


class Stroemung:
    """Quellenfreies Stroemungsfeld aus mehreren Rauschskalen."""

    def __init__(self, breite, hoehe, skalen=((26, 1.0), (12, 0.42), (6, 0.15)),
                 saat=1, gitter=6):
        self.w, self.h = breite, hoehe
        self.g = gitter                      # Feld in Gitterpunkten je g Pixel
        gw, gh = breite // gitter, hoehe // gitter
        rng = np.random.default_rng(saat)
        self.paare = []
        for skala, gew in skalen:
            felder = []
            for _ in range(2):               # zwei Phasen zum Ueberblenden
                k = rng.normal(0, 1, (max(4, gh // skala), max(4, gw // skala)))
                p = zoom(k, (gh / k.shape[0], gw / k.shape[1]), order=3)
                p = gaussian_filter(p, skala * 0.5).astype(np.float32)
                gy, gx = np.gradient(p)
                # Rotation des Potentials: quellenfrei, also keine Punkte, an
                # denen Partikel verschwinden oder aus dem Nichts auftauchen
                n = max(np.abs(gy).max(), np.abs(gx).max()) + 1e-6
                felder.append((gy / n, -gx / n))
            self.paare.append((felder, gew))

    def geschwindigkeit(self, x, y, phase):
        """Feld an den Partikelpositionen abtasten."""
        gx = np.clip(x / self.g, 0, self.w // self.g - 1)
        gy = np.clip(y / self.g, 0, self.h // self.g - 1)
        vx = np.zeros_like(x)
        vy = np.zeros_like(y)
        mischen = 0.5 + 0.5 * np.sin(phase)
        for felder, gew in self.paare:
            for f, anteil in ((felder[0], mischen), (felder[1], 1.0 - mischen)):
                if anteil < 1e-3:
                    continue
                vx += gew * anteil * map_coordinates(f[0], [gy, gx], order=1, mode="nearest")
                vy += gew * anteil * map_coordinates(f[1], [gy, gx], order=1, mode="nearest")
        return vx, vy


class Wolke:
    """Eine Partikelwolke, die sich im Feld zu Faeden zieht."""

    def __init__(self, anzahl, breite, hoehe, saat=2):
        self.w, self.h = breite, hoehe
        self.rng = np.random.default_rng(saat)
        self.x = np.zeros(0, np.float32)
        self.y = np.zeros(0, np.float32)
        self.gew = np.zeros(0, np.float32)
        self.anzahl = anzahl

    def saeen_fleck(self, mitte, radius, anzahl=None, streuung=1.0):
        """Partikel in einem weichen Fleck aussetzen."""
        n = anzahl or self.anzahl
        r = radius * np.sqrt(self.rng.random(n)) ** streuung
        a = self.rng.random(n) * 2 * np.pi
        self.x = np.concatenate([self.x, (mitte[0] + r * np.cos(a)).astype(np.float32)])
        self.y = np.concatenate([self.y, (mitte[1] + r * np.sin(a)).astype(np.float32)])
        # leicht unterschiedliche Helligkeit erzeugt die Streifung in den Faeden
        self.gew = np.concatenate([self.gew,
                                   (0.45 + 0.55 * self.rng.random(n)).astype(np.float32)])

    def bewegen(self, feld, phase, tempo, drift=(0.0, 0.0), dt=1.0, zittern=0.0):
        """Ein Teilschritt. `zittern` ist die molekulare Diffusion.

        Ohne dieses Zittern bleibt der Rand der Wolke eine geschlossene Linie -
        das Ergebnis sieht nach Marmorpapier aus, nicht nach Tinte. Erst der
        zufaellige Anteil franst die Raender zu Schleiern aus.
        """
        vx, vy = feld.geschwindigkeit(self.x, self.y, phase)
        self.x += (vx * tempo + drift[0]) * dt
        self.y += (vy * tempo + drift[1]) * dt
        if zittern:
            n = self.x.size
            self.x += self.rng.normal(0, zittern, n).astype(np.float32)
            self.y += self.rng.normal(0, zittern, n).astype(np.float32)


def auftragen(puffer, wolke, breite, hoehe, anteil=1.0):
    """Eine Wolke additiv in einen flachen Puffer legen.

    bincount statt add.at: beide summieren Wiederholungen am selben Index auf,
    bincount ist dabei rund zehnmal schneller. Aufgetragen wird bei jedem
    Teilschritt - nur dadurch entsteht eine durchgehende Spur statt einer
    Punktwolke.
    """
    xi = np.clip(wolke.x, 0, breite - 1.001).astype(np.int32)
    yi = np.clip(wolke.y, 0, hoehe - 1.001).astype(np.int32)
    puffer += np.bincount(yi * breite + xi, weights=wolke.gew * anteil,
                          minlength=hoehe * breite).astype(np.float32)


def fertig(puffer, breite, hoehe, weichzeichnen=0.55):
    bild = puffer.reshape(hoehe, breite)
    return gaussian_filter(bild, weichzeichnen) if weichzeichnen else bild
