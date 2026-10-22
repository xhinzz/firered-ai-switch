"""Roteiro da história do FireRed: marcos em ordem, com onde acontecem, o que exigem e o que liberam.

Escrito à mão a partir da história do jogo; os detalhes de cada evento o modelo confere na tela e com info_mapa.
"""

import re
from functools import lru_cache

from fireredia import caminhos
from fireredia.mundo import mapa

MARCOS = [
    ("inicial", "Escolher o Pokémon inicial no laboratório do Oak", "MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB", [], ""),
    (
        "encomenda",
        "Pegar o Oak's Parcel na loja de Viridian e entregar ao Oak (recebe a Pokédex e Poké Balls)",
        "MAP_VIRIDIAN_CITY_MART",
        ["inicial"],
        "Pokédex; loja de Viridian passa a vender",
    ),
    ("floresta", "Atravessar a Floresta de Viridian até Pewter", "MAP_VIRIDIAN_FOREST", ["encomenda"], "Pewter City"),
    (
        "brock",
        "Vencer BROCK (Pewter Gym): Boulder Badge e TM39",
        "MAP_PEWTER_CITY_GYM",
        ["floresta"],
        "FLASH fora da batalha; saída leste de Pewter (Rota 3)",
    ),
    (
        "tenis",
        "Receber os RUNNING SHOES do assistente do Oak na saída leste de Pewter",
        "MAP_PEWTER_CITY",
        ["brock"],
        "correr com B",
    ),
    (
        "mt_moon",
        "Atravessar o Mt. Moon, vencer a Team Rocket e escolher um fóssil (DOME ou HELIX)",
        "MAP_MT_MOON_B2F",
        ["brock"],
        "Rota 4 leste e Cerulean",
    ),
    (
        "rival_cerulean",
        "Batalha com o rival na entrada norte de Cerulean (ponte)",
        "MAP_CERULEAN_CITY",
        ["mt_moon"],
        "",
    ),
    (
        "nugget",
        "Nugget Bridge (Rota 24): cinco treinadores e o Rocket do Nugget",
        "MAP_ROUTE24",
        ["rival_cerulean"],
        "Rota 25",
    ),
    (
        "bill",
        "Ajudar o BILL na casa da Rota 25 (Sea Cottage): recebe o S.S. TICKET",
        "MAP_ROUTE25_SEA_COTTAGE",
        ["nugget"],
        "S.S. Ticket; Rocket da casa roubada sai do caminho",
    ),
    (
        "misty",
        "Vencer MISTY (Cerulean Gym): Cascade Badge e TM03",
        "MAP_CERULEAN_CITY_GYM",
        ["mt_moon"],
        "CUT fora da batalha",
    ),
    (
        "casa_roubada",
        "Com o S.S. TICKET o policial sai da porta da casa roubada: atravessá-la, vencer o Rocket do quintal "
        "(TM28 DIG) e seguir para a Rota 5 (a saída sul tem árvore de CUT e o Slowbro)",
        "MAP_CERULEAN_CITY_HOUSE2",
        ["bill"],
        "caminho para o sul (Rota 5)",
    ),
    ("vermilion", "Rota 5, Underground Path e Rota 6 até Vermilion", "MAP_VERMILION_CITY", ["casa_roubada"], ""),
    (
        "bicicleta",
        "BIKE VOUCHER no Pokémon Fan Club (Vermilion) e trocar pela BICYCLE na loja de Cerulean",
        "MAP_CERULEAN_CITY_BIKE_SHOP",
        ["vermilion"],
        "Bicycle (mais rápida; exigida na Cycling Road)",
    ),
    (
        "ss_anne",
        "Embarcar no S.S. Anne com o S.S. Ticket, vencer o rival e falar com o capitão: HM01 CUT",
        "MAP_SSANNE_CAPTAINS_OFFICE",
        ["vermilion", "bill"],
        "HM01 CUT",
    ),
    ("vara_velha", "OLD ROD com o pescador de Vermilion", "MAP_VERMILION_CITY_HOUSE1", ["vermilion"], "pesca"),
    (
        "surge",
        "Vencer LT. SURGE (Vermilion Gym; árvore de CUT na entrada; latas com interruptores): Thunder Badge e TM34",
        "MAP_VERMILION_CITY_GYM",
        ["ss_anne", "misty"],
        "FLY fora da batalha",
    ),
    (
        "flash",
        "HM05 FLASH com o assistente do Oak na Rota 2 (pede 10 espécies na Pokédex; Diglett's Cave leva lá)",
        "MAP_ROUTE2_EAST_BUILDING",
        ["ss_anne"],
        "HM05 FLASH (Rock Tunnel fica claro)",
    ),
    (
        "rock_tunnel",
        "Rota 9 (CUT) e 10, Centro da Rota 10 e Rock Tunnel (FLASH ajuda) até Lavender",
        "MAP_LAVENDER_TOWN",
        ["misty", "ss_anne"],
        "Lavender Town",
    ),
    ("celadon", "Rota 8, Underground Path e Rota 7 até Celadon", "MAP_CELADON_CITY", ["rock_tunnel"], ""),
    (
        "cha",
        "Receber TEA da senhora da Celadon Mansion (os guardas de Saffron aceitam)",
        "MAP_CELADON_CITY_CONDOMINIUMS_1F",
        ["celadon"],
        "entrar em Saffron",
    ),
    (
        "eevee",
        "Pegar o EEVEE no terraço da Celadon Mansion (quarto do telhado)",
        "MAP_CELADON_CITY_CONDOMINIUMS_ROOF_ROOM",
        ["celadon"],
        "EEVEE",
    ),
    (
        "erika",
        "Vencer ERIKA (Celadon Gym; árvore de CUT): Rainbow Badge e TM19",
        "MAP_CELADON_CITY_GYM",
        ["celadon", "ss_anne"],
        "STRENGTH fora da batalha",
    ),
    (
        "esconderijo",
        "Rocket Game Corner: esconderijo, LIFT KEY, vencer Giovanni: SILPH SCOPE",
        "MAP_ROCKET_HIDEOUT_B4F",
        ["celadon"],
        "Silph Scope",
    ),
    (
        "torre",
        "Pokémon Tower com o Silph Scope: fantasma Marowak, salvar o Mr. Fuji: POKé FLUTE",
        "MAP_POKEMON_TOWER_7F",
        ["esconderijo"],
        "Poké Flute (acorda os Snorlax)",
    ),
    (
        "snorlax",
        "Acordar e capturar os SNORLAX das Rotas 12 e 16 com a Poké Flute",
        "MAP_ROUTE12",
        ["torre"],
        "Rotas 12-15 e 16-18",
    ),
    (
        "fly",
        "HM02 FLY na casa escondida da Rota 16 (atrás de uma árvore de CUT)",
        "MAP_ROUTE16_NORTH_ENTRANCE_1F",
        ["torre", "ss_anne"],
        "HM02 FLY",
    ),
    (
        "fuchsia",
        "Chegar a Fuchsia (Rotas 12-15 ou Cycling Road 16-18 com a Bicycle)",
        "MAP_FUCHSIA_CITY",
        ["snorlax"],
        "",
    ),
    (
        "safari",
        "Safari Zone: HM03 SURF na Secret House e GOLD TEETH; devolver ao Warden: HM04 STRENGTH",
        "MAP_SAFARI_ZONE_WEST_REST_HOUSE",
        ["fuchsia"],
        "HM03 SURF, HM04 STRENGTH",
    ),
    (
        "koga",
        "Vencer KOGA (Fuchsia Gym): Soul Badge e TM06",
        "MAP_FUCHSIA_CITY_GYM",
        ["fuchsia"],
        "SURF fora da batalha",
    ),
    (
        "silph",
        "Saffron (dar o TEA ao guarda) e Silph Co.: CARD KEY, rival, Giovanni; LAPRAS no 7F; MASTER BALL",
        "MAP_SILPH_CO_11F",
        ["cha", "torre"],
        "Lapras, Master Ball, Saffron Gym aberto",
    ),
    (
        "dojo",
        "Vencer o Fighting Dojo de Saffron: escolher HITMONLEE ou HITMONCHAN",
        "MAP_SAFFRON_CITY_DOJO",
        ["silph"],
        "",
    ),
    (
        "sabrina",
        "Vencer SABRINA (Saffron Gym; teletransportes): Marsh Badge e TM04",
        "MAP_SAFFRON_CITY_GYM",
        ["silph"],
        "ROCK SMASH fora da batalha",
    ),
    (
        "cinnabar",
        "Surfar até Cinnabar (pela Rota 21 ou pelas Seafoam Islands)",
        "MAP_CINNABAR_ISLAND",
        ["koga", "safari"],
        "",
    ),
    (
        "chave_secreta",
        "Pokémon Mansion: interruptores, SECRET KEY",
        "MAP_POKEMON_MANSION_B1F",
        ["cinnabar"],
        "Cinnabar Gym",
    ),
    (
        "fosseis",
        "Reviver os fósseis no laboratório de Cinnabar (OMANYTE/KABUTO; Old Amber vira AERODACTYL)",
        "MAP_CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM",
        ["cinnabar"],
        "",
    ),
    (
        "blaine",
        "Vencer BLAINE (Cinnabar Gym; quiz): Volcano Badge e TM38",
        "MAP_CINNABAR_ISLAND_GYM",
        ["chave_secreta"],
        "WATERFALL fora da batalha",
    ),
    (
        "sevii",
        "Ir com o Bill para a One Island e cumprir o pedido de lá (Mt. Ember)",
        "MAP_ONE_ISLAND",
        ["blaine"],
        "Viridian Gym abre na volta",
    ),
    ("giovanni", "Vencer GIOVANNI (Viridian Gym): Earth Badge e TM26", "MAP_VIRIDIAN_CITY_GYM", ["sevii"], ""),
    ("rival_22", "Batalha com o rival na Rota 22", "MAP_ROUTE22", ["giovanni"], "Rota 23"),
    (
        "victory_road",
        "Rota 23 (guardas conferem as 8 insígnias) e Victory Road (pedras de STRENGTH)",
        "MAP_VICTORY_ROAD_3F",
        ["rival_22", "erika"],
        "Indigo Plateau",
    ),
    (
        "liga",
        "Elite dos 4 (Lorelei, Bruno, Agatha, Lance) e o Campeão",
        "MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F",
        ["victory_road"],
        "fim da história",
    ),
]
IDS = [m[0] for m in MARCOS]
# gatilhos de piso que empurram o jogador de volta enquanto a variável não muda: marco que libera
PORTOES_VAR = {"VAR_MAP_SCENE_ROUTE5_ROUTE6_ROUTE7_ROUTE8_GATES": "cha"}
# NPCs que o script do mapa põe no caminho enquanto uma flag não é ligada (setobjectxyperm ao carregar o mapa)
PORTOES_NPC = {
    "bill": [
        ("MAP_CERULEAN_CITY", 30, 12),  # policial na porta da casa roubada (sem FLAG_GOT_SS_TICKET)
        ("MAP_CERULEAN_CITY", 26, 31),
        ("MAP_CERULEAN_CITY", 27, 31),
    ]
}  # Slowbro e a menina na saída sul


@lru_cache(maxsize=32)
def portoes(feitos: frozenset, insignias: frozenset):
    """Tiles (mapa, x, y) que a história ainda fecha: guardas de Saffron sem o TEA, Cycling Road sem a bicicleta,
    guardas de insígnia (Rotas 22/23) e os Snorlax antes da Poké Flute. O mapa sozinho não sabe disso."""
    tem = " ".join(insignias).lower()
    res = set()
    for m, d in mapa.mapas().items():
        for c in d.get("coord_events") or []:
            script = c.get("script", "")
            insignia = re.search(r"([A-Z][a-z]+)BadgeGuard", script)
            if (
                (PORTOES_VAR.get(c.get("var")) not in (None, *feitos))
                or ("NeedBike" in script and "bicicleta" not in feitos)
                or (insignia and insignia[1].lower() not in tem)
            ):
                res.add((m, c["x"], c["y"]))
        for o in d.get("object_events") or []:
            if "SNORLAX" in o.get("graphics_id", "") and "snorlax" not in feitos:
                res.add((m, o["x"], o["y"]))
    for marco, tiles in PORTOES_NPC.items():
        if marco not in feitos:
            res.update(tiles)
    return frozenset(res)


DETONADO = caminhos.DADOS / "detonado"  # seções do detonado (secao_NN.md), com marcos e mapas no cabeçalho


def detonado(chave):
    """[(arquivo, texto)] das seções do detonado cujo cabeçalho cita o marco do roteiro ou o mapa (MAP_...)."""
    achados = []
    for arq in sorted(DETONADO.glob("secao_*.md")):
        texto_ = arq.read_text(encoding="utf-8")
        cabecalho = "\n".join(texto_.splitlines()[:6])
        if re.search(rf"(?<![\w]){re.escape(chave)}(?![\w])", cabecalho):
            achados.append((arq.name, texto_))
    return achados


def proximo_marco(feitos):
    """Primeiro marco do roteiro liberado e ainda não feito."""
    return next((id_ for id_, _, _, req, _ in MARCOS if id_ not in feitos and all(r in feitos for r in req)), None)


LUTAS_VAR = {"VAR_MAP_SCENE_CERULEAN_CITY_RIVAL": "rival_cerulean"}


@lru_cache(maxsize=32)
def lutas_no_caminho(feitos: frozenset):
    """Gatilhos de luta obrigatória ainda não vencida. Só para planejar: o que fica depois deles não está disponível
    antes da vitória (o ir_para passa por eles, porque é lá que a luta acontece)."""
    return frozenset(
        (m, c["x"], c["y"])
        for m, d in mapa.mapas().items()
        for c in d.get("coord_events") or []
        if LUTAS_VAR.get(c.get("var")) not in (None, *feitos)
    )


def texto(feitos: dict):
    """Roteiro com a situação de cada marco e os próximos disponíveis (pré-requisitos cumpridos)."""
    linhas, proximos = [], []
    for id_, desc, mapa_, req, libera in MARCOS:
        feito = id_ in feitos
        pronto = all(r in feitos for r in req)
        if not feito and pronto:
            proximos.append(id_)
        marca = "x" if feito else (">" if pronto else " ")
        linhas.append(f"[{marca}] {id_}: {desc} | {mapa_}" + (f" | libera: {libera}" if libera else ""))
    return f"próximos possíveis: {', '.join(proximos) or 'nenhum'}\n" + "\n".join(linhas)
