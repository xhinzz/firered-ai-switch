# Seção 11 — Saffron City, Silph Co., Fighting Dojo e Saffron Gym
Marcos do roteiro cobertos: silph, dojo, sabrina; novo: tm29_mr_psychic, novo: tutor_thunder_wave, novo: tutor_mimic
Mapas: MAP_ROUTE7_EAST_ENTRANCE, MAP_ROUTE5_SOUTH_ENTRANCE, MAP_ROUTE6_NORTH_ENTRANCE, MAP_ROUTE8_WEST_ENTRANCE, MAP_SAFFRON_CITY, MAP_SAFFRON_CITY_CONNECTION, MAP_SAFFRON_CITY_POKEMON_CENTER_1F, MAP_SAFFRON_CITY_POKEMON_CENTER_2F, MAP_SAFFRON_CITY_MART, MAP_SAFFRON_CITY_MR_PSYCHICS_HOUSE, MAP_SAFFRON_CITY_DOJO, MAP_SILPH_CO_1F, MAP_SILPH_CO_ELEVATOR, MAP_SILPH_CO_5F, MAP_SILPH_CO_9F, MAP_SILPH_CO_2F, MAP_SILPH_CO_3F, MAP_SILPH_CO_4F, MAP_SILPH_CO_6F, MAP_SILPH_CO_7F, MAP_SILPH_CO_8F, MAP_SILPH_CO_10F, MAP_SILPH_CO_11F, MAP_SAFFRON_CITY_COPYCATS_HOUSE_1F, MAP_SAFFRON_CITY_COPYCATS_HOUSE_2F, MAP_SAFFRON_CITY_HOUSE, MAP_SAFFRON_CITY_GYM, MAP_SAFFRON_CITY_POKEMON_TRAINER_FAN_CLUB

## Passo a passo
1. **Entrar em Saffron com o TEA.** Saffron só tem entrada pelas 4 portarias: Rota 7 → MAP_ROUTE7_EAST_ENTRANCE
   (gatilho na coluna x=6, y=4..6), Rota 8 → MAP_ROUTE8_WEST_ENTRANCE (x=6, y=4..6), Rota 5 → MAP_ROUTE5_SOUTH_ENTRANCE
   (linha y=5, x=3..5), Rota 6 → MAP_ROUTE6_NORTH_ENTRANCE (linha y=5, x=3..5). Sem TEA o guarda empurra o jogador de
   volta. Com o TEA (FLAG_GOT_TEA) basta pisar no gatilho: o TEA é consumido e VAR_MAP_SCENE_ROUTE5_ROUTE6_ROUTE7_ROUTE8_GATES
   vira 1, abrindo as QUATRO portarias de vez. MAP_SAFFRON_CITY_CONNECTION é só o muro visto das rotas (não se entra nele).
   Chegadas em MAP_SAFFRON_CITY: da Rota 7 em (8,27); da Rota 8 em (58,27); da Rota 5 em (34/35,5); da Rota 6 em (34/35,46).
2. **Saffron ocupada pela Team Rocket.** Grunts parados bloqueiam portas até Giovanni cair na Silph (FLAG_HIDE_SAFFRON_ROCKETS):
   (22,15) na porta da Copycat's house (22,14); (27,22) na porta da casa (27,21); (46,13) na porta do Saffron Gym (46,12).
   Abertos desde já: Pokémon Center (porta (24,38)), Mart (40,21), Mr. Psychic (43,38), Fighting Dojo (40,12), Fan Club (47,21).
3. **Pokémon Center** MAP_SAFFRON_CITY_POKEMON_CENTER_1F (porta (24,38)): vira ponto de retorno. Mart em (40,21).
4. **TM29 (PSYCHIC)**: MAP_SAFFRON_CITY_MR_PSYCHICS_HOUSE (porta (43,38)). Falar com Mr. Psychic em (7,4) (ex.: de (7,5)
   olhando para cima). Dá a TM29 sem condição (precisa de espaço na bolsa).
5. **Fighting Dojo** MAP_SAFFRON_CITY_DOJO (porta (40,12)) — já está aberto, não precisa da Silph. Ver "Lutas" e
   "Quebra-cabeças". Vencer o KARATE MASTER e escolher UMA Poké Ball: HITMONLEE (5,3) ou HITMONCHAN (7,3), Nv25.
6. **Silph Co. fechada até a Pokémon Tower.** Sem FLAG_RESCUED_MR_FUJI (salvar o Mr. Fuji no topo da torre) o script
   põe o grunt-segurança em (33,31), na frente da porta (33,30). Depois de salvar o Fuji ele fica em (34,31), dormindo,
   e a porta fica livre. Entrar: MAP_SILPH_CO_1F (chega em (8,20)).
7. **Silph 1F → elevador → 5F.** O elevador funciona desde o começo e vai a qualquer andar (1F–11F). Porta do elevador
   em (22,3) no 1F. Dentro (MAP_SILPH_CO_ELEVATOR): painel em (0,2) → ficar em (0,3) olhando para cima, apertar A,
   escolher o andar; sair andando para baixo pelo tile (2,5).
8. **5F: pegar o CARD KEY** (truque do painel). No 5F, ir para oeste pelo corredor y=5 até as colunas x=9..10 e descer até
   (10,19). Não pisar no painel (15,7). O corredor sul até o CARD KEY é fechado pelos grunts parados em (9,21) e (35,7);
   a única entrada é o painel (10,20): pisar nele → MAP_SILPH_CO_9F (22,18); dar um passo para (21,18) e voltar para
   (22,18) → volta ao 5F em (10,20), agora do lado de dentro. Andar para leste pelas linhas y=20/21 até (21,21) e pegar
   o CARD KEY em (22,21) olhando para a direita. A partir daqui toda porta-barreira da Silph abre: ficar de frente para
   ela e apertar A (abre para sempre). Lista das portas em "Quebra-cabeças".
9. **Coleta com o CARD KEY** (opcional, 100%): ver "Itens" — tudo se alcança pelo elevador + portas. Bom momento:
   9F tem uma moça (2,16) que cura o time de graça enquanto a Rocket estiver no prédio (porta 2 do 9F).
10. **3F → painel central → 7F (rival).** Elevador até o 3F (sai em (22,3)). Descer o corredor x=22..25; o grunt
    TRAINER_TEAM_ROCKET_GRUNT_25 em (25,9) olha para o corredor (luta praticamente forçada). Em (22,12) olhando para
    oeste, abrir a porta 2 (tiles x=20..21, y=11..13). Na sala central pisar no painel (13,14) → MAP_SILPH_CO_7F (5,4).
11. **7F sala noroeste (só se chega pelo painel do 3F).** Andar para oeste: os gatilhos (2,4)/(2,5) disparam o rival
    (parado em (2,6)) → luta TRAINER_RIVAL_SILPH_SQUIRTLE. Depois ele sai. Falar com o funcionário em (0,7) (de (1,7),
    olhando para a esquerda): dá LAPRAS Nv25 (vai para o PC se o time estiver cheio). Ir para (4,8) e pisar no painel
    (5,8) → MAP_SILPH_CO_11F (2,5).
12. **11F lado oeste → GIOVANNI.** Descer a coluna x=0..2 até y=18; o grunt TRAINER_TEAM_ROCKET_GRUNT_41 em (2,19)
    (olha para cima, visão 5) é inevitável ao cruzar (2,18). REVIVE escondido em (10,18): de (10,19) olhando para cima.
    Em (5,18) ou (6,18) olhando para cima, abrir a porta (tiles x=5..6, y=16..17). Subir até (5,15)/(6,15): gatilho →
    GIOVANNI vem até o jogador → TRAINER_BOSS_GIOVANNI_2.
13. **Depois de vencer Giovanni:** todos os Rockets e cientistas da Silph somem (inclusive os não enfrentados) e os de
    Saffron também; civis aparecem. Falar com o presidente em (9,9) → MASTER BALL (precisa de espaço). Sair: ESCAPE ROPE
    funciona na Silph; ou voltar pelos painéis 11F (2,5) → 7F, 7F (5,4) → 3F e elevador.
14. **Agora abertos:** Saffron Gym (46,12), Copycat's house (22,14), casa (27,21).
15. **Copycat** (MAP_SAFFRON_CITY_COPYCATS_HOUSE_1F → escada (10,2) → 2F): menina em (9,6). Com uma POKé DOLL na bolsa
    (compra em MAP_CELADON_CITY_DEPARTMENT_STORE_4F) ela ensina MIMIC uma única vez e fica com a POKé DOLL. Não dá TM no
    FireRed. NUGGET escondido em (2,1) do 2F: de (2,2) olhando para cima.
16. **Saffron Gym** MAP_SAFFRON_CITY_GYM: labirinto de painéis (rota exata em "Quebra-cabeças"). Vencer SABRINA (14,11)
    → MARSH BADGE (FLAG_BADGE06_GET: ROCK SMASH fora da batalha e obediência até Nv70) + TM04 (CALM MIND).
17. Próximo destino: Fuchsia (Cycling Road a oeste de Celadon, ou Rotas 12–15 a partir de Lavender), se ainda não foi.

## Lutas obrigatórias
### Rival — TRAINER_RIVAL_SILPH_SQUIRTLE
- Onde: MAP_SILPH_CO_7F, gatilho de piso (2,4) ou (2,5); rival em (2,6). Só se chega pelo painel 3F (13,14) (exige CARD KEY).
- Time: PIDGEOT Nv37 [WING ATTACK, FEATHERDANCE, QUICK ATTACK, WHIRLWIND]; GROWLITHE Nv38 [FLAME WHEEL, TAKE DOWN, ROAR,
  LEER]; EXEGGCUTE Nv35 [CONFUSION, HYPNOSIS, LEECH SEED, STUN SPORE]; ALAKAZAM Nv35 [FUTURE SIGHT, CALM MIND, REFLECT,
  RECOVER]; BLASTOISE Nv40 [WATER GUN, BITE, RAPID SPIN, PROTECT]. Sem itens. (Golpes padrão por nível — conferir.)
- Tipos que funcionam: Elétrico/Grama no BLASTOISE (CHARIZARD é fraco a ele); Elétrico/Gelo/Pedra no PIDGEOT;
  Água/Terra/Pedra no GROWLITHE; Fogo/Voador no EXEGGCUTE; ataques físicos fortes ou Dark/Bug/Ghost no ALAKAZAM.
- Nível recomendado do time: 40+.

### Team Rocket Grunt — TRAINER_TEAM_ROCKET_GRUNT_25
- Onde: MAP_SILPH_CO_3F (25,9), olhando para a esquerda, visão 3 — cobre o corredor que leva à porta da sala central.
- Time: RATICATE Nv28; HYPNO Nv28; RATICATE Nv28.
- Tipos que funcionam: Lutador nos RATICATE; Dark/Ghost/Bug no HYPNO. Nível: 35+.

### Team Rocket Grunt — TRAINER_TEAM_ROCKET_GRUNT_41
- Onde: MAP_SILPH_CO_11F (2,19), olhando para cima, visão 5; é preciso cruzar (2,18) para chegar à porta da diretoria.
- Time: CUBONE Nv32; DROWZEE Nv32; MAROWAK Nv32.
- Tipos que funcionam: Água/Grama nos CUBONE/MAROWAK; Dark/Ghost/Bug no DROWZEE. Nível: 38+.

### GIOVANNI — TRAINER_BOSS_GIOVANNI_2
- Onde: MAP_SILPH_CO_11F, gatilho (5,15)/(6,15) logo após a porta da diretoria; Giovanni começa em (6,11).
- Time: NIDORINO Nv37 [HORN ATTACK, POISON STING, FURY ATTACK]; KANGASKHAN Nv35 [FAKE OUT, MEGA PUNCH, RAGE]; RHYHORN Nv37
  [ROCK BLAST, FURY ATTACK, SCARY FACE]; NIDOQUEEN Nv41 [BODY SLAM, DOUBLE KICK, POISON STING]. Sem itens.
- Tipos que funcionam: Terra (TM28 DIG, que o CHARIZARD aprende) em NIDORINO, RHYHORN e NIDOQUEEN; Água no RHYHORN (4x) e
  na NIDOQUEEN; Psíquico nos dois Nidos; Lutador no KANGASKHAN. Fogo/Voador vai mal contra RHYHORN.
- Nível recomendado do time: 40–42.

### KARATE MASTER — TRAINER_BLACK_BELT_KOICHI (marco dojo)
- Onde: MAP_SAFFRON_CITY_DOJO (6,5), olhando para baixo, visão 2; os gatilhos (5,5)/(7,5) também o fazem virar.
- Time: HITMONLEE Nv37 @BLACK BELT; HITMONCHAN Nv37 @BLACK BELT (golpes padrão: HI JUMP KICK; SKY UPPERCUT, FIRE/ICE/
  THUNDERPUNCH — conferir).
- Tipos que funcionam: Psíquico e Voador (CHARIZARD com WING ATTACK/golpes voadores). Evitar Normal/Pedra/Gelo/Dark.
- Nível recomendado do time: 38+.

### SABRINA — TRAINER_LEADER_SABRINA
- Onde: MAP_SAFFRON_CITY_GYM (14,11), sala central; falar de (14,12).
- Time: KADABRA Nv38 [PSYBEAM, REFLECT, FUTURE SIGHT, CALM MIND]; MR MIME Nv37 [BARRIER, PSYBEAM, BATON PASS, CALM MIND];
  VENOMOTH Nv38 [PSYBEAM, GUST, LEECH LIFE, SUPERSONIC]; ALAKAZAM Nv43 [PSYCHIC, RECOVER, FUTURE SIGHT, CALM MIND].
  Itens: HYPER POTION x2, FULL HEAL.
- Tipos que funcionam: Bug/Ghost/Dark; ataques físicos fortes (a defesa especial deles é alta, e CALM MIND acumula);
  Fogo/Voador/Pedra/Psíquico no VENOMOTH. Evitar Lutador e Veneno. FUTURE SIGHT cai 2 turnos depois.
- Nível recomendado do time: 43–45.

## Treinadores opcionais relevantes
Todos os da Silph (Rockets, cientistas e o Juggler) somem quando Giovanni perde — enfrentar antes para EXP/dinheiro.
- MAP_SILPH_CO_2F: TRAINER_TEAM_ROCKET_GRUNT_24 (29,12) 5 Pokémon Nv25; TRAINER_SCIENTIST_JERRY (28,18) Nv28;
  TRAINER_TEAM_ROCKET_GRUNT_23 (20,14) Nv29; TRAINER_SCIENTIST_CONNOR (5,19) Nv26 (sala sudoeste).
- MAP_SILPH_CO_3F: TRAINER_SCIENTIST_JOSE (4,12) Nv29 (sala oeste, porta 1).
- MAP_SILPH_CO_4F: TRAINER_TEAM_ROCKET_GRUNT_27 (33,16) Nv28; TRAINER_TEAM_ROCKET_GRUNT_26 (10,19) Nv29;
  TRAINER_SCIENTIST_RODNEY (14,8) ELECTRODE Nv33 (sala via porta 2 ou painel 6F (2,6)).
- MAP_SILPH_CO_5F: TRAINER_TEAM_ROCKET_GRUNT_29 (35,7) HYPNO Nv33; TRAINER_JUGGLER_DALTON (23,13) Nv29;
  TRAINER_SCIENTIST_BEAU (11,6) Nv26; TRAINER_TEAM_ROCKET_GRUNT_28 (9,21) ARBOK Nv33 (ao lado do painel (10,20)).
- MAP_SILPH_CO_6F: TRAINER_TEAM_ROCKET_GRUNT_30 (21,5) Nv29; TRAINER_SCIENTIST_TAYLOR (9,11) 5 Pokémon Nv25;
  TRAINER_TEAM_ROCKET_GRUNT_31 (18,17) Nv28.
- MAP_SILPH_CO_7F: TRAINER_TEAM_ROCKET_GRUNT_33 (24,5) Nv29 (na frente da porta 2); TRAINER_TEAM_ROCKET_GRUNT_35 (13,4)
  Nv26; TRAINER_SCIENTIST_JOSHUA (3,13) Nv29; TRAINER_TEAM_ROCKET_GRUNT_34 (24,15) Nv29 (sala sudeste, painel 5F (33,5)).
- MAP_SILPH_CO_8F: TRAINER_TEAM_ROCKET_GRUNT_32 (28,5) Nv26; TRAINER_TEAM_ROCKET_GRUNT_36 (10,17) Nv28;
  TRAINER_SCIENTIST_PARKER (9,4) Nv29.
- MAP_SILPH_CO_9F: TRAINER_SCIENTIST_ED (26,16) Nv28; TRAINER_TEAM_ROCKET_GRUNT_38 (15,18) Nv28 (fim do corredor da
  porta 2); TRAINER_TEAM_ROCKET_GRUNT_37 (1,6) Nv28 (sala noroeste: painel 3F (2,14) ou porta 1).
- MAP_SILPH_CO_10F: TRAINER_SCIENTIST_TRAVIS (2,7) Nv29; TRAINER_TEAM_ROCKET_GRUNT_39 (0,13) MACHOKE Nv33.
- MAP_SILPH_CO_11F: TRAINER_TEAM_ROCKET_GRUNT_40 (16,12) 5 Pokémon Nv25 (lado leste, corredor do ZINC).
- MAP_SAFFRON_CITY_DOJO (todos com BLACK BELT; visão 7, cobrem o salão inteiro — na prática forçados ao subir pelo meio):
  TRAINER_BLACK_BELT_HIDEKI (1,10) MACHOP/MACHOKE Nv32; TRAINER_BLACK_BELT_HITOSHI (11,10) MACHOP/MANKEY/PRIMEAPE Nv31;
  TRAINER_BLACK_BELT_MIKE (1,8) MANKEY x2/PRIMEAPE Nv31; TRAINER_BLACK_BELT_AARON (11,8) PRIMEAPE Nv36.
- MAP_SAFFRON_CITY_GYM (todos olhando para baixo, visão 3; todos evitáveis na rota mínima):
  TRAINER_PSYCHIC_CAMERON (24,18) SLOWPOKE x2/SLOWBRO Nv33 [sala SE]; TRAINER_PSYCHIC_TYRON (24,10) MR MIME/KADABRA Nv34
  [L]; TRAINER_PSYCHIC_JOHAN (24,2) KADABRA x2/SLOWPOKE/MR MIME Nv31 [NE]; TRAINER_CHANNELER_AMANDA (14,2) GASTLY/HAUNTER
  Nv34 [N]; TRAINER_PSYCHIC_PRESTON (4,2) SLOWBRO Nv38 [NO]; TRAINER_CHANNELER_STACY (4,10) HAUNTER Nv38 [O];
  TRAINER_CHANNELER_TASHA (4,18) GASTLY x2/HAUNTER Nv33 [SO].

## Itens
"de (x,y) ↑/↓/←/→" = tile onde ficar e direção para apertar A. "porta N" = barreira que o CARD KEY abre.
### MAP_SAFFRON_CITY_MR_PSYCHICS_HOUSE
- (7,4) TM29 (PSYCHIC) — presente do Mr. Psychic.
### MAP_SAFFRON_CITY_COPYCATS_HOUSE_2F (só depois da Silph)
- (2,1) NUGGET — escondido, de (2,2) ↑.
### MAP_SILPH_CO_2F
- (11,21) ULTRA BALL — escondido, de (11,20) ↓ ou (10,21) →. Sala sudoeste: porta 2 (de (5,14)/(6,14) ↓) ou sem chave
  pelo painel 6F (29,5) → 2F (7,19).
### MAP_SILPH_CO_3F
- (8,10) HYPER POTION — visível, sala oeste (porta 1, de (11,12) ←); pegar de (7,10) → ou (8,11) ↑.
- (34,18) PROTEIN — escondido, de (34,19) ↑ (canto sudeste; sem chave, pela parte de baixo ou painel (29,14)→(32,20)).
### MAP_SILPH_CO_4F
- (3,11) MAX REVIVE, (4,12) ESCAPE ROPE, (2,13) FULL HEAL — visíveis, sala noroeste (porta 1, de (3,18)/(4,18) ↑);
  de (3,12) ↑ = MAX REVIVE, de (3,12) → = ESCAPE ROPE, de (3,13) ← = FULL HEAL.
- (30,18) TM41 (TORMENT) — visível, sem chave; de (30,19) ↑.
- (35,20) IRON — escondido, de (35,19) ↓ ou (34,20) →.
### MAP_SILPH_CO_5F
- (22,21) CARD KEY — key item, visível; de (21,21) → (só pelo truque do painel (10,20), passo 8).
- (4,9) PROTEIN — visível, sala noroeste (porta 1, de (9,9)/(9,10) ←).
- (1,18) TM01 (FOCUS PUNCH) — visível, sala sudoeste: porta 2 (de (9,18)/(9,19) ←) ou sem chave pelo painel 3F (3,20) →
  5F (2,20); pegar de (0,18) → ou (1,19) ↑.
- (32,9) PP UP — escondido, sem chave; de (32,10) ↑ ou (31,9) →.
- (13,16) ELIXIR — escondido, salinha central (porta 3, de (20,13)/(20,14) ←); de (13,17) ↑ ou (14,16) ←.
### MAP_SILPH_CO_6F
- (2,14) HP UP, (1,17) X SPECIAL — visíveis, sala sudoeste (porta, de (7,15)/(7,16) ←); de (3,14) ← e de (1,18) ↑.
- (1,8) CARBOS — escondido, sem chave; de (1,9) ↑ ou (2,8) ←.
### MAP_SILPH_CO_7F
- (30,11) TM08 (BULK UP) e (22,11) ZINC escondido — sala centro-leste (porta 2, de (24,6)/(25,6) ↓, ou porta 3 de
  (25,15)/(26,15) ↑); TM08 de (29,11) →; ZINC de (22,12) ↑ ou (23,11) ←.
- (0,12) CALCIUM — visível, sala sudoeste, sem chave; de (1,12) ← ou (0,13) ↑.
### MAP_SILPH_CO_8F
- (24,8) IRON — visível, sala leste (entra pelo corredor de baixo, x=24..25); de (24,9) ↑.
- (29,10) NUGGET — escondido, mesma sala; de (29,11) ↑ ou (28,10) →.
### MAP_SILPH_CO_9F
- (11,14) MAX POTION e (5,8) CALCIUM — escondidos, área oeste (porta 2, de (14,16)/(14,17) ←); MAX POTION de (11,15) ↑;
  CALCIUM de (5,9) ↑ ou (6,8) ←.
### MAP_SILPH_CO_10F (tudo sem chave, pelo elevador)
- (2,15) ULTRA BALL de (1,15) →; (5,15) CARBOS de (6,15) ←; (3,17) RARE CANDY de (3,18) ↑ — visíveis, canto sudoeste.
- (9,9) HP UP — escondido; de (9,10) ↑ ou (10,9) ←.
### MAP_SILPH_CO_11F
- (16,18) ZINC — visível, lado leste (elevador), sem chave; de (16,17) ↓ ou (15,18) →.
- (10,18) REVIVE — escondido, lado oeste; de (10,19) ↑.
- (9,9) MASTER BALL — presente do presidente após vencer Giovanni.
### MAP_SAFFRON_CITY_GYM
- TM04 (CALM MIND) — presente da SABRINA junto com a MARSH BADGE.

## NPCs importantes
- MAP_ROUTE5_SOUTH_ENTRANCE / MAP_ROUTE6_NORTH_ENTRANCE / MAP_ROUTE7_EAST_ENTRANCE / MAP_ROUTE8_WEST_ENTRANCE: guardas;
  aceitam o TEA (consumido) e liberam as quatro portarias.
- MAP_SAFFRON_CITY (34,31)/(33,31): grunt-segurança da Silph; na frente da porta até salvar o Mr. Fuji.
- MAP_SAFFRON_CITY_MART (2,3): vende GREAT BALL, HYPER POTION, REVIVE, FULL HEAL, ESCAPE ROPE, MAX REPEL.
- MAP_SAFFRON_CITY_MR_PSYCHICS_HOUSE (7,4): Mr. Psychic, TM29 (PSYCHIC).
- MAP_SILPH_CO_2F (10,4): tutora de THUNDER WAVE (uma vez só, a qualquer momento, inclusive depois da Silph). Sala
  noroeste: sem chave pelo painel 3F (33,5) → 2F (2,6), ou porta 1 do 2F (de (5,10)/(6,10) ↑).
- MAP_SILPH_CO_7F (0,7): funcionário que dá LAPRAS Nv25 (uma vez).
- MAP_SILPH_CO_9F (2,16): moça que cura o time (só enquanto a Rocket ocupa o prédio).
- MAP_SILPH_CO_11F (9,9): presidente, MASTER BALL após Giovanni.
- MAP_SAFFRON_CITY_COPYCATS_HOUSE_2F (9,6): Copycat; com POKé DOLL ensina MIMIC uma vez e fica com a boneca.
- MAP_SAFFRON_CITY_DOJO (5,3)/(7,3): Poké Balls com HITMONLEE / HITMONCHAN (só uma, após vencer o KARATE MASTER).
- MAP_SAFFRON_CITY_GYM (15,20): Gym Guy (só dicas).
- MAP_SAFFRON_CITY_POKEMON_TRAINER_FAN_CLUB e MAP_SAFFRON_CITY_HOUSE: sem itens/presentes; os fãs do clube só aparecem
  no pós-jogo (conferir). MAP_SAFFRON_CITY_POKEMON_CENTER_2F: Union Room/troca por cabo (ignorar).

## Pokémon disponíveis (FireRed)
### MAP_SAFFRON_CITY e MAP_SILPH_CO_*
- Nenhum selvagem (sem grama nem água em Saffron e na Silph).
### MAP_SILPH_CO_7F
- presente: LAPRAS Nv25 (funcionário em (0,7), após o rival).
### MAP_SAFFRON_CITY_DOJO
- presente: HITMONLEE Nv25 OU HITMONCHAN Nv25 (só um). O outro, para a Pokédex, só cruzando o escolhido com DITTO na
  Day Care da Four Island (nasce TYROGUE; evolui conforme Ataque x Defesa) — conferir.

## Quebra-cabeças
### Silph Co. — portas do CARD KEY (barreiras fechadas até apertar A de frente com o CARD KEY; abrem de vez)
Tiles bloqueados por andar (x,y): 2F porta1 x5-6,y8-9 | porta2 x5-6,y15-16. 3F porta1 x9-10,y11-13 | porta2 x20-21,
y11-13. 4F porta1 x3-4,y16-17 | porta2 x14-15,y11-12. 5F porta1 x7-8,y8-10 | porta2 x7-8,y17-19 | porta3 x18-19,y12-14.
6F x5-6,y14-16. 7F porta1 x11-12,y8-9 (sala sem itens) | porta2 x24-25,y7-8 | porta3 x25-26,y13-14. 8F x5-6,y9-11 (sem
itens). 9F porta1 x2-3,y9-11 | porta2 x12-13,y15-17 | porta3 x21-22,y6-7 e porta4 x21-22,y12-13 (sala vazia).
10F x12-13,y11-12 (sem itens). 11F x5-6,y16-17 (diretoria — obrigatória).
### Silph Co. — painéis de teletransporte (todos de mão dupla)
2F(2,6)↔3F(33,5) | 2F(7,19)↔6F(29,5) | 2F(15,6)↔8F(2,17) | 2F(33,19)↔8F(10,6) | 3F(2,14)↔9F(9,4) | 3F(3,20)↔5F(2,20) |
3F(4,6)↔5F(15,7) | 3F(13,14)↔7F(5,4) | 3F(29,14)↔3F(32,20) | 4F(2,20)↔10F(14,17) | 4F(12,9)↔10F(10,14) |
4F(18,6)↔6F(2,6) | 4F(18,14)↔10F(14,9) | 5F(10,20)↔9F(22,18) | 5F(33,5)↔7F(25,17) | 7F(5,8)↔11F(2,5) | 8F(2,12)↔8F(11,10).
Ao chegar num painel é preciso sair dele e pisar de novo para voltar.
Escadas (sempre no alto do mapa): 1F(31,2)↔2F(30,2), 2F(28,2)↔3F(28,2), 3F(30,2)↔4F(30,2), 4F(28,2)↔5F(28,2),
5F(30,2)↔6F(26,2), 6F(14,2)↔7F(19,2), 7F(27,2)↔8F(28,2), 8F(16,2)↔9F(16,2), 9F(18,2)↔10F(8,2), 10F(6,2)↔11F(7,2).
Portas do elevador: (22,3) em 1F–5F e 8F; (20,3) no 6F; (23,3) no 7F; (24,3) no 9F; (13,3) no 10F e 11F. Atende 1F–11F.
### Silph Co. — caminho mínimo até Giovanni
1F (22,3) elevador → 5F → corredor x=9..10 → painel 5F(10,20) → 9F(22,18) → pisar de novo → 5F(10,20) → CARD KEY (22,21)
→ elevador (22,3) do 5F (ou painel (10,20) → 9F e elevador (24,3)) → 3F → porta 2 de (22,12) → painel 3F(13,14) →
7F(5,4) → rival em (2,4)/(2,5) → painel 7F(5,8) → 11F(2,5) → (5,18) abrir porta ↑ → (5,15) Giovanni → presidente (9,9).
Partes isoladas: a sala noroeste do 7F só tem acesso pelo painel 3F(13,14) (sala central do 3F, atrás da porta 2); o lado
oeste do 11F e a diretoria só pelo painel 7F(5,8). O lado leste do 11F (elevador/escada) não liga com a diretoria.
### Saffron Gym — painéis (sala = grade 3x3: NO/N/NE, O/centro/L, SO/entrada/SE)
Tabela completa: (18,20)[entrada]→(28,23)[SE]; (0,4)[NO]→(20,7)[NE]; (0,7)[NO]→(18,15)[centro]; (0,12)[O]→(28,15)[L];
(0,15)[O]→(8,7)[NO]; (0,20)[SO]→(28,7)[NE]; (0,23)[SO]→(16,7)[N]; (8,4)[NO]→(16,4)[N]; (8,7)[NO]→(0,15)[O];
(8,12)[O]→(12,7)[N]; (8,15)[O]→(8,23)[SO]; (8,20)[SO]→(20,23)[SE]; (8,23)[SO]→(8,15)[O]; (12,4)[N]→(20,15)[L];
(12,7)[N]→(8,12)[O]; (16,4)[N]→(8,4)[NO]; (16,7)[N]→(0,23)[SO]; (18,15)[centro]→(0,7)[NO]; (20,4)[NE]→(20,12)[L];
(20,7)[NE]→(0,4)[NO]; (20,12)[L]→(20,4)[NE]; (20,15)[L]→(12,4)[N]; (20,20)[SE]→(28,4)[NE]; (20,23)[SE]→(8,20)[SO];
(28,4)[NE]→(20,20)[SE]; (28,7)[NE]→(0,20)[SO]; (28,12)[L]→(28,20)[SE]; (28,15)[L]→(0,12)[O]; (28,20)[SE]→(28,12)[L];
(28,23)[SE]→(18,20)[entrada].
Rota mínima (4 painéis, nenhuma luta forçada):
1. Entrada (14,22) → (15,22)…(18,22) → (18,21) → painel (18,20) → chega em (28,23) [SE].
2. (27,23) → (27,22) → oeste pela linha y=22 até (21,22) → (21,21) → (20,21) → painel (20,20) → chega em (28,4) [NE].
   Não pisar em (20,23) nem (28,20).
3. (27,4) → (27,5) → (27,6) → oeste pela linha y=6 até (21,6) → (20,6) → painel (20,7) → chega em (0,4) [NO].
   Linha y=6 fica fora da visão de JOHAN (24,2). Não pisar em (20,4) nem (28,7).
4. (0,5) → (0,6) → painel (0,7) → chega em (18,15) [centro]. Andar até (14,12) e falar com SABRINA (14,11) olhando ↑.
### Fighting Dojo — ordem
Entrar por (6,14) e subir pelo meio: linha y=10 → HIDEKI (1,10) e HITOSHI (11,10); linha y=8 → MIKE (1,8) e AARON
(11,8); depois (6,6) → KARATE MASTER KOICHI (6,5). Depois: (5,4) ↑ = Poké Ball do HITMONLEE (5,3); (7,4) ↑ = HITMONCHAN
(7,3). Responder YES; a outra bola fica e não pode ser pega.

## Dicas para jogar bem
- Ordem: Mr. Psychic e Dojo assim que entrar em Saffron (Dojo não depende da Silph); Silph depois da Pokémon Tower;
  Gym, Copycat e casa (27,21) só depois de Giovanni na Silph.
- Antes da Silph: time ~40, HYPER POTIONs/REVIVEs do Mart de Saffron, espaço no time ou no PC para o LAPRAS, espaço na
  bolsa para MASTER BALL/TMs. A moça do 9F (2,16) cura de graça enquanto a Rocket estiver lá — use antes do 3F/7F/11F.
- Enfrente os Rockets e cientistas antes de Giovanni (somem todos depois). Os itens e a tutora do 2F ficam para sempre.
- TM28 (DIG) no CHARIZARD resolve 3 dos 4 de Giovanni; para o rival leve algo Elétrico/Grama contra o BLASTOISE.
- Guardar a MASTER BALL para um lendário (MEWTWO, os pássaros lendários).
- HITMONLEE (ataque físico, HI JUMP KICK) costuma render mais que HITMONCHAN; os dois só via Dojo + cruzamento.
- MIMIC (Copycat) e THUNDER WAVE (Silph 2F) são de uma vez só: escolher bem o Pokémon (conferir compatibilidade na tela).
- MARSH BADGE libera ROCK SMASH fora da batalha (a HM06 vem depois, em outra seção) e Pokémon trocados até Nv70 obedecem.
- Nada aqui exige HM. ESCAPE ROPE funciona dentro da Silph (não no elevador).
