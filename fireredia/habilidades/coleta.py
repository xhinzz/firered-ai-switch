"""Coleta de todos os itens de um mapa e obtenção de Pokémon falando com NPCs (presentes, compras, trocas, escolhas)."""

import time

from fireredia.controle import maos
from fireredia.habilidades import batalha
from fireredia.mundo import conhecimento
from fireredia.percepcao import olhos, texto

CAIXA_TEXTO = (110, 160, 0, 240)


def _chave(m, item):
    return f"{m}:{item['x']},{item['y']}"


def assinatura(golpes):
    """Golpes de campo de quando um item ficou fora de alcance; com golpe novo ele volta para a lista."""
    return ",".join(sorted(golpes))


def itens_pendentes(estado, m, golpes=None):
    """Itens do mapa ainda não pegos; com golpes, sem os que já ficaram fora de alcance com esses mesmos golpes."""
    feitos, fora = set(estado.dados["itens_coletados"]), estado.dados.get("itens_fora") or {}
    return [
        i
        for i in conhecimento.itens_dos_mapas().get(m, [])
        if _chave(m, i) not in feitos and (golpes is None or fora.get(_chave(m, i)) != assinatura(golpes))
    ]


def coletar_itens(nav, estado, limite=25):
    """Visita e pega cada item (do chão e escondido) do mapa atual que ainda não está marcado como coletado."""
    m = nav.loc.ultima.mapa
    pendentes, relato = itens_pendentes(estado, m, nav.mundo.golpes), []
    if not pendentes:
        return f"nenhum item pendente alcançável em {m}"
    while pendentes and limite:
        limite -= 1
        p = nav.loc.ultima
        i = min(pendentes, key=lambda it: abs(it["x"] - p.x) + abs(it["y"] - p.y))
        pendentes.remove(i)
        # escondido "debaixo" pega pisando em cima; o resto pega de frente, como placa
        r = nav.ir(("tile" if i["debaixo"] else "vizinho", m, i["x"], i["y"]))
        if r.startswith("interrompido"):
            return "; ".join(relato + [f"parei indo ao {i['item']} ({i['x']},{i['y']}): {r}"])
        if not r.startswith("chegou"):
            relato.append(f"{i['item']} ({i['x']},{i['y']}) fora de alcance: {r}")
            estado.atualizar(
                itens_fora={**(estado.dados.get("itens_fora") or {}), _chave(m, i): assinatura(nav.mundo.golpes)}
            )
            continue
        maos.apertar("A")
        time.sleep(0.8)
        if olhos.classificar(olhos.tela()) == "dialogo":
            batalha.avancar(prazo=15)
            estado.ajustar_item(i["item"], 1, f"achado em {m} ({i['x']},{i['y']})")
            relato.append(f"pegou {i['item']}")
        else:
            relato.append(f"{i['item']} ({i['x']},{i['y']}) já tinha sido pego antes")
        estado.atualizar(itens_coletados=estado.dados["itens_coletados"] + [_chave(m, i)])
    resto, fora = (
        len(itens_pendentes(estado, m, nav.mundo.golpes)),
        len(itens_pendentes(estado, m)) - len(itens_pendentes(estado, m, nav.mundo.golpes)),
    )
    return (
        "; ".join(relato)
        + (
            f" | ainda faltam {resto} alcançáveis neste mapa"
            if resto
            else f" | todos os itens alcançáveis de {m} conferidos"
        )
        + (f" | {fora} fora de alcance com os golpes de campo atuais (volte com HM nova)" if fora else "")
    )


def obter_pokemon(nav, estado, especie, escolher_no_time=None):
    """Vai até o NPC/objeto que dá a espécie (presente, compra, troca, escolha) e conduz a conversa.

    Aceita as perguntas (YES), recusa só o apelido. Troca: escolhe no time a espécie pedida (escolher_no_time)."""
    opcoes = [o for o in conhecimento.obtencao_de(especie) if o["x"] is not None]
    if not opcoes:
        return f"não sei de NPC que dê {especie}"
    o = opcoes[0]
    r = nav.ir(("vizinho", o["mapa"], o["x"], o["y"]))
    if not r.startswith("chegou"):
        return f"não cheguei a quem dá {especie} em {o['mapa']} ({o['x']},{o['y']}): {r}"
    maos.apertar("A")
    time.sleep(0.6)
    recebeu, relato = False, [f"{o['tipo']} em {o['mapa']}"]
    for _ in range(15):
        e = batalha.avancar(prazo=20)
        n = olhos.tela()
        if e == "sim_nao":
            apelido = texto.tem(n, "nickname", CAIXA_TEXTO)
            recebeu = recebeu or apelido
            batalha.responder(not apelido)
            relato.append("apelido: não" if apelido else "respondeu YES")
            continue
        if e == "outro" and o["pede"] and escolher_no_time:
            relato.append(escolher_no_time(o["pede"]))
            continue
        if e in ("batalha_menu", "batalha_texto"):
            return "; ".join(relato + ["começou uma batalha (encontro fixo): capture com enfraquecer_e_capturar"])
        if e == "outro":
            maos.apertar("B")  # ficha nova da Pokédex e telas de recebimento
            time.sleep(0.6)
            continue
        break
    if recebeu:
        estado.registrar_captura(especie, o["nivel"] or 0, f"{o['tipo']} ({o['mapa']})")
    return "; ".join(relato) + (
        " | recebido" if recebeu else " | confira na tela se recebeu (ex.: sem dinheiro, time cheio)"
    )
