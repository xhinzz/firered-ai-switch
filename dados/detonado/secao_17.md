# Seção 17 — Indigo Plateau: Elite Four, Campeão, Hall of Fame e National Pokédex
Marcos do roteiro cobertos: liga, novo: national_dex, novo: revanche_liga
Mapas: MAP_INDIGO_PLATEAU_EXTERIOR, MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F, MAP_INDIGO_PLATEAU_POKEMON_CENTER_2F, MAP_POKEMON_LEAGUE_LORELEIS_ROOM, MAP_POKEMON_LEAGUE_BRUNOS_ROOM, MAP_POKEMON_LEAGUE_AGATHAS_ROOM, MAP_POKEMON_LEAGUE_LANCES_ROOM, MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM, MAP_POKEMON_LEAGUE_HALL_OF_FAME, MAP_PALLET_TOWN, MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB

## Passo a passo
1. Chegada: saindo da Victory Road, siga a Rota 23 (MAP_ROUTE23) para o norte até o Indigo Plateau
   (MAP_INDIGO_PLATEAU_EXTERIOR). Os guardas da Rota 23 que conferem as 8 insígnias ficam na seção anterior.
   Ao pisar no exterior o destino INDIGO PLATEAU entra no FLY. A única porta é a do prédio, no tile (11,6).
2. Dentro do prédio (MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F) você entra por (11,16). Assim que entra, o ponto de
   retorno passa a ser este Centro: se perder qualquer luta da Liga, você volta para cá.
   - Enfermeira em (13,10): cura o time (fale com ela pelo balcão).
   - Vendedor em (0,7), virado para a direita (fale com ele pelo balcão): loja da Liga (lista em "NPCs importantes").
   - Escada para o 2F em (1,14): MAP_INDIGO_PLATEAU_POKEMON_CENTER_2F (só salas de link e Union Room, nada para a história).
   - PC do Centro: use para montar o time final antes de entrar (posição: conferir).
3. Prepare tudo antes de seguir (ver checklist em "Dicas para jogar bem"). Depois de cruzar a porta da Liga NÃO
   dá para voltar: a entrada de cada sala se fecha atrás de você, não há enfermeira nem PC, e nas salas não funcionam
   ESCAPE ROPE, DIG nem FLY. A cura entre as lutas é só com itens da mochila.
4. A porta da Liga fica em (4,1), no fundo à esquerda, ao lado da guarda (COOLTRAINER, em (5,3)). Antes do Hall of
   Fame ela só deseja boa sorte e não bloqueia nada. Pise em (4,1) para entrar na sala de LORELEI.
5. MAP_POKEMON_LEAGUE_LORELEIS_ROOM: ao entrar, o personagem anda sozinho 5 passos para cima (de (6,12) até (6,7)) e
   a entrada se fecha. LORELEI fica em (6,5): suba para (6,6) e aperte A virado para cima. A luta só começa ao falar
   com ela. Ao vencer, abre-se a porta do norte em (6,2), que leva à sala de BRUNO. Contorne a LORELEI para chegar lá.
6. MAP_POKEMON_LEAGUE_BRUNOS_ROOM: mesma estrutura. Anda sozinho até (6,7), BRUNO em (6,5), fale com ele de (6,6).
   Ao vencer, abre (6,2), que leva à sala de AGATHA.
7. MAP_POKEMON_LEAGUE_AGATHAS_ROOM: mesma estrutura. AGATHA em (6,5), fale com ela de (6,6). Ao vencer, abre (6,2),
   que leva à sala de LANCE.
8. MAP_POKEMON_LEAGUE_LANCES_ROOM: você entra por (23,13) e o personagem percorre sozinho um corredor comprido
   (cima 2, esquerda 6, baixo 7, esquerda 11, cima 8). Ele para em (6,10) e a entrada se fecha. Não aperte nada durante o
   trajeto. LANCE fica em (6,8): suba para (6,9) e fale com ele. Ao vencer, abre a passagem em (6,5), que leva à sala do
   Campeão.
9. ANTES de pisar em (6,5): cure o time todo com itens e reordene o time (o primeiro da lista é o que entra na luta).
   Na sala do Campeão a luta começa sozinha, sem chance de usar o menu.
10. MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM: você entra por (6,19), anda sozinho 10 passos até (6,9) e o rival (em (6,8))
    começa a luta na hora: TRAINER_CHAMPION_FIRST_SQUIRTLE. Ele aparece com o nome que você escolheu para o rival no
    começo do jogo.
11. Depois da vitória é tudo automático: o Prof. OAK entra, conversa e leva você para o MAP_POKEMON_LEAGUE_HALL_OF_FAME
    (você chega em (5,12) e anda até (5,4), ao lado do OAK em (6,4)). O time é registrado, recebe a fita de campeão e é
    curado, e o jogo SALVA sozinho ("SAVING… DON'T TURN OFF THE POWER."). Não desligue.
12. Créditos: você aparece no MAP_INDIGO_PLATEAU_EXTERIOR, o rival e o OAK saem do prédio (cena automática) e os
    créditos rodam. Só espere, não dá para pular. No fim aparece "THE END" e o jogo reinicia sozinho na tela de título.
13. Na tela de título escolha CONTINUE. Se aparecer o resumo da jornada ("Previously on your quest..."), aperte B para
    pular. Você surge em Pallet Town (MAP_PALLET_TOWN), na frente de casa, em (6,8). Daqui em diante o jogo está
    "zerado" (FLAG_SYS_GAME_CLEAR).
14. Cena do OAK (automática, na primeira vez que estiver em Pallet depois do Hall of Fame): ele vem até você
    e pede para ver a Pokédex.
    - Se você já esteve na One Island E tem pelo menos 60 espécies de Kanto CAPTURADAS (conta o "OWNED" da Pokédex de
      Kanto; "SEEN" não conta), ele diz "Come. Follow me." e leva você ao laboratório
      (MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB). Lá o rival aparece e o OAK atualiza as duas Pokédex: a sua vira NATIONAL
      POKéDEX (mensagem "...POKéDEX was upgraded!").
    - Com menos de 60 capturados ele elogia o esforço e vai embora. Sem ter ido à One Island ele só comenta a viagem e
      vai embora. Nos dois casos, depois que cumprir as condições, vá ao laboratório e fale com o OAK em (6,3): ele
      avalia a Pokédex e, com 60 ou mais capturados e a One Island já visitada, faz a mesma cena da NATIONAL POKéDEX.
    - Não precisa de RUBY nem SAPPHIRE. É o contrário: o Celio (MAP_ONE_ISLAND_POKEMON_CENTER_1F) só pede o RUBY (começo
      da parte 2 das Sevii) DEPOIS que você tem a NATIONAL POKéDEX.
15. Depois do Hall of Fame:
    - A Liga é zerada (portas fechadas de novo, Campeão liberado para nova luta) e pode ser refeita com os MESMOS times
      enquanto você não tiver a NATIONAL POKéDEX. É boa fonte de EXP e dinheiro (cerca de ₽29.100 por volta completa).
    - Com a NATIONAL POKéDEX, mas antes de entregar a SAPPHIRE ao Celio, a Liga fica FECHADA: a guarda se posiciona em
      (4,2), na frente da porta, e diz que LORELEI está ausente.
    - Depois de entregar a SAPPHIRE ao Celio (MAP_ONE_ISLAND_POKEMON_CENTER_1F; liga FLAG_SYS_CAN_LINK_WITH_RS), a Liga
      reabre com os times de revanche (ver "Revanche" abaixo). Esse mesmo evento também libera o guarda da Cerulean Cave.
    - Novos NPCs aparecem no 1F do Indigo (FLAG_HIDE_POSTGAME_GOSSIPERS liberada): BLACK BELT em (23,13), COOLTRAINER em
      (16,15) e o POKéMON JOURNAL em (22,9)/(23,9). Só conversa.

## Lutas obrigatórias
Todos os membros da Elite Four usam 2 FULL RESTORE. O Campeão usa 4. Lute com o time cheio e troque de Pokémon pelo
tipo. Prêmios aproximados: LORELEI ₽5.400, BRUNO ₽5.600, AGATHA ₽5.800, LANCE ₽6.000, Campeão ₽6.300.

### LORELEI — TRAINER_ELITE_FOUR_LORELEI
- Onde: MAP_POKEMON_LEAGUE_LORELEIS_ROOM, LORELEI em (6,5) (falar de (6,6))
- Time: DEWGONG Nv52 [ICE BEAM, SURF, HAIL, SAFEGUARD]; CLOYSTER Nv51 [SPIKES, PROTECT, HAIL, DIVE];
  SLOWBRO Nv52 [ICE BEAM, SURF, AMNESIA, YAWN]; JYNX Nv54 [ICE PUNCH, DOUBLE SLAP, LOVELY KISS, ATTRACT];
  LAPRAS Nv54 @SITRUS BERRY [CONFUSE RAY, ICE BEAM, SURF, BODY SLAM]; itens: FULL RESTORE x2
- Tipos que funcionam: ELECTRIC é o melhor contra quatro dos cinco (todos Water menos JYNX). FIGHTING, ROCK e GRASS
  também acertam DEWGONG, CLOYSTER e LAPRAS em dobro. JYNX (Ice/Psychic) apanha em dobro de FIRE, ROCK, STEEL, GHOST,
  DARK e BUG: o FLAMETHROWER do CHARIZARD resolve.
- Ameaças: LOVELY KISS do JYNX (sono) e ATTRACT (paralisa machos de paixão). Leve FULL HEAL/AWAKENING ou derrube o JYNX
  rápido com fogo. YAWN do SLOWBRO dá sono no turno seguinte. Troque de Pokémon para não dormir. CONFUSE RAY do LAPRAS.
  O DEWGONG tem THICK FAT (fogo e gelo causam metade). O CLOYSTER tem Defesa física altíssima: use golpe especial
  (ELECTRIC). O SLOWBRO com AMNESIA aguenta golpes especiais: derrube antes ou use golpe físico forte. SURF e DIVE causam
  dano dobrado no CHARIZARD.
- Nível recomendado do time: 55+ (ELECTRIC no 50+ já basta aqui).

### BRUNO — TRAINER_ELITE_FOUR_BRUNO
- Onde: MAP_POKEMON_LEAGUE_BRUNOS_ROOM, BRUNO em (6,5) (falar de (6,6))
- Time: ONIX Nv51 [EARTHQUAKE, ROCK TOMB, IRON TAIL, ROAR]; HITMONCHAN Nv53 [SKY UPPERCUT, MACH PUNCH, ROCK TOMB,
  COUNTER]; HITMONLEE Nv53 [MEGA KICK, FORESIGHT, BRICK BREAK, FACADE]; ONIX Nv54 [DOUBLE EDGE, EARTHQUAKE, IRON TAIL,
  SAND TOMB]; MACHAMP Nv56 @SITRUS BERRY [CROSS CHOP, BULK UP, SCARY FACE, ROCK TOMB]; itens: FULL RESTORE x2
- Tipos que funcionam: contra os ONIX (Rock/Ground), WATER e GRASS causam dano x4, e ICE, FIGHTING e GROUND x2. A Defesa
  Especial deles é baixíssima: SURF ou ICE BEAM do LAPRAS derruba de um golpe. Contra HITMONCHAN, HITMONLEE e MACHAMP
  (Fighting), PSYCHIC e FLYING causam x2.
- Ameaças: ROCK TOMB (ONIX, HITMONCHAN e MACHAMP) causa x4 no CHARIZARD. Use o CHARIZARD (WING ATTACK/AERIAL ACE) só
  contra os lutadores e com HP cheio. COUNTER do HITMONCHAN devolve em dobro o dano físico recebido: prefira golpe especial
  (PSYCHIC). MACHAMP tem GUTS (fica mais forte com status): não queime nem envenene ele. Usa BULK UP. LAPRAS sofre x2 de
  golpes Fighting: não o deixe contra os lutadores.
- Nível recomendado do time: 55+.

### AGATHA — TRAINER_ELITE_FOUR_AGATHA
- Onde: MAP_POKEMON_LEAGUE_AGATHAS_ROOM, AGATHA em (6,5) (falar de (6,6))
- Time: GENGAR Nv54 [SHADOW PUNCH, CONFUSE RAY, TOXIC, DOUBLE TEAM]; GOLBAT Nv54 [CONFUSE RAY, POISON FANG, AIR CUTTER,
  BITE]; HAUNTER Nv53 [HYPNOSIS, DREAM EATER, CURSE, MEAN LOOK]; ARBOK Nv56 [SLUDGE BOMB, SCREECH, IRON TAIL, BITE];
  GENGAR Nv58 @SITRUS BERRY [SHADOW BALL, SLUDGE BOMB, HYPNOSIS, NIGHTMARE]; itens: FULL RESTORE x2
- Tipos que funcionam: PSYCHIC causa x2 em TODOS. GHOST e DARK causam x2 em GENGAR e HAUNTER. ELECTRIC, ICE e ROCK causam
  x2 no GOLBAT. GROUND causa x2 só no ARBOK: GENGAR e HAUNTER têm LEVITATE e GOLBAT voa, então EARTHQUAKE não acerta os três.
  NORMAL e FIGHTING não acertam GENGAR nem HAUNTER. O FLAMETHROWER do CHARIZARD é neutro em todos, e nenhum golpe dela
  é super efetivo contra ele: é uma boa escolha aqui.
- Ameaças: HYPNOSIS + DREAM EATER (HAUNTER) e HYPNOSIS + NIGHTMARE (GENGAR Nv58) fazem o Pokémon dormir e drenam vida.
  Acorde na hora com FULL HEAL/AWAKENING ou troque. MEAN LOOK do HAUNTER impede trocar e CURSE tira 1/4 do HP por turno: mate
  o HAUNTER primeiro com golpe forte. TOXIC e CONFUSE RAY do GENGAR Nv54 e do GOLBAT. SCREECH do ARBOK (derruba Defesa).
  ARBOK tem INTIMIDATE.
- Nível recomendado do time: 56+.

### LANCE — TRAINER_ELITE_FOUR_LANCE
- Onde: MAP_POKEMON_LEAGUE_LANCES_ROOM, LANCE em (6,8) (falar de (6,9), depois do corredor automático)
- Time: GYARADOS Nv56 [HYPER BEAM, DRAGON RAGE, TWISTER, BITE]; DRAGONAIR Nv54 [HYPER BEAM, SAFEGUARD, DRAGON RAGE,
  OUTRAGE]; DRAGONAIR Nv54 [HYPER BEAM, SAFEGUARD, THUNDER WAVE, OUTRAGE]; AERODACTYL Nv58 [HYPER BEAM, ANCIENT POWER,
  WING ATTACK, SCARY FACE]; DRAGONITE Nv60 @SITRUS BERRY [HYPER BEAM, SAFEGUARD, OUTRAGE, WING ATTACK];
  itens: FULL RESTORE x2
- Tipos que funcionam: ICE é a chave. Causa x4 no DRAGONITE e x2 nos DRAGONAIR e no AERODACTYL. Use o ICE BEAM do LAPRAS
  (aprende sozinho no Nv31) ou do ARTICUNO. ELECTRIC causa x4 no GYARADOS e x2 no AERODACTYL. ROCK e WATER causam x2 no
  AERODACTYL. DRAGON (DRAGON CLAW, TM02) causa x2 nos três dragões. FIRE é resistido por quase todo o time: o CHARIZARD
  rende pouco aqui.
- Ameaças: HYPER BEAM em todos (dano alto, mas eles perdem o turno seguinte para recarregar; aproveite para atacar ou
  curar). THUNDER WAVE do segundo DRAGONAIR (paralisia; SAFEGUARD dele bloqueia seus status). OUTRAGE (vários turnos,
  depois ele fica confuso). DRAGON RAGE tira sempre 40 HP. ANCIENT POWER do AERODACTYL causa x4 no CHARIZARD.
  GYARADOS tem INTIMIDATE. DRAGONITE come a SITRUS BERRY com HP baixo.
- Nível recomendado do time: 58+ (LAPRAS com ICE BEAM no 55+).

### Campeão (rival) — TRAINER_CHAMPION_FIRST_SQUIRTLE
- Onde: MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM. Luta automática ao entrar (rival em (6,8), você para em (6,9)).
- Time: PIDGEOT Nv59 [AERIAL ACE, FEATHER DANCE, SAND ATTACK, WHIRLWIND]; ALAKAZAM Nv57 [PSYCHIC, FUTURE SIGHT,
  RECOVER, REFLECT]; RHYDON Nv59 [TAKE DOWN, EARTHQUAKE, ROCK TOMB, SCARY FACE]; ARCANINE Nv59 [EXTREME SPEED,
  FLAMETHROWER, ROAR, BITE]; EXEGGUTOR Nv61 [GIGA DRAIN, EGG BOMB, SLEEP POWDER, LIGHT SCREEN];
  BLASTOISE Nv63 @SITRUS BERRY [HYDRO PUMP, RAIN DANCE, SKULL BASH, BITE]; itens: FULL RESTORE x4
- Tipos que funcionam:
  - PIDGEOT: ELECTRIC, ICE e ROCK.
  - ALAKAZAM: GHOST (SHADOW BALL), BUG e DARK causam x2. Ele é frágil na Defesa física, então um golpe físico forte também
    funciona, mas o REFLECT corta golpe físico pela metade. Bata forte e rápido antes de ele usar RECOVER.
  - RHYDON: WATER e GRASS causam x4. ICE, FIGHTING, GROUND e STEEL causam x2. ELECTRIC não pega (Ground + LIGHTNINGROD).
  - ARCANINE: WATER, GROUND e ROCK.
  - EXEGGUTOR: FIRE, ICE, FLYING, POISON, GHOST e DARK causam x2 e BUG x4. É o melhor alvo do CHARIZARD.
  - BLASTOISE: ELECTRIC e GRASS.
- Ameaças: o BLASTOISE Nv63 é o mais forte. Com RAIN DANCE, o HYDRO PUMP fica ainda mais forte e o fogo perde metade da
  força; tem SITRUS BERRY. Guarde para ele um ELECTRIC (ou GRASS) com HP cheio e NUNCA deixe o CHARIZARD contra ele. ROCK TOMB
  do RHYDON causa x4 no CHARIZARD. SLEEP POWDER do EXEGGUTOR (sono). FEATHER DANCE e SAND ATTACK do PIDGEOT (mande logo um
  ELECTRIC). WHIRLWIND e ROAR forçam troca. FUTURE SIGHT cai dois turnos depois. ARCANINE tem INTIMIDATE e EXTREME SPEED
  (sempre ataca primeiro).
- Nível recomendado do time: 60+ (a média dele é ~60 e o último tem Nv63).

### Revanche (opcional; só depois de entregar a SAPPHIRE ao Celio, com FLAG_SYS_CAN_LINK_WITH_RS)
Mesmas salas e posições. Os scripts escolhem os times *_2 quando FLAG_SYS_CAN_LINK_WITH_RS está ligada. Cada um usa
2 FULL RESTORE (o Campeão usa 4).
- TRAINER_ELITE_FOUR_LORELEI_2: DEWGONG Nv64 [ICE BEAM, SURF, SIGNAL BEAM, DOUBLE TEAM]; CLOYSTER Nv63 [ICE BEAM, SURF,
  SUPERSONIC, RAIN DANCE]; PILOSWINE Nv63 [BLIZZARD, EARTHQUAKE, DOUBLE EDGE, ROCK SLIDE]; JYNX Nv66 [ICE BEAM, PSYCHIC,
  LOVELY KISS, ATTRACT]; LAPRAS Nv66 @CHERI BERRY [ICE BEAM, SURF, PSYCHIC, THUNDER]
- TRAINER_ELITE_FOUR_BRUNO_2: STEELIX Nv65 [EARTHQUAKE, IRON TAIL, CRUNCH, ROCK TOMB]; HITMONCHAN Nv65 [SKY UPPERCUT,
  MACH PUNCH, ROCK SLIDE, COUNTER]; HITMONLEE Nv65 [MEGA KICK, FORESIGHT, EARTHQUAKE, ROCK SLIDE]; STEELIX Nv66
  [EARTHQUAKE, IRON TAIL, CRUNCH, DRAGON BREATH]; MACHAMP Nv68 @PERSIM BERRY [CROSS CHOP, EARTHQUAKE, BRICK BREAK,
  ROCK SLIDE]
- TRAINER_ELITE_FOUR_AGATHA_2: GENGAR Nv66 [SHADOW BALL, PSYCHIC, CONFUSE RAY, HYPNOSIS]; CROBAT Nv66 [SLUDGE BOMB,
  AIR CUTTER, SHADOW BALL, CONFUSE RAY]; MISDREAVUS Nv65 [SHADOW BALL, PSYCHIC, THUNDERBOLT, ATTRACT]; ARBOK Nv68
  [SLUDGE BOMB, EARTHQUAKE, GIGA DRAIN, DOUBLE TEAM]; GENGAR Nv70 @CHESTO BERRY [SHADOW BALL, PSYCHIC, THUNDERBOLT,
  SLUDGE BOMB]
- TRAINER_ELITE_FOUR_LANCE_2: GYARADOS Nv68 [HYPER BEAM, DRAGON DANCE, EARTHQUAKE, THUNDER WAVE]; DRAGONITE Nv66
  [HYPER BEAM, EARTHQUAKE, DRAGON CLAW, FLAMETHROWER]; KINGDRA Nv66 [HYPER BEAM, DRAGON DANCE, SURF, ICE BEAM];
  AERODACTYL Nv70 [HYPER BEAM, ANCIENT POWER, AERIAL ACE, EARTHQUAKE]; DRAGONITE Nv72 @PERSIM BERRY [HYPER BEAM, OUTRAGE,
  THUNDERBOLT, ICE BEAM]
- TRAINER_CHAMPION_REMATCH_SQUIRTLE: HERACROSS Nv72 [MEGAHORN, EARTHQUAKE, COUNTER, ROCK TOMB]; ALAKAZAM Nv73 [PSYCHIC,
  SHADOW BALL, CALM MIND, REFLECT]; TYRANITAR Nv72 [CRUNCH, EARTHQUAKE, THUNDERBOLT, AERIAL ACE]; ARCANINE Nv73
  [EXTREME SPEED, OVERHEAT, AERIAL ACE, IRON TAIL]; EXEGGUTOR Nv73 [GIGA DRAIN, PSYCHIC, SLEEP POWDER, LIGHT SCREEN];
  BLASTOISE Nv75 @SITRUS BERRY [HYDRO PUMP, ICE BEAM, EARTHQUAKE, RAIN DANCE]
- Nível recomendado para a revanche: 70+. Não é necessária para os 100% (não dá item nem Pokémon). Rende EXP e dinheiro.

## Treinadores opcionais relevantes
Nenhum nestes mapas. Fora das cinco lutas acima não há treinadores no Indigo Plateau.

## Itens
Nenhum item no chão nem escondido no Indigo Plateau, nas salas da Liga ou no Hall of Fame. (Os itens escondidos do
caminho, como FULL RESTORE, MAX ETHER e MAX ELIXIR, ficam na Rota 23 e são da seção anterior.)

## NPCs importantes
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F (13,10): enfermeira (cura). Este Centro vira o ponto de retorno ao entrar.
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F (0,7): loja: ULTRA BALL ₽1200, GREAT BALL ₽600, FULL RESTORE ₽3000,
  MAX POTION ₽2500, REVIVE ₽1500, FULL HEAL ₽600, MAX REPEL ₽700. Não vende HYPER POTION nem AWAKENING. HYPER POTION se
  compra antes em MAP_CINNABAR_ISLAND_MART ou MAP_SAFFRON_CITY_MART, e AWAKENING em MAP_CELADON_CITY_DEPARTMENT_STORE_2F.
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F (5,3): guarda da porta da Liga (porta em (4,1)). Antes do Hall of Fame só dá boa
  sorte. Com a NATIONAL POKéDEX e sem FLAG_SYS_CAN_LINK_WITH_RS ela fica em (4,2) bloqueando a porta ("LORELEI is absent").
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F (7,14): rapaz de conselhos (avisa que perder obriga a recomeçar a Elite Four).
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F (23,13), (16,15), (22,9)/(23,9): BLACK BELT, COOLTRAINER e POKéMON JOURNAL, que
  só aparecem depois do Hall of Fame (só conversa).
- MAP_INDIGO_PLATEAU_POKEMON_CENTER_2F: atendentes de link (Union Room, trocas e batalhas por cabo). Nada para a história.
- MAP_ROUTE23: guardas que conferem as insígnias no caminho (ver seção anterior).
- MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB (6,3): Prof. OAK. Depois do Hall of Fame, com 60+ espécies de Kanto capturadas e a
  One Island visitada, dá a NATIONAL POKéDEX (se não tiver dado já na cena de Pallet).

## Pokémon disponíveis (FireRed)
Nenhum. Não há encontros selvagens, presentes nem trocas no Indigo Plateau, nas salas da Liga ou no Hall of Fame.

## Quebra-cabeças
Nenhum. Só há trechos automáticos: entrar em cada sala da Elite Four anda 5 passos sozinho, a sala do LANCE tem um
corredor percorrido sozinho e a sala do Campeão anda 10 passos e já começa a luta. Cada porta (6,2), ou (6,5) na sala do
LANCE, só abre depois de vencer o ocupante da sala.

## Dicas para jogar bem
Checklist de preparação (antes de pisar em (4,1)):
- Níveis: time de 6 com média 58 a 60. O CHARIZARD e o Pokémon que vai enfrentar o BLASTOISE devem estar no 60+. Com média
  abaixo de 55 a chance de perder é alta.
- Cobertura sugerida para quem começou com CHARMANDER:
  - CHARIZARD (FLAMETHROWER, WING ATTACK, SLASH, mais TM26 EARTHQUAKE de MAP_VIRIDIAN_CITY_GYM e TM02 DRAGON CLAW de
    MAP_VICTORY_ROAD_1F (14,1)): bom contra JYNX, AGATHA e EXEGGUTOR.
  - LAPRAS (presente da Silph Co.; ICE BEAM no Nv31, SURF, BODY SLAM): contra LANCE, os ONIX, RHYDON e ARCANINE.
  - Um ELECTRIC com THUNDERBOLT (ZAPDOS Nv50 em MAP_POWER_PLANT, JOLTEON com THUNDERSTONE, ELECTABUZZ ou RAICHU): contra
    LORELEI, GYARADOS, PIDGEOT e BLASTOISE. O ZAPDOS é fraco a ICE: cuidado com o ICE BEAM da LORELEI.
  - Um PSYCHIC (TM29 PSYCHIC de MAP_SAFFRON_CITY_MR_PSYCHICS_HOUSE em SLOWBRO/KADABRA/HYPNO etc.): contra BRUNO e AGATHA.
  - ARTICUNO Nv50 (MAP_SEAFOAM_ISLANDS_B4F) ou outro ICE extra, e um tanque (SNORLAX).
  - TM13 ICE BEAM, TM24 THUNDERBOLT e TM35 FLAMETHROWER custam 4000 fichas cada no prêmio do Game Corner
    (MAP_CELADON_CITY_GAME_CORNER_PRIZE_ROOM). TM30 SHADOW BALL custa 4500.
- Mochila mínima: 10 FULL RESTORE (ou 15 entre MAX POTION e HYPER POTION), 8 a 10 REVIVE, 5 FULL HEAL (ou AWAKENING
  e PARLYZ HEAL), além de ETHER/ELIXIR guardados para repor PP. Para 10 FULL RESTORE + 10 REVIVE + 5 FULL HEAL são
  ₽48.000.
- Entre as salas não há cura. Cure com itens fora de batalha (menu) ao fim de cada luta e reordene o time para a
  próxima. O menu SAVE funciona dentro das salas, e ao continuar você volta à mesma sala com o progresso mantido.
- Perder qualquer uma das cinco lutas manda você de volta ao MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F, curado, sem parte do
  dinheiro (maior nível do time x 4 x 30; com Nv60 são ₽7.200) e com a Elite Four inteira zerada (recomeça na LORELEI).
  Nada além disso se perde: insígnias, itens obtidos, Pokémon capturados e outros marcos continuam. A EXP e o dinheiro das
  lutas vencidas antes da derrota ficam. Dá para treinar repetindo LORELEI e BRUNO.
- Depois de perder, se precisar sair para treinar ou comprar, use FLY para INDIGO PLATEAU para voltar.
- Para os 100%: a NATIONAL POKéDEX exige 60 espécies de Kanto CAPTURADAS. Se ainda faltam, capture o que estiver ao
  alcance antes ou logo depois do Hall of Fame. Sem ela, o Celio não inicia a parte 2 das Sevii (RUBY/SAPPHIRE, ilhas 4 a 7)
  e o restante do pós-jogo fica travado.
- Se quiser farmar EXP/dinheiro refazendo a Liga com os times originais, faça isso ANTES de pegar a NATIONAL POKéDEX:
  depois dela a Liga fica fechada até a SAPPHIRE ser entregue.
- Nada fica inacessível depois desta seção: a Rota 23, a Victory Road e o Indigo Plateau continuam abertos (FLY para
  INDIGO PLATEAU).
