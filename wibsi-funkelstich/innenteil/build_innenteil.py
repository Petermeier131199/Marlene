"""Innenteil Wibsi Funkelstich als druckfertiges PDF (Entwurf).

Format 13,5 x 21,5 cm + 3 mm Beschnitt, Kapitelbilder randabfallend auf der
linken Seite, Kapitelanfang gegenüber rechts. Alle Textseiten rein schwarz/grau,
damit nur die Bildseiten als Farbseiten zählen.
"""
import glob
import html
import os
import re
import sys

import markdown
from weasyprint import HTML

D = os.path.dirname(os.path.abspath(__file__))
KAP = sys.argv[1] if len(sys.argv) > 1 else '/home/user/Marlene/wibsi-funkelstich/lektorat'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, 'Wibsi_Funkelstich_Innenteil_ENTWURF.pdf')
IMG = os.environ.get('WIBSI_IMG', os.path.join(D, 'img'))
FONTS = os.path.expanduser('~/.fonts')


def clean(md):
    md = re.sub(r'^\[NEU GESCHRIEBEN[^\]]*\]\s*$', '', md, flags=re.M)
    md = re.sub(r'^\[/NEU\]\s*$', '', md, flags=re.M)
    md = re.sub(r'\[NEU –[^\]]*\]\s*', '', md)
    md = md.replace(' [/NEU]', '').replace('[/NEU]', '')
    md = re.sub(r'^\*\*ENDE\*\*\s*$', '', md, flags=re.M)
    return md.strip()


def chapter(path):
    md = clean(open(path, encoding='utf-8').read())
    m = re.match(r'^#\s*(\d+)\s*[–-]\s*(.+)$', md.splitlines()[0])
    num, title = m.group(1), m.group(2).strip()
    body = '\n'.join(md.splitlines()[1:]).strip()
    body_html = markdown.markdown(body)
    # erster Absatz bekommt die Initiale
    body_html = re.sub(r'<p>([„»"]?\w)', lambda m: '<p class="first"><span class="dc">' + m.group(1) + '</span>', body_html, count=1)
    return int(num), title, body_html


CSS = f"""
@font-face {{ font-family: 'EBG'; src: url(file://{FONTS}/EBG-400.ttf); font-weight: 400; }}
@font-face {{ font-family: 'EBG'; src: url(file://{FONTS}/EBG-500.ttf); font-weight: 500; }}
@font-face {{ font-family: 'EBG'; src: url(file://{FONTS}/EBG-600.ttf); font-weight: 600; }}
@font-face {{ font-family: 'EBG'; src: url(file://{FONTS}/EBG-400i.ttf); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: 'EBG'; src: url(file://{FONTS}/EBG-500i.ttf); font-weight: 500; font-style: italic; }}
@font-face {{ font-family: 'Cinzel'; src: url(file://{FONTS}/cinzel.ttf); font-weight: 700; }}
@font-face {{ font-family: 'Corm'; src: url(file://{FONTS}/CG-Italic600.ttf); font-weight: 600; font-style: italic; }}

@page {{
  size: 135mm 215mm; bleed: 3mm;
  margin: 17mm 15mm 21mm 20mm;
  @bottom-center {{ content: counter(page); font: 9pt 'EBG'; color: #333; margin-top: 6mm; vertical-align: top; }}
}}
@page :left  {{ margin-left: 15mm; margin-right: 20mm; }}
@page :right {{ margin-left: 20mm; margin-right: 15mm; }}
@page :blank {{ @bottom-center {{ content: none; }} }}
@page front {{ @bottom-center {{ content: none; }} }}
@page opener {{ @bottom-center {{ content: none; }} }}
@page bild {{ margin: 0; @bottom-center {{ content: none; }} }}

html {{ font-family: 'EBG'; font-size: 11.2pt; line-height: 15.4pt; color: #000; hyphens: auto; }}
body {{ margin: 0; }}
p {{ margin: 0; text-align: justify; text-indent: 1.2em; orphans: 2; widows: 2; }}
p.first, blockquote p, li p {{ text-indent: 0; }}
.dc {{ float: left; font-family: 'EBG'; font-weight: 500; font-size: 43pt; line-height: 33pt; margin: 1.5pt 2.5pt -2pt 0; color: #111; }}
blockquote {{ margin: 8pt 6mm; font-style: italic; }}
blockquote p {{ text-align: left; margin-bottom: 4pt; }}
ul {{ margin: 6pt 0 6pt 4mm; padding: 0; list-style: none; }}
li {{ margin-bottom: 2pt; padding-left: 4mm; text-indent: -4mm; }}
li::before {{ content: '✦  '; font-size: 7pt; vertical-align: 1pt; }}
strong {{ font-weight: 600; }}

.bild {{ page: bild; break-before: left; position: relative; height: 215mm; }}
.bild img {{ position: absolute; top: -3mm; left: -3mm; width: 141mm; height: 221mm; object-fit: cover; }}

.kapitel {{ break-before: right; }}
.kopf {{ page: opener; text-align: center; padding-top: 24mm; margin-bottom: 11mm; }}
.kopf .nr {{ font-family: 'EBG'; font-weight: 500; font-size: 32pt; line-height: 1; font-variant-numeric: lining-nums; color: #111; }}
.kopf .orn {{ font-size: 8pt; letter-spacing: 6pt; margin: 6pt 0 5pt; color: #444; }}
.kopf .titel {{ font-family: 'Corm'; font-style: italic; font-weight: 600; font-size: 20pt; line-height: 1.15; }}

.front {{ page: front; break-before: page; text-align: center; }}
.front.recto {{ break-before: right; }}
.schmutz {{ padding-top: 55mm; font-family: 'Cinzel'; font-weight: 700; font-size: 17pt; letter-spacing: .5pt; }}
.tp-autor {{ padding-top: 22mm; font-family: 'Cinzel'; font-weight: 700; font-size: 11pt; letter-spacing: 2pt; }}
.tp-titel {{ margin-top: 20mm; font-family: 'Cinzel'; font-weight: 700; font-size: 25pt; line-height: 1.15; }}
.tp-unter {{ margin-top: 7mm; font-family: 'Corm'; font-style: italic; font-weight: 600; font-size: 14pt; }}
.tp-orn {{ margin-top: 12mm; font-size: 9pt; letter-spacing: 8pt; }}
.tp-genre {{ margin-top: 10mm; font-size: 11pt; font-style: italic; }}
.impressum {{ text-align: left; font-size: 8pt; line-height: 11pt; padding-top: 112mm; }}
.impressum p {{ text-align: left; text-indent: 0; margin-bottom: 5pt; }}
.widmung {{ padding-top: 60mm; font-style: italic; font-size: 12.5pt; }}
.platzhalter {{ background: #ececec; }}

.ende {{ text-align: center; margin-top: 12mm; font-family: 'Cinzel'; font-weight: 700; font-size: 10pt; letter-spacing: 3pt; }}

.autorin {{ page: front; break-before: right; text-align: center; padding-top: 6mm; }}
.autorin h2 {{ font-family: 'Cinzel'; font-weight: 700; font-size: 13pt; letter-spacing: 1pt; margin: 0 0 7mm; }}
.autorin img {{ width: 62mm; height: 82.7mm; object-fit: cover; }}
.autorin .vita {{ margin: 7mm 4mm 0; text-align: center; text-indent: 0; font-size: 11pt; line-height: 15pt; }}
.autorin .credit {{ margin-top: 4mm; font-size: 7.5pt; color: #444; text-indent: 0; text-align: center; }}
"""


def front_matter():
    return f"""
<section class="front"><div class="schmutz">Wibsi Funkelstich</div></section>
<section class="front recto">
  <div class="tp-autor">GABI SCHOLZ</div>
  <div class="tp-titel">Wibsi<br>Funkelstich</div>
  <div class="tp-unter">Auf der Suche nach der verlorenen Magie</div>
  <div class="tp-orn">✦ ✦ ✦</div>
  <div class="tp-genre">Ein Adventsmärchen in 24 Kapiteln</div>
</section>
<section class="front"><div class="impressum">
  <p>© 2026 Gabi Scholz<br>Alle Rechte vorbehalten.</p>
  <p>Illustrationen und Umschlaggestaltung: mit KI-Unterstützung erstellt.</p>
  <p class="platzhalter">[Lektorat / Satz: bitte ergänzen]</p>
  <p class="platzhalter">[Verlags- und Herstellerangaben nach BoD-Vorgabe]</p>
  <p class="platzhalter">ISBN: [wird von BoD vergeben]</p>
  <p>Bibliografische Information der Deutschen Nationalbibliothek: Die Deutsche Nationalbibliothek verzeichnet diese Publikation in der Deutschen Nationalbibliografie; detaillierte bibliografische Daten sind im Internet über https://dnb.d-nb.de abrufbar.</p>
</div></section>
<section class="front recto"><div class="widmung"><span class="platzhalter">Für meinen Hexenzirkel</span></div></section>
"""


def author_page():
    return f"""
<section class="autorin">
  <h2>Über die Autorin</h2>
  <img src="file://{IMG}/autorin.jpg">
  <p class="vita"><strong>Gabi Scholz</strong> lebt mit ihrer Familie in Ingolstadt. Sie ist Kräuterhexe, Vollzeitmama und lebt nach dem Motto „Ich mach’s einfach!“. <em>Wibsi Funkelstich</em> entstand als Adventsgeschenk für ihren Hexenzirkel: Jeden Tag im Dezember schrieb sie ein neues Kapitel – vierundzwanzig Tage lang.</p>
  <p class="credit platzhalter">Foto: [Name der Fotografin / des Fotografen]</p>
</section>
"""


def build():
    parts = [front_matter()]
    for f in sorted(glob.glob(os.path.join(KAP, 'kapitel-*.md'))):
        num, title, body = chapter(f)
        parts.append(f'<div class="bild"><img src="file://{IMG}/kapitel-{num:02d}.jpg"></div>')
        parts.append(f'<section class="kapitel"><div class="kopf"><div class="nr">{num}</div>'
                     f'<div class="orn">✦ ✦ ✦</div><div class="titel">{html.escape(title)}</div></div>{body}'
                     + ('<div class="ende">✦ Ende ✦</div>' if num == 24 else '') + '</section>')
    parts.append(author_page())
    doc = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
    open(os.path.join(D, 'innenteil.html'), 'w', encoding='utf-8').write(doc)
    rendered = HTML(string=doc, base_url=D).render()
    if len(rendered.pages) % 2:  # gerade Seitenzahl für den Druck
        doc = doc.replace('</body>', '<section class="front" style="break-before: page"><p>&#8203;</p></section></body>')
        rendered = HTML(string=doc, base_url=D).render()
    rendered.write_pdf(OUT)
    print(OUT, len(rendered.pages), 'Seiten')


if __name__ == '__main__':
    build()
