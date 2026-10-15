"""
Pagina-ponte de VIDEO — o video com og:video e o botao "Saiba mais"
====================================================================

Por que existe (15/10/2026): no Facebook, Instagram e Threads o Reel que o robo
publica nao tem campo de botao; so' anuncio pago e post de LINK tem. O post de
link com a pagina-ponte (gerar-ponte.py) ja' leva botao; esta variante poe o
VIDEO na pagina, para a Meta ler og:video e poder tocar o video no feed. A Meta
diz que "pode", sem garantia (developers.facebook.com/docs/sharing/webmasters).
E' um TESTE: so' se promove a rotina depois de a Meta provar que le o video.

Le _seo/ponte-video.json e escreve v/<apelido>.html.

Como rodar (da pasta do site):
    python -X utf8 _seo/gerar-ponte-video.py

REGRAS QUE ESTE SCRIPT NAO PODE QUEBRAR (as mesmas do gerar-ponte.py)
1. A pagina NAO redireciona sozinha e NAO tem script: quem segue e' o visitante,
   pelo botao.
2. Sem preco, sem nota, sem o nome da Magalu.
3. Pagina de teste leva noindex.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent      # .../site-ofertas

# Reaproveita o CSS e o SITE da ponte de produto, em vez de copiar.
_spec = importlib.util.spec_from_file_location("ponte", RAIZ / "_seo" / "gerar-ponte.py")
_ponte = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ponte)
SITE = _ponte.SITE

CSS_VIDEO = """
.video{margin-top:1.4rem;max-width:420px;border:1px solid var(--risco);
  border-radius:var(--raio);overflow:hidden;background:var(--aco)}
.video video{width:100%;height:auto;display:block;background:#000}
"""

PROIBIDO = [
    (r"(?i)magalu|magazine\s*luiza|\blu\b", "nome da loja Magalu"),
    (r"R\$|\d+,\d{2}\b", "preco"),
    (r"(?i)\bnota\b|avalia", "nota ou avaliacao"),
]


def conferir(p: dict) -> None:
    texto = " ".join(str(p.get(k, "")) for k in ("titulo", "resumo", "botao"))
    for padrao, nome in PROIBIDO:
        if re.search(padrao, texto):
            sys.exit(f"RECUSADO ({p['apelido']}): {nome} no texto da pagina.")
    if not str(p["destino"]).startswith(SITE + "/"):
        sys.exit(f"RECUSADO ({p['apelido']}): o botao so' leva a pagina do proprio site.")
    for k in ("video", "capa"):
        if not (RAIZ / p[k]).exists():
            sys.exit(f"FALTA {k} de {p['apelido']}: {RAIZ / p[k]}")


def pagina(p: dict) -> str:
    url = f"{SITE}/v/{p['apelido']}.html"
    video = f"{SITE}/{p['video']}"
    capa = f"{SITE}/{p['capa']}"
    t = escape(p["titulo"])
    r = escape(p["resumo"])
    w, h = int(p["largura"]), int(p["altura"])
    destino = escape(p["destino"], quote=True)
    robots = '<meta name="robots" content="noindex">\n' if p.get("teste") else ""
    return f"""<!doctype html>
<html lang="pt-BR" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t} — Abriu o Cofre</title>
<meta name="description" content="{r}">
{robots}<meta name="theme-color" content="#0A0D12">
<link rel="icon" href="{SITE}/logo.png">
<link rel="canonical" href="{url}">
<meta property="og:type" content="video.other">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{r}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Abriu o Cofre">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="{capa}">
<meta property="og:video" content="{video}">
<meta property="og:video:url" content="{video}">
<meta property="og:video:secure_url" content="{video}">
<meta property="og:video:type" content="video/mp4">
<meta property="og:video:width" content="{w}">
<meta property="og:video:height" content="{h}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:image" content="{capa}">
<style>
{_ponte.CSS}
{CSS_VIDEO}
</style>
</head>
<body>
<header class="topo">
  <div class="dentro">
    <a class="marca" href="{SITE}/">
      <img src="{SITE}/logo.png" alt="" width="40" height="40">
      <span class="marca-nome">Abriu o <b>Cofre</b></span>
    </a>
  </div>
</header>
<div class="dentro">
<main>
  <h1>{t}</h1>
  <p class="resumo">{r}</p>
  <div class="video"><video controls playsinline preload="metadata" poster="{capa}" width="{w}" height="{h}" src="{video}"></video></div>
  <p><a class="ir" href="{destino}">{escape(p["botao"])} →</a></p>
</main>
</div>
<footer class="rodape">
  <div class="dentro">
    <p><a href="{SITE}/">Todos os achados</a> · <a href="https://t.me/abriuocofre" target="_blank" rel="noopener">Canal no Telegram</a> · <a href="https://www.instagram.com/abriuocofre/" target="_blank" rel="noopener">Instagram</a></p>
    <p style="margin-top:.7rem">Abriu o Cofre é participante de programas de afiliados e recebe comissão pelas compras feitas pelos links dos canais — você paga exatamente o mesmo preço.</p>
  </div>
</footer>
</body>
</html>
"""


def main() -> int:
    itens = json.loads((RAIZ / "_seo" / "ponte-video.json").read_bytes().decode("utf-8"))
    for p in itens:
        conferir(p)
    for p in itens:
        texto = pagina(p)
        # Trava da regra 1: nenhuma forma de pular sozinho, e nenhum script.
        if re.search(r"(?i)http-equiv\s*=\s*\"?refresh|location\s*[.=]|<script", texto):
            sys.exit(f"RECUSADO ({p['apelido']}): a pagina redirecionaria sozinha ou tem script.")
        saida = RAIZ / "v" / f"{p['apelido']}.html"
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(texto.encode("utf-8"))
        print(f"ok  v/{p['apelido']}.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
