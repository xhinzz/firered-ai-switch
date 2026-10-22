"""Birth Island: resolve o triângulo pelo plano_deoxys e captura o Deoxys (a batalha abre sozinha no 10º toque)."""

import time

from fireredia.controle import maos
from fireredia.habilidades import batalha, menus
from fireredia.missoes import lendarios, planos, viagem
from fireredia.mundo import mapa
from fireredia.percepcao import olhos
from fireredia.sessao import apertar

MAPA = "MAP_BIRTH_ISLAND_EXTERIOR"
INICIO = (15, 13)  # logo abaixo do triângulo na posição inicial (15,12)


def plano():
    colisao, _, _ = mapa.grade(MAPA)
    return planos.plano_deoxys(colisao.astype(bool), INICIO)


def tocar(direcao):
    maos.andar(direcao, 0.05, correr=False)  # vira para o triângulo (ele bloqueia: não anda)
    time.sleep(0.4)
    apertar("A", espera=2.2)  # o triângulo some e reaparece na próxima posição


def resolver():
    """Salva, faz os 10 toques conferindo a posição a cada trecho e joga a Master Ball."""
    menus.fechar_tudo()
    print(menus.salvar(), flush=True)
    print(viagem.ir(("tile", MAPA, *INICIO), tentativas=3))
    tocar("CIMA")
    atual = INICIO
    for i, (rota, face, triangulo) in enumerate(plano(), start=2):
        for d in rota:
            maos.andar(d, 0.2, correr=False)
            time.sleep(0.45)
            vx, vy = planos.DIRECOES[d]
            atual = (atual[0] + vx, atual[1] + vy)
        p = batalha.LOC.localizar(olhos.assentar(0.4), global_=True)
        print(f"  toque {i}: triângulo em {triangulo}, jogador em {p and (p.x, p.y)} (esperado {atual})", flush=True)
        if not p or (p.x, p.y) != atual:
            raise RuntimeError("saí do plano: o triângulo volta ao início; rode de novo")
        tocar(face)
    lendarios.esperar_batalha(12)
    return lendarios.master()
