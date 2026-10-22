# Seção 2 — Rota 1, Viridian City, OAK'S PARCEL, Rota 22 e Rota 2 (lado oeste)
Marcos do roteiro cobertos: encomenda; novo: town_map, novo: teachy_tv, novo: rival_22_cedo (opcional)
Mapas: MAP_ROUTE1, MAP_VIRIDIAN_CITY, MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F, MAP_VIRIDIAN_CITY_MART, MAP_VIRIDIAN_CITY_SCHOOL, MAP_VIRIDIAN_CITY_HOUSE, MAP_PALLET_TOWN, MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB, MAP_PALLET_TOWN_RIVALS_HOUSE, MAP_ROUTE22, MAP_ROUTE22_NORTH_ENTRANCE, MAP_ROUTE2, MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE, MAP_ROUTE2_HOUSE, MAP_ROUTE2_EAST_BUILDING, MAP_VIRIDIAN_CITY_GYM

## Passo a passo
1. Rota 1 (MAP_ROUTE1), entrando pela borda sul (vindo de Pallet). O funcionário da loja (6,28), perto da placa (9,31),
   anda para cima e para baixo: fale com ele para ganhar uma POTION (uma vez só). As bordas (ledges) só se pulam para
   o sul; para subir use os vãos. A grama tem PIDGEY e RATTATA, mas ainda não há POKé BALL — só EXP.
2. Viridian City (MAP_VIRIDIAN_CITY). Portas: Centro Pokémon (26,26), loja (36,19), escola (25,18), casa (25,11),
   ginásio (36,10).
   - Centro (MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F): enfermeira em (7,2); cure e salve. Ele vira o ponto de retorno.
   - Loja (MAP_VIRIDIAN_CITY_MART): ao entrar, o vendedor (2,3) chama você automaticamente e entrega o OAK'S PARCEL
     (key item). Até a entrega ele NÃO vende nada.
   - O caminho para o norte (Rota 2) está fechado: o velho deitado em (21,11) bloqueia e pisar em (22,11) te empurra
     de volta ("propriedade particular"). Só abre depois que você recebe a POKéDEX.
   - O ginásio (porta (36,10)) está trancado: pisar em (36,11) mostra a porta fechada. Abre sozinho ao entrar em
     Viridian já com as insígnias 2 a 7 (CASCADE até VOLCANO) — fim do jogo.
   - POTION no chão em (17,5), já acessível: entre no caminho estreito do oeste da cidade em (8,16), suba a coluna
     x=8 até (8,5) e ande para leste até (16,5). A árvore de CUT (18,5) só separa esse corredor do lado leste.
   - Escola (MAP_VIRIDIAN_CITY_SCHOOL) e casa (MAP_VIRIDIAN_CITY_HOUSE): só textos (quadro com os 5 estados).
3. Volte a Pallet (Rota 1 para o sul) e entre no laboratório (MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB). Fale com o OAK
   (6,3): ele recebe o pacote, o RIVAL entra, e você ganha a POKéDEX e 5 POKé BALL. Isso libera ao mesmo tempo:
   a loja de Viridian, o velho de Viridian, o TOWN MAP da DAISY e o rival à espera na Rota 22.
4. Casa do rival (MAP_PALLET_TOWN_RIVALS_HOUSE): DAISY à mesa (5,4) entrega o TOWN MAP (key item). Depois ela passa
   a andar pela sala.
5. Volte a Viridian. Na loja compre POKé BALL ($200) — umas 5 a 10 — e POTION ($300).
6. Velho da captura: agora ele está em pé em (21,8). Para ir ao norte é obrigatório passar por (20,8) ou (22,8)
   (únicos tiles livres da linha), o que dispara a cena: ele demonstra a captura de um WEEDLE Nv5 (luta automática,
   não precisa apertar nada) e dá a TEACHY TV (key item). Depois o caminho fica livre.
7. Opcional — Rota 22 (MAP_ROUTE22), saída oeste de Viridian:
   - A grama do lado leste (x34-39, y9-13) tem MANKEY (ótimo contra o BROCK: LOW KICK no Nv6). Dá para usá-la sem
     encontrar o rival.
   - Seguir para oeste passando por (33,4), (33,5) ou (33,6) chama o rival: TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE.
     Todo o lado oeste da rota (grama x15-21, lagoa, portaria) só é alcançado passando por esses tiles.
     Aqui perder = desmaio normal (perde dinheiro e volta ao último Centro). A luta não é exigida pela história e some
     para sempre depois da luta com o rival em Cerulean (Seção 5) — só vale EXP/dinheiro.
   - A portaria norte (porta (8,5)/(9,5) -> MAP_ROUTE22_NORTH_ENTRANCE) tem um policial (8,2) e o gatilho (7,2) que
     exige a BOULDER BADGE. A Rota 23 seguinte pede todas as insígnias e SURF — só no fim do jogo.
8. Rota 2, lado oeste (MAP_ROUTE2): saia de Viridian pelo norte (x19-23, y0). Entra-se no corredor oeste (x2-13).
   Grama em (6..12, 56..60). Ledges em y=55 e y=70 só para o sul. A portaria da floresta fica em (5,51)/(6,51)
   (MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE); atravesse a portaria até a porta norte (7,1) -> Floresta (Seção 3).
9. Fechado na Rota 2 até ter CUT (HM01 + CASCADE BADGE): as árvores (16,62) e (15,69) separam o lado leste (ETHER,
   PARLYZ HEAL, prédio do assistente do OAK) e a árvore (11,13), perto de Pewter, separa o bolsão com a casa da troca
   (MAP_ROUTE2_HOUSE, porta (17,22)) e a entrada norte da Diglett's Cave (17,11). A árvore (18,26) separa esse bolsão
   do prédio MAP_ROUTE2_EAST_BUILDING (portas (18,41)/(19,41) e (18,46)/(19,46)). Ou seja: mesmo vindo pela Diglett's
   Cave, o HM05 exige CUT.

## Lutas obrigatórias
Nenhuma nesta seção (a cena do velho em Viridian é automática). Luta opcional detalhada abaixo.
### RIVAL (opcional) — TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE
- Onde: MAP_ROUTE22, gatilhos (33,4), (33,5), (33,6); só existe depois da POKéDEX e até a luta de Cerulean.
- Time: PIDGEY Nv9 [TACKLE, SAND ATTACK]; SQUIRTLE Nv9 [TACKLE, TAIL WHIP]; sem itens. Prêmio $144.
- Tipos que funcionam: EMBER (CHARMANDER aprende no Nv7) no PIDGEY; contra o SQUIRTLE use SCRATCH (Fogo é
  pouco eficaz). MANKEY (LOW KICK/SCRATCH) também serve.
- Nível recomendado do time: CHARMANDER Nv10+ com EMBER e POTIONs na bolsa. Perder aqui custa dinheiro.

## Treinadores opcionais relevantes
- Nenhum treinador comum nesta seção (Rota 1, Rota 2 oeste e Rota 22 não têm treinadores além do rival).

## Itens
### MAP_ROUTE1
- (6,28) POTION — presente do funcionário da loja (uma vez)
### MAP_VIRIDIAN_CITY
- (17,5) POTION — visível (corredor oeste, ver passo 2)
- TEACHY TV — key item, presente do velho da captura (passo 6)
### MAP_VIRIDIAN_CITY_MART
- OAK'S PARCEL — key item, presente do vendedor ao entrar (entregar ao OAK)
### MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB
- POKéDEX + 5 POKé BALL — presente do OAK ao entregar o pacote
### MAP_PALLET_TOWN_RIVALS_HOUSE
- TOWN MAP — key item, presente da DAISY (5,4) depois da POKéDEX
### MAP_ROUTE2 (só com CUT)
- (17,54) ETHER — visível, lado leste
- (17,64) PARLYZ HEAL — visível, lado leste
### MAP_ROUTE2_EAST_BUILDING (só com CUT)
- HM05 (FLASH) — presente do assistente do OAK (4,6) se você tiver 10 ou mais espécies CAPTURADAS na POKéDEX
### MAP_VIRIDIAN_CITY_GYM (fim do jogo)
- (2,2) MACHO BRACE — escondido "sob os pés" no lugar onde o GIOVANNI fica; só aparece com o ITEMFINDER

## NPCs importantes
- MAP_ROUTE1 (6,28): funcionário da loja de Viridian — POTION grátis.
- MAP_VIRIDIAN_CITY_MART (2,3): vendedor — OAK'S PARCEL; depois da POKéDEX vende POKé BALL $200, POTION $300,
  ANTIDOTE $100, PARLYZ HEAL $200.
- MAP_VIRIDIAN_CITY (21,11) -> (21,8): velho — bloqueia o norte até a POKéDEX; depois demonstra captura e dá TEACHY TV.
- MAP_VIRIDIAN_CITY (8,26): tutor de DREAM EATER (ensina uma vez). Fica atrás da árvore de CUT (11,24); voltar com CUT.
- MAP_VIRIDIAN_CITY (36,10): ginásio — trancado até ter CASCADE, THUNDER, RAINBOW, SOUL, MARSH e VOLCANO BADGE.
- MAP_PALLET_TOWN_RIVALS_HOUSE (5,4): DAISY — TOWN MAP.
- MAP_ROUTE22_NORTH_ENTRANCE (8,2): policial — exige BOULDER BADGE para passar à Rota 23.
- MAP_ROUTE2_HOUSE (7,2): REYLEY — troca: pede ABRA, dá MR. MIME "MIMIEN" (só com CUT; ABRA aparece mais adiante).
  No FireRed o MR. MIME só se obtém por esta troca.
- MAP_ROUTE2_EAST_BUILDING (4,6): assistente do OAK — HM05 (FLASH) com 10 espécies capturadas (só com CUT).

## Pokémon disponíveis (FireRed)
### MAP_ROUTE1
- grama: PIDGEY 2-5 (50%), RATTATA 2-4 (50%)
### MAP_VIRIDIAN_CITY (lagoa; vara/SURF só mais tarde)
- surf: PSYDUCK 20-40 (100%)
- OLD ROD: MAGIKARP 5 (100%)
- GOOD ROD: POLIWAG 5-15 (60%), MAGIKARP 5-15 (20%), GOLDEEN 5-15 (20%)
- SUPER ROD: POLIWAG 15-25 (40%), POLIWHIRL 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)
### MAP_ROUTE22
- grama: RATTATA 2-5 (45%), MANKEY 2-5 (45%), SPEAROW 3-5 (10%)
- surf: PSYDUCK 20-40 (100%)
- OLD ROD: MAGIKARP 5 (100%)
- GOOD ROD: POLIWAG 5-15 (60%), MAGIKARP 5-15 (20%), GOLDEEN 5-15 (20%)
- SUPER ROD: POLIWAG 15-25 (40%), POLIWHIRL 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)
- (a lagoa da Rota 22 fica no lado oeste, depois do gatilho do rival)
### MAP_ROUTE2
- grama: RATTATA 2-5 (45%), PIDGEY 2-5 (45%), CATERPIE 4-5 (5%), WEEDLE 4-5 (5%)
### MAP_ROUTE2_HOUSE
- troca: ABRA -> MR. MIME (só com CUT)
- Aviso de varas: OLD ROD em Vermilion, GOOD ROD em Fuchsia, SUPER ROD na Rota 12; SURF exige HM03 + SOUL BADGE.

## Quebra-cabeças
Nenhum. Só bloqueios de história: velho de Viridian (até a POKéDEX), ginásio de Viridian (insígnias 2-7),
portaria da Rota 22 (BOULDER BADGE), árvores de CUT da Rota 2.

## Dicas para jogar bem
- Ordem eficiente: pacote na loja -> OAK -> DAISY -> loja (POKé BALLs) -> velho (TEACHY TV) -> grama leste da Rota 22
  (MANKEY) -> Rota 2.
- Capturas que valem a pena agora: MANKEY (Rota 22; LOW KICK é super eficaz e muito forte contra o ONIX do BROCK,
  KARATE CHOP no Nv11) e CATERPIE (Rota 2/Floresta; vira BUTTERFREE no Nv10 com CONFUSION). Capture também PIDGEY,
  RATTATA e SPEAROW: são espécies para a POKéDEX (a meta de 10 capturados libera o HM05 depois).
- CHARMANDER aprende EMBER no Nv7 e METAL CLAW no Nv13 (Aço, super eficaz contra o BROCK). Treinar até o Nv12-13
  aqui e na Floresta facilita muito a próxima seção.
- Pegue já a POTION (17,5) de Viridian (não precisa de CUT). Para 100%, voltar depois com CUT: ETHER e PARLYZ HEAL
  da Rota 2, tutor de DREAM EATER em Viridian, troca do MR. MIME, HM05 (FLASH). Com ITEMFINDER, o MACHO BRACE no
  ginásio de Viridian.
- O rival da Rota 22 é a única luta perdível desta seção (some depois de Cerulean); não traz item, só EXP e $144.
