"""Lendários: chegar ao tile, salvar, abrir a batalha e jogar a Master Ball (conferida pelo nome antes de usar)."""

import time

from fireredia.habilidades import batalha, menus
from fireredia.missoes import viagem
from fireredia.percepcao import olhos
from fireredia.sessao import apertar

VIRIDIAN_NPC = ("MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F", 11, 5, "DIREITA")  # senhor (12,5): NPC 2 do código de batalha


def master():
    """Batalha recém-aberta: avança até o menu e joga a Master Ball (a posição no bolso muda quando um tipo acaba)."""
    batalha.avancar()
    for posicao in (1, 2, 3):
        r = batalha.capturar(posicao, bola="MASTER", master=True)
        print(f"  bola na posição {posicao}:", r, flush=True)
        if not r.startswith("na posição"):
            return r
    return "não achei a MASTER BALL no bolso"


def esperar_batalha(toques=6):
    """Passa os textos (grito, "Mew!", cena do Ho-Oh) apertando A até a batalha abrir."""
    for _ in range(toques):
        if olhos.classificar(olhos.assentar(0.6)).startswith("batalha"):
            break
        apertar("A", espera=1.5)
    time.sleep(2)


def capturar(mapa, x, y, direcao=None, salvar=True):
    """Anda até (x, y), salva, vira para `direcao` e fala (direcao=None: o tile já é o gatilho) e captura.

    Salvar antes garante que uma batalha perdida ou uma fuga não custem o lendário: basta recarregar."""
    if salvar:
        menus.fechar_tudo()
        print(menus.salvar(), flush=True)
    r = viagem.ir(("tile", mapa, x, y), tentativas=4)
    if direcao:
        if not r.startswith("chegou"):
            raise RuntimeError(r)
        apertar(direcao, espera=0.5)  # vira sem andar: o lendário ocupa o tile
        apertar("A", espera=1.5)
    esperar_batalha(12)
    return master()
