# Etsy-Shop – Strategie & Fahrplan

Ein eigenständiges Projekt. **Keine Verbindung zu anderen Inhalten dieses Vaults** –
eigene Marke, eigenes Thema, eigener Shopname.

| Datei | Inhalt |
|---|---|
| `README.md` | Strategie, Zahlen, 90-Tage-Plan (dieses Dokument) |
| `produkt-ideen.md` | Drei Nischen mit konkreten Produkten und Bewertung |
| `rechtliches-deutschland.md` | Gewerbe, Steuern, Pflichttexte, Lizenzen, KI-Kennzeichnung |
| `listing-vorlage.md` | Copy-&-Paste-Gerüst für jedes Listing |

---

## 1. Die Einsicht, an der die meisten Etsy-Pläne scheitern

**Etsy ist kein Marktplatz für Werkzeuge. Etsy ist ein Geschenke-Marktplatz.**

Das klingt banal und entscheidet trotzdem über alles. Wer auf Etsy sucht, ist in
einer von zwei Stimmungen:

- *„Ich brauche ein Geschenk, das nicht nach Geschenk aussieht."* ← der Großteil
- *„Ich brauche etwas Hübsches für mich."* ← der Rest

Was dort **nicht** passiert: „Ich suche ein gutes Werkzeug zur Kostenkontrolle."
Diese Menschen googeln. Deshalb verkaufen sich Planer und Vorlagen auf Etsy zwar,
aber gegen tausend identische Konkurrenten und im Preiskampf – während
**personalisierte Geschenke** genau die Kaufabsicht treffen, die dort ohnehin
vorhanden ist, und dabei 3–5× so viel kosten dürfen.

Daraus folgt die gesamte Strategie:

> **Hauptmotor: personalisierte, digital ausgelieferte Geschenke – erzeugt per
> Skript, nicht per Hand.**
> **Zweite Säule: deutschsprachige Werkzeuge** als planbares, saisonunabhängiges
> Grundrauschen.

---

## 2. Warum „personalisiert" der einzige haltbare Burggraben ist

Seit 2023 ist jedes Produkt wertlos, das eine KI in 30 Sekunden erzeugen kann. Wall
Art, generische Planer, Zitat-Poster: überflutet, Preise im freien Fall.

Personalisierte Produkte sind aus einem einfachen Grund immun: **Sie existieren vor
der Bestellung noch nicht.** Man kann sie nicht kopieren, nicht stapelweise
hochladen, nicht per Screenshot klauen. Der Wert liegt nicht in der Datei, sondern
im *Erzeugen* der Datei.

Der Haken – und genau hier liegt die Chance:

| | Handarbeit (die meisten Shops) | Skript (dein Weg) |
|---|---|---|
| Aufwand je Bestellung | 10–25 Min. in Canva/Photoshop | 1–2 Min. Daten eintragen, Rest automatisch |
| Bei 5 Bestellungen/Tag | ~2 Stunden Arbeit | ~10 Minuten |
| Bei 30 Bestellungen/Tag | unmöglich nebenbei | unverändert machbar |
| Fehlerquote | steigt mit Müdigkeit | konstant null |
| Qualität | schwankt | identisch |

Deshalb deckeln fast alle personalisierten Shops sich selbst: Der Erfolg erschlägt
sie. Wer den Erzeugungsschritt automatisiert, skaliert linear weiter – und das ist
ein technisches Problem, kein Design-Problem.

**Erste Investition ist also nicht ein Produkt, sondern ein Generator:**

```
generator.py  →  Eingabe: Name, Datum, Ort, Farbwelt
              →  Ausgabe: druckfertige PDFs in 5 Formaten (A4, A3, A2, 30×40, 50×70)
                          + 5 fertige Listing-Mockups
```

Etsy unterstützt das offiziell über **„Made-to-Order"-Digitalartikel**: Der Käufer
zahlt und gibt seine Daten im Personalisierungsfeld ein, du lädst die fertige Datei
danach zur Bestellung hoch. Übliche Lieferzusage: **innerhalb von 24 Stunden** –
realistisch schaffst du 5 Minuten, was regelmäßig 5-Sterne-Bewertungen auslöst.

---

## 3. Was Etsy kostet (Stand 2026)

| Posten | Höhe |
|---|---|
| Einstellgebühr | 0,20 USD je Listing, 4 Monate gültig |
| Transaktionsgebühr | 6,5 % vom Artikelpreis |
| Zahlungsabwicklung (DE) | 4 % + 0,30 € |
| Offsite Ads | unter 10.000 USD Jahresumsatz **abwählbar** – sofort tun; darüber Pflicht (12 %) |

**Bei 18 €:** −1,17 € −1,02 € −0,18 € = **rund 15,60 € netto (87 %)**, ohne
Materialkosten. Das ist der eigentliche Grund, warum digital + personalisiert
funktioniert: Ein 18-€-Verkauf bringt mehr ein als drei 6-€-Verkäufe und macht
weniger Arbeit.

Die MwSt für digitale Downstreams führt Etsy in der EU selbst ab – kein OSS nötig,
solange ausschließlich über Etsy verkauft wird.

**Technische Grenze:** 5 Dateien à 20 MB pro Listing. Für Poster heißt das: PDF mit
eingebetteten Vektoren statt 300-dpi-PNG (ein A2-PNG sprengt die Grenze sofort),
JPEG statt PNG bei Bildinhalten.

---

## 4. Preise – höher ansetzen, als sich richtig anfühlt

| Produkttyp | Spanne | Anmerkung |
|---|---|---|
| Nicht personalisiert, eine Datei | 3–6 € | nur als Einstieg/Köder |
| Bundle, nicht personalisiert | 9–15 € | |
| **Personalisiert, ein Motiv** | **12–25 €** | Kernbereich |
| Personalisiert + Express/mehrere Formate | 25–39 € | |
| Werkzeug mit echtem Rechenwert (Tabelle) | 9–19 € | |

Ein 4-€-Produkt und ein 19-€-Produkt bekommen auf Etsy ungefähr gleich viele Klicks.
Der Preis filtert nicht die Käufer, sondern die Schnäppchenjäger – und genau die
schreiben die schlechten Bewertungen. **Niedrige Preise sind auf Etsy kein
Wettbewerbsvorteil, sondern ein Qualitätssignal nach unten.**

---

## 5. Der 90-Tage-Plan

### Woche 1–2 · Fundament (bevor ein einziges Produkt existiert)
- **Nische festlegen** (siehe `produkt-ideen.md`, Auswahlverfahren in §6 dort).
- **Shopname**: aussprechbar, keine Bindestriche, kein „Shop/Store/DE", nicht zu eng
  am ersten Produkt. Vorher prüfen: Etsy-Suche, DPMA-Markenregister, Domain,
  Instagram-Handle.
- **Gewerbe anmelden** (15–70 €) – vor dem ersten Verkauf.
- **Generator bauen.** Ein Motiv, aber vollständig automatisiert: Eingabe → fertige
  Dateien → fertige Mockups. Lieber zwei Wochen hier als zwei Wochen Design.

### Woche 3–4 · Start mit 8–10 Listings
Nicht mit einem Produkt starten – ein Ein-Listing-Shop wirkt verlassen und
konvertiert nicht. Zehn Listings entstehen aus **einem** Generator, indem man nach
**Anlass** schneidet, nicht nach Motiv:

> dasselbe Motiv als „Geschenk zum Hochzeitstag", „zur Geburt", „zum 18.",
> „zur Silberhochzeit", „zur Einschulung", „zum Renteneintritt", „zum Einzug",
> „zur Erinnerung", „zur Taufe", „zum Jubiläum"

Jedes dieser Listings hat eigene Suchbegriffe, eigene Bilder, eigenen Text – und
kostet dich 20 Minuten statt einer Neuentwicklung. **Das ist der wichtigste
handwerkliche Trick auf Etsy.**

- Etsy Ads mit 1,00 €/Tag auf die drei besten Listings – nicht als Umsatzquelle,
  sondern um überhaupt Daten zu bekommen.
- Offsite Ads abwählen.

### Monat 2 · Messen statt raten
Wöchentlich in die Statistik, und **nur eine Kennzahl gleichzeitig** angehen:

| Symptom | Ursache | Hebel |
|---|---|---|
| wenige Impressionen | SEO | Titel + Tags |
| viele Impressionen, wenige Klicks | erstes Bild | Hero-Mockup |
| viele Klicks, keine Käufe | Preis, Vertrauen, Beschreibung | Beschreibung, Bild 2 + 5, Bewertungen |

- 5–8 neue Listings, davon mindestens 3 auf saisonale Anlässe der **nächsten**
  8 Wochen (Etsy-Käufe laufen der Saison 6–8 Wochen voraus).
- Zweite Säule (Werkzeug) als erstes Produkt vorbereiten.

### Monat 3 · Verdichten
- 25–30 Listings, klare Bestseller erkennbar.
- Bestseller **vertiefen**: Varianten, Formate, Sprachen, Bundle mit zweitem Motiv.
- Erst jetzt Instagram/Pinterest – Pinterest ist für Etsy der bei Weitem
  wirksamere Kanal, weil dort ebenfalls nach Anlässen gesucht wird.

### Die ersten Bewertungen
Ohne Bewertungen kauft kaum jemand, ohne Käufe gibt es keine Bewertungen. Was
legitim wirkt:
- Erste 4–6 Wochen bewusst günstiger einsteigen, danach anheben.
- **Schneller liefern als versprochen** – bei personalisierten Artikeln der stärkste
  Hebel überhaupt.
- Automatische Käufernachricht: *„Wenn etwas nicht passt, schreib mir zuerst, ich
  löse das."* Verhindert mehr 2-Sterne-Bewertungen als jede Bitte 5-Sterne erzeugt.
- **Nie** Bewertungen kaufen oder selbst bestellen. Ein gesperrter Shop ist endgültig.

---

## 6. Erwartungshaltung – ehrlich

- Die ersten 4–8 Wochen passiert fast nichts. Etsy braucht Verkaufssignale, bevor es
  ein Listing überhaupt ausspielt.
- Realistisch: **ab 30–40 guten Listings und 4–6 Monaten** sind 300–800 €/Monat
  erreichbar, wenn die Nische stimmt und die Produkte personalisiert sind. Mit
  reinen Nicht-Personalisierten eher 100–300 €.
- Der erste Dezember ist der Test: Geschenke-Shops machen 30–40 % des Jahresumsatzes
  zwischen Mitte November und Weihnachten. Wer im Januar startet, hat elf Monate
  Anlauf – das ist gut, nicht schlecht.
- Wer „5.000 € passiv in 30 Tagen" verspricht, verkauft einen Kurs darüber.

---

## 7. Langfristig: Etsy ist der Anfang, nicht das Ziel

Etsy gehört der Kunde, nicht dir. Du bekommst Reichweite und zahlst mit
Abhängigkeit – ein Kontoproblem kann alles auf null setzen.

| | Etsy | Eigener Shop (Payhip, Shopify) |
|---|---|---|
| Rolle | Entdeckung, Kaltkunden, Vertrauen über Bewertungen | Marge, Beziehung, Wiederkauf |
| Gebühren | ~11–17 % | ~5 % |
| Risiko | Konto weg = alles weg | gehört dir |

Ab Monat 6 parallel: eigener Shop mit denselben Produkten (Payhip nimmt 5 %, kein
Monatsbeitrag) und **eine E-Mail-Liste**. In jedes ausgelieferte PDF eine letzte
Seite mit echtem Bonus gegen E-Mail-Adresse. Geschenkkäufer kaufen wieder – jedes
Jahr gibt es einen neuen Anlass, und wer einmal zufrieden war, sucht beim nächsten
Mal nicht neu.

---

## 8. Was ich bewusst nicht empfehle

- **Generische Wall Art, Zitat-Poster, „2026 Planner"** – gegen KI-Massenware
  verliert man über den Preis, also gar nicht.
- **KI-Prompt-Bundles** – verstoßen gegen Etsys Creativity Standards.
- **Print on Demand nebenbei** – andere Logistik, andere Retouren. Später, wenn
  digital trägt.
- **Breites Sortiment.** Etsy belohnt thematische Dichte: 20 Listings zu einem Thema
  ranken sich gegenseitig hoch, 20 Listings zu 20 Themen ranken gar nicht.
- **Social Media vor dem Sortiment.** Reichweite ohne Produkte verpufft. Vor
  20 Listings maximal 2 h/Woche.
