# „Über Essen und über mich" – Einblender für das 40-Minuten-Video

Vier Elemente für den Schnitt in Final Cut Pro. Alles 1920×1080, 25 fps, stumm.

## Dateien

| Datei | Länge | Wofür |
|---|---|---|
| `out/titelkarte.mp4` | 4,0 s | Titelkarte – kommt **nach** dem gesprochenen Einstieg |
| `out/triggerwarnung.mov` | 6,0 s | Bauchbinde **mit Alphakanal**, liegt über dem laufenden Bild |
| `out/zwischenblende.mp4` | 3,6 s | überbrückt die Lücke in der Aufnahme |
| `out/abbinder.mp4` | 11,0 s | Anlaufstellen, ganz am Schluss |
| `out/*-vorschau.png` | – | je ein Standbild zum schnellen Draufschauen |
| `out/triggerwarnung.mp4` | 6,0 s | nur zur Ansicht (ohne Alphakanal, **nicht** für den Schnitt) |

Die Vollbildkarten liegen als H.264 vor – bei flächigen Grafiken ist das visuell
gleichwertig zu ProRes und rund 25× kleiner. Nur die Bauchbinde braucht ProRes
4444, weil H.264 keinen Alphakanal transportiert. Wenn deine Timeline trotzdem
durchgehend ProRes will: `PRORES=1 python3 cards.py`.

## Aufbau des Videos

Die Reihenfolge ist bewusst so – dein gesprochener Einstieg („mich mal richtig
nackig machen … seelisch, nicht körperlich") ist das Stärkste, was das Video hat.
Alles, was davorsteht, verbrennt ihn. Deshalb kein Vorspann.

| Position | Element |
|---|---|
| 0:00 | **Kalter Start.** Kein Logo, kein Titel. Deine Worte, sofort. |
| während deiner gesprochenen Triggerwarnung | `triggerwarnung.mov` als Überlagerung, unten links |
| direkt danach, wenn der Einstieg abgeschlossen ist | `titelkarte.mp4` |
| an der Lücke | `zwischenblende.mp4` |
| ganz am Ende | `abbinder.mp4` |

Die Triggerwarnung ist damit dreifach abgesichert – gesprochen, eingeblendet und
in der Videobeschreibung –, ohne den Einstieg zu verraten.

## In Final Cut Pro

1. Alle Dateien aus `out/` in die Mediathek importieren (Datei → Importieren → Medien).
2. **Vollbildkarten** (`titelkarte`, `zwischenblende`, `abbinder`) auf die
   Hauptspur ziehen, an die gewünschte Stelle. Sie blenden selbst auf und ab –
   also **keine** zusätzliche Blende (kein ⌘T) darüberlegen, sonst wird es doppelt
   weich.
3. **Bauchbinde** (`triggerwarnung.mov`) eine Spur **über** dem Video ablegen,
   an die Stelle, an der du die Warnung aussprichst. Der Alphakanal wird
   automatisch erkannt, es ist nichts einzustellen.
4. **Zwischenblende:** die kaputten Sekunden herausschneiden, die Karte in die
   Lücke setzen. Wichtig ist der Ton – siehe unten.

### Ton an der Zwischenblende

Da an der Stelle Bild **und** Ton fehlen, entsteht sonst ein Loch. Zwei
Möglichkeiten, in dieser Reihenfolge:

- **Musik**, die schon vorher leise unter dem Gespräch liegt, über der Karte kurz
  aufblüht und danach wieder zurückgeht. Trägt die Lücke am unauffälligsten.
- **Raumton**: 3–4 Sekunden Stille aus deiner eigenen Aufnahme (eine Stelle, an
  der du nicht sprichst) kopieren und unter die Karte legen. Absolute digitale
  Stille klingt wie ein Aussetzer, echter Raumton nicht.

Nur schneiden und nichts darunterlegen wirkt wie ein Fehler – genau das, was die
Karte vermeiden soll.

## Text der Karten

- **Titelkarte:** ÜBER ESSEN / UND ÜBER MICH — *Seelisch. Nicht körperlich.*
- **Bauchbinde:** TRIGGERWARNUNG — *Körperbild · gestörtes Essverhalten*
- **Zwischenblende:** *Hier haben mich ein paar Sekunden verlassen. / Die Kamera, meine ich.*
- **Abbinder:** Beratungstelefon Essstörungen 0221 892031 · TelefonSeelsorge
  0800 111 0 111 und 116 123 · im Notfall 112

Die Nummern sind in Montserrat gesetzt, nicht in Cormorant: Cormorant hat
Mediävalziffern, in denen eine 1 wie ein I aussieht – bei einer Hilfenummer nicht
vertretbar.

## Farbwelt

Aus einem Standbild des Videos abgeleitet, damit die Karten nicht gegen den Raum
schlagen: helle Wand, helle Eiche, der Goldrahmen im Hintergrund, der braune
Ledersessel, das Burgunder im Blumenstrauß.

| Farbe | Hex | Verwendung |
|---|---|---|
| Cremiges Off-White | `#F1EBE3` | Grund der Karten |
| Tiefes Warmbraun | `#3B342E` | Schrift |
| Gold | `#B08A4A` | Haarlinien, Kleinversalien |
| Burgunder | `#8C3A38` | einziger Akzent: Hilfenummern, „Triggerwarnung" |
| Zurückgenommenes Grau | `#7C7064` | Nebenzeilen |

Typografie: Cormorant Garamond (Titel, Fließzeilen), Montserrat (Kleinversalien,
Ziffern). Beide von Google Fonts, frei lizenziert (OFL).

## Neu rendern

Voraussetzungen: Python 3, `pip install pillow numpy imageio-ffmpeg`, dazu die
beiden Schriften in `fonts/` (nicht im Repository, OFL – frei herunterladbar):

    mkdir -p fonts
    curl -L -o fonts/CormorantGaramond.ttf \
      "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf"
    curl -L -o fonts/Montserrat.ttf \
      "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"

Dann:

    python3 cards.py                      # alle vier
    python3 cards.py zwischenblende       # nur eine
    FPS=30 python3 cards.py               # andere Bildrate
    PRORES=1 python3 cards.py             # zusaetzlich ProRes-.mov fuer alle

Texte, Farben und Timing stehen oben in `cards.py`, jede Karte in einer eigenen
Funktion.

## YouTube-Thumbnail

`thumbnail.py` rendert 1280×720 im gleichen Look. Drei Textvarianten:

| Datei | Zeile | Bemerkung |
|---|---|---|
| `out/thumbnail-c-ehrlich.jpg` | 40 MINUTEN **EHRLICH.** | **Empfehlung** – nennt die Länge, verspricht nichts Falsches |
| `out/thumbnail-a-nackig.jpg` | SEELISCH **NACKIG.** | stärkster Haken, aber siehe unten |
| `out/thumbnail-b-titel.jpg` | ÜBER ESSEN UND ÜBER MICH | ruhig; wiederholt allerdings nur den Titel |

Zu Variante a: „nackig" neben diesem Thema zieht Klicks an, die niemandem
nützen – dieselbe Überlegung, aus der der Videotitel nicht so heißt. Die
Unterzeile fängt es ab, aber die Entscheidung liegt bei dir.

Ein Thumbnail mit Gesicht schlägt reine Schrift auf YouTube deutlich – es wird
auf dem Handy briefmarkengroß gesehen. Sobald du ein Standbild hast:

    python3 thumbnail.py --foto standbild.png --fokus 0.62 --seite links

`--fokus` verschiebt den Ausschnitt waagerecht (0 = links, 1 = rechts) und
entscheidet, wo dein Gesicht landet; `--seite` sagt, auf welcher Hälfte die
Schrift steht – das Gesicht gehört auf die andere. Ein cremefarbener Verlauf
legt sich über die Textseite, damit die Schrift ruhigen Untergrund bekommt.

Ziffern werden in Montserrat gesetzt und auf die Versalhöhe der Cormorant
skaliert – aus demselben Grund wie beim Abbinder.

## Veröffentlichen

Instagram scheidet für 40 Minuten aus – Reels gehen bis 3 Minuten, längere
Uploads gibt es dort seit dem Ende von IGTV nicht mehr.

Empfohlener Weg:

1. **YouTube-Kanal** anlegen (kostenlos, mit jedem Google-Konto) und das Video
   zunächst als **„nicht gelistet"** hochladen: es hat dann eine Adresse zum
   Teilen, taucht aber in keiner Suche und in keinen Empfehlungen auf. Später
   mit einem Klick auf öffentlich stellen.
2. **Kommentare abschalten** (Einstellungen → Community). Bei diesem Thema keine
   Kleinigkeit.
3. **Instagram als Zubringer**: 30–60 Sekunden Ausschnitt als Reel, Link im
   Profil oder in der Story.
4. **Alternative Vimeo** (ab ca. 7 €/Monat), falls dir stört, dass YouTube neben
   deinem Video eigene Empfehlungen ausspielt. Vimeo tut das nicht.

### Videobeschreibung

Fertig zum Kopieren in `youtube-beschreibung.txt`. Aufbau und Begründung:

- **Die ersten zwei Zeilen sind die Triggerwarnung.** YouTube zeigt nur rund
  drei Zeilen, alles weitere steckt hinter „…mehr" und wird kaum gelesen. Eine
  Warnung, die man aufklappen muss, ist keine.
- Danach erst der Text, der zum Schauen einlädt.
- **Die Anlaufstellen stehen über den Kapiteln**, nicht ganz unten. Wer sie
  braucht, sucht sie nicht.
- **Kapitel** brauchen mindestens drei Zeitmarken, und die erste muss `0:00`
  sein – sonst zeigt YouTube gar keine an. Die Platzhalter musst du mit
  echten Zeitmarken füllen.
- **Instagram-Link** ganz unten, nicht oben: oben würde er von der Warnung
  ablenken.

Angaben zum Beratungstelefon geprüft über
[essstoerungen.bioeg.de](https://essstoerungen.bioeg.de/hilfe-finden/welche-beratung-gibt-es/telefonberatung/)
(Bundesinstitut für Öffentliche Gesundheit, vormals BZgA).
