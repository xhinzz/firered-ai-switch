# ACE em Pokémon FireRed (inglês) via Mail glitch (Mr. Mime + Farfetch'd + Retro Mail)

Pesquisa feita em 2026-10-08, antes da montagem. O que depois foi validado no console (e as ferramentas que automatizam
isso) está em [ace.md](ace.md). Convenções deste documento:

- **[fonte]** ao lado de cada código indica de onde ele foi copiado (lista completa na seção 6).
- **(conferir)** = não confirmado em fonte confiável ou inferido por mim; testar antes de automatizar.
- **(derivado)** = obtido aplicando, sem inventar nada, uma regra/tabela dada pela fonte.
- Nos nomes de caixa copiados do pokemon-ace-notes, `_` (ou espaço na forma `[...]`) = caractere ESPAÇO digitado. "Vazio" = posição não digitada (confirmar o nome antes).

> **Correção importante de premissa:** FireRed/LeafGreen **não estão no app Nintendo Switch Online (GBA)**.
> Foram lançados em 27/02/2026 como **jogos avulsos do eShop** (US$ 19,99 cada), sem save states, sem rewind,
> sem pontos de restauração e **sem Save Data Cloud** (página oficial da Nintendo: "Save Data Cloud: Not supported").
> Isso muda a seção de riscos: o único "desfazer" é não salvar e dar soft reset. Detalhes nas seções 2 e 5.

---

## 1. Resumo

**O que é.** A combinação Mr. Mime (Recycle) + Farfetch'd (Knock Off) + Retro Mail + batalha dupla é o **Mail glitch**
(Mail removal glitch, descoberto por luckytyphlosion). Ele não é o ACE em si: ele deixa o save num estado em que o
jogo passa a oferecer uma 7ª "carta" fantasma, a **question mark Mail (QMM)**, cuja tela vem preenchida com `???`.
As palavras escritas nessa carta são gravadas **direto nos dados do slot 1 da Caixa 3 do PC** (no jogo não japonês:
personality value e OT ID). Com 2 cartas bem escolhidas transforma-se um slot vazio na espécie glitch **0x0351**,
a "Pokémon de ACE" padrão do FRLG ocidental. Trocar de lugar (swap) qualquer Pokémon com a 0x0351 no PC faz o
console executar como código ARM os **nomes das caixas do PC** (o que se chama *PC swap / grab ACE*). A partir daí,
cada "código" é só um conjunto de nomes de caixa. [pokemon-ace-notes: introdução, mail-glitch, pre-E4 route; GCW: PC swap ACE]

**Por que funciona (curto).**
1. Knock Off na entrada do Mr. Mime arranca a Retro Mail sem liberar o slot de dados de carta; o Recycle no turno
   seguinte devolve a baga consumida antes, e o jogo perde o vínculo entre o item Mail e seu slot de dados.
2. Dando carta a um 6º Pokémon, o jogo usa o "ID de carta" 0xFF → 256º slot de carta, que cai **dentro dos dados do PC**
   (Caixa 3, slot 1). Cada palavra da carta = 16 bits escritos ali. [mail-glitch]
3. O nome da espécie glitch 0x0351 é longo demais e, ao ser carregado no swap, transborda um buffer e sobrescreve o
   ponteiro de função `monPlaceChangeFunc` com um endereço dentro das caixas; a execução escorrega até os nomes das
   caixas. [pokemon-ace-notes: introdução; GCW: PC swap ACE]

**O que dá para gerar.** Qualquer espécie (inclusive exclusivas do LeafGreen como Vulpix, evoluções por troca como
Alakazam/Gengar/Machamp/Golem, e Mew), por três caminhos documentados: (a) gerar o Pokémon "do nada" num slot do PC,
(b) fazer um NPC entregar um Pokémon de presente com o seu OT, (c) iniciar uma batalha selvagem/evento e capturar
(Mew com a flag "fateful encounter", que é obrigatória para ele obedecer). Também: itens, flags, respawn de lendários,
etc. [Sleipnir17 Pastebin VAgKwjwJ; E-Sh4rk CodeGenerator / EmeraldACE_web]

**Método encontrado nas fontes confiáveis: SIM**, com passo a passo completo para o setup (Mail glitch → 0x0351) e
códigos de teste. Para gerar Vulpix/Mew há dois níveis de prontidão — ver seção 4.10.

---

## 2. Versões

### 2.1 FireRed inglês GBA: 1.0 vs 1.1 (Rev 1 / "Rev A")

| | 1.0 (rev 0) | 1.1 (rev 1) | Fonte |
|---|---|---|---|
| Abertura (cena do logo GAME FREAK) | **sem** o texto "PRESENTS" | mostra "PRESENTS" | decomp `src/intro.c` (`#if REVISION >= 1 GFScene_CreatePresentsSprite`); busca citando GCW/Bulbapedia |
| Categoria na Pokédex (Pokémon capturado) | corta na 1ª palavra: Pidgey = "TINY POKéMON" | completa: "TINY BIRD POKéMON" | decomp `src/pokedex_screen.c` `DexScreen_PrintMonCategory` (`#if REVISION == 0` para no espaço); GCW "List of revision differences" |
| Data de build | `2004 04 26 11:20` | `2004 07 20 09:30` | decomp `src/main.c` |

**Como o jogador descobre a revisão (cartucho GBA):** o teste mais fácil é capturar um Pidgey/Spearow (categoria
"TINY BIRD") e abrir a entrada na Pokédex — "TINY" sozinho = 1.0. Alternativa: assistir à abertura e ver se aparece
"PRESENTS" abaixo de GAME FREAK.

**O método muda entre 1.0 e 1.1?**
- **Setup (Mail glitch, palavras da QMM, rota HOCK → 0x0351): NÃO.** "Works on English 1.0/1.1" [Papa Jefé doc];
  "Same steps on all versions and languages (except Japanese)" [Papa Jefé doc]; as tabelas de palavras do
  pokemon-ace-notes são por idioma, não por revisão.
- **Códigos de nome de caixa: depende do código.** Códigos relativos ao PC (gerar Pokémon no slot, teste do Bulbasaur,
  Box 14 exit) valem para todas as versões não japonesas. Códigos que usam **endereços de ROM** (rodar script via NPC,
  "Start Fateful Mew Battle", warp etc.) têm uma versão para 1.0, outra para 1.1 e outra para Switch
  (ex.: Sleipnir separa "For English FireRed_1.0" e "For English FireRed_1.1"; o CodeGenerator tem as opções
  "English 1.0", "English 1.1" e "English Switch").

**Códigos de versão no CodeGenerator do E-Sh4rk** (lidos do HTML de `index_frlg.html`):
`eng0` = "English 1.0", `eng1` = "English 1.1", `eng10` = "English Switch" (idem `spa10`, `fra10`, `ita10`,
`ger10`, `jap10`). **Não existe `eng11`**, e `?lang=eng10` seleciona o **Switch**, não a 1.0 do GBA. Detalhes e
diferenças entre eles na seção 4.12.

### 2.2 FireRed no Nintendo Switch (2026)

- **Não é NSO.** Lançamento avulso no eShop em 27/02/2026 (AU 28/02), US$ 19,99, digital, Switch e Switch 2;
  versões de idioma separadas, sem opção de trocar idioma; troca/batalha só por **comunicação local sem fio**
  (2–5 jogadores); "Online play is not supported". [Nintendo AU; pokemon.com; Nintendo Support FAQ; Wikipedia]
- **Sem save states / rewind / restore points** (razão citada: impedir savescum de encontros/trocas e por causa do
  Pokémon HOME). **Save Data Cloud: Not supported** (página oficial do produto). [Nintendo AU produto; Threads @serebii_joe; busca]
- **Soft reset:** A+B+SELECT(−)+START(+) e também A+B+X+Y. [GameRant]
- **Pokémon HOME:** compatibilidade liberada em 07/10/2026 (HOME 4.1.0), envio **só de ida**. Se o jogo em si recebeu
  atualização junto: **(conferir)** — fontes divergem (Siliconera fala em "update your game and app"; o FAQ da
  Nintendo só exige HOME 4.1.0).
- **Qual "revisão" é a ROM interna:** o decomp pret/pokefirered (cópia local, commit `037335f4`) já suporta o build do
  Switch como `GAME_REVISION = 10` (`make firered_switch`, `firered_switch.sha1`), data de build
  `"2025 12 19 15:38 22afedd9"`. Ele inclui as correções da 1.1 (`REVISION >= 1`) e acrescenta, entre outras:
  - **filtro de palavrões em toda tela de nomes**, inclusive **nome de caixa do PC** (`naming_screen.c`:
    `if (!svc_BadWordCheck(...)) SaveInputText();` — se o texto for barrado, **o nome simplesmente não é gravado**);
  - gravação do save delegada ao emulador (`svc_WriteSector`, `svc_FinishSave`);
  - Aurora Ticket e Mystic Ticket entregues ao entrar no Hall da Fama (Deoxys, Lugia, Ho-Oh viram obtíveis sem ACE);
  - correção do bug dos cães lendários sumirem com Roar; remoção do atalho de "Berry fix" na tela-título;
  - layout de RAM diferente (bibliotecas de link movidas) → endereços estáticos mudam.
  [decomp local; Serebii "Nintendo Switch Additions"]
- **Impacto no ACE (pokemon-ace-notes, FAQ FRLG, "As of 1st March 2026"):**
  - Precisam de versão própria para Switch: códigos com endereço de ROM, códigos que leem/escrevem RAM estática
    (seed do RNG, teleporte, dados da party), códigos que dependem de comportamento de GBA não emulado, e
    **códigos impossíveis de digitar por esbarrarem no filtro de palavrões da Nintendo**.
  - Ajustes gerais para Switch: **não colocar espaços nos 3 últimos caracteres das Caixas 4, 8 e 12** (deixar vazio e
    confirmar antes); trocar a saída antiga das caixas 10/11 (ver 4.10).
  - O Box 14 exit funciona no Switch (o Switch "já tem BIOS de GBA integrada"). [frlg-box-14-exit]
  - O CodeGenerator do E-Sh4rk tem as opções "English Switch" (e FR/IT/DE/ES Switch) para FRLG.
- **Como saber a versão no Switch:** só existe um build por idioma; a versão do software aparece nas opções do jogo
  no menu HOME (botão + sobre o ícone) **(conferir o texto exato do menu)**. Se aparecer algo além de 1.0.0, tratar
  códigos "English Switch" que usam endereços como suspeitos até achar confirmação.

---

## 3. Pré-requisitos

### 3.1 Pokémon (dados conferidos no decomp local)

| Papel | Espécie / origem | Nível e golpes | Item | Observações |
|---|---|---|---|---|
| Knock Off | **CH'DING** (Farfetch'd), troca por Spearow em `MAP_VERMILION_CITY_HOUSE2` | Knock Off no **nível 21**. Trocando um Spearow nv. 21 (cancelar a evolução no 20 com B) ele já vem com Sand-Attack, Leer, Fury Attack, Knock Off | vem segurando **STICK** (irrelevante) | OT ELYSSA, ID 8810. Obedece até 30 com 2 insígnias |
| Recycle | **MIMIEN** (Mr. Mime), troca por Abra em `MAP_ROUTE2_HOUSE` | Recycle no **nível 33**. Abra nv. 33 trocado → Mr. Mime nv. 33 com Magical Leaf, Encore, Psybeam, Recycle | **Retro Mail** (qualquer mensagem) | OT REYLEY, ID 1985. **Nv. 33 só obedece com 4 insígnias** (limite 50); com 2–3 insígnias o limite é 30 e ele pode desobedecer no turno do Recycle. Alternativa: Porygon aprende Recycle no 44 [mail-glitch] |
| Baga | qualquer Pokémon | — | baga consumível. Sitrus (restaura 30) ou Oran (10); ambas ativam com HP ≤ 50% | Itens escondidos: Oran Berry na Route 3 e Route 25; Sitrus Berry na Route 6 (decomp `map.json`) |
| Party 4–6 | quaisquer | — | **sem** Retro Mail | — |

Para a rota de ACE recomendada (HOCK 2.O) **os EVs do Mr. Mime não importam** (ele não é o Pokémon corrompido). Por
isso não é obrigatório treinar Abra até 33 sem evoluir: pode trocar um Abra baixo e subir o Mr. Mime até 33 (ele é
trocado, ganha EXP extra) — só respeitar a obediência. Papa Jefé recomenda Abra 33 apenas para a rota MIMIEN, em que
os EVs dele precisam ser exatos.

### 3.2 Itens

| Item | Quantidade | Onde | Fonte |
|---|---|---|---|
| Retro Mail | "preferably at least one hundred" (mínimo realista ~20: 1 perdida no glitch + 5 de "enchimento" recuperáveis + 1 consumida por confirmação da QMM) | Celadon Dept. Store 4F, 50 cada (100 = 5.000) | mail-glitch; Jefé |
| HP Up | **8** (ou 1 + 7 duplicações pela QMM) | Celadon Dept. Store 5F, 9.800 cada (decomp `CeladonCity_DepartmentStore_5F`) | pre-E4 route; Jefé |
| Baga consumível | 1 | ver 3.1 | mail-glitch |

### 3.3 Progresso na história

- **Mail glitch:** precisa de Celadon (Retro Mail), dos dois Pokémon de troca e de uma batalha dupla.
  Recomendado ter a **4ª insígnia (Erika, Celadon)** para o Mr. Mime nv. 33 obedecer.
- **Rota HOCK 2.O (pré-Elite 4):** só usa grupos de palavras sempre liberados (TRAINER, MISC., ADJECTIVES — decomp
  `easy_chat.c`: apenas EVENTS, MOVE 1, MOVE 2 exigem `FLAG_SYS_GAME_CLEAR`). O HOCK precisa derrotar 1 Caterpie
  selvagem (Viridian Forest) e 1 Doduo (Route 16) ou 1 Mankey (Route 22) para os EVs (4.6); não é Pokémon guardado.
- **Rota pós-Elite 4 (alternativa, 1 carta só):** exige Hall da Fama (grupo MOVE 1/MOVE 2) e Magikarp **visto** na
  Pokédex.
- **Mew pelo código "Fateful Mew Battle at Daycare":** Day Care da Route 5; não exige Elite 4.

### 3.4 Onde fazer a batalha dupla (decomp `data/scripts/trainers.inc`, `trainer_parties.h`, `map.json`)

| Local | Treinadores | Time | Quando |
|---|---|---|---|
| **Route 8** | Twins **Eli & Anne** | Clefairy 22 + Jigglypuff 22 | a mais cedo: depois de Rock Tunnel/Lavender, antes de Celadon (conferir acesso no jogo) |
| **Route 12** | Young Couple **Gia & Jes** | Nidoran♂ 24 + Nidoran♀ 24 | ao norte do Snorlax (y=63/64 vs Snorlax y=70): acessível vindo de Lavender sem Poké Flute |
| **Route 16** | Young Couple **Lea & Jed** | Rapidash 29 + Ninetales 29 | oeste de Celadon, trilha norte (Snorlax fica na trilha sul). **A preferida pelas fontes** (só dão EV de Speed/Sp.Def) |
| Route 14 / 15 | Twins Kiri & Jan / Crush Kin Ron & Mya | Lv 29 | região de Fuchsia (depois) |
| Route 19, 21, ilhas Sevii | vários pares | — | mais tarde |

Revanches pelo VS Seeker também servem ("VS Seeker Rematches are OK!" [Jefé]). Se ainda não lutou com o par, pare
fora da linha de visão deles e **salve ali** [mail-glitch].

### 3.5 PC e party

- **Caixa 3, slot 1 vazio** antes de usar a QMM (tudo que estiver ali é corrompido).
- Para disparar o ACE com a 0x0351: **Caixa 13 a partir do slot 7 e toda a Caixa 14 vazias** (exceto bootstraps feitos
  para isso); para os códigos de teste, **Caixa 9 slot 30 vazio**; para o código do Sleipnir, **Caixas 13 e 14 vazias** e
  **Caixa 9 slot 27 vazio**.
- Nunca guardar nada de valor nos **slots 7, 8 e 9 da Caixa 13** (a 0x0351 gera bad eggs ali). Guardar a 0x0351 fora
  das Caixas 13 e 14. [frlg-faq]
- HOCK e 0x0351 não têm `hasSpecies`: **somem se entrarem numa seleção em grupo** (mão laranja arrastando vários).
  Mover sempre um por vez. [general-faq]
- Pokémon "fantasma"/bad eggs invisíveis depois do ponto de entrada derrubam o ACE (limpar com seleção em grupo).
- Party: 6 Pokémon na hora de abrir a QMM; ordem específica na batalha (4.2).
- Nomes de caixa: o setup não usa; cada código depois define os seus.

---

## 4. Passo a passo

> Regra geral das fontes: **salvar antes de cada etapa irreversível e verificar o resultado ANTES de salvar de novo**.
> "After executing a code you should check if it was successful or not before saving the game." [Sleipnir VAgKwjwJ]

### 4.1 Obter os Pokémon e itens
1. Capturar Spearow (rotas 3/4) e Abra (rota 24/25 etc.).
2. Trocar Spearow por CH'DING (Vermilion, `MAP_VERMILION_CITY_HOUSE2`); levar CH'DING ao nv. 21 (ou trocar Spearow já 21).
3. Trocar Abra por MIMIEN (`MAP_ROUTE2_HOUSE`); levar MIMIEN ao nv. 33.
4. Em Celadon: comprar Retro Mail (4F) e 1 HP Up (5F). Pegar uma Oran/Sitrus Berry.
5. Dar uma Retro Mail ao Mr. Mime (escrever qualquer coisa e confirmar).

### 4.2 Disparar o Mail glitch (batalha dupla) [mail-glitch; Jefé]
1. Ordem da party: **1º** Pokémon segurando a baga; **2º** Farfetch'd (Knock Off); **3º** Mr. Mime (Recycle) segurando
   Retro Mail; 4º–6º sem carta.
2. Ir até perto de um par de batalha dupla (3.4) sem entrar na linha de visão. **Salvar.**
3. Iniciar a batalha dupla (falar com o par).
4. Fazer o 1º Pokémon consumir a baga (HP ≤ 50%). Quantos turnos forem precisos.
   *(Sugestão minha, não está nas fontes: o Farfetch'd pode atacar o aliado para baixar o HP.)*
5. No turno seguinte ao consumo: no 1º Pokémon escolher **POKéMON → trocar pelo Mr. Mime**; no Farfetch'd escolher
   **FIGHT → KNOCK OFF mirando o aliado** (a posição de onde sai o 1º Pokémon). A troca acontece antes; o Knock Off acerta
   o Mr. Mime que acabou de entrar.
   Mensagem de sucesso: "[ _ ] knocked off [ _ ]'s RETRO MAIL" [Jefé].
6. No turno seguinte: Mr. Mime usa **RECYCLE**. Mensagem de sucesso: "[ _ ] found one [ _ ] BERRY!" [Jefé].
7. Terminar a batalha (tudo bem se ele comer a baga reciclada).
8. Verificação: **nenhum** Pokémon da party segurando carta = glitch ativo. Caso contrário, soft reset e repetir.

### 4.3 Confirmar a question mark Mail [mail-glitch; Jefé]
1. Caixa 3, slot 1 vazio.
2. Party com 6 Pokémon. Dar Retro Mail aos 5 primeiros (qualquer mensagem; Jefé: POKéMON → ABRA é a mais rápida).
3. Dar Retro Mail ao **6º**: deve abrir a tela de carta já preenchida com **`???` em todas as 9 palavras**. Isso é a QMM.
   - Se o glitch foi disparado mais de uma vez, a QMM aparece antes: nº de Pokémon necessário = 7 − nº de disparos.
   - Se aparecer uma mensagem antiga em vez de `???`: depositar e retirar esse Pokémon do PC (zera o Mail ID) e repetir.
4. Não escrever nada ainda: START para confirmar ou B para sair. Pode salvar depois de confirmar que a QMM aparece.
5. As 5 cartas normais podem ser retiradas; o glitch continua. Para abrir a QMM de novo, basta repetir 2–3.

Layout da carta: grade de 2 colunas × 5 linhas, 9 palavras (decomp `easy_chat_2.c`: `EASY_CHAT_TYPE_MAIL`,
`numColumns = 2`, `numRows = 5`; `MAIL_WORDS_COUNT 9`). Palavra 1 = linha 1 esquerda, 2 = linha 1 direita,
3 = linha 2 esquerda, 4 = linha 2 direita, e assim por diante. No FRLG não japonês as palavras 1–2 escrevem o
personality value e 3–9 o OT ID do slot (tabela completa em [mail-glitch]).

### 4.4 Duplicar o HP Up (opcional, mas faça ANTES do 4.5)
Mecânica documentada: confirmar a QMM sem mudar nada gasta 1 Retro Mail e acrescenta +1 do item que o 6º Pokémon
estiver segurando. [mail-glitch; Jefé]
1. 6º Pokémon segura o HP Up. Caixa 3, slot 1 vazio.
2. Dar Retro Mail a ele → QMM (`???`) → confirmar sem editar. +1 HP Up na mochila.
3. Repetir até ter 8.

Por que antes: a QMM guarda as últimas palavras escritas. Depois do 4.5, confirmar a QMM com o slot vazio recria o
HOCK lá dentro (inferência a partir de "Triggering the question mark Mail again will not reset the contents" — conferir).

### 4.5 Criar o HOCK (espécie glitch 0x0200) — rota "Pre-Elite Four (HOCK 2.O)" [pokemon-ace-notes; Jefé]
1. Caixa 3, slot 1 **vazio**.
2. Abrir a QMM (dar Retro Mail ao 6º). Deixar a palavra 1 como `???`.
3. **Escrever exatamente** (inglês) [frlg-non-jpn-pre-e4-route]:

   | | coluna esquerda | coluna direita |
   |---|---|---|
   | linha 1 | `???` (não mexer) | `HIGHS` |
   | linha 2 | `I CHOOSE YOU` | `WANDERING` |

   Grupos das palavras (decomp `include/constants/easy_chat.h`): `HIGHS` = MISC., `I CHOOSE YOU` = TRAINER,
   `WANDERING` = ADJECTIVES. Palavras 5–9 ficam `???`.
4. Confirmar (START → YES).
5. Abrir o PC → Caixa 3, slot 1: deve haver **HOCK, nível 4, fêmea**. Ícone pode ser de outro Pokémon com cores
   erradas ou um "?" — o que vale é o nome. [frlg-faq]
   - Se o nome não for HOCK ou virar bad egg: palavras ou slot errados. Apagar o bad egg com seleção em grupo e refazer.

### 4.6 EVs do HOCK [pokemon-ace-notes; Jefé]
1. Retirar o HOCK para a party (cursor normal, um por vez).
2. Dar **8 HP Up** (= 80 EV de HP).
3. Batalhar e derrotar **1 Caterpie** (Viridian Forest) → +1 EV de HP.
4. Batalhar e derrotar **1 Doduo** (Route 16) **ou 1 Mankey** (Route 22) → +1 EV de Ataque.
5. O HOCK só pode ganhar EXP nessas duas lutas ("safe to use in battle and switch out" [Jefé]). Total final esperado:
   81 HP / 3 Atk (o HOCK já nasce com 2 de Ataque). Evitar Exp. Share; Pokérus dobraria os EVs (conferir que não tem).
6. Devolver o HOCK para a **Caixa 3, slot 1**.

### 4.7 Converter em 0x0351 [pokemon-ace-notes; Jefé]
1. Abrir a QMM: aparece a mensagem anterior (normal).
2. **Trocar de lugar as palavras 2 e 4** (não precisa mexer em 1 e 3):

   | | coluna esquerda | coluna direita |
   |---|---|---|
   | linha 1 | `???` | `WANDERING` |
   | linha 2 | `I CHOOSE YOU` | `HIGHS` |

3. Confirmar (START → YES).
4. Caixa 3, slot 1: espécie **0x0351**, nome parecido com `ËÁÈîÂ Î ËÁ`, **nível 100, macho**. ACE pronto.
5. Mover a 0x0351 (cursor normal) para fora das Caixas 13–14. **Agora pode salvar.**

**Alternativa pós-Elite 4 (uma carta só, slot vazio, Magikarp visto)** [frlg-non-jpn-post-e4-route; Jefé]:

| | coluna esquerda | coluna direita |
|---|---|---|
| linha 1 | `BULK UP` | `CAPABLE` |
| linha 2 | `KARATE CHOP` | `MAGIKARP` |

`MAGIKARP` tem de vir do grupo **POKéMON**, não de POKéMON2 nem do modo A-Z (índices internos diferentes). [frlg-faq]

### 4.8 Como disparar o ACE [pokemon-ace-notes]
Antes: nomes de caixa do código digitados e conferidos; pré-requisitos do código feitos; Caixa 13 slot 7 em diante e
Caixa 14 vazias. Conferir a Caixa 13 antes de cada disparo: a conversão deixou um "Bad EGG" no slot 9; saiu com seleção
em grupo começando nele e cobrindo os slots 7-9 (soltar no mesmo lugar só devolve quem tem `hasSpecies`).
1. PC → **MOVE POKéMON**.
2. **SELECT** → cursor laranja ("Relocate Mode"; Jefé chama de mão amarela).
3. **A** sobre qualquer Pokémon (pega).
4. Levar até a 0x0351 → **A** (troca) → **A** de novo (troca de volta).
5. Soltar o Pokémon em qualquer lugar.

Editar nome de caixa: no PC, cursor no título da caixa → A → NAME (o mesmo menu tem WALLPAPER). No Switch, **reabrir e
conferir cada nome depois de digitar**: se o filtro barrar, o nome antigo continua (decomp `naming_screen.c`).

Estado montado no save: caixas 1-11 com "Make any Pokémon shiny" (`C.kn5 9n` … `.o`, alvo Caixa 10 casa 2), Weedle na
Caixa 1 casa 3 como peça do disparo. `menus.tornar_shiny` faz o ciclo inteiro (confere Caixas 13/14 e a casa alvo, salva
antes de disparar, confere a estrela do resumo no sprite em 106,40). Trocar esses nomes desliga a ferramenta.

### 4.9 Códigos de setup / bootstrap

#### 4.9.1 Teste de funcionamento (Bulbasaur) — rodar primeiro [frlg-non-jpn-pre-e4-route, "Checking if everything worked"]
Caixa 9 slot 30 vazio. Nomes:
```
Box  1:	C C U n n R E o	[CCUnnREo]
Box  2:	P R o / G w m  	[PRo/Gwm]   (change '/' to 'B' for inaccurate emulators)
Box  3:	A A T S , m    	[AATS,m]
Box  4:	A / F Q m      	[A/FQm]
Box  5:	D F Q m        	[DFQm]
Box  6:	_ F o H I o o r	[ FoHIoor]
Box  7:	x n            	[xn]
Box 8+:	(anything)
```
Resultado: **Bulbasaur shiny, nível 0, fêmea** na Caixa 9 slot 30 (pode apagar depois).
- Este código já usa a saída ` FoHIoor`/`xn`, que é a versão "ajustada para Switch" do FAQ.
- **No Switch, usar `/` (variante console).** O FAQ do Switch não manda trocar para `B`; mas isso é inferência
  **(conferir)**: se travar com `/`, tentar `B` e anotar qual o Switch aceita — essa escolha vale para todos os códigos
  com variantes "console/new emulators" vs "old/inaccurate emulators".

#### 4.9.2 Box 14 exit (necessário para todos os códigos "Bootstrapped") [frlg-box-14-exit]
```
Box 14: U . o _ _ , o a	[U.o  ,oa]
```
Papéis de parede (inglês):
- Box 1: ETCETERA → STARS
- Box 2: SCENERY 1 → DESERT
- Box 3 and later: anything

Teste opcional (Kadabra) [frlg-box-14-exit]:
```
Box  1: C C U n n R . o [CCUnnR.o]
Box  2: P R o / G w m   [PRo/Gwm]
Box  3: A A R G . m     [AARG.m]
Box  4: A / F Q m       [A/FQm]
Box  5: D F Q m         [DFQm]
Box  6: A               [A]
Box  7: A               [A]
Box  8: A               [A]
Box  9: A               [A]
Box 10: A               [A]
Box 11: A               [A]
Box 12: A               [A]
Box 13: A               [A]
Box 14: (leave as is)
```
Resultado: sem travar, **Kadabra shiny, nível 0, fêmea** no último slot da Caixa 9. Se renomear a Caixa 14 depois, os
códigos "Bootstrapped" deixam de funcionar até refazer este passo.

(Papa Jefé usa outra forma de Box 14 exit, gravada via ACE: nome final `[ _ F o ì _ _ _ _ ]`. As duas existem; este
documento usa a do pokemon-ace-notes porque se digita direto.)

#### 4.9.3 Ajustes de Switch para códigos antigos [frlg-faq, "Code adjustments needed for Switch rereleases"]
- Caixas 4, 8 e 12: não digitar espaço nas 3 últimas posições — deixar vazio e confirmar antes.
  ```
  Original:
  Box 4: E _ F R m _ _ _ [E FRm   ]

  Adjusted:
  Box 4: E _ F R m       [E FRm]
  ```
- Saída antiga das Caixas 10/11 (todos os códigos grab ACE do Pastebin do Sleipnir):
  ```
  Original:
  Box 11: … o _ _ _ _ _ _ […o      ]

  Adjusted:
  Box 11: . o             [.o]
  ```
- Saída mais nova:
  ```
  Original:
  Box 10: _ F o H I C o r [ FoHICor]
  Box 11: B n             [Bn]

  Adjusted:
  Box 10: _ F o H I o o r [ FoHIoor]
  Box 11: x n             [xn]
  ```
Motivo técnico (minha leitura, conferir): os 3 últimos caracteres das caixas 4/8/12 mais o terminador formam uma
instrução ARM inteira (`FF000000`, condição "NV"), e a saída antiga usa `movs pc, #0x354` (com S); o emulador do Switch
trava nessas duas instruções onde o GBA real não trava.

### 4.10 Gerar Pokémon específicos

#### 4.10.1 Caminho A — códigos com nomes prontos nas fontes (Sleipnir17, "Generate any shiny Pokémon in your box")
Fonte: [Sleipnir VAgKwjwJ], "For all non-Japanese versions" (vale 1.0, 1.1; Switch com os ajustes de 4.9.3).
Gera o Pokémon **shiny** na **Caixa 9 slot 27** (deixar vazio), **com todos os dados em branco**: sem golpes, sem EVs,
sem IVs, nível 0, sem OT. Requer Caixas 13 e 14 vazias.

Modelo copiado da fonte (o valor de 4 dígitos hex da espécie é ♥♦♣♠):
```
Box names:
  Box 1:  (*……oGSUn) [two …]
* = F if ♠=0, G if ♠=1, H if ♠=2, I [upper case i] if ♠=3, J if ♠=4, K if ♠=5, L if ♠=6, M if ♠=7, N if ♠=8, O [upper case o] if ♠=9, P if ♠=A, Q if ♠=B, R if ♠=C, S if ♠=D, T if ♠=E, U if ♠=F
 
  Box 2:  (-…o*D!n ) [one …; ends with space]
* = J if ♣=0, K if ♣=1, L if ♣=2, M if ♣=3, N if ♣=4, O [upper case o] if ♣=5, P if ♣=6, Q if ♣=7, R if ♣=8, S if ♣=9, T if ♣=A, U if ♣=B, F if ♣=C, G if ♣=D, H if ♣=E, I [upper case i] if ♣=F

  Box 3:  (EE*B!n  ) [ends with two spaces]
if ♣=C,D,E,F, then
* = J if ♦=0, K if ♦=1, L if ♦=2, M if ♦=3, N if ♦=4, O [upper case o] if ♦=5, P if ♦=6, Q if ♦=7, R if ♦=8, S if ♦=9, T if ♦=A, U if ♦=B, F if ♦=C, G if ♦=D, H if ♦=E, I [upper case i] if ♦=F
if ♣=0,1,2,3,4,5,6,7,8,9,A,B, then
* = I [upper case i] if ♦=0, J if ♦=1, K if ♦=2, L if ♦=3, M if ♦=4, N if ♦=5, O [upper case o] if ♦=6, P if ♦=7, Q if ♦=8, R if ♦=9, S if ♦=A, T if ♦=B, U if ♦=C, F if ♦=D, G if ♦=E, H if ♦=F

  Box 4:  (E*/!n   ) [ends with three spaces]
if ♦=D,E,F or (♦=C and ♣=C,D,E,F), then
* = J if ♥=0, K if ♥=1, L if ♥=2, M if ♥=3, N if ♥=4, O [upper case o] if ♥=5, P if ♥=6, Q if ♥=7, R if ♥=8, S if ♥=9, T if ♥=A, U if ♥=B, F if ♥=C, G if ♥=D, H if ♥=E, I [upper case i] if ♥=F
if ♦=0,1,2,3,4,5,6,7,8,9,A,B, or (♦=C and ♣=0,1,2,3,4,5,6,7,8,9,A,B), then
* = I [upper case i] if ♥=0, J if ♥=1, K if ♥=2, L if ♥=3, M if ♥=4, N if ♥=5, O [upper case o] if ♥=6, P if ♥=7, Q if ♥=8, R if ♥=9, S if ♥=A, T if ♥=B, U if ♥=C, F if ♥=D, G if ♥=E, H if ♥=F

  Box 5:  (k-Po*1xm) [number one]                                                     * = , on old emulators ♀ on new emulators/console
  Box 6:  (EEE/…Rm ) [one …; ends with space]
  Box 7:  (EED…Rm  ) [one …; ends with two spaces]
  Box 8:  (E       ) [ends with seven spaces]
  Box 9:  (E       ) [ends with seven spaces]
  Box 10: (     …oa) [starts with five spaces; one …]
  Box 11: (…o      ) [one …; ends with six spaces]
  Box 12 onwards: Anything
```

Índices (Gen III, Gen 1 = nº da Pokédex Nacional): **Vulpix 37 = `0025`**, **Mew 151 = `0097`**,
Alakazam 65 = `0041`, Machamp 68 = `0044`, Golem 76 = `004C`, Gengar 94 = `005E`.

**Vulpix (`0025` → ♥=0 ♦=0 ♣=2 ♠=5)** (derivado):

| Caixa | GBA (console) — notação da fonte | Switch (ajustes do FAQ aplicados, conferir) |
|---|---|---|
| 1 | `(K……oGSUn)` [two …] | igual |
| 2 | `(-…oLD!n )` [one …; ends with space] | igual |
| 3 | `(EEIB!n  )` [ends with two spaces] | igual |
| 4 | `(EI/!n   )` [ends with three spaces] | `EI/!n` (5 caracteres, confirmar) |
| 5 | `(k-Po♀1xm)` [number one] | igual |
| 6 | `(EEE/…Rm )` [one …; ends with space] | igual |
| 7 | `(EED…Rm  )` [one …; ends with two spaces] | igual |
| 8 | `(E       )` [ends with seven spaces] | `E` + 4 espaços, confirmar |
| 9 | `(E       )` [ends with seven spaces] | igual |
| 10 | `(     …oa)` [starts with five spaces; one …] | igual |
| 11 | `(…o      )` [one …; ends with six spaces] | `.o` (ponto, o minúsculo) |

**Mew (`0097` → ♥=0 ♦=0 ♣=9 ♠=7)** (derivado): igual ao Vulpix, exceto
- Caixa 1: `(M……oGSUn)` [two …]
- Caixa 2: `(-…oSD!n )` [one …; ends with space]

Conferência da derivação (feita por mim a partir das instruções ARM listadas na fonte: `mov r11,#0xC♠`, depois
`adc` de `0xC*0`, `0xC*00` e `0xC*000`, com carry 0): Vulpix 0xC5 + 0xC60 + 0xC300 + 0xC3000 = 0xD0025 → 16 bits
baixos `0025`; Mew 0xC7 + 0xCD0 + 0xC300 + 0xC3000 = 0xD0097 → `0097`. Bate.

**Limitações do caminho A (importantes):**
- Pokémon "em branco": nível 0, sem golpes, sem OT/nome do treinador, sem apelido válido. Precisa ganhar nível (Rare
  Candy/Day Care) para aprender golpes.
- **Mew gerado assim nunca obedece**: no FRLG, Mew e Deoxys sem a flag *fateful encounter* desobedecem sempre
  (decomp `src/battle_util.c`, `IsBattlerModernFatefulEncounter`: "only false if illegal Mew or Deoxys"). Para Mew use o
  caminho B.
- Sem OT seu, conta como "de outro treinador" para obediência.
- Bom como prova de conceito e para "registrar" a espécie; para Pokémon usáveis/enviáveis ao HOME, prefira o caminho B.

#### 4.10.2 Caminho B — códigos do CodeGenerator (Pokémon com dados do próprio jogo) — **nomes não incluídos aqui**
O CodeGenerator monta os nomes de caixa no navegador a partir de um modelo; não há nomes prontos publicados para estes
códigos (pendência, seção 7). Uso detalhado na seção 4.12. Resumo:
1. Abrir `https://e-sh4rk.github.io/CodeGenerator/index_frlg.html?lang=eng10&game=fr` (Switch) — ou `lang=eng1`
   (cartucho 1.1) / `lang=eng0` (cartucho 1.0).
2. Escolher o código, preencher a espécie, clicar **Compute** e copiar os nomes da saída caractere a caractere.

| Objetivo | Código no CodeGenerator | Saída | Como usar (comentários do próprio código) |
|---|---|---|---|
| **Vulpix** (ou qualquer espécie: Alakazam, Gengar…) com **seu OT** | **Create any Gift Pokemon (Bootstrapped)** — autor Theocatic; mesmo arquivo para eng0/eng1/eng10 | Bootstrapped (exige 4.9.2) | `PokemonHex` = espécie (Vulpix = 37), `PokemonLV = 25` por padrão. Executar o ACE e falar com o **senhor (Old Gentleman) do Centro Pokémon de Viridian** |
| **Mew obediente** | **Fateful Mew Battle at Daycare (Bootstrapped)** — Adrichu00 e PapaJefe; arquivo universal (eng0/eng1/eng10) | Bootstrapped | Depositar antes um Pokémon no Day Care da **Route 5**: o nível do Mew = nº índice desse Pokémon (Pikachu #25 → Mew nv. 25; sem depósito = nv. 0). Executar e falar com o Daycare Man → batalha contra Mew com *fateful encounter*. Ele repete a batalha até você sair do prédio. Não exige Elite 4 |
| Batalha selvagem com qualquer espécie | **Start wild battle with any Pokemon** — Theocatic / final | GrabACEExit (saída das caixas 10/11) | Falar com o Old Gentleman de Viridian; nv. 25 padrão. No Switch a saída 10/11 pode precisar do ajuste 4.9.3 (conferir) |
| Pokémon "do nada" (como o caminho A) | **Create Pokemon species from nothing** | GrabACEExit | Cria na Caixa 10 slot 19, shiny, só a espécie, com `hasSpecies` setado |

Há também "Start Fateful Mew Battle (Bootstrapped)" (PapaJefe), com arquivos distintos para FR 1.0, FR 1.1 e
FR Switch, que exige Elite 4 e mexe nas flags do evento do Deoxys; o próprio arquivo recomenda a versão "at Daycare".

Sem ACE, no Switch: exclusivas do LeafGreen e evoluções por troca são obtíveis legitimamente por troca local sem fio
com outro Switch + outra cópia (LeafGreen), e Deoxys/Lugia/Ho-Oh após o Hall da Fama (tickets).

### 4.11 Pontos de verificação por tela (úteis para a automação)
| Etapa | Evidência na tela |
|---|---|
| Knock Off | texto "knocked off … RETRO MAIL" |
| Recycle | texto "found one … BERRY!" |
| Glitch ativo | após a batalha, ninguém segura carta |
| QMM | carta do 6º Pokémon abre com `???` nas 9 palavras |
| HOCK | Caixa 3 slot 1: nome HOCK, Lv4, fêmea |
| 0x0351 | nome tipo `ËÁÈîÂ Î ËÁ`, Lv100, macho |
| Nome de caixa aceito (Switch) | reabrir e comparar com o esperado (o filtro descarta sem aviso) |
| ACE ok | Bulbasaur shiny Lv0 ♀ em Caixa 9/30; Kadabra shiny Lv0 ♀ no último slot da Caixa 9 |
| Falha | travamento/tela congelada → fechar o software e voltar ao último save |

### 4.12 CodeGenerator do E-Sh4rk (FRLG): o que ele assume e como usar

Fontes desta seção: página `https://e-sh4rk.github.io/CodeGenerator/index_frlg.html` (HTML lido), documentação
`https://e-sh4rk.github.io/CodeGenerator/doc/index.html`, repositório `https://github.com/E-Sh4rk/CodeGenerator`
(código-fonte OCaml lido: `Utils/settings.ml`, `Charset/charset.ml`, `Charset/name.ml`, `html/scripts.js`,
`html/autocomplete.js`) e os modelos de código em `https://e-sh4rk.github.io/EmeraldACE_web/files_frlg/`.

#### 4.12.1 Qual setup os códigos gerados assumem
- A própria página diz: **"Note: Codes are for Grab ACE by default (unless specified otherwise in the title)."**
- Os tutoriais que ela indica são o vídeo do Papa Jefé (`https://youtu.be/v_JfJ0WS07U`) e o "Written guide" =
  pokemon-ace-notes. Ou seja: **grab/swap ACE com a espécie glitch 0x0351**, criada pela question mark Mail depois do
  **Mail glitch (Mr. Mime com Recycle + Farfetch'd com Knock Off + Retro Mail + batalha dupla)** — exatamente o setup
  das seções 3 a 4.7. Pré-requisitos e passos: seções 3, 4.1–4.8.
- Códigos com **"(move ACE)"** no título são do outro método (ACE por golpe inválido, que exige trazer um Pokémon de um
  Emerald por troca — Sleipnir `https://pastebin.com/UFspsi9N`). **Não usar** com a 0x0351.
- Ponto de entrada: o swap com a 0x0351 (4.8) faz a CPU entrar nas caixas do PC (área de ACE a partir da Caixa 13
  slot 7, mais toda a Caixa 14) e escorregar até os nomes das caixas, que são o código.
- Cada código declara sua saída no cabeçalho (`@@ exit = ...`):
  - `GrabACEExit` — saída nas caixas 10/11 (`mov r0, #0x0` / `mov r15, #0x354`); não precisa de preparo.
  - `Bootstrapped` — exige o **Box 14 exit** já montado (4.9.2). Renomear a Caixa 14 quebra estes códigos.
  - `ROM_BX_lr_Box10_Grab` e similares — saídas que pulam para a ROM.
  Os comentários do próprio código listam o resto (local onde executar, slots vazios, NPC com quem falar).

#### 4.12.2 Como usar o gerador
1. Abrir `https://e-sh4rk.github.io/CodeGenerator/index_frlg.html?lang=eng10&game=fr`.
   `lang` e `game` só pré-selecionam os dois primeiros seletores (`html/scripts.js`). Valores: `eng0` (English 1.0),
   `eng1` (English 1.1), `eng10` (English Switch); `game=fr` (Fire-Red) ou `game=lg` (Leaf-Green).
2. 3º seletor: escolher o código (há filtro por categoria). O texto do código aparece em **Main code**; a aba
   **Exit codes** contém a biblioteca de saídas (não mexer).
3. Ajustar os parâmetros no Main code. Linhas marcadas com `@input:species` têm autocompletar: digitar o nome
   (ex.: `VULPIX`) e escolher a sugestão, ou escrever o número (ex.: `PokemonHex = 37`). Outros parâmetros comuns:
   `PokemonLV = 25`, `NPC = 2`, `inaccurate_emu = 0`, `aligned_pc = 0 ; Set to 1 on old emulators` — no Switch/console
   manter 0 (inferência pela regra "console", conferir com o teste 4.9.1).
4. Clicar **Compute**. Em **Result** aparecem os nomes `Box 1`, `Box 2`, … **Compute another** pede outra
   codificação equivalente (útil se algum nome esbarrar no filtro de palavrões do Switch — conferir).
5. Formato da saída (do código-fonte): caracteres separados por espaço; **`_` = ESPAÇO** (byte 0x00); **`–` = hífen
   do teclado** (byte 0xAE); `…` é **um** caractere. Posições não listadas = não digitar nada (o gerador usa por padrão
   `0xFFFFFFFF`, isto é, posições vazias, como "no-op" dentro de nomes — `doc/index.html`, parâmetro `filler0`).
6. Digitar cada nome: PC → cursor no título da caixa → A → **NAME**.
7. Disparar o ACE (swap com a 0x0351, 4.8) no local que o código pedir; conferir o resultado **antes** de salvar.

**Teclado da tela de nome de caixa** (decomp `src/naming_screen.c`, `sKeyboardChars`; inglês):

| Página | Linha 1 | Linha 2 | Linha 3 | Linha 4 |
|---|---|---|---|---|
| UPPER (abre nesta) | `A B C D E F ␣ .` | `G H I J K L ␣ ,` | `M N O P Q R S` | `T U V W X Y Z` |
| lower | `a b c d e f ␣ .` | `g h i j k l ␣ ,` | `m n o p q r s` | `t u v w x y z` |
| OTHERS | `0 1 2 3 4` | `5 6 7 8 9` | `! ? ♂ ♀ / -` | `… “ ” ‘ ’` |

(`␣` = tecla de espaço.) **SELECT** troca de página (UPPER → lower → OTHERS → UPPER), **B** apaga, **START** leva ao OK.
A tela abre **vazia** (não reaproveita o nome antigo), na página UPPER, máx. **8** caracteres. Um nome só de espaços
não é gravado. No Switch o filtro pode recusar o nome sem aviso (2.2).

**Caracteres que mais causam erro** [general-faq]: `l` (L minúsculo) × `I` (i maiúsculo) × `1`; `O` × `0`;
`…` (um caractere, página OTHERS) × `...` × `.`; `‘` × `’` e `“` × `”` (Sleipnir chama de "lefty"/"righty");
`_` (espaço no gerador) × `-`/`–` (hífen); `,` × `.`; espaço × posição vazia. Caracteres fora do teclado
(ex.: `ì`, `Œ`) **não se digitam** — só aparecem como resultado de um código.

#### 4.12.3 Códigos prontos — situação
**As saídas do gerador para `eng10` NÃO estão copiadas neste documento.** O gerador só calcula os nomes no navegador
e a execução local do motor foi bloqueada pela política deste ambiente, então não há como eu reproduzir a saída
"exatamente como o gerador gera" sem inventar. Para obtê-las: seguir 4.12.2 com os códigos abaixo e colar o
resultado aqui.

Gerar Pokémon (detalhes de uso em 4.10.2):

| Código no gerador | Arquivo (eng0 / eng1 / eng10) | Saída do código |
|---|---|---|
| Create any Gift Pokemon (Bootstrapped) | `pkmn/CreateAnyGiftPokemonBootstrapped.txt` (igual nos três) | entrega na party pelo NPC de Viridian, com seu OT |
| Start wild battle with any Pokemon | `pkmn/StartWildBattleWithAnyPokemon.txt` (igual) | batalha selvagem para capturar |
| Create Pokemon species from nothing | `pkmn/PokemonFromNothing.txt` (igual) | Caixa 10 slot 19, só a espécie |
| Fateful Mew Battle at Daycare (Bootstrapped) | `pkmn/FatefulMew_Universal.txt` (igual) | batalha com Mew obediente no Day Care da Route 5 |
| Start Fateful Mew Battle (Bootstrapped) | `FatefulMew_FR_ENG.txt` / `FatefulMew_FR_Rev1_ENG.txt` / `FatefulMew_FR_ENG_SWITCH.txt` | Mew no Indigo Plateau, exige Elite 4 (versão antiga) |

Flags de Pokédex (vistos/capturados):

| Código no gerador | Autor (do arquivo) | Efeito (comentários do código) | Saída |
|---|---|---|---|
| Complete Kanto Pokédex (Bootstrapped) | Adrichu00 (baseado no código do Sleipnir) | "registers all species from 1 to 150" — grava as flags *owned* e *seen* | Bootstrapped |
| Complete National Pokédex (Bootstrapped) | Adrichu00 (baseado no Sleipnir) | "registers all species except Jirachi and Deoxys" | Bootstrapped |
| Complete the full Pokédex (Bootstrapped) | ComplexRobot | "Completes the entire Pokédex, including the National Dex"; tem `aligned_pc = 0 ; Set to 1 on old emulators` | Bootstrapped |
| Get National Dex via NPC | Adrichu00 / Papa Jefe / Theocatic / final | ativa a Pokédex Nacional e a troca com RS; rodar no Centro Pokémon de Viridian e falar com o senhor abaixo do PC. **Aviso do código:** ativa o 2º round da Elite 4 | `ROM_BX_lr_Box10_Grab` |

Todos os quatro usam o **mesmo arquivo** para eng0, eng1 e eng10.

Nomes prontos que existem fora do gerador:
- "Generate any shiny Pokémon in your box" (Sleipnir) — já reproduzido em 4.10.1, com Vulpix e Mew derivados.
- "Get National Pokédex and enable RSE trading" (Sleipnir, `pastebin.com/VAgKwjwJ`, lista de grab ACE) — liga a
  Pokédex Nacional, **não** marca vistos/capturados.
- "Box names code to complete your Pokédex (FireRed LeafGreen)" (Sleipnir, `pastebin.com/CxZwhy8Y`) tem nomes
  prontos, mas está ligado à lista de **move ACE** (`mcd1pDn9`) e termina com a saída "Store bx r0 opcode" típica
  daquela lista; a versão para grab ACE é justamente o "Complete National Dex" do gerador ("Based on Sleipnir's code").
  **Não usar com a 0x0351** (inferência pela origem e pela saída — conferir).

#### 4.12.4 Diferenças entre eng0, eng1 e eng10
- **O motor não diferencia versões do inglês:** `Utils/settings.ml` usa só as 3 primeiras letras
  (`String.sub language 0 3` → `"eng"`). Toda diferença vem do **arquivo de modelo** que a lista
  (`files_frlg/list.json`) associa a cada versão. Se o arquivo é o mesmo, **a saída é a mesma** para eng0/eng1/eng10.
  Para obter a variante 1.1, basta trocar o seletor para "English 1.1" (`lang=eng1`) e clicar Compute; idem 1.0 (`eng0`).
- **1.0 × 1.1 (FireRed):** só dois códigos mudam — "Run script via NPC" e "Start Fateful Mew Battle (Bootstrapped)",
  porque usam endereço de script na ROM. Ex. Fateful Mew: 1.0 `script = 0x0816B094`, 1.1 `script = 0x0816B10C`
  (`offset = 0x5D9C` nos dois), Switch `script = 0x0816E78B`, `offset = 0x5D8A`.
- **Arquivo próprio para Switch (eng10):** Change PRNG seed and teleport (Bootstrapped); Read Pokemon PID / SID /
  TID and SID / IVEA / EVs / contest stats / Pokérus / ribbons and obedience; Run script via NPC; Change Pokemon Level;
  Create Tradeback NPC; Start Fateful Mew Battle (Bootstrapped); Teleport anywhere (Bootstrapped); Make any Pokémon Shiny.
- **Sem versão para Switch:** Change Trainer Name (e Bootstrapped), Perform PID or TID corruption, Change Pokémon OT Name,
  Replace Pokemon OT w/ Your Trainer Name, Run script via GlobalScriptContext, Change Pokémon PID or TID (Bootstrapped)
  e todos os "(move ACE)".
- **Ajustes do FAQ do Switch (4.9.3):** como o motor não sabe que é Switch, nada é ajustado automaticamente por ele.
  Duas observações (inferências, conferir): a `GrabACEExit` do gerador é `mov r15, #0x354` **sem S**, o mesmo efeito
  do ajuste `.o` do FAQ; e o preenchimento padrão com posições vazias (`filler0 = 0xFFFFFFFF`) tende a já respeitar a
  regra das caixas 4/8/12. Mesmo assim, conferir os nomes gerados contra 4.9.3 antes de usar.
- **Qual escolher:** cartucho GBA → identificar a revisão (2.1: "PRESENTS" na abertura ou categoria do Pidgey na
  Pokédex) e usar `eng0` ou `eng1`; Switch → sempre `eng10` (só existe um build por idioma; não há 1.0/1.1 no Switch).
  **Não existe versão de FireRed no app Nintendo Switch Online (GBA)** (2.2).

---

## 5. Riscos e segurança

**O que pode estragar o save**
- A QMM sobrescreve o que estiver na **Caixa 3 slot 1** (corrompe/destrói o Pokémon).
- Palavras erradas na QMM → bad egg em vez de HOCK/0x0351 (recuperável: apagar com seleção em grupo e refazer).
- **EVs errados no HOCK** → bad egg na conversão; refazer exige um HOCK novo (há Retro Mail sobrando). Na rota MIMIEN o
  erro de EV **não tem volta** (EVs não se zeram no FRLG) — mais um motivo para usar a rota HOCK.
- A 0x0351 corrompe os **slots 7–9 da Caixa 13** (bad eggs). Não guarde nada de valor lá.
- HOCK/0x0351 e Pokémon criados do nada **somem** em seleção em grupo.
- Código com erro de digitação ou slot ocupado onde devia estar vazio → travamento, softlock ou escrita em lugar
  errado da memória. Se salvar depois disso, a corrupção fica permanente.
- Códigos que escrevem em slots fixos (Caixa 9/27, 9/30, 10/19) apagam o que estiver lá.
- Disparar o Mail glitch várias vezes desloca a QMM (aparece com menos Pokémon) e impede o desfazer pela troca do ZYNX.
- **Switch:** filtro de palavrões pode recusar um nome de caixa **sem avisar** (o nome antigo continua) → o código roda
  com nome errado. Conferir cada nome antes de disparar.
- **Switch:** códigos de ROM/RAM para GBA (ou de outra versão do Switch, caso haja update) quebram ou corrompem.
- **Pokémon HOME:** envio é **só de ida** e não achei nada sobre checagem de legalidade dos Pokémon do FRLG Switch nem
  sobre sanções **(conferir antes de enviar qualquer coisa gerada por ACE)**. Nunca enviar espécies glitch/bad eggs.

**Antes de tentar**
- No Switch **não há** save state, rewind, ponto de restauração nem backup em nuvem (Save Data Cloud não suportado).
  O único "desfazer" é: **salvar num ponto seguro → testar → se der errado, soft reset (A+B+SELECT+START ou A+B+X+Y)
  ou fechar o software sem salvar**. Modo repouso não substitui o save.
- Salvar imediatamente antes da batalha dupla, antes do HOCK, antes da conversão em 0x0351 e antes de cada código.
- Só salvar depois de conferir o resultado esperado (tabela 4.11).
- Esvaziar as caixas exigidas e manter Pokémon valiosos em caixas baixas, longe da Caixa 13/14.
- Rodar o teste do Bulbasaur (4.9.1) antes de qualquer código "de verdade".

**Como desfazer / recuperar**
- Etapa que deu errado e não foi salva: soft reset.
- Bad eggs/glitch indesejados: seleção em grupo (mão laranja, segurar A, arrastar, soltar, A de novo) [general-faq]. Para
  bad eggs "teimosos": clonagem reversa na Battle Tower (pode não funcionar em cartucho falso) [general-faq].
- Desligar o Mail glitch (cartas voltam ao normal) [mail-glitch]:
  - por ACE, sem ninguém da party segurando carta:
    ```
    Box 1: 2 B U n _ F . o [2BUn F.o]
    Box 2: A A A A T ! q   [AAAAT!q] ← replace 4th 'A' with 'C' for inaccurate emulators
    Box 3: A A ♂ H Q m H 2 [AA♂HQmH2]
    Box 4: o , J Q m       [o,JQm]
    Box 5: B L Q m … O Q m [BLQm…OQm]
    Box 6: _ F o ♂ Q Q m r [ Fo♂QQmr]
    Box 7: v n             [vn]
    ```
    (usa uma saída nas caixas 6/7 que o FAQ do Switch não cobre — **conferir no Switch**);
  - pela troca in-game do **ZYNX** (Jynx que vem segurando carta): com todos menos um da party segurando carta, trocar
    o que não segura. Não funciona se o glitch foi disparado mais de uma vez;
  - por troca com outro jogo de Gen 3 (no Switch, troca local sem fio).

---

## 6. Fontes

**Primárias (confiáveis)**
- pokemon-ace-notes (Luong Truong "final/togebit" e colaboradores; repositório clonado, commit `ea6f692`, 2026-07-25) —
  principal referência atual de ACE em FRLG, com nota específica para o Switch:
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-introduction/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/mail-glitch/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-non-jpn-ace/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-non-jpn-pre-e4-route/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-non-jpn-post-e4-route/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-non-jpn-mimien-route/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-non-jpn-other-empty-slot-routes/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-box-14-exit/
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/frlg-faq/ (seção "Switch rerelease")
  - https://pomeg-letterbombers.github.io/pokemon-ace-notes/general-faq/
  - https://github.com/pomeg-letterbombers/pokemon-ace-notes (fonte markdown)
- Papa Jefé, guia escrito "FireRed and LeafGreen ACE — Mail Glitch & Arbitrary Code Execution Setup Guide" —
  https://docs.google.com/document/d/1khCyziorop1M2AI0JNLSaMqK3fV_SfIXeSYmevQ3DfE/ — pesquisador conhecido; bate com o
  pokemon-ace-notes; escrito antes do Switch (lista só GBA/DS/3DS/mGBA).
- Vídeos (títulos/autores confirmados via oEmbed, conteúdo não assistido): Papa Jefé
  https://www.youtube.com/watch?v=3jkcq8e9NO4 , https://www.youtube.com/watch?v=v_JfJ0WS07U ,
  https://www.youtube.com/watch?v=8d2kd2_iVps ; pokemerrp https://www.youtube.com/watch?v=yVhK4pLC9ac ;
  Sleipnir17 https://www.youtube.com/watch?v=kwOIOzczs8w ; MankeyMite https://www.youtube.com/watch?v=P0EswIGfQpQ .
- Sleipnir17, Pastebin — autor de referência de códigos Gen 3; anterior ao Switch:
  - https://pastebin.com/VAgKwjwJ (códigos grab ACE FRLG, inclui "Generate any shiny Pokémon")
  - https://pastebin.com/UFspsi9N (setup antigo via move ACE com Emerald)
  - https://pastebin.com/mcd1pDn9 (códigos move ACE)
- E-Sh4rk CodeGenerator — https://e-sh4rk.github.io/CodeGenerator/index_frlg.html (página; ex.:
  `?lang=eng10&game=fr`), documentação https://e-sh4rk.github.io/CodeGenerator/doc/index.html , código-fonte
  https://github.com/E-Sh4rk/CodeGenerator (lido: `Utils/settings.ml`, `Charset/charset.ml`, `Charset/name.ml`,
  `html/scripts.js`), modelos dos códigos FRLG em https://e-sh4rk.github.io/EmeraldACE_web/files_frlg/list.json
  (ex.: `pkmn/FatefulMew_Universal.txt`, `pkmn/CreateAnyGiftPokemonBootstrapped.txt`,
  `misc/CompleteNationalDex.txt`) — ferramenta padrão da comunidade, mantida (repo atualizado em 2026-09);
  primária para os códigos, mas a saída só existe no navegador.
- Sleipnir17, "Short exit code guide" (PDF linkado pelo gerador) —
  https://e-sh4rk.github.io/EmeraldACE_web/doc/FRLG_Short_Exit_Codes_Guide.pdf — voltado ao setup antigo (move ACE).
- Sleipnir17, https://pastebin.com/CxZwhy8Y (completar Pokédex; lista de move ACE, ver 4.12.3).
- Glitch City Wiki — https://glitchcity.wiki/wiki/Mail_removal_glitch , https://glitchcity.wiki/wiki/PC_swap_arbitrary_code_execution ,
  https://glitchcity.wiki/wiki/List_of_revision_differences_in_the_core_Pok%C3%A9mon_games — wiki da comunidade de glitches; confiável.
- Decompilação pret/pokefirered (cópia local `dados/pokefirered`, commit `037335f4`) — verdade de base para dados do
  jogo, revisões 1.0/1.1/Switch, filtro de nomes, obediência, layout da carta, grupos de palavras.

**Oficiais / imprensa (sobre o lançamento no Switch)**
- https://www.nintendo.com/au/news-and-articles/pokemon-firered-version-and-pokemon-leafgreen-version-are-coming-to-nintendo/ — oficial.
- https://www.nintendo.com/au/games/nintendo-switch/pokemon-leafgreen-version/ — oficial ("Save Data Cloud: Not supported").
- https://en-americas-support.nintendo.com/app/answers/detail/a_id/71365/ — FAQ oficial (HOME 4.1.0, troca local).
- https://www.pokemon.com/us/pokemon-news/the-pokemon-firered-version-and-pokemon-leafgreen-version-games-are-releasing-on-nintendo-switch — oficial.
- https://www.serebii.net/fireredleafgreen/nintendoswitch.shtml — Serebii, confiável (tickets, correção dos cães).
- https://en.wikipedia.org/wiki/Pok%C3%A9mon_FireRed_and_LeafGreen — secundária.
- https://gamerant.com/pokemon-firered-leafgreen-reset/ — imprensa (combinações de soft reset).
- https://www.siliconera.com/pokemon-home-works-with-pokemon-firered-and-leafgreen-switch-now/ e
  https://mynintendonews.com/2026/10/07/pokemon-home-now-compatible-with-fire-red-and-leaf-green-patch-notes/ — imprensa (HOME).
- https://www.threads.com/@serebii_joe/post/DU-zFcbCAxd/ — opinião de editor do Serebii sobre a ausência de save states.

**Baixa confiabilidade (só para ver o que afirmam)**
- https://prodigygamers.com/2026/03/08/pokemon-firered-leafgreen-how-to-do-ace-glitch/ e
  https://prodigygamers.com/2026/03/10/pokemon-firered-leafgreen-spawn-or-get-any-pokemon/ — content farm; copia
  Papa Jefé/CodeGenerator; afirma "Save and exit the PC" antes de falar com o NPC, o que **só aparece lá** (não
  recomendado: salve só depois de verificar).
- https://deltiasgaming.com/pokemon-firered-and-leafgreen-duplicate-item-glitch-explained/ , https://itemlevel.net/… ,
  https://overcentral.com/… , https://gamerant.com/pokemon-fire-red-leaf-green-mail-duplication-glitch-how-to-do/ —
  repetem o Mail glitch para duplicar itens; consistentes com as primárias, nada novo.
- TikTok @paperking64 — descreve a rota pós-Elite 4 (MAGIKARP do grupo POKéMON, Lea & Jed); consistente, não usado como base.

**Não lidas**
- Bulbapedia (bloqueio Cloudflare), incl. a página de rascunho `User:C.Ezra.M/Mail_corruption`.
- TCRF (retornou página anti-bot sem conteúdo útil).

---

## 7. Pendências

0. **Relatos de ACE no Switch:** o dono da partida informou que o YouTuber Thalera fez o ACE na versão do Switch
   (vídeo não localizado na busca: conferir o vídeo para ver o setup, os códigos usados e os ajustes do emulador).
   Segundo o dono, num dos vídeos ele usou o **Complete National Pokédex (Bootstrapped)** do CodeGenerator: indício de
   que o Box 14 exit (4.9.2) e os códigos bootstrapped funcionam no Switch (eng10).
   Um guia de 2026 também afirma que o Mail glitch continua na versão do Switch
   (https://prodigygamers.com/2026/03/08/pokemon-firered-leafgreen-how-to-do-ace-glitch/).
1. **Saídas do CodeGenerator (eng10/eng1/eng0) não estão neste documento** — nem para gerar Pokémon (Gift, Wild
   battle, From nothing, Fateful Mew at Daycare) nem para as flags de Pokédex. O CodeGenerator só gera no navegador;
   tentei rodar o motor dele localmente e a execução foi bloqueada pela política do ambiente. Gerar no site (4.12.2)
   e colar aqui. Se quiser que eu gere localmente, é preciso liberar a execução do motor JS do gerador.
1b. A premissa "`eng10` = English 1.0 / `eng11` = Rev 1" não confere com a página: `eng0` = 1.0, `eng1` = 1.1,
   `eng10` = Switch, e não há `eng11` (2.1, 4.12).
2. **Switch = variante "console" ou "emulador impreciso"?** (`/` vs `B` no teste; `♀` vs `,` no código do Sleipnir).
   Inferido "console"; confirmar com o teste 4.9.1.
3. **Ajustes de Switch no código do Sleipnir** (Caixa 4 sem espaços finais, Caixa 8 = `E` + 4 espaços, Caixa 11 = `.o`)
   foram derivados das regras gerais do FAQ, não testados por ninguém que eu tenha encontrado.
4. **O jogo do Switch foi atualizado junto com o HOME (07/10/2026)?** Se sim, códigos "English Switch" com endereços
   fixos podem ter quebrado; os relativos ao PC provavelmente não (inferência).
5. Quais nomes de caixa esbarram no filtro de palavrões do Switch — não há lista; só testando.
6. Checagem de legalidade do HOME para Pokémon gerados via ACE no FRLG do Switch — nada encontrado.
7. O código de desfazer o Mail glitch usa uma saída (caixas 6/7) não coberta pelo FAQ do Switch.
8. Nenhuma fonte primária descreve o Mail glitch rodando no Switch passo a passo; o FAQ e o CodeGenerator tratam o
   grab ACE no Switch como funcional (com ajustes) e a mecânica é lógica do jogo, mas **não vi confirmação explícita
   de alguém que fez HOCK → 0x0351 no Switch**.
9. Acesso exato no mapa: casa da troca do Mr. Mime na Route 2 (Cut/Diglett's Cave) e se Lea & Jed exigem Cut — conferir no jogo.
10. Texto exato do menu de opções do Switch que mostra a versão do software.
