"""Caminhada de missão: foge de todo selvagem, luta com treinador (de quem não se foge) e insiste até chegar."""

from contextlib import contextmanager

from fireredia.contexto import contexto
from fireredia.habilidades import batalha, piloto
from fireredia.missoes.conversa import brigar
from fireredia.percepcao import olhos

GOLPES_LUTA = (1, 4, 2)  # posições dos golpes do primeiro do time, em rodízio, quando não dá para fugir

# NPCs que o decomp mostra no lugar mas a história já tirou (a flag que os esconde não é lida da tela). Liberar um tile
# com o NPC ainda lá só faz o navegador esbarrar duas vezes e marcar o tile como bloqueado.
LIBERAR = {
    ("MAP_CERULEAN_CITY", 1, 13),  # guarda da Cerulean Cave: sai quando a Sapphire é entregue ao Celio
    ("MAP_MT_EMBER_EXTERIOR", 41, 40),
    ("MAP_MT_EMBER_EXTERIOR", 42, 40),  # Rockets da entrada do Ruby Path
    ("MAP_SIX_ISLAND_RUIN_VALLEY", 24, 25),  # cientista da porta do Dotted Hole: sai depois da Icefall Cave
    ("MAP_NAVEL_ROCK_BASE", 10, 15),  # Lugia, depois de capturado
}


def fugir_ou_lutar(_mapa=None):
    """Resolvedor de selvagens do navegador: RUN duas vezes; se não der (treinador), luta com GOLPES_LUTA."""
    for _ in range(2):
        batalha.avancar(prazo=10)
        batalha.fugir()
        if batalha.avancar(prazo=15) == "mapa":
            return True, "fugiu"
    return brigar(GOLPES_LUTA) == "fim", "lutou (não deu para fugir)"


@contextmanager
def fugindo():
    """Troca o resolvedor do piloto (que captura e treina) pelo de fuga enquanto durar o bloco."""
    nav = contexto().nav
    antes = nav.resolver
    nav.resolver = fugir_ou_lutar
    try:
        yield nav
    finally:
        nav.resolver = antes


def ir(destino, tentativas=6, liberar=(), **opcoes):
    """Anda até `destino` (formato do Navegador: ("tile", mapa, x, y), ("mapa", mapa)...). Devolve o último relato."""
    r = ""
    with fugindo() as nav:
        for _ in range(tentativas):
            batalha.LOC.localizar(olhos.tela(), global_=True)
            if olhos.classificar(olhos.tela()).startswith("batalha"):
                fugir_ou_lutar()
            r = nav.ir(destino, liberar=LIBERAR | set(liberar), **opcoes)
            print(" ", r, nav.relato[-2:], flush=True)
            if r.startswith(("chegou", "sem caminho")):
                break
    return r


def sincronizar():
    """Relê o time no jogo (depois de ensinar HM, capturar, trocar ordem) e recalcula os golpes de campo."""
    from fireredia.habilidades import menus

    ctx = contexto()
    menus.fechar_tudo()
    r = piloto.sincronizar_time(ctx.estado)
    menus.fechar_tudo()
    ctx.atualizar_capacidades()
    return r
