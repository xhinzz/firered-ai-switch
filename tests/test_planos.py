"""Planejamento puro: triângulo do Deoxys e gelo deslizante, em grades sintéticas (sem decomp)."""

import numpy as np

from fireredia.missoes import planos


def _simular_deoxys(colisao, plano, inicio):
    """Refaz o plano passo a passo e confere as regras do jogo (passos permitidos, triângulo como obstáculo)."""
    pos = inicio
    for k, (rota, face, triangulo) in enumerate(plano, start=1):
        assert triangulo == planos.DEOXYS_POSICOES[k]
        assert len(rota) <= planos.DEOXYS_PASSOS[k - 1]
        for d in rota:
            vx, vy = planos.DIRECOES[d]
            pos = (pos[0] + vx, pos[1] + vy)
            assert not colisao[pos[1], pos[0]] and pos != triangulo
        vx, vy = planos.DIRECOES[face]
        assert (pos[0] + vx, pos[1] + vy) == triangulo  # tocou de frente


def test_deoxys_em_campo_aberto():
    colisao = np.zeros((30, 30), bool)
    colisao[0, :] = colisao[-1, :] = colisao[:, 0] = colisao[:, -1] = True
    plano = planos.plano_deoxys(colisao)
    assert plano is not None and len(plano) == 10
    _simular_deoxys(colisao, plano, (15, 13))


def test_deoxys_sem_solucao_quando_ilhado():
    colisao = np.ones((30, 30), bool)
    colisao[13, 15] = False  # só o tile de partida
    assert planos.plano_deoxys(colisao) is None


def test_deslize_para_na_pedra_e_fora_do_gelo():
    colisao = np.zeros((7, 7), bool)
    gelo = np.zeros((7, 7), bool)
    gelo[1:6, 1:6] = True
    colisao[1, 4] = True  # pedra no gelo
    assert planos.deslizar(colisao, gelo, (1, 1), "DIREITA") == (3, 1)  # para antes da pedra
    assert planos.deslizar(colisao, gelo, (1, 1), "BAIXO") == (1, 6)  # sai do gelo e para no chão
    gelo[:] = False
    assert planos.deslizar(colisao, gelo, (1, 1), "BAIXO") == (1, 2)  # chão comum: um tile


def test_plano_gelo_acha_caminho_dando_a_volta():
    colisao = np.ones((6, 6), bool)
    colisao[1:5, 1:5] = False
    gelo = ~colisao
    colisao[1, 3] = True  # pedra no caminho
    rota = planos.plano_gelo(colisao, gelo, (1, 4), (2, 1))
    pos = (1, 4)
    for d in rota:
        pos = planos.deslizar(colisao, gelo, pos, d)
    assert pos == (2, 1)
