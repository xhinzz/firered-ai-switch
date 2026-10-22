"""Gera os dados do site (site/dados, site/mapas, site/sprites) a partir da memória da campanha e do decomp.

O replay mostra a campanha como ela foi gravada pela IA (memoria/eventos.jsonl): posição a cada evento, decisões,
time, insígnias, marcos e capturas. Os mapas visitados são desenhados do decomp; os sprites saem dele também.
Uso: python scripts/gerar_site.py
"""

import io
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from fireredia import caminhos  # noqa: E402
from fireredia.mundo import mapa  # noqa: E402
from fireredia.painel import painel  # noqa: E402

SITE = RAIZ / "site"
ANO = 2026
TEXTO_MAX = 320
IMAGENS = [
    "campanha.gif",
    "painel.png",
    "localizacao.png",
    "plano_deoxys.png",
    "plano_gelo.png",
    "deoxys_shiny.png",
    "hooh_navel_rock.png",
    "lugia_navel_rock.png",
    "mewtwo_cerulean_cave.png",
    "deoxys_birth_island.png",
    "time_caes.png",
    "icefall_gelo.png",
    "ruby_path_pedras.png",
    "batalha.png",
    "ace_nomes_das_caixas.png",
]
# lendários do pós-jogo (jogados por roteiro, fora do diário do agente) para a galeria
LENDARIOS = ["MEWTWO", "SUICUNE", "ENTEI", "RAIKOU", "HO_OH", "LUGIA", "DEOXYS"]


def _segundos(t):
    return int(datetime.strptime(f"{t} {ANO}", "%d/%m %H:%M:%S %Y").timestamp())


def _time_da_leitura(texto):
    return [[esp, int(nv)] for esp, nv in re.findall(r"([A-Z][A-Z_.'♀♂-]+) nv(\d+)", texto.split("|")[0])]


def _com_posicao(eventos):
    """Eventos com local completo; capturas e afins gravam só o nome do mapa: herdam a última posição conhecida."""
    ultima = None
    for e in eventos:
        local = e.get("local")
        if isinstance(local, dict) and "x" in local:
            ultima = local
        elif isinstance(local, str) and ultima:
            e["local"] = ultima if ultima["mapa"] == local else {"mapa": local, "x": -1, "y": -1}
        elif ultima:
            e["local"] = ultima
        else:
            continue
        yield e


def _salvar_sprite(png, destino):
    """Alguns sprites do decomp trazem dois quadros empilhados (64x128): fica o primeiro."""
    img = Image.open(io.BytesIO(png))
    img.crop((0, 0, img.width, min(img.height, img.width))).save(destino, optimize=True)


def _desenho(mapa_id):
    borda = mapa.BORDA * 16
    img = Image.fromarray(mapa.renderizar_mapa(mapa_id))
    img = img.crop((borda, borda, img.width - borda, img.height - borda))
    return img.convert("P", palette=Image.ADAPTIVE, colors=64)


def gerar():
    eventos = [json.loads(linha) for linha in (caminhos.MEMORIA / "eventos.jsonl").open(encoding="utf-8")]
    estado = json.loads((caminhos.MEMORIA / "estado.json").read_text(encoding="utf-8"))
    eventos = list(_com_posicao(eventos))
    inicio = _segundos(eventos[0]["t"])
    tipos, mapas, linhas = [], [], []
    times, insignias, marcos, capturas = [], [[0, "Boulder"]], [], []
    for i, e in enumerate(eventos):
        if e["tipo"] not in tipos:
            tipos.append(e["tipo"])
        m = e["local"]["mapa"]
        if m not in mapas:
            mapas.append(m)
        texto = re.sub(r"[A-Za-z]:\\+(?:[^\'\"\s]+\\+)*", "", e["texto"])  # caminhos locais em mensagens de erro
        texto = texto if len(texto) <= TEXTO_MAX else texto[: TEXTO_MAX - 1] + "…"
        linhas.append(
            [
                _segundos(e["t"]) - inicio,
                e.get("ep", 0),
                tipos.index(e["tipo"]),
                mapas.index(m),
                e["local"]["x"],
                e["local"]["y"],
                texto,
            ]
        )
        if e["tipo"] == "leitura" and e["texto"].startswith("time"):
            times.append([i, _time_da_leitura(e["texto"])])
        elif e["tipo"] == "insignia" and (nome := re.search(r"insígnia (\w+)", e["texto"])):
            insignias.append([i, nome[1]])
        elif e["tipo"] == "historia" and e["texto"].startswith("marco "):
            marcos.append([i, e["texto"].split(":", 1)[-1].strip() or e["texto"]])
        elif e["tipo"] == "captura" and (cap := re.match(r"([A-Z][A-Z_.'♀♂-]+) nv (\d+)", e["texto"])):
            capturas.append([i, cap[1], int(cap[2])])

    (SITE / "mapas").mkdir(parents=True, exist_ok=True)
    tamanhos = {}
    for m in mapas:
        img = _desenho(m)
        tamanhos[m] = [img.width // 16, img.height // 16]
        img.save(SITE / "mapas" / f"{m}.png", optimize=True)

    especies = {esp for _, time in times for esp, _ in time} | {c[1] for c in capturas} | set(LENDARIOS)
    (SITE / "sprites").mkdir(exist_ok=True)
    for esp in sorted(especies):
        png = painel.sprite_pokemon(esp)
        if png:
            _salvar_sprite(png, SITE / "sprites" / f"{esp}.png")
    (SITE / "sprites" / "shiny").mkdir(exist_ok=True)
    for esp in LENDARIOS:  # todos ficaram shiny pelo ACE: a galeria usa a paleta shiny do decomp
        pasta = painel.GRAFICOS / "pokemon" / painel._pasta_especie(esp)
        png = painel._rgba(pasta / "front.png", pasta / "shiny.pal")
        _salvar_sprite(png, SITE / "sprites" / "shiny" / f"{esp}.png")
    (SITE / "sprites" / "insignias.png").write_bytes(painel.sprite_insignias())

    c = estado.get("contadores", {})
    dados = {
        "inicio": eventos[0]["t"],
        "resumo": {
            "episodios": sum(1 for e in eventos if e["tipo"] == "episodio"),
            "acoes": sum(1 for e in eventos if e["tipo"] == "acao"),
            "decisoes": sum(1 for e in eventos if e["tipo"] == "decisao"),
            "capturas": c.get("capturas"),
            "batalhas": c.get("batalhas_terminadas"),
            "tempo_jogo": estado.get("tempo_jogo"),
        },
        "tipos": tipos,
        "mapas": [[m, *tamanhos[m]] for m in mapas],
        "eventos": linhas,
        "times": times,
        "insignias": insignias,
        "marcos": marcos,
        "capturas": capturas,
    }
    (SITE / "dados").mkdir(exist_ok=True)
    (SITE / "dados" / "campanha.json").write_text(
        json.dumps(dados, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    (SITE / "img").mkdir(exist_ok=True)
    for nome in IMAGENS:
        shutil.copy2(RAIZ / "docs" / "img" / nome, SITE / "img" / nome)
    return len(linhas), len(mapas), len(especies)


if __name__ == "__main__":
    eventos, mapas, especies = gerar()
    print(f"site: {eventos} eventos, {mapas} mapas, {especies} espécies")
