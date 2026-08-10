/* ===========================================================================
   OFERTAS — o único arquivo que precisa ser editado no dia a dia.
   ===========================================================================

   Para publicar uma oferta nova, copie um bloco inteiro (de { até },)
   e cole no TOPO da lista. O que estiver em cima aparece primeiro.

   Campos:

     loja      "amazon"  ou  "mercadolivre"
     titulo    Nome do produto, curto. Como você falaria para um amigo.
     texto     Uma ou duas frases suas dizendo por que vale a pena.
     preco     ⚠️ SÓ para "mercadolivre". Na Amazon é PROIBIDO escrever
               o preço (regra do contrato de Associados). Em oferta da
               Amazon deixe assim:  preco: "",
     selo      Etiqueta curta no canto do card. Ex: "menor preço do ano",
               "frete grátis", "só hoje". Pode deixar "" se não tiver.
     imagem    Endereço da foto do produto. Deixe "" se não tiver — o card
               mostra o símbolo do cofre no lugar e continua bonito.
     link      O SEU link de afiliado. Amazon: gerado pela barra SiteStripe.
               Mercado Livre: gerado no painel de Afiliados.

   ⚠️ NUNCA apague a vírgula do fim de cada bloco.
   =========================================================================== */

const OFERTAS = [

  // ---- COLE AS OFERTAS NOVAS AQUI EM CIMA ----

  {
    loja:   "amazon",
    titulo: "Air fryer 5 litros",
    texto:  "Fritura crocante sem óleo e sem a sujeira da panela.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B08HZBX16R?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Creatina 1 kg",
    texto:  "Pote grande sai bem mais em conta por dose do que os de 300 g.",
    preco:  "",
    selo:   "+500 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1dcn6E4"
  },
  {
    loja:   "amazon",
    titulo: "Air fryer 8 litros",
    texto:  "Quem cozinha para muita gente não frita em duas levas.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0BJFJGW4B?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Máquina de acabamento",
    texto:  "O acerto da nuca e da barba em casa, entre um corte e outro.",
    preco:  "",
    selo:   "+50 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2LCk5F7"
  },
  {
    loja:   "amazon",
    titulo: "Caixa de som JBL Go 4",
    texto:  "Som de bolso que não morre com respingo de piscina.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0CX5C6WP3?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Bicicleta aro 29",
    texto:  "Alumínio não enferruja na chuva, e o freio a disco segura no molhado.",
    preco:  "",
    selo:   "+1.000 vendidas",
    imagem: "",
    link:   "https://meli.la/2qt9Z7Z"
  },
  {
    loja:   "amazon",
    titulo: "JBL Boombox 3",
    texto:  "Para churrasco, praia e quintal, longe de tomada.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0BF66H9XW?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Parafusadeira e furadeira",
    texto:  "Duas baterias: uma trabalha enquanto a outra carrega.",
    preco:  "",
    selo:   "+100 mil vendidas",
    imagem: "",
    link:   "https://meli.la/2ifkSsj"
  },
  {
    loja:   "amazon",
    titulo: "Organizador colmeia",
    texto:  "Meia, calcinha e cueca cada uma no seu quadradinho.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B078J855LF?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Lavadora portátil",
    texto:  "Sem tomada e sem mangueira presa: ela puxa a água de um balde.",
    preco:  "",
    selo:   "+100 mil vendidas",
    imagem: "",
    link:   "https://meli.la/2cGUqFq"
  },
  {
    loja:   "amazon",
    titulo: "Smartwatch Amazfit Active 2",
    texto:  "Passos, sono e batimentos no pulso, sem pegar o celular.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0F9PDYH3M?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Carregador turbo 40 W",
    texto:  "Carrega dois aparelhos ao mesmo tempo, sem brigar pela tomada.",
    preco:  "",
    selo:   "+50 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2YTn5cY"
  },
  {
    loja:   "amazon",
    titulo: "Galaxy Watch7 44 mm",
    texto:  "Acompanha treino e sono e avisa das mensagens no pulso.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0D96V7WRB?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Gel-creme facial",
    texto:  "Textura em gel: seca rápido e não deixa o rosto pegajoso.",
    preco:  "",
    selo:   "+100 mil vendidos",
    imagem: "",
    link:   "https://meli.la/22zbnt4"
  },
  {
    loja:   "amazon",
    titulo: "Aspirador automotivo",
    texto:  "Areia do tapete e migalha do banco saem sem tomada.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B07TM6SVL7?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Air fryer 4 litros",
    texto:  "Quatro litros dão conta do jantar de uma família pequena.",
    preco:  "",
    selo:   "+100 mil vendidas",
    imagem: "",
    link:   "https://meli.la/1ozgPPG"
  },
  {
    loja:   "amazon",
    titulo: "Jogo de lençol Queen",
    texto:  "Sai da máquina e vai para a cama sem passar ferro.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0CGJN34ZH?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 2 câmeras wi-fi",
    texto:  "Duas câmeras num kit só, e o mesmo aplicativo cuida das duas.",
    preco:  "",
    selo:   "+250 mil vendidas",
    imagem: "",
    link:   "https://meli.la/23gmfeW"
  },
  {
    loja:   "amazon",
    titulo: "Cafeteira Mondial",
    texto:  "Confira a tomada da sua casa antes de comprar.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B08HZJCDRQ?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Calça jeans masculina",
    texto:  "O elastano é o que deixa sentar e agachar sem repuxar.",
    preco:  "",
    selo:   "+250 mil vendidas",
    imagem: "",
    link:   "https://meli.la/2fxksPj"
  },
  {
    loja:   "amazon",
    titulo: "Escova elétrica Oral-B",
    texto:  "O sensor de pressão poupa a gengiva de quem escova com força.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B08PFSYF9R?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 2 travesseiros",
    texto:  "Vêm dois: dá para trocar os da cama de casal de uma vez só.",
    preco:  "",
    selo:   "+100 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1sqcdM7"
  },
  {
    loja:   "amazon",
    titulo: "Oral-B PRO Series 1",
    texto:  "Temporizador de 2 minutos para não escovar com pressa.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B07FFJ2T6T?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Tênis Kappa Park 2.0",
    texto:  "Tênis de marca, com etiqueta de original, para andar o dia inteiro.",
    preco:  "",
    selo:   "+100 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2nBmood"
  },
  {
    loja:   "amazon",
    titulo: "Carregador portátil",
    texto:  "Viagem, apagão e dia longo fora deixam de ser problema.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B094YR4SLJ?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Garrafa Stanley 473 ml",
    texto:  "A Stanley na versão leve: cabe no suporte do carro e na mochila.",
    preco:  "",
    selo:   "+1.000 vendidas",
    imagem: "",
    link:   "https://meli.la/2arixzz"
  },
  {
    loja:   "amazon",
    titulo: "Liquidificador 1400 W",
    texto:  "Vitamina, massa de bolo e até gelo sem travar no meio.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B08TLH52PQ?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Faqueiro 24 peças",
    texto:  "Serviço completo para seis pessoas, de uma marca que todo mundo conhece.",
    preco:  "",
    selo:   "+250 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1CnLq76"
  },
  {
    loja:   "amazon",
    titulo: "Echo Dot com Alexa",
    texto:  "Toca música, dá a previsão do tempo e acende a luz.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B09B8VGCR8?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 10 pares de meias",
    texto:  "Dez pares de uma vez: a gaveta para de ter meia sem par.",
    preco:  "",
    selo:   "+100 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1TqVyje"
  },
  {
    loja:   "amazon",
    titulo: "Kindle 11ª geração",
    texto:  "Lê no sol, na cama e no ônibus sem cansar a vista.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B09SWTG9GF?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 50 cabides",
    texto:  "O veludo segura a alça, e o perfil fino abre espaço no guarda-roupa.",
    preco:  "",
    selo:   "+10 mil vendidos",
    imagem: "",
    link:   "https://meli.la/139EXgo"
  },
  {
    loja:   "amazon",
    titulo: "Jogo de panelas",
    texto:  "Ovo que não gruda e panela que lava com uma passada.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B086YK7M5Y?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Hidratante corporal",
    texto:  "Loção de farmácia, em frasco que cabe na bolsa.",
    preco:  "",
    selo:   "+1.000 vendidos",
    imagem: "",
    link:   "https://meli.la/1BNaseo"
  },
  {
    loja:   "amazon",
    titulo: "Garrafa térmica Stanley 1 litro",
    texto:  "Café quente de manhã, água gelada à tarde, na mesma garrafa.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0CGY1H894?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 2 calças jogger",
    texto:  "Duas de uma vez: uma na máquina e a outra no corpo.",
    preco:  "",
    selo:   "+100 mil vendidas",
    imagem: "",
    link:   "https://meli.la/1AcRLNw"
  },
  {
    loja:   "amazon",
    titulo: "Filtro de linha",
    texto:  "Protege a TV e o computador do solavanco de energia.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B09BDF296F?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Aparador de pelos",
    texto:  "Dez acessórios num aparelho só, e liga em 110 ou em 220.",
    preco:  "",
    selo:   "+5 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1fe9Bvx"
  },
  {
    loja:   "amazon",
    titulo: "Mop giratório",
    texto:  "Piso limpo sem se abaixar e sem esfregão pingando pela casa.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B08DJ8WBSD?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 3 body splash",
    texto:  "Três fragrâncias para revezar na semana, em frasco grande.",
    preco:  "",
    selo:   "+50 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2Ud9WSd"
  },
  {
    loja:   "amazon",
    titulo: "Câmera wi-fi",
    texto:  "Você vê a casa pelo celular de onde estiver.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B09Q3K4YLS?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit Wella Nutri-Enrich",
    texto:  "A dupla completa, que é como o próprio fabricante manda usar.",
    preco:  "",
    selo:   "+1.000 vendidos",
    imagem: "",
    link:   "https://meli.la/1nrN1QM"
  },
  {
    loja:   "amazon",
    titulo: "Repetidor de wi-fi",
    texto:  "O quarto do fundo onde o vídeo trava tem conserto barato.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0755PV4H7?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Palmilha de gel",
    texto:  "Recorta no número do seu pé e passa de um sapato para o outro.",
    preco:  "",
    selo:   "+10 mil vendidas",
    imagem: "",
    link:   "https://meli.la/1zeawqm"
  },
  {
    loja:   "amazon",
    titulo: "Protetor solar facial",
    texto:  "Protege dos raios e ainda segura o brilho durante o dia.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0BD6755LC?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Microfone de lapela",
    texto:  "Prende na camisa e o celular grava sua voz longe do barulho da rua.",
    preco:  "",
    selo:   "+10 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1ejFAvb"
  },
  {
    loja:   "amazon",
    titulo: "Sanduicheira e grill",
    texto:  "Misto quente na ida e bife grelhado na volta.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B09WWY48B7?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Jaqueta corta-vento",
    texto:  "Leve o bastante para viver enrolada dentro da bolsa.",
    preco:  "",
    selo:   "+10 mil vendidas",
    imagem: "",
    link:   "https://meli.la/1a4Dr8g"
  },
  {
    loja:   "amazon",
    titulo: "Vaporizador de roupas",
    texto:  "Tira o vinco na hora, sem montar tábua de passar.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B08B6DLFYD?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Varal de chão 3 andares",
    texto:  "Dobra e encosta na parede quando a roupa termina de secar.",
    preco:  "",
    selo:   "+10 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2R9JMLQ"
  },
  {
    loja:   "amazon",
    titulo: "Fone Redmi Buds 4",
    texto:  "Corta o barulho do ônibus e passa de 30 horas com o estojo.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0B3XFRF6X?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit 10 potes de vidro",
    texto:  "Vidro não guarda cheiro nem mancha com molho de tomate.",
    preco:  "",
    selo:   "+100 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2tETpmw"
  },
  {
    loja:   "amazon",
    titulo: "Maleta com 129 peças",
    texto:  "O básico do conserto de casa, tudo no mesmo lugar.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B076N2S8FV?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Impressora HP Smart Tank",
    texto:  "Tanque de tinta: enche o reservatório em vez de trocar cartucho.",
    preco:  "",
    selo:   "+100 mil vendidas",
    imagem: "",
    link:   "https://meli.la/2jZTUMM"
  },
  {
    loja:   "amazon",
    titulo: "Caneca térmica 350 ml",
    texto:  "Café quente até a última xícara, mesmo bebendo devagar.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0CT61XYBM?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Sabão líquido 5 litros",
    texto:  "Galão de cinco litros: é a compra que demora a acabar.",
    preco:  "",
    selo:   "+250 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1hGj198"
  },
  {
    loja:   "amazon",
    titulo: "Kit churrasco",
    texto:  "O clássico do fim de semana, em três peças.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B07GS3MLJX?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Kit catraca 46 peças",
    texto:  "Quarenta e seis peças na maleta, cada uma no seu lugar.",
    preco:  "",
    selo:   "+250 mil vendidos",
    imagem: "",
    link:   "https://meli.la/1Dcc3by"
  },
  {
    loja:   "amazon",
    titulo: "Garrafa esportiva",
    texto:  "Água gelada o dia inteiro, sem peso na mochila.",
    preco:  "",
    selo:   "passou no corte do cofre",
    imagem: "",
    link:   "https://www.amazon.com.br/dp/B0CY44C3Y4?tag=abriuocofre-20"
  },
  {
    loja:   "mercadolivre",
    titulo: "Mini compressor de ar",
    texto:  "Calibra o pneu no estacionamento, sem depender do posto.",
    preco:  "",
    selo:   "+5 mil vendidos",
    imagem: "",
    link:   "https://meli.la/2Ddo8KM"
  },

];


/* ===========================================================================
   ATALHOS FIXOS — páginas da própria Amazon que ficam sempre no ar.
   Não têm preço nem foto, então não esbarram em nenhuma regra.
   =========================================================================== */

const ATALHOS = [
  {
    titulo: "Ofertas do Dia",
    texto: "A página de promoções da Amazon, atualizada por eles várias vezes ao dia.",
    link: "https://www.amazon.com.br/deals?tag=abriuocofre-20"
  },
  {
    titulo: "Os mais vendidos",
    texto: "O que o Brasil inteiro está comprando agora, categoria por categoria.",
    link: "https://www.amazon.com.br/gp/bestsellers/?tag=abriuocofre-20"
  },
  {
    titulo: "Em alta na semana",
    texto: "Produtos que subiram de posição nos últimos dias — costuma ter achado bom.",
    link: "https://www.amazon.com.br/gp/movers-and-shakers/?tag=abriuocofre-20"
  }
];
