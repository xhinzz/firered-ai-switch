"""Diálogo e batalha conduzidos por roteiro: passar texto, responder Sim/Não, lutar com golpes escolhidos."""

import time

from fireredia.habilidades import batalha
from fireredia.percepcao import olhos, texto
from fireredia.sessao import apertar


def falar(maximo=30, resposta=None, primeiro=True):
    """Aperta A enquanto houver diálogo (o primeiro A puxa a conversa) e devolve as falas lidas.

    resposta: "sim"/"nao" para a pergunta Sim/Não que aparecer; None deixa a pergunta aberta."""
    falas = []
    if primeiro:
        apertar("A", espera=1.2)
    for _ in range(maximo):
        tela = olhos.assentar(0.5, prazo=3.0)
        if resposta is not None and olhos.borda_sim_nao(tela):
            batalha.responder(resposta == "sim")
            time.sleep(1.2)
            continue
        fala = " ".join(texto.ler_caixa(tela).split())
        if olhos.classificar(tela) != "dialogo" and not fala:
            break
        if fala and (not falas or falas[-1] != fala):
            falas.append(fala)
            print(" ", fala, flush=True)
        apertar("A", espera=1.0)
    return falas


def brigar(golpes=(1,), limite=40):
    """Luta a batalha aberta com os golpes dados (posições 1-4, em rodízio) até voltar ao mapa. "fim" ou "limite".

    Golpe sem PP sai do rodízio; "trocar de Pokémon?" e "dar apelido?" recebem Não."""
    golpes = tuple(golpes)
    for i in range(limite):
        n = olhos.assentar(0.6, prazo=4.0)
        tipo = olhos.classificar(n)
        if tipo == "batalha_menu":
            r = batalha.lutar(golpes[i % len(golpes)])
            if isinstance(r, str) and "indisponível" in r:
                golpes = golpes[1:] or (1,)
        elif tipo == "sim_nao" or olhos.borda_sim_nao(n):
            batalha.responder(False)
        elif tipo.startswith("batalha") or tipo == "dialogo":
            apertar("A", espera=0.8)
        elif tipo == "golpes":
            apertar("B", espera=0.6)
        elif batalha.LOC.localizar(n, global_=False) is not None:
            return "fim"
        else:
            apertar("B", espera=0.8)
    return "limite"
