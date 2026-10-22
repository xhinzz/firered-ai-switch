"""PC fora do ACE: guardar um Pokémon do time numa caixa escolhida, sem depender da caixa aberta."""

from fireredia.contexto import contexto
from fireredia.habilidades import batalha, menus
from fireredia.percepcao import olhos


def guardar_em_caixa(especie, caixa):
    """Time -> Caixa `caixa`, casa 3 (precisa estar livre), no modo MOVE. Sai do PC na Caixa 1."""
    batalha.LOC.localizar(olhos.tela(), global_=True)
    erro = menus.abrir_armazenamento(contexto().nav, "MOVE")
    if erro:
        return erro
    olhos.assentar(1.0)
    if not menus._voltar_caixa1():
        return "não achei a Caixa 1 pelo nome do código SHINY"
    n = menus._andar_caixas(caixa - 1)
    if 2 in menus._ocupadas(n):
        menus._voltar_caixa1()
        menus.fechar_tudo(prazo=10)
        return f"a Caixa {caixa}, casa 3, está ocupada"
    menus._ap(("CIMA", 0.6), ("A", 0.4))  # botão PARTY POKéMON
    for _ in range(7):
        p = menus._no_painel(olhos.assentar(0.6, prazo=2.0))
        if p and p[0] == especie:
            break
        menus._ap(("BAIXO", 0.2))
    else:
        menus._ap(("B", 1.2))
        menus._voltar_caixa1()
        menus.fechar_tudo(prazo=10)
        return f"{especie} não está no time"
    # MOVE pega; B esconde o time; START = título; BAIXO = casa 3; A abre PLACE; A solta
    menus._ap(("A", 0.6), ("A", 1.0), ("B", 1.2), ("START", 0.6), ("BAIXO", 0.5), ("A", 0.6), ("A", 1.0))
    n = olhos.assentar(1.0, prazo=2.5)
    p = menus._no_painel(n)
    ok = p and p[0] == especie and 2 in menus._ocupadas(n)
    menus._ap(("CIMA", 0.6))
    menus._voltar_caixa1()
    menus.fechar_tudo(prazo=10)
    return f"{especie} na Caixa {caixa}, casa 3" if ok else f"não confirmei {especie} na Caixa {caixa} (painel: {p})"
