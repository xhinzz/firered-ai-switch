# Seção 9 — Celadon City, Rocket Hideout, Pokémon Tower e a POKé FLUTE
Marcos do roteiro cobertos: celadon (chegada), cha, eevee, erika, esconderijo, torre; novo: coin_case, tms_bebidas, rival_torre, marowak, flauta, premios_cassino
Mapas: MAP_CELADON_CITY, MAP_CELADON_CITY_POKEMON_CENTER_1F, MAP_CELADON_CITY_CONDOMINIUMS_1F, MAP_CELADON_CITY_CONDOMINIUMS_2F, MAP_CELADON_CITY_CONDOMINIUMS_3F, MAP_CELADON_CITY_CONDOMINIUMS_ROOF, MAP_CELADON_CITY_CONDOMINIUMS_ROOF_ROOM, MAP_CELADON_CITY_DEPARTMENT_STORE_1F, MAP_CELADON_CITY_DEPARTMENT_STORE_2F, MAP_CELADON_CITY_DEPARTMENT_STORE_3F, MAP_CELADON_CITY_DEPARTMENT_STORE_4F, MAP_CELADON_CITY_DEPARTMENT_STORE_5F, MAP_CELADON_CITY_DEPARTMENT_STORE_ROOF, MAP_CELADON_CITY_DEPARTMENT_STORE_ELEVATOR, MAP_CELADON_CITY_RESTAURANT, MAP_CELADON_CITY_HOUSE1, MAP_CELADON_CITY_HOTEL, MAP_CELADON_CITY_GAME_CORNER, MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM, MAP_CELADON_CITY_GYM, MAP_ROCKET_HIDEOUT_B1F, MAP_ROCKET_HIDEOUT_B2F, MAP_ROCKET_HIDEOUT_B3F, MAP_ROCKET_HIDEOUT_B4F, MAP_ROCKET_HIDEOUT_ELEVATOR, MAP_ROUTE7_EAST_ENTRANCE, MAP_POKEMON_TOWER_1F, MAP_POKEMON_TOWER_2F, MAP_POKEMON_TOWER_3F, MAP_POKEMON_TOWER_4F, MAP_POKEMON_TOWER_5F, MAP_POKEMON_TOWER_6F, MAP_POKEMON_TOWER_7F, MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE

## Passo a passo
Convenções: escadas laterais (tiles *_STAIR_WARP) levam a outro andar quando o jogador está EM CIMA delas e aperta
a direção da escada (DIR nas escadas "RIGHT", ESQ nas "LEFT"); portas de elevador (MB_WARP_DOOR) são entradas
apertando CIMA a partir do tile de baixo. Itens no chão: ficar ao lado, virar para o item e apertar A.

1. Chegada pela Rota 7 (borda leste, linhas 12-15) em MAP_CELADON_CITY. Centro Pokémon: porta (48,11).
   Caminhos da cidade sem HM: a rua principal (linha 12-15), o sul (linhas 24-33) e o norte (faixa das linhas
   2-3, alcançada subindo por x 51 linhas 7-11 → oeste pela linha 7 até x 38 → subir x 38-39 até a linha 3).
   Duas árvores de CUT na cidade: (52,22) (só atalho) e (40,35) (a ÚNICA passagem para o Ginásio).
2. ETHER (5,3) no canto noroeste (faixa norte; pegar de (5,4) olhando para CIMA).
   PP UP escondido em (55,20): pelo sul, subir a coluna x 54-55 a partir da linha 30 até (55,21) e olhar para CIMA.
3. TEA (marco cha): Celadon Mansion pela porta da frente (30,11) → MAP_CELADON_CITY_CONDOMINIUMS_1F. A senhora
   (2,9): falar de (3,9) olhando para ESQ. Dá o TEA (key item) uma única vez. O TEA abre as 4 portarias de Saffron.
4. EEVEE (marco eevee): só pela porta dos FUNDOS da Mansion. A escada da frente não chega ao quarto do telhado.
   Rota: faixa norte da cidade até (30,3), descer para (30,4) (porta dos fundos, seta) → 1F chega em (2,1):
   BAIXO 1, DIR 2 até a escada (4,2) [DIR] → 2F (4,2): ESQ 2 até a escada (2,2) [ESQ] → 3F (2,2): DIR 2 até a
   escada (4,2) [DIR] → MAP_CELADON_CITY_CONDOMINIUMS_ROOF (4,2): BAIXO 2, DIR 1, BAIXO 9 até (5,13), ESQ 3 até
   (2,13) → CIMA na porta (2,12) → MAP_CELADON_CITY_CONDOMINIUMS_ROOF_ROOM. Poké Ball (7,3): EEVEE Nv25 (vai para o
   PC se o time estiver cheio). Deixar um espaço livre no time é o mais prático.
5. Department Store (portas (11,14) e (15,14)). Escadas: 1F (4,2) [ESQ] → 2F (9,2) [DIR] → 3F (3,2) [ESQ] →
   4F (9,2) [DIR] → 5F (3,2) [ESQ] → terraço; há também elevador (porta (6,1) de cada andar). Lojas por andar em
   "NPCs importantes". Terraço (MAP_CELADON_CITY_DEPARTMENT_STORE_ROOF): máquinas em (10,3), (11,3), (12,3) (ficar em
   (10..12,4) olhando para CIMA). Comprar FRESH WATER ($200), SODA POP ($300) e LEMONADE ($350) e dar UMA de cada
   à menina (5,4) (anda pela área): FRESH WATER → TM16 (LIGHT SCREEN); SODA POP → TM20 (SAFEGUARD);
   LEMONADE → TM33 (REFLECT). Cada TM só uma vez; ela pergunta qual bebida dar quando há mais de uma.
6. COIN CASE (novo coin_case): MAP_CELADON_CITY_RESTAURANT (porta (37,29)). Homem (1,2): falar de (2,2) olhando
   ESQ (ou de (0,2)). Sem COIN CASE não se compra ficha, não se joga, não se pegam fichas do chão nem se troca prêmio.
7. MAP_CELADON_CITY_GAME_CORNER (porta (34,21)): fichas grátis (ver Itens) e prêmios no Prize Room (porta
   (39,20)). Rocket TRAINER_TEAM_ROCKET_GRUNT_7 em (11,2) olhando para o pôster (11,1), visão 0: falar com ele de
   (11,3). Após a vitória ele sai andando. Ficar em (11,2), olhar para CIMA e apertar A no pôster: interruptor abre
   a escada em (15,2)-(17,2). Ir até (15,2) e apertar DIR → MAP_ROCKET_HIDEOUT_B1F (12,2).
8. Rocket Hideout (marco esconderijo) — solução completa em "Quebra-cabeças". Resumo:
   B1F norte (ESCAPE ROPE, PP UP escondido) → escada (17,2) → B2F labirinto de setas (MOON STONE, TM12, X SPEED,
   SUPER POTION) → escada (23,12) → B1F sudoeste (HYPER POTION, 2 Rockets) → volta à B2F (23,12) → escada (21,2)
   → B3F (TM21, NUGGET escondido, RARE CANDY, BLACKGLASSES) → escada (15,18) → B4F oeste (MAX ETHER, TM49,
   Rocket TRAINER_TEAM_ROCKET_GRUNT_18 que larga a LIFT KEY) → voltar ao elevador → B4F leste (CALCIUM, 2 Rockets
   da porta, GIOVANNI) → SILPH SCOPE. Depois da derrota de Giovanni os Rockets da cidade somem.
9. ERIKA (marco erika; exige CUT e CASCADE BADGE): árvore da cidade (40,35): da rua sul ir até (40,34), CUT,
   descer a (40,36), oeste pela linha 36 até x 11, subir até (11,31) e CIMA na porta (11,30). Dentro: 3 árvores de
   CUT; qualquer uma abre caminho. Mais curta: subir pela coluna x 6, cortar (6,8), continuar até (6,5) e falar com
   ERIKA (6,4). Recebe RAINBOWBADGE (STRENGTH fora de batalha; obediência até Nv50) e TM19 (GIGA DRAIN).
10. TEA em Saffron: de Celadon pegar a Rota 7 e entrar em MAP_ROUTE7_EAST_ENTRANCE; ao pisar em (6,4)/(6,5)/(6,6)
    o guarda (6,2) pega o TEA e libera TODAS as portarias de Saffron (Rotas 5, 6, 7 e 8). Atravessar Saffron até a
    portaria leste (Rota 8) é o caminho mais curto para Lavender. (Alternativa: Underground Path Rota 7 ↔ Rota 8.)
11. Pokémon Tower (marco torre), MAP_LAVENDER_TOWN → porta da torre. 1F sem selvagens. Escada 1F (18,9) [DIR].
    2F: rival em (16,5); ao pisar em (17,5) ou (16,6) a luta começa (inevitável): TRAINER_RIVAL_POKEMON_TOWER_SQUIRTLE.
    Escada (4,10) [ESQ] → 3F. 3F → escada (18,10) [DIR] → 4F → escada (4,10) [ESQ] → 5F → escada (18,10) [DIR] → 6F.
    Sem SILPH SCOPE os selvagens aparecem como "GHOST": não dá para atacar nem capturar, só fugir.
12. 5F: zona purificada (10..12, 8..10): entrar nela cura todo o time (sai e entra de novo para curar outra vez).
    CLEANSE TAG (11,9) fica no meio dela.
13. 6F: a escada para o 7F é (11,16) [ESQ]. Pisar em (11,15) ou (12,16) dispara o fantasma. Sem SILPH SCOPE a
    batalha não tem como ser vencida, o jogador foge e é empurrado 1 passo para cima. Com o SCOPE: MAROWAK Nv30
    (selvagem fixo). Precisa NOCAUTEAR: Poké Balls são desviadas; fugir faz o evento repetir.
14. 7F: três Rockets inevitáveis no corredor (cada um cobre a largura toda): TRAINER_TEAM_ROCKET_GRUNT_19 (9,10),
    TRAINER_TEAM_ROCKET_GRUNT_20 (13,8), TRAINER_TEAM_ROCKET_GRUNT_21 (9,6). Mr. Fuji (11,4): falar de (11,5).
    Ele leva o jogador direto para MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE (chega na porta (4,7)).
15. POKé FLUTE (novo flauta): na casa, falar de novo com o Mr. Fuji (3,3) (de (3,4) olhando CIMA): POKé FLUTE (key
    item). Libera acordar os SNORLAX (Rota 12 ao sul de Lavender e Rota 16 a oeste de Celadon). Também libera a
    porta da Silph Co. (o Rocket da porta de Saffron dorme depois do resgate do Fuji).

## Lutas obrigatórias
### Rocket do Game Corner — TRAINER_TEAM_ROCKET_GRUNT_7
- Onde: MAP_CELADON_CITY_GAME_CORNER (11,2), visão 0 (falar com ele de (11,3)). Prêmio $640.
- Time: RATICATE Nv20; ZUBAT Nv20
- Tipos que funcionam: Lutador/Pedra/Elétrico/Psíquico. Nível recomendado: 22+.
### Rocket da LIFT KEY — TRAINER_TEAM_ROCKET_GRUNT_18
- Onde: MAP_ROCKET_HIDEOUT_B4F (4,2), olha para baixo, visão 1 (luta ao pisar em (4,3)). Prêmio $672.
- Time: KOFFING Nv21; ZUBAT Nv21. Depois da vitória a LIFT KEY aparece no chão em (3,2).
- Tipos: Psíquico (KOFFING tem Levitate), Elétrico/Pedra no ZUBAT.
### Guardas da porta de Giovanni — TRAINER_TEAM_ROCKET_GRUNT_16 e TRAINER_TEAM_ROCKET_GRUNT_17
- Onde: MAP_ROCKET_HIDEOUT_B4F (16,14) e (19,14), visão 0 (falar com cada um). A barreira (17..18,12..13) só
  some quando os DOIS estiverem derrotados. Prêmio $736 cada.
- Times: GRUNT_16 SANDSHREW Nv23; EKANS Nv23; SANDSLASH Nv23. GRUNT_17 EKANS Nv23; SANDSHREW Nv23; ARBOK Nv23.
- Tipos: Água/Planta/Gelo nos SANDSHREW/SANDSLASH; Psíquico/Terra nos EKANS/ARBOK.
### GIOVANNI — TRAINER_BOSS_GIOVANNI
- Onde: MAP_ROCKET_HIDEOUT_B4F (19,4), falar de (19,5). Prêmio $2900.
- Time: ONIX Nv25 [ROCK THROW, BIND, RAGE, HARDEN]; RHYHORN Nv24 [STOMP, FURY ATTACK, SCARY FACE, TAIL WHIP];
  KANGASKHAN Nv29 [FAKE OUT, MEGA PUNCH, BITE, TAIL WHIP] (golpes padrão por nível).
- Tipos que funcionam: Água/Planta (4x em ONIX e RHYHORN), Lutador/Gelo; KANGASKHAN só sente Lutador
  (TM31 BRICK BREAK, 2F da loja). Fogo/Elétrico são ruins contra ONIX/RHYHORN. ONIX com RAGE: acabar rápido.
- Nível recomendado: 29-31.
### ERIKA — TRAINER_LEADER_ERIKA
- Onde: MAP_CELADON_CITY_GYM (6,4), falar de (6,5). Prêmio $2900; RAINBOWBADGE + TM19 (GIGA DRAIN).
- Time: VICTREEBEL Nv29 [STUN SPORE, ACID, POISONPOWDER, GIGA DRAIN]; TANGELA Nv24 [POISONPOWDER, CONSTRICT,
  INGRAIN, GIGA DRAIN]; VILEPLUME Nv29 [SLEEP POWDER, ACID, STUN SPORE, GIGA DRAIN]; usa HYPER POTION e FULL HEAL.
- Tipos que funcionam: Fogo (CHARMELEON/CHARIZARD é ideal), Voador, Gelo, Psíquico (VICTREEBEL/VILEPLUME são
  Planta/Veneno). Evitar Água/Terra/Pedra. Levar AWAKENING, PARLYZ HEAL, ANTIDOTE.
- Nível recomendado: 30-32.
### Rival na torre — TRAINER_RIVAL_POKEMON_TOWER_SQUIRTLE
- Onde: MAP_POKEMON_TOWER_2F, gatilhos (17,5) e (16,6) (rival em (16,5)). Prêmio $900 (conferir).
- Time: PIDGEOTTO Nv25 [GUST, SAND-ATTACK, QUICK ATTACK, WHIRLWIND]; GROWLITHE Nv23 [ROAR, EMBER, LEER, ODOR
  SLEUTH]; EXEGGCUTE Nv22 [HYPNOSIS, REFLECT, LEECH SEED, CONFUSION]; KADABRA Nv20 [TELEPORT, KINESIS, CONFUSION,
  DISABLE]; WARTORTLE Nv25 [WITHDRAW, WATER GUN, BITE, RAPID SPIN].
- Tipos: Elétrico (PIDGEOTTO, WARTORTLE), Água/Terra/Pedra (GROWLITHE), Fogo/Inseto/Voador (EXEGGCUTE),
  Inseto/Fantasma/Sombrio (KADABRA). Nível recomendado: 27+.
### MAROWAK fantasma (encontro fixo, não é treinador)
- Onde: MAP_POKEMON_TOWER_6F, gatilhos (11,15) e (12,16). Exige SILPH SCOPE na mochila.
- MAROWAK Nv30 [HEADBUTT, LEER, FOCUS ENERGY, BONEMERANG]. Não captura (as bolas são desviadas). Vencer por KO.
- Tipos: Água/Planta/Gelo. Elétrico não pega. Nível recomendado: 30.
### Rockets do 7F — TRAINER_TEAM_ROCKET_GRUNT_19, _20, _21
- Onde: MAP_POKEMON_TOWER_7F (9,10), (13,8), (9,6), visão 4, inevitáveis. Prêmios $800 / $832 / $736.
- Times: GRUNT_19 ZUBAT Nv25; ZUBAT Nv25; GOLBAT Nv25. GRUNT_20 KOFFING Nv26; DROWZEE Nv26.
  GRUNT_21 ZUBAT Nv23; RATTATA Nv23; RATICATE Nv23; ZUBAT Nv23.
- Tipos: Elétrico/Psíquico/Pedra/Gelo nos morcegos; Psíquico no KOFFING; Inseto/Fantasma/Sombrio no DROWZEE.

## Treinadores opcionais relevantes
- MAP_CELADON_CITY_GYM: TRAINER_LASS_KAY (3,11) BELLSPROUT/WEEPINBELL 23, $368 — na linha do caminho;
  TRAINER_COOLTRAINER_MARY (8,7) 5 Pokémon Nv22, usa SUPER POTION, $792 — vê (7,7)-(6,7), no caminho da árvore
  (6,8); TRAINER_BEAUTY_BRIDGET (9,10) 4 Pokémon Nv21 $1512; TRAINER_PICNICKER_TINA (10,7) BULBASAUR/IVYSAUR 24
  $480; TRAINER_BEAUTY_TAMIA (2,6) 2 BELLSPROUT 24 $1728; TRAINER_BEAUTY_LORI (5,4) EXEGGCUTE 24 $1728;
  TRAINER_LASS_LISA (7,4) ODDISH/GLOOM 23 $368. As BEAUTYs pagam bem.
- MAP_ROCKET_HIDEOUT_B1F: TRAINER_TEAM_ROCKET_GRUNT_9 (4,9) 2 RATICATE 21 (vê a linha 9 a leste; no caminho da
  ESCAPE ROPE); TRAINER_TEAM_ROCKET_GRUNT_8 (24,12) DROWZEE/MACHOP 21 e TRAINER_TEAM_ROCKET_GRUNT_12 (21,27)
  GRIMER/KOFFING 22 — os dois são inevitáveis no caminho a pé B1F norte → elevador (24,25);
  TRAINER_TEAM_ROCKET_GRUNT_10 (10,22) GRIMER/KOFFING x2 Nv20 e TRAINER_TEAM_ROCKET_GRUNT_11 (6,32) 4 ratos Nv19
  (área sudoeste, via B2F (23,12)).
- MAP_ROCKET_HIDEOUT_B2F: TRAINER_TEAM_ROCKET_GRUNT_13 (20,6) olha em volta, visão 2, 5 Pokémon Nv17 — na entrada
  do labirinto.
- MAP_ROCKET_HIDEOUT_B3F: TRAINER_TEAM_ROCKET_GRUNT_15 (19,9) olha para cima, visão 4 (2 MACHOP 21) — no caminho
  do TM21; TRAINER_TEAM_ROCKET_GRUNT_14 (2,20) visão 2 (RATTATA/RATICATE/DROWZEE 20) — evitável.
- Torre: canalizadoras (só GASTLY/HAUNTER, $704-$768). Inevitáveis no caminho: 5F TRAINER_CHANNELER_RUTH (11,4)
  e TRAINER_CHANNELER_TAMMY (19,7) HAUNTER 23; 6F TRAINER_CHANNELER_JENNIFER (18,6) e TRAINER_CHANNELER_EMILIA
  (9,6). Demais: 3F PATRICIA (10,14) 22, CARLY (9,9) 24, HOPE (12,4) 23; 4F LAUREL (17,7) 2x23, JODY (15,13) 22,
  PAULA (4,12) 24; 5F KARINA (7,12) 24, JANAE (11,16) 22; 6F ANGELICA (13,10) 3x22 (ids TRAINER_CHANNELER_<NOME>).

## Itens
### MAP_CELADON_CITY
- (5,3) ETHER — visível
- (55,20) PP UP — escondido (de (55,21) olhando CIMA)
### MAP_CELADON_CITY_CONDOMINIUMS_1F
- TEA — key item, presente da senhora (2,9)
### MAP_CELADON_CITY_CONDOMINIUMS_ROOF_ROOM
- (7,3) Poké Ball do EEVEE Nv25 — presente
### MAP_CELADON_CITY_DEPARTMENT_STORE_ROOF
- TM16 (LIGHT SCREEN), TM20 (SAFEGUARD), TM33 (REFLECT) — presente da menina (5,4) em troca das bebidas
### MAP_CELADON_CITY_RESTAURANT
- COIN CASE — key item, presente do homem (1,2)
### MAP_CELADON_CITY_GYM
- TM19 (GIGA DRAIN) — da ERIKA após a vitória
### MAP_CELADON_CITY_GAME_CORNER (precisa COIN CASE; total 260 fichas no chão + 50 de NPCs)
- Fichas escondidas: (2,4) x10; (3,8) x10; (2,11) x20; (6,12) x10; (9,9) x10; (8,5) x20; (10,4) x10;
  (13,3) x10; (15,5) x10; (17,5) x40; (15,13) x100; (12,12) x10
- NPCs: FISHER (4,7) 10 fichas; SCIENTIST (13,7) 20 fichas; GENTLEMAN (16,10) 20 fichas (uma vez cada)
### MAP_ROCKET_HIDEOUT_B1F
- (5,16) ESCAPE ROPE — visível (pegar de (6,16) olhando ESQ)
- (1,22) HYPER POTION — visível (área sudoeste; pegar de (2,22))
- (16,17) PP UP — escondido no vaso (de (16,18) olhando CIMA)
### MAP_ROCKET_HIDEOUT_B2F
- (2,5) MOON STONE; (5,7) TM12 (TAUNT); (15,3) X SPEED; (0,14) SUPER POTION — visíveis (rota no labirinto abaixo)
### MAP_ROCKET_HIDEOUT_B3F
- (19,14) TM21 (FRUSTRATION); (12,12) RARE CANDY; (14,24) BLACKGLASSES — visíveis
- (1,3) NUGGET — escondido (de (2,3) olhando ESQ)
### MAP_ROCKET_HIDEOUT_B4F
- (4,14) MAX ETHER (de (4,15) olhando CIMA); (1,6) TM49 (SNATCH) (de (2,6) olhando ESQ) — visíveis
- (3,2) LIFT KEY — key item, aparece após derrotar o GRUNT_18
- (6,23) CALCIUM — visível (de (6,24) olhando CIMA)
- (16,6) NET BALL — escondido (de (17,6) olhando ESQ); (22,6) NEST BALL — escondido (de (21,6) olhando DIR)
- (20,5) SILPH SCOPE — key item, aparece após vencer GIOVANNI
### MAP_POKEMON_TOWER_3F
- (13,2) ESCAPE ROPE — visível
### MAP_POKEMON_TOWER_4F
- (12,11) ELIXIR; (8,11) AWAKENING; (11,16) GREAT BALL — visíveis
### MAP_POKEMON_TOWER_5F
- (11,9) CLEANSE TAG; (6,16) NUGGET (de (7,16) olhando ESQ) — visíveis
- (7,3) BIG MUSHROOM — escondido (de (8,3) olhando ESQ)
### MAP_POKEMON_TOWER_6F
- (5,15) RARE CANDY; (15,15) X ACCURACY — visíveis
### MAP_POKEMON_TOWER_7F
- (11,4) SOOTHE BELL — escondido "sob os pés" no lugar do Mr. Fuji: só sai com ITEMFINDER, parado em (11,4)
  depois que o Fuji foi embora (apertar A virado para ele não funciona). Voltar depois do ITEMFINDER.
### MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE
- POKé FLUTE — key item, presente do Mr. Fuji (3,3)

## NPCs importantes
- MAP_CELADON_CITY (26,19): tutor de SOFTBOILED (uma vez; só CLEFAIRY/CLEFABLE/CHANSEY e família, MEW).
- MAP_CELADON_CITY_DEPARTMENT_STORE_2F: balconista de TMs (1,6): TM05 ROAR $1000, TM15 HYPER BEAM $7500, TM28 DIG
  $2000, TM31 BRICK BREAK $3000, TM43 SECRET POWER $3000, TM45 ATTRACT $3000. Balconista (1,8): GREAT BALL $600,
  SUPER POTION $700, REVIVE $1500, ANTIDOTE $100, PARLYZ HEAL $200, AWAKENING $250, BURN HEAL $250, ICE HEAL $250,
  SUPER REPEL $500.
- MAP_CELADON_CITY_DEPARTMENT_STORE_3F (10,9): tutor de COUNTER (uma vez, atrás do balcão).
- MAP_CELADON_CITY_DEPARTMENT_STORE_4F (3,13): POKé DOLL $1000, RETRO MAIL $50, FIRE STONE, THUNDERSTONE,
  WATER STONE, LEAF STONE ($2100 cada).
- MAP_CELADON_CITY_DEPARTMENT_STORE_5F: (1,6) HP UP, PROTEIN, IRON, CALCIUM, ZINC, CARBOS ($9800 cada); (1,7)
  X ATTACK $500, X DEFEND $550, X SPEED $350, X SPECIAL $350, X ACCURACY $950, GUARD SPEC. $700, DIRE HIT $650.
- MAP_CELADON_CITY_DEPARTMENT_STORE_ROOF: máquinas (10..12,3) FRESH WATER $200, SODA POP $300, LEMONADE $350;
  menina sedenta (5,4) troca bebida por TM (ver Passo 5).
- MAP_CELADON_CITY_CONDOMINIUMS_1F (2,9): senhora do TEA. 3F (3,8): GAME DESIGNER — com os 150 de Kanto
  CAPTURADOS (MEW não conta) mostra o DIPLOMA.
- MAP_CELADON_CITY_GAME_CORNER: (6,2) vende fichas (falar de (6,4) olhando CIMA, por cima do balcão): 50 por $1000 ou 500 por $10000 (máximo 9999 fichas).
  Pôster (11,1) = interruptor do esconderijo.
- MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM (balcão: falar de (x,4) olhando CIMA): (2,2) itens: SMOKE BALL 800, MIRACLE SEED 1000,
  CHARCOAL 1000, MYSTIC WATER 1000, YELLOW FLUTE 1600 fichas. (4,2) Pokémon (FireRed): ABRA Nv9 180, CLEFAIRY Nv8
  500, DRATINI Nv18 2800, SCYTHER Nv25 5500, PORYGON Nv26 9999 fichas. (6,2) TMs: TM13 ICE BEAM 4000, TM23 IRON
  TAIL 3500, TM24 THUNDERBOLT 4000, TM30 SHADOW BALL 4500, TM35 FLAMETHROWER 4000 fichas.
- MAP_ROCKET_HIDEOUT_ELEVATOR: painel em (0,2) (ficar em (0,3) olhando CIMA). Andares: B1F, B2F, B4F. Sem LIFT KEY
  diz que precisa de chave. Para sair, voltar a (2,5) e apertar BAIXO.
- MAP_POKEMON_TOWER_5F (12,8): canalizadora da zona purificada (cura).
- MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE (3,3): Mr. Fuji (POKé FLUTE).

## Pokémon disponíveis (FireRed)
### MAP_CELADON_CITY (lago (24..29,21..23); pescar/surfar de (25..29,24) olhando CIMA)
- OLD ROD: MAGIKARP 5 (100%)
- GOOD ROD: MAGIKARP 5-15 (100%)
- SUPER ROD: MAGIKARP 15-35 (99%), GRIMER 30-40 (1%)
- surf (depois): PSYDUCK 5-40 (99%), KOFFING 30-40 (1%)
### MAP_CELADON_CITY_CONDOMINIUMS_ROOF_ROOM
- presente: EEVEE 25 (o único EEVEE do jogo)
### MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM
- prêmio: ABRA 9; CLEFAIRY 8; DRATINI 18; SCYTHER 25; PORYGON 26 (PORYGON só existe aqui)
### MAP_POKEMON_TOWER_3F (só com SILPH SCOPE dá para lutar/capturar)
- caverna: GASTLY 13-19 (90%), CUBONE 15-17 (9%), HAUNTER 20 (1%)
### MAP_POKEMON_TOWER_4F e MAP_POKEMON_TOWER_5F
- caverna: GASTLY 13-19 (86%), CUBONE 15-17 (9%), HAUNTER 20 (5%)
### MAP_POKEMON_TOWER_6F
- caverna: GASTLY 14-19 (85%), CUBONE 17-19 (9%), HAUNTER 21-23 (6%)
- encontro fixo: MAROWAK 30 (não capturável)
### MAP_POKEMON_TOWER_7F
- caverna: GASTLY 15-19 (75%), HAUNTER 23-25 (15%), CUBONE 17-19 (10%)
(Torre 1F/2F e Rocket Hideout: sem selvagens.)

## Quebra-cabeças
### Entrada secreta (MAP_CELADON_CITY_GAME_CORNER)
- O Rocket (11,2) fica no único tile de onde se lê o pôster (11,1). Vencê-lo (falar de (11,3)), pisar em (11,2),
  olhar CIMA, A. A escada aparece em (15,2)-(17,2) (fica aberta para sempre). Em (15,2) apertar DIR.
- Antes do interruptor o tile (15,2) é chão comum, apesar de haver warp no mapa.
### Setas giratórias (regra do jogo)
- Pisar numa seta empurra o jogador na direção dela; cada nova seta no trajeto muda a direção; para ao pisar num
  tile de parada ou ao bater em parede/objeto (itens no chão e Rockets também param o giro). Abaixo, "gira→(x,y)" é
  onde o jogador para. Os passos já contam com os itens anteriores recolhidos (os itens bloqueiam até serem pegos).
### MAP_ROCKET_HIDEOUT_B1F (chegada do Game Corner em (12,2))
- ESCAPE ROPE: BAIXO 2 (12,4); ESQ 2 (10,4); BAIXO 4 (10,8); ESQ 5 (5,8) [GRUNT_9 vê a linha 9]; BAIXO 2 (5,10);
  ESQ 1 (4,10); BAIXO 3 (4,13); DIR 2 (6,13); BAIXO 3 (6,16); olhar ESQ.
- PP UP: de (12,2) DIR 3 (15,2); BAIXO 16 (15,18); DIR 1 (16,18); olhar CIMA.
- Escada para B2F: (17,2), apertar DIR.
- Elevador do B1F (a pé, sem labirinto): de (17,2) BAIXO 2 (17,4); DIR 2 (19,4); BAIXO 4 (19,8); DIR 3 (22,8);
  BAIXO 5 (22,13) [GRUNT_8]; ESQ 3 (19,13); BAIXO 4 (19,17); DIR 2 (21,17); BAIXO 9 (21,26) [GRUNT_12];
  DIR 3 (24,26); CIMA na porta (24,25). Só funciona com a LIFT KEY.
### MAP_ROCKET_HIDEOUT_B2F (chegada do B1F norte em (28,2))
1. MOON STONE: ESQ 1 (27,2); BAIXO 4 (27,6); ESQ 6 (21,6) [GRUNT_13]; CIMA 1 (21,5); ESQ 4 (17,5); BAIXO 1 (17,6);
   ESQ gira→(1,4); DIR 1 (2,4); olhar BAIXO, pegar (2,5). Obrigatório pegar: a pedra tapa o caminho.
2. TM12: BAIXO 1 (2,5); DIR 1 (3,5); BAIXO gira→(7,6); ESQ 2 (5,6); olhar BAIXO, pegar (5,7).
3. X SPEED: DIR 4 (9,6); CIMA gira→(1,4); ESQ 1 (0,4); CIMA 2 (0,2); DIR 4 (4,2); BAIXO 2 (4,4); DIR 2 (6,4);
   CIMA 2 (6,2); DIR 8 (14,2); BAIXO 1 (14,3); olhar DIR, pegar (15,3).
4. SUPER POTION: CIMA 1 (14,2); ESQ 2 (12,2); BAIXO 2 (12,4); ESQ gira→(1,4); DIR 1 (2,4); BAIXO 1 (2,5); DIR 1
   (3,5); BAIXO gira→(7,6); DIR 2 (9,6); BAIXO 3 (9,9); DIR gira→(14,13); ESQ 1 (13,13); ESQ gira→(10,15); DIR 3
   (13,15); BAIXO 3 (13,18); ESQ gira→(1,14); olhar ESQ, pegar (0,14).
5. Saída sudeste (escada (23,12) para o B1F sudoeste): ESQ 1 (0,14); CIMA 2 (0,12); DIR 3 (3,12); CIMA gira→(7,6);
   DIR 2 (9,6); BAIXO 3 (9,9); DIR gira→(14,13); ESQ 1 (13,13); ESQ gira→(10,15); DIR 3 (13,15); BAIXO 2 (13,17);
   ESQ gira→(8,19); DIR 1 (9,19); BAIXO gira→(13,20); DIR 2 (15,20); CIMA 2 (15,18); DIR 1 (16,18); CIMA 1
   (16,17); DIR 7 (23,17); CIMA 5 (23,12); apertar DIR → B1F (15,30): HYPER POTION em (1,22) (ESQ 5 (10,30); CIMA 2
   (10,28); ESQ 8 (2,28); CIMA 6 (2,22); olhar ESQ). Voltar pela mesma escada.
6. Da área sudeste (chegando em (23,12)): elevador = BAIXO 2 (23,14); DIR 2 (25,14); BAIXO 3 (25,17); DIR 3 (28,17);
   CIMA na porta (28,16). Escada para B3F = ESQ 4 (19,12); BAIXO 3 (19,15); ESQ 4 (15,15); CIMA 1 (15,14); CIMA
   gira→(15,8); DIR 6 (21,8); CIMA 6 (21,2); apertar DIR.
7. Voltando do B3F (chegada em (21,2)) com a LIFT KEY: o mais curto é subir ao B1F: BAIXO 2 (21,4); DIR 2 (23,4);
   BAIXO 1 (23,5); DIR 2 (25,5); BAIXO 1 (25,6); DIR 3 (28,6); CIMA 4 (28,2); DIR → B1F (17,2) e usar o elevador
   do B1F (rota acima). (Pelo labirinto até (28,17) também dá: refazer os passos 1, 5 e 6.)
### MAP_ROCKET_HIDEOUT_B3F (chegada em (18,2))
- NUGGET: ESQ 15 (3,2); BAIXO 1 (3,3); ESQ 1 (2,3); olhar ESQ (escondido em (1,3)).
- TM21: DIR 16 (18,3); BAIXO 1 (18,4); DIR 1 (19,4); BAIXO 3 (19,7) [GRUNT_15]; ESQ 3 (16,7); BAIXO 5 (16,12);
  DIR 1 (17,12); BAIXO 1 (17,13); DIR 2 (19,13); olhar BAIXO.
- RARE CANDY: ESQ 3 (16,13); CIMA 4 (16,9); DIR 2 (18,9); CIMA 1 (18,8); DIR 1 (19,8); CIMA 4 (19,4); ESQ 7 (12,4);
  BAIXO 5 (12,9); ESQ 3 (9,9); BAIXO gira→(9,14); DIR gira→(10,13); DIR 2 (12,13); olhar CIMA.
- BLACKGLASSES: ESQ 4 (8,13); CIMA 1 (8,12); CIMA gira→(8,9); DIR 4 (12,9); CIMA 2 (12,7); ESQ 7 (5,7); BAIXO 2
  (5,9); ESQ gira→(2,9); BAIXO 1 (2,10); BAIXO gira→(6,11); ESQ 2 (4,11); BAIXO 3 (4,14); ESQ 3 (1,14); BAIXO 2
  (1,16); DIR 1 (2,16); DIR gira→(7,20); ESQ 2 (5,20); BAIXO 5 (5,25); DIR 8 (13,25); CIMA 2 (13,23); DIR 1 (14,23);
  olhar BAIXO, pegar (14,24).
- Escada para B4F: DIR 1 (15,23); CIMA 5 (15,18); apertar ESQ.
- Volta (da escada (15,18) até (18,2)): BAIXO 2 (15,20); ESQ 5 (10,20); CIMA 5 (10,15); CIMA gira→(10,13); ESQ 2
  (8,13); CIMA 1 (8,12); CIMA gira→(8,9); DIR 4 (12,9); CIMA 5 (12,4); DIR 6 (18,4); CIMA 2 (18,2); apertar DIR.
### MAP_ROCKET_HIDEOUT_B4F
- Lado oeste (chegada da escada em (11,15); isolado do resto): MAX ETHER: ESQ 7 (4,15), olhar CIMA. TM49: ESQ 2
  (9,15); CIMA 8 (9,7); ESQ 7 (2,7); CIMA 1 (2,6), olhar ESQ. LIFT KEY: de (9,7) ESQ 4 (5,7); CIMA 4 (5,3); ESQ 1
  (4,3) → GRUNT_18 luta; depois ESQ 1 (3,3), olhar CIMA, pegar (3,2). Escada de volta: (11,15), apertar DIR.
- Elevador (só com LIFT KEY): B1F (24,25), B2F (28,16), B4F (20,23). O lado leste do B4F só se alcança por ele.
- Lado leste (sai do elevador em (20,24)): CALCIUM: ESQ 6 (14,24); CIMA 1 (14,23); ESQ 3 (11,23); BAIXO 1
  (11,24); ESQ 5 (6,24); olhar CIMA. Guardas: voltar a (17,24), CIMA até (17,16); falar com GRUNT_16 de (16,15)
  e com GRUNT_17 de (19,15) (os dois olham para baixo e não puxam luta sozinhos). A barreira (17..18,12..13) abre.
  Subir por x 17 até (17,5), DIR 2 (19,5), olhar CIMA: GIOVANNI. Depois: SILPH SCOPE (20,5) (de (19,5) olhando
  DIR); NET BALL de (17,6) olhando ESQ; NEST BALL: de (18,11) DIR 3 (21,11), CIMA 5 (21,6), olhar DIR.
  Sair pelo elevador → B1F → escada (12,2) [ESQ] → Game Corner.
### Mansion (EEVEE)
- A escada da frente (1F (12,2) → 2F → 3F (12,2) → telhado (10,2)) cai na metade leste do telhado, sem acesso à
  porta (2,12). Usar a porta dos fundos (30,4) da cidade (Passo 4).
### Celadon Gym
- Sem CUT não se entra (árvore (40,35) na cidade). Dentro, árvores (6,8), (3,5), (9,6): cortar uma basta.
### Pokémon Tower
- 2F: rival inevitável (gatilhos (17,5)/(16,6)). 5F: zona de cura (10..12,8..10). 6F: MAROWAK exige SILPH SCOPE
  e precisa ser nocauteado; só então a escada (11,16) libera. 7F: 3 Rockets inevitáveis, Fuji em (11,4).

## Dicas para jogar bem
- Ordem eficiente: COIN CASE e fichas grátis → TEA → EEVEE → loja (WATER STONE, TM31, bebidas → 3 TMs) → ERIKA →
  esconderijo → TEA na portaria da Rota 7 → Saffron → Lavender → torre → Fuji.
- Com CHARMANDER: CHARMELEON varre a ERIKA. Contra GIOVANNI e o MAROWAK falta Água: EEVEE + WATER STONE ($2100,
  4F) = VAPOREON, ótimo nos dois. Alternativa: THUNDERSTONE/FIRE STONE (JOLTEON/FLAREON).
- O EEVEE de Celadon é o único do jogo. VAPOREON, JOLTEON e FLAREON contam para a Pokédex: os outros dois só por
  ovo (EEVEE + DITTO na creche que faz ovos, Four Island, pós-Liga) (conferir). Não descartar o EEVEE.
- PORYGON (9999 fichas) só existe no Prize Room: obrigatório para 100%. ABRA (180) sai com as fichas grátis
  (310 no total). SCYTHER/DRATINI também aparecem na Safari Zone no FireRed.
- TMs do Prize Room valem muito para CHARIZARD: TM35 FLAMETHROWER; TM24 THUNDERBOLT e TM13 ICE BEAM para outros.
- Na torre, levar SUPER POTIONs/REVIVEs; a zona do 5F cura de graça. REPEL/POKé DOLL ajudam com os GHOST antes do
  SCOPE (POKé DOLL foge de qualquer selvagem). A CLEANSE TAG reduz encontros se o primeiro do time segurar.
- Não perder antes de sair: ETHER e PP UP da cidade, as 12 fichas do chão, os 3 TMs das bebidas, TM19, todos os
  itens do esconderijo (inclusive NUGGET, NET BALL, NEST BALL, PP UP escondidos), BIG MUSHROOM da torre.
- Fica para depois: SOOTHE BELL (7F, precisa ITEMFINDER do assistente do Oak na Rota 11); lago de Celadon com SURF
  (PSYDUCK) e SUPER ROD (GRIMER 1%); DIPLOMA (150 capturados).
- Saindo de Celadon para oeste: Rota 16. O SNORLAX (31,13) só acorda com a POKé FLUTE, mas a casa do HM02 FLY
  (MAP_ROUTE16_HOUSE) já é alcançável com CUT pela árvore (41,11) e pelo corredor de cima da portaria (seção 10).
- RAINBOWBADGE libera STRENGTH fora de batalha (o HM04 vem do Warden de Fuchsia). Depois da POKé FLUTE: Rotas
  12-15 e 16-18 até Fuchsia; Saffron/Silph Co. já liberadas (TEA + Fuji resgatado).
