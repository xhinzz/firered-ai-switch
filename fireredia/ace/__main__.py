"""python -m fireredia.ace <comando>: ferramentas do ACE pelo PC do Centro Pokémon em que o jogador está.

Exemplos:
    python -m fireredia.ace codigos
    python -m fireredia.ace gerar "Start wild battle with any Pokemon" --set PokemonHex=0xF5 --set PokemonLV=50
    python -m fireredia.ace digitar ITEM_MASTER
    python -m fireredia.ace trocar WILD_SUICUNE WILD_ENTEI
    python -m fireredia.ace conferir
    python -m fireredia.ace disparar
    python -m fireredia.ace shiny MEWTWO
"""

import argparse
import logging
import sys

from fireredia.ace.codigos import CODIGOS


def _lista(nome):
    try:
        return CODIGOS[nome.upper()]
    except KeyError:
        raise argparse.ArgumentTypeError(
            f"código desconhecido: {nome} (veja: python -m fireredia.ace codigos)"
        ) from None


def _parametro(texto):
    nome, _, valor = texto.partition("=")
    return nome, valor  # vai para o código como foi escrito (0xF5, 50)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="python -m fireredia.ace", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="comando", required=True)
    sub.add_parser("codigos", help="lista os códigos guardados e seus nomes de caixa")
    g = sub.add_parser("gerar", help="gera nomes de caixa pelo CodeGenerator do E-Sh4rk (precisa do Node.js)")
    g.add_argument("codigo", help="nome no catálogo ou caminho de um .txt")
    g.add_argument("--set", type=_parametro, action="append", default=[], metavar="NOME=VALOR")
    d = sub.add_parser("digitar", help="digita as Caixas 1-11 com um código")
    d.add_argument("lista", type=_lista)
    d.add_argument("--pular", type=int, nargs="*", default=[], help="caixas que já estão certas")
    t = sub.add_parser("trocar", help="redigita só as caixas que mudam de um código para outro")
    t.add_argument("atual", type=_lista)
    t.add_argument("nova", type=_lista)
    sub.add_parser("conferir", help="mostra as casas ocupadas das Caixas 13 e 14 (bad eggs)")
    x = sub.add_parser("disparar", help="confere as Caixas 13/14, salva e dispara o código das caixas")
    x.add_argument("--sem-salvar", action="store_true")
    s = sub.add_parser("shiny", help="deixa um Pokémon do time shiny (código SHINY nas caixas)")
    s.add_argument("especie")
    a = p.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # “ ” ♀ … dos nomes de caixa
    logging.basicConfig(level=logging.INFO, format="  %(message)s")

    if a.comando == "codigos":
        for nome, lista in CODIGOS.items():
            print(f"{nome:15} {' | '.join(lista)}")
    elif a.comando == "gerar":
        from fireredia.ace import gerador

        for k, nome in enumerate(gerador.gerar(a.codigo, **dict(a.set)), start=1):
            print(f"Caixa {k:2}: {nome!r}")
    elif a.comando == "digitar":
        from fireredia.ace import caixas

        print("tira de conferência:", caixas.digitar(a.lista, pular=set(a.pular)))
    elif a.comando == "trocar":
        from fireredia.ace import caixas

        caixas.trocar(a.atual, a.nova)
    elif a.comando == "conferir":
        from fireredia.ace import caixas

        print("livres para o disparo:", caixas.livres_13_14())
    elif a.comando == "disparar":
        from fireredia.ace import disparo

        print(disparo.disparar(salvar=not a.sem_salvar))
    elif a.comando == "shiny":
        from fireredia.contexto import contexto
        from fireredia.habilidades import menus

        print(menus.tornar_shiny(contexto().nav, a.especie))


if __name__ == "__main__":
    main()
