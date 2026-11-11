"""Teste de ponta a ponta no navegador (opcional; requer Playwright).
Uso: python -m http.server 8000 --directory app   (em outro terminal)   e depois   python tools/teste_navegador.py"""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000/'
erros = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for nome, vp in (('desktop', {'width': 1360, 'height': 900}), ('celular', {'width': 390, 'height': 844})):
        pg = b.new_context(viewport=vp).new_page()
        pg.on('pageerror', lambda e: erros.append(str(e)))
        pg.on('console', lambda m: erros.append(m.text) if m.type == 'error' else None)
        pg.goto(URL); pg.wait_for_selector('.card')
        for i in range(7):
            pg.locator('.day').nth(i).click()
            n = pg.locator('.card').count(); assert n == 7, f'{nome} dia {i+1}: {n} cartões'
            pg.wait_for_function("[...document.images].filter(i=>i.closest('.card')).every(i=>i.complete)")
            for img in pg.locator('.card img').element_handles():
                pg.evaluate("i => i.scrollIntoView()", img)
            pg.wait_for_timeout(250)
            quebradas = pg.evaluate("[...document.querySelectorAll('.card img')].filter(i=>!i.complete||i.naturalWidth===0).length")
            assert quebradas == 0, f'{nome} dia {i+1}: {quebradas} imagens quebradas'
            largura = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            assert largura <= 0, f'{nome} dia {i+1}: rolagem horizontal ({largura}px)'
        # progresso: marcar, recarregar, desmarcar
        pg.locator('.day').nth(0).click(); pg.locator('.btn.check').nth(0).click()
        assert pg.locator('.progress-text strong, .progress').first.get_attribute('aria-label').startswith('1 de 7')
        pg.reload(); pg.wait_for_selector('.card'); pg.locator('.day').nth(0).click()
        assert pg.locator('.card[data-done=true]').count() == 1, 'progresso não persistiu'
        pg.locator('.btn.check').nth(0).click(); assert pg.locator('.card[data-done=true]').count() == 0
        # cronômetro
        pg.locator('.btn.rest').nth(0).click(); pg.wait_for_timeout(1200)
        assert pg.locator('#timer').is_visible() and pg.inner_text('#clock') != '00:00'
        pg.click('#pause'); assert pg.inner_text('#pause') == 'Continuar'
        pg.click('#close-timer'); assert not pg.locator('#timer').is_visible()
        print(f'{nome}: 7 dias x 7 cartões, imagens, sem rolagem horizontal, progresso e cronômetro OK')
    b.close()
assert not erros, erros
print('Sem erros de console.')
