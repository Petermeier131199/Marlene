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

## Strukturtest Partikel (`strukturtest-partikel.mp4`)

2 Sekunden, Graustufen, keine Choreografie – nur die Frage, ob die feine
Fadenstruktur der Referenzen überhaupt erreichbar ist.

**Warum ein anderes Verfahren.** Auf einem Gitter transportierte Farbdichte muss
in jedem Schritt weichgezeichnet werden, sonst zerfällt sie in Treppen. Genau
diese Weichzeichnung frisst die feinen Fäden weg – damit entstehen zwangsläufig
Wolken, nie Filigranes. Das war der Grund, warum alle vier Vorversuche
scheitern mussten, unabhängig von den Parametern.

Hier bewegen sich stattdessen 700.000 einzelne Partikel durch ein quellenfreies
Strömungsfeld und werden bei jedem Teilschritt additiv aufgezeichnet. Ein Faden
ist dann die Spur vieler Punkte, die fast denselben Weg nehmen.

**Drei Erkenntnisse aus den Durchgängen:**

Ein kleiner Fleck in einem groben Feld *wandert nur*. Dehnung braucht
Geschwindigkeitsunterschiede über die Wolke hinweg – also entweder eine große
Wolke oder ein feines Feld.

Ohne zufälliges Zittern der Partikel (molekulare Diffusion) bleibt der Rand der
Wolke eine geschlossene Linie: Das Ergebnis sieht nach Marmorpapier aus, nicht
nach Tinte.

Länglich gesät statt als Scheibe, mit anhaltendem Drift, ergibt das Band der
Referenzen statt einer Wolke, die sich an Ort und Stelle kringelt.

## Markensequenz „Der Punkt" (`signatur-punkt-und-faecher.mp4`)

3,9 Sekunden auf cremeweißem Grund, in ihren Farben – Blau und ihr Gelb.
Vollbild, kein Alphakanal nötig: vorne und hinten überblenden, fertig.

**Ablauf.** Ein blaues Band zieht von links oben herein, ein gelbes von rechts
unten. Beide laufen auf einen Punkt zu, verdichten sich – und aus diesem Punkt
fächert alles nach oben auf, in **dreizehn Blättern**, abwechselnd blau und
gelb. So viele Blätter hat der Fächer in ihrem Logo. Die Bewegung zeichnet ihr
Zeichen, ohne dass ein Logo zu sehen ist.

**Zwei Entscheidungen, die technisch erzwungen waren:**

*Die Blätter greifen ineinander, statt übereinanderzuliegen.* Die Farben werden
nach dem Absorptionsgesetz auf den hellen Grund gerechnet – Tinte auf Papier
schluckt Licht, sie strahlt nicht. Blau schluckt Rot, Gelb schluckt Blau; liegen
beide am selben Ort, schlucken sie zusammen alles Licht und der Fächer wird
schwarz. Abwechselnde Blätter lösen das Problem und sehen zugleich besser aus.

*Der Fächer ist ein eigener Ausbruch, kein weitertransportiertes Band.* Tinte
sieht nur deshalb nach Tinte aus, weil sie zerläuft – ein lesbarer Fächer
braucht aber scharfe Strahlen. Transportiert man die Bänder weiter, zerstreut
die Diffusion den Fächer, bevor er zu sehen ist. Der Ausbruch ist schnell genug,
um ihr davonzulaufen, und wird dann abgebremst. Die Übergabe verbirgt eine
Überblendung von drei Zehntelsekunden.
