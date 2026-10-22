# Seção 16 — Rota 22 (rival), Rota 23 (guardas das insígnias) e Victory Road
Marcos do roteiro cobertos: rival_22, victory_road, novo: tutor_double_edge
Mapas: MAP_VIRIDIAN_CITY, MAP_ROUTE22, MAP_ROUTE22_NORTH_ENTRANCE, MAP_ROUTE23, MAP_VICTORY_ROAD_1F, MAP_VICTORY_ROAD_2F, MAP_VICTORY_ROAD_3F, MAP_INDIGO_PLATEAU_EXTERIOR, MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F

## Passo a passo
1. Requisitos: 8 insígnias (EARTH BADGE do GIOVANNI), HM03 SURF e HM04 STRENGTH ensinados (SURF usa a Soul Badge,
   STRENGTH usa a Rainbow Badge). Time ~50. Não há Centro Pokémon entre Viridian e o Indigo Plateau.
2. Rota 22 (MAP_ROUTE22): sair de Viridian pelo oeste. Vencer o GIOVANNI deixa VAR_MAP_SCENE_ROUTE22 = 3. Com isso,
   pisar em (33,4), (33,5) ou (33,6) dispara a luta tardia com o rival: ele aparece pelo oeste e vem até você.
   Essa coluna x=33 (y 4–6) é a única ligação entre o lado de Viridian e o lado da portaria (as saliências da
   linha y=15 só deixam descer). Então a luta é inevitável. Depois dela a variável vai a 4 e não há revanche aqui.
3. Seguir a oeste até a portaria da Liga: porta em (8,5)/(9,5) → MAP_ROUTE22_NORTH_ENTRANCE.
4. Portaria (MAP_ROUTE22_NORTH_ENTRANCE): entra-se por baixo (7,10). O guarda em (8,2) confere a BOULDER BADGE ao
   pisar em (7,2) (só enquanto VAR_MAP_SCENE_ROUTE23 = 0). Sem ela, o jogador é empurrado para trás. Sair pelo norte
   (7,1) → Rota 23 (8,153).
5. Rota 23 (MAP_ROUTE23), sul → norte. Sete guardas, cada um confere UMA insígnia, em ordem. Cada gatilho só vale
   quando a anterior já foi conferida (VAR_MAP_SCENE_ROUTE23 = n−1). Sem a insígnia, o guarda empurra para trás.
   - CASCADE: guarda (15,149); gatilhos (10,148), (11,148), (12,148), (13,149), (14,149). Depois subir o corredor
     x 13–15.
   - THUNDER: guarda (8,140); gatilhos (4,139), (5,139), (6,140), (7,140). Depois subir o corredor x 6–8.
   - RAINBOW: guarda (14,123); gatilhos (10,122), (11,122), (12,123), (13,123). Depois subir o corredor x 12–14 até
     y=118.
   - SURF obrigatório: a terra acaba em y=118. Surfar para o norte a partir de y=117. Não há cachoeira (WATERFALL não
     é usado) nem pedras de STRENGTH na Rota 23.
   - SOUL: guarda em terra (16,112); gatilhos na água (13–15,112) e nas margens (8–12,109), (11–12,111). Continuar
     surfando pelo canal x 13–15 (y 108–111) até o lago grande. Há uma ilha (x 8–13, y 99–103) com MAX ETHER
     escondido (11,101).
   - MARSH: guarda em terra (10,94); gatilhos na água (7–9,94) e (2–5,92). Surfar pelo canal x 7–9 (y 90–93) até
     o lago seguinte e desembarcar na margem norte (y=83, em x 2–8 ou 15–21). Subir pelas colunas de terra x=8 ou
     x=15 (y 78–82).
   - VOLCANO: grama alta (y 61–76). Guarda (14,61); gatilhos (10,60), (11,60), (12,61), (13,61). Depois subir o
     corredor x 12–14 (y 55–60).
   - EARTH: guarda (6,35); gatilhos (1,31) a (1,36), (4,35), (5,35). Liberado: entrada da Victory Road em (5,28).
6. Victory Road (MAP_VICTORY_ROAD_1F → 2F → 3F → 2F → 3F → 2F → saída leste). Pedras de STRENGTH em interruptores
   de chão. Solução completa em "Quebra-cabeças". Resumo:
   - 1F: pedra (7,18) até o interruptor (20,16). Isso abre a barreira (12,14)/(12,15). Subir ao platô, passar pelas
     COOLTRAINERS NAOMI e ROLANDO e pegar a escada (3,2) para o 2F.
   - 2F (chegada (1,9)): pedra (6,17) até o interruptor (2,19), que abre a barreira (13,10)/(13,11). Pegar TM37,
     FULL HEAL e TM07 e subir pela escada (34,9) ao 3F.
   - 3F (chegada (34,9)): MAX REVIVE (COOLTRAINER GEORGE) e TM50. Desvio opcional: escada (5,2) desce ao 2F noroeste
     (POKéMANIAC DAWSON, GUARD SPEC.) e volta. Depois empurrar a pedra (32,5) até o interruptor (7,7), que abre a
     barreira (12,12)/(12,13). Descer à parte sul (COOLTRAINERS COLBY e CAROLINE), empurrar a pedra (33,18) no
     buraco (34,18) e pular atrás.
   - 2F (cai em (34,19)): empurrar a pedra que caiu, (33,19), até o interruptor (14,19). Isso abre a barreira
     (33,16)/(33,17). Escada (36,17) → 3F (39,17) → escada (37,10) → 2F (38,9).
   - 2F leste: tutor de DOUBLE-EDGE (40,9). Sair por (48,12), andando para a direita/baixo na seta → Rota 23 (18,28).
7. Rota 23 norte: de (18,28) descer para (18,29) → leste até (21,29) → norte x=21 até (21,17) → (17,17) → (17,16)
   → (16,16) → norte x=16 até (16,11) → (15,11) → norte x=15 até (15,2) → oeste até (12,2) → (12,1)–(12,0) (degraus)
   → Indigo Plateau (MAP_INDIGO_PLATEAU_EXTERIOR). Itens escondidos no labirinto: LUM BERRY (3,18), MAX ELIXIR (9,8).
8. Indigo Plateau: porta do Centro Pokémon em (11,6) → MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F (cura, PC, loja). A
   Elite dos 4 é a seção seguinte.

## Lutas obrigatórias
### Rival (Rota 22, luta tardia) — TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE
- Onde: MAP_ROUTE22, gatilhos (33,4), (33,5), (33,6) com VAR_MAP_SCENE_ROUTE22 = 3 (depois do GIOVANNI). O rival sai
  de (25,4).
- Time: PIDGEOT Nv47 [FEATHER DANCE, WING ATTACK, GUST, QUICK ATTACK]; RHYHORN Nv45 [TAKE DOWN, HORN DRILL, ROCK BLAST,
  FURY ATTACK]; GROWLITHE Nv45 [FLAME WHEEL, TAKE DOWN, LEER, AGILITY]; EXEGGCUTE Nv45 [SOLAR BEAM, SLEEP POWDER,
  POISON POWDER, STUN SPORE]; ALAKAZAM Nv47 [PSYCHIC, CALM MIND, FUTURE SIGHT, DISABLE]; BLASTOISE Nv53 [WATER GUN,
  RAIN DANCE, BITE, RAPID SPIN]. Prêmio $1908.
- Tipos que funcionam: Electric/Ice/Rock no PIDGEOT; Water/Grass no RHYHORN (HORN DRILL é OHKO); Water/Ground/Rock no
  GROWLITHE; Fire/Flying/Ice no EXEGGCUTE (CHARIZARD vai bem); Dark/Ghost/Bug no ALAKAZAM (bater rápido, antes do
  CALM MIND acumular); Electric/Grass no BLASTOISE (o CHARIZARD perde para ele).
- Nível recomendado do time: 50–53.

## Treinadores opcionais relevantes
Na Victory Road quase todos ficam na linha de visão do caminho. Contar com as lutas e levar curas.
- MAP_VICTORY_ROAD_1F: TRAINER_COOLTRAINER_NAOMI (14,6) Nv42 ×5 (PERSIAN, PONYTA, RAPIDASH, VULPIX, NINETALES),
  $1512, vê a coluna x=14 ao subir (forçada). TRAINER_COOLTRAINER_ROLANDO (5,2) Nv42 ×5 (RATICATE, IVYSAUR,
  WARTORTLE, CHARMELEON, CHARIZARD), $1512, vê a coluna x=5 perto da escada (forçada).
- MAP_VICTORY_ROAD_2F: TRAINER_BLACK_BELT_DAISUKE (20,11) MACHOKE/MACHOP Nv43, $1032, no platô, olha para baixo e para
  a esquerda (provável). TRAINER_JUGGLER_GREGORY (36,5) MR. MIME Nv48, $1920, vê x=36 para cima (provável a caminho do
  TM07). TRAINER_TAMER_VINCENT (26,6) PERSIAN/GOLDUCK Nv44, $1760, anda. TRAINER_JUGGLER_NELSON (31,16)
  DROWZEE/HYPNO/KADABRA×2 Nv41, $1640, olha para a esquerda. TRAINER_POKEMANIAC_DAWSON (7,4) CHARMELEON/LAPRAS/LICKITUNG
  Nv40, $1920 (só pelo desvio noroeste).
- MAP_VICTORY_ROAD_3F: TRAINER_COOLTRAINER_GEORGE (40,7) Nv42 ×5 (EXEGGUTOR, SANDSLASH, CLOYSTER, ELECTRODE, ARCANINE),
  $1512, luta ao pisar em (39,7) para pegar o MAX REVIVE. TRAINER_COOLTRAINER_ALEXA (21,5) Nv42 ×5 (CLEFAIRY,
  JIGGLYPUFF, PERSIAN, DEWGONG [SHEER COLD], CHANSEY), usa FULL RESTORE, $1512. TRAINER_COOLTRAINER_COLBY (10,17)
  Nv41–43 ×5 (KINGLER [GUILLOTINE], POLIWHIRL, TENTACRUEL, SEADRA, BLASTOISE), $1548, vê (5–9,17) (forçado no caminho
  sul). TRAINER_COOLTRAINER_CAROLINE (11,16) Nv42 ×5 (BELLSPROUT, WEEPINBELL, VICTREEBEL, PARAS, PARASECT [SPORE]),
  $1512. TRAINER_COOL_COUPLE_RAY_TYRA (38,13)/(39,13) dupla NIDOQUEEN/NIDOKING Nv45, $2160, veem só (38,14)/(39,14).
  Dá para desviar pela coluna x=40 ou x=36.

## Itens
### MAP_ROUTE23
- (11,101) MAX ETHER — escondido (ilha do lago; precisa SURF)
- (20,72) ULTRA BALL — escondido (no muro entre as estátuas, a nordeste do lago; olhar para cima de (20,73))
- (19,42) FULL RESTORE — escondido (na pedra a leste da grama mais ao norte; de (18,42) ou (20,42))
- (2,29) SITRUS BERRY — escondido (a oeste-sudoeste da entrada da Victory Road)
- (10,67) ASPEAR BERRY — escondido (a sudoeste do guarda da VOLCANO)
- (3,128) LEPPA BERRY — escondido (a noroeste do guarda da THUNDER)
- (3,18) LUM BERRY — escondido (parte norte, a sudoeste do labirinto de pedras)
- (9,8) MAX ELIXIR — escondido (parte noroeste do labirinto)
### MAP_VICTORY_ROAD_1F
- (14,1) TM02 (DRAGON CLAW) — TM, visível (precisa STRENGTH; ver quebra-cabeças)
- (12,3) RARE CANDY — visível (precisa STRENGTH; só um dos dois por "carga" da pedra)
- (16,1) FULL RESTORE — escondido (na pedra; olhar para a esquerda de (17,1))
- (12,12) ULTRA BALL — escondido (na pedra; olhar para baixo de (12,11))
### MAP_VICTORY_ROAD_2F
- (14,13) TM37 (SANDSTORM) — TM, visível (pegar de (14,14))
- (25,13) FULL HEAL — visível (pegar de (25,12))
- (40,7) TM07 (HAIL) — TM, visível (pegar de (39,7))
- (17,6) GUARD SPEC. — visível (área noroeste, só pela escada (5,2) do 3F)
### MAP_VICTORY_ROAD_3F
- (38,7) MAX REVIVE — visível (pegar de (39,7); o GEORGE luta)
- (12,9) TM50 (OVERHEAT) — TM, visível (pegar de (12,8))

## NPCs importantes
- MAP_ROUTE22_NORTH_ENTRANCE (8,2): guarda da BOULDER BADGE.
- MAP_ROUTE23: guardas CASCADE (15,149), THUNDER (8,140), RAINBOW (14,123), SOUL (16,112), MARSH (10,94),
  VOLCANO (14,61), EARTH (6,35).
- MAP_VICTORY_ROAD_2F (40,9): tutor de DOUBLE-EDGE (ensina UMA vez só, a um Pokémon compatível; escolher bem).
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F: loja ULTRA BALL, GREAT BALL, FULL RESTORE, MAX POTION, REVIVE, FULL HEAL,
  MAX REPEL; enfermeira e PC.

## Pokémon disponíveis (FireRed)
### MAP_ROUTE22
- grama: RATTATA 2-5 (45%), MANKEY 2-5 (45%), SPEAROW 3-5 (10%)
- surf: PSYDUCK 20-40 (100%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: POLIWAG 5-15 (60%), MAGIKARP 5-15 (20%), GOLDEEN 5-15 (20%)
- SUPER ROD: POLIWAG 15-25 (40%), POLIWHIRL 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)
### MAP_ROUTE23
- grama: MANKEY 32-34 (30%), FEAROW 40-44 (25%), EKANS 32-34 (20%), SPEAROW 32-34 (15%), PRIMEAPE 42 (5%), ARBOK 44 (5%)
- surf: PSYDUCK 20-40 (100%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: POLIWAG 5-15 (60%), MAGIKARP 5-15 (20%), GOLDEEN 5-15 (20%)
- SUPER ROD: POLIWAG 15-25 (40%), POLIWHIRL 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)
### MAP_VICTORY_ROAD_1F e MAP_VICTORY_ROAD_3F (mesma tabela)
- caverna: ONIX 40-46 (30%), MACHOP 32 (20%), GEODUDE 32 (20%), ZUBAT 32 (10%), ARBOK 44 (5%), GOLBAT 44 (5%),
  MAROWAK 44-46 (5%), MACHOKE 44-46 (5%)
### MAP_VICTORY_ROAD_2F
- caverna: MACHOP 34 (20%), GEODUDE 34 (20%), ONIX 45-48 (20%), PRIMEAPE 42 (10%), ZUBAT 34 (10%), ARBOK 46 (5%),
  GOLBAT 46 (5%), MAROWAK 46-48 (5%), MACHOKE 46-48 (5%)

## Quebra-cabeças
Regras (conferidas no código): STRENGTH precisa ser ativado de novo a cada troca de mapa (falar com a pedra e
aceitar). O jogador NÃO anda junto ao empurrar: a pedra vai 1 tile e você fica parado. O interruptor só dispara quando
uma PEDRA chega nele; o jogador pisando não faz nada. Entrar na Rota 23 zera todos os interruptores e as pedras da
Victory Road, e as barreiras voltam. Subir/descer escadas entre andares devolve as pedras às posições iniciais, mas
mantém os interruptores já ativados.
"←2" = empurrar 2 vezes para a esquerda. Entre parênteses, onde ficar para empurrar.

### Victory Road 1F (MAP_VICTORY_ROAD_1F) — pedra (7,18) → interruptor (20,16)
1. Da entrada (11,20), ir a (7,17) e empurrar ↓1: pedra em (7,19).
2. De (6,19) empurrar →5: pedra em (12,19).
3. De (12,20) empurrar ↑2: pedra em (12,17).
4. De (11,17) empurrar →7: pedra em (19,17).
5. De (19,18) empurrar ↑2: pedra em (19,15).
6. De (18,15) empurrar →1: pedra em (20,15).
7. De (20,14) empurrar ↓1: pedra em (20,16) = interruptor. A barreira (12,14)/(12,15) some.
Caminho até a escada: (7,19) → subir x=7 pelos degraus (7,16) até (7,14) → leste por y=14, passando (12,14), até
(14,14) → norte x=14 até (14,8) (NAOMI) → oeste até (10,8) → degraus (10,9) → (10,10) → oeste até (5,10) → norte
x=5/x=4 até (4,2) (ROLANDO) → escada (3,2).
Canto nordeste (opcional, itens): do platô, degraus (18,9) → (18,10) → (21,10) → norte x=21 até (21,4) → (20,4) →
(20,3) → (17,3). A pedra (16,3) só deixa pegar UM item por vez (busca exaustiva confirma):
- TM02: de (17,3) empurrar ←3 (pedra em (13,3)); andar até (14,3), subir a (14,2), olhar para cima e pegar (14,1).
- RARE CANDY: de (17,3) empurrar ←2 (pedra em (14,3)); ir (15,3) → (15,4) → (14,4) e empurrar ↑1 (pedra em
  (14,2)); subir a (14,3), ir a (13,3) e pegar (12,3) à esquerda.
- Para resetar a pedra (16,3) sem perder o interruptor: subir a escada (3,2) até o 2F e descer de novo.
- FULL RESTORE escondido: de (17,1) olhar para a esquerda (16,1). ULTRA BALL escondida: de (12,11) olhar para baixo.

### Victory Road 2F (MAP_VICTORY_ROAD_2F) — pedra (6,17) → interruptor (2,19)
1. Da chegada (1,9), descer até (7,17) e empurrar ←2: pedra em (4,17).
2. De (4,16) empurrar ↓2: pedra em (4,19).
3. De (5,19) empurrar ←2: pedra em (2,19) = interruptor. A barreira (13,10)/(13,11) some.
(Outra ordem que também serve: ↓1, ←2, ↓1, ←2.)
Caminho: (4,19) → norte x=4 até (4,13) → leste até (9,13) → degraus (9,12) → platô (9,11) → leste por y=11 passando
(13,11) até (16,11) → (16,12) → leste até (20,12) → sul x=20 até (20,17) → (23,17) → degraus (23,18) → (23,19).
- TM37: de (23,19) oeste até (18,19) → norte x=18 até (18,14) → oeste até (14,14) e pegar acima.
- Para o leste: (23,20) → leste por y=20 até (35,20) → (35,19) → (40,19) → norte x=40 até (40,14) → oeste até (34,14).
  FULL HEAL: (34,12) → oeste até (25,12), pegar abaixo. TM07: (34,10) → (33,10) → (33,7) → oeste até (27,7) →
  (27,4) → leste até (37,4) → (37,7) → (39,7), pegar à direita (o GREGORY vê x=36).
- Escada para o 3F: (34,14) → norte x=34 até (34,9).
A pedra (8,7) separa o canto noroeste do resto. Não é necessária.

### Victory Road 3F (MAP_VICTORY_ROAD_3F) — pedra (32,5) → interruptor (7,7)
Chegada (34,9). MAX REVIVE: (34,3) → leste até (39,3) → descer até (39,7) (GEORGE) → pegar à esquerda. TM50: de (34,3)
oeste por y=3 até (12,3) → descer até (12,8) → pegar abaixo.
Desvio opcional ao 2F noroeste: (12,3) → (12,4) → oeste até (7,4) → (7,3) → (6,3) → (6,2) → escada (5,2). No 2F
(chegada (3,3)): DAWSON (7,4) e GUARD SPEC. (17,6). Voltar pela mesma escada (3,3). Fazer esse desvio ANTES de
começar a empurrar a pedra, porque trocar de andar devolve a pedra a (32,5).
Empurrões (verificados tile a tile):
1. De (32,6) empurrar ↑2: pedra em (32,3).
2. De (33,3) empurrar ←22: pedra em (10,3).
3. De (10,2) empurrar ↓1: pedra em (10,4).
4. De (11,4) empurrar ←4: pedra em (6,4).
5. De (6,3) empurrar ↓3: pedra em (6,7).
6. De (5,7) empurrar →1: pedra em (7,7) = interruptor. A barreira (12,12)/(12,13) some.
Caminho para o buraco: (5,7) → norte até (5,4) → leste por y=4/y=3 até (29,3) → sul x=29 até (29,8) → (25,8) →
degraus (25,7) → platô (25,6) → oeste por y=6 até (16,6) → sul x=16 até (16,12) → oeste por y=12, passando (12,12),
até (10,12) → (10,11) → oeste até (4,11) → degraus (4,12) → sul x=4 até (4,17) (COLBY vê (5–9,17)) → (5,17) → (5,19)
→ leste por y=19 até (21,19) → (21,18) → leste por y=18 até (32,18) → empurrar →1: a pedra (33,18) cai no buraco
(34,18) → pisar em (34,18) e cair no 2F em (34,19).
A pedra (19,15) não sai do lugar pelo norte (bloqueio de direção) e a (35,13) não é necessária.

### Victory Road 2F leste — pedra que caiu (33,19) → interruptor (14,19)
1. De (34,19) empurrar ←19 seguidos (andar 1 para a esquerda entre cada empurrão): pedra em (14,19) = interruptor.
   A barreira (33,16)/(33,17) some.
2. Leste por y=19 até (23,19) → degraus (23,18) → (23,17) → leste por y=17, passando (33,17), até a escada (36,17).
3. 3F (chegada (39,17)): norte pela coluna x=40 (ou x=36) até y=11 → escada (37,10). Evitar (38,14)/(39,14) se não
   quiser a dupla RAY & TYRA.
4. 2F (chegada (38,9)): tutor (40,9). Saída: seta em (48,12) → Rota 23 (18,28).

## Dicas para jogar bem
- Nível: rival 45–53, Victory Road 40–48 e a Elite dos 4 logo depois. Chegar com o time em ~52+ e o bolso com
  FULL RESTORE/REVIVE/MAX POTION. ESCAPE ROPE ou DIG tiram da caverna, mas sair para a Rota 23 zera os quebra-cabeças.
- O tutor de DOUBLE-EDGE (2F) é uso único: ensinar ao Pokémon que vai ficar no time final.
- A luta antiga do rival na Rota 22 (TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE), se não foi feita no início do jogo, não
  acontece mais (a variável pula para 3 com a vitória sobre o GIOVANNI).
- Itens que exigem HM: tudo da Rota 23 entre y=117 e y=83 (inclusive MAX ETHER da ilha) só com SURF. TM02/RARE
  CANDY só com STRENGTH. GUARD SPEC. só pelo desvio noroeste. Os escondidos precisam de botão A (ITEMFINDER ajuda).
- Pescar/surfar na Rota 23 rende POLIWHIRL e PSYDUCK. Na grama, PRIMEAPE/FEAROW/ARBOK (FireRed).
- Depois de chegar ao Indigo Plateau, a Rota 23 norte e a Victory Road continuam acessíveis para voltar a treinar:
  a saída (18,28) da Rota 23 leva direto ao 2F leste.
