# -*- coding: utf-8 -*-
"""
Prepara as fotos dos cards do site a partir das ILUSTRACOES puras.

Por que a ilustracao pura, e nao a peca de feed:
  - a peca de feed (artes-instagram/feed-*) e 100% tipografica, sem o produto
    a vista -> BLOQUEADA desde 17/08/2026, nao entra em canal nenhum;
  - a peca montada (artes-instagram/produtos/pecas) traz "LINK NA BIO", que so
    faz sentido no Instagram, e o recorte de algumas esta rasgado;
  - a ilustracao pura (1024x1024, fundo preto, produto inteiro, sem texto) e o
    que combina com o card escuro do site e nao carrega regra nenhuma.

O corte: o card e 4/3. Em vez de cortar no meio as cegas, acho a caixa do
produto (pixels claros sobre o fundo preto) e centro a janela 1024x768 nela,
para nao decapitar produto alto nem cortar pe de produto baixo.

Rodar:  python -X utf8 site-ofertas\\_seo\\preparar-imagens.py
"""
import json
import os
import re
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ILUSTRA = os.path.join(RAIZ, "artes-instagram", "produtos", "ilustracoes")
DESTINO = os.path.join(RAIZ, "site-ofertas", "img", "ofertas")
OFERTAS = os.path.join(RAIZ, "site-ofertas", "ofertas.js")

LARGURA, ALTURA = 900, 675          # 4:3, o mesmo formato do .card-foto
QUALIDADE = 82

# ---------------------------------------------------------------- casamento
# Amazon: posicional puro. azf-NN e a NN-esima oferta "amazon" do ofertas.js.
# Mercado Livre: os arquivos mlf-NN nao seguem a ordem das ofertas (4 arquivos
# nao viraram oferta), entao o mapa vai escrito a mao, conferido item a item.
MAPA_ML = {
    1: "mlf-01-creatina",            2: "mlf-03-bicicleta-aro29",
    3: "mlf-04-parafusadeira",       4: "mlf-05-lava-jato",
    5: "mlf-07-gel-facial-garnier",  6: "mlf-08-airfryer-mondial",
    7: "mlf-09-cameras-icsee",       8: "mlf-10-calca-jeans",
    9: "mlf-11-travesseiros",       10: "mlf-12-tenis-kappa",
    11: "mlf-13-stanley-473",       12: "mlf-14-faqueiro-tramontina",
    13: "mlf-16-cabides-veludo",    14: "mlf-17-hidratante-mantecorp",
    15: "mlf-19-aparador-mondial",  16: "mlf-20-body-splash",
    17: "mlf-21-wella-invigo",      18: "mlf-22-palmilha-gel",
    19: "mlf-23-microfone-lapela",  20: "mlf-24-jaqueta-cortavento",
    21: "mlf-25-varal-chao",        22: "mlf-26-potes-vidro",
    23: "mlf-27-impressora-hp",     24: "mlf-28-sabao-omo",
    25: "mlf-29-catraca-46",        26: "mlf-30-compressor-ar",
}


# Um bloco de oferta inteiro, de "{ loja:" ate o "link:". O campo "imagem:"
# mora DENTRO desse trecho -- e por isso que o mesmo padrao serve para LER a
# oferta e para ESCREVER a foto de volta nela, sem tocar em mais nada.
PADRAO_BLOCO = re.compile(
    r"\{\s*loja:\s*\"(.*?)\",\s*titulo:\s*\"(.*?)\",.*?link:\s*\"(.*?)\"", re.S)


def ler_ofertas():
    src = open(OFERTAS, encoding="utf-8").read()
    return PADRAO_BLOCO.findall(src)


def escrever_no_ofertas(feitos):
    """Grava o campo `imagem:` de cada bloco do ofertas.js.

    Era o unico elo feito a mao da esteira: o script sempre soube qual foto
    pertence a qual oferta (e o `feitos`), mas quem escrevia o caminho no
    ofertas.js era o Arimar. Resultado medido em 16/09/2026: as 14 ofertas
    novas ficaram com `imagem: ""` e SUMIRAM do gerador de pins (42 de 56).

    O que ele NAO faz, de proposito:
      - nao apaga nada e nao mexe em outro campo -- so troca o que esta entre
        as aspas do `imagem:` daquele bloco;
      - nao inventa bloco nem muda a ordem;
      - nao pisa em caminho ja escrito e igual (conta so o que mudou).
    """
    with open(OFERTAS, encoding="utf-8", newline="") as f:
        src = f.read()
    blocos = list(PADRAO_BLOCO.finditer(src))
    trocas = []
    # De tras para frente: mexer no fim nao desloca o inicio do bloco anterior.
    for i in sorted(feitos, reverse=True):
        if i >= len(blocos):
            continue
        bloco = blocos[i]
        texto = bloco.group(0)
        novo, n = re.subn(r"(imagem:\s*\")[^\"]*(\")",
                          lambda m: m.group(1) + feitos[i] + m.group(2),
                          texto, count=1)
        if n and novo != texto:
            src = src[:bloco.start()] + novo + src[bloco.end():]
            trocas.append((i, bloco.group(2), feitos[i]))
    if not trocas:
        print("\nofertas.js: nada a escrever, os %d caminhos ja estavam la"
              % len(feitos))
        return
    with open(OFERTAS, "w", encoding="utf-8", newline="") as f:
        f.write(src)
    print("\nofertas.js: %d campo(s) `imagem:` preenchido(s)" % len(trocas))
    for i, titulo, caminho in sorted(trocas):
        print("  %2d  %-34s <- %s" % (i + 1, titulo[:34], caminho))


def caixa_do_produto(im, limiar=28):
    """Retangulo que contem tudo o que nao e fundo preto."""
    cinza = im.convert("L")
    mascara = cinza.point(lambda p: 255 if p > limiar else 0)
    caixa = mascara.getbbox()
    return caixa or (0, 0, im.width, im.height)


def cortar_4x3(im):
    larg = im.width
    alt = round(larg * ALTURA / LARGURA)
    if alt >= im.height:                     # ja e mais larga que 4:3
        return im
    x0, y0, x1, y1 = caixa_do_produto(im)
    centro = (y0 + y1) // 2
    topo = centro - alt // 2
    topo = max(0, min(topo, im.height - alt))
    return im.crop((0, topo, larg, topo + alt))


def main():
    os.makedirs(DESTINO, exist_ok=True)
    blocos = ler_ofertas()

    alvo = {}                                # indice da oferta -> nome do arquivo
    n_am = n_ml = 0
    for i, (loja, titulo, _link) in enumerate(blocos):
        if loja == "amazon":
            n_am += 1
            achados = [f for f in os.listdir(ILUSTRA)
                       if f.startswith("azf-%02d-" % n_am)]
        else:
            n_ml += 1
            base = MAPA_ML.get(n_ml)
            achados = [base + ".png"] if base and os.path.exists(
                os.path.join(ILUSTRA, base + ".png")) else []
        if achados:
            alvo[i] = (achados[0], titulo)

    feitos, pesos = {}, []
    for i, (arquivo, titulo) in sorted(alvo.items()):
        origem = os.path.join(ILUSTRA, arquivo)
        nome = arquivo.replace(".png", ".jpg")
        saida = os.path.join(DESTINO, nome)
        im = Image.open(origem).convert("RGB")
        im = cortar_4x3(im).resize((LARGURA, ALTURA), Image.LANCZOS)
        im.save(saida, "JPEG", quality=QUALIDADE, optimize=True,
                progressive=True)
        peso = os.path.getsize(saida) / 1024
        pesos.append(peso)
        feitos[i] = "img/ofertas/" + nome
        print("  %2d  %-34s <- %-32s %5.0f KB" % (i + 1, titulo[:34],
                                                  arquivo, peso))

    sem = [(i, b[1]) for i, b in enumerate(blocos) if i not in feitos]
    print("\n%d de %d ofertas com foto | peso total %.1f MB | maior %.0f KB"
          % (len(feitos), len(blocos), sum(pesos) / 1024, max(pesos)))
    if sem:
        print("\nSEM ILUSTRACAO (%d) -- o card mostra o simbolo do cofre:" % len(sem))
        for i, t in sem:
            print("  %2d  %s" % (i + 1, t))

    mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "fotos-das-ofertas.json")
    json.dump({str(k): v for k, v in feitos.items()},
              open(mapa, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nmapa: " + mapa)

    escrever_no_ofertas(feitos)


if __name__ == "__main__":
    sys.exit(main())
