# Arquitetura

[English](../architecture.md)

O sistema é um laço sobre um quadro de 240×160 por vez: **ver → decidir → apertar → conferir**. Ele tem quatro
restrições. O jogo roda em hardware real, então não há como voltar no tempo. Os toques passam por Bluetooth e se
perdem. O único sensor é a imagem. E o modelo de linguagem é lento e custa dinheiro, então só cuida do julgamento.

```
           ┌────────────── agente (LLM) ──────────────────┐
           │ estrategista: plano   executor: ~60 ferramentas │
           └───────────────┬──────────────────────────────┘
                           │ chamadas de ferramenta
 percepcao ──quadro──▶ habilidades ──macros──▶ controle ──Bluetooth──▶ Switch
     ▲                     │  ▲                                        │
     │                     ▼  │                                        │
     └──── mundo (decomp: mapas, espécies, fonte) ◀──── estado (memória) │
     ▲                                                                 │
     └──────────────────── HDMI → placa de captura → OBS ◀─────────────┘
```

## Percepção: `fireredia.percepcao`

**Captura** (`olhos.capturar`). A fonte principal é o projetor em janela do OBS, capturado com `PrintWindow` e
`PW_RENDERFULLCONTENT`. Isso funciona mesmo com a janela coberta e leva cerca de 27 ms em 2560×1440. Sem o projetor,
ou com ele em pé (monitor que dorme o vira para retrato), a captura passa para a Câmera Virtual do OBS, lida numa
thread. A área do GBA é recortada por frações fixas da janela e reduzida para os 240×160 nativos.

**Classificação** (`olhos.classificar`). Estatísticas baratas de pixel em regiões fixas: a caixa azul da batalha, a
caixa branca de texto, a divisória da lista de golpes, a borda do Sim/Não. A tela cai em uma de sete classes; o mapa
em si é reconhecido pela localização, não aqui.

**Localização** (`olhos.Localizador`). Cada mapa é desenhado a partir do decomp: tilesets, paletas, metatiles e mais
sete metatiles de borda tirados dos mapas conectados. O quadro é então comparado por correlação cruzada normalizada:

1. Primeiro, numa janela de ±6 tiles em volta da última posição, no mapa esperado. É o caso comum e leva milissegundos.
2. Depois, nos mapas vizinhos (conexões e destinos de porta).
3. Por fim, uma busca global: todos os mapas em ¼ da resolução, com os seis melhores refinados na resolução cheia, em
   cerca de 1 s.

Casos especiais que viraram regra:
- **Interiores idênticos.** Todos os Centros Pokémon têm o mesmo layout. O empate se resolve por qual deles é
  alcançável a partir da última posição.
- **Andares do mesmo prédio** são quase iguais, então decide o letreiro que aparece ao entrar ("SILPH CO. 2F").
- **Névoa.** Nos andares com névoa da Pokémon Tower o encaixe certo dá 0,42–0,46, então esses mapas são comparados em
  imagens passa-alta, com limite reescalado.
- Uma posição fora dos limites do mapa vira coordenada do mapa conectado.

**Texto** (`texto.py`). Não há OCR genérico. O leitor carrega do decomp a folha de glifos, as larguras e o charmap do
jogo. Para *achar* uma string, ele a desenha na fonte do jogo e compara por template. Para *ler* texto livre, separa
as linhas e casa glifo a glifo. É assim que se leem diálogos, itens de menu, nomes no painel do PC, títulos de caixa e
os números de HP e nível.

**Espécies.** Sprites de frente (inimigo), de costas (o seu) e do resumo são comparados com os sprites do decomp para
as espécies candidatas, como a tabela de selvagens do mapa atual.

## Controle: `fireredia.controle`

`servidor_wsl.py` roda como root no WSL (Ubuntu 22.04, porque o NXBT fixa o `dbus-python` 1.2.16). Ele assume o
adaptador Bluetooth USB, repassado pelo `usbipd`, emula um Pro Controller e expõe um único endpoint HTTP: `POST /` com
uma macro NXBT e `GET /` com o estado da conexão. O cliente (`maos.py`) segura cada botão por pelo menos 50 ms. Toques
mais curtos se perderam na medição (7 de 8 a 33 ms). `jogar.subir_controle()` anexa o adaptador, sobe o servidor e
espera a conexão. Se o NXBT acusa `crashed`, ele reinicia.

## Mundo: `fireredia.mundo`

Tudo é lido do decomp em tempo de execução e guardado em cache (`functools.lru_cache`):

- **`mapa.py`**: cabeçalhos de mapa, layouts, blocos, grades de colisão e elevação, comportamentos de metatile,
  conexões, portas, objetos (NPCs, itens, pedras, árvores), tabelas de selvagens e o desenho usado na localização.
- **`conhecimento.py`**: espécies (atributos, tipos, evoluções, golpes por nível, compatibilidade com TM/HM), golpes,
  tabela de tipos, fórmulas de dano, captura e experiência, itens, presentes e trocas tirados dos scripts dos mapas, e
  ajuda para planejar o time.
- **`roteiro.py`**: a história como marcos em ordem. Cada marco diz onde acontece, o que exige e quais *portões* abre:
  guardas de Saffron, o Snorlax, a Cycling Road, as conferências de insígnia da Rota 23. Os portões são tiles
  bloqueados para o navegador até o marco ser cumprido. `dados/detonado/` é um detonado de 17 seções escrito para o
  agente e indexado por marco e por mapa.

## Habilidades: `fireredia.habilidades`

A **navegação** (`navegacao.py`) é um Dijkstra sobre estados `(mapa, x, y, elevação)` que cobrem o mundo inteiro. Um
vizinho pode ser:
- um passo;
- um pulo de degrau;
- uma porta, incluindo as que um script abre trocando o metatile;
- uma divisa com o mapa seguinte;
- entrar ou sair do Surf, e sair da água só vale para elevação 3, como em `CanStopSurfing`;
- uma seta giratória, seguida até onde para;
- Cut ou Rock Smash no tile da frente.

Grama alta custa mais, e tile de NPC também. Os quebra-cabeças de pedra têm planejador próprio (`plano_da_pedra`): uma
busca em largura sobre *(posição da pedra, região alcançável pelo jogador)*, seguindo `TryPushBoulder`.

A execução é em malha fechada. O plano sai em trechos, o quadro é localizado depois de cada um e os desvios são
contados. Duas tentativas sem sair do lugar marcam o tile como bloqueado, o que cobre NPCs que o dado não mostra, e a
rota é replanejada. Destino longe usa FLY até a melhor cidade visitada. Batalha selvagem no caminho vai para um
resolvedor, que é o piloto automático durante a campanha e "sempre fugir" nas missões.

As **batalhas** (`batalha.py`) nunca apertam A às cegas. Antes de confirmar, elas conferem se a setinha está na ação,
no golpe ou no Pokémon certos, porque o jogo ignora toques enquanto a caixa abre. O **piloto de selvagens**
(`piloto.py`) reconhece a espécie pelo sprite. Se a espécie ainda falta na Pokédex, enfraquece com um golpe que não
derruba e joga a bola; senão, foge (ou luta, no modo treino). A **batalha contra treinador** (`combate.py`) identifica
o treinador pelo texto de abertura, simula a luta com as fórmulas do jogo e decide turno a turno. Líderes, rivais,
Elite dos 4, lutas duplas e qualquer luta que a simulação não vença com folga voltam para o modelo.

**Menus** (`menus.py`): menu START, time e páginas do resumo (espécie, nível, HP, golpes e PP), bolsos da mochila,
lojas, o PC (guardar, tirar, mover entre caixas), usar itens e golpes de campo, salvar, curar, FLY conferindo o
letreiro e `tornar_shiny` (ver [ACE](ace.md)).

## Agente: `fireredia.agente`

Os episódios alternam entre dois papéis:

| | Estrategista | Executor |
|---|---|---|
| Modelo padrão | Claude Opus (`claude-opus-5-5`) | Claude Sonnet (`claude-sonnet-5-5`) |
| Turnos por episódio | 30 | 60 |
| Função | ler a memória e o detonado, definir objetivo, estratégia e um plano em passos | jogar o plano passo a passo com as ferramentas |

O executor devolve ao estrategista a cada 4 episódios, depois de 2 episódios sem concluir um passo ou quando pede
replanejamento. Cada episódio começa de um resumo novo e compacto da memória, então o contexto com imagens nunca
cresce de um episódio para o outro.

As ~60 ferramentas de `ferramentas.py` caem em cinco grupos:

- **Ver:** `ver_tela`.
- **Agir em alto nível:** `ir_para`, `falar_com`, `lutar`, `capturar`, `enfraquecer_e_capturar`, `curar`, `comprar`,
  `guardar_no_pc`, `pescar`, `empurrar_pedra`, `coletar_itens`, `obter_pokemon`, `treinar`...
- **Botão cru**, quando nada serve: `apertar`.
- **Conhecimento:** `info_mapa`, `onde_encontrar`, `info_treinador`, `avaliar_time`, `decidir_golpe_novo`, `roteiro`,
  `detonado`, `pokemon_faltando`...
- **Memória:** `atualizar_memoria`, `registrar_evento`, `anotar`, `concluir_marco`.

Toda ferramenta confere a tela antes e depois de agir e devolve um relato curto e, quando ajuda, o quadro.

Claude roda pelo Agent SDK com configuração isolada: sem configurações, skills ou servidores MCP do usuário. GPT
(Responses API) e Gemini rodam num laço próprio de chamadas de ferramenta em `provedores.py`, com o mesmo prompt, as
mesmas ferramentas e a mesma memória.

## Memória: `fireredia.estado`

- `memoria/estado.json`: o presente. Guarda time, mochila com quantidades, PC, Pokédex, marcos, insígnias, mapas
  visitados, plano, estratégia, contadores e custo.
- `memoria/eventos.jsonl`: o histórico, só de acréscimo. Registra cada decisão, plano, batalha, captura, item ganho ou
  gasto, troca de mapa e save. O [`docs/campanha.md`](../campanha.md) é gerado a partir dele.

Leituras da tela (time, mochila, PC) atualizam o estado quando ele envelhece. O modelo fica sabendo o que foi lido e o
que mudou.

## Missões e ACE: `fireredia.missoes`, `fireredia.ace`

O pós-jogo foi jogado por roteiros determinísticos construídos sobre as mesmas habilidades. As partes de planejamento
puro ficam em `missoes/planos.py`: a busca do triângulo do Deoxys e a de deslize no gelo. Elas recebem só grades de
colisão, então têm testes unitários com grades sintéticas. Ver [ACE e pós-jogo](ace.md).

## Decisões de projeto

- **Sem ler a memória do jogo.** Ler a RAM eliminaria quase todo o trabalho de percepção, mas o objetivo era jogar o
  console como uma pessoa joga. A exceção é o ACE, que altera o jogo *de dentro do próprio jogo*.
- **O decomp como base de conhecimento.** Tabela escrita à mão envelhece. Ler o código-fonte dá mapas, colisão e
  fórmulas exatos e mantém os dados do jogo fora deste repositório.
- **Código para reflexo, modelo para julgamento.** Andar, selvagens e menus são determinísticos e baratos. O modelo é
  chamado para planos, lutas de treinador que pedem raciocínio e qualquer imprevisto.
- **Malha fechada em tudo.** Cada macro é curta e seguida de conferência. Sequências longas às cegas foram a principal
  fonte de falhas no começo.
- **Import sem efeito colateral.** Caminhos e o `.env` ficam em `caminhos.py`, o navegador e a memória são montados
  por `contexto.contexto()` no primeiro uso e o decomp é lido sob demanda.
