const pptxgen = require('pptxgenjs');
const sharp = require('sharp');
const path = require('path');

const P = '/home/user/Marlene/poleschak-social-media';
const IMG = path.join(__dirname, 'img');
const OUT = path.join(P, 'praesentation', 'poleschak-social-media-masterplan.pptx');

const C = { or: 'EB5A1B', orH: 'FF7F22', rost: '722C0D', nacht: '111111', anth: '222222', grau: '545559', silber: 'B4B5BB', hell: 'F4F4F4', weiss: 'FFFFFF', panel: 'E9E9EA' };
const F = { xb: 'Poppins ExtraBold', sb: 'Poppins SemiBold', md: 'Poppins Medium', rg: 'Poppins', lt: 'Poppins Light' };
const W = 13.333, H = 7.5, M = 0.75;

const LOGO_NEG = `${P}/assets/logo-negativ.png`;
const LOGO_POS = `${P}/assets/logo-transparent.png`;
const LOGO_R = 381 / 745;
const V = (n) => `${P}/vorlagen/export/${n}.png`;
const ic = (n, c = 'w') => `${IMG}/${n}-${c}.png`;

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Social Media · Alarmanlagen Poleschak';
pres.title = 'Social-Media-Masterplan Alarmanlagen Poleschak';

let pageNo = 0;

// ---------- helpers ----------
function base(dark, bg) {
  const s = pres.addSlide();
  pageNo++;
  s.background = { color: bg || (dark ? C.nacht : C.weiss) };
  return s;
}
function kicker(s, text, dark, x = M, y = 0.55, col) {
  const dot = col ? C.nacht : C.or;
  s.addShape(pres.shapes.OVAL, { x, y: y + 0.07, w: 0.16, h: 0.16, fill: { color: dot }, line: { color: dot } });
  s.addText(text.toUpperCase(), { x: x + 0.28, y, w: 9, h: 0.3, margin: 0, fontFace: F.lt, fontSize: 12, charSpacing: 5, color: col || (dark ? C.silber : C.grau), isTextBox: true });
}
function title(s, runs, dark, opts = {}) {
  const arr = typeof runs === 'string' ? [{ text: runs }] : runs;
  s.addText(arr.map(r => ({ text: r.text, options: { color: r.o ? C.or : (dark ? C.weiss : C.nacht), breakLine: r.br } })), {
    x: M, y: opts.y || 0.95, w: opts.w || 11.8, h: opts.h || 0.9, margin: 0, fontFace: F.xb, fontSize: opts.size || 34, valign: 'top', isTextBox: true,
  });
}
function footer(s, dark) {
  const h = 0.36;
  s.addImage({ path: dark ? LOGO_NEG : LOGO_POS, x: M, y: H - 0.62, w: h / LOGO_R, h });
  s.addText(String(pageNo).padStart(2, '0'), { x: W - M - 1, y: H - 0.55, w: 1, h: 0.3, margin: 0, align: 'right', fontFace: F.lt, fontSize: 11, charSpacing: 3, color: dark ? C.silber : C.grau, isTextBox: true });
}
function iconCircle(s, icon, x, y, d = 0.62, fill = C.or, iconColor = 'w') {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill } });
  const p = d * 0.26;
  s.addImage({ path: ic(icon, iconColor), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p });
}
function txt(s, text, o) {
  s.addText(text, Object.assign({ margin: 0, fontFace: F.rg, fontSize: 14, color: C.anth, valign: 'top', isTextBox: true }, o));
}
function card(s, x, y, w, h, fill = C.hell) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill } });
}
function bullets(s, items, o, color = C.anth, size = 14) {
  // eigene Aufzählung mit Signal-Punkt: robust in PowerPoint und LibreOffice
  const lh = size * 1.4 / 72, cpi = 72 / (size * 0.56);
  let y = o.y;
  items.forEach(t => {
    const runs = typeof t === 'string' ? [{ text: t }] : t;
    const len = runs.reduce((a, r) => a + r.text.length, 0);
    const lines = Math.max(1, Math.ceil(len / ((o.w - 0.3) * cpi)));
    const h = lines * lh + 0.04;
    s.addShape(pres.shapes.OVAL, { x: o.x, y: y + lh / 2 - 0.05, w: 0.1, h: 0.1, fill: { color: C.or }, line: { color: C.or } });
    s.addText(runs.map(r => ({ text: r.text, options: { bold: !!r.b, color: r.o ? C.or : color } })), { x: o.x + 0.25, y, w: o.w - 0.25, h, margin: 0, fontFace: F.rg, fontSize: size, valign: 'top', isTextBox: true });
    y += h + 0.12;
  });
}

(async () => {
  const igMeta = await sharp(`${IMG}/ig-mockup.png`).metadata();

  // ================= 1 TITEL =================
  {
    const s = base(true);
    s.addImage({ path: `${IMG}/waves.png`, x: 8.4, y: 1.0, w: 5.2, h: 5.2 });
    kicker(s, 'Social-Media-Masterplan · Instagram', true, M, 0.7);
    s.addImage({ path: LOGO_NEG, x: M, y: 1.45, w: 1.35 / LOGO_R, h: 1.35 });
    s.addText([
      { text: 'Wir sind wach,', options: { color: C.weiss, breakLine: true } },
      { text: 'damit du ', options: { color: C.weiss } },
      { text: 'schlafen', options: { color: C.or } },
      { text: ' kannst.', options: { color: C.weiss } },
    ], { x: M, y: 3.2, w: 8.2, h: 2.1, margin: 0, fontFace: F.xb, fontSize: 50, valign: 'top', isTextBox: true });
    txt(s, 'Vorschlag für die Geschäftsführung · 07.10.2026 · [Dein Name]', { x: M, y: 6.55, w: 9, h: 0.35, fontSize: 14, color: C.silber });
    s.addNotes('Einstieg: Der Claim ist die Idee in einem Satz. Unsere Leitstelle ist nachts wach, und genau das zeigen wir auf Instagram. In den nächsten 20 Minuten zeige ich, wie wir damit Kunden und neue Kolleginnen und Kollegen gewinnen und was es kostet.');
  }

  // ================= 2 AUSGANGSLAGE =================
  {
    const s = base(false);
    kicker(s, 'Ausgangslage', false);
    title(s, [{ text: 'Die Nische ist ' }, { text: 'frei.', o: true }], false);
    const it = [['FaMagnifyingGlass', 'Kaum sichtbar', 'In der Region nutzt noch kein Sicherheitstechnik-Betrieb Instagram konsequent.'], ['FaUsers', 'Ohne feste Zuständigkeit', 'Unser Kanal hat aktuell niemanden, der ihn regelmäßig betreut.'], ['FaStar', 'Starker Ruf, wenig gezeigt', 'Kunden sind zufrieden, aber online sieht man davon kaum etwas.'], ['FaUserGraduate', 'Erst online, dann Anruf', 'Kunden und Bewerber schauen zuerst auf Instagram und Google.']];
    it.forEach((t, i) => {
      const x = M + (i % 2) * 3.65, y = 2.05 + Math.floor(i / 2) * 2.2;
      card(s, x, y, 3.4, 1.95);
      iconCircle(s, t[0], x + 0.3, y + 0.28, 0.55);
      txt(s, t[1], { x: x + 0.3, y: y + 0.95, w: 2.9, h: 0.35, fontFace: F.sb, fontSize: 15, color: C.nacht });
      txt(s, t[2], { x: x + 0.3, y: y + 1.3, w: 2.9, h: 0.6, fontSize: 11, color: C.grau });
    });
    card(s, 8.3, 2.05, 4.3, 4.15, C.nacht);
    s.addImage({ path: `${IMG}/waves.png`, x: 10.6, y: 2.2, w: 1.9, h: 1.9 });
    s.addText([{ text: 'Wer jetzt anfängt, wird die ', options: { color: C.weiss } }, { text: 'Nummer 1', options: { color: C.or } }, { text: ' in der Region.', options: { color: C.weiss } }], { x: 8.65, y: 4.0, w: 3.7, h: 1.9, margin: 0, fontFace: F.xb, fontSize: 24, valign: 'top', isTextBox: true });
    footer(s, false);
    s.addNotes('Hintergrund für Rückfragen (Stand 09/2026, ca.-Werte): Größter regionaler Wettbewerber Pfättisch ca. 1.059 Instagram-Follower; unsere Facebook-Seite ca. 150, LinkedIn 17 Follower; Google Gaimersheim 5,0 Sterne bei 17 Bewertungen.');
  }

  // ================= 3 WARUM JETZT =================
  {
    const s = base(true);
    kicker(s, 'Warum jetzt', true);
    title(s, [{ text: 'Der richtige ' }, { text: 'Zeitpunkt.', o: true }], true);
    const st = [['FaHouse', 'Einbrüche nehmen wieder zu', 'Das Bedürfnis nach Sicherheit und Beratung wächst.'], ['FaUserGraduate', 'Nachwuchs wird knapp', 'Azubis und Fachkräfte wählen den Arbeitgeber, den sie kennen.'], ['FaHandshake', 'Vertrauen entsteht online', 'Wer sich zeigt, wird gefragt, als Dienstleister und als Arbeitgeber.']];
    st.forEach((v, i) => {
      const x = M + i * 4.0;
      card(s, x, 2.05, 3.75, 2.5, C.anth);
      iconCircle(s, v[0], x + 0.3, 2.35, 0.65);
      txt(s, v[1], { x: x + 0.3, y: 3.15, w: 3.2, h: 0.45, fontFace: F.sb, fontSize: 15, color: C.weiss });
      txt(s, v[2], { x: x + 0.3, y: 3.65, w: 3.2, h: 0.8, fontSize: 13, color: C.silber });
    });
    card(s, M, 4.95, 11.8, 1.05, C.anth);
    iconCircle(s, 'FaCalendarDays', M + 0.3, 5.17, 0.6);
    txt(s, [{ text: 'Tag des Einbruchschutzes: ', options: { fontFace: F.sb, color: C.weiss } }, { text: 'Mit der Zeitumstellung beginnt die dunkle Jahreszeit. Der perfekte Startschuss für unseren Kanal.', options: { color: 'DDDDDD' } }], { x: M + 1.15, y: 5.22, w: 10.4, h: 0.6, fontSize: 15, valign: 'middle' });
    footer(s, true);
    s.addNotes('Hintergrund für Rückfragen: PKS 2025 Deutschland 82.920 Wohnungseinbrüche (+5,7 %), Bayern 3.806 (+5,6 %); GDV: Ø-Schaden 3.850 €; HWK München: 24 % der Lehrstellen im Handwerk Oberbayern 2023/24 unbesetzt. 44,9 % der Einbrüche scheitern im Versuch, Sicherung wirkt. Tag des Einbruchschutzes: 25.10.2026.');
  }

  // ================= 4 USP =================
  {
    const s = base(false);
    kicker(s, 'Was uns einzigartig macht', false);
    title(s, [{ text: 'Wir bauen nicht nur ein. ' }, { text: 'Wir sind da, wenn es ernst wird.', o: true }], false, { h: 1.3, size: 30 });
    const steps = [['FaPenRuler', 'Planung', 'Individuelles Sicherheitskonzept'], ['FaScrewdriverWrench', 'Einbau', 'VdS-anerkannte Errichtung'], ['FaHeadset', '24h-Leitstelle', 'Wir sind wach, rund um die Uhr'], ['FaCarSide', 'Wachdienst', 'SWD fährt raus, vor Ort']];
    steps.forEach((st, i) => {
      const x = M + i * 3.05;
      card(s, x, 2.55, 2.75, 2.35, i === 2 ? C.nacht : C.hell);
      iconCircle(s, st[0], x + 0.3, 2.85, 0.7);
      txt(s, st[1], { x: x + 0.3, y: 3.75, w: 2.3, h: 0.45, fontFace: F.xb, fontSize: 18, color: i === 2 ? C.weiss : C.nacht });
      txt(s, st[2], { x: x + 0.3, y: 4.2, w: 2.3, h: 0.6, fontSize: 13, color: i === 2 ? C.silber : C.grau });
      if (i < 3) s.addText('→', { x: x + 2.75, y: 3.45, w: 0.3, h: 0.5, margin: 0, align: 'center', fontFace: F.xb, fontSize: 22, color: C.or, isTextBox: true });
    });
    txt(s, 'Die meisten Wettbewerber decken nur Planung und Einbau ab. Die komplette Kette aus einer Hand ist unsere stärkste Geschichte, für Kunden und für Bewerber.', { x: M, y: 5.2, w: 11.8, h: 0.6, fontSize: 15 });
    const badges = ['Seit 1975', 'VdS 3403', 'DIN 14675', 'ISO 9001', 'Telenot-Stützpunkt', '25 Jahre BHE'];
    let bx = M;
    badges.forEach(b => { const w = 0.3 + b.length * 0.105; card(s, bx, 5.95, w, 0.42, C.panel); txt(s, b, { x: bx, y: 5.95, w, h: 0.42, fontFace: F.sb, fontSize: 11, align: 'center', valign: 'middle', color: C.anth }); bx += w + 0.15; });
    footer(s, false);
    s.addNotes('Das ist der Kern der ganzen Strategie: Die Leitstelle ist unser Alleinstellungsmerkmal. Keine Agentur und kein Wettbewerber kann zeigen, was bei uns nachts passiert.');
  }

  // ================= 5 MARKENKERN =================
  {
    const s = base(true);
    kicker(s, 'Markenkern', true);
    txt(s, 'Für Kunden', { x: M, y: 1.2, w: 5.5, h: 0.35, fontFace: F.lt, fontSize: 14, color: C.silber, charSpacing: 3 });
    s.addText([{ text: 'Wir sind wach, damit du ', options: { color: C.weiss } }, { text: 'schlafen', options: { color: C.or } }, { text: ' kannst.', options: { color: C.weiss } }], { x: M, y: 1.6, w: 7.2, h: 1.6, margin: 0, fontFace: F.xb, fontSize: 36, valign: 'top', isTextBox: true });
    txt(s, 'Für Bewerber', { x: M, y: 3.55, w: 5.5, h: 0.35, fontFace: F.lt, fontSize: 14, color: C.silber, charSpacing: 3 });
    s.addText([{ text: 'Mach Alarm. ', options: { color: C.weiss } }, { text: 'Beruflich.', options: { color: C.or } }], { x: M, y: 3.95, w: 7.2, h: 0.8, margin: 0, fontFace: F.xb, fontSize: 36, isTextBox: true });
    txt(s, 'Tonalität', { x: 8.6, y: 1.2, w: 4, h: 0.35, fontFace: F.lt, fontSize: 14, color: C.silber, charSpacing: 3 });
    [['FaMoon', 'Ruhig statt panisch'], ['FaCircleCheck', 'Fakten statt Angstmache'], ['FaMapLocationDot', 'Nahbar und regional'], ['FaEyeSlash', 'Immer diskret']].forEach((t, i) => {
      iconCircle(s, t[0], 8.6, 1.7 + i * 0.85, 0.55);
      txt(s, t[1], { x: 9.35, y: 1.7 + i * 0.85, w: 3.4, h: 0.55, fontFace: F.sb, fontSize: 16, color: C.weiss, valign: 'middle' });
    });
    card(s, M, 5.25, 11.8, 0.9, C.anth);
    txt(s, [{ text: 'Ansprache: ', options: { fontFace: F.sb, color: C.weiss } }, { text: '„du“ auf Instagram (Plattform-Norm, Recruiting). „Sie“ auf Website, in Angeboten und in der Beratung. In Nachrichten spiegeln wir den Kunden.', options: { color: 'DDDDDD' } }], { x: M + 0.3, y: 5.25, w: 11.2, h: 0.9, fontSize: 14, valign: 'middle' });
    footer(s, true);
    s.addNotes('Beide Claims sind freigegeben. Die Ansprache „du“ ist eine Empfehlung, die letzte Entscheidung liegt bei der Geschäftsführung.');
  }

  // ================= 5a STRATEGIE-HAUS =================
  {
    const s = base(false);
    kicker(s, 'Das Strategie-Haus', false);
    s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: M, y: 0.95, w: 11.8, h: 1.0, fill: { color: C.nacht }, line: { color: C.nacht } });
    card(s, M, 1.9, 11.8, 0.85, C.nacht);
    txt(s, [{ text: 'VISION  ', options: { fontFace: F.sb, color: C.or, fontSize: 11, charSpacing: 3 } }, { text: 'Der sichtbarste und vertrauenswürdigste Sicherheitspartner der Region, für Kunden und für Mitarbeitende.', options: { fontFace: F.xb, color: C.weiss } }], { x: M + 0.3, y: 1.9, w: 11.2, h: 0.85, fontSize: 17, align: 'center', valign: 'middle' });
    const pil = [['FaHouse', 'Kunden gewinnen', 'Familien und Eigenheimbesitzer in der Region', 'Kostenlose Sicherheitsberatung'], ['FaUserGraduate', 'Nachwuchs begeistern', 'Schülerinnen, Schüler und ihre Eltern', 'Praktikum per WhatsApp'], ['FaUserTie', 'Fachkräfte überzeugen', 'Elektroniker und Quereinsteiger', 'Bewerbung in 60 Sekunden']];
    pil.forEach((p, i) => {
      const x = M + i * 4.0;
      card(s, x, 2.95, 3.8, 2.45);
      iconCircle(s, p[0], x + 0.3, 3.2, 0.6);
      txt(s, p[1], { x: x + 1.05, y: 3.25, w: 2.6, h: 0.5, fontFace: F.xb, fontSize: 16, color: C.nacht, valign: 'middle' });
      txt(s, 'FÜR WEN', { x: x + 0.3, y: 3.95, w: 3.2, h: 0.25, fontFace: F.sb, fontSize: 9, color: C.or, charSpacing: 2 });
      txt(s, p[2], { x: x + 0.3, y: 4.2, w: 3.2, h: 0.45, fontSize: 12, color: C.anth });
      txt(s, 'WEG ZU UNS', { x: x + 0.3, y: 4.7, w: 3.2, h: 0.25, fontFace: F.sb, fontSize: 9, color: C.or, charSpacing: 2 });
      txt(s, p[3], { x: x + 0.3, y: 4.95, w: 3.2, h: 0.35, fontFace: F.sb, fontSize: 12, color: C.nacht });
    });
    card(s, M, 5.6, 11.8, 0.85, C.or);
    txt(s, [{ text: 'FUNDAMENT  ', options: { fontFace: F.sb, color: C.nacht, fontSize: 11, charSpacing: 3 } }, { text: 'Planung → Einbau → 24h-Leitstelle → Wachdienst · Familienunternehmen · diskret, echt, nahbar', options: { fontFace: F.sb, color: C.weiss } }], { x: M + 0.3, y: 5.6, w: 11.2, h: 0.85, fontSize: 13, align: 'center', valign: 'middle' });
    footer(s, false);
    s.addNotes('Das Haus fasst die Strategie zusammen: Die Vision ist das Dach, die drei Ziele tragen es, das Fundament ist das, was uns schon heute ausmacht.');
  }

  // ================= 5b DER WEG =================
  {
    const s = base(true);
    kicker(s, 'Der Weg', true);
    title(s, [{ text: 'Vom Fremden zum ' }, { text: 'Kunden oder Kollegen.', o: true }], true);
    const st = [['FaMagnifyingGlass', 'Sehen', 'Echte Einblicke fallen auf: „Die sind ja nachts für uns wach.“'], ['FaHandshake', 'Vertrauen', 'Gesichter, Wissen und Haltung: „Die kennen sich aus.“'], ['FaWhatsapp', 'Kontakt', 'Eine Nachricht genügt: Beratung, Praktikum, Bewerbung.'], ['FaHeart', 'Bindung', 'Kunden empfehlen uns, Mitarbeitende zeigen stolz, wo sie arbeiten.']];
    st.forEach((p, i) => {
      const x = M + i * 3.0, last = i === 3;
      card(s, x, 2.2, 2.7, 3.4, last ? C.or : C.anth);
      iconCircle(s, p[0], x + 0.3, 2.5, 0.65, last ? C.nacht : C.or);
      txt(s, (i + 1) + ' · ' + p[1], { x: x + 0.3, y: 3.4, w: 2.2, h: 0.5, fontFace: F.xb, fontSize: 20, color: C.weiss });
      txt(s, p[2], { x: x + 0.3, y: 4.0, w: 2.2, h: 1.4, fontSize: 13, color: last ? C.weiss : C.silber });
      if (i < 3) s.addText('→', { x: x + 2.7, y: 3.6, w: 0.3, h: 0.5, margin: 0, align: 'center', fontFace: F.xb, fontSize: 22, color: C.or, isTextBox: true });
    });
    txt(s, 'Social Media ist kein Selbstzweck, sondern der Anfang einer Beziehung.', { x: M, y: 5.95, w: 11.8, h: 0.4, fontSize: 15, color: C.silber });
    footer(s, true);
    s.addNotes('Jede Stufe braucht andere Inhalte: Reels für Aufmerksamkeit, Wissen und Gesichter für Vertrauen, eine niedrige Hürde für den Kontakt.');
  }

  // ================= 6 ZIELGRUPPEN =================
  {
    const s = base(false);
    kicker(s, 'Zielgruppen', false);
    title(s, 'Drei Menschen, für die wir posten.', false);
    const P3 = [
      ['FaHouse', '45 %', 'Familie Huber', 'Eigenheim in der Region, 35–65', 'Auslöser: Einbruch in der Nachbarschaft, dunkle Jahreszeit, Urlaub', 'Kostenlose Sicherheitsberatung'],
      ['FaUserGraduate', '30 %', 'Leon, 16 (+ Mama)', 'Schüler, technikbegeistert, auf Reels und TikTok', 'Frage: „Sind die Leute nett? Was verdiene ich?“', 'Praktikum per WhatsApp'],
      ['FaUserTie', '15 %', 'Markus & Sabrina', 'Elektroniker bzw. Quereinsteigerin (Leitstelle, Sicherheitsdienst)', 'Suchen Abwechslung, Sicherheit, Wertschätzung', 'Bewerbung in 60 Sekunden'],
    ];
    P3.forEach((p, i) => {
      const x = M + i * 4.0, y = 2.1;
      card(s, x, y, 3.7, 4.3);
      iconCircle(s, p[0], x + 0.3, y + 0.3, 0.7);
            txt(s, p[2], { x: x + 0.3, y: y + 1.2, w: 3.1, h: 0.45, fontFace: F.xb, fontSize: 18, color: C.nacht });
      txt(s, p[3], { x: x + 0.3, y: y + 1.7, w: 3.1, h: 0.75, fontSize: 13, color: C.grau });
      txt(s, p[4], { x: x + 0.3, y: y + 2.5, w: 3.1, h: 0.8, fontSize: 13, color: C.grau });
      card(s, x + 0.3, y + 3.5, 3.1, 0.5, C.nacht);
      txt(s, '→ ' + p[5], { x: x + 0.3, y: y + 3.5, w: 3.1, h: 0.5, fontFace: F.sb, fontSize: 12, color: C.weiss, align: 'center', valign: 'middle' });
    });
    txt(s, 'Dazu Marke und Region für alle. Gewerbekunden erreichen wir später über LinkedIn (Stufe 2).', { x: M, y: 6.5, w: 11.8, h: 0.3, fontSize: 11, color: C.grau });
    footer(s, false);
    s.addNotes('Hintergrund: Anteil am Content ca. 45 % Kunden, 30 % Azubis, 15 % Fachkräfte, 10 % Marke. Saisonal verschiebt sich das: Oktober bis März mehr Kundenthemen, Januar bis April und September mehr Azubi-Themen.');
  }

  // ================= 7 MARKEN-KIT =================
  {
    const s = base(false);
    kicker(s, 'Marken-Kit', false);
    title(s, [{ text: 'Das Logo bleibt. ' }, { text: 'Die Regeln sind neu.', o: true }], false);
    const sw = [['EB5A1B', 'Signal-Orange', '#EB5A1B', C.weiss], ['111111', 'Nacht', '#111111', C.weiss], ['222222', 'Anthrazit', '#222222', C.weiss], ['F4F4F4', 'Hellgrau', '#F4F4F4', C.nacht]];
    sw.forEach((c, i) => {
      const x = M + i * 1.95;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.05, w: 1.75, h: 1.75, rectRadius: 0.1, fill: { color: c[0] }, line: { color: c[0] === 'F4F4F4' ? 'DDDDDD' : c[0] } });
      txt(s, c[1], { x: x + 0.15, y: 3.05, w: 1.5, h: 0.3, fontFace: F.sb, fontSize: 12, color: c[3] });
      txt(s, c[2], { x: x + 0.15, y: 3.35, w: 1.5, h: 0.3, fontSize: 11, color: c[3] });
    });
    txt(s, 'Viel Nacht und Weiß, Orange nur als Signal: Es markiert das Wichtigste, nie alles.', { x: M, y: 3.95, w: 7.6, h: 0.35, fontSize: 13, color: C.grau });
    txt(s, 'Poppins', { x: M, y: 4.55, w: 4, h: 0.8, fontFace: F.xb, fontSize: 44, color: C.nacht });
    txt(s, 'ExtraBold für Headlines · SemiBold für Sublines · Regular für Text · Light für Kicker. Klar, modern, gut lesbar.', { x: M, y: 5.4, w: 7.4, h: 0.7, fontSize: 13, color: C.grau });
    card(s, 8.85, 2.05, 3.75, 4.2, C.hell);
    s.addImage({ path: `${P}/assets/profilbild-weiss.png`, x: 9.72, y: 2.35, w: 2.0, h: 2.0 });
    txt(s, 'Profilbild: das Signal', { x: 9.1, y: 4.5, w: 3.3, h: 0.4, fontFace: F.sb, fontSize: 15, color: C.nacht, align: 'center' });
    txt(s, 'Der Schriftzug ist im kleinen Kreis nicht lesbar, das Signal schon. Wiedererkennbar auf einen Blick.', { x: 9.1, y: 4.9, w: 3.3, h: 0.9, fontSize: 12, color: C.grau, align: 'center' });
    footer(s, false);
    s.addNotes('Details im Marken-Kit (8 Seiten, liegt als PDF bei). Das Profilbild zeigt nur das Signal aus dem Logo. Das braucht Ihre Freigabe. Die Endfassung kommt aus der Vektordatei des Logos.');
  }

  // ================= 8 DREI WELTEN =================
  {
    const s = base(false, C.panel);
    kicker(s, 'Drei Vorlagen-Welten', false);
    title(s, [{ text: 'Drei Welten. ' }, { text: 'Eine DNA.', o: true }], false);
    const w3 = [['karussell-schwachstellen-4', 'Nachtschicht', 'Kunden · Leitstelle · Einsätze'], ['karussell-schwachstellen-1', 'Wissen', 'Tipps · Mythen · Förderung'], ['post-karriere-praktikum', 'Karriere', 'Azubis · Fachkräfte · Team']];
    w3.forEach((t, i) => {
      const x = M + 0.2 + i * 4.0, h = 3.9, w = h * 1080 / 1350;
      s.addImage({ path: V(t[0]), x, y: 1.95, w, h, shadow: { type: 'outer', color: '000000', opacity: 0.25, blur: 8, offset: 3, angle: 90 } });
      txt(s, t[1], { x, y: 5.95, w: 3.2, h: 0.4, fontFace: F.xb, fontSize: 17, color: C.nacht });
      txt(s, t[2], { x, y: 6.35, w: 3.2, h: 0.3, fontSize: 12, color: C.grau });
    });
    footer(s, false);
    s.addNotes('Jede Zielgruppe hat ihren eigenen Look. Durch Farben, Schrift und Signal-Elemente bleibt alles als Poleschak erkennbar. ');
  }

  // ================= 9 PROFIL =================
  {
    const s = base(true);
    kicker(s, 'Profil-Relaunch', true);
    title(s, [{ text: 'Der erste Eindruck in ' }, { text: '3 Sekunden.', o: true }], true);
    const ih = 4.7, iw = ih * igMeta.width / igMeta.height;
    s.addImage({ path: `${IMG}/ig-mockup.png`, x: M, y: 1.95, w: iw, h: ih });
    const pts = [['FaBolt', 'Profilbild: das Signal', 'wiedererkennbar im Feed und in Stories'], ['FaListCheck', 'Bio in 4 Zeilen', 'Versprechen · Leistungen · seit 1975 & Region · Handlung'], ['FaStar', 'Highlights', 'Über uns · Leitstelle · Karriere · Tipps · Kunden'], ['FaWhatsapp', 'WhatsApp als Haupt-Button', 'niedrigste Hürde für Kunden und Azubis'], ['FaLock', 'Kein Notrufkanal', 'automatische Antwort verweist auf 110 und die Leitstelle']];
    pts.forEach((p, i) => {
      const y = 2.0 + i * 0.9, x = M + iw + 0.6;
      iconCircle(s, p[0], x, y, 0.55);
      txt(s, p[1], { x: x + 0.75, y: y - 0.02, w: 5.2, h: 0.35, fontFace: F.sb, fontSize: 15, color: C.weiss });
      txt(s, p[2], { x: x + 0.75, y: y + 0.32, w: 5.2, h: 0.35, fontSize: 12, color: C.silber });
    });
    footer(s, true);
    s.addNotes('Das Profil wird im Aufbaumonat komplett neu aufgesetzt. Follower-Zahlen tragen wir nach der Nullmessung ein. Aktuell habe ich noch keinen Zugang zum Account.');
  }

  // ================= 10 CONTENT-SÄULEN =================
  {
    const s = base(false);
    kicker(s, 'Strategie', false);
    title(s, 'Fünf Content-Säulen.', false);
    const pil = [['FaHeadset', 'Aus der Leitstelle', 'Nachtschicht, Alarmablauf, unser Versprechen'], ['FaLightbulb', 'Sicher wissen', 'Tipps, Mythen und Förderung, ruhig erklärt'], ['FaUserGraduate', 'Mach Alarm. Beruflich.', 'Ausbildung, Jobs und der Alltag im Team'], ['FaPeopleGroup', 'Familie Poleschak', 'Menschen, Geschichte und Region'], ['FaStar', 'Vertrauen', 'Qualität, Auszeichnungen, Stimmen unserer Kunden']];
    pil.forEach((p, i) => {
      const x = M + i * 2.4;
      card(s, x, 2.1, 2.2, 3.6, i === 0 ? C.nacht : C.hell);
      iconCircle(s, p[0], x + 0.3, 2.4, 0.65);
      txt(s, p[1], { x: x + 0.3, y: 3.3, w: 1.75, h: 0.8, fontFace: F.xb, fontSize: 15, color: i === 0 ? C.weiss : C.nacht });
      txt(s, p[2], { x: x + 0.3, y: 4.15, w: 1.75, h: 1.3, fontSize: 12, color: i === 0 ? C.silber : C.grau });
    });
    txt(s, 'Die Leitstelle ist die kleinste Säule, aber die wichtigste: Sie macht uns unverwechselbar.', { x: M, y: 6.0, w: 11.8, h: 0.4, fontSize: 14, color: C.anth });
    footer(s, false);
    s.addNotes('Hintergrund: geplanter Anteil am Feed ca. 25 % Leitstelle, 30 % Sicher wissen, 30 % Karriere, 10 % Familie, 5 % Vertrauen.');
  }

  // ================= 11 FORMATE & RHYTHMUS =================
  {
    const s = base(false);
    kicker(s, 'Formate & Rhythmus', false);
    title(s, [{ text: 'Regelmäßig ' }, { text: 'statt zufällig.', o: true }], false);
    const f = [['Reels', 'neue Menschen erreichen'], ['Karussells', 'Wissen zum Speichern'], ['Bild-Posts', 'Gesichter und Vertrauen'], ['Stories', 'Nähe und Austausch']];
    f.forEach((v, i) => {
      const x = M + i * 2.95;
      card(s, x, 2.0, 2.75, 1.4, i === 0 ? C.nacht : C.hell);
      txt(s, v[0], { x: x + 0.3, y: 2.2, w: 2.3, h: 0.45, fontFace: F.xb, fontSize: 20, color: i === 0 ? C.or : C.nacht });
      txt(s, v[1], { x: x + 0.3, y: 2.7, w: 2.3, h: 0.5, fontSize: 13, color: i === 0 ? C.silber : C.grau });
    });
    const days = [['Mo', 'Story'], ['Di', 'Reel'], ['Mi', 'Story'], ['Do', 'Karussell'], ['Fr', 'Story'], ['Sa', ''], ['So', 'Bild-Post']];
    days.forEach((d, i) => {
      const x = M + i * 1.7, feed = ['Reel', 'Karussell', 'Bild-Post'].includes(d[1]);
      card(s, x, 3.75, 1.55, 1.45, feed ? C.nacht : (d[1] ? C.hell : 'FAFAFA'));
      txt(s, d[0], { x, y: 3.9, w: 1.55, h: 0.45, fontFace: F.xb, fontSize: 20, color: feed ? C.weiss : C.nacht, align: 'center' });
      if (d[1]) txt(s, d[1], { x, y: 4.55, w: 1.55, h: 0.35, fontFace: F.sb, fontSize: 12, color: feed ? C.or : C.grau, align: 'center' });
    });
    bullets(s, [
      [{ text: 'Feste Tage und feste Serien', b: true }, { text: ': Man weiß, was kommt.' }],
      [{ text: 'Vorgeplant', b: true }, { text: ' über die Meta Business Suite, passend zum Schichtdienst.' }],
      [{ text: 'Automatisch auch auf Facebook', b: true }, { text: ': erreicht Eltern und ältere Kunden, ohne Mehraufwand.' }],
    ], { x: M, y: 5.5, w: 11.8, h: 1.2 }, C.anth, 13);
    footer(s, false);
    s.addNotes('Hintergrund: Start mit ca. drei Feed-Beiträgen pro Woche plus Stories. Uhrzeiten und Tage werden nach den ersten Wochen anhand der Instagram-Auswertung angepasst.');
  }

  // ================= 12 SERIEN =================
  {
    const s = base(true);
    kicker(s, 'Serien', true);
    title(s, [{ text: 'Serien sparen Zeit ' }, { text: 'und machen neugierig.', o: true }], true);
    const se = [['FaMoon', '„3 Uhr nachts“', 'POV aus der Leitstelle: Was passiert, wenn dein Alarm losgeht?'], ['FaCircleQuestion', '„Mythos oder Fakt?“', '„Einbrecher kommen nachts“, „Die Smart-Home-Kamera reicht“, immer mit Quelle'], ['FaUserGraduate', '„Frag den Azubi“', 'Ein Azubi beantwortet echte Fragen von Schülern'], ['FaScrewdriverWrench', '„30 Sekunden Technik“', 'Montage im Zeitraffer, Werkzeug-Nahaufnahmen'], ['FaUsers', '„Wer ist eigentlich …?“', 'Ein Gesicht aus dem Team, mit Einwilligung'], ['FaListCheck', '„Sicher-Check“', 'Checklisten für Urlaub, dunkle Jahreszeit, Neubau']];
    se.forEach((t, i) => {
      const x = M + (i % 3) * 4.0, y = 2.05 + Math.floor(i / 3) * 2.2;
      card(s, x, y, 3.75, 1.95, C.anth);
      iconCircle(s, t[0], x + 0.3, y + 0.3, 0.55);
      txt(s, t[1], { x: x + 1.0, y: y + 0.35, w: 2.6, h: 0.45, fontFace: F.sb, fontSize: 15, color: C.weiss, valign: 'middle' });
      txt(s, t[2], { x: x + 0.3, y: y + 1.0, w: 3.2, h: 0.8, fontSize: 12, color: C.silber });
    });
    footer(s, true);
    s.addNotes('Wiederkehrende Formate: Aufbau, Vorlage und Schnitt sind immer gleich. Dadurch schaffe ich mehr Qualität in weniger Zeit, und die Follower wissen, was sie erwartet.');
  }

  // ================= 13 REDAKTIONSPLAN =================
  {
    const s = base(false);
    kicker(s, 'Redaktionsplan', false);
    title(s, 'So sieht der November 2026 aus.', false);
    const rows = [['Di 03.11.', 'Reel', '„3 Uhr nachts“ #1: Ein Alarm geht ein', 'Leitstelle'], ['Do 05.11.', 'Karussell', 'Dunkle Jahreszeit: 5 Schwachstellen am Haus', 'Sicher wissen'], ['So 08.11.', 'Bild', 'Das ist die Nachtschicht', 'Familie'], ['Di 10.11.', 'Reel', '„Frag den Azubi“ #1: Was machst du eigentlich?', 'Karriere'], ['Fr 13.11.', 'Karussell', 'Rauchmeldertag: Rauchmelder testen', 'Sicher wissen'], ['So 15.11.', 'Bild', 'Danke für eure Bewertungen!', 'Vertrauen'], ['Di 17.11.', 'Reel', 'Mythos: Die Smart-Home-Kamera reicht doch', 'Sicher wissen'], ['Do 19.11.', 'Karussell', 'Ausbildung Elektroniker/in in 6 Slides', 'Karriere'], ['So 22.11.', 'Bild', 'Wir suchen: Servicetechniker (m/w/d)', 'Karriere'], ['Di 24.11.', 'Reel', '„30 Sekunden Technik“: Ein Melder entsteht', 'Leitstelle'], ['Do 26.11.', 'Karussell', 'Sicherung wirkt: Viele Einbrüche scheitern', 'Sicher wissen'], ['So 29.11.', 'Bild', 'Seit 1975: Familie Poleschak', 'Familie']];
    const hdr = ['Datum', 'Format', 'Thema', 'Säule'].map(h => ({ text: h, options: { bold: true, color: C.weiss, fill: { color: C.nacht }, fontFace: F.sb } }));
    const body = rows.map((r, i) => r.map((c, j) => ({ text: c, options: { color: j === 1 && c === 'Reel' ? C.or : C.anth, bold: j === 1 && c === 'Reel', fill: { color: i % 2 ? C.weiss : C.hell } } })));
    s.addTable([hdr, ...body], { x: M, y: 1.85, w: 11.8, colW: [1.5, 1.5, 6.3, 2.5], fontFace: F.rg, fontSize: 11, rowH: 0.33, border: { type: 'none' }, margin: [0.02, 0.1, 0.02, 0.1], valign: 'middle' });
    footer(s, false);
    s.addNotes('Konkreter Plan für den ersten vollen Monat. Der Rauchmeldertag am Freitag, 13.11., ist ein bundesweiter Aktionstag. Stories kommen jeweils montags, mittwochs und freitags dazu.');
  }

  // ================= 14 JAHRESKALENDER =================
  {
    const s = base(false);
    kicker(s, 'Jahresplan', false);
    title(s, '12 Monate im Überblick.', false);
    const months = ['Okt', 'Nov', 'Dez', 'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt'];
    const gx = M, gw = 11.8, cw = gw / 13, gy = 2.2;
    months.forEach((m, i) => {
      card(s, gx + i * cw + 0.03, gy, cw - 0.06, 0.5, i === 0 || i === 12 ? C.nacht : C.hell);
      txt(s, m, { x: gx + i * cw, y: gy, w: cw, h: 0.5, fontFace: F.sb, fontSize: 12, align: 'center', valign: 'middle', color: i === 0 || i === 12 ? C.weiss : C.nacht });
    });
    txt(s, '2026', { x: gx, y: gy - 0.35, w: 2, h: 0.3, fontSize: 10, color: C.grau });
    txt(s, '2027', { x: gx + 3 * cw, y: gy - 0.35, w: 2, h: 0.3, fontSize: 10, color: C.grau });
    const bar = (from, to, y, label, fill, tc) => { card(s, gx + from * cw + 0.03, y, (to - from + 1) * cw - 0.06, 0.45, fill); txt(s, label, { x: gx + from * cw + 0.15, y, w: (to - from + 1) * cw - 0.3, h: 0.45, fontFace: F.sb, fontSize: 11, color: tc, valign: 'middle' }); };
    bar(0, 5, 3.0, 'Kundenkampagne „Kostenlose Sicherheitsberatung“', C.nacht, C.weiss);
    bar(3, 6, 3.6, 'Azubi-Kampagne „Mach Alarm. Beruflich.“', C.or, C.weiss);
    bar(11, 12, 3.6, 'Messe & Herbst', C.or, C.weiss);
    bar(0, 0, 4.2, 'Aufbau', C.panel, C.nacht);
    const ev = [[0, '25.10. Start (Einbruchschutz-Tag)', 0], [1, '13.11. Rauchmeldertag', 1], [6, '6-Monats-Review', 0], [10, '13.08. Rauchmeldertag', 1], [11, 'Ausbildungsstart', 2], [12, '31.10.2027 Jahresbilanz', 0]];
    ev.forEach(e => {
      const x = gx + e[0] * cw + cw / 2, y = 4.9 + e[2] * 0.6;
      s.addShape(pres.shapes.OVAL, { x: x - 0.09, y: y + 0.06, w: 0.18, h: 0.18, fill: { color: C.or }, line: { color: C.or } });
      const right = x > gx + gw - 2.6;
      txt(s, e[1], { x: right ? x - 2.75 : x + 0.18, y, w: 2.55, h: 0.3, fontSize: 11, color: C.anth, align: right ? 'right' : 'left' });
    });
    footer(s, false);
    s.addNotes('Die Kampagnen folgen den Saisons: Einbruchsaison Oktober bis März, Azubi-Bewerbungsphase Januar bis April, Ausbildungsmesse im Herbst. Nach sechs Monaten gibt es ein Review mit echten Zahlen.');
  }

  // ================= 15 RECRUITING =================
  {
    const s = base(false, C.or);
    s.addImage({ path: `${IMG}/waves-k.png`, x: 9.3, y: 3.2, w: 4.6, h: 4.6 });
    kicker(s, 'Recruiting-Kampagne', false, M, 0.55, C.nacht);
    s.addText([{ text: 'Mach Alarm. ', options: { color: C.weiss } }, { text: 'Beruflich.', options: { color: C.nacht } }], { x: M, y: 0.95, w: 11, h: 0.9, margin: 0, fontFace: F.xb, fontSize: 38, isTextBox: true });
    const ph = [['1 · Aufmerksamkeit', 'Jan.–Feb.', '„Frag den Azubi“, Tag als Azubi, Technik-Reels', 'Folgen & Teilen'], ['2 · Bewerbung', 'Feb.–Apr.', 'Beste Reels werden beworben, Karussell „Ausbildung in 6 Slides“', 'Praktikum anfragen'], ['3 · Messe & Herbst', 'Sep.–Okt.', 'Ausbildungsplatzbörse, neue Azubis stellen sich vor', 'Kennenlernen'], ['Fachkräfte', 'bei offenen Stellen', '„Kollege erzählt“, Einblick Leitstelle', 'Bewerben']];
    ph.forEach((p, i) => {
      const x = M + i * 2.95;
      card(s, x, 2.1, 2.75, 2.9, C.nacht);
      txt(s, p[0], { x: x + 0.25, y: 2.3, w: 2.3, h: 0.35, fontFace: F.sb, fontSize: 14, color: C.or });
      txt(s, p[1], { x: x + 0.25, y: 2.7, w: 2.3, h: 0.3, fontSize: 11, color: C.silber });
      txt(s, p[2], { x: x + 0.25, y: 3.15, w: 2.3, h: 1.1, fontSize: 12, color: C.weiss });
      txt(s, '→ ' + p[3], { x: x + 0.25, y: 4.45, w: 2.3, h: 0.35, fontFace: F.sb, fontSize: 13, color: C.or });
    });
    card(s, M, 5.35, 3.9, 0.6, C.nacht); txt(s, 'Azubis → Praktikum per WhatsApp', { x: M, y: 5.35, w: 3.9, h: 0.6, fontFace: F.sb, fontSize: 13, color: C.weiss, align: 'center', valign: 'middle' });
    card(s, M + 4.1, 5.35, 3.9, 0.6, C.nacht); txt(s, 'Fachkräfte → Bewerbung in 60 Sekunden', { x: M + 4.1, y: 5.35, w: 3.9, h: 0.6, fontFace: F.sb, fontSize: 13, color: C.weiss, align: 'center', valign: 'middle' });
    txt(s, 'Anzeigen immer (m/w/d), ohne Ausschluss nach Alter oder Geschlecht (AGG). Angesprochen wird über Region, Interessen und Gestaltung.', { x: M, y: 6.15, w: 8.3, h: 0.5, fontSize: 11, color: C.nacht });
    s.addImage({ path: LOGO_POS, x: M, y: H - 0.62, w: 0.36 / LOGO_R, h: 0.36 });
    txt(s, String(pageNo).padStart(2, '0'), { x: W - M - 1, y: H - 0.55, w: 1, h: 0.3, fontFace: F.lt, fontSize: 11, color: C.nacht, align: 'right', charSpacing: 3 });
    s.addNotes('Niedrige Hürden sind der Schlüssel: kein Anschreiben, kein Formular-Marathon. Die Rückmeldung an Bewerber innerhalb von 48 Stunden übernimmt die Personalabteilung, das ist nicht Teil meiner Social-Media-Aufgabe.');
  }

  // ================= 16 KUNDEN & WERBUNG =================
  {
    const s = base(false);
    kicker(s, 'Kunden & Werbung', false);
    title(s, [{ text: 'Werbung, ' }, { text: 'bewusst einfach.', o: true }], false);
    card(s, M, 2.0, 5.6, 4.35, C.nacht);
    txt(s, 'Kundenkampagne', { x: M + 0.35, y: 2.25, w: 5, h: 0.35, fontFace: F.lt, fontSize: 12, color: C.silber, charSpacing: 3 });
    txt(s, '„Kostenlose Sicherheitsberatung“', { x: M + 0.35, y: 2.65, w: 5, h: 0.5, fontFace: F.xb, fontSize: 20, color: C.weiss });
    bullets(s, ['In der Einbruchsaison im Herbst und Winter', 'Gezielt in der Region rund um unsere Standorte', 'Mit unseren besten Wissens- und Leitstellen-Beiträgen', [{ text: 'Stichwort „Instagram“', b: true }, { text: ' per WhatsApp: Wir sehen, woher Anfragen kommen' }], 'Weiterleitung an den Vertrieb am selben Tag'], { x: M + 0.35, y: 3.35, w: 5, h: 2.8 }, C.weiss, 13);
    txt(s, 'So läuft es', { x: 6.9, y: 2.0, w: 5, h: 0.35, fontFace: F.sb, fontSize: 16, color: C.nacht });
    [['1', 'Organisch posten'], ['2', 'Den besten Beitrag gezielt bewerben'], ['3', 'Wirkung im Monatsbericht festhalten']].forEach((t, i) => {
      const y = 2.5 + i * 0.62;
      s.addShape(pres.shapes.OVAL, { x: 6.9, y, w: 0.45, h: 0.45, fill: { color: C.or }, line: { color: C.or } });
      txt(s, t[0], { x: 6.9, y, w: 0.45, h: 0.45, fontFace: F.xb, fontSize: 14, color: C.weiss, align: 'center', valign: 'middle' });
      txt(s, t[1], { x: 7.5, y, w: 5.1, h: 0.45, fontSize: 13, valign: 'middle' });
    });
    card(s, 6.9, 4.6, 5.7, 1.75, C.hell);
    iconCircle(s, 'FaBolt', 7.2, 4.9, 0.55);
    txt(s, 'Geld folgt Wirkung', { x: 7.95, y: 4.88, w: 4.4, h: 0.4, fontFace: F.sb, fontSize: 15, color: C.nacht });
    txt(s, 'Werbebudget fließt nur in Beiträge, die organisch schon funktionieren. Keine teuren Experimente.', { x: 7.95, y: 5.3, w: 4.4, h: 0.9, fontSize: 12, color: C.grau });
    footer(s, false);
    s.addNotes('Das Werbebudget legen wir gemeinsam fest. Geld fließt nur in Beiträge, die schon funktionieren.');
  }

  // ================= 18 ERFOLG =================
  {
    const s = base(true);
    kicker(s, 'Woran wir Erfolg erkennen', true);
    title(s, [{ text: 'Was sich verändern ' }, { text: 'soll.', o: true }], true);
    const k = [['FaMagnifyingGlass', 'Sichtbarkeit', 'Man kennt uns in der Region, auch ohne Einbruch in der Nachbarschaft.'], ['FaHandshake', 'Vertrauen', 'Wer an Sicherheit denkt, denkt zuerst an Poleschak.'], ['FaWhatsapp', 'Anfragen', 'Beratungen entstehen auch über Instagram.'], ['FaUserGraduate', 'Nachwuchs', 'Junge Leute melden sich von selbst für ein Praktikum.'], ['FaUserTie', 'Arbeitgeberbild', 'Bewerber kennen uns schon, bevor sie sich bewerben.'], ['FaHeart', 'Teamstolz', 'Kolleginnen und Kollegen teilen unsere Beiträge gern.']];
    k.forEach((v, i) => {
      const x = M + (i % 3) * 4.0, y = 2.0 + Math.floor(i / 3) * 1.95;
      card(s, x, y, 3.75, 1.7, C.anth);
      iconCircle(s, v[0], x + 0.3, y + 0.3, 0.55);
      txt(s, v[1], { x: x + 1.05, y: y + 0.3, w: 2.5, h: 0.55, fontFace: F.xb, fontSize: 17, color: C.weiss, valign: 'middle' });
      txt(s, v[2], { x: x + 0.3, y: y + 1.0, w: 3.2, h: 0.6, fontSize: 12, color: C.silber });
    });
    txt(s, 'Wir schauen regelmäßig, was wirkt, und berichten jeden Monat auf einer Seite.', { x: M, y: 6.0, w: 11.8, h: 0.35, fontSize: 13, color: C.silber });
    footer(s, true);
    s.addNotes('Konkrete Zielwerte legen wir nach einer Nullmessung gemeinsam fest.');
  }

  // ================= 19 ORGANISATION =================
  {
    const s = base(false);
    kicker(s, 'Organisation', false);
    title(s, [{ text: 'Klein starten. ' }, { text: 'Mit Erfahrung wachsen.', o: true }], false);
    card(s, M, 2.0, 5.75, 4.3, C.nacht);
    txt(s, 'Stufe 1 · Start', { x: M + 0.35, y: 2.25, w: 5, h: 0.45, fontFace: F.xb, fontSize: 20, color: C.or });
    bullets(s, ['Feste interne Zuständigkeit für Social Media', 'Klarer Stundenrahmen, getrennt von der Schichtarbeit', 'Fokus auf Instagram, automatisch auch Facebook', 'Wochenplan mit kurzer Freigabe durch die Geschäftsführung', 'Monatlicher Bericht auf einer Seite'], { x: M + 0.35, y: 2.95, w: 5.1, h: 3.2 }, C.weiss, 13);
    card(s, M + 6.05, 2.0, 5.75, 4.3, C.hell);
    txt(s, 'Stufe 2 · Ausbau', { x: M + 6.4, y: 2.25, w: 5, h: 0.45, fontFace: F.xb, fontSize: 20, color: C.nacht });
    txt(s, 'nach dem Review, wenn Stufe 1 wirkt', { x: M + 6.4, y: 2.7, w: 5, h: 0.3, fontSize: 12, color: C.grau });
    bullets(s, ['Mehr Videos und Serien', 'LinkedIn für Gewerbekunden', 'Google-Profile und Bewertungen aktiv pflegen', 'Größere Kampagnen zu Ausbildung und Einbruchschutz'], { x: M + 6.4, y: 3.2, w: 5.1, h: 2.9 }, C.anth, 13);
    footer(s, false);
    s.addNotes('Umfang, Stundenrahmen und Vergütung bespreche ich gern persönlich.');
  }

  // ================= 20 INTERN VS AGENTUR =================
  {
    const s = base(false);
    kicker(s, 'Intern statt Agentur', false);
    title(s, [{ text: 'Echt geht ' }, { text: 'nur von innen.', o: true }], false);
    card(s, M, 2.0, 5.75, 4.3, C.hell); card(s, M + 6.05, 2.0, 5.75, 4.3, C.nacht);
    txt(s, 'Agentur', { x: M + 0.35, y: 2.25, w: 5, h: 0.45, fontFace: F.xb, fontSize: 20, color: C.nacht });
    bullets(s, ['Nicht vor Ort, Drehtermine müssen geplant werden', 'Kein Zugang zur Leitstelle bei Nacht', 'Muss Abläufe und Menschen erst kennenlernen', 'Braucht trotzdem eine interne Ansprechperson'], { x: M + 0.35, y: 2.95, w: 5.1, h: 3.2 }, C.anth, 14);
    txt(s, 'Intern', { x: M + 6.4, y: 2.25, w: 5, h: 0.45, fontFace: F.xb, fontSize: 20, color: C.or });
    bullets(s, ['Täglich vor Ort, spontane Momente inklusive', 'Content aus erster Hand: die Nachtschicht', 'Kennt Team, Technik und Abläufe', 'Diskretion ist gelebter Alltag'], { x: M + 6.4, y: 2.95, w: 5.1, h: 3.2 }, C.weiss, 14);
    footer(s, false);
    s.addNotes('Ehrlich: Eine Agentur ist nicht unbedingt teurer. Der Unterschied liegt in Echtheit und Zugang.');
  }

  // ================= 21 WARUM ICH =================
  {
    const s = base(true);
    kicker(s, 'Warum intern', true);
    title(s, [{ text: 'Ich bin nachts wach. ' }, { text: 'Ich bin das Versprechen.', o: true }], true, { h: 1.3, w: 7.5 });
    card(s, 8.6, 1.0, 4.0, 5.2, C.anth);
    s.addImage({ path: ic('FaCamera', 'o'), x: 10.25, y: 2.9, w: 0.7, h: 0.7 });
    txt(s, 'Foto von dir einsetzen', { x: 8.6, y: 3.75, w: 4.0, h: 0.4, fontFace: F.sb, fontSize: 13, color: C.silber, align: 'center' });
    const pts = [['FaHeadset', 'Ich arbeite im Nachtdienst der Leitstelle', 'Ich kenne die Abläufe, die Menschen und die Momente, die man zeigen kann und die man nicht zeigen darf.'], ['FaEyeSlash', 'Diskretion ist mein Alltag', 'Datenschutz und Sicherheit sind in unserem Geschäft nicht verhandelbar. Das bringe ich mit.'], ['FaUsers', 'Ich bin mittendrin', 'Nah an Team, Azubis und Technik. Kein Briefing, keine Anfahrt, keine Drehtag-Pauschale.']];
    pts.forEach((p, i) => {
      const y = 2.55 + i * 1.25;
      iconCircle(s, p[0], M, y, 0.6);
      txt(s, p[1], { x: M + 0.85, y: y - 0.02, w: 6.6, h: 0.4, fontFace: F.sb, fontSize: 16, color: C.weiss });
      txt(s, p[2], { x: M + 0.85, y: y + 0.38, w: 6.6, h: 0.65, fontSize: 12, color: C.silber });
    });
    footer(s, true);
    s.addNotes('Persönlicher Teil: Warum ich die richtige Person bin. Ein Foto von mir in der Leitstelle (ohne lesbare Monitore) wirkt hier sehr stark.');
  }

  // ================= 22 SPIELREGELN =================
  {
    const s = base(false);
    kicker(s, 'Voraussetzungen & Spielregeln', false);
    title(s, 'Was es braucht, damit es funktioniert.', false);
    const L = [['FaKey', 'Admin-Zugang', 'Instagram, Facebook, Meta Business Suite + Werbekonto'], ['FaHandshake', 'Freigabe in 24 h', 'Wochenplan montags, eine feste Ansprechperson'], ['FaCamera', 'Foto-Einwilligungen', 'schriftlich, freiwillig, jederzeit widerrufbar (Vorlage fertig)'], ['FaClock', 'Arbeitszeit getrennt', 'Social Media in eigener Arbeitszeit, nie während der Schicht']];
    const R = [['FaEyeSlash', 'Diskretionsregel', '„Könnte ein Einbrecher aus dem Bild etwas lernen?“ Dann nicht.'], ['FaStar', 'QR-Karten für Google', 'Techniker geben sie nach dem Auftrag ab (Firmenprozess)'], ['FaMagnifyingGlass', '„Wie aufmerksam geworden?“', 'bei jeder Anfrage im Büro erfassen'], ['FaHouse', 'Website-Korrekturen', 'Firmenalter, FAQ 2023, © 2024 (einmalig)']];
    [[L, M], [R, M + 6.1]].forEach(([arr, x0]) => arr.forEach((p, i) => {
      const y = 2.05 + i * 1.08;
      iconCircle(s, p[0], x0, y, 0.55);
      txt(s, p[1], { x: x0 + 0.75, y: y - 0.02, w: 4.9, h: 0.35, fontFace: F.sb, fontSize: 15, color: C.nacht });
      txt(s, p[2], { x: x0 + 0.75, y: y + 0.33, w: 4.9, h: 0.5, fontSize: 12, color: C.grau });
    }));
    footer(s, false);
    s.addNotes('Links steht, was ich brauche. Rechts stehen Firmenprozesse, die außerhalb meiner 43 Stunden laufen, aber stark auf die Ziele einzahlen.');
  }

  // ================= 23 FAHRPLAN =================
  {
    const s = base(false);
    kicker(s, 'Fahrplan', false);
    title(s, [{ text: 'Von der Entscheidung zum ' }, { text: 'Start am 25.10.', o: true }], false);
    const st = [['07.10.', 'Entscheidung', 'Freigabe von Modell, Budget, Profilbild'], ['Okt.', 'Aufbaumonat', 'Zugang, Profil, Gestaltung, Einwilligungen'], ['25.10.', 'Start', 'Tag des Einbruchschutzes, erster großer Post'], ['Jan. 2027', 'Azubi-Kampagne', '„Mach Alarm. Beruflich.“'], ['Apr. 2027', '6-Monats-Review', 'Zahlen auf den Tisch, Entscheidung Stufe 2'], ['Okt. 2027', 'Jahresbilanz', '12 Monate, alle Ziele im Check']];
    const y0 = 3.3, x0 = M + 0.3, step = 2.05;
    s.addShape(pres.shapes.LINE, { x: x0 + 0.2, y: y0 + 0.2, w: step * 5, h: 0, line: { color: C.silber, width: 2 } });
    st.forEach((p, i) => {
      const x = x0 + i * step;
      s.addShape(pres.shapes.OVAL, { x, y: y0, w: 0.4, h: 0.4, fill: { color: i === 2 ? C.or : C.nacht }, line: { color: C.weiss, width: 2 } });
      txt(s, p[0], { x: x - 0.3, y: y0 - 0.7, w: 2.0, h: 0.4, fontFace: F.xb, fontSize: 16, color: i === 2 ? C.or : C.nacht });
      txt(s, p[1], { x: x - 0.3, y: y0 + 0.6, w: 1.9, h: 0.35, fontFace: F.sb, fontSize: 14, color: C.nacht });
      txt(s, p[2], { x: x - 0.3, y: y0 + 0.95, w: 1.8, h: 1.0, fontSize: 11, color: C.grau });
    });
    card(s, M, 5.6, 11.8, 0.7, C.hell);
    txt(s, [{ text: 'Stufe 2 (nach Zielerreichung): ', options: { fontFace: F.sb, color: C.nacht } }, { text: 'mehr Videos, Ausbau auf LinkedIn und Google, größere Kampagnen.', options: { color: C.anth } }], { x: M + 0.3, y: 5.6, w: 11.2, h: 0.7, fontSize: 13, valign: 'middle' });
    footer(s, false);
    s.addNotes('Der Zeitpunkt ist ideal: Der Aufbaumonat fällt in den Oktober, und der Start am Tag des Einbruchschutzes gibt uns sofort ein starkes Thema.');
  }

  // ================= 24 ABSCHLUSS =================
  {
    const s = base(true);
    s.addImage({ path: `${IMG}/waves.png`, x: 9.2, y: 2.3, w: 4.3, h: 4.3 });
    kicker(s, 'Meine Bitte an Sie', true, M, 0.7);
    s.addText([{ text: 'Lassen Sie uns zeigen, ', options: { color: C.weiss, breakLine: true } }, { text: 'dass wir wach sind.', options: { color: C.or } }], { x: M, y: 1.2, w: 9, h: 1.5, margin: 0, fontFace: F.xb, fontSize: 40, valign: 'top', isTextBox: true });
    const d = [['1', 'Grünes Licht für den Start', 'Aufbau im Oktober, Startschuss zum Tag des Einbruchschutzes'], ['2', 'Rahmen und Werbebudget festlegen', 'besprechen wir gern persönlich'], ['3', 'Freigabe von Profilbild und Ansprache', 'Signal-Symbol aus dem Logo, „du“ auf Instagram']];
    d.forEach((p, i) => {
      const y = 3.15 + i * 1.0;
      s.addShape(pres.shapes.OVAL, { x: M, y, w: 0.55, h: 0.55, fill: { color: C.or }, line: { color: C.or } });
      txt(s, p[0], { x: M, y, w: 0.55, h: 0.55, fontFace: F.xb, fontSize: 16, color: C.weiss, align: 'center', valign: 'middle' });
      txt(s, p[1], { x: M + 0.8, y: y - 0.03, w: 7.8, h: 0.35, fontFace: F.sb, fontSize: 16, color: C.weiss });
      txt(s, p[2], { x: M + 0.8, y: y + 0.32, w: 7.8, h: 0.3, fontSize: 12, color: C.silber });
    });
    footer(s, true);
    s.addNotes('Abschluss mit drei klaren Entscheidungen, um die ich bitte. Danach Fragen. Unterlagen im Anhang: Marken-Kit (PDF), Vorlagen, Strategie-Dokument.');
  }

  await pres.writeFile({ fileName: OUT });
  console.log('written', OUT);
})();
