"""Navegação: caminho entre quaisquer dois pontos do mundo (portas e divisas de mapa) e execução com correção pela tela."""

import heapq
import json
import logging
import re
import time
from collections import deque
from functools import lru_cache

import numpy as np

from fireredia.controle import maos
from fireredia.habilidades import batalha
from fireredia.mundo import mapa
from fireredia.percepcao import olhos, texto

PASSO = 0.134  # s por tile correndo (8 frames); andando são 16
GIRO = 0.12  # mudar de direção: o jogo vira primeiro e só anda se o botão continuar apertado (medido ~0,1-0,13 s)
LATENCIA = 0.25  # comando -> tela mudar, medido ~215 ms (Bluetooth + app do Switch + captura)
ANIMACAO_CAMPO = 2.8  # Cut/Surf: a animação segue ~2,6 s depois que a caixa de texto fecha e ignora o controle
log = logging.getLogger("navegacao")
MAX_SEGMENTO = 10  # tiles por comando antes de conferir a posição
MB = mapa.comportamentos()
OPOSTA = {"CIMA": "BAIXO", "BAIXO": "CIMA", "ESQUERDA": "DIREITA", "DIREITA": "ESQUERDA"}
CONEXAO = {"CIMA": "up", "BAIXO": "down", "ESQUERDA": "left", "DIREITA": "right"}
PULOS = {
    MB["MB_JUMP_EAST"]: "DIREITA",
    MB["MB_JUMP_WEST"]: "ESQUERDA",
    MB["MB_JUMP_NORTH"]: "CIMA",
    MB["MB_JUMP_SOUTH"]: "BAIXO",
}
SETAS = {
    MB["MB_EAST_ARROW_WARP"]: "DIREITA",
    MB["MB_WEST_ARROW_WARP"]: "ESQUERDA",
    MB["MB_NORTH_ARROW_WARP"]: "CIMA",
    MB["MB_SOUTH_ARROW_WARP"]: "BAIXO",
    # escada de prédio (Underground Path, portarias): dispara em cima dela andando para o lado da escada
    # (field_control_avatar.c, IsDirectionalStairWarpMetatileBehavior), não ao pisar
    MB["MB_UP_LEFT_STAIR_WARP"]: "ESQUERDA",
    MB["MB_DOWN_LEFT_STAIR_WARP"]: "ESQUERDA",
    MB["MB_UP_RIGHT_STAIR_WARP"]: "DIREITA",
    MB["MB_DOWN_RIGHT_STAIR_WARP"]: "DIREITA",
}
# tile que bloqueia a saída nessa direção (metatile_behavior.c: Is{East,West,North,South}Blocked)
BLOQUEIO = {
    d: {MB[f"MB_IMPASSABLE_{s}"] for s in sufixos}
    for d, sufixos in {
        "DIREITA": ("EAST", "NORTHEAST", "SOUTHEAST"),
        "ESQUERDA": ("WEST", "NORTHWEST", "SOUTHWEST"),
        "CIMA": ("NORTH", "NORTHEAST", "NORTHWEST"),
        "BAIXO": ("SOUTH", "SOUTHEAST", "SOUTHWEST"),
    }.items()
}
AGUA = {
    MB[n]
    for n in (
        "MB_POND_WATER",
        "MB_FAST_WATER",
        "MB_DEEP_WATER",
        "MB_WATERFALL",
        "MB_OCEAN_WATER",
        "MB_UNUSED_WATER",
        "MB_CYCLING_ROAD_WATER",
        "MB_EASTWARD_CURRENT",
        "MB_WESTWARD_CURRENT",
        "MB_NORTHWARD_CURRENT",
        "MB_SOUTHWARD_CURRENT",
    )
}
GRAMA = {MB["MB_TALL_GRASS"]}
# ponytail: correnteza empurra o surf (Seafoam B3F/B4F só param com as pedras do Strength, quebra-cabeça que fica com o
# modelo): bloqueada, o caminho para Cinnabar sai por Pallet e pela Rota 21
CORRENTEZA = {
    MB[n] for n in ("MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT", "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT")
}
# setas do Rocket Hideout: giram e empurram até o tile amarelo ou até bater (field_player_avatar.c)
GIROS = {
    MB["MB_SPIN_RIGHT"]: "DIREITA",
    MB["MB_SPIN_LEFT"]: "ESQUERDA",
    MB["MB_SPIN_UP"]: "CIMA",
    MB["MB_SPIN_DOWN"]: "BAIXO",
}
PARA_GIRO = MB["MB_STOP_SPINNING"]
# ponytail: a Cycling Road não é modelada — bicicleta obrigatória anda 2 tiles no toque de 1 e a ladeira
# (MB_CYCLING_ROAD_PULL_DOWN) puxa para o sul quando o botão solta. Custo alto faz o caminho dar a volta por Celadon
# enquanto houver outro; modelar velocidade da bicicleta e a ladeira se ela virar caminho único
CICLOVIA = {"MAP_ROUTE17": 20}
WARP_AO_PISAR = {v for n, v in MB.items() if any(k in n for k in ("WARP", "DOOR", "LADDER", "ESCALATOR"))} - set(SETAS)
# obstáculo que só some com o golpe certo; o resto dos objetos (NPCs, itens) pode já ter saído do lugar
OBSTACULOS = {"CUT_TREE": "cut", "ROCK_SMASH_ROCK": "rock_smash", "PUSHABLE_BOULDER": "strength"}


@lru_cache
def _warps_por_tile(m):
    return {(x, y): (d, dx, dy) for x, y, d, dx, dy in mapa.warps(m)}


@lru_cache
def _objetos(m):
    """{(x, y): golpe necessário ou None}"""
    return {(x, y): OBSTACULOS.get(gfx) for x, y, gfx, *_ in mapa.objetos(m)}


PORTA_SCRIPT = 8  # custo extra de passar onde um script pode ter aberto: fechada, vira bloqueado e replaneja


@lru_cache
def _portas_de_script():
    """{mapa: {(x, y)}} que scripts abrem com setmetatile (quiz da Blaine, interruptor da mansão, Victory Road...).
    O mapa estático só tem o estado inicial; o atual depende de flags, que não dá para ler da tela."""
    dados = mapa.RAIZ / "data"
    por_pasta = {d["name"]: m for m, d in mapa.mapas().items()}
    res = {}

    def juntar(m, bloco):
        for x, y, tile, col in re.findall(r"setmetatile\s+(\d+),\s*(\d+),\s*(\w+),\s*(\w+)", bloco):
            if col in ("0", "FALSE") and "Statue" not in tile:
                res.setdefault(m, set()).add((int(x), int(y)))

    for f in (dados / "maps").glob("*/scripts.inc"):
        if f.parent.name in por_pasta:
            juntar(por_pasta[f.parent.name], f.read_text(encoding="utf-8"))
    mansao = (dados / "scripts" / "pokemon_mansion.inc").read_text(encoding="utf-8")  # um arquivo para os 4 andares
    for andar, bloco in re.findall(
        r"PokemonMansion_EventScript_(?:Press|Reset)Switch_(\w+)::\n(.*?)\breturn", mansao, re.S
    ):
        juntar(f"MAP_POKEMON_MANSION_{andar}", bloco)
    return res


class Mundo:
    """Grafo de estados (mapa, x, y, elevação) com as regras de movimento do jogo."""

    def __init__(self):
        self.bloqueados = set()  # (mapa, x, y) que travaram na execução: NPC parado, objeto, dado divergente
        self.liberados = set()  # árvore/pedra já removida neste trajeto (voltam quando o mapa recarrega)
        self.evitar_grama = True
        self.golpes = set()  # golpes de campo utilizáveis (conhecimento.capacidades): cut, rock_smash, surf...
        self.portoes = set()  # (mapa, x, y) que a história ainda fecha (roteiro.portoes)

    def _entrar(self, m, x, y, z, d, comp_atual, desembarque=False):
        """Estado ao pisar em (x, y) vindo na direção d, ou None se bloqueado."""
        col, elev, comp = mapa.grade(m)
        b = comp[y, x]
        fechado = col[y, x] and (x, y) not in _portas_de_script().get(m, ())
        if (
            comp_atual in BLOQUEIO[d]
            or b in BLOQUEIO[OPOSTA[d]]
            or fechado
            or (m, x, y) in self.bloqueados
            or (m, x, y) in self.portoes
        ):
            return None
        e = elev[y, x]
        if b in AGUA:  # só surfando; cachoeira precisa de Waterfall
            return (m, x, y, e) if "surf" in self.golpes and b != MB["MB_WATERFALL"] and b not in CORRENTEZA else None
        if (
            z and e not in (0, 15) and e != z and (not desembarque or e != 3)
        ):  # IsElevationMismatchAt; CanStopSurfing só em 3
            return None
        return (m, x, y, z if e == 15 else e)

    def _deslizar(self, m, x, y, z, d):
        """Onde o giro para: cada seta muda a direção, o amarelo para, bater para (TryUpdatePlayerSpinDirection)."""
        col, _, comp = mapa.grade(m)
        h, w = col.shape
        vistos = set()
        while comp[y, x] != PARA_GIRO:
            d = GIROS.get(comp[y, x], d)
            if (x, y, d) in vistos:
                return None  # giro em círculo: o planejador não usa
            vistos.add((x, y, d))
            vx, vy = mapa.DIRECOES[d]
            novo = self._entrar(m, x + vx, y + vy, z, d, comp[y, x]) if 0 <= x + vx < w and 0 <= y + vy < h else None
            if not novo:
                break
            _, x, y, z = novo
        return m, x, y, z

    def vizinhos(self, est):
        m, x, y, z = est
        col, elev, comp = mapa.grade(m)
        h, w = col.shape
        atual = comp[y, x]
        na_agua = atual in AGUA
        warps = _warps_por_tile(m)
        if (x, y) in warps and atual in SETAS:
            d, dx, dy = warps[(x, y)]
            yield 1, (d, dx, dy, 0), ("seta", SETAS[atual])
        for d, (vx, vy) in mapa.DIRECOES.items():
            nx, ny = x + vx, y + vy
            if not (0 <= nx < w and 0 <= ny < h):
                for direcao, viz, ox, oy in mapa.conexoes(m):
                    wv, hv = mapa.tamanho(viz)
                    if direcao == CONEXAO[d] and 0 <= nx - ox < wv and 0 <= ny - oy < hv:
                        novo = self._entrar(viz, nx - ox, ny - oy, z, d, atual)
                        if novo:
                            yield 1, novo, ("passo", d)
                continue
            b = comp[ny, nx]
            if b in PULOS:
                lx, ly = nx + vx, ny + vy
                if PULOS[b] == d and 0 <= lx < w and 0 <= ly < h:
                    novo = self._entrar(m, lx, ly, 0, d, 0)
                    if novo:
                        yield 2, novo, ("pulo", d)
                continue
            # entrada que um script abre (Ruby Path do Mt. Ember): no mapa estático o tile ainda é parede sem warp
            aberta = (nx, ny) in _portas_de_script().get(m, ())
            if (nx, ny) in warps and (b in WARP_AO_PISAR or aberta) and (m, nx, ny) not in self.bloqueados:
                dm, dx, dy = warps[(nx, ny)]  # porta dispara antes da colisão do tile
                yield 2 + (PORTA_SCRIPT if aberta else 0), (dm, dx, dy, 0), ("passo", d)
                continue
            novo = self._entrar(m, nx, ny, z, d, atual, desembarque=na_agua and b not in AGUA)
            if not novo:
                continue
            if b in GIROS:  # pisou na seta: o destino é onde o giro termina, um comando só
                fim = self._deslizar(*novo, d)
                if fim:
                    yield 3, fim, ("giro", d)
                continue
            if b in AGUA and not na_agua:
                yield 4, novo, ("surf", d)  # da margem para a água: "Would you like to use SURF?"
                continue
            objs = _objetos(m)
            if (nx, ny) in objs and (m, nx, ny) not in self.liberados:
                golpe = objs[(nx, ny)]
                if golpe:
                    # ponytail: Strength empurra pedra (quebra-cabeça de Victory Road/Seafoam): fica com o modelo
                    if golpe in self.golpes and golpe != "strength":
                        yield 4, novo, ("campo", d)  # Cut/Rock Smash: remove e entra
                    continue
                custo = 26  # NPC/item na posição inicial: evita, mas passa se for o único caminho
            else:
                custo = 1 + (2 if self.evitar_grama and b in GRAMA else 0)
            if col[ny, nx]:  # só passa aqui porque é porta que um script abre
                custo += PORTA_SCRIPT
            yield custo, novo, ("passo", d)

    def alcancaveis(self, origem, limite=500_000):
        """{mapa: ordem em que a busca chegou nele} a pé de origem com os golpes de campo atuais; a ordem serve de
        distância. Aproximado: guardas e eventos de história não bloqueiam aqui."""
        vistos, fila, mapas_ = {origem}, deque([origem]), {origem[0]: 0}
        while fila and len(vistos) < limite:
            for _, novo, _ in self.vizinhos(fila.popleft()):
                if novo not in vistos:
                    vistos.add(novo)
                    mapas_.setdefault(novo[0], len(mapas_))
                    fila.append(novo)
        return mapas_

    def caminho(self, origem, chegou, limite=300_000):
        """Dijkstra de origem (mapa, x, y, z) até um estado com chegou(estado). Lista de (ação, estado depois)."""
        dist, pai = {origem: 0}, {origem: None}
        fila = [(0, 0, origem)]
        n = 0
        while fila and n < limite:
            c, _, est = heapq.heappop(fila)
            if c > dist[est]:
                continue
            if chegou(est):
                passos = []
                while pai[est]:
                    ant, acao = pai[est]
                    passos.append((acao, est))
                    est = ant
                return passos[::-1]
            n += 1
            for custo, novo, acao in self.vizinhos(est):
                nc = c + custo * CICLOVIA.get(novo[0], 1)
                if nc < dist.get(novo, 1 << 30):
                    dist[novo], pai[novo] = nc, (est, acao)
                    heapq.heappush(fila, (nc, n, novo))
        return None


def objetivo(destino):
    """destino: ("tile", mapa, x, y) | ("mapa", mapa) | ("vizinho", mapa, x, y) | ("algum", {mapas}) -> função de chegada."""
    tipo, m, *xy = destino
    if tipo == "algum":
        return lambda e: e[0] in m
    if tipo == "tile":
        return lambda e: e[0] == m and (e[1], e[2]) == tuple(xy)
    if tipo == "mapa":
        return lambda e: e[0] == m
    return lambda e: e[0] == m and abs(e[1] - xy[0]) + abs(e[2] - xy[1]) == 1


FLY_CUSTO = 60  # passos que um voo "custa" (menu, mapa, animação): só voa quando encurta bem mais que isso
ABERTO = {"MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE"}  # onde o FLY funciona


def _fonte(caminho):
    arq = mapa.RAIZ / caminho
    return arq.read_text(encoding="utf-8") if arq.exists() else texto._git_show(caminho)


@lru_cache
def _celulas_kanto():
    """{MAPSEC: (coluna, linha)} da primeira célula de cada seção no mapa do FLY de Kanto (22 x 15)."""
    camada = re.search(
        r"\[LAYER_MAP\]\s*=\s*\{(.*?)\n    \},", _fonte("src/data/region_map/region_map_layout_kanto.h"), re.S
    )[1]
    celulas = {}
    for y, linha in enumerate(re.findall(r"\{([^{}]*)\}", camada)):
        for x, sec in enumerate(s.strip() for s in linha.split(",")):
            celulas.setdefault(sec, (x, y))
    return celulas


@lru_cache
def destinos_de_voo():
    """{cidade: ((x, y) do pouso, (coluna, linha) no mapa do FLY, nome no letreiro)} das cidades de Kanto."""
    res = {}
    for h in json.loads(_fonte("src/data/heal_locations.json"))["heal_locations"]:
        sec = mapa.mapas()[h["map"]].get("region_map_section")
        if sec in _celulas_kanto() and "ROUTE" not in sec:  # Centros das Rotas 4 e 10 ocupam várias células
            res[h["map"]] = ((h["x"], h["y"]), _celulas_kanto()[sec], sec[len("MAPSEC_") :].replace("_", " "))
    return res


def plano_da_pedra(mundo, m, pedra, alvo, jogador, outras=()):
    """[(tile de onde empurrar, direção)] que leva a pedra até o alvo, ou None. Busca em largura sobre (pedra, região do
    jogador). Regras de TryPushBoulder (field_player_avatar.c): o jogador anda no lugar e a pedra anda 1 tile, se o tile
    da frente não tem colisão, objeto nem porta; outras = posições atuais das outras pedras."""
    col, elev, comp = mapa.grade(m)
    h, w = col.shape
    iniciais = {(x, y) for x, y, gfx, *_ in mapa.objetos(m) if gfx == "PUSHABLE_BOULDER"}
    npcs = {(x, y) for x, y, gfx, *_ in mapa.objetos(m) if gfx != "PUSHABLE_BOULDER"}
    z_pedra = int(elev[pedra[1], pedra[0]])
    portas = set(_warps_por_tile(m))

    def pedra_pode(x, y):
        if 0 <= x < w and 0 <= y < h and comp[y, x] == MB["MB_FALL_WARP"]:
            return (x, y) == alvo  # a pedra cai pelo buraco para o andar de baixo: só serve como destino
        return (
            0 <= x < w
            and 0 <= y < h
            and not col[y, x]
            and int(elev[y, x]) in (z_pedra, 0, 15)
            and comp[y, x] not in AGUA
            and (x, y) not in npcs
            and (x, y) not in outras
            and (x, y) not in portas
        )

    def regiao(p, b):
        """Tiles do mapa que o jogador alcança andando, com a pedra em b."""
        mundo.liberados = {(m, *t) for t in iniciais}  # pedra fora do lugar inicial: a posição atual é que bloqueia
        mundo.bloqueados = {(m, *b)} | {(m, *t) for t in outras}
        _, elev_, _ = mapa.grade(m)
        z = int(elev_[p[1], p[0]])
        ini = (m, *p, 0 if z == 15 else z)
        vistos, fila = {ini}, deque([ini])
        while fila:
            for _, novo, acao in mundo.vizinhos(fila.popleft()):
                if novo[0] == m and acao[0] == "passo" and novo not in vistos:
                    vistos.add(novo)
                    fila.append(novo)
        return {(x, y) for _, x, y, _ in vistos}

    try:
        r0 = regiao(jogador, pedra)
        chave0 = (pedra, min(r0))
        pai, fila = {chave0: None}, deque([(pedra, jogador, r0)])
        while fila:
            b, p, r = fila.popleft()
            if b == alvo:
                passos, k = [], (b, min(r))
                while pai[k]:
                    k, empurrao = pai[k]
                    passos.append(empurrao)
                return passos[::-1]
            for d, (vx, vy) in mapa.DIRECOES.items():
                atras, frente = (b[0] - vx, b[1] - vy), (b[0] + vx, b[1] + vy)
                if atras in r and pedra_pode(*frente):
                    r2 = regiao(atras, frente)
                    k = (frente, min(r2))
                    if k not in pai:
                        pai[k] = ((b, min(r)), (atras, d))
                        fila.append((frente, atras, r2))
        return None
    finally:
        mundo.liberados, mundo.bloqueados = set(), set()


def _segmento(passos):
    """Quantos passos iniciais dá para fazer num comando só: mesma direção, sem porta no meio."""
    acao, est = passos[0]
    if acao[0] != "passo":
        return 1
    n = 1
    while n < len(passos) and n < MAX_SEGMENTO and passos[n][0] == acao and passos[n][1][0] == passos[n - 1][1][0]:
        n += 1
    return n


def ao_ar_livre(m):
    """FLY só funciona ao ar livre, e o mapa que abre é o da região onde se está."""
    dados = mapa.mapas().get(m, {})
    return dados.get("map_type") in ABERTO and dados.get("region_map_section") in _celulas_kanto()


class Navegador:
    def __init__(self, loc: olhos.Localizador, mundo: Mundo | None = None):
        self.loc = loc
        self.mundo = mundo or Mundo()
        self.virado = None  # última direção andada
        self.resolver = None  # resolver(mapa) -> (resolvida, relato): selvagem no caminho (piloto.resolver_selvagem)
        self.resolver_treinador = None  # o mesmo para diálogo no caminho (treinador que viu: piloto.resolver_treinador)
        self.relato = []  # o que o piloto fez nas caminhadas desde a última limpeza
        self.flash = None  # flash() -> texto: usa FLASH do time (caverna escura não deixa localizar)
        self.voar = None  # voar(celula, nome) -> texto: FLY até a cidade dessa célula do mapa de Kanto
        self.visitados = set  # visitados() -> mapas já visitados (destinos possíveis do FLY)

    def _origem(self, pos):
        _, elev, _ = mapa.grade(pos.mapa)
        z = int(elev[pos.y, pos.x]) if 0 <= pos.y < elev.shape[0] and 0 <= pos.x < elev.shape[1] else 0
        return pos.mapa, pos.x, pos.y, 0 if z == 15 else z

    def _talvez_voar(self, chegou, pos):
        """Voa até a cidade visitada de onde o caminho fica bem mais curto que andando; texto do que fez ou None.

        pos é a posição que a caminhada acabou de ler: reler logo depois de uma porta pegava a animação e desistia."""
        if not self.voar or "fly" not in self.mundo.golpes or not ao_ar_livre(pos.mapa):
            return None
        andando = self.mundo.caminho(self._origem(pos), chegou)
        passos = len(andando) if andando is not None else 10**6
        if passos <= FLY_CUSTO:
            return None
        melhor = None
        for cidade, (pouso, celula, nome) in destinos_de_voo().items():
            if cidade in self.visitados():
                p = self.mundo.caminho(self._origem(olhos.Posicao(cidade, *pouso, 1.0, True)), chegou, limite=60_000)
                if p is not None and (melhor is None or len(p) < melhor[0]):
                    melhor = (len(p), cidade, pouso, celula, nome)
        if not melhor or FLY_CUSTO + melhor[0] >= passos:
            return None
        r = self.voar(melhor[3], melhor[4])
        if r.startswith("voou"):
            self.loc.ultima = olhos.Posicao(melhor[1], *melhor[2], 1.0, True)
        return f"{r} ({melhor[0]} passos dali; andando seriam {passos if andando is not None else 'sem caminho'})"

    def _ver(self, esperado=None, espera=3.0):
        """(estado da tela, posição) só depois que a tela assentou: dois quadros seguidos quase iguais.

        Localizar no meio do escurecimento de porta casa mapa errado (caverna escura com 0,83)."""
        # porta: a animação da porta abrindo também "assenta"; espera o mapa novo aparecer
        # (entrada de caverna escurece devagar e mostra a faixa com o nome do lugar)
        troca = esperado and self.loc.ultima and esperado[0] != self.loc.ultima.mapa
        fim = time.monotonic() + (6.0 if troca else espera)
        anterior = None
        while True:
            n = olhos.tela()
            estado = olhos.classificar(n)
            if estado == "dialogo" and not texto.legivel(texto.ler_caixa(n)):
                estado = "outro"  # chão claro de cidade (Celadon) na faixa da caixa de texto: sem letra não é diálogo
            if estado not in ("preto", "outro"):
                return estado, None
            assentou = anterior is not None and np.abs(n.astype(np.int16) - anterior).mean() < 2.0
            anterior = n.astype(np.int16)
            acabou = time.monotonic() > fim
            if (assentou and estado == "outro") or acabou:
                pos = self.loc.localizar(n, esperado, global_=acabou or not troca) if estado == "outro" else None
                if acabou or not troca or (pos and pos.mapa == esperado[0]):
                    if troca and pos and pos.confianca < olhos.CERTO:
                        # escada que não disparou: o andar esperado tem o mesmo canto e casa ~0,81 com a tela de baixo
                        pos = self.loc.conferir(n, pos)
                    return estado, pos
            time.sleep(0.05)

    def empurrar_pedra(self, m, pedra, alvo, outras=()):
        """Leva a pedra até o alvo com STRENGTH: planeja os empurrões (plano_da_pedra) e anda até atrás dela a cada um."""
        _, pos = self._ver()
        if not pos or pos.mapa != m:
            return f"não estou em {m} ({pos and pos.mapa})"
        b, outras = tuple(pedra), {tuple(o) for o in outras}
        plano = plano_da_pedra(self.mundo, m, b, tuple(alvo), (pos.x, pos.y), outras)
        if plano is None:
            return f"não há como levar a pedra de {b} até {tuple(alvo)} com o jogador em ({pos.x},{pos.y})"
        iniciais = {(m, x, y) for x, y, gfx, *_ in mapa.objetos(m) if gfx == "PUSHABLE_BOULDER"}
        for i, (atras, d) in enumerate(plano):
            r = self.ir(("tile", m, *atras), bloquear={(m, *b)} | {(m, *o) for o in outras}, liberar=iniciais)
            if not r.startswith("chegou"):
                return f"empurrão {i + 1} de {len(plano)} (pedra em {b}): {r}"
            maos.apertar(d, segurar=0.05)  # vira para a pedra
            time.sleep(0.3)
            if i == 0:  # A na pedra: pergunta do STRENGTH (ou só o aviso, se já está ativo)
                maos.apertar("A")
                if batalha.avancar(prazo=10) == "sim_nao":
                    batalha.responder(True)
                    olhos.assentar(ANIMACAO_CAMPO)
                    batalha.avancar(prazo=10)  # "X used STRENGTH!" e "...move boulders around!" depois da animação
            # a pedra anda 32 quadros com o controle travado; soltar antes evita um passo a mais depois
            maos.andar(d, 0.3, correr=False)
            time.sleep(0.9)
            vx, vy = mapa.DIRECOES[d]
            b = (b[0] + vx, b[1] + vy)
            self.virado = d
        return f"pedra empurrada até {b} em {len(plano)} empurrões"

    def ir(self, destino, max_passos=400, piloto=True, bloquear=(), liberar=(), voar=True):
        """Anda até o destino. Devolve texto com o resultado: chegou | interrompido (batalha/diálogo) | sem caminho | perdido.

        Com piloto, selvagem no caminho é resolvido por self.resolver(mapa) -> (resolvida, relato) e a caminhada segue;
        o relato fica em self.relato para quem chamou. bloquear/liberar: (mapa, x, y) que a caminhada já começa sabendo
        (pedra empurrada: a posição atual bloqueia e a inicial não)."""
        chegou = objetivo(destino)
        self.mundo.bloqueados = set(bloquear)
        self.mundo.liberados = set(liberar)
        pode_voar = voar and bool(self.voar) and "fly" in self.mundo.golpes  # avaliado na 1ª vez ao ar livre
        plano, esperado, origem, alvo, travadas = None, None, None, None, 0
        falhas = {}  # tile -> tentativas sem sair do lugar
        resolvidas, flash_tentado, desvios, ultima_acao = 0, False, 0, None
        bicicleta = False  # de bicicleta (Cycling Road obriga) virar não gasta tempo: o GIRO a mais vira um tile a mais
        self.virado = None  # entre uma caminhada e outra o modelo pode ter apertado direções
        for _ in range(max_passos):
            estado, pos = self._ver(esperado[:3] if esperado else None)
            # FLASH acaba ao sair para área aberta (overworld.c); entre andares da caverna continua valendo
            if estado == "preto" and self.flash and not flash_tentado and olhos.escuro(olhos.tela()):
                flash_tentado = True
                self.relato.append(f"caverna escura: {self.flash()}")
                continue
            if estado != "outro":
                # "Wild X appeared!" às vezes é lido como diálogo; treinador começa com diálogo sem "Wild"
                selvagem = (
                    estado.startswith("batalha")
                    or estado == "preto"
                    or (estado == "dialogo" and texto.tem(olhos.tela(), "Wild", (100, 160, 0, 240)))
                )
                resolver = self.resolver if selvagem else self.resolver_treinador if estado == "dialogo" else None
                if piloto and resolver and resolvidas < 10:
                    resolvidas += 1
                    ok, rel = resolver(self.loc.ultima.mapa if self.loc.ultima else None)
                    self.relato.append(rel)
                    if ok:
                        plano, esperado, origem = None, None, None
                        continue
                return f"interrompido: {estado}"
            if not pos:
                return "perdido: não reconheço o mapa na tela (menu aberto, cutscene ou área escura)"
            atual = (pos.mapa, pos.x, pos.y)
            if chegou(atual + (0,)):
                if destino[0] == "vizinho":
                    d = next(
                        k for k, (vx, vy) in mapa.DIRECOES.items() if (pos.x + vx, pos.y + vy) == tuple(destino[2:])
                    )
                    maos.apertar(d, segurar=0.03)  # toque curto vira sem andar (ou esbarra no NPC)
                    self.virado = d
                return f"chegou: {pos.mapa} ({pos.x},{pos.y})"
            if pode_voar and ao_ar_livre(pos.mapa):
                pode_voar = False
                if voo := self._talvez_voar(chegou, pos):
                    self.relato.append(voo)
                    plano, esperado, origem = None, None, None
                    continue
            if esperado and atual != esperado[:3]:
                desvios += 1
                log.info("desvio %d: esperava %s depois de %s, está em %s", desvios, esperado[:3], ultima_acao, atual)
                if not bicicleta and ultima_acao[0] == "passo" and origem and origem[0] == pos.mapa:
                    vx, vy = mapa.DIRECOES[ultima_acao[1]]
                    # passou do ponto na direção do passo: toque de 0,18 s (0,06 + GIRO) anda 2 tiles de bicicleta
                    bicicleta = (pos.x - origem[1]) * vx + (pos.y - origem[2]) * vy > ultima_acao[2]
                if desvios > 25:  # nunca chega onde o plano espera (mapa confundido, tela que engana): devolve
                    return f"perdido: a posição não bate com o caminho planejado em {pos.mapa} ({pos.x},{pos.y})"
                if atual == origem and alvo[0] == pos.mapa:
                    # não saiu do lugar duas vezes: o tile da frente está ocupado (NPC parado, objeto que o dado não
                    # mostra). Uma vez só pode ser toque ignorado (tela voltando de batalha ou menu)
                    falhas[alvo[:3]] = falhas.get(alvo[:3], 0) + 1
                    if falhas[alvo[:3]] >= 2:
                        self.mundo.bloqueados.add(alvo[:3])
                    travadas += 1
                    if travadas > 6:
                        return f"travado em {pos.mapa} ({pos.x},{pos.y})"
                plano = None
            if not plano:
                _, elev, _ = mapa.grade(pos.mapa)
                z = int(elev[pos.y, pos.x]) if 0 <= pos.y < elev.shape[0] and 0 <= pos.x < elev.shape[1] else 0
                no = (pos.mapa, pos.x, pos.y, 0 if z == 15 else z)
                plano = self.mundo.caminho(no, chegou)
                if plano is None and pode_voar:  # sem caminho a pé de dentro do prédio/caverna: sai para voar
                    plano = self.mundo.caminho(no, lambda n: ao_ar_livre(n[0]))
                if plano is None:
                    return f"sem caminho de {pos.mapa} ({pos.x},{pos.y}) até {destino}"
            n = _segmento(plano)
            (tipo, d), alvo = plano[0]
            ultima_acao = (tipo, d, n)
            if tipo in ("campo", "surf"):
                # vira para a árvore/pedra/água e aceita "use CUT? / use SURF?"; depois replaneja de onde parar
                maos.apertar(d, segurar=0.03)
                time.sleep(0.3)
                maos.apertar("A")
                if batalha.avancar(prazo=12) == "sim_nao":
                    batalha.responder(True)
                    # passo dado durante a animação se perde duas vezes e o tile vira bloqueado
                    olhos.assentar(ANIMACAO_CAMPO)
                    if tipo == "campo":
                        self.mundo.liberados.add(alvo[:3])
                else:  # sem a pergunta (virada perdida, posição errada): árvore continua lá
                    falhas[alvo[:3]] = falhas.get(alvo[:3], 0) + 1
                    if falhas[alvo[:3]] >= 2:
                        self.mundo.bloqueados.add(alvo[:3])
                self.virado, plano, esperado, origem = d, None, None, None
                continue
            origem, esperado = atual, plano[n - 1][1]
            # direção desconhecida (depois de giro ou de botão do modelo): sem o tempo de virar. Somá-lo com o jogador
            # já virado vira um passo a mais (no labirinto de setas cai numa seta); faltar um passo só replaneja
            giro = GIRO if self.virado is not None and self.virado != d and not bicicleta else 0
            if tipo == "passo":
                # passo começado termina sozinho: basta segurar até o início do último
                maos.andar(d, (n - 1) * PASSO + 0.06 + giro)
            else:
                # pulo e tapete de saída não disparam com toque curto; durante o pulo (~32 frames) o jogo ignora o botão
                maos.andar(d, 0.2 + giro, correr=False)
                time.sleep(0.5)
            time.sleep(LATENCIA)
            self.virado = None if tipo == "giro" else d  # a seta deixa o jogador virado para onde o giro acabou
            plano = plano[n:]
        return "limite de passos atingido"
