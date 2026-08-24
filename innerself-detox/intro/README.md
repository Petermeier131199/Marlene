# Innerself Detox – Video-Intro (5 Sekunden)

Animiertes Intro auf Basis von Konzept 2 (Golden Hour). Der Hintergrund ist echtes
bewegtes Material: Kerze flackert, Rauch steigt auf und loest sich auf, Vorhang
atmet, Kamera steht still. Der Titel ist als echte Textebene darueber gerechnet und
dadurch gestochen scharf.

## Dateien

| Datei | Inhalt |
|---|---|
| `innerself-detox-intro-1080p-30fps.mp4` | Intro, 1920x1080, 30 fps, 5,00 s, ohne Ton |
| `innerself-detox-intro-1080p-25fps.mp4` | dieselbe Animation in 25 fps (deutsche Schnitt-Timeline) |
| `intro-endbild.png` | letzter Frame als Standbild - zugleich die Titelbild-Variante mit korrekt konstruierter Blume des Lebens |
| `cleanplate-ohne-schrift.png` | Hintergrundbild ohne jede Schrift, fuer weitere Varianten |

## Ablauf (Atemrhythmus)

| Zeit | Was passiert |
|---|---|
| 0,0–1,3 s | nur die Szene: Kerze flackert, Rauch steigt, ganz langsames Heranfahren |
| 1,3–2,9 s | Titel taucht Buchstabe fuer Buchstabe aus der Unschaerfe auf und treibt dabei leicht nach oben – wie vom Rauch getragen |
| 2,6–3,5 s | Goldlinien ziehen aus der Mitte nach aussen |
| 2,7–4,1 s | Blume des Lebens glimmt einmal sanft auf (Ausatmen), Subline blendet nach |
| 4,1–5,0 s | Halten auf dem vollen Titel, Rauch zieht ruhig weiter |

Das Heranfahren laeuft ueber die gesamten 5 s von 104,5 % auf 100 % – bewusst so
langsam, dass man es kaum bemerkt.

## Weiterverwenden

Beide Dateien sind stumm, du legst deine Musik im Schnittprogramm darunter. Der
Schluss haelt still, du kannst also hart schneiden oder selbst ueberblenden.

Neu rendern (z. B. mit anderem Untertitel oder anderer Laenge):

    python3 render.py <hintergrund.mp4|standbild.png> <ausgabe.mp4>

Texte, Farben und Positionen stehen in `titleart.py`, das Timing oben in
`render.py`. Benoetigt Pillow, numpy und imageio-ffmpeg.

## Blume des Lebens

Die Blume des Lebens wird als Vektor gezeichnet, nicht aus dem Bild uebernommen:
19 gleich grosse Kreise im Sechseckraster mit Mittelpunktsabstand r, sodass jeder
Kreis durch die Mittelpunkte seiner Nachbarn laeuft - nur so entstehen die echten
Bluetenblaetter. Aussen zwei duenne Begrenzungsringe bei 3r. Siehe
`titleart.flower_of_life()`.
