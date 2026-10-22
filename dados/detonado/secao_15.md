# Seção 15 — Rota 21, Power Plant (ZAPDOS) e Ginásio de Viridian (GIOVANNI)
Marcos do roteiro cobertos: giovanni, novo: zapdos
Mapas: MAP_ROUTE21_SOUTH, MAP_ROUTE21_NORTH, MAP_PALLET_TOWN, MAP_ROUTE10, MAP_POWER_PLANT, MAP_VIRIDIAN_CITY, MAP_VIRIDIAN_CITY_GYM

## Passo a passo
1. Ponto de partida: Ilha Cinnabar (MAP_CINNABAR_ISLAND), com a Volcano Badge (BLAINE). Se o BILL ainda espera no
   Centro Pokémon de Cinnabar, a viagem às Sevii é opcional antes do GIOVANNI: o ginásio de Viridian só confere as
   insígnias 2 a 7 (ver item 9).
2. Rota 21 Sul (MAP_ROUTE21_SOUTH): sair de Cinnabar para o norte surfando (SURF). Rota só de água, com ilhotas de
   pescadores. Treinadores na água: SWIMMER JACK (15,24) visão 3, SWIMMER ROLAND (10,29) anda e vê 4 tiles,
   SWIMMER JEROME (15,38) visão 3. Pescadores CLAUDE (11,8) e NOLAN (14,15) têm visão 0 (só lutam se falar com eles).
3. Rota 21 Norte (MAP_ROUTE21_NORTH): continuar ao norte. SIS AND BRO LIL & IAN (14,35)/(15,35) = luta dupla (visão 1).
   SWIMMER SPENCER (12,44) anda em círculo perto da ilhota do PEARL escondido (17,42). Pescadores WADE (16,26) e
   RONALD (7,27) só com conversa. No topo (x 11–16, y 5–10) fica a grama alta com TANGELA, logo abaixo de Pallet.
4. Pallet Town (MAP_PALLET_TOWN): passagem; a mãe (casa do jogador) recupera o time. Daqui, usar FLY até a Rota 10
   (Centro Pokémon da Rota 10).
5. Rota 10 (MAP_ROUTE10): do Centro Pokémon, surfar o rio para o sul, passando pela entrada do Rock Tunnel. Perto da
   Power Plant: POKéMANIAC MARK (13,44), olhando para a esquerda, visão 5 (luta quase certa). MAX ETHER escondido em
   (12,40). Porta da Power Plant em (7,40).
6. Power Plant (MAP_POWER_PLANT): entra-se em (5,38), canto sudoeste. Tudo no mesmo nível (sem quebra-cabeça). Ordem
   prática (sentido horário): MAX POTION (7,27) subindo pela sala de entrada → sala central longa (y 21–27): ELIXIR
   (26,22), pegar de (26,21) olhando para baixo, e TM17 (40,22) de (40,21) ou (41,22) → sala sudeste: TM25 (46,37)
   de (46,38) ou (47,37) → corredor estreito para o norte → sala nordeste: THUNDERSTONE (45,4) de (45,5) →
   oeste até a sala final com o ZAPDOS (5,11).
   - Duas "Poké Balls" são ELECTRODE Nv34 disfarçados: (30,38) no corredor sul e (36,5) na sala nordeste. Falar com
     eles inicia luta selvagem; qualquer resultado (vencer, fugir, capturar) remove o objeto para sempre.
   - Itens escondidos: MAX ELIXIR (29,16), no chão em frente à máquina mais a leste da sala central, alcançável de
     (29,17) ou (28,16); THUNDERSTONE (8,12) na sala do ZAPDOS (de (8,13), (7,12) ou (9,12)).
7. ZAPDOS (5,11): falar com ele = luta lendária Nv50. Salvar antes. Ver "Dicas" sobre o que acontece se derrotar ou
   fugir. Depois, sair pela saída lateral oeste (1,11)/(0,13), que dá na Rota 10, e voar para Viridian.
8. Viridian City (MAP_VIRIDIAN_CITY): a porta do ginásio fica em (36,10). Enquanto a porta está trancada, pisar em
   (36,11) faz o jogador ler "trancado" e pular a saliência para trás. A tranca abre AO ENTRAR em Viridian
   (transição de mapa) tendo as insígnias 2–7: Cascade, Thunder, Rainbow, Soul, Marsh e Volcano. A Boulder Badge não é
   conferida. O velho em (34,11) passa a dizer que o líder voltou.
9. Ginásio de Viridian (MAP_VIRIDIAN_CITY_GYM): piso de setas giratórias (ver Quebra-cabeças). Correr não é permitido
   aqui. Lutas forçadas no caminho: COOLTRAINER WARREN e BLACK BELT TAKASHI. Os outros seis treinadores são opcionais.
10. Vencer GIOVANNI (2,2): recebe a EARTH BADGE (todos os Pokémon obedecem; insígnia 8) e o TM26 (EARTHQUAKE).
    Falar com ele de novo depois da luta: tela escurece e ele some de vez. A vitória também arma a luta tardia com
    o rival na Rota 22 (seção 16).
11. Com o GIOVANNI fora, ficar EM CIMA do tile (2,2) e usar o ITEMFINDER: MACHO BRACE (item enterrado sob os pés,
    só aparece com o ITEMFINDER, não com o botão A).
12. Próximo destino: Rota 22, a oeste de Viridian, rumo ao Indigo Plateau (seção 16). Levar SURF e STRENGTH no time.

## Lutas obrigatórias
### Cooltrainer Warren — TRAINER_COOLTRAINER_WARREN
- Onde: MAP_VIRIDIAN_CITY_GYM (13,7), olhando para a direita, visão 3: dispara ao passar por (15,7) ou (16,7).
- Time: MAROWAK Nv37 [BONEMERANG]; MAROWAK Nv37; RHYHORN Nv38 [TAKE DOWN, ROCK BLAST]; NIDORINA Nv39;
  NIDOQUEEN Nv39 [BODY SLAM, BITE, DOUBLE KICK]; usa HYPER POTION. Prêmio $1404.
- Tipos que funcionam: Water, Grass, Ice. Contra os NIDO, Psychic e Ground também servem.
- Nível recomendado do time: 42+.

### Black Belt Takashi — TRAINER_BLACK_BELT_TAKASHI
- Onde: MAP_VIRIDIAN_CITY_GYM (10,2), olhando para baixo, visão 3: dispara ao entrar em (10,5). Ele desce até (10,4).
- Time: MACHOKE Nv38; MACHOP Nv38; MACHOKE Nv38 (todos com BLACK BELT). Prêmio $912.
- Tipos que funcionam: Psychic, Flying.
- Nível recomendado do time: 42+.

### Giovanni — TRAINER_LEADER_GIOVANNI
- Onde: MAP_VIRIDIAN_CITY_GYM (2,2): falar com ele de (3,2) olhando para a esquerda ou de (2,3) olhando para cima.
- Time: RHYHORN Nv45 [TAKE DOWN, ROCK BLAST, SCARY FACE, EARTHQUAKE]; DUGTRIO Nv42 [SLASH, SAND TOMB, MUD SLAP,
  EARTHQUAKE]; NIDOQUEEN Nv44 [BODY SLAM, DOUBLE KICK, POISON STING, EARTHQUAKE]; NIDOKING Nv45 [THRASH,
  DOUBLE KICK, POISON STING, EARTHQUAKE]; RHYHORN Nv50 [TAKE DOWN, ROCK BLAST, SCARY FACE, EARTHQUAKE].
  Itens: HYPER POTION ×2, FULL HEAL. Prêmio $5000.
- Tipos que funcionam: Water e Grass (4× nos RHYHORN), Ice. Psychic contra os NIDO. Flying é imune a EARTHQUAKE,
  mas o CHARIZARD leva 4× do ROCK BLAST dos RHYHORN: não deixar o CHARIZARD contra eles.
- Nível recomendado do time: 48–50. Um Water forte (LAPRAS da Silph, ou o que tiver SURF) resolve a luta.

## Treinadores opcionais relevantes
- MAP_ROUTE21_NORTH: TRAINER_SIS_AND_BRO_LIL_IAN (dupla) Nv33, $264; TRAINER_SWIMMER_MALE_SPENCER Nv33, $132;
  TRAINER_FISHERMAN_WADE (6× MAGIKARP Nv27) $972; TRAINER_FISHERMAN_RONALD Nv28 $1008 (pescadores: visão 0).
- MAP_ROUTE21_SOUTH: TRAINER_SWIMMER_MALE_JACK (STARMIE Nv37) $148; TRAINER_SWIMMER_MALE_ROLAND Nv32 $128 (anda);
  TRAINER_SWIMMER_MALE_JEROME Nv33 $132; TRAINER_FISHERMAN_CLAUDE Nv31 $1116; TRAINER_FISHERMAN_NOLAN Nv33 $1188.
- MAP_ROUTE10: TRAINER_POKEMANIAC_MARK (RHYHORN Nv29; LICKITUNG Nv29) $1392, visão 5 na margem da Power Plant.
- MAP_VIRIDIAN_CITY_GYM (todos dão dinheiro/EXP bons):
  - TRAINER_TAMER_JASON (10,10) RHYHORN Nv43, $1720, olha para baixo.
  - TRAINER_COOLTRAINER_YUJI (12,10) Nv38 ×5 (SANDSLASH, GRAVELER, ONIX, GRAVELER, MAROWAK), $1368, olha para baixo.
  - TRAINER_BLACK_BELT_ATSUSHI (11,14) MACHOP/MACHOKE Nv40, $960, olha para cima.
  - TRAINER_COOLTRAINER_SAMUEL (6,8) Nv37–39 ×5, $1404, olha para baixo.
  - TRAINER_BLACK_BELT_KIYO (3,11) MACHOKE Nv43, $1032, olha para a esquerda (visão 2).
  - TRAINER_TAMER_COLE (2,21) ARBOK/TAUROS Nv39, $1560, olha para a direita (visão 2).
  Nenhum desses bloqueia o caminho descrito no quebra-cabeça.

## Itens
### MAP_ROUTE21_NORTH
- (17,42) PEARL — escondido (na ilhota perto do SWIMMER SPENCER).
### MAP_ROUTE10
- (12,40) MAX ETHER — escondido (perto do POKéMANIAC MARK; precisa SURF para chegar).
### MAP_POWER_PLANT
- (7,27) MAX POTION — visível
- (26,22) ELIXIR — visível (pegar de (26,21))
- (40,22) TM17 (PROTECT) — TM, visível
- (46,37) TM25 (THUNDER) — TM, visível
- (45,4) THUNDERSTONE — visível (pegar de (45,5))
- (29,16) MAX ELIXIR — escondido
- (8,12) THUNDERSTONE — escondido (sala do ZAPDOS)
- (30,38) e (36,5) — NÃO são itens: ELECTRODE Nv34 disfarçados.
### MAP_VIRIDIAN_CITY_GYM
- TM26 (EARTHQUAKE) — presente do GIOVANNI ao vencer.
- (2,2) MACHO BRACE — escondido sob os pés: só com ITEMFINDER, parado no tile, depois que o GIOVANNI some.
### MAP_VIRIDIAN_CITY
- (17,5) POTION — visível, ao lado da árvore de CUT (18,5) (se ainda não pegou em seção anterior).

## NPCs importantes
- MAP_VIRIDIAN_CITY (34,11): velho; antes da tranca abrir diz que o ginásio está fechado, depois avisa que o líder voltou.
- MAP_VIRIDIAN_CITY (8,26): tutor de DREAM EATER (atrás da árvore de CUT (11,24)), se ainda não usado.
- MAP_VIRIDIAN_CITY_GYM (16,20): Gym Guy na entrada, conselhos sobre o tipo Ground.
- MAP_VIRIDIAN_CITY_MART: POKé BALL, POTION, ANTIDOTE, PARLYZ HEAL (loja fraca; comprar curas em Celadon ou no
  Indigo Plateau).
- MAP_PALLET_TOWN: a mãe recupera o time na casa do jogador.

## Pokémon disponíveis (FireRed)
### MAP_ROUTE21_NORTH e MAP_ROUTE21_SOUTH (mesma tabela)
- grama: TANGELA 17-28 (100%) — só há grama no Norte (y 5–10)
- surf: TENTACOOL 5-40 (100%)
- OLD ROD: MAGIKARP 5 (100%)
- GOOD ROD: HORSEA 5-15 (60%), MAGIKARP 5-15 (20%), KRABBY 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (80%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_PALLET_TOWN
- surf: TENTACOOL 5-40 (100%)
- OLD ROD: MAGIKARP 5-10 (100%); GOOD ROD: HORSEA 5-15 (60%), MAGIKARP 5-15 (20%), KRABBY 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (40%), SHELLDER 15-25 (40%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_ROUTE10 (água)
- surf: TENTACOOL 5-40 (100%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: HORSEA 5-15 (60%), MAGIKARP 5-15 (20%), KRABBY 5-15 (20%)
- SUPER ROD: HORSEA 15-35 (84%), GYARADOS 15-25 (15%), PSYDUCK 25-35 (1%)
### MAP_POWER_PLANT
- chão: VOLTORB 22-25 (30%), MAGNEMITE 22-25 (30%), PIKACHU 22-26 (25%), MAGNETON 31-34 (10%), ELECTABUZZ 32-35 (5%)
- encontro fixo: ZAPDOS Nv50 (5,11) [THUNDER WAVE, AGILITY, DETECT, DRILL PECK; habilidade PRESSURE]
- encontro fixo: ELECTRODE Nv34 ×2 nas Poké Balls falsas (30,38) e (36,5) [tem SELF-DESTRUCT]
### MAP_VIRIDIAN_CITY (lago)
- surf: PSYDUCK 20-40 (100%)
- OLD ROD: MAGIKARP 5 (100%); GOOD ROD: POLIWAG 5-15 (60%), MAGIKARP 5-15 (20%), GOLDEEN 5-15 (20%)
- SUPER ROD: POLIWAG 15-25 (40%), POLIWHIRL 20-30 (40%), GYARADOS 15-25 (15%), PSYDUCK 15-35 (5%)

## Quebra-cabeças
### Ginásio de Viridian — setas giratórias (conferido no layout do mapa)
Regra do piso: pisar numa seta faz o jogador deslizar naquela direção. Passando por outra seta, a direção muda. Ele
só para num tile de PARADA ou ao bater numa parede/pessoa. Setas e paradas relevantes:
- (16,13) seta para baixo → para em (16,15); (19,14) seta para cima → desliza a coluna x=19 até a parada (19,3);
- (19,2) seta para a esquerda → desliza a linha y=2 até a parada (11,2);
- (11,3) seta para a direita (manda para (17,3), beco sem saída); (18,3) seta para baixo; (4,10) seta para baixo;
  (5,17)/(4,18) setas para a direita; (13,21)/(13,22) setas para a esquerda; (0,20)/(1,20) setas para cima.
O BLACK BELT TAKASHI parado em (10,2) tapa a passagem de (11,2) para o oeste. É preciso lutar com ele primeiro, por
baixo, para ele descer até (10,4). Solução (entrada em (17,21)):
1. Subir x=17 até (17,15); oeste até (14,15); subir até (14,13); (13,13); subir x=13 até (13,10); leste até
   (15,10); subir x=15 até (15,6). Em (15,7) o WARREN vê e luta (ele para em (14,7)).
2. De (15,6) ir a oeste até (12,6), descer para (12,7), oeste até (10,7) e subir para (10,6) e depois (10,5): o
   TAKASHI desce até (10,4) e luta. NÃO sair do ginásio depois disso: ao recarregar o mapa ele volta para (10,2).
3. Voltar: (10,6) → (10,7) → (12,7) → (12,6) → (15,6) → descer x=15 até (15,10) → (16,10) → descer até (16,12) →
   pisar em (16,13) (seta, desliza até a parada (16,15)) → (17,15) → (18,15) → subir para (18,14).
4. De (18,14) pisar à direita em (19,14) (seta para cima): desliza até a parada (19,3).
5. De (19,3) pisar para cima em (19,2) (seta para a esquerda): desliza até a parada (11,2).
6. (10,2) (vazio agora) → (10,3) → oeste até (7,3) → descer x=7 até (7,6) → oeste até (3,6) → subir x=3 até (3,2).
   Virar para a esquerda e falar com o GIOVANNI (2,2).
Caminho alternativo, se já lutou com o TAKASHI por baixo: da entrada, subir x=17 até (17,15) → (18,15) → (18,14) e
seguir os passos 4–6.

## Dicas para jogar bem
- ZAPDOS: salvar antes de falar com ele. Se ele DESMAIAR, some para sempre (flag de "já lutou"). Se FUGIR da luta,
  ele "voa", mas reaparece ao reentrar na Power Plant. Capturar: ULTRA BALLs/TIMER BALLs; SLEEP/PARALYZE ajudam; Rock
  e Ice causam mais dano, Electric quase não faz efeito. A MASTER BALL resolve, mas MEWTWO (pós-jogo) é o alvo
  mais difícil para ela.
- ELECTRODE falsos podem usar SELF-DESTRUCT: capturar logo (2 registros de ELECTRODE de graça) ou evitar.
- Power Plant tem PIKACHU, MAGNEMITE/MAGNETON e ELECTABUZZ (FireRed): bom lugar para completar a Pokédex.
- TANGELA no FireRed aparece na grama da Rota 21 Norte (100%). Capturar enquanto passa.
- Pescar com SUPER ROD na Rota 21/Pallet: SEADRA (4%), SHELLDER (só em Pallet).
- Itens que exigem HM/condição: PEARL (Rota 21) e MAX ETHER (Rota 10) só com SURF; MACHO BRACE só com ITEMFINDER,
  depois de vencer o GIOVANNI e falar com ele de novo.
- Antes da Rota 22: time ~50, com quem saiba SURF e STRENGTH. Comprar FULL RESTORE/MAX POTION/REVIVE (o Indigo
  Plateau vende, mas só no fim da seção 16). A Victory Road é longa e não tem Centro Pokémon.
