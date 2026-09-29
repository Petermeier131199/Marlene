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
    kicker(s, '01 · Ausgangslage', false);
    title(s, [{ text: 'Die Nische ist ' }, { text: 'frei.', o: true }], false);
    const stats = [
      ['ca. 1.059', 'Follower hat der größte regionale Wettbewerber (Pfättisch)'],
      ['ca. 150', 'Follower hat unsere Facebook-Seite'],
      ['17', 'Follower hat unsere LinkedIn-Seite'],
      ['5,0 ★', 'bei Google, aber nur 17 Bewertungen'],
    ];
    stats.forEach((st, i) => {
      const x = M + (i % 2) * 3.55, y = 2.15 + Math.floor(i / 2) * 2.2;
      card(s, x, y, 3.3, 1.95);
      txt(s, st[0], { x: x + 0.3, y: y + 0.28, w: 2.8, h: 0.75, fontFace: F.xb, fontSize: 34, color: C.or });
      txt(s, st[1], { x: x + 0.3, y: y + 1.05, w: 2.8, h: 0.75, fontSize: 13, color: C.grau });
    });
    txt(s, 'Was das bedeutet', { x: 8.2, y: 2.15, w: 4.4, h: 0.4, fontFace: F.sb, fontSize: 18, color: C.nacht });
    bullets(s, [
      'Kein Sicherheitstechnik-Betrieb in der Region nutzt Instagram ernsthaft.',
      'Unser Kanal hat aktuell keine feste Zuständigkeit.',
      [{ text: 'Mit ca. ' }, { text: '1.100 echten Followern', b: true }, { text: ' aus der Region wären wir die ' }, { text: 'Nummer 1.', b: true, o: true }],
      'Bewerber und Kunden prüfen uns online, bevor sie anrufen.',
    ], { x: 8.2, y: 2.7, w: 4.4, h: 3.6 }, C.anth, 15);
    footer(s, false);
    s.addNotes('Zahlen: Follower laut Suchmaschinen-Snippets (Stand Sept. 2026, ca.-Werte). Google-Bewertung Gaimersheim laut Das Örtliche. Kernbotschaft: Wir müssen nicht gegen große Accounts antreten, in unserer Region ist Platz 1 mit überschaubarem Aufwand erreichbar.');
  }

  // ================= 3 WARUM JETZT =================
  {
    const s = base(true);
    kicker(s, '02 · Warum jetzt', true);
    title(s, [{ text: 'Einbrüche steigen. ' }, { text: 'Fachkräfte fehlen.', o: true }], true);
    const st = [
      ['82.920', 'Wohnungseinbrüche 2025 in Deutschland (+5,7 %)'],
      ['3.806', 'Wohnungseinbrüche 2025 in Bayern (+5,6 %)'],
      ['3.850 €', 'durchschnittlicher Schaden pro Einbruch, so hoch wie nie'],
      ['24 %', 'der Lehrstellen im Handwerk Oberbayern blieben unbesetzt'],
    ];
    st.forEach((v, i) => {
      const x = M + i * 3.0;
      txt(s, v[0], { x, y: 2.5, w: 2.8, h: 0.9, fontFace: F.xb, fontSize: 40, color: C.or });
      txt(s, v[1], { x, y: 3.45, w: 2.6, h: 1.0, fontSize: 14, color: 'DDDDDD' });
    });
    card(s, M, 4.85, 11.8, 1.05, C.anth);
    iconCircle(s, 'FaCalendarDays', M + 0.3, 5.07, 0.6);
    txt(s, [{ text: '25.10.2026: Tag des Einbruchschutzes. ', options: { fontFace: F.sb, color: C.weiss } }, { text: 'Mit der Zeitumstellung beginnt die Einbruchsaison. Der perfekte Startschuss für unseren Kanal.', options: { color: 'DDDDDD' } }], { x: M + 1.15, y: 5.12, w: 10.4, h: 0.6, fontSize: 15, valign: 'middle' });
    txt(s, 'Quellen: PKS 2025 (BKA), StMI Bayern 16.03.2026, GDV 2025, HWK München (2023/24), polizei-beratung.de', { x: M, y: 6.25, w: 11.8, h: 0.3, fontSize: 10, color: C.grau });
    footer(s, true);
    s.addNotes('Zwei Probleme, eine Lösung: Mehr Einbrüche bedeuten mehr Beratungsbedarf, und uns fehlen Azubis und Fachkräfte. Instagram adressiert beides. Wichtig: 44,9 % der Einbrüche scheitern im Versuch, Sicherung wirkt. Das ist unsere positive Botschaft, wir machen keine Angst.');
  }

  // ================= 4 USP =================
  {
    const s = base(false);
    kicker(s, '03 · Was uns einzigartig macht', false);
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
    kicker(s, '04 · Markenkern', true);
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

  // ================= 6 ZIELGRUPPEN =================
  {
    const s = base(false);
    kicker(s, '05 · Zielgruppen', false);
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
      txt(s, p[1], { x: x + 2.2, y: y + 0.35, w: 1.2, h: 0.6, fontFace: F.xb, fontSize: 26, color: C.or, align: 'right' });
      txt(s, p[2], { x: x + 0.3, y: y + 1.2, w: 3.1, h: 0.45, fontFace: F.xb, fontSize: 18, color: C.nacht });
      txt(s, p[3], { x: x + 0.3, y: y + 1.7, w: 3.1, h: 0.75, fontSize: 13, color: C.grau });
      txt(s, p[4], { x: x + 0.3, y: y + 2.5, w: 3.1, h: 0.8, fontSize: 13, color: C.grau });
      card(s, x + 0.3, y + 3.5, 3.1, 0.5, C.nacht);
      txt(s, '→ ' + p[5], { x: x + 0.3, y: y + 3.5, w: 3.1, h: 0.5, fontFace: F.sb, fontSize: 12, color: C.weiss, align: 'center', valign: 'middle' });
    });
    txt(s, '+ 10 % Marke & Region für alle. Gewerbekunden erreichen wir später über LinkedIn (Stufe 2).', { x: M, y: 6.5, w: 11.8, h: 0.3, fontSize: 11, color: C.grau });
    footer(s, false);
    s.addNotes('Die Prozentzahlen geben den Anteil am Content an. Saisonal verschiebt sich das: Oktober bis März mehr Kundenthemen, Januar bis April und September mehr Azubi-Themen.');
  }

  // ================= 7 MARKEN-KIT =================
  {
    const s = base(false);
    kicker(s, '06 · Marken-Kit', false);
    title(s, [{ text: 'Das Logo bleibt. ' }, { text: 'Die Regeln sind neu.', o: true }], false);
    const sw = [['EB5A1B', 'Signal-Orange', '#EB5A1B', C.weiss], ['111111', 'Nacht', '#111111', C.weiss], ['222222', 'Anthrazit', '#222222', C.weiss], ['F4F4F4', 'Hellgrau', '#F4F4F4', C.nacht]];
    sw.forEach((c, i) => {
      const x = M + i * 1.95;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.05, w: 1.75, h: 1.75, rectRadius: 0.1, fill: { color: c[0] }, line: { color: c[0] === 'F4F4F4' ? 'DDDDDD' : c[0] } });
      txt(s, c[1], { x: x + 0.15, y: 3.05, w: 1.5, h: 0.3, fontFace: F.sb, fontSize: 12, color: c[3] });
      txt(s, c[2], { x: x + 0.15, y: 3.35, w: 1.5, h: 0.3, fontSize: 11, color: c[3] });
    });
    txt(s, '60 % Nacht/Weiß · 30 % Grau · 10 % Orange. Orange markiert das Wichtigste, nie alles.', { x: M, y: 3.95, w: 7.6, h: 0.35, fontSize: 13, color: C.grau });
    txt(s, 'Poppins', { x: M, y: 4.55, w: 4, h: 0.8, fontFace: F.xb, fontSize: 44, color: C.nacht });
    txt(s, 'ExtraBold für Headlines · SemiBold für Sublines · Regular für Text · Light für Kicker. Kostenlos, in Canva vorhanden.', { x: M, y: 5.4, w: 7.4, h: 0.7, fontSize: 13, color: C.grau });
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
    kicker(s, '07 · Drei Vorlagen-Welten', false);
    title(s, [{ text: 'Drei Welten. ' }, { text: 'Eine DNA.', o: true }], false);
    const w3 = [['karussell-schwachstellen-4', 'Nachtschicht', 'Kunden · Leitstelle · Einsätze'], ['post-pks-2025', 'Wissen', 'Tipps · Mythen · Zahlen'], ['post-karriere-ausbildung', 'Karriere', 'Azubis · Fachkräfte · Team']];
    w3.forEach((t, i) => {
      const x = M + 0.2 + i * 4.0, h = 3.9, w = h * 1080 / 1350;
      s.addImage({ path: V(t[0]), x, y: 1.95, w, h, shadow: { type: 'outer', color: '000000', opacity: 0.25, blur: 8, offset: 3, angle: 90 } });
      txt(s, t[1], { x, y: 5.95, w: 3.2, h: 0.4, fontFace: F.xb, fontSize: 17, color: C.nacht });
      txt(s, t[2], { x, y: 6.35, w: 3.2, h: 0.3, fontSize: 12, color: C.grau });
    });
    footer(s, false);
    s.addNotes('Jede Zielgruppe hat ihren eigenen Look. Durch Farben, Schrift und Signal-Elemente bleibt alles als Poleschak erkennbar. Die Vorlagen sind fertig und werden in Canva als Markenvorlagen angelegt.');
  }

  // ================= 9 PROFIL =================
  {
    const s = base(true);
    kicker(s, '08 · Profil-Relaunch', true);
    title(s, [{ text: 'Der erste Eindruck in ' }, { text: '3 Sekunden.', o: true }], true);
    const ih = 4.7, iw = ih * igMeta.width / igMeta.height;
    s.addImage({ path: `${IMG}/ig-mockup.png`, x: M, y: 1.95, w: iw, h: ih });
    const pts = [['FaBolt', 'Profilbild: das Signal', 'wiedererkennbar im Feed und in Stories'], ['FaListCheck', 'Bio in 4 Zeilen', 'Versprechen · Leistungen · seit 1975 & Region · Handlung'], ['FaStar', '5 Highlights', 'Über uns · Leitstelle · Karriere · Tipps · Kunden'], ['FaWhatsapp', 'WhatsApp als Haupt-Button', 'niedrigste Hürde für Kunden und Azubis'], ['FaLock', 'Kein Notrufkanal', 'automatische Antwort verweist auf 110 und die Leitstelle']];
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
    kicker(s, '09 · Strategie', false);
    title(s, 'Fünf Content-Säulen.', false);
    const pil = [['FaHeadset', 'Aus der Leitstelle', 'Nachtschicht, Alarmablauf, Technik', 25], ['FaLightbulb', 'Sicher wissen', 'Tipps, Mythen, Zahlen, Förderung', 30], ['FaUserGraduate', 'Mach Alarm. Beruflich.', 'Azubi-Alltag, Jobs, Benefits', 30], ['FaPeopleGroup', 'Familie Poleschak', 'Team, 50 Jahre, Region', 10], ['FaStar', 'Vertrauen', 'Zertifikate, Bewertungen, Referenzen', 5]];
    pil.forEach((p, i) => {
      const y = 2.05 + i * 0.88;
      iconCircle(s, p[0], M, y, 0.6);
      txt(s, p[1], { x: M + 0.8, y: y - 0.02, w: 4.5, h: 0.35, fontFace: F.sb, fontSize: 15, color: C.nacht });
      txt(s, p[2], { x: M + 0.8, y: y + 0.32, w: 4.5, h: 0.3, fontSize: 12, color: C.grau });
      txt(s, p[3] + ' %', { x: 5.9, y: y + 0.05, w: 1, h: 0.45, fontFace: F.xb, fontSize: 18, color: C.or, align: 'right' });
    });
    s.addChart(pres.charts.DOUGHNUT, [{ name: 'Anteil', labels: pil.map(p => p[1]), values: pil.map(p => p[3]) }], {
      x: 7.6, y: 1.8, w: 4.9, h: 4.6, holeSize: 55, chartColors: [C.nacht, C.or, C.orH, C.grau, C.silber],
      showLegend: false, showValue: false, showPercent: true, dataLabelColor: C.weiss, dataLabelFontSize: 12, dataLabelFontFace: F.sb,
      showTitle: false,
    });
    footer(s, false);
    s.addNotes('Die Anteile beziehen sich auf die Feed-Beiträge. Die Leitstellen-Säule ist klein, aber am wichtigsten für die Wiedererkennung.');
  }

  // ================= 11 FORMATE & RHYTHMUS =================
  {
    const s = base(false);
    kicker(s, '10 · Formate & Rhythmus', false);
    title(s, [{ text: '3 Posts pro Woche. ' }, { text: 'Vorgeplant.', o: true }], false);
    [['4', 'Reels'], ['4', 'Karussells'], ['4', 'Bild-Posts'], ['13', 'Story-Tage']].forEach((v, i) => {
      const x = M + i * 1.55;
      txt(s, v[0], { x, y: 2.1, w: 1.4, h: 0.9, fontFace: F.xb, fontSize: 44, color: C.or });
      txt(s, v[1], { x, y: 2.95, w: 1.4, h: 0.3, fontFace: F.sb, fontSize: 13, color: C.nacht });
    });
    txt(s, 'pro Monat', { x: M, y: 3.3, w: 3, h: 0.3, fontSize: 12, color: C.grau });
    const days = [['Mo', 'Story'], ['Di', 'Reel'], ['Mi', 'Story'], ['Do', 'Karussell'], ['Fr', 'Story'], ['Sa', ''], ['So', 'Bild-Post']];
    days.forEach((d, i) => {
      const x = M + i * 1.7, feed = ['Reel', 'Karussell', 'Bild-Post'].includes(d[1]);
      card(s, x, 4.05, 1.55, 1.55, feed ? C.nacht : (d[1] ? C.hell : 'FAFAFA'));
      txt(s, d[0], { x, y: 4.2, w: 1.55, h: 0.45, fontFace: F.xb, fontSize: 20, color: feed ? C.weiss : C.nacht, align: 'center' });
      if (d[1]) txt(s, d[1], { x, y: 4.9, w: 1.55, h: 0.35, fontFace: F.sb, fontSize: 12, color: feed ? C.or : C.grau, align: 'center' });
    });
    bullets(s, [
      [{ text: '18–20 Uhr', b: true }, { text: ' zum Start, nach 4 Wochen anhand der Insights nachjustieren' }],
      [{ text: 'Meta Business Suite', b: true }, { text: ' (kostenlos): alles vorgeplant, passt zum Nachtdienst' }],
      [{ text: 'Automatisch auch auf Facebook', b: true }, { text: ': erreicht Eltern und Kunden ab 55, ohne Mehraufwand' }],
    ], { x: 7.1, y: 2.05, w: 5.5, h: 1.8 }, C.anth, 13);
    footer(s, false);
    s.addNotes('Paket S passt genau in 43 Stunden pro Monat. Die Rhythmus-Tage sind Startwerte, die wir nach den ersten Daten optimieren.');
  }

  // ================= 12 SERIEN =================
  {
    const s = base(true);
    kicker(s, '11 · Serien', true);
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
    kicker(s, '12 · Redaktionsplan', false);
    title(s, 'So sieht der November 2026 aus.', false);
    const rows = [['Di 03.11.', 'Reel', '„3 Uhr nachts“ #1: Ein Alarm geht ein', 'Leitstelle'], ['Do 05.11.', 'Karussell', 'Dunkle Jahreszeit: 5 Schwachstellen am Haus', 'Sicher wissen'], ['So 08.11.', 'Bild', 'Das ist die Nachtschicht', 'Familie'], ['Di 10.11.', 'Reel', '„Frag den Azubi“ #1: Was machst du eigentlich?', 'Karriere'], ['Fr 13.11.', 'Karussell', 'Rauchmeldertag: Rauchmelder testen', 'Sicher wissen'], ['So 15.11.', 'Bild', '5,0 ★ bei Google: Danke!', 'Vertrauen'], ['Di 17.11.', 'Reel', 'Mythos: Die Smart-Home-Kamera reicht doch', 'Sicher wissen'], ['Do 19.11.', 'Karussell', 'Ausbildung Elektroniker/in in 6 Slides', 'Karriere'], ['So 22.11.', 'Bild', 'Wir suchen: Servicetechniker (m/w/d)', 'Karriere'], ['Di 24.11.', 'Reel', '„30 Sekunden Technik“: Ein Melder entsteht', 'Leitstelle'], ['Do 26.11.', 'Karussell', 'Fast jeder 2. Einbruch scheitert (PKS)', 'Sicher wissen'], ['So 29.11.', 'Bild', 'Seit 1975: Familie Poleschak', 'Familie']];
    const hdr = ['Datum', 'Format', 'Thema', 'Säule'].map(h => ({ text: h, options: { bold: true, color: C.weiss, fill: { color: C.nacht }, fontFace: F.sb } }));
    const body = rows.map((r, i) => r.map((c, j) => ({ text: c, options: { color: j === 1 && c === 'Reel' ? C.or : C.anth, bold: j === 1 && c === 'Reel', fill: { color: i % 2 ? C.weiss : C.hell } } })));
    s.addTable([hdr, ...body], { x: M, y: 1.85, w: 11.8, colW: [1.5, 1.5, 6.3, 2.5], fontFace: F.rg, fontSize: 11, rowH: 0.33, border: { type: 'none' }, margin: [0.02, 0.1, 0.02, 0.1], valign: 'middle' });
    footer(s, false);
    s.addNotes('Konkreter Plan für den ersten vollen Monat. Der Rauchmeldertag am Freitag, 13.11., ist ein bundesweiter Aktionstag. Stories kommen jeweils montags, mittwochs und freitags dazu.');
  }

  // ================= 14 JAHRESKALENDER =================
  {
    const s = base(false);
    kicker(s, '13 · Jahresplan', false);
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
    kicker(s, '14 · Recruiting-Kampagne', false, M, 0.55, C.nacht);
    s.addText([{ text: 'Mach Alarm. ', options: { color: C.weiss } }, { text: 'Beruflich.', options: { color: C.nacht } }], { x: M, y: 0.95, w: 11, h: 0.9, margin: 0, fontFace: F.xb, fontSize: 38, isTextBox: true });
    const ph = [['1 · Aufmerksamkeit', 'Jan.–Feb.', '„Frag den Azubi“, Tag als Azubi, Technik-Reels', 'organisch'], ['2 · Bewerbung', 'Feb.–Apr.', 'Beste Reels werden beworben, Karussell „Ausbildung in 6 Slides“', '250 €/Monat'], ['3 · Messe & Herbst', 'Sep.–Okt.', 'Ausbildungsplatzbörse, neue Azubis stellen sich vor', '200 €/Monat'], ['Fachkräfte', 'bei offenen Stellen', '„Kollege erzählt“, Einblick Leitstelle', '150 €/Monat']];
    ph.forEach((p, i) => {
      const x = M + i * 2.95;
      card(s, x, 2.1, 2.75, 2.9, C.nacht);
      txt(s, p[0], { x: x + 0.25, y: 2.3, w: 2.3, h: 0.35, fontFace: F.sb, fontSize: 14, color: C.or });
      txt(s, p[1], { x: x + 0.25, y: 2.7, w: 2.3, h: 0.3, fontSize: 11, color: C.silber });
      txt(s, p[2], { x: x + 0.25, y: 3.15, w: 2.3, h: 1.1, fontSize: 12, color: C.weiss });
      txt(s, p[3], { x: x + 0.25, y: 4.45, w: 2.3, h: 0.35, fontFace: F.sb, fontSize: 13, color: C.weiss });
    });
    card(s, M, 5.35, 3.9, 0.6, C.nacht); txt(s, 'Azubis → Praktikum per WhatsApp', { x: M, y: 5.35, w: 3.9, h: 0.6, fontFace: F.sb, fontSize: 13, color: C.weiss, align: 'center', valign: 'middle' });
    card(s, M + 4.1, 5.35, 3.9, 0.6, C.nacht); txt(s, 'Fachkräfte → Bewerbung in 60 Sekunden', { x: M + 4.1, y: 5.35, w: 3.9, h: 0.6, fontFace: F.sb, fontSize: 13, color: C.weiss, align: 'center', valign: 'middle' });
    txt(s, 'Anzeigen immer (m/w/d), ohne Ausschluss nach Alter oder Geschlecht (AGG). Angesprochen wird über Region, Interessen und Gestaltung.', { x: M, y: 6.15, w: 8.3, h: 0.5, fontSize: 11, color: C.nacht });
    s.addImage({ path: LOGO_POS, x: M, y: H - 0.62, w: 0.36 / LOGO_R, h: 0.36 });
    txt(s, String(pageNo).padStart(2, '0'), { x: W - M - 1, y: H - 0.55, w: 1, h: 0.3, fontFace: F.lt, fontSize: 11, color: C.nacht, align: 'right', charSpacing: 3 });
    s.addNotes('Niedrige Hürden sind der Schlüssel: kein Anschreiben, kein Formular-Marathon. Die Rückmeldung an Bewerber innerhalb von 48 Stunden übernimmt die Personalabteilung, das ist nicht Teil des Minijobs.');
  }

  // ================= 16 KUNDEN & WERBUNG =================
  {
    const s = base(false);
    kicker(s, '15 · Kunden & Werbung', false);
    title(s, [{ text: 'Werbung, ' }, { text: 'bewusst einfach.', o: true }], false);
    card(s, M, 2.0, 5.6, 4.35, C.nacht);
    txt(s, 'Kundenkampagne', { x: M + 0.35, y: 2.25, w: 5, h: 0.35, fontFace: F.lt, fontSize: 12, color: C.silber, charSpacing: 3 });
    txt(s, '„Kostenlose Sicherheitsberatung“', { x: M + 0.35, y: 2.65, w: 5, h: 0.5, fontFace: F.xb, fontSize: 20, color: C.weiss });
    bullets(s, ['Okt.–März (Einbruchsaison), 250 €/Monat', 'Umkreis ca. 25 km um Gaimersheim & Pfaffenhofen', 'Beste Karussells und „3 Uhr nachts“-Reels', [{ text: 'Stichwort „Instagram“', b: true }, { text: ' per WhatsApp: jede Anfrage messbar' }], 'Weiterleitung an den Vertrieb am selben Tag'], { x: M + 0.35, y: 3.35, w: 5, h: 2.8 }, C.weiss, 13);
    txt(s, 'So läuft es', { x: 6.9, y: 2.0, w: 5, h: 0.35, fontFace: F.sb, fontSize: 16, color: C.nacht });
    [['1', 'Organisch posten'], ['2', 'Nach 3–5 Tagen den besten Beitrag „bewerben“'], ['3', 'Ergebnis im Monatsreport festhalten']].forEach((t, i) => {
      const y = 2.5 + i * 0.62;
      s.addShape(pres.shapes.OVAL, { x: 6.9, y, w: 0.45, h: 0.45, fill: { color: C.or }, line: { color: C.or } });
      txt(s, t[0], { x: 6.9, y, w: 0.45, h: 0.45, fontFace: F.xb, fontSize: 14, color: C.weiss, align: 'center', valign: 'middle' });
      txt(s, t[1], { x: 7.5, y, w: 5.1, h: 0.45, fontSize: 13, valign: 'middle' });
    });
    s.addChart(pres.charts.BAR, [{ name: 'Budget', labels: ['Kunden', 'Azubis', 'Fachkräfte'], values: [1500, 1400, 900] }], {
      x: 6.8, y: 4.4, w: 5.8, h: 1.95, barDir: 'bar', chartColors: [C.or], showValue: true, dataLabelFormatCode: '#,##0 "€"', dataLabelColor: C.anth, dataLabelFontSize: 11, dataLabelPosition: 'outEnd',
      catAxisLabelColor: C.anth, catAxisLabelFontSize: 11, valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false,
      showTitle: true, title: 'Werbebudget 3.800 € pro Jahr', titleFontSize: 12, titleColor: C.nacht, titleFontFace: F.sb, valAxisMaxVal: 1900,
    });
    footer(s, false);
    s.addNotes('Mit etwa 2 Stunden pro Monat für Werbeanzeigen bauen wir keine komplexen Kampagnen. Geld fließt nur in Beiträge, die organisch schon funktionieren. Agentur-Richtwerte: 20–60 € pro Lead, 10–18 € pro Bewerbung. Wir rechnen vorsichtig mit dem doppelten Preis.');
  }

  // ================= 17 VORLAGEN =================
  {
    const s = base(false, C.panel);
    kicker(s, '16 · Vorlagen', false);
    title(s, [{ text: '19 Vorlagen. ' }, { text: 'Fertig.', o: true }], false);
    const imgs = [['reel-cover-3-uhr-nachts', 9 / 16], ['karussell-schwachstellen-1', 0.8], ['karussell-schwachstellen-2', 0.8], ['post-stelle-servicetechniker', 0.8], ['story-umfrage', 9 / 16]];
    let x = M; const h = 3.05;
    imgs.forEach(im => { const w = h * im[1]; s.addImage({ path: V(im[0]), x, y: 1.95, w, h, shadow: { type: 'outer', color: '000000', opacity: 0.22, blur: 6, offset: 2, angle: 90 } }); x += w + 0.22; });
    txt(s, 'Reel-Cover · Karussell · Posts · Stories · 5 Highlight-Cover. Dazu Bildunterschriften, Reel-Drehbuch, Stellenanzeige, Antwortbausteine und Einwilligungsvorlage. In Canva als Markenvorlagen angelegt, entsteht ein Post in ca. 10 Minuten.', { x: M, y: 5.35, w: 11.8, h: 0.8, fontSize: 13, color: C.anth });
    footer(s, false);
    s.addNotes('Alle Vorlagen liegen in Originalgröße vor. Fotoplatzhalter werden mit echten Bildern aus dem Team gefüllt, nach Einwilligung.');
  }

  // ================= 18 ZIELE =================
  {
    const s = base(true);
    kicker(s, '17 · Ziele für 12 Monate', true);
    title(s, [{ text: 'Messbar. ' }, { text: 'Nicht gefühlt.', o: true }], true);
    const k = [['1.100', 'Follower aus der Region, damit Nr. 1'], ['≥ 20', 'Bewerbungen pro Jahr über Social Media'], ['≥ 1', 'Einstellung pro Jahr über Social Media'], ['≥ 3', 'Kundenanfragen pro Monat (ab Monat 4)'], ['17 → 40', 'Google-Bewertungen'], ['≥ 2 %', 'Engagement-Rate (Branche Ø 0,48 %)']];
    k.forEach((v, i) => {
      const x = M + (i % 3) * 4.0, y = 2.0 + Math.floor(i / 3) * 1.9;
      card(s, x, y, 3.75, 1.65, C.anth);
      txt(s, v[0], { x: x + 0.3, y: y + 0.2, w: 3.2, h: 0.75, fontFace: F.xb, fontSize: 34, color: C.or });
      txt(s, v[1], { x: x + 0.3, y: y + 0.98, w: 3.2, h: 0.55, fontSize: 13, color: C.weiss });
    });
    txt(s, 'Gemessen über: Stichwort „Instagram“ · „Wie sind Sie auf uns aufmerksam geworden?“ · Monatsreport auf 1 Seite · Nullmessung am ersten Tag', { x: M, y: 5.95, w: 11.8, h: 0.35, fontSize: 12, color: C.silber });
    footer(s, true);
    s.addNotes('Die Ziele gelten für Stufe 1 (Paket S). Nach der Nullmessung justieren wir die Follower- und Engagement-Ziele falls nötig nach. Benchmark Engagement: Socialinsider 2026.');
  }

  // ================= 19 MODELL / STUNDEN =================
  {
    const s = base(false);
    kicker(s, '18 · Das Modell', false);
    title(s, [{ text: 'Stufe 1: Minijob. ' }, { text: '43 Stunden im Monat.', o: true }], false);
    card(s, M, 2.0, 4.6, 4.4, C.nacht);
    txt(s, 'Bei der Alarmanlagen Poleschak GmbH', { x: M + 0.35, y: 2.25, w: 4, h: 0.35, fontFace: F.lt, fontSize: 11, color: C.silber, charSpacing: 2 });
    txt(s, 'ca. 905 €', { x: M + 0.35, y: 2.7, w: 4, h: 0.8, fontFace: F.xb, fontSize: 40, color: C.or });
    txt(s, 'Kosten pro Monat für die Firma (603 € Minijob inkl. ca. 31 % Abgaben + Sachbezug, Internetpauschale)', { x: M + 0.35, y: 3.5, w: 3.9, h: 0.8, fontSize: 12, color: C.weiss });
    bullets(s, ['Paket S: 12 Feed-Beiträge + 13 Story-Tage pro Monat', 'Arbeitszeit dokumentiert, getrennt von SWD-Schichten', 'Vergütung dynamisch an die Minijob-Grenze'], { x: M + 0.35, y: 4.5, w: 3.9, h: 1.8 }, C.weiss, 12);
    const tasks = [['Reels', 12], ['Karussells', 6], ['Community', 5.4], ['Material-Vorrat', 4.3], ['Story-Tage', 3.25], ['Planung & Freigabe', 3.25], ['Bild-Posts', 3], ['Werbeanzeigen', 2.2], ['Reporting', 2.2]];
    s.addChart(pres.charts.BAR, [{ name: 'Stunden', labels: tasks.map(t => t[0]), values: tasks.map(t => t[1]) }], {
      x: 5.7, y: 1.9, w: 6.9, h: 4.6, barDir: 'bar', chartColors: [C.or], showValue: true, dataLabelFormatCode: '0.0 "h"', dataLabelPosition: 'outEnd', dataLabelFontSize: 11, dataLabelColor: C.anth,
      catAxisLabelColor: C.anth, catAxisLabelFontSize: 11, catAxisOrientation: 'maxMin', valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false,
      showTitle: true, title: 'Stunden pro Monat: ca. 41,6 von max. 43', titleFontSize: 12, titleColor: C.nacht, titleFontFace: F.sb, valAxisMaxVal: 14,
    });
    footer(s, false);
    s.addNotes('Ich bin bei der SWD angestellt. Social Media übernehme ich als Minijob bei der Poleschak GmbH, einem eigenen Arbeitgeber. Das ist für die Firma die günstigste Variante. Vorab prüfen lassen: Lohnbüro bzw. Steuerberater (getrennte Arbeitgeber bei gleicher Inhaberin). Aufbaumonat: nur 2 statt 4 Reels, damit die 43 h reichen.');
  }

  // ================= 20 INVESTITION =================
  {
    const s = base(false);
    kicker(s, '19 · Investition & Gegenwert', false);
    title(s, [{ text: 'Rechnet sich ab ' }, { text: 'ca. 1 Auftrag pro Monat.', o: true }], false);
    const st = [['15.300 €', 'Gesamtkosten pro Jahr', 'Minijob 10.900 € · Werbung 3.800 € · Ausstattung 600 €'], ['≈ 1', 'Auftrag pro Monat reicht', 'bei angenommenen 1.200 € Deckungsbeitrag pro Auftrag'], ['1.500–3.000 €', 'spart jede Einstellung', 'typische Vollkosten pro Einstellung über Social Recruiting']];
    st.forEach((v, i) => {
      const x = M + i * 4.0;
      txt(s, v[0], { x, y: 2.0, w: 3.8, h: 0.8, fontFace: F.xb, fontSize: 32, color: C.or });
      txt(s, v[1], { x, y: 2.8, w: 3.6, h: 0.35, fontFace: F.sb, fontSize: 14, color: C.nacht });
      txt(s, v[2], { x, y: 3.15, w: 3.6, h: 0.6, fontSize: 11, color: C.grau });
    });
    card(s, M, 4.1, 5.75, 2.3, C.hell); card(s, M + 6.05, 4.1, 5.75, 2.3, C.nacht);
    txt(s, 'Agentur (Instagram)', { x: M + 0.3, y: 4.3, w: 5, h: 0.35, fontFace: F.sb, fontSize: 15, color: C.nacht });
    bullets(s, ['ca. 800–1.800 € pro Monat, Werbebudget extra', 'Nicht vor Ort, Drehtage kosten extra', 'Kein Zugang zur Leitstelle bei Nacht', 'Braucht trotzdem eine interne Ansprechperson'], { x: M + 0.3, y: 4.75, w: 5.2, h: 1.6 }, C.anth, 12);
    txt(s, 'Intern (Minijob)', { x: M + 6.35, y: 4.3, w: 5, h: 0.35, fontFace: F.sb, fontSize: 15, color: C.or });
    bullets(s, ['ca. 905 € pro Monat, planbar', 'Täglich vor Ort, spontane Momente', 'Content aus erster Hand: die Nachtschicht', 'Echter Recruiting-Content von innen'], { x: M + 6.35, y: 4.75, w: 5.2, h: 1.6 }, C.weiss, 12);
    footer(s, false);
    s.addNotes('Ehrlich gesagt: Eine Agentur ist nicht teurer. Der Unterschied liegt in Menge und Echtheit des Materials. Die 1.200 € Deckungsbeitrag sind eine Annahme, bitte mit Ihren Zahlen prüfen. Recruiting-Vollkosten: Agentur-Richtwerte (webtak.de).');
  }

  // ================= 21 WARUM ICH =================
  {
    const s = base(true);
    kicker(s, '20 · Warum intern', true);
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
    kicker(s, '21 · Voraussetzungen & Spielregeln', false);
    title(s, 'Was es braucht, damit es funktioniert.', false);
    const L = [['FaKey', 'Admin-Zugang', 'Instagram, Facebook, Meta Business Suite + Werbekonto'], ['FaHandshake', 'Freigabe in 24 h', 'Wochenplan montags, eine feste Ansprechperson'], ['FaCamera', 'Foto-Einwilligungen', 'schriftlich, freiwillig, jederzeit widerrufbar (Vorlage fertig)'], ['FaClock', 'Arbeitszeit getrennt', 'Content nur in Minijob-Zeit, nie während der SWD-Schicht']];
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
    kicker(s, '22 · Fahrplan', false);
    title(s, [{ text: 'Von der Entscheidung zum ' }, { text: 'Start am 25.10.', o: true }], false);
    const st = [['07.10.', 'Entscheidung', 'Freigabe von Modell, Budget, Profilbild'], ['Okt.', 'Aufbaumonat', 'Zugang, Nullmessung, Profil, Canva, Einwilligungen'], ['25.10.', 'Start', 'Tag des Einbruchschutzes, erster großer Post'], ['Jan. 2027', 'Azubi-Kampagne', '„Mach Alarm. Beruflich.“'], ['Apr. 2027', '6-Monats-Review', 'Zahlen auf den Tisch, Entscheidung Stufe 2'], ['Okt. 2027', 'Jahresbilanz', '12 Monate, alle Ziele im Check']];
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
    txt(s, [{ text: 'Stufe 2 (nach Zielerreichung): ', options: { fontFace: F.sb, color: C.nacht } }, { text: 'Paket M mit 9 Reels/Monat, Ausbau auf LinkedIn und Google, durch Umschichten von Stunden zwischen SWD und Poleschak.', options: { color: C.anth } }], { x: M + 0.3, y: 5.6, w: 11.2, h: 0.7, fontSize: 13, valign: 'middle' });
    footer(s, false);
    s.addNotes('Der Zeitpunkt ist ideal: Der Aufbaumonat fällt in den Oktober, und der Start am Tag des Einbruchschutzes gibt uns sofort ein starkes Thema.');
  }

  // ================= 24 ABSCHLUSS =================
  {
    const s = base(true);
    s.addImage({ path: `${IMG}/waves.png`, x: 9.2, y: 2.3, w: 4.3, h: 4.3 });
    kicker(s, 'Meine Bitte an Sie', true, M, 0.7);
    s.addText([{ text: 'Lassen Sie uns zeigen, ', options: { color: C.weiss, breakLine: true } }, { text: 'dass wir wach sind.', options: { color: C.or } }], { x: M, y: 1.2, w: 9, h: 1.5, margin: 0, fontFace: F.xb, fontSize: 40, valign: 'top', isTextBox: true });
    const d = [['1', 'Start des Minijobs bei der Poleschak GmbH', 'ab [Datum], ideal Mitte Oktober für den Start am 25.10.'], ['2', 'Werbebudget von 3.800 € pro Jahr', 'nur für Beiträge, die nachweislich funktionieren'], ['3', 'Freigabe von Profilbild und „du“ auf Instagram', 'Signal-Symbol aus dem Logo, Ansprache wie besprochen']];
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
