"""Gera app/stars.svg (fundo estrelado) e os ícones do app (icon.svg, icon-192.png, icon-512.png).
Os PNGs usam Playwright (pip install playwright && playwright install chromium); se faltar, só o SVG é gerado."""
import random
from pathlib import Path
app = Path(__file__).resolve().parent.parent / 'app'

rnd = random.Random(7)
dots = ''
for _ in range(70):
    x, y = rnd.uniform(0, 600), rnd.uniform(0, 600)
    r = rnd.choice([.5, .6, .8, 1, 1.3]); o = rnd.choice([.25, .35, .5, .7])
    dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity="{o}"/>'
for _ in range(5):
    x, y = rnd.uniform(20, 580), rnd.uniform(20, 580)
    dots += f'<path d="M{x:.1f} {y-4:.1f}L{x+1:.1f} {y-1:.1f}L{x+4:.1f} {y:.1f}L{x+1:.1f} {y+1:.1f}L{x:.1f} {y+4:.1f}L{x-1:.1f} {y+1:.1f}L{x-4:.1f} {y:.1f}L{x-1:.1f} {y-1:.1f}Z" fill="#f2cf8a" opacity=".7"/>'
(app/'stars.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">{dots}</svg>', encoding='utf-8')

def icon(rx):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a1f9a"/><stop offset=".6" stop-color="#1a1040"/><stop offset="1" stop-color="#0f0826"/></linearGradient>
<radialGradient id="n" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#b9a6ff" stop-opacity=".55"/><stop offset="1" stop-color="#b9a6ff" stop-opacity="0"/></radialGradient>
<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4d8"/><stop offset="1" stop-color="#f2cf8a"/></linearGradient>
<filter id="b"><feGaussianBlur stdDeviation="14"/></filter></defs>
<rect width="512" height="512" rx="{rx}" fill="url(#g)"/><circle cx="256" cy="256" r="190" fill="url(#n)"/>
<g stroke="#b9a6ff" stroke-opacity=".5" stroke-width="3" fill="none"><path d="M118 360 190 318M338 190 400 142"/></g>
<g fill="#fff"><circle cx="118" cy="360" r="5" opacity=".8"/><circle cx="190" cy="318" r="4" opacity=".6"/><circle cx="400" cy="142" r="5" opacity=".8"/><circle cx="338" cy="190" r="3.5" opacity=".6"/></g>
<path d="M256 120 276 236 392 256 276 276 256 392 236 276 120 256 236 236Z" fill="#f2cf8a" opacity=".6" filter="url(#b)"/>
<path d="M256 120 276 236 392 256 276 276 256 392 236 276 120 256 236 236Z" fill="url(#s)"/></svg>'''
(app/'icon.svg').write_text(icon(112), encoding='utf-8')
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for size in (192, 512):
            pg = b.new_page(viewport={'width': size, 'height': size})
            pg.set_content(f'<body style="margin:0">{icon(0).replace("<svg ", f"<svg width={size} height={size} ")}</body>')
            pg.screenshot(path=str(app/f'icon-{size}.png'))
        b.close()
    print('Ícones PNG gerados.')
except Exception as e:
    print('PNG não gerado:', e)
