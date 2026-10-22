# Architecture

[Português](pt-BR/arquitetura.md)

The system is a loop over one 240×160 frame at a time: **see → decide → press → check**. It has four constraints.
The game runs on real hardware, so there is no save-state rewinding. Inputs travel over Bluetooth and get lost.
The only sensor is the picture. And the language model is slow and costs money, so it only handles judgement.

```
           ┌────────────── agente (LLM) ──────────────┐
           │ strategist: plan     executor: ~60 tools │
           └───────────────┬──────────────────────────┘
                           │ tool calls
 percepcao ──frame──▶  habilidades  ──macros──▶  controle ──Bluetooth──▶ Switch
     ▲                     │  ▲                                          │
     │                     ▼  │                                          │
     └──── mundo (decomp: maps, species, font) ◀────── estado (memory)   │
     ▲                                                                   │
     └──────────────────────── HDMI → capture card → OBS ◀───────────────┘
```

## Perception: `fireredia.percepcao`

**Capture** (`olhos.capturar`). The primary source is OBS's windowed projector, grabbed with `PrintWindow` and
`PW_RENDERFULLCONTENT`. That works while the window is covered and takes about 27 ms at 2560×1440. When the projector
is missing or rotated (a monitor that sleeps turns it portrait), it falls back to the OBS Virtual Camera, read on a
background thread. The GBA area is cropped by fixed fractions of the window and resized to the native 240×160.

**Classification** (`olhos.classificar`). Cheap pixel statistics on fixed regions: the blue battle box, the white
text box, the divider of the move list, the yes/no border. The screen falls into one of seven classes, and the map
itself is recognised by localisation, not here.

**Localisation** (`olhos.Localizador`). Every map is rendered from the decomp: tilesets, palettes, metatiles, plus
seven metatiles of border taken from the connected maps. The frame is then matched with normalised cross-correlation:

1. First, a window of ±6 tiles around the last known position on the expected map. This is the common case and takes
   milliseconds.
2. Then the neighbouring maps (connections and warp targets).
3. Finally a global search: every map at ¼ resolution, with the best six refined at full resolution, in about 1 s.

Special cases that became rules:
- **Identical interiors.** All Pokémon Centers share a layout. A tie is resolved by which one can be reached from the
  last position.
- **Floors of the same building** look almost the same, so the floor sign shown on entry ("SILPH CO. 2F") decides.
- **Fog.** On the foggy Pokémon Tower floors the correct match scores 0.42–0.46, so those maps are matched on
  high-pass images with a rescaled threshold.
- A position outside the map's bounds is converted into coordinates of the connected map.

**Text** (`texto.py`). There is no generic OCR. The reader loads the game's glyph sheet, glyph widths and charmap from
the decomp. To *find* a string it draws it in the game font and template-matches it. To *read* free text it segments
lines and matches glyphs one by one. That is how dialogs, menu entries, PC panel names, box titles and HP/level
numbers are read.

**Species.** Front sprites (enemy), back sprites (own) and summary sprites are compared against the decomp's sprites
for the candidate species, such as the wild table of the current map.

## Control: `fireredia.controle`

`servidor_wsl.py` runs as root in WSL (Ubuntu 22.04, because NXBT pins `dbus-python` 1.2.16). It owns the USB
Bluetooth dongle, which is passed through with `usbipd`, emulates a Pro Controller and exposes one HTTP endpoint:
`POST /` with an NXBT macro, `GET /` with the connection state. The client (`maos.py`) holds each button for at least
50 ms. Shorter presses were measured to drop (7 of 8 at 33 ms). `jogar.subir_controle()` attaches the dongle, starts
the server and waits for the connection. If NXBT reports `crashed`, it restarts it.

## World: `fireredia.mundo`

Everything is parsed from the decomp at runtime and cached (`functools.lru_cache`):

- **`mapa.py`**: map headers, layouts, block data, collision and elevation grids, metatile behaviours, connections,
  warps, object events (NPCs, items, boulders, trees), wild encounter tables, and the rendering used by localisation.
- **`conhecimento.py`**: species (stats, types, evolutions, learnsets, TM/HM compatibility), moves, type chart,
  damage, catch and experience formulas, items, gifts and in-game trades from map scripts, and team planning helpers.
- **`roteiro.py`**: the story as ordered milestones. Each milestone has where it happens, what it requires and which
  *gates* it opens: Saffron guards, the Snorlax, the Cycling Road, the badge checks on Route 23. Gates are blocked tiles
  for the navigator until their milestone is done. `dados/detonado/` is a 17-section walkthrough written for the agent
  and indexed by milestone and map.

## Skills: `fireredia.habilidades`

**Navigation** (`navegacao.py`) is Dijkstra over states `(map, x, y, elevation)` that span the whole world. A
neighbour can be:
- a step;
- a ledge jump;
- a warp, including doors that a script opens by changing a metatile;
- a connection to the next map;
- surfing on or off, where leaving the water only works onto elevation 3, as in `CanStopSurfing`;
- spinner tiles followed to where they stop;
- Cut and Rock Smash on the tile ahead.

Tall grass costs extra and so do NPC tiles. Boulder puzzles have their own planner (`plano_da_pedra`): a BFS over
*(boulder position, region the player can reach)* that follows `TryPushBoulder`.

Execution is closed-loop. The plan is sent in segments, the frame is localised after each one, and deviations are
counted. Two failed attempts on the same tile mark it as blocked, which covers NPCs the data doesn't show, and the
route is re-planned. Far destinations use Fly to the best visited town. Wild battles on the way go to a resolver,
which is the autopilot during the campaign and "always run" during missions.

**Battles** (`batalha.py`) never press A blindly. Before confirming, they check that the arrow is on the intended
action, move or Pokémon, because the game ignores input while a box opens. The **wild autopilot** (`piloto.py`)
identifies the species by its sprite. If the species is still missing from the Pokédex, it weakens it with a move that
cannot knock it out and throws a ball; otherwise it runs, or fights in training mode. **Trainer battles**
(`combate.py`) identify the trainer from the opening text, simulate the fight with the game's formulas and play turn
by turn. Gym leaders, rivals, the Elite Four, double battles and any fight the simulation can't win comfortably go
back to the model.

**Menus** (`menus.py`): START menu, team and summary pages (species, level, HP, moves and PP), bag pockets, shops,
the PC (deposit, withdraw, move between boxes), using items and field moves, saving, healing, Fly with label
verification, and `tornar_shiny` (see [ACE](ace.md)).

## Agent: `fireredia.agente`

Episodes alternate between two roles:

| | Strategist | Executor |
|---|---|---|
| Default model | Claude Opus (`claude-opus-5-5`) | Claude Sonnet (`claude-sonnet-5-5`) |
| Turns per episode | 30 | 60 |
| Job | read the memory and the walkthrough, set objective, strategy and a step plan | play the plan step by step with tools |

The executor hands back to the strategist every 4 episodes, after 2 episodes without finishing a step, or when it
asks to re-plan. Each episode starts from a fresh, compact summary of the memory, so context with screenshots never
grows across episodes.

The ~60 tools in `ferramentas.py` fall into five groups:

- **Seeing:** `ver_tela`.
- **Acting at a high level:** `ir_para`, `falar_com`, `lutar`, `capturar`, `enfraquecer_e_capturar`, `curar`,
  `comprar`, `guardar_no_pc`, `pescar`, `empurrar_pedra`, `coletar_itens`, `obter_pokemon`, `treinar`...
- **Raw input** when nothing fits: `apertar`.
- **Knowledge:** `info_mapa`, `onde_encontrar`, `info_treinador`, `avaliar_time`, `decidir_golpe_novo`, `roteiro`,
  `detonado`, `pokemon_faltando`...
- **Memory:** `atualizar_memoria`, `registrar_evento`, `anotar`, `concluir_marco`.

Every tool checks the screen before and after it acts and returns a short text report plus, when useful, the frame.

Claude runs through the Agent SDK with an isolated configuration: no user settings, skills or MCP servers. GPT
(Responses API) and Gemini run through a small tool-calling loop in `provedores.py` with the same prompt, tools and
memory.

## Memory: `fireredia.estado`

- `memoria/estado.json`: the present. It holds team, bag with quantities, PC, Pokédex, milestones, badges, visited
  maps, plan, strategy, counters and cost.
- `memoria/eventos.jsonl`: the history, append-only. It records every decision, plan, battle, capture, item gained or
  spent, map change and save. [`docs/campanha.md`](campanha.md) is generated from it.

Reads from the screen (team, bag, PC) refresh the state when it gets old. The model is told what was read and what
changed.

## Missions and ACE: `fireredia.missoes`, `fireredia.ace`

The post-game was played by deterministic scripts built on the same skills. The pure planning parts live in
`missoes/planos.py`: the Deoxys triangle search and the ice-floor slide search. They take collision grids only, so
they are unit-tested on synthetic grids. See [ACE & post-game](ace.md).

## Design decisions

- **No game memory reading.** RAM reading would remove most of the perception work, but the goal was to play the
  console the way a person does. The exception is ACE, which changes the game *from inside the game*.
- **The decomp as the knowledge base.** Hand-written tables drift. Parsing the source gives exact maps, collision and
  formulas, and keeps game data out of this repository.
- **Code for reflexes, a model for judgement.** Walking, wild battles and menus are deterministic and cheap. The model
  is called for plans, trainer fights that need thought and anything unexpected.
- **Closed loop everywhere.** Every macro is short and followed by a check. Long blind sequences were the main
  source of failures early on.
- **No side effects on import.** Paths and `.env` loading live in `caminhos.py`, the navigator and memory are built by
  `contexto.contexto()` on first use, and the decomp is read lazily.
