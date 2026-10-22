"""Ferramentas de bancada para scripts e missões: apertar com pausa, ler a caixa de diálogo e fotografar a tela."""

import time

from PIL import Image

from fireredia import caminhos
from fireredia.controle import maos
from fireredia.habilidades import batalha
from fireredia.percepcao import olhos, texto

FOTOS = caminhos.LOGS / "fotos"


def apertar(*botoes, espera=0.6):
    """Aperta cada botão e espera a animação; para sequência de menu em que cada toque precisa ser visto pelo jogo."""
    for b in botoes:
        maos.apertar(b)
        time.sleep(espera)


def ler():
    """Texto da caixa de diálogo em uma linha."""
    return " ".join(texto.ler_caixa(olhos.tela()).split())


def foto(nome="tela"):
    """Salva a tela 3x (720x480) em logs/fotos/<nome>.png e imprime o tipo de tela, o texto e a posição."""
    FOTOS.mkdir(parents=True, exist_ok=True)
    n = olhos.tela()
    Image.fromarray(n).resize((720, 480), Image.NEAREST).save(FOTOS / f"{nome}.png")
    tipo = olhos.classificar(n)
    p = batalha.LOC.localizar(n) if tipo == "outro" else None
    print(nome, "|", tipo, "|", repr(texto.ler_caixa(n)), "|", p and (p.mapa, p.x, p.y))
    return n
