# ACE and post-game missions

[Português](pt-BR/ace.md)

After the Champion, the campaign went on with deterministic scripts: the Sevii post-game quest, the legendaries, and
**arbitrary code execution (ACE)** for what the game no longer offers. That meant more Master Balls, the three
legendary dogs, and shiny versions of everything caught.

| Pokémon | How | Shiny |
|---|---|---|
| Mewtwo | Cerulean Cave B1F after the Sevii quest, Master Ball | ACE |
| Suicune, Entei, Raikou | ACE *Start wild battle* through an NPC, Master Ball | ACE |
| Ho-Oh, Lugia | Navel Rock (MysticTicket), Master Ball | ACE |
| Deoxys | Birth Island triangle puzzle (AuroraTicket), Master Ball | ACE |

<img src="img/deoxys_shiny.png" width="420" alt="Shiny Deoxys summary page">

## How ACE works in FireRed

The research notes, with sources, are in [ace-pesquisa.md](ace-pesquisa.md) (Portuguese). In short:

1. The **Mail glitch** (Mr. Mime + Farfetch'd + Retro Mail in a double battle) produces a corrupted Pokémon that is
   turned into the glitch species **0x0351**.
2. With the 0x0351 in Box 3, slot 1, a "swap twice with the relocate hand" in the PC jumps into memory that holds the
   **names of the PC boxes**.
3. So **a program is written by typing box names**. Each name is up to 8 characters, and each character is a byte of
   ARM code. E-Sh4rk's CodeGenerator turns a program into the 11 names, with an exit routine that returns cleanly to
   the game.

The trigger in this save is the Weedle in Box 1, slot 3, swapped twice with the 0x0351.

<img src="img/ace_nomes_das_caixas.png" width="380" alt="Box names 1 to 11 holding the 'make shiny' code">

*Boxes 1–11 holding the "Make any Pokémon shiny" code (target: Box 10, slot 2).*

## The safe workflow

Typing on the Switch loses keys, and a wrong byte can crash the game or damage the save. Each step therefore checks
the screen:

| Step | Command | Checks |
|---|---|---|
| Generate | `python -m fireredia.ace gerar "<code>" --set Name=value` | Downloads E-Sh4rk's engine and catalogue to `dados/gerador/` (not versioned) and runs it with Node |
| Type | `python -m fireredia.ace digitar <CODE>` | For each character: keyboard page (background colour), cursor position (the blinking outline), then A. Each box is photographed, and a strip of all 11 titles is saved for review |
| Change | `python -m fireredia.ace trocar <OLD> <NEW>` | Retypes only the boxes that differ (the three dog codes differ only in Box 4) |
| Inspect | `python -m fireredia.ace conferir` | Box 13 from slot 7 on and Box 14 must be empty, because the code runs through them; a conversion leftover (Bad Egg) shows up there |
| Trigger | `python -m fireredia.ace disparar` | Checks boxes 13/14, **saves**, checks in the PC panel that the Weedle is in the hand before and after the double swap, and puts it back |
| Shiny | `python -m fireredia.ace shiny MEWTWO` | Moves the Pokémon to Box 10, slot 2, saves, triggers, opens the summary and checks the **shiny star**, then brings it back to the team |

Stored codes (`python -m fireredia.ace codigos`): `SHINY`, `ITEM_MASTER` (5 Master Balls to the PC item storage),
`ITEM_CANDY`, `WILD_SUICUNE` / `WILD_ENTEI` / `WILD_RAIKOU` (the NPC 2 of the current map starts a level-50 battle),
`GIFT_*`, `IVS_*`, `LER_*` (diagnostics). The generator reproduces them exactly. For example,
`gerar "Start wild battle with any Pokemon" --set PokemonHex=0xF5 --set PokemonLV=50` produces `WILD_SUICUNE`.

<img src="img/ace_caixas_do_pc.png" alt="The 14 PC boxes with the code in their names">

## Missions

`python -m fireredia.missoes <mission>`, with the game open. Every capture saves first, so a failed battle never
costs the Pokémon.

### Sevii post-game quest (played step by step on top of the mission helpers)

The Cerulean Cave guard only leaves after Celio's Network Machine works. That required the Ruby (Mt. Ember, Ruby
Path), the Rainbow Pass, the Sapphire (Dotted Hole, Six Island) and the Rocket Warehouse (Five Island). Two
dependencies were not obvious and came out of the decomp:

- The scientist blocking the Dotted Hole door (`SixIsland_RuinValley`) is hidden by a flag that is only set after the
  **Icefall Cave** rescue of Lorelei, and that rescue needs **Waterfall**, whose HM is inside the same cave.
- The Dotted Hole door opens only when **Cut** is used from tile (24,25) facing north (`CutMoveRuinValleyCheck`).

The path-finder needed two rule fixes to get through:
- the Ruby Path entrance is a door opened by a script;
- getting off Surf only works onto elevation 3.

The boulder puzzles were solved by `plano_da_pedra`.

### Icefall Cave: cracked ice and sliding (`missoes/gelo.py`)

On the first floor, stepping twice on thin ice drops you to B1F. On B1F the floor is ice and you slide until you hit
something. `planos.plano_gelo` is a BFS over the stopping points; the route to the HM07 ladder is four slides:

<img src="img/plano_gelo.png" width="300" alt="Four slides on Icefall Cave B1F">

### Navel Rock (`missoes/navel_rock.py`)

The way to Ho-Oh (4 rooms) and to Lugia (11 rooms) is a chain of identical 3×3 ladder rooms, so the screen can't
tell which floor you are on. Each ladder leads to the ladder in the *same* position on the next floor. The walker
therefore enters at one corner, leaves through the opposite one, alternates, and counts rooms. The long corridor of
the Fork is too uniform to localise in, so it is crossed by running into the wall.

### Birth Island: the Deoxys triangle (`missoes/deoxys.py`)

Touching the triangle moves it to the next of 10 positions. If you take more than a fixed number of steps before the
next touch (`sDeoxysStepCaps`: 4, 8, 8, 8, 4, 4, 4, 6, 3, 3), it resets. The 11th touch starts the battle.
`planos.plano_deoxys` is a depth-first search over the side you touch from, because that side decides the distance
to the next position. The plan uses every step budget exactly, and it worked on the first try:

<img src="img/plano_deoxys.png" width="420" alt="Deoxys triangle plan drawn over Birth Island">

```
$ python -m fireredia.missoes plano-deoxys
toque  2: triângulo em (11, 14), 4 passos ['ESQUERDA', 'ESQUERDA', 'ESQUERDA', 'ESQUERDA'] -> BAIXO
toque  3: triângulo em (15, 8), 8 passos ['CIMA', 'CIMA', 'CIMA', 'CIMA', 'DIREITA', 'DIREITA', 'DIREITA', 'DIREITA'] -> CIMA
...
toque 11: triângulo em (15, 10), 3 passos ['CIMA', 'CIMA', 'CIMA'] -> CIMA
```

### All missions

| Command | What it does |
|---|---|
| `plano-deoxys` | Prints the triangle plan (offline) |
| `deoxys` | Saves, plays the 11 touches checking the position after each segment, throws the Master Ball |
| `mewtwo` | Cerulean Cave B1F, Master Ball |
| `ho-oh`, `lugia` | Fork → ladder rooms → summit / base → capture |
| `npc-viridian` | After triggering a `WILD_*` code in the Viridian Pokémon Center: talk to the old man, Master Ball |
| `balsa <DEST>` | Seagallop ferry to `VERMILION`, `ONE`…`SEVEN`, `NAVEL` or `BIRTH`, reading the menus on screen |
| `guardar <SPECIES> <BOX>` | Moves a team member to slot 3 of a given box |
| `ir <MAP> <X> <Y>` | Walks there, running from wild Pokémon and fighting trainers |
