# Muster für den langen Übergang

Drei Entwürfe, gleiche Aura-Farbwelt (Gold, Rosé, Violett, Türkis, Licht),
unterschiedliche Bewegung. Je 4,5 Sekunden, Alphakanal, Volldeckung in der
Mitte. Nicht für den Schnitt gedacht, sondern zum Ansehen und Auswählen.

| Datei | Bewegung |
|---|---|
| `muster-a-aura-atem.mov` | Das Licht blüht aus der Fläche auf, hält, geht zurück. |
| `muster-b-aurasaum.mov` | Das Licht kommt von allen vier Rändern herein und schließt sich. |
| `muster-c-aurazug.mov` | Ein Lichtschleier zieht sehr langsam von unten nach oben durch. |
| `muster-d-tinte-im-wasser.mov` | 5,0 s: Tinte berührt die Wasseroberfläche und sinkt in Fäden nach unten. Ihre Farbwelt: Gelb als Farbe, Blau nur als Licht. |

## Warum keine Strömungssimulation mehr

Die beiden verworfenen Versuche haben Farbe durch ein Strömungsfeld
transportiert. Transport erzeugt zwangsläufig Wirbel, und Wirbel lesen sich als
Unruhe – genau der Kritikpunkt. Hier bewegt sich nichts durch das Bild: Es sind
große, weiche Lichtfelder, die langsam atmen, ihre Mittelpunkte kaum merklich
verschieben und in eigener Phase schimmern (`aura.py`). Optisch fast
Stillstand, trotzdem lebendig.

## Muster D: Tinte im klaren Wasser

Gedacht als Markensequenz für alle ihre Videos, nicht nur für den Kongress –
deshalb ohne Kongress-Orange, allein in ihren Farben (Gelb `#E7B428`, Blau
`#2F5AAE`, aus dem Stylesheet ihrer Website).

Drei Dinge unterscheiden es von den drei verworfenen Versuchen:

**Es fließt nach unten.** Alle Vorversuche breiteten sich aus – radial, seitlich,
atmend. Schwerkraft ist eine einzige, gleichbleibende Richtung, und genau das
macht sie ruhig. Transport war nie das Problem, Turbulenz war es.

**Das Wasser bleibt klar.** Das Bild ist über vier Fünftel der Laufzeit
sichtbar; nur um die Mitte herum verdichtet sich die Farbe kurz zu einer
geschlossenen Fläche, damit die Sequenz auch einen Schnitt tragen kann.

**Es gibt einen Berührungspunkt.** Die Farbe kommt oben herein, an drei Stellen,
nicht mittig und nicht symmetrisch – dort, wo der Pinsel das Wasser berührt.

Das Wirbelfeld in `tinte.py` ist bewusst schwach gehalten: Ohne jede
Verwirbelung bleiben glatte Säulen statt Fäden, mit zu viel wird es unruhig.
Die Schwerkraft ist rund fünfmal stärker als der Wirbel.
