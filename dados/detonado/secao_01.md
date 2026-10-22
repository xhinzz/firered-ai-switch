# Seção 1 — Introdução e Pallet Town (escolha do inicial)
Marcos do roteiro cobertos: inicial
Mapas: MAP_PALLET_TOWN_PLAYERS_HOUSE_2F, MAP_PALLET_TOWN_PLAYERS_HOUSE_1F, MAP_PALLET_TOWN, MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB, MAP_PALLET_TOWN_RIVALS_HOUSE

## Passo a passo
1. Tela título: A ou START. NEW GAME: o jogo mostra os controles e uma apresentação; depois o Prof. OAK pergunta
   BOY/GIRL e o nome do jogador (até 7 letras; SELECT troca a página de letras, B apaga, START/OK confirma).
   Em seguida o nome do rival: escolher da lista (no FireRed: GREEN, GARY, KAZ, TORU) ou digitar. Daqui em diante
   "RIVAL" = esse nome.
2. Começa no quarto (MAP_PALLET_TOWN_PLAYERS_HOUSE_2F). O PC fica em (1,1): fique em (1,2) olhando para cima, A,
   WITHDRAW ITEM e retire a POTION que já está guardada (é o único item da casa). A escada fica em (10,2).
   Dica de configuração: START > OPTION > TEXT SPEED FAST deixa os diálogos mais rápidos.
3. Térreo (MAP_PALLET_TOWN_PLAYERS_HOUSE_1F): MOM em (8,4) só avisa que o OAK te procura. Saída pelo tapete
   (4,8)/(5,8), andando para baixo. A TV em (6,1) é só texto.
4. Pallet Town (MAP_PALLET_TOWN): porta de casa (6,7), casa do rival (15,7), laboratório do OAK (16,13).
   O OAK ainda não está no laboratório. Ande para a saída norte: pisar em (12,1) ou (13,1) dispara a cena — o OAK
   te para ("não vá para a grama sem Pokémon") e te leva andando até o laboratório. Não precisa fazer nada.
5. Laboratório (MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB): OAK fica em (6,3) e o RIVAL em (5,4). Três POKé BALLs na mesa:
   (8,4) BULBASAUR, (9,4) SQUIRTLE, (10,4) CHARMANDER. Fique em (10,5) olhando para cima, A, e responda YES para
   CHARMANDER. Apelido: NO (ou dar um nome). O RIVAL pega o SQUIRTLE (9,4).
   - Antes de escolher, pisar na linha de saída (5,8)/(6,8)/(7,8) faz o OAK te chamar de volta (um passo para cima).
6. Luta obrigatória: depois de escolher, ao pisar em (5,8), (6,8) ou (7,8) (a única passagem para a porta, que fica em
   (5..7,12)) o RIVAL te desafia — TRAINER_RIVAL_OAKS_LAB_SQUIRTLE. Perder NÃO dá game over: o time é curado e a
   história segue igual. Vencendo: $80 e EXP (CHARMANDER deve chegar ao Nv6).
7. Depois da luta MOM (8,4) cura o time sempre que você falar com ela (Centro Pokémon grátis em Pallet).
8. Casa do rival (MAP_PALLET_TOWN_RIVALS_HOUSE): DAISY está sentada à mesa em (5,4). Agora só conversa; o TOWN MAP
   ela dá depois que você tiver a POKéDEX (Seção 2).
9. Siga para o norte, para a Rota 1 (MAP_ROUTE1) e Viridian City (Seção 2). O OAK no laboratório, se você falar com
   ele agora, só diz que dá para chegar à próxima cidade.

## Lutas obrigatórias
### RIVAL — TRAINER_RIVAL_OAKS_LAB_SQUIRTLE
- Onde: MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB, gatilho ao pisar em (5,8), (6,8) ou (7,8) depois de escolher o inicial.
- Time: SQUIRTLE Nv5 [TACKLE, TAIL WHIP]; sem itens.
- Tipos que funcionam: só há golpes Normal no CHARMANDER Nv5 (SCRATCH, GROWL). Use SCRATCH sempre; GROWL é perda
  de turno. Fogo não ajuda contra Água (e o CHARMANDER ainda não tem EMBER).
- Nível recomendado do time: CHARMANDER Nv5 (é o único possível). Se o HP ficar baixo, use a POTION do PC (ITEM).
  Derrota não tem custo: o jogo cura e continua.

## Treinadores opcionais relevantes
- Nenhum nesta seção.

## Itens
### MAP_PALLET_TOWN_PLAYERS_HOUSE_2F
- (1,1) POTION — guardada no PC do quarto (retirar com WITHDRAW ITEM; fique em (1,2) olhando para cima)
### MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB
- POKéDEX e 5 POKé BALL — presente do OAK (6,3) só ao entregar o OAK'S PARCEL (Seção 2)
- 5 POKé BALL extras — o OAK dá uma única vez se você estiver SEM nenhuma POKé BALL, só com o inicial capturado
  na POKéDEX e já tiver passado pelo rival da Rota 22 (ou pelo de Cerulean)
### MAP_PALLET_TOWN_RIVALS_HOUSE
- TOWN MAP — key item, presente da DAISY (5,4), só depois da POKéDEX (Seção 2)

## NPCs importantes
- MAP_PALLET_TOWN_PLAYERS_HOUSE_1F (8,4): MOM — cura o time depois da luta no laboratório (sempre que falar).
- MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB (6,3): Prof. OAK — inicial agora; POKéDEX ao receber o OAK'S PARCEL; avalia a
  POKéDEX quando você fala com ele; mais tarde a NATIONAL DEX (pós-Liga).
- MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB (3,11), (2,10), (11,10): assistentes — só texto.
- MAP_PALLET_TOWN_RIVALS_HOUSE (5,4): DAISY — TOWN MAP depois da POKéDEX; depois do fim da Liga ela "penteia" um
  Pokémon (aumenta a amizade).
- MAP_PALLET_TOWN (3,10): moça da placa — mostra a dica do menu START; (13,17) homem — fala do PC. Só texto.

## Pokémon disponíveis (FireRed)
### MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB
- presente: CHARMANDER Nv5 (escolha deste save). BULBASAUR e SQUIRTLE não voltam a aparecer — só por troca.
### MAP_PALLET_TOWN (água ao sul, rumo à Rota 21 — exige SURF ou vara, muito mais tarde)
- surf: TENTACOOL 5-40 (100%)
- OLD ROD: MAGIKARP 5-10 (100%)
- GOOD ROD: HORSEA 5-15 (60%), MAGIKARP 5-15 (20%), KRABBY 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (40%), SHELLDER 15-25 (40%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
- Aviso: OLD ROD vem em Vermilion, GOOD ROD em Fuchsia, SUPER ROD na Rota 12; SURF exige HM03 + SOUL BADGE.

## Quebra-cabeças
Nenhum.

## Dicas para jogar bem
- Não há grama segura sem Pokémon: o caminho norte (12,1)/(13,1) sempre dispara a cena do OAK até você ter o inicial.
- A luta do laboratório não pode ser perdida de verdade; mesmo assim, vencer dá a EXP do Nv6.
- Nada aqui fica perdido para sempre: a POTION do PC pode ser retirada a qualquer hora, o TOWN MAP fica esperando.
- Para 100% da POKéDEX: BULBASAUR e SQUIRTLE (e evoluções) só por troca com outro jogo.
- Salve (START > SAVE) depois da luta; o ponto de retorno ao desmaiar ainda é a casa do jogador.
- A água ao sul de Pallet leva à Rota 21 e a Cinnabar — só com SURF (fim do jogo).
