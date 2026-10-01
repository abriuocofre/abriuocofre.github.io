"""Prints das paginas-ponte em 1080 e 375 px (Chrome headless pelo Playwright).

Rodar: python -X utf8 site-ofertas/_seo/prints-ponte/tirar-prints.py [apelido ...]
Sem apelido, tira de todas as pontes de p/. Grava aqui mesmo:
<apelido>-1080.png e <apelido>-375.png (primeira tela) e -375-inteira.png.
Tambem mede: largura rolavel > janela (vazamento lateral) e fundo do body.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
SITE = AQUI.parent.parent
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"

nomes = sys.argv[1:] or sorted(p.stem for p in (SITE / "p").glob("*.html"))
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROME, headless=True)
    for nome in nomes:
        url = (SITE / "p" / f"{nome}.html").as_uri()
        for larg, alt in ((1080, 1000), (375, 812)):
            pg = nav.new_page(viewport={"width": larg, "height": alt},
                              device_scale_factor=1, color_scheme="light")
            pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(400)
            pg.screenshot(path=str(AQUI / f"{nome}-{larg}.png"))
            if larg == 375:
                pg.screenshot(path=str(AQUI / f"{nome}-375-inteira.png"), full_page=True)
            m = pg.evaluate("""() => {
              const b = document.querySelector('.ir-topo').getBoundingClientRect();
              return {rola: document.documentElement.scrollWidth, janela: innerWidth,
                fundo: getComputedStyle(document.body).backgroundColor,
                botao_y: Math.round(b.top), botao_alt: Math.round(b.height),
                botao_larg: Math.round(b.width),
                href: document.querySelector('.ir-topo').href,
                url_final: location.href}
            }""")
            print(nome, larg, m)
            pg.close()
    nav.close()
