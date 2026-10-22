"""Dados do FireRed vindos do pokefirered (pret): mapas, colisão, portas, conexões e o desenho de cada mapa."""

import json
import re
from functools import lru_cache

import numpy as np
from PIL import Image

from fireredia import caminhos

RAIZ = caminhos.DECOMP
PRIMARIO = 640  # tiles e metatiles do tileset primário (include/fieldmap.h)
PALS_PRIMARIO = 7
BORDA = 7  # metatiles desenhados em volta do mapa (MAP_OFFSET)
DIRECOES = {"CIMA": (0, -1), "BAIXO": (0, 1), "ESQUERDA": (-1, 0), "DIREITA": (1, 0)}


def _ler_pal(caminho):
    return np.array(caminho.read_text().split()[3:], dtype=np.uint8).reshape(-1, 3)  # pula cabeçalho JASC


@lru_cache
def _pastas():
    """Símbolo C (gTilesetTiles_X, gTilesetPalettes_X, gMetatiles_X, gMetatileAttributes_X) -> pasta dos arquivos."""
    arquivos = (
        "src/data/tilesets/graphics.h",
        "src/data/tilesets/metatiles.h",
        "src/graphics.c",
    )  # primários ficam em graphics.c
    texto = "".join((RAIZ / f).read_text() for f in arquivos)
    return {
        s: RAIZ / p
        for s, p in re.findall(r'(\w+)\[\](?:\[16\])? =\s*\{?\s*INCBIN_U\d+\("(data/tilesets/\w+/\w+)/', texto)
    }


@lru_cache
def _cabecalhos():
    """gTileset_X -> símbolos de cada parte; tilesets diferentes compartilham gráficos."""
    texto = (RAIZ / "src/data/tilesets/headers.h").read_text()
    return {
        nome: dict(re.findall(r"\.(tiles|palettes|metatiles|metatileAttributes) = (\w+)", corpo))
        for nome, corpo in re.findall(r"struct Tileset (\w+) =\s*\{(.*?)\};", texto, re.S)
    }


@lru_cache
def _tileset(simbolo):
    cab, pastas = _cabecalhos()[simbolo], _pastas()
    img = np.array(Image.open(pastas[cab["tiles"]] / "tiles.png")) & 0xF
    h, w = img.shape
    tiles = img.reshape(h // 8, 8, w // 8, 8).swapaxes(1, 2).reshape(-1, 8, 8)
    pals = np.stack([_ler_pal(pastas[cab["palettes"]] / "palettes" / f"{i:02}.pal") for i in range(16)])
    metatiles = np.fromfile(pastas[cab["metatiles"]] / "metatiles.bin", dtype="<u2").reshape(-1, 8)
    atributos = np.fromfile(pastas[cab["metatileAttributes"]] / "metatile_attributes.bin", dtype="<u4")
    return tiles, pals, metatiles, atributos


def _completar(arr, n):
    return np.concatenate([arr[:n], np.zeros((n - min(len(arr), n), *arr.shape[1:]), arr.dtype)])


@lru_cache
def comportamentos():
    """MB_* -> valor (include/constants/metatile_behaviors.h)."""
    texto = (RAIZ / "include/constants/metatile_behaviors.h").read_text()
    return {n: int(v, 16) for n, v in re.findall(r"#define (MB_\w+) (0x[0-9A-Fa-f]+)", texto)}


@lru_cache
def mapas():
    """MAP_* -> map.json (portas, NPCs, conexões)."""
    return {m["id"]: m for m in (json.loads(f.read_text()) for f in (RAIZ / "data/maps").glob("*/map.json"))}


@lru_cache
def layouts():
    # layouts.json traz sobras de Ruby/Sapphire sem mapa nenhum; só os usados pelo FireRed
    usados = {m["layout"] for m in mapas().values()}
    return {
        lay["id"]: lay
        for lay in json.loads((RAIZ / "data/layouts/layouts.json").read_text())["layouts"]
        if lay.get("id") in usados
    }


def tamanho(mapa_id):
    lay = layouts()[mapas()[mapa_id]["layout"]]
    return lay["width"], lay["height"]


@lru_cache
def _metas_layout(layout_id):
    lay = layouts()[layout_id]
    t1, p1, m1, a1 = _tileset(lay["primary_tileset"])
    t2, p2, m2, a2 = _tileset(lay["secondary_tileset"])
    return (
        np.concatenate([_completar(t1, PRIMARIO), t2]),
        np.concatenate([p1[:PALS_PRIMARIO], p2[PALS_PRIMARIO:]]),
        np.concatenate([_completar(m1, PRIMARIO), m2]),
        np.concatenate([_completar(a1, PRIMARIO), a2]),
    )


@lru_cache
def grade(mapa_id):
    """(colisão, elevação, comportamento) por tile, cada um (altura, largura)."""
    lay = layouts()[mapas()[mapa_id]["layout"]]
    blocos = np.fromfile(RAIZ / lay["blockdata_filepath"], "<u2").reshape(lay["height"], lay["width"])
    atributos = _metas_layout(lay["id"])[3]
    ids = blocos & 0x3FF
    comp = np.where(ids < len(atributos), atributos[np.minimum(ids, len(atributos) - 1)] & 0x1FF, 0)
    return (blocos >> 10) & 3, blocos >> 12, comp


def _desenhar_metatile(entradas, tiles, pals, fundo):
    bloco = np.empty((16, 16, 3), np.uint8)
    bloco[:] = fundo
    for camada in (entradas[:4], entradas[4:]):  # de baixo pra cima; cor 0 é transparente
        for i, e in enumerate(camada):
            t = tiles[e & 0x3FF] if (e & 0x3FF) < len(tiles) else np.zeros((8, 8), np.uint8)
            if e & 0x400:
                t = t[:, ::-1]
            if e & 0x800:
                t = t[::-1]
            y, x = (i // 2) * 8, (i % 2) * 8
            visivel = t != 0
            bloco[y : y + 8, x : x + 8][visivel] = pals[e >> 12][t][visivel]
    return bloco


@lru_cache
def renderizar(layout_id):
    """Imagem RGB do layout com BORDA metatiles de borda em volta."""
    lay = layouts()[layout_id]
    tiles, pals, metas, _ = _metas_layout(layout_id)
    w, h = lay["width"], lay["height"]
    blocos = np.fromfile(RAIZ / lay["blockdata_filepath"], "<u2").reshape(h, w) & 0x3FF
    borda = np.fromfile(RAIZ / lay["border_filepath"], "<u2").reshape(lay["border_height"], lay["border_width"]) & 0x3FF
    ys, xs = np.mgrid[-BORDA : h + BORDA, -BORDA : w + BORDA]
    grade_ = borda[ys % borda.shape[0], xs % borda.shape[1]]  # mosaico alinhado à origem do mapa (fieldmap.c)
    grade_[BORDA : BORDA + h, BORDA : BORDA + w] = blocos
    cache = {}
    img = np.empty((grade_.shape[0] * 16, grade_.shape[1] * 16, 3), np.uint8)
    for (y, x), mid in np.ndenumerate(grade_):
        if mid not in cache:
            ent = metas[mid] if mid < len(metas) else np.zeros(8, np.uint16)
            cache[mid] = _desenhar_metatile(ent, tiles, pals, pals[0][0])
        img[y * 16 : (y + 1) * 16, x * 16 : (x + 1) * 16] = cache[mid]
    return img


def conexoes(mapa_id):
    """[(direção, mapa vizinho, ox, oy)]: origem do vizinho nas coordenadas deste mapa."""
    w, h = tamanho(mapa_id)
    res = []
    for c in mapas()[mapa_id].get("connections") or []:
        if c["map"] not in mapas() or c["direction"] not in ("up", "down", "left", "right"):
            continue
        wv, hv = tamanho(c["map"])
        o = c["offset"]
        ox, oy = {"up": (o, -hv), "down": (o, h), "left": (-wv, o), "right": (w, o)}[c["direction"]]
        res.append((c["direction"], c["map"], ox, oy))
    return res


@lru_cache
def renderizar_mapa(mapa_id):
    """Desenho do mapa com os mapas conectados colados na borda, como a tela mostra perto da divisa."""
    img = renderizar(mapas()[mapa_id]["layout"]).copy()
    for _, viz, ox, oy in conexoes(mapa_id):
        wv, hv = tamanho(viz)
        rv = renderizar(mapas()[viz]["layout"])[BORDA * 16 : (BORDA + hv) * 16, BORDA * 16 : (BORDA + wv) * 16]
        x0, y0 = (ox + BORDA) * 16, (oy + BORDA) * 16
        cx0, cy0 = max(x0, 0), max(y0, 0)
        cx1, cy1 = min(x0 + rv.shape[1], img.shape[1]), min(y0 + rv.shape[0], img.shape[0])
        if cx1 > cx0 and cy1 > cy0:
            img[cy0:cy1, cx0:cx1] = rv[cy0 - y0 : cy1 - y0, cx0 - x0 : cx1 - x0]
    return img


def warps(mapa_id):
    """[(x, y, mapa destino, x destino, y destino)] — portas, escadas e saídas."""
    res = []
    for w in mapas()[mapa_id].get("warp_events") or []:
        dest = mapas().get(w["dest_map"])
        if not dest:  # MAP_DYNAMIC (elevadores, colosseum)
            continue
        alvos = dest.get("warp_events") or []
        i = int(w["dest_warp_id"])
        if i < len(alvos):
            res.append((w["x"], w["y"], w["dest_map"], alvos[i]["x"], alvos[i]["y"]))
    return res


def objetos(mapa_id):
    """NPCs, itens e obstáculos na posição inicial: [(x, y, gráfico, script, é_treinador, alcance_visão)]."""
    return [
        (
            o["x"],
            o["y"],
            o["graphics_id"].removeprefix("OBJ_EVENT_GFX_"),
            o.get("script", ""),
            o.get("trainer_type", "TRAINER_TYPE_NONE") != "TRAINER_TYPE_NONE",
            o.get("trainer_sight_or_berry_tree_id", "0"),
        )
        for o in mapas()[mapa_id].get("object_events") or []
        if o.get("type", "object") == "object"
    ]


# chance de cada slot da tabela de encontros (src/wild_encounter.c)
_SLOTS = {
    "land_mons": [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1],
    "water_mons": [60, 30, 5, 4, 1],
    "rock_smash_mons": [60, 30, 5, 4, 1],
    "fishing_mons": [70, 30, 60, 20, 20, 40, 40, 15, 4, 1],
}
_METODOS = {"land_mons": "grama/caverna", "water_mons": "surf", "rock_smash_mons": "rock smash"}
_VARAS = ((0, 2, "old rod"), (2, 5, "good rod"), (5, 10, "super rod"))


@lru_cache
def selvagens():
    """MAP_* -> {método: {espécie: (nível mín, nível máx, chance %)}}, versão FireRed."""
    dados = json.loads((RAIZ / "src/data/wild_encounters.json").read_text())
    res = {}
    for e in dados["wild_encounter_groups"][0]["encounters"]:
        if not e["base_label"].endswith("_FireRed"):
            continue
        por_metodo = res.setdefault(e["map"], {})
        for campo, slots in _SLOTS.items():
            mons = (e.get(campo) or {}).get("mons") or []
            faixas = _VARAS if campo == "fishing_mons" else ((0, len(mons), _METODOS[campo]),)
            for ini, fim, metodo in faixas:
                for chance, m in zip(slots[ini:fim], mons[ini:fim], strict=False):
                    esp = m["species"].removeprefix("SPECIES_")
                    a = por_metodo.setdefault(metodo, {}).get(esp, (99, 0, 0))
                    por_metodo[metodo][esp] = (min(a[0], m["min_level"]), max(a[1], m["max_level"]), a[2] + chance)
    return res


def onde_encontrar(especie):
    """[(mapa, método, nível mín, nível máx, chance %)] ordenado pela chance."""
    alvo = especie.upper().replace(" ", "_").removeprefix("SPECIES_")
    return sorted(
        (
            (m, met, *dados[alvo])
            for m, metodos in selvagens().items()
            for met, dados in metodos.items()
            if alvo in dados
        ),
        key=lambda r: -r[4],
    )


def descrever(mapa_id):
    """Resumo em texto para o cérebro: tamanho, saídas, NPCs, itens, placas e Pokémon selvagens."""
    m = mapas()[mapa_id]
    w, h = tamanho(mapa_id)
    linhas = [f"{mapa_id}: {w}x{h} tiles (x 0..{w - 1}, y 0..{h - 1}), tipo {m.get('map_type', '?')}"]
    if conexoes(mapa_id):
        linhas.append("divisas: " + "; ".join(f"{d} -> {viz}" for d, viz, _, _ in conexoes(mapa_id)))
    if warps(mapa_id):
        linhas.append("portas/escadas: " + "; ".join(f"({x},{y}) -> {d}" for x, y, d, _, _ in warps(mapa_id)))
    objs = []
    for x, y, gfx, script, treinador, visao in objetos(mapa_id):
        nome = script.split("_EventScript_")[-1] if script else ""
        objs.append(
            f"({x},{y}) {gfx}{' TREINADOR visão ' + visao if treinador else ''}{' [' + nome + ']' if nome else ''}"
        )
    if objs:
        linhas.append("objetos na posição inicial (podem ter se movido ou sumido): " + "; ".join(objs))
    placas = [
        f"({b['x']},{b['y']}) {b.get('script', '').split('_EventScript_')[-1] or b.get('item', '')}"
        for b in m.get("bg_events") or []
    ]
    if placas:
        linhas.append("placas/itens escondidos: " + "; ".join(placas))
    for metodo, especies in selvagens().get(mapa_id, {}).items():
        linhas.append(
            f"selvagens ({metodo}): "
            + ", ".join(f"{e} {a}-{b} {c}%" for e, (a, b, c) in sorted(especies.items(), key=lambda i: -i[1][2]))
        )
    return "\n".join(linhas)
