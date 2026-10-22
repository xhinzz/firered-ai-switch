"""Baixa o decomp pret/pokefirered (só as pastas que o projeto lê, ~40 MB) para dados/pokefirered.

Mapas, colisão, gráficos dos tilesets, fonte do jogo, espécies, golpes e roteiros vêm todos daqui: o projeto não
inclui nenhum dado do jogo. Uso: python scripts/baixar_decomp.py [destino]
"""

import subprocess
import sys
from pathlib import Path

URL = "https://github.com/pret/pokefirered.git"
COMMIT = "037335f4c725d7c9aecdac87066f2002b4bd7e14"  # versão em que os caminhos e formatos foram conferidos
PASTAS = [
    "charmap.txt",
    "data/layouts",
    "data/maps",
    "data/scripts/item_ball_scripts.inc",
    "data/tilesets",
    "graphics/fonts",
    "graphics/items",
    "graphics/pokemon",
    "graphics/trainer_card",
    "graphics/trainers",
    "include/constants/items.h",
    "include/constants/opponents.h",
    "include/constants/species.h",
    "src/data/battle_moves.h",
    "src/data/ingame_trades.h",
    "src/data/items.h",
    "src/data/items.json",
    "src/data/pokemon/evolution.h",
    "src/data/pokemon/level_up_learnset_pointers.h",
    "src/data/pokemon/level_up_learnsets.h",
    "src/data/pokemon/species_info.h",
    "src/data/pokemon/tmhm_learnsets.h",
    "src/data/text/move_names.h",
    "src/data/tilesets",
    "src/data/trainer_parties.h",
    "src/data/trainers.h",
    "src/data/wild_encounters.json",
    "src/graphics.c",
]
# lidos com `git show` (fora do checkout esparso): buscar agora deixa o projeto funcionando sem rede depois
SOB_DEMANDA = ["src/battle_main.c", "src/text.c", "src/data/region_map/region_map_layout_kanto.h"]


def git(*args, cwd=None):
    subprocess.run(["git", *args], cwd=cwd, check=True)


def main(destino):
    destino = Path(destino)
    if (destino / ".git").exists():
        print(f"{destino} já existe; conferindo o commit")
    else:
        git("clone", "--filter=blob:none", "--no-checkout", "--sparse", URL, str(destino))
    git("sparse-checkout", "set", "--skip-checks", *PASTAS, cwd=destino)
    git("checkout", "--quiet", COMMIT, cwd=destino)
    for caminho in SOB_DEMANDA:
        subprocess.run(["git", "show", f"HEAD:{caminho}"], cwd=destino, check=True, capture_output=True)
    print(f"decomp pronto em {destino} ({COMMIT[:7]})")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from fireredia import caminhos

    main(sys.argv[1] if len(sys.argv) > 1 else caminhos.DECOMP)
