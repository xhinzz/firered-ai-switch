"""Teclado da tela de nome de caixa (naming_screen.c): digita conferindo, pela tela, a página e a tecla de cada letra.

Toque perdido no Switch é comum; digitar às cegas trocava letras. Aqui cada caractere só é confirmado depois de ver a
página certa (cor de fundo do teclado) e o cursor (o contorno que pisca) sobre a tecla.
"""

import time

import numpy as np

from fireredia.controle import maos
from fireredia.percepcao import olhos, texto
from fireredia.sessao import apertar

TECLAS = {
    "UPPER": ["ABCDEF .", "GHIJKL ,", "MNOPQRS", "TUVWXYZ"],
    "LOWER": ["abcdef .", "ghijkl ,", "mnopqrs", "tuvwxyz"],
    "SYM": ["01234", "56789", "!?♂♀/-", "…“”‘'"],
}
COLUNAS = {"UPPER": 8, "LOWER": 8, "SYM": 6}
CICLO = ["UPPER", "LOWER", "SYM"]  # SELECT troca na ordem: maiúsculas -> minúsculas -> símbolos -> maiúsculas
XPOS = {
    "UPPER": [0, 12, 24, 56, 68, 80, 92, 123],
    "LOWER": [0, 12, 24, 56, 68, 80, 92, 123],
    "SYM": [0, 22, 44, 66, 88, 110],
}  # x de cada coluna, relativo à primeira tecla (37,5 na tela nativa)
FUNDO = {"UPPER": (123, 182, 205), "LOWER": (227, 163, 114), "SYM": (153, 201, 106)}  # cor dominante de cada página
PAUSA = 0.16


def onde(ch, pagina="UPPER"):
    """(página, linha, coluna) do caractere, preferindo a página atual."""
    for pg in [pagina] + [p for p in CICLO if p != pagina]:
        for r, linha in enumerate(TECLAS[pg]):
            if ch in linha:
                return pg, r, linha.index(ch)
    raise ValueError(f"caractere {ch!r} não está no teclado")


def toque(botao):
    maos.apertar(botao)
    time.sleep(PAUSA)


def tela_de_nome(n=None):
    return texto.achar(olhos.tela() if n is None else n, "BOX NAME?", (28, 50, 60, 170))[0] >= texto.ACHOU


def pagina_na_tela():
    """Página aberta pela cor de fundo do teclado; None se a tela de nome não está aberta ou a cor não é conhecida."""
    n = olhos.tela()
    if not tela_de_nome(n):
        return None
    cores, qtd = np.unique(n[76:146, 22:178].reshape(-1, 3).astype(int), axis=0, return_counts=True)
    dominante = cores[qtd.argmax()]
    dist = {pg: int(np.abs(dominante - np.array(c)).max()) for pg, c in FUNDO.items()}
    pg = min(dist, key=dist.get)
    return pg if dist[pg] < 20 else None


def cursor_na_tela():
    """Centro do contorno do cursor: a única coisa que pisca no teclado (vermelho <-> branco)."""
    quadros = []
    for _ in range(10):
        quadros.append(olhos.tela()[72:150, 15:190].astype(np.int16))
        time.sleep(0.05)
    variacao = np.stack(quadros).std(axis=0).max(axis=2)
    ys, xs = np.nonzero(variacao > 25)
    if len(xs) < 15:
        return None
    return xs.mean() + 15, ys.mean() + 72


def posicao(pagina):
    """(coluna, linha) da tecla sob o cursor."""
    c = cursor_na_tela()
    if c is None:
        return None
    cx, cy = c
    col = min(range(len(XPOS[pagina])), key=lambda i: abs(cx - (37.5 + XPOS[pagina][i])))
    return col, int(round((cy - 87.5) / 16))


def digitar_conferindo(alvo, apagar=0):
    """Digita `alvo` na tela de nome aberta. A tela abre vazia: B no vazio leva o cursor ao botão BACK, então apagar=0."""
    for _ in range(apagar):
        toque("B")
    for ch in alvo:
        pagina = pagina_na_tela()
        pg, r, c = onde(ch, pagina or "UPPER")
        for _ in range(4):
            if pagina == pg:
                break
            toque("SELECT")
            time.sleep(0.35)
            pagina = pagina_na_tela()
        if pagina != pg:
            raise RuntimeError(f"não cheguei à página {pg} para {ch!r}")
        for _ in range(12):
            p = posicao(pagina)
            if p is None:
                raise RuntimeError("cursor fora do teclado")
            x, y = p
            if (x, y) == (c, r):
                break
            toque("DIREITA" if c > x else "ESQUERDA" if c < x else "BAIXO" if r > y else "CIMA")
            time.sleep(0.15)
        if posicao(pagina) != (c, r):
            raise RuntimeError(f"cursor não chegou em {ch!r}")
        toque("A")
        time.sleep(0.15)


def abrir_nome():
    """No título da caixa: A > NAME, conferindo que a tela de nome abriu (senão para sem apertar mais nada)."""
    apertar("A", espera=0.6)
    fim = time.monotonic() + 2.5
    while texto.achar(olhos.tela(), "JUMP", (55, 75, 140, 220))[0] < texto.ACHOU:  # menu JUMP/WALLPAPER/NAME
        if time.monotonic() > fim:
            raise RuntimeError("o menu da caixa não abriu")
        time.sleep(0.2)
    time.sleep(0.3)
    apertar("BAIXO", "BAIXO", espera=0.4)
    for _ in range(3):  # A perdido deixa o menu aberto com NAME marcado: aperta de novo
        apertar("A", espera=2.0)
        for _ in range(10):
            if tela_de_nome():
                time.sleep(0.6)
                return
            time.sleep(0.3)
        if texto.achar(olhos.tela(), "JUMP", (55, 75, 140, 220))[0] < texto.ACHOU:
            break
    raise RuntimeError("a tela de nome não abriu")


def confirmar_nome():
    """START (cursor no OK) + A, insistindo até a tela fechar: um A perdido deixava a tela aberta e o toque seguinte
    escrevia no teclado."""
    toque("START")
    time.sleep(0.5)
    for _ in range(4):
        toque("A")
        time.sleep(2.0)
        if not tela_de_nome():
            time.sleep(0.5)
            return
    raise RuntimeError("a tela de nome não fechou")
