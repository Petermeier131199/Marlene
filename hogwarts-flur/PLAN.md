# Hogwarts im Flur — Projektplan Wandtapete

Stand: 18.08.2026 · Ziel: Blick durch einen gotischen Torbogen auf ein Hogwarts-inspiriertes Schloss, als individuell gedruckte Vliestapete über die komplette Flurwand.

---

## 1. Maße & Bestellgröße

Gemessene Teilstücke (von links nach rechts):

| Segment | Breite |
|---|---|
| Wandstück links | 10 cm |
| Tür links | 80 cm |
| **Mittelteil (Torbogen-Motiv)** | **243 cm** |
| Tür rechts | 80 cm |
| Wandstück rechts | 16 cm |
| **Summe** | **429 cm** |

Höhe: **230 cm** (Oberkante Fußleiste/Fliese bis Decke). Türen: 80 × 200 cm.

**⚠️ Mess-Diskrepanz:** Die Teilstücke ergeben 429 cm, deine Angabe „ca. 4,5 m" bzw. die Skizze (98 + 243 + 118 = 459 cm) weichen davon ab. Vermutlich sind in der Skizze die Türzargen mit drin, in den 80 cm nur das Türblatt. **Vor der Bestellung: Gesamtlänge einmal am Stück messen** (oben an der Decke UND unten an der Fußleiste — das größere Maß zählt), Höhe an drei Stellen (links, Mitte, rechts).

**Bestellmaß-Empfehlung:** Gesamtmaß + 5–10 cm Zugabe in beide Richtungen, also z. B. **460 × 240 cm** (bei bestätigten 450 cm Länge). Die Türen werden NICHT vorher ausgeschnitten — man bestellt das volle Rechteck und schneidet vor Ort am Türrahmen ab. Der „Verschnitt" von ~3,2 m² ist normal und einkalkuliert.

## 2. Pixelrechnung (die Kernfrage)

Formel: `Pixel = (cm ÷ 2,54) × dpi`. Faustregel: **100 dpi ≈ 40 px/cm, 150 dpi ≈ 60 px/cm.**

Für einen Flur (Betrachtungsabstand oft unter 1,5 m) gilt:
- **150 dpi** = Referenzqualität, gestochen scharf auch aus 50 cm
- **100–120 dpi** = sehr gut, im Alltag nicht von 150 dpi zu unterscheiden
- **unter 80 dpi** = wird aus der Nähe sichtbar weich (bei > 3 m Abstand okay, im Flur nicht)

### Mittelteil (Torbogen + Schloss), 243 × 230 cm

| Qualität | Pixelmaß | Megapixel |
|---|---|---|
| 150 dpi (optimal) | 14.350 × 13.580 px | ~195 MP |
| 120 dpi (Ziel) | 11.480 × 10.870 px | ~125 MP |
| 100 dpi (Minimum) | 9.570 × 9.060 px | ~87 MP |

### Gesamtwand, Bestellmaß 460 × 240 cm

| Qualität | Pixelmaß | Megapixel |
|---|---|---|
| 150 dpi | 27.170 × 14.170 px | ~385 MP |
| 120 dpi | 21.730 × 11.340 px | ~246 MP |
| 100 dpi | 18.110 × 9.450 px | ~171 MP |

**Ziel: Masterdatei der Gesamtwand mit 100–120 dpi (ca. 18.000–21.700 px breit), das Bogen-Motiv im Mittelteil möglichst Richtung 120–150 dpi.** Die Steinflächen links/rechts/über den Türen sind unkritisch — Steintextur verzeiht niedrigere Detaildichte und kann aus nativ hochauflösenden, kachelbaren Texturen aufgebaut werden.

Dateiformat für den Druck: JPG in maximaler Qualität oder TIFF, Farbraum sRGB. Manche Anbieter wollen die Datei im Maßstab 1:10 — steht jeweils in deren Druckdaten-Vorgaben.

## 3. Motivkonzept

Basis sind deine beiden Vorschau-Bilder (Tag / Nacht):

- **Komposition:** 3 gotische Spitzbögen mit Säulen im 243-cm-Mittelteil; das Schloss im mittleren/rechten Bogen (dorthin fällt der Blick beim Betreten), See und Wald in den äußeren Bögen für Tiefe.
- **Tiefenillusion:** Balustrade mit Läufer unten (wie in deiner Nacht-Version) verankert den Blick und macht den „Fenster-Effekt" glaubwürdiger. Fluchtpunkt auf Augenhöhe (~155–160 cm über Boden).
- **Lichtstimmung — Empfehlung Abenddämmerung/goldene Stunde:** Die Nacht-Version ist die atmosphärischste, macht den fensterlosen Flur aber real dunkler. Dämmerung mit warm erleuchteten Schlossfenstern holt beides: Magie + Helligkeit. Finale Entscheidung liegt bei dir — Tag, Dämmerung, Nacht.
- **Steuerung der Ränder:** Links/rechts der Bögen und über den Türen läuft ruhige Steinmauer-Textur weiter. Im Bereich Lichtschalter/Steckdosen (rechte Seite) ruhige Fläche einplanen, damit die Ausschnitte nicht auffallen. Optional: Schalter-/Steckdosenrahmen gegen Bronze-/Antik-Optik tauschen (15–30 €).
- **Laterne:** Die Wandlaterne aus deinem Nacht-Mockup geht ohne Elektrik — Akku-/Batterie-LED-Wandlaterne (30–60 €).
- **Rechtlicher Hinweis:** Ein „originalgetreues" Hogwarts (Filmvorlage 1:1) ist urheberrechtlich geschützt — Druckdienste lassen dich bei Upload bestätigen, dass du die Rechte hast, und können exakte Filmkopien ablehnen. Ein *angelehntes* Fantasy-Schloss (wie in deinen Mockups) für private Nutzung ist unproblematisch. Je „originalgetreuer" der Bruder zeichnet, desto mehr gilt: nur privat nutzen, nicht veröffentlichen/verkaufen.

## 4. Weg zur Druckdatei

### Plan A: KI-Generierung + Upscaling (empfohlen als Basis)

Direkt „druckfertig aus Higgsfield" geht **nicht** — KI-Generatoren liefern 1–4 MP, Higgsfield-Upscale bis 4K (~4.100 px). 4.100 px auf 243 cm = nur ~43 dpi. Der Workflow:

1. **Motiv generieren** (Higgsfield/Firefly o. ä.), mehrere Varianten, im ~1:1-Format fürs Mittelteil. Malerischer/illustrativer Stil — der übersteht Upscaling deutlich besser als Fotorealismus.
2. **Erste Stufe hochskalieren** auf 4K (Higgsfield `upscale`).
3. **Zweite Stufe: AI-Upscaler auf Zielgröße** — Topaz Gigapixel AI (~99 €, Referenz) oder Upscayl (kostenlos, Open Source): 4.100 px × 3–4× → 12.000–16.000 px. ✔️
4. **Montage der Masterdatei** (Krita/Affinity/Photoshop): Mittelteil-Motiv + nativ hochauflösende Steintextur für die Randflächen + ggf. Balustrade in eine Datei mit 18.000–21.700 px Gesamtbreite setzen. Maßstabskontrolle: Tür-Ausschnittpositionen einzeichnen.
5. **Qualitätskontrolle:** Einen 50 × 50 cm-Ausschnitt in Originalauflösung als Poster/Testdruck drucken lassen (~5–15 €) und aus 1 m Abstand prüfen — bevor 300+ € für die Tapete fällig werden.

### Plan B: Bruder zeichnet digital

Machbar, aber die Leinwand muss stimmen: **1:1 bei 120 dpi = 11.480 × 10.870 px** fürs Mittelteil (Krita oder Photoshop, ab 16–32 GB RAM okay). Alternativ auf 50 % malen (5.700 × 5.400 px) und am Ende 2× hochskalieren — bei gemaltem Stil praktisch verlustfrei.

### Plan A+B (beste Qualität): Hybrid

KI-Bild generieren und hochskalieren, dann übermalt/verfeinert der Bruder die kritischen Details (Fensterlichter, Turmkanten, Steinstruktur der Bögen) auf der fertigen Auflösung. So bekommt ihr KI-Komposition + handwerkliche Schärfe genau da, wo man hinschaut.

## 5. Anbieter & Kosten

Fläche: ~460 × 240 cm = **~11 m²**. Alle drucken eigene Motive auf Vlies (Latex-Druck, geruchsneutral, „paste the wall").

| Anbieter | Preisniveau | Bemerkung |
|---|---|---|
| [wir-machen-druck.de](https://www.wir-machen-druck.de/foto-tapete-extrem-guenstig-drucken,category,15140.html) | ~€ (ab ~10–20 €/m²) | Günstigster Weg, solide Qualität |
| [fototapeten24.net](https://www.fototapeten24.net/) | ab 17 €/m² | Budget-Alternative |
| [digitaldruck-fabrik.de](https://www.digitaldruck-fabrik.de/plakate-poster/fototapete.aspx) | €€ | Kämmerer-Vlies 150 g/m² |
| [A.S. Création / tapetenshop.de](https://www.tapetenshop.de/service-und-beratung/service/individuelle-fototapete/) | ab ~30 €/m² | Markenhersteller, bis 2000 × 350 cm |
| [Bilderwelten.de](https://www.bilderwelten.de/fototapeten) | €€€ | Premium, on-demand in DE gefertigt |
| [Photowall.de](https://www.photowall.de) | €€€ (Pauschale/m², Kleister inkl.) | **Empfehlung:** 30-Tage-Rückgabe auch bei eigenem Motiv + Maßanfertigung, sehr gute Anleitungen |
| [Rebel Walls](https://rebelwalls.com/de/tapeten) | €€€ | Zufriedenheitsgarantie, kostenloser Versand |

**Kostenrahmen gesamt:**

| Posten | Budget | Premium |
|---|---|---|
| Tapete ~11 m² | 190–250 € | 350–480 € |
| Testdruck-Poster | 10 € | 15 € |
| Kleister, Tiefgrund, Werkzeug | 40–60 € | 40–60 € (bei Photowall Kleister inkl.) |
| Optional: LED-Laterne + Antik-Schalterrahmen | — | 50–90 € |
| **Summe** | **~250–320 €** | **~450–650 €** |

## 6. Anbringen — was zu bedenken ist

**Untergrund (1–2 Tage vorher):** Auf dem Foto sind Schrammen/Flecken zu sehen → Macken verspachteln, anschleifen, dann **pigmentierten (weißen) Tapeziergrund** streichen. Grund: gleichmäßige Saugfähigkeit + keine durchscheinenden Farbunterschiede, und die Tapete lässt sich später rückstandsfrei ablösen. Wand muss trocken, fest, fett- und staubfrei sein.

**Logistik:** Vliestapete kommt in nummerierten Bahnen (meist 50–100 cm breit). Wandklebetechnik: Kleister auf die Wand rollen, trockene Bahn einlegen — zu zweit arbeiten. Raumklima 18–22 °C, keine Zugluft, Trocknung 24 h.

**Schritt für Schritt:**
1. Strom aus → Schalter-/Steckdosenabdeckungen im Motivbereich abschrauben.
2. Lot-/Laserlinie für die erste Bahn (nicht auf den Türrahmen als „Senkrechte" verlassen).
3. Bahn für Bahn nach Nummerierung; je nach Anbieter stumpf auf Stoß oder mit Überlappung + **Doppelnahtschnitt** (beide Bahnen gleichzeitig mit Cutter am Lineal durchtrennen → unsichtbare Naht).
4. Mit Tapezierroller/-bürste von der Mitte nach außen blasenfrei andrücken.
5. **Türen:** Bereich übertapezieren, dann am Türrahmen mit scharfem Cutter + breitem Spachtel als Führung sauber abschneiden. Immer frische Klingen!
6. **Steckdosen:** übertapezieren, nach dem Antrocknen kreuzweise einschneiden und ausschneiden, Abdeckungen wieder montieren.
7. Überstände an Decke und Fußleiste zum Schluss am Spachtel abschneiden.

**Werkzeugliste:** Vlieskleister + Rolle, Tapezierbürste/Andrückroller, Nahtroller, Cutter + Ersatzklingen, breiter Spachtel (Schneidführung), Lineal/Wasserwaage oder Laser, Bleistift, Leiter, sauberer Schwamm.

Zeitbedarf reine Tapezierarbeit: zu zweit ein halber Tag.

## 7. Nächste Schritte

1. **Du:** Gesamtlänge + Höhe final nachmessen (s. o.), Lichtstimmung entscheiden (Tag/Dämmerung/Nacht), Budgetklasse wählen.
2. **Wir:** Motiv-Varianten generieren (Bögen, Blickwinkel, Licht) → Favorit wählen.
3. Upscaling + Masterdatei bauen, Türpositionen einzeichnen.
4. Testdruck 50 × 50 cm bestellen und prüfen.
5. Tapete bestellen (Lieferzeit meist 3–7 Werktage).
6. Wand vorbereiten, Wochenend-Termin zum Tapezieren, Laterne + Schalterrahmen montieren. ✨

### Offene Fragen an dich

1. Ergibt die Kontrollmessung 429, 450 oder 459 cm? (Und Höhe wirklich überall 230 cm?)
2. Lichtstimmung: Tag, **Abenddämmerung (meine Empfehlung)** oder Nacht?
3. Balustrade + Läufer unten im Motiv: ja/nein?
4. Budget- oder Premium-Anbieter?
5. Soll ich direkt erste Motiv-Varianten mit Higgsfield generieren?
