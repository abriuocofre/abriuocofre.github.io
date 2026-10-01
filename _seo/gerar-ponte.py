"""
Paginas-ponte — uma pagina NOSSA por produto, com a NOSSA arte
==============================================================

Por que existe (26/09/2026): o post do Facebook com botao "Comprar agora" so'
mostra a imagem da pagina para onde o link aponta. Apontando direto para a
loja, sai a foto da loja. Apontando para esta pagina, sai a arte do molde, que
esta' no og:image. A pagina tem o botao que leva a loja pelo link de afiliado.

Le _seo/ponte.json e escreve:
    img/ponte/<apelido>.jpg     a arte do molde (copiada de artes-instagram)
    img/ponte/<apelido>-og.jpg  a mesma arte num QUADRADO, para o og:image
    p/<apelido>.html            a pagina

Por que o quadrado (27/09/2026, medido): no post de link, a Meta corta a
imagem em quadrado pelo centro. A arte 4:5 perdia o topo (a marca) e o rodape
(@abriuocofre). O quadrado leva a arte inteira no meio e, nas laterais, ela
mesma desfocada e escurecida.

Como rodar (da pasta site-ofertas):
    python -X utf8 _seo/gerar-ponte.py

REGRAS QUE ESTE SCRIPT NAO PODE QUEBRAR
1. A pagina NAO redireciona sozinha. A Meta reprova anuncio cujo destino pula
   para outro site, e a Amazon nao aceita link que esconde o destino. Quem vai
   a loja e' o visitante, pelo botao.
2. Magalu: o nome da loja nao aparece (contrato 11.6, confirmado por escrito
   em 21/08/2026). O link ja diz de onde vem.
3. Preco e nota nao aparecem: envelhecem, e o site e' estatico.
4. Todo link de afiliado sai com rel="sponsored nofollow noopener".
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent      # .../site-ofertas
SITE = "https://abriuocofre.github.io"

LOJAS = {
    "magalu": {
        "tag": "Achado do cofre",
        "botao": "Ver o preço na loja",
        "conferir": [
            "Veja se quem vende é a própria loja ou um parceiro.",
            "Confira o frete e o prazo para o seu CEP antes de fechar.",
            "O preço muda durante o dia — vale o que estiver na página da loja.",
        ],
    },
    "amazon": {
        "tag": "Amazon",
        "botao": "Ver o preço na Amazon",
        "conferir": [
            "Veja quem vende: a própria Amazon ou um parceiro do marketplace.",
            "Confira o prazo de entrega para o seu CEP antes de fechar o pedido.",
            "O preço muda várias vezes ao dia — vale o que estiver na página da loja.",
        ],
    },
    "mercadolivre": {
        "tag": "Mercado Livre",
        "botao": "Ver o preço no Mercado Livre",
        "conferir": [
            "Olhe a reputação do vendedor — a barra verde e o total de vendas.",
            "Anúncio com FULL sai do depósito do próprio Mercado Livre.",
            "Leia as perguntas respondidas: é onde aparece o defeito escondido.",
        ],
    },
}

PROIBIDO = [
    (r"(?i)magalu|magazine\s*luiza|\blu\b", "nome da loja Magalu (contrato 11.6)"),
    (r"R\$|\d+,\d{2}\b", "preco"),
    (r"(?i)\bnota\b|avalia", "nota ou avaliacao"),
]

CSS = """:root{color-scheme:dark;
  --breu:#0A0D12; --aco:#111823; --risco:#22303F;
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
.dentro{width:100%;max-width:var(--largura);margin-inline:auto;padding-inline:1rem}
.topo{border-bottom:1px solid var(--risco);padding-block:1.15rem}
.marca{display:flex;align-items:center;gap:.75rem;text-decoration:none}
.marca img{width:40px;height:40px;flex:0 0 auto}
.marca-nome{font-family:"Chakra Petch","Segoe UI",sans-serif;font-weight:700;
  font-size:1.05rem;letter-spacing:.06em;text-transform:uppercase}
.marca-nome b{color:var(--ambar);font-weight:700}
main{padding-block:1.4rem 3rem}
.loja-tag{display:inline-block;font-size:.7rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--tinta-3);margin-bottom:.5rem}
h1{font-family:"Chakra Petch","Segoe UI",sans-serif;font-weight:600;
  font-size:clamp(1.5rem,5.2vw,2.2rem);line-height:1.15;text-wrap:balance}
.selo{display:inline-block;margin-top:.85rem;padding:.3rem .7rem;border-radius:999px;
  background:var(--ambar-op);color:var(--ambar);font-size:.76rem;font-weight:600}
.resumo{margin-top:1rem;font-size:1.06rem;color:var(--tinta-2);max-width:52ch}
.ir{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
  margin-top:1.4rem;padding:1rem 1.6rem;border-radius:999px;background:var(--ambar);
  color:#1A1206;font-weight:600;text-decoration:none;font-size:1.05rem}
.ir:hover{filter:brightness(1.06)}
.foto{margin-top:1.6rem;max-width:480px;border:1px solid var(--risco);
  border-radius:var(--raio);overflow:hidden;background:var(--aco)}
.foto a{display:block}
.foto img{width:100%;height:auto}
.aviso{margin:1.6rem 0 0;border-left:3px solid var(--ambar);padding-left:1rem;
  color:var(--tinta-2);font-size:.88rem;line-height:1.55;max-width:58ch}
.aviso b{color:var(--ambar)}
.bloco{margin-top:2.2rem;border:1px solid var(--risco);border-radius:var(--raio);
  background:var(--aco);padding:1.2rem 1.3rem}
.bloco h2{font-family:"Chakra Petch","Segoe UI",sans-serif;font-size:1rem;
  letter-spacing:.04em;text-transform:uppercase;color:var(--tinta-2);margin-bottom:.8rem}
.bloco ul{list-style:none;display:grid;gap:.6rem}
.bloco li{position:relative;padding-left:1.15rem;color:var(--tinta-2);font-size:.95rem}
.bloco li::before{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;
  border-radius:2px;background:var(--ciano)}
.rodape{border-top:1px solid var(--risco);padding-block:1.6rem 2.6rem;
  color:var(--tinta-3);font-size:.84rem}
.rodape a{color:var(--tinta-2)}
@media (max-width:520px){.ir{display:flex;width:100%}}"""


def conferir(p: dict) -> None:
    texto = " ".join(str(p.get(k, "")) for k in ("titulo", "selo", "resumo"))
    for padrao, nome in PROIBIDO:
        if re.search(padrao, texto):
            sys.exit(f"RECUSADO ({p['apelido']}): {nome} no texto da pagina.")
    if p["loja"] not in LOJAS:
        sys.exit(f"RECUSADO ({p['apelido']}): loja desconhecida '{p['loja']}'.")
    if p["loja"] == "amazon" and "tag=abriuocofre" not in p["link"]:
        sys.exit(f"RECUSADO ({p['apelido']}): link da Amazon sem a etiqueta.")


def pagina(p: dict) -> str:
    loja = LOJAS[p["loja"]]
    url = f"{SITE}/p/{p['apelido']}.html"
    img = f"{SITE}/img/ponte/{p['apelido']}-og.jpg"
    t = escape(p["titulo"])
    r = escape(p["resumo"])
    link = escape(p["link"], quote=True)
    ir = (f'<a class="ir" href="{link}" target="_blank" rel="sponsored nofollow noopener">'
          f'{escape(loja["botao"])} →</a>')
    conf = "\n".join(f"      <li>{escape(c)}</li>" for c in loja["conferir"])
    return f"""<!doctype html>
<html lang="pt-BR" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t} — Abriu o Cofre</title>
<meta name="description" content="{r}">
<meta name="theme-color" content="#0A0D12">
<link rel="icon" href="{SITE}/logo.png">
<link rel="canonical" href="{url}">
<meta property="og:type" content="product">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{r}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1080">
<meta property="og:image:height" content="1080">
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
  <span class="loja-tag">{escape(loja["tag"])}</span>
  <h1>{t}</h1>
  <p><span class="selo">{escape(p.get("selo", ""))}</span></p>
  <p class="resumo">{r}</p>
  <p>{ir}</p>
  <figure class="foto"><a href="{link}" target="_blank" rel="sponsored nofollow noopener"><img src="../img/ponte/{p['apelido']}.jpg" alt="{t}" width="1080" height="1350"></a></figure>
  <p class="aviso"><b>#publi</b> · Este é um link de afiliado: se você comprar por ele, o canal recebe uma comissão e você paga o mesmo preço. Preço e estoque mudam a qualquer momento — o que vale é o que estiver na página da loja.</p>
  <section class="bloco">
    <h2>Antes de comprar, confira</h2>
    <ul>
{conf}
    </ul>
  </section>
</main>
</div>
<footer class="rodape">
  <div class="dentro">
    <p><a href="{SITE}/">Todos os achados</a> · <a href="https://t.me/abriuocofre" target="_blank" rel="noopener">Canal no Telegram</a> · <a href="https://www.instagram.com/abriuocofre/" target="_blank" rel="noopener">Instagram</a></p>
    <p style="margin-top:.7rem">Abriu o Cofre é participante de programas de afiliados. Como afiliado, o canal recebe uma comissão por compras qualificadas — você paga exatamente o mesmo preço.</p>
  </div>
</footer>
</body>
</html>
"""


def quadrado(arte: Path, saida: Path, lado: int = 1080) -> None:
    """A arte inteira no meio de um quadrado; as laterais sao ela desfocada."""
    from PIL import Image, ImageEnhance, ImageFilter
    im = Image.open(arte).convert("RGB")
    alta = round(lado * im.height / im.width)
    fundo = im.resize((lado, alta)).crop((0, (alta - lado) // 2, lado, (alta - lado) // 2 + lado))
    fundo = ImageEnhance.Brightness(fundo.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
    larg = round(im.width * lado / im.height)
    fundo.paste(im.resize((larg, lado), Image.LANCZOS), ((lado - larg) // 2, 0))
    fundo.save(saida, quality=88, optimize=True)


def main() -> int:
    itens = json.loads((RAIZ / "_seo" / "ponte.json").read_bytes().decode("utf-8"))
    for p in itens:
        conferir(p)
    for p in itens:
        origem = (RAIZ / p["arte"]).resolve()
        if not origem.exists():
            sys.exit(f"FALTA a arte de {p['apelido']}: {origem}")
        destino = RAIZ / "img" / "ponte" / f"{p['apelido']}.jpg"
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origem, destino)
        quadrado(destino, destino.with_name(f"{p['apelido']}-og.jpg"))
        html = RAIZ / "p" / f"{p['apelido']}.html"
        html.parent.mkdir(parents=True, exist_ok=True)
        html.write_bytes(pagina(p).encode("utf-8"))
        print(f"ok  p/{p['apelido']}.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
