# Konzept: Auftragskunst aus persönlichen Daten

Arbeitsstand des Brainstormings. Grundhaltung: **lieber wenige Produkte, dafür
solche, die heraussstechen.**

---

## 1. Der Einwand zuerst: „Meine Geschenke waren für eine Person gedacht"

Der Einwand ist richtig – und er löst sich auf, sobald man zwischen zwei Dingen
trennt:

| | Was verkauft würde | Fühlt sich an wie |
|---|---|---|
| **Das Rezept** | „Mein Adventskalender für X, zum Nachbauen" | Ausverkauf einer Erinnerung |
| **Die Handschrift** | Das *Format* und das Gespür, mit dem so etwas entsteht | Handwerk, das man anbietet |

Die Bridgerton-Zeitung ist nicht „das Geschenk für X". Sie ist ein **Format**:
*ein persönlicher Brief, getarnt als fiktives Dokument.* Das Format gehört dir, die
Ausführung gehört jedes Mal einem anderen Menschen. Niemand bekommt je dasselbe
Stück – genau wie bisher.

Die Konsequenz für das Geschäftsmodell: **Auftragsarbeit statt Produktkopie.**
Jeder Käufer bekommt wieder ein Unikat. Was verkauft wird, ist der Blick darauf.

---

## 2. Human-Design-Poster – Prüfung

### Machbarkeit: besser als gedacht
Die Chart-Berechnung ist vollständig deterministisch (Planetenpositionen zur Geburt
plus Sonnenbogen von 88 Tagen davor, abgebildet auf die 64 Tore). Dafür existieren
freie Python-Bibliotheken auf Basis der Swiss Ephemeris (u. a. `human-design-py`,
MIT-Lizenz, gegen bodygraph.io verifiziert).

**Der Datenschritt kostet also Sekunden, nicht Stunden.** Was Arbeit macht, ist
allein die künstlerische Übersetzung – und genau die ist der Wert.

### Recht: der Punkt, den man kennen muss
„The Human Design System", „Rave BodyGraph" und „Rave Mandala" sind eingetragene
Marken von Jovian Archive. Daraus folgt:

- **Nicht** das offizielle BodyGraph-Diagramm nachbauen oder verwenden.
- **Nicht** als Shop- oder Markenname verwenden („Human Design Studio" ≠ gute Idee).
- Beschreibend darf man sagen, worauf das Bild beruht („nach deinen Geburtsdaten,
  inspiriert von deinem Human-Design-Chart"). Als **Suchbegriff** in Tags ist das
  beschreibende Nutzung – üblich, aber kein rechtsfreier Raum. Vor dem Start einmal
  fachlich prüfen lassen.
- Keine Wirkungs-, Heil- oder Zukunftsaussagen. Es ist Kunst und Selbstreflexion,
  nichts weiter.

**Die gute Nachricht:** Der eigene Anspruch – *es soll nicht sofort „Human Design"
schreien, sondern als Kunstbild funktionieren* – ist gleichzeitig die saubere
rechtliche Lösung. Je weiter das Bild vom offiziellen Diagramm weg ist, desto
unproblematischer und desto besser verkauft es sich.

### Positionierung: der eigentliche Vorteil
Ein Bild, das man aufhängen kann, **ohne sich zu erklären**, hat einen viel größeren
Markt als ein Esoterik-Poster:
- Es ist verschenkbar an Menschen, die mit dem Thema nichts anfangen.
- Es passt in ein Wohnzimmer, in dem sonst kein Chart hängen würde.
- Es wird nicht über den Preis verglichen, weil es kein Vergleichsprodukt gibt.

### Das Problem: Aufwand pro Stück
2 Stunden Arbeit für 25 € sind 12,50 € Stundenlohn – vor Gebühren und Steuern. Das
ist kein Nebenverdienst, das ist ein teures Hobby. Drei Auswege:

| Weg | Preis | Aufwand/Stück | Anmerkung |
|---|---|---|---|
| **A – Premium-Auftrag** | 79–149 € | 1,5–3 h | Wenige Plätze im Monat, bewusst limitiert |
| **B – Parametrisches System** | 29–49 € | 10–20 Min. | Erfordert, dass die Gestaltungsregeln in Code stehen |
| **C – Preisleiter** | 29 / 89 / 149 € | gestaffelt | Günstige Stufe bringt Bewertungen, teure den Umsatz |

**Empfohlene Reihenfolge: erst A, dann B.** Zuerst 8–10 Stück von Hand verkaufen –
dabei zeigt sich, welche Gestaltungsentscheidungen jedes Mal gleich getroffen werden.
Genau die werden danach zu Regeln im Generator. Wer zuerst die Maschine baut, baut
regelmäßig die falsche.

### Parametrisch denken (Notizen für später)
Aus den Chart-Daten lassen sich gestalterische Parameter ableiten, ohne das Diagramm
zu zeigen: definierte Zentren → Gewicht und Dichte der Komposition; Kanäle → Linien
und Verbindungen; Typ → Grundform; Profil → Bildaufteilung; Autorität → Farbwelt.
Das Ergebnis ist dann für jede Person nachweislich anders, ohne dass man es
„lesen" muss.

---

## 3. Weitere Formate in derselben Handschrift

Nicht alles bauen. Als Auswahl fürs Brainstorming:

| Idee | Kern | Aufwand/Stück | Preis |
|---|---|---|---|
| **Die fiktive Zeitung** | Persönlicher Brief, getarnt als Titelseite – Verlobung, 50. Geburtstag, Abschied in den Ruhestand | hoch (Text!) | 49–129 € |
| **Das historische Dokument** | Telegramm, Urkunde, Theaterprogramm, Speisekarte *dieses einen Abends* | mittel–hoch | 39–89 € |
| **Datenkunst-Poster** | Human Design, Geburtsdaten, gemeinsame Zeitachse – abstrakt übersetzt | mittel | 29–149 € |
| **Adventskalender-System** | **Nicht** der gefüllte Kalender, sondern die druckbare Vorlage + 24 Textimpulse, damit der Käufer *seinen eigenen* Brief schreibt | einmalig | 12–19 € |
| **„Ein Jahr in Briefen"** | 12 Umschlagvorlagen + Schreibimpulse, monatlich zu öffnen | einmalig | 14–19 € |

**Die Zeitung ist der stärkste unfaire Vorteil.** Sie verlangt nicht Design, sondern
**Schreiben** – und genau daran scheitern die anderen. Auf Etsy gibt es fertige
Zeitungs-Templates zuhauf, aber kaum jemanden, der den Text dazu schreiben kann.

**Das Adventskalender-System ist der wirtschaftliche Gegenpol**: einmal gebaut,
unbegrenzt verkaufbar, Saison September–November, und es gibt genau das weiter, was
gefragt war – das Gespür, nicht das fertige Geschenk.

---

## 4. Die Shop-Struktur, die daraus folgt

Zwei Ebenen, ein Handschrift:

| | Auftragsarbeit | Vorlagen |
|---|---|---|
| Beispiele | Zeitung, Dokument, Datenkunst-Poster | Adventskalender-System, Briefjahr |
| Preis | 49–149 € | 12–19 € |
| Menge | 4–10 pro Monat, limitiert | unbegrenzt |
| Rolle | Umsatz und Handschrift | Sichtbarkeit, Bewertungen, Reichweite |

Die Vorlagen ziehen Käufer an und erzeugen die Bewertungen, ohne die niemand
149 € bei einem unbekannten Shop ausgibt. Die Auftragsarbeiten machen den Umsatz.

**Limitierung offen kommunizieren** („4 Plätze im Monat") ist kein Marketingtrick,
sondern Selbstschutz: Sie hält die Qualität oben, den Preis oben und verhindert,
dass aus Freude Fließbandarbeit wird.

---

## 5. Offene Fragen

1. Schreibst du gern? (Entscheidet Zeitung vs. reine Bildkunst.)
2. Wie viele Stunden pro Monat sollen Aufträge bekommen? (Entscheidet Preis und
   Platzzahl.)
3. Kennst du Human Design gut genug, um es glaubwürdig zu übersetzen – oder ist es
   für dich eine Formsprache, kein Weltbild? (Beides ist tragfähig, aber es
   verändert die Texte.)
4. Bilder der bisherigen Geschenke: daraus lässt sich die Handschrift ableiten
   (Farben, Typografie, Tonfall) und als Hausstil festschreiben.
