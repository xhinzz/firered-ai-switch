"""Caixas do PC como memória do código ACE: digitar nomes, trocar só o que muda e conferir as Caixas 13 e 14.

Todas as funções abrem o PC no modo MOVE POKéMON (o Centro Pokémon precisa estar na tela) e saem dele com a Caixa 1
aberta: a caixa aberta ao sair é a que recebe capturas, e o disparo começa sempre pela Caixa 1.
"""

import numpy as np
from PIL import Image

from fireredia import sessao
from fireredia.ace import teclado
from fireredia.ace.codigos import CODIGOS
from fireredia.contexto import contexto
from fireredia.habilidades import batalha, menus
from fireredia.percepcao import olhos, texto

NORMALIZA = {"–": "-", "’": "'"}  # o gerador mostra 0xAE e 0xB4 assim; no teclado são '-' e "'"
CASAS_LIVRES_13 = 6  # da casa 7 em diante a Caixa 13 precisa estar vazia (o código passa por ali); a 14 inteira


def _titulo_e(n, nome):
    # papel de parede claro (céu da Caixa 10) suja a máscara da letra branca: 0,84 no certo, até 0,34 nos outros
    return texto.achar(n, nome, menus.TITULO_ACE, claro=True)[0] >= 0.7


def e_caixa1(n=None, nomes=None):
    """A caixa aberta é a 1? Reconhece pelo primeiro nome de qualquer código conhecido (ou dos `nomes` dados)."""
    n = olhos.assentar(0.5) if n is None else n
    return any(_titulo_e(n, nome) for nome in (nomes or {lista[0] for lista in CODIGOS.values()}))


def abrir():
    """Abre o PC em MOVE POKéMON com o cursor no título da Caixa 1."""
    menus.fechar_tudo(prazo=10)
    batalha.LOC.localizar(olhos.tela(), global_=True)
    erro = menus.abrir_armazenamento(contexto().nav, "MOVE")
    if erro:
        raise RuntimeError(erro)
    olhos.assentar(1.0)
    sessao.apertar("START", espera=0.6)
    n = olhos.assentar(0.5)
    for _ in range(menus.CAIXAS_PC):
        if e_caixa1(n):
            return
        n = menus._andar_caixas(1)
    raise RuntimeError("não achei a Caixa 1 pelo nome: as caixas não têm um código conhecido")


def fechar(caixa_atual):
    """Volta à Caixa 1 e sai do PC."""
    menus._andar_caixas(1 - caixa_atual)
    menus.fechar_tudo(prazo=10)


def nomear(nomes, primeira):
    """Cursor no título da Caixa `primeira`: digita os nomes nela e nas seguintes. Devolve a caixa onde parou."""
    caixa = primeira
    for k, nome in enumerate(nomes):
        if k:
            menus._andar_caixas(1)
            caixa += 1
        teclado.abrir_nome()
        teclado.digitar_conferindo("".join(NORMALIZA.get(c, c) for c in nome))
        sessao.foto(f"cx{caixa}_campo")
        teclado.confirmar_nome()
        sessao.foto(f"cx{caixa}_ok")
        print(f"caixa {caixa}: {nome!r}", flush=True)
    return caixa


def digitar(lista, pular=()):
    """Digita as Caixas 1-11 com o código `lista` (pulando as caixas em `pular`) e monta a tira de conferência."""
    abrir()
    caixa = 1
    for k, nome in enumerate(lista[:11], start=1):
        if k in pular:
            continue
        menus._andar_caixas(k - caixa)
        caixa = nomear([nome], k)
    fechar(caixa)
    return tira_dos_titulos(range(1, 12))


def trocar(atual, nova):
    """Redigita só as caixas em que `nova` difere de `atual` (os códigos de batalha diferem só na Caixa 4)."""
    abrir()
    caixa = 1
    for k, (a, b) in enumerate(zip(atual, nova, strict=False), start=1):
        if a != b:
            menus._andar_caixas(k - caixa)
            caixa = nomear([b], k)
    fechar(caixa)


def conferir_13_14():
    """(casas ocupadas da Caixa 13, da Caixa 14). Bad egg da conversão aparece na 13; o disparo exige as duas livres."""
    abrir()
    o13 = menus._ocupadas(menus._andar_caixas(12))
    o14 = menus._ocupadas(menus._andar_caixas(1))
    if not e_caixa1(menus._andar_caixas(1)):
        raise RuntimeError("não voltei à Caixa 1")
    menus.fechar_tudo(prazo=10)
    return o13, o14


def livres_13_14():
    o13, o14 = conferir_13_14()
    print("caixa 13:", o13, "| caixa 14:", o14, flush=True)
    return not o14 and not any(i >= CASAS_LIVRES_13 for i in o13)


def tira_dos_titulos(caixas, arquivo="titulos"):
    """Junta numa imagem só a faixa do título de cada foto cx<N>_ok.png (3x), para conferir o código de uma vez."""
    faixas = [np.array(Image.open(sessao.FOTOS / f"cx{c}_ok.png").convert("RGB"))[50:120, 290:670] for c in caixas]
    destino = sessao.FOTOS / f"{arquivo}.png"
    Image.fromarray(np.vstack(faixas)).resize((760, 140 * len(faixas)), Image.NEAREST).save(destino)
    return destino
