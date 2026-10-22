"""Icefall Cave: passos conferidos um a um (gelo fino racha no 1º passo e derruba no 2º) e deslizes no gelo do B1F."""

import time

import numpy as np

from fireredia.controle import maos
from fireredia.habilidades import batalha
from fireredia.missoes import planos, viagem
from fireredia.mundo import mapa
from fireredia.percepcao import olhos, texto

MB_ICE = 0x23  # include/constants/metatile_behaviors.h


def grades(mapa_id):
    """(colisão, gelo) do mapa."""
    colisao, _, comportamento = mapa.grade(mapa_id)
    return colisao.astype(bool), comportamento == MB_ICE


def onde():
    p = batalha.LOC.localizar(olhos.assentar(0.3), global_=True)
    return p and (p.mapa, p.x, p.y)


def andar(*direcoes, pausa=0.55):
    """Um tile por toque, fugindo de selvagem no caminho. Toque que só vira o boneco é repetido uma vez."""
    for d in direcoes:
        antes = onde()
        maos.andar(d, 0.14, correr=False)
        time.sleep(pausa)
        if olhos.classificar(olhos.assentar(0.4)).startswith("batalha") or texto.tem(olhos.tela(), "Wild"):
            viagem.fugir_ou_lutar()
            time.sleep(1.0)
        depois = onde()
        if depois == antes:
            maos.andar(d, 0.14, correr=False)
            time.sleep(pausa)
            depois = onde()
        print(f"  {d}: {antes} -> {depois}", flush=True)
    return onde()


def deslizar_ate(mapa_id, alvo):
    """No gelo do mapa: calcula e executa a sequência de deslizes da posição atual até `alvo`."""
    _, x, y = onde()
    colisao, gelo = grades(mapa_id)
    rota = planos.plano_gelo(colisao, gelo, (x, y), alvo)
    if rota is None:
        raise RuntimeError(f"sem sequência de deslizes de {(x, y)} até {alvo}")
    for d in rota:
        maos.andar(d, 0.25, correr=False)  # toque curto demais só vira o boneco
        time.sleep(2.5)
        print(f"  {d}: {onde()}", flush=True)
    return onde()


def _teste():
    colisao, gelo = grades("MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F")
    assert planos.plano_gelo(colisao, gelo, (16, 9), (17, 13)) == ["CIMA", "DIREITA", "BAIXO", "ESQUERDA"]
    return np.count_nonzero(gelo)
