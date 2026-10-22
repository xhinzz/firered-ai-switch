# Seção 14 — Sevii Islands parte I: One, Two e Three Island (METEORITE, Bikers, LOSTELLE, MOLTRES)
Marcos do roteiro cobertos: sevii; novo: tri_pass, novo: game_corner, novo: bikers, novo: lostelle, novo: meteorito, novo: volta_cinnabar, novo: hm06, novo: moltres, novo: blast_burn
Mapas: MAP_ONE_ISLAND_HARBOR, MAP_ONE_ISLAND, MAP_ONE_ISLAND_POKEMON_CENTER_1F, MAP_TWO_ISLAND_HARBOR, MAP_TWO_ISLAND, MAP_TWO_ISLAND_JOYFUL_GAME_CORNER, MAP_TWO_ISLAND_HOUSE, MAP_TWO_ISLAND_CAPE_BRINK, MAP_TWO_ISLAND_CAPE_BRINK_HOUSE, MAP_THREE_ISLAND_HARBOR, MAP_THREE_ISLAND_PORT, MAP_THREE_ISLAND, MAP_THREE_ISLAND_POKEMON_CENTER_1F, MAP_THREE_ISLAND_MART, MAP_THREE_ISLAND_BOND_BRIDGE, MAP_THREE_ISLAND_BERRY_FOREST, MAP_ONE_ISLAND_TREASURE_BEACH, MAP_ONE_ISLAND_KINDLE_ROAD, MAP_ONE_ISLAND_KINDLE_ROAD_EMBER_SPA, MAP_MT_EMBER_EXTERIOR, MAP_MT_EMBER_SUMMIT_PATH_1F, MAP_MT_EMBER_SUMMIT_PATH_2F, MAP_MT_EMBER_SUMMIT_PATH_3F, MAP_MT_EMBER_SUMMIT, MAP_CINNABAR_ISLAND

## Passo a passo
Resumo da cadeia obrigatória: CELIO dá o TRI-PASS → entrar no Joyful Game Corner (Two Island) → vencer os 4 Bikers
(Three Island) → salvar a LOSTELLE do HYPNO (Berry Forest) → entregar o METEORITE ao pai dela → pisar na coluna x=12
do Centro da One Island → o BILL leva você de volta a Cinnabar. O Mt. Ember NÃO faz parte do pedido (é opcional:
MOLTRES e HM06). Durante toda a viagem a balsa só liga as ilhas 1, 2 e 3 (Vermilion não aparece no menu) e o FLY só
mostra o mapa das ilhas: não há como voltar a Kanto antes do fim.

1. Chegada (automática, vindo de Cinnabar com o BILL): MAP_ONE_ISLAND_HARBOR → MAP_ONE_ISLAND; o BILL leva você até
   o Pokémon Net Center (porta (14,5)) → MAP_ONE_ISLAND_POKEMON_CENTER_1F.
2. Cena do CELIO (automática, marco novo tri_pass): o BILL dá o METEORITE (key item) e o CELIO (15,6) dá o TRI-PASS
   (key item) e a página extra do TOWN MAP (se você nunca pegou o TOWN MAP com a irmã do rival, recebe o próprio
   TOWN MAP). A partir daqui o PC NÃO abre (nem Pokémon nem itens: "usual PC services unavailable") até você pisar
   em MAP_THREE_ISLAND_PORT. O pedido: levar o METEORITE ao dono do Game Corner de Two Island.
   - One Island NÃO tem Poké Mart. Enfermeira em (5,2); a porta do Centro é (9,9).
3. Balsa: porta (12,18) da ilha → MAP_ONE_ISLAND_HARBOR, marinheiro em (8,6) → escolha TWO ISLAND.
4. MAP_TWO_ISLAND_HARBOR → MAP_TWO_ISLAND. Fale UMA vez com o vendedor da barraca (28,4) (isso é necessário para a
   barraca ampliar o estoque depois). Centro em (21,7).
5. Joyful Game Corner (porta (39,9) → MAP_TWO_ISLAND_JOYFUL_GAME_CORNER) — marco novo game_corner. Cena automática
   ao entrar: o pai da LOSTELLE (5,5) pede para procurá-la em Three Island; um Biker entra por engano e sai. Essa
   cena é o que ativa a gangue de Three Island (sem ela os Bikers só bloqueiam a rua e nada dispara).
6. Opcional agora (ou depois): Cape Brink ao norte da cidade (saída norte x 36–40) → MAP_TWO_ISLAND_CAPE_BRINK; casa
   (12,16) com a tutora dos golpes supremos (ver NPCs). RARE CANDY escondido em (15,13).
7. Balsa da Two Island → THREE ISLAND. MAP_THREE_ISLAND_HARBOR → MAP_THREE_ISLAND_PORT: ao entrar nesse mapa o PC
   volta a funcionar em todo lugar (BILL e CELIO terminaram a conexão com Kanto).
8. Suba para MAP_THREE_ISLAND (saída norte do porto, x 10–12). A gangue ocupa a rua em (7..11, 22..24) e bloqueia
   todo o norte da cidade (Mart, casas, Bond Bridge). O Centro (porta (14,27), entra por (14,28)) fica ANTES da
   gangue: cure-se lá antes de seguir — são 4 lutas seguidas sem cura.
9. Marco novo bikers: pise na linha y=27 (x 7–11) → diálogo entre moradores e o chefe. Dê mais um passo para y=26
   (x 7–11) → um Biker pergunta se quer briga: responda YES (NO só faz você recuar um passo). Lutas em sequência:
   TRAINER_BIKER_GOON → TRAINER_BIKER_GOON_2 → TRAINER_BIKER_GOON_3 → TRAINER_CUE_BALL_PAXTON. A gangue some, também
   os Bikers do porto.
10. Logo depois, fale com o morador (7,24): FULL RESTORE (só enquanto a LOSTELLE não foi salva — depois do resgate
    os dois moradores somem do mapa). O outro (8,23) diz que a LOSTELLE foi para a Bond Bridge.
11. Agora dá para usar o Mart (porta (18,12) → MAP_THREE_ISLAND_MART): compre ULTRA BALLs e HYPER POTIONs.
12. Saída oeste da cidade (borda x=0, y 7–9) → MAP_THREE_ISLAND_BOND_BRIDGE. Atravesse a ponte para oeste
    (treinadores na linha de visão) até a entrada da floresta (12,6)/(13,6) → MAP_THREE_ISLAND_BERRY_FOREST (chega
    em (42..44,41)). CUT e SURF não são necessários para chegar à LOSTELLE.
13. Marco novo lostelle: a LOSTELLE está no canto noroeste, em (4,8). Fale com ela → HYPNO Nv30 selvagem aparece
    (evento único). Vencer, capturar ou fugir completam o evento (o script não confere o resultado). Ela dá a
    IAPAPA BERRY e vocês são levados automaticamente para dentro do Game Corner de Two Island.
14. Marco novo meteorito: cena automática de reencontro; fale com o pai (5,5): ele recebe o METEORITE e dá a MOON STONE
    (se a mochila estiver cheia, volte depois para pegar; a volta para casa já fica liberada de qualquer jeito).
15. Antes de voltar ao Centro da One Island, faça os extras de One Island que quiser (Treasure Beach, Kindle Road,
    Ember Spa/HM06, Mt. Ember/MOLTRES — passos 17–20). Tudo continua acessível depois pela balsa de Vermilion.
16. Marco novo volta_cinnabar: balsa até a One Island, entre no Centro. BILL e CELIO ficam em (14,7)/(14,8). Pisar
    em QUALQUER tile da coluna x=12 (y 6–9) dispara a despedida e o BILL leva você de barco para MAP_CINNABAR_ISLAND.
    (Para só curar, vá da porta (9,9) até a enfermeira (5,2) sem passar de x=11.) Em Cinnabar o BILL fala que com
    o TRI-PASS dá para voltar pela balsa de Vermilion e vai embora. Fim da parte I; a LOSTELLE passa a ficar em
    casa (MAP_THREE_ISLAND_HOUSE1). Próximo: Ginásio de Viridian (seção 15).

Extras de One Island (precisam de SURF; ROCK SMASH/STRENGTH conforme indicado):
17. Treasure Beach: da ilha (perto do porto, x 10–14, y 18–19) SURF para o sul → MAP_ONE_ISLAND_TREASURE_BEACH
    (8 itens escondidos, ver Itens).
18. Kindle Road: saia pela borda leste da One Island (x=23, y 12–13) → MAP_ONE_ISLAND_KINDLE_ROAD em (0..2,130..133).
    SURF para o norte até a praia (8..16,116..121) e suba a pé (grama e muitos treinadores) até a Ember Spa
    (porta (15,58)).
19. Marco novo hm06: MAP_ONE_ISLAND_KINDLE_ROAD_EMBER_SPA — o velho em (10,5) dá a HM06 (ROCK SMASH; uso fora de
    batalha exige a MARSH BADGE). Pisar no tile (13,13) das águas termais cura o time inteiro (repete a cada entrada no mapa).
20. Mt. Ember (marco novo moltres): da Kindle Road, SURF da margem oeste (x≈10–14, y≈51–57) para o norte até a praia
    (6..16,7..18) e entre em (11,6)/(12,6) → MAP_MT_EMBER_EXTERIOR (chega em (28..29,48)).
    a) STRENGTH é obrigatório logo no início (ver Quebra-cabeças A). ROCK SMASH não é necessário para chegar ao topo.
    b) Suba pelo lado oeste (RANGER BETH em (14,42), RANGER LOGAN em (15,28)) até a caverna (14,24) →
       MAP_MT_EMBER_SUMMIT_PATH_1F (2,15) → escada (11,1) → MAP_MT_EMBER_SUMMIT_PATH_2F (8,39) → escada (39,6) →
       MAP_MT_EMBER_SUMMIT_PATH_3F (2,4) → saída (11,8) → MAP_MT_EMBER_EXTERIOR (39,19), parte de cima.
    c) Topo: entrada do cume em (29,7) → MAP_MT_EMBER_SUMMIT (chega em (9,15)). Empurre as pedras (Quebra-cabeças B)
       e fale com o MOLTRES em (9,6).
    d) A Ruby Path (porta (42,39), com dois Rockets parados em (41,40)/(42,40)) está FECHADA até o pós-jogo.

## Lutas obrigatórias
### Biker (1º) — TRAINER_BIKER_GOON
- Onde: MAP_THREE_ISLAND, gatilho na linha y=26 (x 7–11), depois da cena da linha y=27
- Time: KOFFING Nv37 [HAZE, SMOKESCREEN, SLUDGE, TACKLE]; GRIMER Nv37 [ACID ARMOR, SCREECH, MINIMIZE, SLUDGE]; sem itens
- Tipos que funcionam: Psychic (Ground não acerta KOFFING, que tem LEVITATE); Ground no GRIMER
- Nível recomendado do time: 40+
### Biker (2º) — TRAINER_BIKER_GOON_2
- Onde: em seguida, sem cura
- Time: KOFFING Nv38 [HAZE, SMOKESCREEN, SLUDGE, TACKLE]
- Tipos que funcionam: Psychic
- Nível recomendado do time: 40+
### Biker (3º) — TRAINER_BIKER_GOON_3
- Onde: em seguida, sem cura
- Time: GRIMER Nv38 [SLUDGE, MINIMIZE, SCREECH, ACID ARMOR]
- Tipos que funcionam: Ground, Psychic
- Nível recomendado do time: 40+
### Cue Ball PAXTON (chefe) — TRAINER_CUE_BALL_PAXTON
- Onde: em seguida, sem cura (ele desce até você)
- Time: WEEZING Nv39 [SELF-DESTRUCT, SLUDGE, SMOKESCREEN, HAZE]; MUK Nv39 [SLUDGE, MINIMIZE, SCREECH, ACID ARMOR]; sem itens
- Tipos que funcionam: Psychic nos dois; Ground só no MUK (WEEZING tem LEVITATE). Cuidado com o SELF-DESTRUCT.
- Nível recomendado do time: 40+ (recompensa $936)
### HYPNO selvagem (evento da LOSTELLE) — sem TRAINER_ (encontro fixo)
- Onde: MAP_THREE_ISLAND_BERRY_FOREST, ao falar com a LOSTELLE (4,8)
- Time: HYPNO Nv30 [CONFUSION, HEADBUTT, POISON GAS, MEDITATE]
- Tipos que funcionam: Bug, Ghost, Dark; qualquer golpe forte resolve (é Nv30)
- Nível recomendado do time: 35+. Pode capturar (há HYPNO selvagem 37–40 na mesma floresta).

## Treinadores opcionais relevantes
- MAP_ONE_ISLAND_TREASURE_BEACH: TRAINER_SWIMMER_FEMALE_AMARA (8,11) SEEL/SEEL/DEWGONG Nv36, $144 (precisa SURF)
- MAP_ONE_ISLAND_KINDLE_ROAD (Nv33–39; boa EXP):
  TRAINER_FISHERMAN_TOMMY (15,25) 2 GOLDEEN Nv33 + 3 SEAKING Nv35, $1260; TRAINER_SWIMMER_FEMALE_MARIA (11,32) 2 SEADRA
  Nv37; TRAINER_SWIMMER_MALE_FINN (7,39) STARMIE Nv38; TRAINER_CRUSH_GIRL_SHARON (9,53) MANKEY/PRIMEAPE Nv37, $888;
  TRAINER_BLACK_BELT_HUGH (11,64) MACHOP/MACHOKE Nv37, $888; TRAINER_BLACK_BELT_SHEA (16,64) MACHOP/MACHOKE Nv38,
  $912; TRAINER_CRUSH_KIN_MIK_KIA (8,68)/(9,68) DUPLA MACHOKE/PRIMEAPE Nv39, $1872; TRAINER_SWIMMER_MALE_GARRETT
  (19,79) SHELLDER/CLOYSTER Nv35 + WARTORTLE Nv38; TRAINER_CAMPER_BRYCE (11,89) NIDORINO/RATICATE/SANDSLASH Nv36,
  $720; TRAINER_CRUSH_GIRL_TANYA (18,105) HITMONLEE/HITMONCHAN Nv38, $912; TRAINER_PICNICKER_CLAIRE (9,108) MEOWTH x2/
  PIKACHU/CLEFAIRY Nv35, $700; TRAINER_SWIMMER_FEMALE_ABIGAIL (17,132) PSYDUCK Nv35/36 + GOLDUCK Nv37 (ilhota perto
  da entrada). Os Fighting do meio da estrada ficam em corredores estreitos.
- MAP_MT_EMBER_EXTERIOR: TRAINER_PKMN_RANGER_BETH (14,42) BELLSPROUT/GLOOM/GLOOM Nv38, usa FULL RESTORE, $1368 (logo
  depois das pedras); TRAINER_CRUSH_GIRL_JOCELYN (22,35) 2 HITMONCHAN Nv38, $912; TRAINER_PKMN_RANGER_LOGAN (15,28)
  visão 5, EXEGGCUTE Nv37 [SLEEP POWDER...] / EXEGGUTOR Nv40 [HYPNOSIS], usa FULL RESTORE, $1440 (vigia a entrada
  da caverna). TRAINER_TEAM_ROCKET_GRUNT_43/44 só lutam no pós-jogo.
- MAP_THREE_ISLAND_BOND_BRIDGE: TRAINER_AROMA_LADY_NIKKI (27,10) visão 5 BELLSPROUT/WEEPINBELL Nv37, $1036 (perto
  da entrada da floresta); TRAINER_TUBER_AMIRA (33,13) POLIWAG/POLIWHIRL/POLIWAG Nv34–35; TRAINER_TUBER_ALEXIS (50,11)
  2 STARYU + 2 KRABBY Nv34; TRAINER_AROMA_LADY_VIOLET (68,10) BULBASAUR/IVYSAUR/IVYSAUR Nv36, $1008;
  TRAINER_TWINS_JOY_MEG (77,5)/(78,5) DUPLA 2 CLEFAIRY Nv37, $888; TRAINER_SWIMMER_FEMALE_TISHA (36,4) KINGLER Nv38
  (precisa SURF).

## Itens
### MAP_ONE_ISLAND_POKEMON_CENTER_1F
- METEORITE — key item, presente do BILL (cena de chegada)
- TRI-PASS — key item, presente do CELIO (15,6) (mesma cena)
- Página do TOWN MAP (ou o TOWN MAP, se ainda não tinha) — presente do CELIO
### MAP_ONE_ISLAND_TREASURE_BEACH (precisa SURF; todos renováveis)
- (8,20) STARDUST — escondido
- (13,27) STARDUST — escondido
- (11,31) PEARL — escondido
- (9,34) PEARL — escondido
- (15,22) ULTRA BALL — escondido
- (16,33) ULTRA BALL — escondido
- (15,29) STAR PIECE — escondido
- (8,27) BIG PEARL — escondido
### MAP_ONE_ISLAND_KINDLE_ROAD
- (15,70) ETHER — visível; ROCK SMASH nas rochas (15,75), (15,74), (15,73), subindo pela coluna x=15 a partir de (15,76)
- (17,103) MAX REPEL — visível; areia isolada a leste, chegar de SURF
- (18,114) CARBOS — visível; descendo pela coluna x=18: ROCK SMASH em (18,111) e (18,112), pegar de (18,113)
### MAP_ONE_ISLAND_KINDLE_ROAD_EMBER_SPA
- HM06 (ROCK SMASH) — TM/HM, presente do velho (10,5)
### MAP_MT_EMBER_EXTERIOR
- (13,6) ULTRA BALL — visível; parte de cima, beco a oeste da entrada do cume
- (48,20) DIRE HIT — visível; lado leste
- (38,10) FIRE STONE — visível; exige ROCK SMASH + STRENGTH (Quebra-cabeças C)
- (18,17) FIRE STONE — escondido sobre uma rocha; ficar em (18,16) virado para o sul e apertar A
- (8,30) ULTRA BALL — escondido; fim do beco a oeste/sudoeste do LOGAN (pegar de (9,30))
### MAP_TWO_ISLAND
- (39,16) REVIVE — visível; CUT na árvore (30,16) e seguir a linha y=16 para leste
### MAP_TWO_ISLAND_CAPE_BRINK
- (15,13) RARE CANDY — escondido; atrás da casa da tutora (pegar de (14,13))
- (16,28) PP MAX — escondido; areia na margem leste do lago, chegar de SURF por (15,28)
### MAP_TWO_ISLAND_JOYFUL_GAME_CORNER
- MOON STONE — presente do pai da LOSTELLE (5,5) ao entregar o METEORITE
### MAP_THREE_ISLAND
- FULL RESTORE — presente do morador (7,24) depois dos Bikers e ANTES de salvar a LOSTELLE
- (18,17) ZINC — visível; CUT na árvore (20,7) e descer pela coluna x=21
- (5,13) PP UP — escondido; só pela Bond Bridge: CUT na árvore (86,13) dela e seguir a linha y=13 para leste até
  Three Island (0..4,13)
### MAP_THREE_ISLAND_BOND_BRIDGE
- (61,5) MAX REPEL — escondido sobre uma rocha; ficar em (61,6) virado para o norte
- (33,7) STARDUST — escondido (renovável); a pé
- (44,12) PEARL — escondido (renovável); banco de areia no mar, precisa SURF
### MAP_THREE_ISLAND_BERRY_FOREST
- (12,5) MAX ETHER — visível
- (27,11) FULL HEAL — visível
- (12,43) MAX ELIXIR — visível; precisa SURF + CUT (Quebra-cabeças D)
- IAPAPA BERRY — presente da LOSTELLE depois do HYPNO
- Berries escondidas (renováveis): RAZZ (31,25), BLUK (15,15), NANAB (25,24), WEPEAR (11,24), ORAN (37,18),
  CHERI (14,23), CHESTO (47,5), PECHA (7,30), RAWST (16,5), ASPEAR (25,6), PERSIM (46,32), PINAP (43,16), LUM (8,5)
### MAP_THREE_ISLAND_DUNSPARCE_TUNNEL (pós-jogo)
- NUGGET — presente do garimpeiro só com a National Pokédex; (21,3) NUGGET escondido na parte escavada (pós-jogo)

## NPCs importantes
- MAP_ONE_ISLAND_POKEMON_CENTER_1F (15,6): CELIO — dá TRI-PASS; no pós-jogo (National Pokédex) pede o RUBY e depois
  troca o TRI-PASS pelo RAINBOW PASS (ilhas 4–7). BILL (14,6) só conversa até a volta.
- Marinheiros da Seagallop em (8,6) de MAP_ONE_ISLAND_HARBOR / MAP_TWO_ISLAND_HARBOR / MAP_THREE_ISLAND_HARBOR: durante a
  viagem só 1↔2↔3; depois da volta a Cinnabar também Vermilion. Em Vermilion o marinheiro da balsa (24,33) leva a
  One/Two/Three com o TRI-PASS. Cinnabar não tem balsa própria.
- MAP_ONE_ISLAND_KINDLE_ROAD_EMBER_SPA (10,5): velho — HM06. Tile (13,13): cura grátis.
- MAP_MT_EMBER_EXTERIOR (29,45): Hiker tutor de EXPLOSION (uma vez só, logo na entrada).
- MAP_TWO_ISLAND (28,4): barraca. Estoque inicial GREAT BALL, FRESH WATER; depois de salvar a LOSTELLE (e de já ter
  falado com ele uma vez antes) ULTRA BALL, GREAT BALL, SODA POP, FRESH WATER; após o Hall of Fame + LEMONADE e
  MOOMOO MILK; após a ligação com Hoenn REPEAT BALL, TIMER BALL, LAVA COOKIE.
- MAP_TWO_ISLAND_HOUSE (7,5): Move Maniac — relembra golpes de nível; cobra 1 BIG MUSHROOM ou 2 TINY MUSHROOM.
- MAP_TWO_ISLAND_CAPE_BRINK_HOUSE (4,4): tutora dos golpes supremos. Ensina BLAST BURN (marco novo blast_burn) se o
  PRIMEIRO Pokémon do time for CHARIZARD com amizade máxima (255). Não confere o treinador original. Uma vez só por
  golpe (FRENZY PLANT/VENUSAUR e HYDRO CANNON/BLASTOISE pelas mesmas regras).
- MAP_TWO_ISLAND_JOYFUL_GAME_CORNER (5,5): pai da LOSTELLE (pedido, METEORITE → MOON STONE). Minijogos só por link.
- MAP_THREE_ISLAND (7,24) e (8,23): moradores — FULL RESTORE e a pista da Bond Bridge.
- MAP_THREE_ISLAND_MART: ULTRA BALL, HYPER POTION, REVIVE, FULL HEAL, ESCAPE ROPE, MAX REPEL (só depois dos Bikers).
- MAP_THREE_ISLAND_BERRY_FOREST (4,8): LOSTELLE — HYPNO Nv30 e IAPAPA BERRY.
- MAP_THREE_ISLAND_DUNSPARCE_TUNNEL (6,3): garimpeiro bloqueando o túnel até a National Pokédex.

## Pokémon disponíveis (FireRed)
### MAP_ONE_ISLAND
- surf: TENTACOOL 5-40 (95%), TENTACRUEL 35-40 (5%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: HORSEA 5-15 (80%), MAGIKARP 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (40%), SHELLDER 15-25 (40%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_ONE_ISLAND_TREASURE_BEACH
- grama: SPEAROW 31-32 (30%), TANGELA 33-35 (30%), FEAROW 36-40 (20%), MEOWTH 31 (10%), PSYDUCK 31 (5%), PERSIAN 37-40 (5%)
- surf: TENTACOOL 5-40 (95%), TENTACRUEL 35-40 (5%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: HORSEA 5-15 (80%), MAGIKARP 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (80%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_ONE_ISLAND_KINDLE_ROAD
- grama: PONYTA 31-34 (30%), SPEAROW 30-32 (25%), FEAROW 36 (10%), GEODUDE 31 (10%), MEOWTH 31 (10%), PSYDUCK 34 (5%),
  RAPIDASH 37-40 (5%), PERSIAN 37-40 (5%)
- surf: TENTACOOL 5-40 (95%), TENTACRUEL 35-40 (5%)
- rock smash: GEODUDE 5-30 (95%), GRAVELER 25-40 (5%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: HORSEA 5-15 (80%), MAGIKARP 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (80%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_MT_EMBER_EXTERIOR
- grama: PONYTA 30-36 (35%), FEAROW 38-40 (25%), SPEAROW 30-32 (15%), MACHOP 35 (10%), GEODUDE 33 (10%), RAPIDASH 39-42 (5%)
- rock smash: GEODUDE 5-30 (95%), GRAVELER 25-40 (5%)
### MAP_MT_EMBER_SUMMIT_PATH_1F e MAP_MT_EMBER_SUMMIT_PATH_3F
- caverna: GEODUDE 29-37 (50%), MACHOP 31-39 (50%)
### MAP_MT_EMBER_SUMMIT_PATH_2F
- caverna: GEODUDE 30-34 (40%), MACHOP 32-36 (40%), MACHOKE 38-40 (20%)
- rock smash: GEODUDE 5-30 (95%), GRAVELER 25-40 (5%)
### MAP_MT_EMBER_SUMMIT
- encontro fixo: MOLTRES Nv50 [FIRE SPIN, AGILITY, ENDURE, FLAMETHROWER] (único)
### MAP_TWO_ISLAND
- nenhum selvagem (mar agitado: sem surf nem pesca)
### MAP_TWO_ISLAND_CAPE_BRINK
- grama: ODDISH 30-32 (30%), SPEAROW 31 (20%), GLOOM 36-38 (15%), FEAROW 36 (10%), MEOWTH 31 (10%), PSYDUCK 31 (5%),
  GOLDUCK 37-40 (5%), PERSIAN 37-40 (5%)
- surf: PSYDUCK 5-40 (95%), GOLDUCK 35-40 (5%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: POLIWAG 5-15 (60%), MAGIKARP 5-15 (20%), GOLDEEN 5-15 (20%)
- SUPER ROD: POLIWAG 15-25 (40%), POLIWHIRL 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)
### MAP_THREE_ISLAND_BOND_BRIDGE
- grama: PIDGEY 29-32 (30%), ODDISH 31 (20%), PIDGEOTTO 34-40 (15%), GLOOM 36 (10%), MEOWTH 31 (10%), VENONAT 34 (5%),
  PSYDUCK 31 (5%), PERSIAN 37-40 (5%)
- surf: TENTACOOL 5-40 (95%), TENTACRUEL 35-40 (5%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: HORSEA 5-15 (80%), MAGIKARP 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (80%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_THREE_ISLAND_BERRY_FOREST
- grama: PIDGEOTTO 37 (20%), GLOOM 35 (20%), PIDGEY 32 (10%), ODDISH 30 (10%), VENONAT 34 (10%), DROWZEE 34 (10%),
  EXEGGCUTE 35 (5%), PSYDUCK 31 (5%), VENOMOTH 37-40 (5%), HYPNO 37-40 (5%)
- surf: PSYDUCK 5-40 (95%), GOLDUCK 35-40 (5%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: GOLDEEN 5-15 (60%), MAGIKARP 5-15 (20%), POLIWAG 5-15 (20%)
- SUPER ROD: GOLDEEN 15-25 (40%), SEAKING 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)
- encontro fixo: HYPNO Nv30 (evento da LOSTELLE, uma vez)
### MAP_THREE_ISLAND_PORT (pós-jogo)
- grama do penhasco leste: DUNSPARCE 5-35 (100%) — só pelo túnel escavado (National Pokédex)
### MAP_MT_EMBER_RUBY_PATH_* (pós-jogo)
- 1F: GEODUDE 32-40 (50%), MACHOP 34-38 (40%), MACHOKE 40-42 (10%); B1F/B2F_STAIRS: GEODUDE 34-42 (70%), SLUGMA 24-30 (30%);
  B2F/B1F_STAIRS: SLUGMA 22-32 (60%), GEODUDE 40-44 (40%); B3F: SLUGMA 18-36 (100%), rock smash SLUGMA 15-35 (90%),
  MAGCARGO 25-45 (10%); rock smash nos outros andares GEODUDE 25-40 (65%), GRAVELER 30-50 (35%)

## Quebra-cabeças
A) MAP_MT_EMBER_EXTERIOR, pedras da entrada (STRENGTH obrigatório). Sem elas não se sai da área da chegada.
   1. De (23,45), empurre a pedra (22,45) para OESTE 3 vezes (ela para em (19,45); você fica em (20,45)).
   2. Desça para (20,46), ande para oeste até (18,46) e empurre a pedra (17,46) para OESTE 3 vezes (para em (14,46);
      você fica em (15,46)).
   3. Suba por (15,45) → (14,45) → (14,44) e siga para o norte (RANGER BETH em (14,42)). As rochas (18,39), (19,40),
      (29,41), (30,42) são atalhos opcionais de ROCK SMASH.
B) MAP_MT_EMBER_SUMMIT (pedras (10,12), (9,12), (8,11), (8,10); MOLTRES em (9,6)). Partindo de (9,15):
   N, N (9,13) → L (10,13) → empurra N: (10,12)→(10,11) → empurra O: (9,12)→(8,12) → N (9,11) → empurra O:
   (8,11)→(7,11) → empurra N: (8,10)→(8,9) → O (7,10) → N (7,9) → empurra L: (8,9)→(9,9) → empurra L: (9,9)→(10,9)
   → N (9,8) → N (9,7) → virado para o norte, A no MOLTRES. Se errar, saia e entre de novo para resetar as pedras.
C) MAP_MT_EMBER_EXTERIOR, FIRE STONE (38,10) (ROCK SMASH + STRENGTH), saindo da parte de cima perto de (33,15):
   N (33,14) → ROCK SMASH para leste em (34,14) → S, S, S até (33,17) → L (34,17) → empurre a pedra (35,17) para
   LESTE 3 vezes (para em (38,17); você em (37,17)) → N, N até (37,15) → ROCK SMASH para oeste em (36,15) → O (36,15)
   → empurre N: (36,14)→(36,13) → empurre O: (35,14)→(34,14) → N, N, N até (35,11) → L, L, L até (38,11) → item ao
   norte. Os degraus (38..40,14) servem para descer de volta.
D) MAP_THREE_ISLAND_BERRY_FOREST, MAX ELIXIR (12,43): SURF no lago do sudoeste (x 6–11, y 32–37), desembarque em
   (6..10,38), CUT nas árvores (11,39), (14,39), (17,39), desça pela coluna x 18–20 até a linha 43, CUT em (16,43) e
   pegue o item em (12,43).
E) MAP_ONE_ISLAND_KINDLE_ROAD: ETHER e CARBOS atrás de rochas de ROCK SMASH (coordenadas em Itens).

## Dicas para jogar bem
- Antes de aceitar a viagem em Cinnabar: compre ULTRA BALL (para o MOLTRES), HYPER POTION, FULL HEAL e REVIVE e
  arrume o time — não há volta a Kanto nem PC até Three Island Port, e One Island não tem loja. Leve no time quem
  sabe SURF (obrigatório para Kindle Road/Treasure Beach/Mt. Ember), STRENGTH (Mt. Ember) e CUT (itens).
- Ordem eficiente: CELIO → Two Island (Game Corner + falar com a barraca) → Three Island (Bikers, FULL RESTORE, Mart)
  → Berry Forest (LOSTELLE) → MOON STONE → extras de One Island com ULTRA BALLs do Mart de Three Island → só então
  pisar na coluna x=12 do Centro da One Island. FLY funciona entre One/Two/Three Island depois de visitadas.
- MOLTRES Nv50: SALVE antes. Se ele desmaiar, some para sempre; se você fugir, volta ao reentrar no mapa. Rock é 4x
  contra ele (cuidado para não nocautear); Water/Electric 2x. Use paralisia/sono e ULTRA BALLs. ENDURE o segura com 1 HP.
- HYPNO do evento é Nv30 e único, mas a espécie é selvagem na mesma floresta: não precisa capturar este.
- FULL RESTORE do morador (7,24) de Three Island: pegue antes de salvar a LOSTELLE (depois ele some).
- BLAST BURN: CHARIZARD na frente do time com amizade 255. Amizade sobe andando com ele no time, subindo de nível e
  com vitaminas; cai se desmaiar. Se ainda não tiver, volte depois (TRI-PASS em Vermilion).
- Itens renováveis (Treasure Beach, berries da Berry Forest, PEARL/STARDUST da Bond Bridge): na primeira visita
  estão todos lá; depois de 1500 passos, ao entrar no mapa, um grupo aleatório reaparece.
- HMs: SURF (Kindle Road, Treasure Beach, Mt. Ember, PP MAX, PEARL, MAX ELIXIR); STRENGTH (Mt. Ember, obrigatório para
  o MOLTRES); ROCK SMASH (ETHER, CARBOS, FIRE STONE (38,10); exige MARSH BADGE); CUT (REVIVE, ZINC, PP UP, MAX ELIXIR).
- O Ginásio de Viridian não depende desta viagem (abre com as insígnias 2–7); a viagem é necessária para 100%.
- Fica para depois da Liga/National Pokédex: Ruby Path (o CELIO pede o RUBY; a entrada (42,39) abre e os Rockets
  TRAINER_TEAM_ROCKET_GRUNT_43/44 lutam), RAINBOW PASS e ilhas 4–7, Dunsparce Tunnel (NUGGETs e DUNSPARCE), novos
  itens da barraca de Two Island. Tudo desta seção continua acessível depois pela balsa de Vermilion.
