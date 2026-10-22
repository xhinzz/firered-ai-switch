"""Navel Rock: salinhas de escada idênticas entre o Fork, o cume (Ho-Oh) e a base (Lugia).

Cada escada leva à escada de mesma posição no andar seguinte, então se entra por um canto e se sai pelo oposto,
alternando (2,2) e (4,4). As salas não se distinguem pela imagem: o andar é deduzido pela contagem.
"""

import time

from fireredia.controle import maos
from fireredia.habilidades import batalha
from fireredia.missoes import lendarios, viagem
from fireredia.percepcao import olhos

SALA = "MAP_NAVEL_ROCK_SUMMIT_PATH_2F"  # todas têm o mesmo desenho 3x3
OPOSTO = {(2, 2): (4, 4), (4, 4): (2, 2)}
ROTAS = {
    (2, 2): [["BAIXO", "BAIXO", "DIREITA", "DIREITA"], ["DIREITA", "DIREITA", "BAIXO", "BAIXO"]],
    (4, 4): [["ESQUERDA", "ESQUERDA", "CIMA", "CIMA"], ["CIMA", "CIMA", "ESQUERDA", "ESQUERDA"]],
}  # neve bloqueia uma
VOLTA = {"BAIXO": "CIMA", "CIMA": "BAIXO", "ESQUERDA": "DIREITA", "DIREITA": "ESQUERDA"}
SALAS_CUME, SALAS_BASE = 4, 11


def posicao_na_sala():
    q = batalha.LOC._no_mapa(olhos.assentar(0.6, prazo=4.0), SALA)
    return q and (q.x, q.y)


def _andar(rota):
    for d in rota:
        maos.andar(d, 0.2, correr=False)
        time.sleep(0.8)
    time.sleep(2.5)


def atravessar(n, canto):
    """Atravessa n salas entrando pelo `canto`. Devolve a posição ao sair delas (Fork, Summit ou Base)."""
    for i in range(n):
        alvo = OPOSTO[canto]
        for rota in ROTAS[canto]:
            _andar(rota)
            g = batalha.LOC.localizar(olhos.tela(), global_=True)
            if g and "PATH" not in g.mapa:
                return g
            if posicao_na_sala() == alvo:
                break
            _andar([VOLTA[d] for d in reversed(rota)])  # bateu na neve no meio: volta ao canto e tenta a outra rota
        print(f"  sala {i + 1}: {canto} -> {alvo}", flush=True)
        canto = alvo
    return batalha.LOC.localizar(olhos.tela(), global_=True)


def correr(direcao, segundos):
    """Corredor longo do Fork: uniforme demais para o localizador, então corre até bater na parede."""
    maos.andar(direcao, segundos, correr=True)
    time.sleep(1.0)
    return batalha.LOC.localizar(olhos.assentar(0.5), global_=True)


def ao_fork_topo():
    """Do porto até o topo do Fork (14,1)."""
    viagem.ir(("mapa", "MAP_NAVEL_ROCK_FORK"), tentativas=4)
    return correr("CIMA", 14.0)


def ate_sair_do_fork(direcao, maximo=26):
    """Anda tile a tile até a escada do topo levar para fora do Fork (um toque depois do warp tiraria do canto)."""
    for _ in range(maximo):
        maos.andar(direcao, 0.2, correr=False)
        time.sleep(0.45)
        g = batalha.LOC.localizar(olhos.assentar(0.4), global_=True)
        if g is None or g.mapa != "MAP_NAVEL_ROCK_FORK":
            time.sleep(2.0)
            return
    raise RuntimeError("não cheguei à escada do Fork")


def ho_oh():
    """Fork -> escada (3,1) -> 4 salas -> cume; o Ho-Oh desce ao pisar em (9,12)."""
    ao_fork_topo()
    ate_sair_do_fork("ESQUERDA")
    print("saiu em", atravessar(SALAS_CUME, (4, 4)))
    return lendarios.capturar("MAP_NAVEL_ROCK_SUMMIT", 9, 12)


def lugia():
    """Fork -> escada (26,1) -> 11 salas -> base; o Lugia fica em (10,15)."""
    ao_fork_topo()
    ate_sair_do_fork("DIREITA")
    print("saiu em", atravessar(SALAS_BASE, (2, 2)))
    return lendarios.capturar("MAP_NAVEL_ROCK_BASE", 10, 16, "CIMA")
