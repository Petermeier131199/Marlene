# Ratgeber „Hühner halten leicht gemacht"

Quelle des PDFs im Repo-Root (`Huehner-halten-leicht-gemacht.pdf`).

- `huehner-ratgeber.html` — der komplette Ratgeber als eine HTML-Datei (A4-Seiten, Print-CSS)
- `fonts/fonts-inline.css` — EB Garamond, Marcellus und Caveat als eingebettete WOFF2 (Base64),
  damit das Layout ohne Netzwerkzugriff identisch rendert

## Neu erzeugen

```bash
node -e "
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.cwd() + '/huehner-ratgeber.html', { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: '../Huehner-halten-leicht-gemacht.pdf', printBackground: true,
                margin: {top:'0',right:'0',bottom:'0',left:'0'}, preferCSSPageSize: true });
  await b.close();
})();
"
```

Chromium behält die `<a href>`-Ziele als klickbare Link-Annotationen im PDF.
