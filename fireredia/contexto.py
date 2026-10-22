"""Navegador ligado à memória da campanha: o mesmo que o agente usa, disponível para scripts e missões."""

from dataclasses import dataclass
from functools import cache

from fireredia.estado import Estado
from fireredia.habilidades import batalha, menus, navegacao, piloto
from fireredia.mundo import conhecimento, roteiro
from fireredia.percepcao import olhos


def _quem_sabe(estado, golpe):
    return next(
        (p for p in estado.dados["time"] if any(menus._sem_pp(g) == golpe for g in p.get("golpes") or [])), None
    )


def montar_navegador(estado, loc):
    """Navegador que resolve selvagens e treinadores pelo piloto, acende FLASH em caverna escura e voa quando encurta."""
    nav = navegacao.Navegador(loc)
    nav.resolver = lambda m: piloto.resolver_selvagem(estado, m)
    nav.resolver_treinador = lambda m: piloto.resolver_treinador(estado, m)

    def flash():
        quem = _quem_sabe(estado, "FLASH")
        return (
            menus.usar_golpe_campo(quem["especie"], "FLASH", quem["golpes"]) if quem else "ninguém do time sabe FLASH"
        )

    def voar(celula, nome):
        quem = _quem_sabe(estado, "FLY")
        return menus.voar(quem["especie"], quem["golpes"], celula, nome) if quem else "ninguém do time sabe FLY"

    nav.flash, nav.voar = flash, voar
    nav.visitados = lambda: set(estado.dados["visitados"])
    if (local := estado.dados.get("local")) and loc.ultima is None:
        # interiores com o mesmo desenho (Centros Pokémon) só se distinguem pelo contexto: parte do último local salvo
        loc.ultima = olhos.Posicao(local["mapa"], local["x"], local["y"], 0.0, True)
    return nav


@dataclass
class Contexto:
    estado: Estado
    nav: navegacao.Navegador

    @property
    def dados(self):
        return self.estado.dados

    def atualizar_capacidades(self):
        """Golpes de campo e portões da história a partir do time e dos marcos salvos (depois de ensinar um HM, etc.)."""
        d = self.dados
        self.nav.mundo.golpes = conhecimento.capacidades(d["time"], d["insignias"])
        self.nav.mundo.portoes = roteiro.portoes(frozenset(d["marcos"]), frozenset(d["insignias"]))


@cache
def contexto():
    """Contexto único do processo, criado na primeira chamada (importar os módulos não toca no jogo nem no disco)."""
    estado = Estado()
    ctx = Contexto(estado, montar_navegador(estado, batalha.LOC))
    ctx.atualizar_capacidades()
    return ctx
