"""
Gerador de SEO do site de ofertas — Abriu o Cofre
==================================================

Lê o UNICO arquivo que se edita no dia a dia (ofertas.js) e escreve, sozinho:

  robots.txt              a porta: diz aos buscadores que pode entrar
  sitemap.xml             o mapa: lista toda pagina e toda imagem de oferta
  catalogo.html           a pagina que LINKA cada oferta (senao elas ficam orfas)
  oferta/<apelido>.html   UMA pagina propria por oferta, com dados estruturados

Por que existe: hoje as ofertas sao desenhadas por JavaScript dentro de uma
pagina so. Para o Google existe UMA pagina; nenhuma oferta tem endereco proprio,
entao nenhuma pode aparecer numa busca por "air fryer 5 litros". Cada oferta com
endereco proprio e' uma porta de entrada nova para quem NAO segue o canal.

Como rodar (da pasta site-ofertas):

    python -X utf8 _seo/gerar-seo.py

REGRAS QUE ESTE SCRIPT NAO PODE QUEBRAR
---------------------------------------
1. PRECO DA AMAZON NUNCA APARECE. O contrato de afiliado proibe escrever o preco
   fora da Amazon. So oferta de loja != "amazon" pode mostrar preco.
2. Todo link de afiliado sai com rel="sponsored nofollow noopener" e target=_blank.
3. Todo endereco publico sai pelo dominio da MARCA (abriuocofre.github.io).
   O dominio ANTIGO do site carrega o nome pessoal do dono e por isso nao
   entra em lugar nenhum — nem como exemplo, nem dentro de um comentario.
   Quem e' esse endereco esta' anotado so no registro interno do projeto.
4. O script NAO apaga nada. Pagina de oferta que saiu do ofertas.js e' apenas
   LISTADA no fim, para decisao humana.

⚠️ O ENDERECO NASCE DO TITULO. Mudar "Air fryer 5 litros" para "Airfryer 5 L"
cria um endereco NOVO e abandona o antigo — o Google perde meses de indexacao.
Titulo de oferta ja publicada so se mexe se houver motivo forte.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

# ── onde fica cada coisa ────────────────────────────────────────────────────
RAIZ = Path(__file__).resolve().parent.parent      # .../site-ofertas
SITE = "https://abriuocofre.github.io"             # dominio da MARCA
PASTA_OFERTA = RAIZ / "oferta"
HOJE = date.today().isoformat()

OG_PADRAO = SITE + "/marca/og-cofre-1200x630.jpg"

LOJAS = {
    "amazon": {
        "nome": "Amazon",
        "de": "da Amazon",
        "botao": "Ver na Amazon",
        "pode_preco": False,
        "conferir": [
            "Veja quem vende: a própria Amazon ou um parceiro do marketplace.",
            "Confira o prazo de entrega para o seu CEP antes de fechar o pedido.",
            "O preço muda várias vezes ao dia — vale o que estiver na página da loja.",
        ],
    },
    "mercadolivre": {
        "nome": "Mercado Livre",
        "de": "do Mercado Livre",
        "botao": "Ver no Mercado Livre",
        "pode_preco": True,
        "conferir": [
            "Olhe a reputação do vendedor — a barra verde e o total de vendas.",
            "Anúncio com FULL sai do depósito do próprio Mercado Livre.",
            "Leia as perguntas respondidas: é onde aparece o defeito escondido.",
        ],
    },
}


# ── ler o ofertas.js ────────────────────────────────────────────────────────
def ler_js() -> str:
    """Le em BYTES e decodifica na mao: modo texto do Windows mexe em quebra
    de linha e nao queremos nenhuma reinterpretacao aqui."""
    return (RAIZ / "ofertas.js").read_bytes().decode("utf-8")


def recortar_lista(texto: str, nome: str) -> str:
    """Devolve o miolo de `const NOME = [ ... ];`."""
    inicio = texto.index("const " + nome)
    abre = texto.index("[", inicio)
    nivel = 0
    for i in range(abre, len(texto)):
        if texto[i] == "[":
            nivel += 1
        elif texto[i] == "]":
            nivel -= 1
            if nivel == 0:
                return texto[abre + 1:i]
    raise ValueError("lista " + nome + " nao fecha")


CAMPO = r'{0}\s*:\s*"((?:[^"\\]|\\.)*)"'


def campos_do_bloco(bloco: str) -> dict:
    item = {}
    for chave in ("loja", "titulo", "texto", "preco", "selo", "imagem", "link"):
        achado = re.search(CAMPO.format(chave), bloco)
        if achado:
            # desfaz apenas os escapes que o JS usa de verdade nestes campos
            valor = achado.group(1)
            valor = valor.replace('\\"', '"').replace("\\\\", "\\")
            item[chave] = valor.strip()
    return item


def separar_blocos(miolo: str) -> list:
    """Cada objeto `{ ... }` de primeiro nivel vira um bloco de texto."""
    blocos, nivel, comeco = [], 0, None
    for i, c in enumerate(miolo):
        if c == "{":
            if nivel == 0:
                comeco = i
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0 and comeco is not None:
                blocos.append(miolo[comeco:i + 1])
                comeco = None
    return blocos


def carregar_ofertas() -> list:
    js = ler_js()
    ofertas = []
    for bloco in separar_blocos(recortar_lista(js, "OFERTAS")):
        item = campos_do_bloco(bloco)
        if item.get("titulo") and item.get("link"):
            ofertas.append(item)
    return ofertas


# ── apelido (o endereco) ────────────────────────────────────────────────────
def apelidar(titulo: str) -> str:
    """'Air fryer 5 litros' -> 'air-fryer-5-litros'. Sem acento, sem surpresa."""
    cru = unicodedata.normalize("NFKD", titulo)
    cru = "".join(c for c in cru if not unicodedata.combining(c))
    cru = cru.lower()
    cru = re.sub(r"[^a-z0-9]+", "-", cru).strip("-")
    return cru[:70] or "oferta"


def apelidar_todas(ofertas: list) -> None:
    usados = {}
    for o in ofertas:
        base = apelidar(o["titulo"])
        n = usados.get(base, 0) + 1
        usados[base] = n
        o["apelido"] = base if n == 1 else base + "-" + str(n)


# ── escrever com seguranca ──────────────────────────────────────────────────
def gravar(caminho: Path, texto: str) -> None:
    """Sempre em bytes UTF-8 e sempre com LF: o modo texto do Windows trocaria
    a quebra de linha do arquivo inteiro e o git acusaria mudanca onde nao ha."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(texto.replace("\r\n", "\n").encode("utf-8"))


def esc(t) -> str:
    """Escapa para dentro de HTML."""
    return (str("" if t is None else t)
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def cortar(t: str, n: int) -> str:
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"


# ── as pecas comuns de HTML ─────────────────────────────────────────────────
FONTES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700'
    '&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
)

ESTILO = """<style>
:root{
  --breu:#0A0D12; --aco:#111823; --aco-alto:#16202D;
  --risco:#22303F; --risco-luz:#2E4055;
  --ciano:#22D3EE; --ambar:#F59E0B; --ambar-op:rgba(245,158,11,.13);
  --tinta:#E8EFF7; --tinta-2:#A3B4C6; --tinta-3:#6D8096;
  --largura:760px; --raio:14px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{background:var(--breu);-webkit-text-size-adjust:100%}
body{background:var(--breu);color:var(--tinta);
  font:400 1rem/1.65 "IBM Plex Sans","Segoe UI",system-ui,sans-serif;overflow-x:hidden}
a{color:inherit}
img{max-width:100%;display:block}
:focus-visible{outline:2px solid var(--ciano);outline-offset:3px;border-radius:4px}
.dentro{width:100%;max-width:var(--largura);margin-inline:auto;padding-inline:1.25rem}

.topo{border-bottom:1px solid var(--risco);padding-block:1.15rem}
.marca{display:flex;align-items:center;gap:.75rem;text-decoration:none}
.marca img{width:40px;height:40px;flex:0 0 auto}
.marca-nome{font-family:"Chakra Petch","Segoe UI",sans-serif;font-weight:700;
  font-size:1.05rem;letter-spacing:.06em;text-transform:uppercase}
.marca-nome b{color:var(--ambar);font-weight:700}

.trilha{font-size:.78rem;color:var(--tinta-3);padding-block:1rem .25rem}
.trilha a{color:var(--tinta-2)}

main{padding-block:.5rem 3rem}
.loja-tag{display:inline-block;font-size:.7rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--tinta-3);margin-bottom:.5rem}
h1{font-family:"Chakra Petch","Segoe UI",sans-serif;font-weight:600;
  font-size:clamp(1.6rem,5.2vw,2.3rem);line-height:1.15;text-wrap:balance}
.selo{display:inline-block;margin-top:.85rem;padding:.3rem .7rem;border-radius:999px;
  background:var(--ambar-op);color:var(--ambar);font-size:.76rem;font-weight:600;
  letter-spacing:.02em}
.resumo{margin-top:1.1rem;font-size:1.08rem;color:var(--tinta-2);max-width:52ch}
.preco{margin-top:1rem;font-family:"Chakra Petch","Segoe UI",sans-serif;
  font-size:1.5rem;font-weight:700;color:var(--ciano)}
.preco small{display:block;font-family:inherit;font-size:.72rem;font-weight:400;
  letter-spacing:.02em;color:var(--tinta-3);margin-top:.2rem}
.sem-preco{margin-top:1rem;font-size:.86rem;color:var(--tinta-3)}

.foto{margin-top:1.6rem;border:1px solid var(--risco);border-radius:var(--raio);
  background:var(--aco);overflow:hidden}
.foto img{width:100%;height:auto}

.ir{display:inline-flex;align-items:center;gap:.5rem;margin-top:1.7rem;
  padding:.9rem 1.4rem;border-radius:999px;background:var(--ambar);color:#1A1206;
  font-weight:600;text-decoration:none;font-size:1rem}
.ir:hover{filter:brightness(1.06)}

.bloco{margin-top:2.4rem;border:1px solid var(--risco);border-radius:var(--raio);
  background:var(--aco);padding:1.25rem 1.35rem}
.bloco h2{font-family:"Chakra Petch","Segoe UI",sans-serif;font-size:1rem;
  letter-spacing:.04em;text-transform:uppercase;color:var(--tinta-2);margin-bottom:.8rem}
.bloco ul{list-style:none;display:grid;gap:.6rem}
.bloco li{position:relative;padding-left:1.15rem;color:var(--tinta-2);font-size:.95rem}
.bloco li::before{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;
  border-radius:2px;background:var(--ciano)}

.aviso{margin-top:2.4rem;border-left:3px solid var(--risco-luz);padding-left:1rem;
  color:var(--tinta-3);font-size:.86rem;max-width:58ch}

.vizinhos{margin-top:2.8rem}
.vizinhos h2{font-family:"Chakra Petch","Segoe UI",sans-serif;font-size:1rem;
  letter-spacing:.04em;text-transform:uppercase;color:var(--tinta-2);margin-bottom:.9rem}
.grade{display:grid;gap:.7rem;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.grade a{display:block;text-decoration:none;border:1px solid var(--risco);
  border-radius:var(--raio);background:var(--aco);padding:.85rem 1rem;
  transition:border-color .15s}
.grade a:hover{border-color:var(--risco-luz)}
.grade span{display:block;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--tinta-3);margin-bottom:.25rem}
.grade strong{display:block;font-weight:600;font-size:.97rem;line-height:1.35}

.rodape{border-top:1px solid var(--risco);padding-block:1.6rem 2.6rem;
  color:var(--tinta-3);font-size:.84rem}
.rodape a{color:var(--tinta-2)}
</style>"""


def cabeca(titulo_aba, descricao, url, imagem, extra=""):
    return (
        '<!doctype html>\n'
        '<html lang="pt-BR" data-theme="dark">\n'
        '<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + esc(titulo_aba) + '</title>\n'
        '<meta name="description" content="' + esc(descricao) + '">\n'
        '<meta name="theme-color" content="#0A0D12">\n'
        '<link rel="icon" href="' + SITE + '/logo.png">\n'
        '<link rel="canonical" href="' + esc(url) + '">\n'
        '<meta property="og:type" content="article">\n'
        '<meta property="og:title" content="' + esc(titulo_aba) + '">\n'
        '<meta property="og:description" content="' + esc(descricao) + '">\n'
        '<meta property="og:image" content="' + esc(imagem) + '">\n'
        '<meta property="og:url" content="' + esc(url) + '">\n'
        '<meta property="og:site_name" content="Abriu o Cofre">\n'
        '<meta property="og:locale" content="pt_BR">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="' + esc(titulo_aba) + '">\n'
        '<meta name="twitter:image" content="' + esc(imagem) + '">\n'
        + FONTES + '\n' + ESTILO + '\n' + extra + '</head>\n<body>\n'
    )


TOPO = (
    '<header class="topo">\n'
    '  <div class="dentro">\n'
    '    <a class="marca" href="' + SITE + '/">\n'
    '      <img src="' + SITE + '/logo.png" alt="" width="40" height="40">\n'
    '      <span class="marca-nome">Abriu o <b>Cofre</b></span>\n'
    '    </a>\n'
    '  </div>\n'
    '</header>\n'
)

RODAPE = (
    '<footer class="rodape">\n'
    '  <div class="dentro">\n'
    '    <p><a href="' + SITE + '/">Voltar para todos os achados</a> · '
    '<a href="' + SITE + '/catalogo.html">Catálogo completo</a> · '
    '<a href="https://t.me/abriuocofre" target="_blank" rel="noopener">Canal no Telegram</a></p>\n'
    '    <p style="margin-top:.7rem">Abriu o Cofre é participante de programas de afiliados. '
    'Como afiliado, o canal recebe uma comissão por compras qualificadas — '
    'você paga exatamente o mesmo preço.</p>\n'
    '  </div>\n'
    '</footer>\n</body>\n</html>\n'
)


# ── a pagina de uma oferta ──────────────────────────────────────────────────
def pagina_da_oferta(o: dict, vizinhas: list) -> str:
    loja = LOJAS.get(o.get("loja", ""), LOJAS["amazon"])
    url = SITE + "/oferta/" + o["apelido"] + ".html"
    imagem = o.get("imagem") or OG_PADRAO
    descricao = cortar(o.get("texto") or (o["titulo"] + " — achado garimpado no " + loja["nome"] + "."), 155)

    # DADOS ESTRUTURADOS — de proposito SEM bloco de preco/oferta:
    # declarar preco para a Amazon violaria o contrato de afiliado, e preco
    # velho em dado estruturado e' pior que preco nenhum.
    grafo = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Abriu o Cofre", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Achados", "item": SITE + "/catalogo.html"},
                    {"@type": "ListItem", "position": 3, "name": o["titulo"]},
                ],
            },
            {
                "@type": "ItemPage",
                "@id": url,
                "url": url,
                "name": o["titulo"],
                "headline": o["titulo"],
                "description": descricao,
                "inLanguage": "pt-BR",
                "primaryImageOfPage": {"@type": "ImageObject", "url": imagem},
                "isPartOf": {"@type": "WebSite", "@id": SITE + "/#site",
                             "name": "Abriu o Cofre", "url": SITE + "/"},
                "publisher": {"@type": "Organization", "@id": SITE + "/#marca",
                              "name": "Abriu o Cofre", "url": SITE + "/",
                              "logo": {"@type": "ImageObject", "url": SITE + "/logo.png"}},
            },
        ],
    }
    jsonld = ('<script type="application/ld+json">\n'
              + json.dumps(grafo, ensure_ascii=False, indent=2) + '\n</script>\n')

    partes = [cabeca(o["titulo"] + " — Abriu o Cofre", descricao, url, imagem, jsonld), TOPO]
    partes.append('<div class="dentro">\n')
    partes.append('<nav class="trilha" aria-label="Trilha"><a href="' + SITE + '/">Início</a> › '
                  '<a href="' + SITE + '/catalogo.html">Achados</a> › ' + esc(o["titulo"]) + '</nav>\n')
    partes.append('<main>\n')
    partes.append('  <span class="loja-tag">' + esc(loja["nome"]) + '</span>\n')
    partes.append('  <h1>' + esc(o["titulo"]) + '</h1>\n')
    if o.get("selo"):
        partes.append('  <p><span class="selo">' + esc(o["selo"]) + '</span></p>\n')
    if o.get("texto"):
        partes.append('  <p class="resumo">' + esc(o["texto"]) + '</p>\n')

    # ⚠️ preco SO fora da Amazon — regra do contrato de afiliado
    if loja["pode_preco"] and o.get("preco"):
        partes.append('  <p class="preco">' + esc(o["preco"])
                      + '<small>preço visto no dia em que a oferta entrou · confira na loja</small></p>\n')
    else:
        partes.append('  <p class="sem-preco">O preço atualizado aparece na página '
                      + esc(loja["de"]) + '.</p>\n')

    if o.get("imagem"):
        partes.append('  <figure class="foto"><img src="' + esc(o["imagem"]) + '" alt="'
                      + esc(o["titulo"]) + '" loading="lazy"></figure>\n')

    partes.append('  <p><a class="ir" href="' + esc(o["link"]) + '" target="_blank" '
                  'rel="sponsored nofollow noopener">' + esc(loja["botao"]) + ' →</a></p>\n')

    partes.append('  <section class="bloco">\n    <h2>Antes de comprar, confira</h2>\n    <ul>\n')
    for linha in loja["conferir"]:
        partes.append('      <li>' + esc(linha) + '</li>\n')
    partes.append('    </ul>\n  </section>\n')

    partes.append('  <p class="aviso">#publi · Este é um link de afiliado: se você comprar por ele, '
                  'o canal recebe uma comissão e você paga o mesmo preço. Preço e disponibilidade '
                  'mudam a qualquer momento — o que vale é o que estiver na página da loja.</p>\n')

    if vizinhas:
        partes.append('  <section class="vizinhos">\n    <h2>Outros achados do cofre</h2>\n'
                      '    <div class="grade">\n')
        for v in vizinhas:
            nome_loja = LOJAS.get(v.get("loja", ""), LOJAS["amazon"])["nome"]
            partes.append('      <a href="' + SITE + '/oferta/' + v["apelido"] + '.html">'
                          '<span>' + esc(nome_loja) + '</span>'
                          '<strong>' + esc(v["titulo"]) + '</strong></a>\n')
        partes.append('    </div>\n  </section>\n')

    partes.append('</main>\n</div>\n')
    partes.append(RODAPE)
    return "".join(partes)


# ── o catalogo: a pagina que impede as ofertas de ficarem orfas ─────────────
def pagina_catalogo(ofertas: list) -> str:
    url = SITE + "/catalogo.html"
    descricao = ("Todos os " + str(len(ofertas)) + " achados do Abriu o Cofre, um por um, "
                 "com página própria: o que é, por que entrou e o que conferir antes de comprar.")
    grafo = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": url, "url": url,
             "name": "Catálogo de achados — Abriu o Cofre",
             "description": descricao, "inLanguage": "pt-BR",
             "isPartOf": {"@type": "WebSite", "@id": SITE + "/#site",
                          "name": "Abriu o Cofre", "url": SITE + "/"}},
            {"@type": "ItemList", "name": "Achados do cofre",
             "numberOfItems": len(ofertas),
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": o["titulo"],
                  "url": SITE + "/oferta/" + o["apelido"] + ".html"}
                 for i, o in enumerate(ofertas)
             ]},
        ],
    }
    jsonld = ('<script type="application/ld+json">\n'
              + json.dumps(grafo, ensure_ascii=False, indent=2) + '\n</script>\n')

    partes = [cabeca("Catálogo de achados — Abriu o Cofre", descricao, url, OG_PADRAO, jsonld), TOPO]
    partes.append('<div class="dentro">\n<main>\n')
    partes.append('  <h1>O catálogo inteiro</h1>\n')
    partes.append('  <p class="resumo">Cada achado tem página própria, com o que é, por que passou '
                  'no corte e o que conferir antes de comprar. São ' + str(len(ofertas))
                  + ' até agora.</p>\n')

    for chave in ("amazon", "mercadolivre"):
        grupo = [o for o in ofertas if o.get("loja") == chave]
        if not grupo:
            continue
        partes.append('  <section class="vizinhos">\n    <h2>' + esc(LOJAS[chave]["nome"])
                      + ' · ' + str(len(grupo)) + '</h2>\n    <div class="grade">\n')
        # selo repetido em meio grupo nao informa nada — vira o nome da loja
        repetidos = {s for s in {o.get("selo") for o in grupo}
                     if s and sum(1 for o in grupo if o.get("selo") == s) > 3}
        for o in grupo:
            selo = o.get("selo")
            rotulo = selo if (selo and selo not in repetidos) else LOJAS[chave]["nome"]
            partes.append('      <a href="' + SITE + '/oferta/' + o["apelido"] + '.html">'
                          '<span>' + esc(rotulo) + '</span>'
                          '<strong>' + esc(o["titulo"]) + '</strong></a>\n')
        partes.append('    </div>\n  </section>\n')

    partes.append('</main>\n</div>\n')
    partes.append(RODAPE)
    return "".join(partes)


# ── sitemap e robots ────────────────────────────────────────────────────────
def gerar_sitemap(ofertas: list) -> str:
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
              '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

    def url(loc, prio, imagens=()):
        bloco = ['  <url>', '    <loc>' + esc(loc) + '</loc>',
                 '    <lastmod>' + HOJE + '</lastmod>',
                 '    <changefreq>daily</changefreq>',
                 '    <priority>' + prio + '</priority>']
        for img in imagens:
            bloco += ['    <image:image><image:loc>' + esc(img) + '</image:loc></image:image>']
        bloco.append('  </url>')
        return bloco

    linhas += url(SITE + "/", "1.0", [OG_PADRAO])
    linhas += url(SITE + "/catalogo.html", "0.9")
    linhas += url(SITE + "/cartoes.html", "0.6")
    for o in ofertas:
        imgs = [o["imagem"]] if o.get("imagem") else []
        linhas += url(SITE + "/oferta/" + o["apelido"] + ".html", "0.8", imgs)
    linhas.append('</urlset>')
    return "\n".join(linhas) + "\n"


ROBOTS = """# Abriu o Cofre — https://abriuocofre.github.io
# Pode entrar: o site inteiro é público, inclusive as imagens das peças.

User-agent: *
Allow: /

Sitemap: {site}/sitemap.xml
""".format(site=SITE)


# ── a rotina ────────────────────────────────────────────────────────────────
def main() -> int:
    ofertas = carregar_ofertas()
    if not ofertas:
        print("ERRO: nenhuma oferta lida de ofertas.js")
        return 1
    apelidar_todas(ofertas)

    # trava de seguranca: preco em oferta da Amazon nunca sai daqui
    for o in ofertas:
        if o.get("loja") == "amazon" and o.get("preco"):
            print("ERRO: a oferta '" + o["titulo"] + "' e' da Amazon e traz preco no "
                  "ofertas.js. O contrato proibe. Apague o preco antes de gerar.")
            return 1

    escritos = []
    for i, o in enumerate(ofertas):
        # 6 vizinhas: as seguintes na lista, dando a volta — cada pagina linka
        # outras seis, e toda pagina acaba recebendo links de outras.
        vizinhas = [ofertas[(i + k) % len(ofertas)] for k in range(1, 7)]
        vizinhas = [v for v in vizinhas if v["apelido"] != o["apelido"]]
        alvo = PASTA_OFERTA / (o["apelido"] + ".html")
        gravar(alvo, pagina_da_oferta(o, vizinhas))
        escritos.append(alvo.name)

    gravar(RAIZ / "catalogo.html", pagina_catalogo(ofertas))
    gravar(RAIZ / "sitemap.xml", gerar_sitemap(ofertas))
    gravar(RAIZ / "robots.txt", ROBOTS)

    print("ofertas lidas .......... " + str(len(ofertas))
          + "  (amazon " + str(sum(1 for o in ofertas if o.get("loja") == "amazon"))
          + " · mercadolivre " + str(sum(1 for o in ofertas if o.get("loja") == "mercadolivre")) + ")")
    print("paginas de oferta ...... " + str(len(escritos)) + " em oferta/")
    print("catalogo.html .......... ok")
    print("sitemap.xml ............ " + str(len(ofertas) + 3) + " endereços")
    print("robots.txt ............. ok")

    # nada e' apagado: so' apontado
    vivos = set(escritos)
    orfas = sorted(p.name for p in PASTA_OFERTA.glob("*.html") if p.name not in vivos)
    if orfas:
        print("\n⚠️  " + str(len(orfas)) + " página(s) em oferta/ não estão mais no ofertas.js.")
        print("   Nada foi apagado. Decida uma a uma:")
        for nome in orfas:
            print("     oferta/" + nome)
    return 0


if __name__ == "__main__":
    sys.exit(main())
