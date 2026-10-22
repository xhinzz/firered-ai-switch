"""Dispara o código das caixas: Weedle (Caixa 1, casa 3) trocado duas vezes, na mão laranja, com a 0x0351 (Caixa 3, casa 1).

Cada etapa é conferida pelo painel PKMN DATA: um toque perdido no Switch pegava outro Pokémon ou deixava a 0x0351 na
mão, e o código rodava (ou não) com o PC num estado inesperado.
"""

from fireredia import sessao
from fireredia.ace import caixas
from fireredia.habilidades import menus
from fireredia.percepcao import olhos

PECA = "WEEDLE"


def _segurando():
    p = menus._no_painel(olhos.assentar(0.6, prazo=2.0))
    return p and p[0]


def disparar(salvar=True):
    """Confere as Caixas 13/14, salva (se o código travar o jogo, nada se perde) e dispara. Levanta erro se algo sair
    do roteiro; o PC fica na Caixa 1."""
    if not caixas.livres_13_14():
        raise RuntimeError("Caixa 13 (casa 7 em diante) ou Caixa 14 ocupada: limpe o bad egg antes de disparar")
    if salvar:
        print(menus.salvar(), flush=True)
    caixas.abrir()
    sessao.apertar("BAIXO", espera=0.8)
    if _segurando() != PECA:
        raise RuntimeError(f"a casa 3 da Caixa 1 não é o {PECA}: {_segurando()}")
    sessao.apertar("SELECT", espera=0.8)  # mão laranja (relocate)
    sessao.apertar("A", espera=1.2)
    if _segurando() != PECA:
        raise RuntimeError(f"não peguei o {PECA}")
    # casa 3 da Caixa 1 -> título -> Caixa 3 -> casa 1
    sessao.apertar("CIMA", espera=0.8)
    sessao.apertar("DIREITA", "DIREITA", espera=1.4)
    sessao.apertar("BAIXO", espera=0.8)
    sessao.apertar("ESQUERDA", "ESQUERDA", espera=0.7)
    sessao.apertar("A", espera=2.0)  # troca: a 0x0351 vem para a mão
    sessao.apertar("A", espera=3.5)  # troca de volta: o código roda aqui
    if _segurando() != PECA:
        raise RuntimeError(f"a mão não voltou a segurar o {PECA}: confira a tela antes de salvar")
    sessao.apertar("CIMA", espera=0.8)
    sessao.apertar("ESQUERDA", "ESQUERDA", espera=1.4)
    sessao.apertar("BAIXO", espera=0.8)
    sessao.apertar("A", espera=1.2)  # devolve o Weedle à casa 3
    sessao.apertar("SELECT", espera=0.6)
    sessao.apertar("START", espera=0.8)
    if not caixas.e_caixa1():
        raise RuntimeError("o disparo terminou fora da Caixa 1")
    menus.fechar_tudo(prazo=10)
    return "código disparado; Weedle de volta à Caixa 1, casa 3"
