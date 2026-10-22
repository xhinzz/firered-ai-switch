"""python -m fireredia.missoes <missão>: missões do pós-jogo por roteiro, com o jogo aberto no Switch.

Exemplos:
    python -m fireredia.missoes plano-deoxys          (offline: mostra os toques do triângulo)
    python -m fireredia.missoes mewtwo
    python -m fireredia.missoes npc-viridian          (depois de disparar um código WILD_*)
    python -m fireredia.missoes balsa NAVEL
    python -m fireredia.missoes ho-oh | lugia | deoxys
    python -m fireredia.missoes guardar SUICUNE 9
    python -m fireredia.missoes ir MAP_CERULEAN_CITY 1 14
"""

import argparse
import logging
import sys


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="python -m fireredia.missoes", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="missao", required=True)
    sub.add_parser("plano-deoxys", help="calcula (sem jogar) os toques do triângulo da Birth Island")
    for nome, ajuda in (
        ("mewtwo", "Cerulean Cave B1F, com Master Ball"),
        ("npc-viridian", "batalha do código WILD_*"),
        ("ho-oh", "cume da Navel Rock"),
        ("lugia", "base da Navel Rock"),
        ("deoxys", "triângulo da Birth Island"),
    ):
        sub.add_parser(nome, help=ajuda)
    b = sub.add_parser("balsa", help="embarca para VERMILION, ONE..SEVEN, NAVEL ou BIRTH")
    b.add_argument("destino")
    g = sub.add_parser("guardar", help="guarda um Pokémon do time na casa 3 de uma caixa")
    g.add_argument("especie")
    g.add_argument("caixa", type=int)
    i = sub.add_parser("ir", help="anda até um tile fugindo de selvagens")
    i.add_argument("mapa")
    i.add_argument("x", type=int)
    i.add_argument("y", type=int)
    a = p.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    logging.basicConfig(level=logging.INFO, format="  %(message)s")

    if a.missao == "plano-deoxys":
        from fireredia.missoes import deoxys

        for k, (rota, face, triangulo) in enumerate(deoxys.plano(), start=2):
            print(f"toque {k:2}: triângulo em {triangulo}, {len(rota)} passos {rota} -> {face}")
        return
    from fireredia.missoes import balsa, deoxys, lendarios, navel_rock, pc, viagem

    acoes = {
        "mewtwo": lambda: lendarios.capturar("MAP_CERULEAN_CAVE_B1F", 7, 13, "CIMA"),
        "npc-viridian": lambda: lendarios.capturar(*lendarios.VIRIDIAN_NPC),
        "ho-oh": navel_rock.ho_oh,
        "lugia": navel_rock.lugia,
        "deoxys": deoxys.resolver,
        "balsa": lambda: balsa.embarcar(a.destino),
        "guardar": lambda: pc.guardar_em_caixa(a.especie.upper(), a.caixa),
        "ir": lambda: viagem.ir(("tile", a.mapa, a.x, a.y)),
    }
    print("RESULTADO:", acoes[a.missao]())


if __name__ == "__main__":
    main()
