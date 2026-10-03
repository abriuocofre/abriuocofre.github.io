"""
gerar-video.py - pagina de PREVIA para compartilhar um video da marca

POR QUE ESTE ARQUIVO EXISTE
Medido em 02/10/2026: o link de um Reel do Facebook (facebook.com/share/r/...
ou facebook.com/reel/...) chega ao WhatsApp SEM titulo e SEM miniatura. O
Facebook nao entrega as etiquetas og: a quem le o link de fora (a propria
Meta, pelo scraper oficial, volta vazia). Ja os links do Instagram, do Threads
e do Telegram entregam miniatura sozinhos.

A saida e' compartilhar o link DESTA pagina, que e' nossa: ela entrega titulo,
descricao e o avatar da marca como miniatura, e leva ao video pelos botoes.

REGRAS
1. A pagina NAO redireciona sozinha: quem vai ao video e' o visitante, pelo botao.
2. E' pagina de video da MARCA. Nao e' para produto de loja de afiliado (a
   Magalu proibiu pagina-ponte em 02/10/2026; Amazon e ML tem regra propria).
3. Sem nome pessoal em lugar nenhum.

Como rodar (da pasta do site):
    python -X utf8 _seo/gerar-video.py
Entrada: _seo/videos.json (uma entrada por video). Saida: v/<slug>.html
"""
from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://abriuocofre.github.io"
IMAGEM = f"{SITE}/marca/og-cofre-1200x630-leve.jpg"   # 1200x630 (cartao grande no WhatsApp: a quadrada vira miniatura e borra), < 100 KB

PAGINA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Abriu o Cofre">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{imagem}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{imagem}">
<style>
:root{{color-scheme:dark;--ouro:#f2b84b;--fundo:#0e0b08;--painel:#1a1510;--texto:#f3ece0}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--fundo);color:var(--texto);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
display:flex;min-height:100vh;align-items:center;justify-content:center;padding:24px 16px}}
main{{width:100%;max-width:440px;text-align:center}}
img{{width:132px;height:132px;border-radius:50%;object-fit:cover;border:3px solid var(--ouro)}}
h1{{font-size:1.45rem;margin:18px 0 6px}}
p{{margin:0 0 22px;opacity:.85}}
a.botao{{display:block;margin:10px 0;padding:14px 18px;border-radius:12px;background:var(--ouro);color:#1b1306;
font-weight:700;text-decoration:none}}
a.botao.fraco{{background:var(--painel);color:var(--texto);border:1px solid #3a2f20;font-weight:600}}
small{{display:block;margin-top:22px;opacity:.6}}
</style>
</head>
<body>
<main>
<img src="{imagem}" alt="Abriu o Cofre">
<h1>{titulo}</h1>
<p>{descricao}</p>
{botoes}
<small>@abriuocofre</small>
</main>
</body>
</html>
"""


def botoes(links: list[dict]) -> str:
    saida = []
    for i, ln in enumerate(links):
        classe = "botao" if i < 2 else "botao fraco"
        saida.append(
            f'<a class="{classe}" href="{escape(ln["url"], quote=True)}" '
            f'rel="noopener" target="_blank">{escape(ln["rotulo"])}</a>'
        )
    return "\n".join(saida)


def main() -> int:
    itens = json.loads((RAIZ / "_seo" / "videos.json").read_text(encoding="utf-8"))
    if not (RAIZ / "marca" / "og-cofre-1200x630-leve.jpg").exists():
        sys.exit("Falta marca/og-cofre-1200x630-leve.jpg (a miniatura).")
    (RAIZ / "v").mkdir(exist_ok=True)
    for v in itens:
        slug = v["slug"]
        if not slug.replace("-", "").isalnum() or slug != slug.lower():
            sys.exit(f"slug invalido: {slug}")
        for ln in v["links"]:
            if not ln["url"].startswith("https://"):
                sys.exit(f"{slug}: link sem https: {ln['url']}")
        html = PAGINA.format(
            titulo=escape(v["titulo"]), descricao=escape(v["descricao"]),
            url=f"{SITE}/v/{slug}.html", imagem=IMAGEM, botoes=botoes(v["links"]),
        )
        (RAIZ / "v" / f"{slug}.html").write_text(html, encoding="utf-8", newline="\n")
        print(f"ok  v/{slug}.html  ->  {SITE}/v/{slug}.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
