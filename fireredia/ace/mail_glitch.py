"""Passos do Mail glitch (montagem do ACE): dar a RETRO MAIL a um Pokémon e escrever a carta, conferindo cada tela.

Usado só na montagem inicial (docs/ace-pesquisa.md, seções 4.2 e 4.3).
"""

import time

from fireredia.habilidades import menus
from fireredia.percepcao import olhos
from fireredia.sessao import apertar, ler


def esperar(trecho, prazo=4.0):
    fim = time.monotonic() + prazo
    while time.monotonic() < fim:
        if trecho in ler():
            return True
        time.sleep(0.2)
    raise RuntimeError(f"esperava {trecho!r}, a tela diz {ler()!r}")


def abrir_carta_para(posicao):
    """Mochila > RETRO MAIL > GIVE > Pokémon na posição (0-5). Deixa o editor de carta aberto."""
    if not menus.abrir_start("BAG"):
        raise RuntimeError("não abriu a mochila")
    time.sleep(1.2)
    if not menus._apontar_item("RETRO MAIL", menus.BOLSOS["ITEMS"]):
        raise RuntimeError("não achei a RETRO MAIL")
    time.sleep(0.8)
    apertar("BAIXO", espera=0.4)
    apertar("A", espera=1.5)  # GIVE
    if menus.cursor_time(olhos.assentar(0.5, prazo=3.0)) is None or not menus.escolher_no_time(posicao):
        raise RuntimeError("a tela do time não abriu")
    time.sleep(2.0)


def escrever_abra_e_confirmar():
    """Carta com a palavra ABRA (grupo POKéMON), confirmada; o Pokémon passa a segurar a MAIL."""
    esperar("Combine nine words")
    apertar("A", "A", "A", espera=1.2)  # palavra 1 > grupo POKéMON > ABRA
    apertar("START", espera=1.2)
    esperar("Okay?")
    apertar("A", espera=2.0)
    esperar("MAIL to hold")
    apertar("A", espera=1.0)
    menus.fechar_tudo()
