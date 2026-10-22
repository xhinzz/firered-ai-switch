"""Seagallop: embarca no porto (Vermilion ou ilhas) para uma ilha, a Navel Rock ou a Birth Island, lendo o menu na tela.

Em Vermilion, com os bilhetes de evento, o marinheiro primeiro pergunta SEVII ISLANDS / NAVEL ROCK / BIRTH ISLAND;
nas ilhas o menu lista os destinos em páginas (OTHER passa para a próxima).
"""

import time

from fireredia.controle import maos
from fireredia.habilidades import batalha, menus
from fireredia.missoes import viagem
from fireredia.missoes.conversa import falar
from fireredia.percepcao import olhos, texto
from fireredia.sessao import apertar, ler

DESTINOS = ["SEVII", "NAVEL", "BIRTH", "VERMILION", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"]
MENU = (10, 115, 100, 240)  # região dos menus de destino na tela nativa
VERMILION = ("MAP_VERMILION_CITY", 23, 32)  # pisar em (23,33) chama o marinheiro (24,33) e confere o bilhete


def ler_menu():
    n = olhos.assentar(0.6)
    return [d for d in DESTINOS if texto.tem(n, d, MENU)]


def _escolher(destino):
    """Menu aberto: desce até o destino (passando por SEVII ou OTHER) e confirma."""
    for _ in range(4):
        itens = ler_menu()
        print("  menu:", itens, flush=True)
        if destino in itens:
            apertar(*["BAIXO"] * itens.index(destino), espera=0.35)
            apertar("A", espera=2.0)
            return
        # Vermilion: SEVII é a 1ª opção e abre o menu das ilhas; nas ilhas OTHER fica logo depois dos destinos
        apertar(*(["BAIXO"] * (0 if "SEVII" in itens else len(itens))), espera=0.35)
        apertar("A", espera=1.5)
    raise RuntimeError(f"{destino} não aparece no menu da balsa")


def embarcar(destino):
    """Do mapa até desembarcar no destino ("FOUR", "NAVEL", "VERMILION"...). Devolve a posição na chegada."""
    destino = destino.upper()
    menus.fechar_tudo()
    atual = batalha.LOC.localizar(olhos.tela(), global_=True)
    if atual is None:
        raise RuntimeError("não sei onde estou: abra o jogo no mapa")
    if "_ISLAND" in atual.mapa:
        print(viagem.ir(("tile", atual.mapa.split("_ISLAND")[0] + "_ISLAND_HARBOR", 8, 5)))
        apertar("BAIXO", espera=0.5)
        apertar("A", espera=1.5)
    else:
        print(viagem.ir(("tile", *VERMILION)))
        maos.apertar("BAIXO", segurar=0.25)
        time.sleep(1.5)
    for _ in range(10):  # bilhetes, "Would you like to board...?" até o menu aparecer
        if ler_menu():
            break
        apertar("A", espera=1.0)
    _escolher(destino)
    falar(4, primeiro=False)
    time.sleep(8)  # viagem
    for _ in range(4):
        if olhos.classificar(olhos.assentar(0.6)) != "dialogo":
            break
        apertar("A", espera=1.2)
    time.sleep(1.5)
    for _ in range(4):  # sai do porto: a porta fica três tiles acima do barco
        maos.apertar("CIMA", segurar=0.3)
        time.sleep(0.3)
    time.sleep(2.5)
    p = batalha.LOC.localizar(olhos.tela(), global_=True)
    print("chegou:", p, "|", ler())
    return p
