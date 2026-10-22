# Seção 13 — Cinnabar Island, Pokémon Mansion, BLAINE e partida para as Sevii Islands
Marcos do roteiro cobertos: cinnabar, fosseis, chave_secreta, blaine, sevii (só o embarque com o BILL em Cinnabar); novo: trocas_lab_cinnabar, novo: tutor_metronome
Mapas: MAP_CINNABAR_ISLAND, MAP_CINNABAR_ISLAND_POKEMON_CENTER_1F, MAP_CINNABAR_ISLAND_MART, MAP_CINNABAR_ISLAND_POKEMON_LAB_ENTRANCE, MAP_CINNABAR_ISLAND_POKEMON_LAB_LOUNGE, MAP_CINNABAR_ISLAND_POKEMON_LAB_RESEARCH_ROOM, MAP_CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM, MAP_POKEMON_MANSION_1F, MAP_POKEMON_MANSION_2F, MAP_POKEMON_MANSION_3F, MAP_POKEMON_MANSION_B1F, MAP_CINNABAR_ISLAND_GYM, MAP_ONE_ISLAND_HARBOR

## Passo a passo
1. Chegada a Cinnabar Island (MAP_CINNABAR_ISLAND) surfando: pela Rota 21 (MAP_ROUTE21_SOUTH, conexão norte) ou
   pela Rota 20 (MAP_ROUTE20, conexão leste, vindo das Seafoam Islands). Exige SURF fora de batalha (Soul Badge +
   HM03). Portas da ilha: Pokémon Mansion (8,3), Ginásio (20,4), Pokémon Lab (8,9), Centro (14,11), Mart (19,11).
   NPCs: senhora (14,6) e velho (11,11) só conversam.
2. Centro Pokémon (MAP_CINNABAR_ISLAND_POKEMON_CENTER_1F): enfermeira (7,2). Entrar no Centro já grava o respawn
   em Cinnabar (e a ilha vira destino de FLY ao pisar nela). Escada para o 2F (Union Room) em (1,6).
3. Mart (MAP_CINNABAR_ISLAND_MART): balconista (2,3). Compre MAX REPEL e ESCAPE ROPE para a Mansion e FULL HEAL
   (queimaduras do BLAINE).
4. O Ginásio está TRANCADO: o gatilho de piso em (20,5), logo abaixo da porta (20,4), mostra "The door is locked…"
   e empurra o jogador 1 tile para baixo. Ele só some quando a SECRET KEY foi pega (flag
   FLAG_HIDE_POKEMON_MANSION_B1F_SECRET_KEY). A checagem roda ao ENTRAR no mapa da ilha, então depois de pegar a
   chave basta sair da Mansion (a pé, ESCAPE ROPE ou FLY) que a porta já abre.
5. Pokémon Lab (porta (8,9) → MAP_CINNABAR_ISLAND_POKEMON_LAB_ENTRANCE, chega em (4,9)). Portas internas:
   Meeting Room (13,5) → MAP_CINNABAR_ISLAND_POKEMON_LAB_LOUNGE; R&D Room (19,5) →
   MAP_CINNABAR_ISLAND_POKEMON_LAB_RESEARCH_ROOM; Testing Room (25,5) → MAP_CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM.
   Não existe TM de presente no Lab no FireRed (a única TM de presente da ilha é a TM38 do BLAINE).
6. Fósseis (marco fosseis), na Testing Room: o cientista que anda por perto de (12,3). Fale com ele, escolha o
   fóssil no menu e responda YES. Ele fica com o item e pede para você dar uma volta. Saia da sala pela porta (7,9)
   (basta entrar na MAP_CINNABAR_ISLAND_POKEMON_LAB_ENTRANCE — é isso que marca o fóssil como pronto) e volte.
   Fale de novo: recebe o Pokémon Nv5 (opção de apelido; com o time cheio vai para o PC). Um fóssil por vez:
   repita o ciclo para o segundo.
   - HELIX FOSSIL → OMANYTE Nv5; DOME FOSSIL → KABUTO Nv5 (só um dos dois, o escolhido no Mt. Moon).
   - OLD AMBER → AERODACTYL Nv5 (o OLD AMBER vem do cientista do Museu de Pewter, MAP_PEWTER_CITY_MUSEUM_1F (21,3),
     sala dos fundos — ver seção 7).
7. Trocas e tutor no Lab (para 100%, ver NPCs importantes): RAICHU→ELECTRODE e VENONAT→TANGELA na Meeting Room,
   PONYTA→SEEL na Testing Room, tutor de METRONOME na R&D Room.
8. Pokémon Mansion (marco chave_secreta): porta (8,3) da ilha → MAP_POKEMON_MANSION_1F em (8,33). Todas as
   estátuas da Mansion acionam o MESMO interruptor (uma flag global para os 4 andares). Siga a sequência da seção
   Quebra-cabeças: ela pega todos os itens e termina na SECRET KEY do B1F (5,7).
9. Volte à ilha e entre no Ginásio (MAP_CINNABAR_ISLAND_GYM, chega em (25,23)). Responda o quiz (tabela em
   Quebra-cabeças): cada resposta certa abre a próxima porta sem luta; resposta errada chama o treinador da sala e,
   vencendo, a porta abre do mesmo jeito. Ninguém no ginásio tem linha de visão (visão 0): só luta quem você chama.
10. BLAINE em (5,4), sala noroeste. Vencer dá a VOLCANOBADGE (WATERFALL fora de batalha) e a TM38 (FIRE BLAST).
    Se não houver espaço para a TM, ele a guarda: fale com ele de novo depois.
11. Cena do BILL (início do marco sevii): ao sair do ginásio, o BILL (parado em (20,7) na ilha) vem até você e
    pergunta se quer ir com ele à One Island (YES/NO).
    - YES: o barco (Seagallop) chega e vocês embarcam na hora → MAP_ONE_ISLAND_HARBOR.
    - NO: ele diz que o barco ainda não chegou e vai esperar no Centro Pokémon. Ele fica em
      MAP_CINNABAR_ISLAND_POKEMON_CENTER_1F (11,5). Quando estiver pronto, fale com ele e responda YES: vocês saem
      do Centro e embarcam.
    Recomendado: responder NO, curar, arrumar o time no PC e comprar itens antes (nas ilhas, até resolver o pedido
    do amigo do BILL, o PC não acessa as caixas — conferir na seção 14). A viagem continua na seção 14.
12. A viagem às Sevii NÃO é obrigatória para abrir o Ginásio de Viridian: a porta de Viridian abre só com as
    insígnias 2 a 7 (CASCADE, THUNDER, RAINBOW, SOUL, MARSH, VOLCANO). Dá para recusar o BILL, ir a Viridian e
    voltar ao BILL depois (ele continua no Centro). Para 100% a viagem é necessária (One/Two/Three Island).

## Lutas obrigatórias
### BLAINE — TRAINER_LEADER_BLAINE
- Onde: MAP_CINNABAR_ISLAND_GYM (5,4), depois das 6 portas do quiz.
- Time: GROWLITHE Nv42 [BITE, ROAR, TAKE DOWN, FIRE BLAST]; PONYTA Nv40 [STOMP, BOUNCE, FIRE SPIN, FIRE BLAST];
  RAPIDASH Nv42 [STOMP, BOUNCE, FIRE SPIN, FIRE BLAST]; ARCANINE Nv47 [BITE, ROAR, TAKE DOWN, FIRE BLAST].
  Itens: HYPER POTION, HYPER POTION, FULL HEAL. Prêmio $4700 + VOLCANOBADGE + TM38 (FIRE BLAST).
- Tipos que funcionam: WATER (LAPRAS, GYARADOS, OMASTAR/KABUTOPS), GROUND (DUGTRIO, RHYDON), ROCK (GOLEM).
  GROWLITHE e ARCANINE costumam ter INTIMIDATE; PONYTA/RAPIDASH podem ter FLASH FIRE (golpe de fogo neles só
  fortalece). ROAR tira seu Pokémon da luta. O CHARIZARD do jogador resiste a fogo mas não causa dano com ele:
  use golpes de outro tipo.
- Nível recomendado do time: 45-50, com um atacante de água forte (SURF) e FULL HEAL/BURN HEAL.

## Treinadores opcionais relevantes
- MAP_POKEMON_MANSION_1F: TRAINER_YOUNGSTER_JOHNSON (8,8, anda esquerda/direita, visão 1) EKANS Nv33, EKANS Nv33,
  RATICATE Nv34 — $544, perto da estátua do 1F.
- MAP_POKEMON_MANSION_1F: TRAINER_SCIENTIST_TED (22,24, olhando à esquerda, visão 4) ELECTRODE Nv29, WEEZING Nv29 —
  $1392; está na área sul onde se cai do 3F, no caminho da escada para o B1F.
- MAP_POKEMON_MANSION_2F: TRAINER_BURGLAR_ARNIE (5,23) CHARMANDER Nv34, CHARMELEON Nv34 — $2992.
- MAP_POKEMON_MANSION_3F: TRAINER_BURGLAR_SIMON (7,13, anda) NINETALES Nv38 — $3344 (área sudoeste, escada do 2F).
- MAP_POKEMON_MANSION_3F: TRAINER_SCIENTIST_BRAYDON (22,13, olhando para baixo, visão 1) MAGNEMITE, MAGNETON,
  VOLTORB Nv33 — $1584, no corredor que leva às sacadas.
- MAP_POKEMON_MANSION_B1F: TRAINER_BURGLAR_LEWIS (20,25, anda) GROWLITHE Nv34, PONYTA Nv34 — $2992.
- MAP_POKEMON_MANSION_B1F: TRAINER_SCIENTIST_IVAN (34,13, olhando para baixo, visão 6) MAGNEMITE Nv34,
  ELECTRODE Nv34 — $1632; vê todo o corredor leste no caminho da TM14 e da estátua norte.
- MAP_CINNABAR_ISLAND_GYM (só lutam se você errar o quiz ou falar com eles):
  TRAINER_BURGLAR_QUINN (25,11) GROWLITHE/VULPIX/NINETALES Nv36 — $3168 (porta 1);
  TRAINER_SUPER_NERD_ERIK (25,4) VULPIX, VULPIX, NINETALES Nv36 — $864 (sem porta, totalmente opcional);
  TRAINER_SUPER_NERD_AVERY (17,5) PONYTA, CHARMANDER, VULPIX, GROWLITHE Nv34 — $816 (porta 2);
  TRAINER_BURGLAR_RAMON (16,11) PONYTA Nv41 — $3608 (porta 3);
  TRAINER_SUPER_NERD_DEREK (16,18) RAPIDASH Nv41 — $984 (porta 4);
  TRAINER_BURGLAR_DUSTY (4,19) VULPIX, GROWLITHE Nv37 — $3256 (porta 5);
  TRAINER_SUPER_NERD_ZAC (4,11) GROWLITHE, VULPIX Nv37 — $888 (porta 6).
  Os BURGLARs pagam muito: vale errar de propósito ou falar com eles para farmar dinheiro/EXP.

## Itens
### MAP_POKEMON_MANSION_1F
- (2,21) MOON STONE — escondido (ficar em (3,21) olhando para oeste e apertar A)
- (22,6) ESCAPE ROPE — visível (corredor norte, entre as colunas)
- (27,15) PROTEIN — visível (sala central; exige o interruptor LIGADO, porta (22-24,10-11))
- (29,32) CARBOS — visível (área sul, onde se cai do 3F; exige interruptor LIGADO para chegar)
### MAP_POKEMON_MANSION_2F
- (18,23) ZINC — visível
- (36,8) CALCIUM — visível (sala nordeste)
- (35,17) HP UP — visível (área leste, ligada à escada (34,22) ↔ 3F (34,18); interruptor LIGADO)
### MAP_POKEMON_MANSION_3F
- (32,6) IRON — visível (sala nordeste; passagem (21,6-8) só aberta com interruptor DESLIGADO)
- (9,19) MAX POTION — visível (área sudoeste, escada 2F (9,14) ↔ 3F (11,11))
- (36,13) RARE CANDY — escondido (fim leste do corredor do Braydon; ficar em (35,13) olhando para leste)
### MAP_POKEMON_MANSION_B1F
- (2,29) FULL RESTORE — visível (canto sudoeste)
- (35,5) ELIXIR — escondido (sala nordeste, 8 tiles a leste da estátua; ficar em (34,5) olhando para leste)
- (23,4) TM14 (BLIZZARD) — visível (sala norte-central)
- (5,7) SECRET KEY — key item (sala noroeste; pegar de (4,7) olhando para leste ou de (5,6) olhando para baixo)
- (6,21) TM22 (SOLARBEAM) — visível (sala oeste; pegar de (6,20) olhando para baixo)
### MAP_CINNABAR_ISLAND_GYM
- TM38 (FIRE BLAST) — presente do BLAINE ao vencer
### MAP_CINNABAR_ISLAND_POKEMON_LAB_LOUNGE
- STARDUST — segurado pelo TANGELA "TANGENY" recebido na troca
### MAP_CINNABAR_ISLAND (e Centro/Mart/Lab)
- Nenhum item no chão nem escondido.

## NPCs importantes
- MAP_CINNABAR_ISLAND_MART (2,3): vende ULTRA BALL, GREAT BALL, HYPER POTION, REVIVE, FULL HEAL, ESCAPE ROPE,
  MAX REPEL.
- MAP_CINNABAR_ISLAND_POKEMON_CENTER_1F (7,2): enfermeira. BILL aparece em (11,5) só se você recusar a viagem.
- MAP_CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM (12,3, anda): cientista dos fósseis — HELIX FOSSIL→OMANYTE,
  DOME FOSSIL→KABUTO, OLD AMBER→AERODACTYL, todos Nv5; sair para a entrada do Lab e voltar entre entregar e receber.
- MAP_CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM (11,8): GARETT — troca: pede PONYTA, dá SEEL "SEELOR". Uma vez.
- MAP_CINNABAR_ISLAND_POKEMON_LAB_LOUNGE (4,6): CLIFTON (velho) — troca: pede RAICHU, dá ELECTRODE "ESPHERE". Uma vez.
- MAP_CINNABAR_ISLAND_POKEMON_LAB_LOUNGE (10,5): NORMA — troca: pede VENONAT, dá TANGELA "TANGENY" (segura
  STARDUST). Uma vez.
- MAP_CINNABAR_ISLAND_POKEMON_LAB_RESEARCH_ROOM (5,4, anda): tutor de METRONOME — ensina uma única vez, a um
  Pokémon compatível (pergunta YES/NO e avisa que só ensina uma vez).
- MAP_CINNABAR_ISLAND_GYM (24,20): Gym Guy, só dá dica (água contra o BLAINE).
- MAP_CINNABAR_ISLAND (20,7): BILL depois da 7ª insígnia (cena descrita no passo 11).

## Pokémon disponíveis (FireRed)
### MAP_CINNABAR_ISLAND
- surf: TENTACOOL 5-40 (100%)
- OLD ROD: MAGIKARP 5 (100%)
- GOOD ROD: HORSEA 5-15 (60%), MAGIKARP 5-15 (20%), KRABBY 5-15 (20%)
- SUPER ROD: HORSEA 15-25 (40%), SHELLDER 15-25 (40%), GYARADOS 15-25 (15%), SEADRA 25-35 (4%), PSYDUCK 25-35 (1%)
### MAP_POKEMON_MANSION_1F, MAP_POKEMON_MANSION_2F, MAP_POKEMON_MANSION_3F (mesma tabela nos três)
- caverna/chão: KOFFING 28-30 (30%), RATICATE 32-36 (30%), GROWLITHE 30-32 (15%), RATTATA 26-28 (15%),
  GRIMER 28 (5%), WEEZING 32 (5%)
### MAP_POKEMON_MANSION_B1F
- caverna/chão: KOFFING 28-30 (30%), RATICATE 34-38 (30%), GROWLITHE 30-32 (15%), DITTO 30 (10%), GRIMER 28 (5%),
  WEEZING 34 (5%), RATTATA 26 (5%)
### MAP_CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM
- presente (fóssil revivido): OMANYTE Nv5 ou KABUTO Nv5 (conforme o fóssil do Mt. Moon); AERODACTYL Nv5 (OLD AMBER)
- troca: SEEL (pede PONYTA)
### MAP_CINNABAR_ISLAND_POKEMON_LAB_LOUNGE
- troca: ELECTRODE (pede RAICHU); TANGELA (pede VENONAT)

## Quebra-cabeças
### Pokémon Mansion — interruptor único
Há 5 estátuas-interruptor. Para usar: fique no tile ABAIXO da estátua, olhe para cima (norte), aperte A,
"A secret switch! Press it?" → YES. Cada uso INVERTE o interruptor nos 4 andares ao mesmo tempo (flag
FLAG_POKEMON_MANSION_SWITCH_STATE). Olhos da estátua PRETOS = DESLIGADO (estado inicial do jogo); VERMELHOS =
LIGADO. O estado fica salvo: ao voltar à Mansion, olhe os olhos da estátua antes de planejar.
Estátuas (posição da estátua → onde ficar):
- 1F: (5,5) → (5,6), sala noroeste (junto do Johnson)
- 2F: (2,16) → (2,17), oeste, perto da escada que chega do 1F
- 3F: (12,5) → (12,6), área noroeste
- B1F sul: (24,29) → (24,30), sala do Lewis
- B1F norte: (27,5) → (27,6), sala nordeste
Barreiras que mudam (tiles x,y). O mapa estático mostra o estado DESLIGADO.
- 1F — DESLIGADO: fechadas (22-24,10-11) [porta para a sala central/PROTEIN], (27-29,25-26) e (32-34,25-26)
  [portas da área sul]; aberta (31-33,18-19) [corredor leste]. LIGADO: o contrário.
- 2F — DESLIGADO: fechadas (24-26,14-15) e (10,28-32) [sala sudoeste do diário]; aberta (12,6-8) [liga a sala
  noroeste, da escada (9,3) para o 3F, ao resto do andar]. LIGADO: abre (24-26,14-15) e (10,30-32); fecha (12,4-8).
- 3F — DESLIGADO: fechada (17-19,11-12) [descida para o corredor das sacadas]; aberta (21,6-8) [sala do IRON].
  LIGADO: abre (17-19,11-12); fecha (21,4-8).
- B1F — DESLIGADO: abertas (33-35,20-21) [corredor leste, para o norte] e (16,28-30); fechadas (12,8-12) [sala
  da SECRET KEY] e (20-22,22-23). LIGADO: abre (12,10-12) e (20-22,22-23); fecha (33-35,20-21) e (16,26-30).
Escadas e quedas (tile de origem → destino):
- 1F (10,13) ↔ 2F (6,14); 2F (9,3) ↔ 3F (8,3); 2F (9,14) ↔ 3F (11,11) [3F sudoeste, beco]; 2F (34,22) ↔ 3F (34,18);
  1F (25,27) ↔ B1F (34,29).
- Buracos/sacadas do 3F (só descem): (18,18), (19,18), (20,18) → 1F (19,22)/(20,22) área sul;
  (23,18), (24,18) → 2F (27,17).
- A área sul do 1F (Ted, CARBOS, escada do B1F) não tem ligação com a entrada: só se chega caindo do 3F; para sair
  dela a pé é preciso o interruptor LIGADO e usar a porta sudeste (34,33).
Sequência que pega tudo (começando DESLIGADO, olhos pretos):
1. 1F (DESLIGADO): entrar em (8,33). MOON STONE escondido (2,21). Ir ao norte: Johnson (8,8), ESCAPE ROPE (22,6).
   Estátua do 1F (ficar em (5,6)) → LIGADO.
2. 1F (LIGADO): passar pela porta (22-24,10-11) e pegar PROTEIN (27,15). Subir a escada (10,13) → 2F (6,14).
3. 2F (LIGADO): ZINC (18,23), Arnie (5,23), diário (6,31) pela porta (10,30-32), CALCIUM (36,8), diário (25,4).
   Escada (9,14) → 3F (11,11): Simon (7,13), MAX POTION (9,19), diário (8,16). Descer de volta por (11,11).
4. 2F: estátua do 2F (ficar em (2,17)) → DESLIGADO. Ir pela passagem (12,6-8) até a escada (9,3) → 3F (8,3).
5. 3F (DESLIGADO): leste pela passagem (21,6-8) até o IRON (32,6). Voltar à estátua (ficar em (12,6)) → LIGADO.
6. 3F (LIGADO): descer por (17-19,11-12) ao corredor. Braydon (22,13). RARE CANDY escondido (36,13). Pelo lado
   leste (x 27-28) ir à escada (34,18) → 2F (34,22) → HP UP (35,17) → voltar pela mesma escada ao 3F.
7. 3F: pisar num buraco (18,18)/(19,18)/(20,18) → cai no 1F (19,22). Ted (22,24), CARBOS (29,32), escada (25,27) →
   B1F (34,29).
8. B1F (LIGADO): da escada suba por x 27-29 até o salão central (y 17-21). Desça pela porta (20-22,22-23) para a
   sala do Lewis (20,25) e do diário (21,27). Para o FULL RESTORE (2,29), desça do salão pelo corredor x 13-15
   (y 22-25) e vá para oeste. Estátua sul (ficar em (24,30)) → DESLIGADO.
9. B1F (DESLIGADO): saia da sala do Lewis pela passagem oeste (16,28-30), suba pelo corredor x 13-15 ao salão,
   vá a leste e desça por x 27-29 até a área da escada; dali suba pela passagem (33-35,20-21) e pelo corredor
   leste x 31-36 (Ivan (34,13) desafia). Sala nordeste: ELIXIR escondido (35,5). Sala norte-central (entrada por
   x 17-19, y 6-8): TM14 (23,4). Estátua norte (ficar em (27,6)) → LIGADO.
10. B1F (LIGADO): entrar pela porta (12,10-12) na ala oeste: SECRET KEY (5,7) e TM22 (6,21).
11. Saída: ESCAPE ROPE (ou FLY/DIG/TELEPORT) é o mais simples. A pé: estátua norte (27,6) → DESLIGADO; ir até a
    estátua sul (24,30) → LIGADO; escada (34,29) → 1F (25,27); subir por (27-29,25-26), descer por (32-34,25-26)
    e sair pela porta (34,33) andando para o sul. (Com o interruptor DESLIGADO a área sul do 1F é beco sem saída.)
Caminho mínimo só para a chave (sem itens): entrada → 1F (10,13) → 2F (9,3) [por (12,6-8)] → 3F estátua (12,6)
LIGAR → buraco (18,18) → 1F escada (25,27) → B1F estátua (24,30) DESLIGAR → estátua (27,6) LIGAR → SECRET KEY (5,7).

### Cinnabar Gym — quiz (cada máquina tem duas metades lado a lado; ficar embaixo e olhar para o norte)
| # | Máquina (x,y) → ficar em | Pergunta | Resposta | Abre | Treinador se errar |
|---|---|---|---|---|---|
| 1 | (22,10)/(23,10) → (22,11)/(23,11) | CATERPIE evolves into METAPOD? | YES | (26-27,8-9), norte para a sala NE | TRAINER_BURGLAR_QUINN |
| 2 | (15,2)/(16,2) → (15,3)/(16,3) | There are nine certified POKéMON LEAGUE BADGES? | NO | (17-18,8-9), sul para a sala central | TRAINER_SUPER_NERD_AVERY |
| 3 | (13,10)/(14,10) → (13,11)/(14,11) | POLIWAG evolves three times? | NO | (17-18,15-16), sul | TRAINER_BURGLAR_RAMON |
| 4 | (13,17)/(14,17) → (13,18)/(14,18) | Are electric moves effective against GROUND-type POKéMON? | NO | (11,22-23), oeste | TRAINER_SUPER_NERD_DEREK |
| 5 | (1,18)/(2,18) → (1,19)/(2,19) | POKéMON of the same kind and level are not identical? | YES | (5-6,16-17), norte | TRAINER_BURGLAR_DUSTY |
| 6 | (1,10)/(2,10) → (1,11)/(2,11) | TM28 contains TOMBSTONY? | NO | (5-6,8-9), norte para o BLAINE | TRAINER_SUPER_NERD_ZAC |
Rota: entrada (25,23) → norte pela sala leste até a máquina 1 → porta (26-27,9) → sala NE → oeste pelas linhas
y 2-4 até a máquina 2 → porta (17-18,9) → máquina 3 → porta (17-18,16) → máquina 4 → porta (11,22-23) para oeste →
máquina 5 → porta (5-6,17) → máquina 6 → porta (5-6,9) → BLAINE (5,4). As portas abertas ficam abertas (flags
FLAG_CINNABAR_GYM_QUIZ_1..6); depois de vencer o BLAINE todas abrem.

### Fósseis
Entregar → sair da Testing Room (entrar na entrada do Lab) → voltar → receber. Sem sair da sala o cientista só
repete que leva tempo.

## Dicas para jogar bem
- Leve MAX REPEL para a Mansion (muitos encontros) e ESCAPE ROPE para sair depois da chave.
- GROWLITHE (Mansion, 15%) é exclusivo do FireRed: capture um (e evolua com FIRE STONE para ARCANINE). DITTO
  aparece no B1F (10%). KOFFING/WEEZING, GRIMER, RATTATA/RATICATE também. VULPIX não existe no FireRed (troca).
- Pegue SHELLDER e HORSEA/SEADRA com a SUPER ROD na ilha se ainda faltam na Pokédex.
- Para 100%: reviva os dois fósseis que tiver (o do Mt. Moon e o OLD AMBER); o outro fóssil do Mt. Moon só por
  troca. Faça as três trocas do Lab: RAICHU (PIKACHU + THUNDER STONE), VENONAT (Rotas 12-15, Safari Zone) e
  PONYTA (no FireRed só selvagem nas Sevii: Kindle Road/Mt. Ember — dá para voltar depois) — elas dão ELECTRODE,
  TANGELA e SEEL (TANGELA também é selvagem na Rota 21; SEEL nas Seafoam Islands).
- TM14 (BLIZZARD) e TM22 (SOLARBEAM) do B1F são fortes; TM38 (FIRE BLAST) é ótima no CHARIZARD.
- Os diários da Mansion (2F (25,4) e (6,31), 3F (8,16), B1F (21,27)) são só história (MEW e MEWTWO), sem item.
- Nada aqui fica inacessível: Mansion, Lab e Ginásio continuam abertos depois. Depois da viagem às Sevii, o BILL
  devolve você a Cinnabar (o barco de ida e volta às ilhas é tratado na seção 14).
- Antes de aceitar a viagem do BILL: cure, deposite/retire Pokémon no PC e compre itens.
- Depois do BLAINE: WATERFALL fora de batalha já está liberado, mas o HM07 só se pega mais tarde nas Sevii
  (Four Island, pós-Liga).
