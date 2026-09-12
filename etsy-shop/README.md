# Etsy-Shop – Strategie & Fahrplan

Neuer Bereich im Vault. Ziel: ein **digitaler Nebenverdienst**, der zu dem passt,
was hier ohnehin schon entsteht – und der nicht nach zwei Monaten tot ist.

| Datei | Inhalt |
|---|---|
| `README.md` | Strategie, Zahlen, 90-Tage-Plan (dieses Dokument) |
| `produkt-ideen.md` | Konkrete Produkte, nach Umsetzbarkeit sortiert |
| `rechtliches-deutschland.md` | Gewerbe, Steuern, Pflichttexte, KI-Kennzeichnung |
| `listing-vorlage.md` | Copy-&-Paste-Gerüst für jedes Listing (Titel, Tags, Bilder) |

---

## 1. Die ehrliche Ausgangslage

Was hier schon liegt, ist mehr wert als die meisten Etsy-Shops am Tag eins haben:

- **Ein fertiges 15-seitiges PDF** („Hühner halten leicht gemacht") plus Checkliste –
  das ist ein verkaufsfertiges Produkt, kein Konzept.
- **Eine visuelle Handschrift**, die trägt: warme Herbstpalette, Cormorant/Montserrat,
  Goldlinien, Blume des Lebens. Das ist eine Marke, auch wenn sie noch nicht so heißt.
- **Eine Render-Pipeline in Python** (`cards.py`, `titleart.py`, `thumbnail.py`).
  Das ist der eigentliche unfaire Vorteil – dazu unten mehr.
- **Fachwissen aus zwei Richtungen**: Hühnerhaltung (belegt, geprüft, ehrlich) und
  Finanzen (beruflich).

Und ebenso ehrlich, damit die Erwartung stimmt:

- Etsy ist bei „printable planner" und „wall art" **maßlos überlaufen** und seit 2023
  mit KI-Massenware geflutet. Wer dort hineinverkauft, verkauft nichts.
- Die ersten 4–8 Wochen passiert fast nichts. Etsy braucht Verkaufssignale, bevor es
  ein Listing überhaupt ausspielt.
- Realistisch: **ab ca. 30–40 guten Listings** und 4–6 Monaten Arbeit sind
  100–400 €/Monat erreichbar. Alles darüber ist möglich, aber nicht planbar.
- Wer dir „5.000 € passiv in 30 Tagen mit Etsy-Printables" verkauft, verkauft dir
  genau das: einen Kurs darüber.

Der Weg, der funktioniert, ist der langweilige: **enge Nische + echte Expertise +
Tiefe statt Masse.**

---

## 2. Die Kernstrategie: „schmal, tief, deutsch"

Drei Entscheidungen, die alles andere bestimmen.

### Entscheidung 1 – Nische statt Sortiment

Nicht „digitale Produkte" verkaufen, sondern **eine Zielperson** bedienen, bis der
Shop bei ihr die erste Adresse ist. Drei Säulen kommen infrage (Details in
`produkt-ideen.md`):

| Säule | Zielperson | Warum sie trägt |
|---|---|---|
| **A – Hühner & Selbstversorgung** | Familie mit Garten, 3–6 Hühner, will nichts falsch machen | Produkt existiert, echte Expertise, kaufkräftig, wenig KI-Müll, stark saisonal planbar |
| **B – Haushalt & Finanzen (deutsch)** | Paare 25–45, Haushaltsbuch, Sparziele | Deutscher Markt deutlich dünner besetzt als der englische; deine Berufsexpertise |
| **C – Ritual & Journaling (Innerself Detox)** | Marlenes künftige Kurskäuferinnen | Baut die Marke auf und füttert den Kurs – Etsy als Zubringer, nicht als Hauptbühne |

**Empfehlung: Start mit A.** Nicht weil es das größte Feld ist, sondern weil dort
in 14 Tagen das erste Produkt online sein kann und weil „Hühnerhaltung" von
KI-Generalisten kaum bedient wird – dafür braucht man echtes Wissen. B ist die
zweite Säule ab Monat 3. C läuft parallel, aber mit anderem Ziel (siehe §6).

### Entscheidung 2 – Tiefe statt Breite

Ein Shop mit **einer** klar erkennbaren Welt schlägt drei halbe Shops. Etsy-SEO
belohnt thematische Dichte: 20 Listings rund um Hühner ranken sich gegenseitig hoch,
20 Listings über 20 Themen ranken gar nicht.

Falls A und B beide laufen sollen: **zwei getrennte Shops** unter einem Konto. Nicht
mischen. Ein Shop, der Hühnerställe *und* Finanzplaner verkauft, wirkt wie ein
Flohmarkt.

### Entscheidung 3 – Der technische Vorteil wird ausgespielt

Das ist der Teil, den 95 % der Etsy-Verkäufer nicht können: Ihr rendert Produkte
**programmatisch**. Daraus folgen Dinge, die manuell unbezahlbar wären:

- **Variantenmaschine**: Ein Ritual-Planer in 6 Farbwelten × 3 Formaten (A4, US Letter,
  iPad/GoodNotes) = 18 Dateien aus einem Skript. Manuell: zwei Tage. Bei euch: ein
  Nachmittag Code, danach Sekunden.
- **Mockups automatisiert**: Die Listing-Bilder entscheiden über den Klick. Ein
  Skript, das jedes PDF in dieselben 5 Mockup-Rahmen setzt (Schreibtisch, Rahmen an
  der Wand, iPad, Detailausschnitt, Übersichtsraster), macht jedes neue Produkt in
  Minuten verkaufsfertig – und gibt dem Shop einen wiedererkennbaren Look.
- **Personalisierung als Preis-Hebel**: Ein Planer mit Namen/Jahreszahl darf 3× so
  viel kosten wie ein anonymer. Der Aufwand ist bei euch eine Zeile Text im Render.
- **Serienfähigkeit**: Jahreswechsel, Jubiläen, neue Sprachen – alles Neurendern
  statt Neuentwerfen.

Konkret zu bauen: `mockup.py` – nimmt ein PDF/PNG und spuckt 5 fertige
Listing-Bilder im Haus-Look aus. **Das ist die erste Investition, nicht das dritte
Produkt.**

---

## 3. Was Etsy wirklich kostet (Stand 2026)

Pro Listing und Verkauf:

| Posten | Höhe |
|---|---|
| Einstellgebühr | 0,20 USD je Listing, gilt 4 Monate (bzw. bei jedem Verkauf neu) |
| Transaktionsgebühr | 6,5 % vom Artikelpreis |
| Zahlungsabwicklung (DE) | 4 % + 0,30 € |
| Offsite Ads | unter 10.000 USD Jahresumsatz **abwählbar**; darüber Pflicht (12 %) |
| Etsy Ads (freiwillig) | Tagesbudget, frei wählbar |

**Rechenbeispiel 8,00 €:** −0,52 € Transaktion −0,62 € Zahlung −0,18 € Einstellung
= **rund 6,70 € netto (≈ 83 %)**. Bei digitalen Produkten ohne Materialkosten ist das
komplett Deckungsbeitrag. Wichtig: Offsite Ads gleich am Anfang abwählen, sonst
reißen einzelne Verkäufe 15 % zusätzlich.

**Die MwSt für digitale Downloads führt Etsy in der EU selbst ab** – du musst dich
nicht um OSS/MOSS kümmern, solange du ausschließlich über Etsy verkaufst. (Beim
eigenen Shop später sieht das anders aus, siehe `rechtliches-deutschland.md`.)

### Die harte technische Grenze

**Maximal 5 Dateien pro Listing, je 20 MB.** Das ist die Regel, an der die meisten
scheitern:

- PDFs mit eingebetteten Fotos sprengen 20 MB schnell → Bilder auf 150 dpi für
  Bildschirm / 300 dpi nur für Druckseiten, JPEG statt PNG im PDF.
- Der Hühner-Ratgeber liegt aktuell bei **3,3 MB** – passt bequem. Gut so.
- **Videos gehen auf Etsy nicht.** Der Innerself-Detox-Kurs kann dort nicht
  ausgeliefert werden (dazu §6).
- Auslieferung per Link auf Google Drive/Dropbox: bringt schlechte Bewertungen und
  ist ein Politik-Risiko. Lieber das Produkt kleiner schneiden.

---

## 4. Shop aufsetzen – die Reihenfolge, die Zeit spart

1. **Gewerbe anmelden** (15–70 €, online in vielen Kommunen). Vor dem ersten Verkauf,
   nicht danach. Details in `rechtliches-deutschland.md`.
2. **Shopname** festlegen. Kriterien: aussprechbar, keine Bindestriche, kein
   „Shop/Store/DE" angehängt, **nicht** zu eng am ersten Produkt (sonst blockiert er
   die zweite Säule). Vorher prüfen: Etsy-Suche, Handelsregister/DPMA, Domain,
   Instagram-Handle. Nachträgliches Umbenennen geht auf Etsy nur einmal frei.
3. **Shop anlegen**, Sprache Deutsch, Währung EUR, Land Deutschland.
4. **Sofort in den Einstellungen:** Offsite Ads deaktivieren (solange erlaubt),
   Urlaubsmodus kennen, Shop-Richtlinien und Impressum eintragen.
5. **Nicht mit einem Listing starten.** Mit **8–10 Listings** am selben Tag online
   gehen. Ein Ein-Produkt-Shop wirkt verlassen und konvertiert nicht.
6. Erst danach: Etsy Ads mit **1,00 €/Tag** auf die drei besten Listings – nicht als
   Umsatzquelle, sondern um überhaupt Daten (Impressionen, Klickraten) zu bekommen.

### Die ersten Bewertungen – das eigentliche Startproblem

Ohne Bewertungen kauft kaum jemand; ohne Käufe gibt es keine Bewertungen. Was
legitim funktioniert:

- **Startpreis bewusst niedrig** (3–5 €) für die ersten 4–6 Wochen, danach anheben.
  Nicht dauerhaft billig bleiben – Preis signalisiert Qualität.
- **Eine Extra-Datei mehr liefern, als das Listing verspricht** („Bonus: Legekalender").
  Kostet nichts, erzeugt 5 Sterne.
- **Nach dem Kauf eine kurze, persönliche Nachricht** (Etsy erlaubt eine automatische
  Käufernachricht). Kein Bettelbrief um Bewertungen – sondern: „Wenn etwas nicht
  passt, schreib mir zuerst, ich löse es." Das verhindert die 2-Sterne-Bewertungen.
- **Verboten und riskant:** Bewertungen kaufen, sich selbst bestellen. Etsy erkennt
  das, und ein gesperrter Shop ist endgültig.

---

## 5. Der 90-Tage-Plan

### Woche 1–2 · Fundament
- Gewerbe anmelden, Shopname prüfen und sichern, Etsy-Konto anlegen.
- `mockup.py` bauen (5 Listing-Bilder aus einer Quelldatei im Haus-Look).
- Hühner-Ratgeber in ein verkaufsfertiges **Bundle** umbauen: Ratgeber-PDF +
  Ausstattungs-Checkliste + Stallplaner + Legekalender (4 Dateien, alle < 20 MB).

### Woche 3–4 · Start mit 8–10 Listings
Aus einem Thema werden zehn Listings, indem man es zerlegt statt wiederholt:
Komplettpaket, Ratgeber einzeln, Checkliste einzeln, Jahreskalender, Futterplan,
Stallplan-Vorlage, Anfänger-Quickstart (1 Seite, 3 €), Winter-Spezial,
Küken-Aufzucht, Notfall-Übersicht (Krankheiten/Tierarzt). Jedes einzeln kaufbar,
das Bundle 2,5× so teuer wie ein Einzelteil.

- Preise: Einzelnes 3–5 €, Bundle 9–14 €.
- Etsy Ads 1 €/Tag, nur zur Datengewinnung.

### Monat 2 · Messen statt raten
- Wöchentlich in die Etsy-Statistik: **Impressionen** (= SEO wirkt) vs.
  **Klickrate** (= Bild/Titel wirken) vs. **Conversion** (= Preis/Beschreibung wirken).
  Jede Kennzahl zeigt auf eine andere Baustelle. Nie alles gleichzeitig ändern.
- Titel und Tags der 3 schwächsten Listings überarbeiten (siehe `listing-vorlage.md`).
- 5–8 neue Listings, davon 2 *personalisiert* (höherer Preis).
- E-Mail-Sammlung starten: In jede PDF eine letzte Seite mit einem echten Bonus gegen
  E-Mail-Adresse. **Das ist langfristig das Wertvollste am ganzen Shop.**

### Monat 3 · Verdichten und zweite Säule
- Zweite Säule (B – Finanzen) als **eigener Shop** vorbereiten, wenn A trägt.
- Saisonales einplanen: Etsy-Käufe laufen der Saison **6–8 Wochen voraus**.
  Küken/Frühjahr → ab Januar listen. Weihnachten → ab Oktober.
- Ziel Ende Monat 3: 25–30 Listings, erste Wiederkäufer, bekannte Bestseller.

---

## 6. Langfristig: Etsy ist der Anfang, nicht das Ziel

Etsy gehört der Kunde, nicht dir. Du bekommst Reichweite und zahlst dafür mit
Abhängigkeit. Deshalb von Anfang an zweigleisig:

| | Etsy | Eigener Kanal |
|---|---|---|
| Rolle | Entdeckung, Kaltkunden, Vertrauen durch Bewertungen | Marge, Beziehung, große Dateien, Kurse |
| Gebühren | ~17 % | ~5 % (Payhip/Digistore24/CopeCart/elopage) |
| Risiko | Konto weg = alles weg | gehört dir |

**Der Innerself-Detox-Kurs gehört nicht auf Etsy** – Videos lassen sich dort nicht
ausliefern, und ein 100-€-Kurs neben 5-€-Printables wirkt falsch. Stattdessen:

- Kurs auf **elopage / Digistore24 / CopeCart** (deutsch, MwSt und Rechnungen
  automatisch, Reseller-Modell nimmt dir die Steuerthemen ab).
- Auf Etsy laufen die **kleinen Türöffner** derselben Welt: Ritual-Journal,
  30-Tage-Workbook, Affirmationskarten, Blume-des-Lebens-Print. 5–12 €, gleiche
  Farbwelt, gleiche Typografie.
- In jedem dieser Produkte: letzte Seite → E-Mail-Liste → später Kursangebot.
  Etsy bezahlt die Kundengewinnung, der Kurs macht den Umsatz.

Das ist das eigentliche Geschäftsmodell. Der Etsy-Shop allein ist ein netter
Nebenverdienst; Etsy **plus E-Mail-Liste plus eigener Kurs** ist der Unterschied
zwischen 200 € und 2.000 € im Monat.

---

## 7. Was ich bewusst nicht empfehle

- **Das Essverhalten-Thema zu monetarisieren.** Das Video ist stark, weil es nichts
  verkauft. Ein „Journal zur Essstörung" auf Etsy wäre rechtlich heikel
  (Heilversprechen, HWG), ethisch fragwürdig und würde rückwirkend das Video
  beschädigen. Finger weg – das ist Haltung, nicht Vorsicht.
- **KI-Prompt-Bundles.** Verstoßen gegen Etsys Creativity Standards.
- **Massen-Wall-Art und generische „2026 Planner".** Dort konkurrierst du mit
  Tausenden identischer KI-Listings und gewinnst über den Preis – also gar nicht.
- **Print on Demand nebenbei.** Andere Logistik, andere Retouren, anderer Shop.
  Später, wenn digital steht.
- **Mehr als 2 Stunden pro Woche in Social Media**, bevor 20 Listings online sind.
  Reichweite ohne Sortiment verpufft.
