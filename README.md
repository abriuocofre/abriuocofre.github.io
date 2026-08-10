# Abriu o Cofre — página de ofertas

Página pública com os achados da Amazon e do Mercado Livre.
Fica no ar em **https://abriuocofre.github.io/**

> O mesmo conteúdo também continua no ar num endereço antigo, que serve as
> imagens dos posts já agendados no Instagram. Ele não aparece para ninguém —
> some sozinho quando a fila de posts terminar.

## Como publicar uma oferta nova

Só existe **um arquivo para mexer**: `ofertas.js`.

1. Abra `ofertas.js` aqui no GitHub e clique no lápis (canto direito).
2. Copie um bloco inteiro de oferta (do `{` até o `},`) e cole logo abaixo
   da linha `// ---- COLE AS OFERTAS NOVAS AQUI EM CIMA ----`.
3. Troque as informações pelas do produto.
4. Role até o fim e clique em **Commit changes**.

Em cerca de um minuto a página já está no ar com a oferta nova.

## Duas regras que não podem ser quebradas

- **Oferta da Amazon não leva preço escrito.** O contrato do Programa de
  Associados só permite mostrar preço vindo da própria Amazon. Em oferta da
  Amazon, deixe `preco: "",` — a página escreve sozinha
  *"preço atualizado na Amazon"*. No Mercado Livre pode escrever o valor.
- **Todo link tem que ser o link de afiliado**, gerado pela barra SiteStripe
  (Amazon) ou pelo painel de Afiliados (Mercado Livre).

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `ofertas.js` | as ofertas e os atalhos — **o único que se edita no dia a dia** |
| `index.html` | a página inteira (visual e funcionamento) |
| `logo.png` | o símbolo do cofre |
