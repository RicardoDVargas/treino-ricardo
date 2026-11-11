from pathlib import Path
import json, re
import xml.etree.ElementTree as ET
root = Path(__file__).resolve().parent
app = root / 'app'
days = json.loads((app / 'workouts.json').read_text(encoding='utf-8'))
assert len(days) == 7, 'Esperados sete dias'
used = set()
for day in days:
    assert len(day['exercises']) == 7, day['name']
    # o app divide o dia em blocos a partir de "Grupo (n) + Grupo (n) + ..."
    counts = [int(n) for n in re.findall(r'\((\d+)\)', day['groups'])]
    assert sum(counts) == 7, f"{day['name']}: contagens em 'groups' devem somar 7"
    for e in day['exercises']:
        assert all(k in e for k in ('name', 'sets', 'rest', 'image'))
        assert isinstance(e['rest'], int) and e['rest'] > 0
        assert (app / 'images' / (e['image'] + '.svg')).is_file(), e['image']
        used.add(e['image'])
for svg in (app / 'images').glob('*.svg'):
    ET.parse(svg)  # garante que o XML é válido
essentials = ['index.html', 'style.css', 'app.js', 'sw.js', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png', 'stars.svg',
              'fonts/cormorant-garamond-latin-500-normal.woff2', 'fonts/cormorant-garamond-latin-600-normal.woff2', 'fonts/manrope-latin-wght-normal.woff2']
for name in essentials:
    assert (app / name).is_file(), name
sw = (app / 'sw.js').read_text(encoding='utf-8')
for asset in re.findall(r"'\./([^']+)'", sw.split('self.addEventListener')[0]):
    if asset: assert (app / asset).is_file(), f'sw.js cita arquivo inexistente: {asset}'
print(f'OK: sete dias, 49 exercícios, {len(used)} ilustrações em uso (válidas), fontes, ícones e cache offline conferidos.')
