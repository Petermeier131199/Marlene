# Channeling Kongress 2026 – Einblendungen & Übergänge

Grafikpaket für das Kongressvideo mit Vanessa Spaleck, Thema
„Erkenne Deinen Seelenplan", Online-Event 01.–11. November 2026.

Alles in **1920 × 1080, 30 fps**.

Aufgebaut wird intern in 4K und erst beim Ausgeben auf 1080p heruntergerechnet –
das wirkt wie achtfaches Antialiasing, Schrift und Goldlinien bleiben dadurch
sauber. 30 statt 25 fps, weil 60 geteilt durch 30 glatt aufgeht: In einer
60p-Timeline wird jedes Bild gleichmäßig verdoppelt, bei 25 fps würde es
ungleichmäßig ruckeln.

## Dateien

### Overlays (mit Alphakanal – auf eine Spur über dein Video legen)

| Datei | Dauer | Einsatz |
|---|---|---|
| `bauchbinde-vanessa-spaleck.mov` | 8,0 s | Namenseinblendung unten links. Einmal nach ca. 10–20 s, bei langen Videos ein zweites Mal nach einem Kapitelwechsel. |
| `uebergang-lichtbluete.mov` | 1,0 s | Hauptübergang für Kapitelwechsel. |
| `uebergang-atemblende.mov` | 0,6 s | Schnitte innerhalb eines Kapitels. |
| `uebergang-faecher.mov` | 1,2 s | Ihr Lotus-Fächer, sparsam einsetzen – einmal als Höhepunkt. |
| `kapitel-1-bauchbinde.mov` … `kapitel-6-bauchbinde.mov` | je 6,0 s | Themen-Einblendung unten links, für Stellen ohne harten Schnitt. |
| `logo-eck.png` | Standbild | Dezente Dauereinblendung oben rechts. |

### Vollbildkarten (eigener Hintergrund, einfach dazwischenschneiden)

| Datei | Dauer | Einsatz |
|---|---|---|
| `titel-opener.mp4` | 6,5 s | Vorspann: Thema und Speakerin, Kongress-Logo als Absender. |
| `kapitel-1-karte.mp4` … `kapitel-6-karte.mp4` | je 4,5 s | Die sechs Kapitel-Zwischentitel. |
| `schluss-1-nachklang.mp4` | 6,0 s | Schlusskarte eins: ein ruhiger Satz, der nachwirkt. |
| `schluss-2-kontakt.mp4` | 7,0 s | Schlusskarte zwei: wo man sie findet. |

## So platzierst du die Übergänge

Die drei Übergänge sind so gebaut, dass sie **in ihrer Mitte das Bild
vollständig abdecken**. Dadurch funktionieren sie an jedem beliebigen Schnitt,
egal was davor und danach liegt:

1. Schnitt setzen, wo der Wechsel sein soll.
2. Übergang auf die Spur darüber ziehen.
3. Den Clip so schieben, dass **seine Mitte genau auf dem Schnitt liegt**
   (bei der Lichtblüte also 0,5 s davor beginnen).

Mehr ist nicht nötig – keine Maske, kein Blendmodus, keine Deckkraftkurve.

## Format der Overlays

MOV mit PNG-Codec und echtem Alphakanal, verlustfrei. Importiert direkt in
Premiere Pro, DaVinci Resolve und Final Cut. Bei diesen Inhalten ist das
kleiner als ProRes 4444 (gemessen 362 gegen 160 MB an derselben Bauchbinde) –
eine ProRes-Fassung liefere ich auf Zuruf nach.

In 4K/60 lagen dieselben Dateien bei 20 bis 265 MB und damit über dem, was
GitHub annimmt; in 1080p/30 sind es zusammen rund 95 MB.

Falls dein Schnittprogramm Alpha ignoriert und die Overlays schwarz erscheinen:
Interpretation auf „Straight (Unmatted)" bzw. „Alpha-Kanal: Gerade" stellen.

## Gestaltung

Die Bildsprache verbindet beide Marken über ihr gemeinsames Element, die
heilige Geometrie in warmem Gold:

- **Kongress:** Original-Logo, Akzentorange `#C46312`, Saat des Lebens.
- **Vanessa Spaleck:** Original-Wortmarke und Lotus-Fächer aus ihrem Logo,
  Gold `#E0B020` bis `#E8C050`, Hausschrift Runalto.
- **Kleine Zeilen** in einer kräftigen Groteske statt in Runalto: Runalto ist
  eine Display-Schrift, deren Haarstriche unter etwa 40 px Zeilenhöhe
  wegbrechen. Sie liegt damit sogar näher an ihrer Logo-Wortmarke.
- **Gemeinsam:** warmes Schwarz `#141110`, Creme `#F7F1E6`.

### Lesbarkeit auf hellem Bild

Ihr Aufnahmeraum ist hell – weiße Wand, warme Stehlampe. Creme auf Weiß trägt
dort nicht. Die Bauchbinde hat deshalb einen kräftigen, weich auslaufenden
Abdunkler plus einen zweiten, engeren direkt hinter dem Schriftblock, und
Wortmarke, Goldlinie und Rollenzeile liegen auf einem weichen Schatten. Damit
liest sie sich auf hellem wie auf dunklem Hintergrund.

Die Wortmarke wird für dunkle Hintergründe von Schwarz auf Creme umgefärbt;
Fächer und Wortmarke werden über die Farbe voneinander getrennt, weil sich im
Original die unteren Blütenblätter mit der Schrift überlagern.

## Rechte und Quellen

Das Kongress-Logo stammt von der öffentlichen Website
(`Logo_CK26_1080p_final_weiss_Schatten`, 1920 × 427 px). Es wird **nirgends
hochskaliert** – auf der 4K-Fläche liegt es bei maximal 1680 px Breite und
bleibt dadurch scharf. Für die finale Fassung lohnt trotzdem die Nachfrage beim
Veranstalter nach einer Vektordatei.

Ihre Schriften (`Runalto`, `Adorn Story Script`) und beide Logos liegen
bewusst **nicht** im Repository, sondern werden von den Originalquellen geladen:
`./fetch-assets.sh`.

## Neu rendern

```bash
./fetch-assets.sh                 # Logos und Schriften holen
python3 render_ck.py assets/      # alles neu rendern
```

Kapitelkarten mit eigenen Titeln:

```python
import render_ck as R
R.kapitel("Dein Titel hier", "Kapitel 3", "kapitel-03.mp4")
```

## Die sechs Kapitel

| | Kennzeichnung | Titel | Unterzeile |
|---|---|---|---|
| 1 | Kapitel 1 | Was ist der Seelenplan? | – |
| 2 | Kapitel 2 | Was heißt es, ehrlich zu leben? | Authentisch im Sinne deines Seelenplans |
| 3 | Kapitel 3 | Wie findest du deinen Seelenplan? | – |
| 4 | Übung | Alles darf da sein | Wahrnehmen, was gerade ist |
| 5 | Kapitel 5 | Annehmen, was ist | Deine Anteile integrieren und ganz werden |
| 6 | Kapitel 6 | Deine Geistführer | Begleiter durch dein Leben |

Einzeilig passen rund 34 Zeichen auf eine Karte – längere Titel gehören in die
Unterzeile. Titel und Kennzeichnung stehen in `kapitel_alle.py`; nach einer
Änderung dort einfach `python3 kapitel_alle.py` laufen lassen.

Die Themen-Bauchbinde ist bewusst anders aufgebaut als die Namens-Bauchbinde –
Saat des Lebens statt Lotus-Fächer, Titel in Runalto statt Wortmarke – damit
der Zuschauer beide nicht verwechselt, sie aber erkennbar zusammengehören.

## Warum kein Anmeldehinweis

Wer das Video sieht, ist bereits beim Kongress angemeldet. Ein „Jetzt kostenfrei
anmelden" am Ende richtet sich an ein Publikum, das hier gar nicht sitzt. Aus
demselben Grund steht im Vorspann kein Veranstaltungstermin mehr: Der Vorspann
sagt jetzt, worum es in diesem Beitrag geht und wer spricht, der Kongress ist
der Absender oben.

## Die Blume des Lebens und das Licht

Die Blume sass von Anfang an pixelgenau mittig, wirkte aber verrutscht. Grund
war der warme Lichtschein dahinter: Er lag bei 52 bzw. 56 Prozent der Bildhöhe,
die Blume bei 50. Ihre obere Hälfte lag dadurch auf dunklerem Grund als die
untere. `_hintergrund_karte(mitte)` nimmt die Höhe jetzt als Parameter, sodass
Licht und Geometrie konzentrisch liegen – und die Karten setzen beides auf den
optischen Schwerpunkt ihres Textblocks statt auf die geometrische Bildmitte.
