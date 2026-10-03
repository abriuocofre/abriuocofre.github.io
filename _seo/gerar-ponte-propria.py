# -*- coding: utf-8 -*-
"""
Paginas-ponte PROPRIAS — a imagem do post do Facebook vira clicavel
====================================================================

Por que existe (03/10/2026): ele viu no Facebook um post do Prometeu e um
cartao de frase e disse "nao estao clicaveis". Resposta dele: queria a IMAGEM
clicavel. No Facebook so' post de LINK tem imagem que abre algo, e a imagem do
post de link vem do og:image da pagina do link. Entao cada cartao e cada peca de
propaganda ganha uma paginazinha nossa (a mesma ideia do gerar-ponte.py, que
serve as ofertas de loja), com a arte quadrada no og:image e um botao grande
para o destino.

DIFERENCAS para o gerar-ponte.py (que e' de afiliado):
  * aqui o conteudo e' NOSSO (cartao, propaganda do Prometeu e do cofre): nao ha
    link de loja, entao nao ha rel="sponsored" nem aviso de comissao;
  * o aviso "#publi" so' aparece onde a legenda do post ja' o traz (Prometeu e
    cartoes de loja);
  * a pagina leva noindex: sao 160 e tantas paginas-veiculo e nao devem poluir
    a busca do site.
  * nada de redirecionamento automatico: o visitante clica no botao.

Fontes (lidas da pasta da automacao, que e' a copia da nuvem):
  automacao-nuvem/propaganda.json       pecas de imagem (as de video saem como Reel)
  automacao-nuvem/fila-instagram.json   cartoes que ainda NAO sairam no Facebook

Saida (dentro desta pasta do site):
    p/<apelido>.html
    img/ponte/<apelido>-og.jpg          arte num quadrado, para o og:image

    apelido = "pr-<nome da peca>"   (propaganda)
              "ca-<arquivo sem .jpg>" (cartao da fila)

Como rodar (a partir da pasta do site):
    python -X utf8 _seo/gerar-ponte-propria.py --automacao D:/Projetos/Projeto-Wayne/automacao-nuvem
    python -X utf8 _seo/gerar-ponte-propria.py --automacao ... --gravar
    python -X utf8 _seo/gerar-ponte-propria.py --automacao ... --gravar --so ca-pia-b05

Sem --gravar so' mostra o que faria. Idempotente: pagina que ja' existe e' refeita
(texto) e a imagem so' e' refeita com --refazer-imagem.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent          # .../site-ofertas (ou o worktree)
SITE = "https://abriuocofre.github.io"
LADO = 800                                              # a Meta usa ~720; 800 sobra
PROMETEU = "https://organizadordeaulas.github.io/"
WHATS = "https://whatsapp.com/channel/0029VbDdIgtAInPgQHeTfy1M"

# Reaproveita o CSS e o recorte quadrado da ponte de afiliado, sem duplicar.
_spec = importlib.util.spec_from_file_location("gerar_ponte", RAIZ / "_seo" / "gerar-ponte.py")
_gp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gp)
CSS, quadrado = _gp.CSS, _gp.quadrado

PROIBIDO = re.compile(r"(?i)magalu|magazine\s*luiza|R\$|\d+,\d{2}\b|\bnota\b|avalia")
GENERICO = "Abriu o Cofre — ofertas, humor e conhecimento todo dia"


def limpa_titulo(legenda: str) -> str:
    """Primeira linha util da legenda, sem emoji na frente e com no maximo ~88 letras."""
    for linha in legenda.split("\n"):
        t = linha.strip()
        if not t or t.startswith("#") or t.lower().startswith("http"):
            continue
        t = re.sub(r"^[^\wÀ-ÿ\"“]+", "", t).strip()
        t = re.sub("[\U0001F000-\U0001FAFF☀-➿️‍]+", "", t).strip()
        if len(t) < 6:
            continue
        if len(t) > 88:
            t = t[:88].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"
        return t
    return GENERICO


def destino(familia: str, legenda: str) -> tuple[str, str, str, bool]:
    """(url do botao, texto do botao, etiqueta pequena, leva #publi?)"""
    if familia.startswith("prometeu"):
        return PROMETEU, "Conhecer o Organizador de Aulas", "Indicação do Abriu o Cofre", True
    if familia.startswith("canal-"):
        rede = familia.split("-")[1]
        rot = {
            "telegram": "Entrar no canal do Telegram",
            "whatsapp": "Entrar no canal do WhatsApp",
            "instagram": "Seguir no Instagram",
            "threads": "Seguir no Threads",
            "facebook": "Curtir a Página no Facebook",
        }.get(rede, "Conhecer o canal")
        for linha in legenda.split("\n"):
            if "Site:" in linha or "Minhas lojas" in linha:
                continue
            m = re.search(r"https?://\S+", linha)
            if m:
                return m.group(0), rot, "Abriu o Cofre", False
        return SITE + "/", rot, "Abriu o Cofre", False
    if familia.startswith("loja-"):
        return SITE + "/#lojas", "Ver minhas lojas", "Abriu o Cofre", True
    return SITE + "/", "Ver os achados do cofre", "Abriu o Cofre", False


def itens_propaganda(d: dict) -> list[dict]:
    saida = []
    for p in d["pecas"]:
        if p.get("tipo") == "video":
            continue                      # video sai como Reel, sem ponte
        nome = p["nome"]
        if "magalu" in nome.lower():
            continue                      # contrato 11.6: o nome da loja nao aparece em texto/URL nosso; fica como foto
        saida.append({
            "apelido": f"pr-{nome}".lower(),
            "familia": nome,
            "legenda": p["legenda"],
            "arte_url": p["image_url"],
        })
    return saida


def itens_cartoes(fila: list[dict]) -> list[dict]:
    saida = []
    for p in fila:
        if p.get("loja") != "cartao" or p.get("publicado_fb_em") or p.get("fb_pular"):
            continue
        arq = p.get("arquivo", "")
        base = re.sub(r"\.jpe?g$", "", arq)
        if not re.fullmatch(r"[a-z0-9-]+", base):
            continue                      # ex.: P3-comecou-prime (maiuscula): fica como foto
        saida.append({
            "apelido": f"ca-{base}",
            "familia": base,
            "legenda": p["legenda"],
            "arte_url": p["image_url"],
        })
    return saida


def pagina(it: dict, titulo: str, url_botao: str, texto_botao: str, etiqueta: str, publi: bool) -> str:
    ap = it["apelido"]
    url = f"{SITE}/p/{ap}.html"
    img = f"{SITE}/img/ponte/{ap}-og.jpg"
    t = escape(titulo)
    desc = escape("Cartões, ofertas e descobertas todo dia no Abriu o Cofre.")
    botao = escape(url_botao, quote=True)
    aviso = ('<p class="aviso"><b>#publi</b> · Indicação do Abriu o Cofre. '
             'Se houver compra, o canal pode receber uma comissão.</p>') if publi else ""
    return f"""<!doctype html>
<html lang="pt-BR" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>{t} — Abriu o Cofre</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0A0D12">
<link rel="icon" href="{SITE}/logo.png">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="{LADO}">
<meta property="og:image:height" content="{LADO}">
<meta property="og:image:alt" content="{t}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Abriu o Cofre">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
{CSS}
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
  <p><a class="ir ir-topo" href="{botao}" target="_blank" rel="noopener">{escape(texto_botao)} →</a></p>
  <span class="loja-tag depois">{escape(etiqueta)}</span>
  <h1>{t}</h1>
  <figure class="foto"><a href="{botao}" target="_blank" rel="noopener"><img src="{escape(it['arte_url'], quote=True)}" alt="{t}" width="1080" height="1350"></a></figure>
  {aviso}
</main>
</div>
<footer class="rodape">
  <div class="dentro">
    <p><a href="{SITE}/">Todos os achados</a> · <a href="https://t.me/abriuocofre" target="_blank" rel="noopener">Canal no Telegram</a> · <a href="{WHATS}" target="_blank" rel="noopener">Canal no WhatsApp</a> · <a href="https://www.instagram.com/abriuocofre/" target="_blank" rel="noopener">Instagram</a></p>
  </div>
</footer>
</body>
</html>
"""


def local_da_arte(arte_url: str) -> Path:
    if not arte_url.startswith(SITE + "/"):
        sys.exit(f"arte fora do site: {arte_url}")
    return RAIZ / arte_url[len(SITE) + 1:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--automacao", required=True, help="pasta automacao-nuvem (copia da nuvem)")
    ap.add_argument("--gravar", action="store_true")
    ap.add_argument("--so", help="apelido unico (ex.: ca-pia-b05)")
    ap.add_argument("--refazer-imagem", action="store_true")
    a = ap.parse_args()
    auto = Path(a.automacao)

    prop = json.loads((auto / "propaganda.json").read_bytes().decode("utf-8-sig"))
    fila = json.loads((auto / "fila-instagram.json").read_bytes().decode("utf-8-sig"))
    itens = itens_propaganda(prop) + itens_cartoes(fila)
    if a.so:
        itens = [i for i in itens if i["apelido"] == a.so]
        if not itens:
            sys.exit(f"nao achei o apelido {a.so}")

    feitos = faltam = 0
    for it in itens:
        arte = local_da_arte(it["arte_url"])
        if not arte.exists():
            print(f"FALTA a arte de {it['apelido']}: {arte}")
            faltam += 1
            continue
        if it["familia"].startswith("prometeu"):
            titulo = "Organizador de Aulas — o caderno de planejamento que cabe no celular"
        elif it["familia"].startswith("prop-"):
            titulo = GENERICO
        else:
            titulo = limpa_titulo(it["legenda"])
        if PROIBIDO.search(titulo):
            titulo = GENERICO
        url_botao, texto_botao, etiqueta, publi = destino(it["familia"], it["legenda"])
        html = pagina(it, titulo, url_botao, texto_botao, etiqueta, publi)
        if re.search(r"(?i)http-equiv\s*=\s*\"?refresh|location\s*[.=]|<script", html):
            sys.exit(f"RECUSADO ({it['apelido']}): a pagina redirecionaria sozinha.")
        print(f"{'ok ' if a.gravar else 'ens'} p/{it['apelido']}.html  -> {texto_botao}  [{titulo[:60]}]")
        if a.gravar:
            pag = RAIZ / "p" / f"{it['apelido']}.html"
            pag.parent.mkdir(parents=True, exist_ok=True)
            pag.write_bytes(html.encode("utf-8"))
            og = RAIZ / "img" / "ponte" / f"{it['apelido']}-og.jpg"
            og.parent.mkdir(parents=True, exist_ok=True)
            if a.refazer_imagem or not og.exists():
                quadrado(arte, og, LADO)
        feitos += 1
    print(f"{feitos} paginas {'gravadas' if a.gravar else '(ensaio)'}; {faltam} sem arte.")
    return 1 if faltam else 0


if __name__ == "__main__":
    sys.exit(main())
