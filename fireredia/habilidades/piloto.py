"""Piloto automático de batalha selvagem: reconhece as espécies pelas sprites e decide sem chamar o modelo.

Espécie que falta na Pokédex: enfraquece com o golpe que não derruba e captura. Já capturada: foge (ou luta, no modo
treino). Treinador, golpe novo, evolução ou tela estranha: devolve o controle ao modelo.
"""

import re
import time

import numpy as np

from fireredia.controle import maos
from fireredia.habilidades import batalha, combate, menus
from fireredia.mundo import conhecimento, mapa
from fireredia.percepcao import olhos, texto


def _bolas(estado):
    return sum(q for k, q in estado.dados["mochila"].items() if k.endswith("BALL") and k != "MASTER BALL")


def _meu(estado, n):
    time_ = estado.dados["time"]
    esp, nota = olhos.identificar_meu(n, [p["especie"] for p in time_])
    if nota >= olhos.IDENTIFICOU:
        return next((p for p in time_ if p["especie"] == esp), None)
    return time_[0] if time_ else None


def _seguros(meu, especie, nivel, hp):
    """Golpes de dano que não derrubam o selvagem (o dano máximo com crítico deixa 6% de HP): [(dano máx, posição, nome)]."""
    res = []
    for i, g in enumerate((meu.get("golpes") or [])[:4], 1):
        d = conhecimento.dano(g, meu["especie"], meu["nivel"], especie, nivel)
        pp = re.search(r"(\d+)\s*/\s*\d+", g)
        # crítico da Gen 3 dobra o dano; EVs, IV baixo do selvagem e ACID baixando DEF também passam da estimativa
        # (ACID estimado em 19% do HP chegou a tirar 39%)
        if d and d[1] > 0 and not (pp and pp[1] == "0") and hp - 2 * d[1] / d[2] >= 0.06:
            res.append((d[1], i, g.split()[0]))
    return res


def _quem_enfraquece(estado, especie, nivel, hp, atual):
    """Do time, quem tira vida sem derrubar e aguenta o selvagem (nível não muito abaixo e HP bom)."""
    opcoes = [
        (max(s)[0], p)
        for p in estado.dados["time"]
        if p is not atual
        and (p.get("hp") is None or p["hp"] > 0.4)
        and (p.get("nivel") or 0) >= nivel - 4
        and (s := _seguros(p, especie, nivel, hp))
    ]
    return max(opcoes, key=lambda o: o[0])[1] if opcoes else None


def enfraquecer_e_capturar(
    estado, especie, nivel, meu, bola="POKE BALL", posicao=1, chance_minima=0.55, max_bolas=6, status=""
):
    """Loop de turnos como um jogador: golpe mais forte que não derruba enquanto a chance de captura é baixa; se o
    Pokémon em campo derruba com qualquer golpe, troca uma vez para um mais fraco que tire vida; bola quando fica boa."""
    relato, bolas, trocou = [], 0, False
    for _ in range(14):
        n = olhos.tela()
        if olhos.classificar(n) != "batalha_menu":
            e = batalha.avancar()
            if e != "batalha_menu":
                return "; ".join(relato + [f"parou: tela {e}"])
            n = olhos.tela()
        hp = olhos.hp_inimigo(n)
        if hp is None:
            return "; ".join(relato + ["não achei a barra de HP do inimigo"])
        p = conhecimento.chance_captura(especie, hp, bola, status) or 0
        seguros = _seguros(meu, especie, nivel, hp)
        if not seguros and p < chance_minima and not trocou:
            outro = _quem_enfraquece(estado, especie, nivel, hp, meu)
            if outro:
                trocou = True
                r = trocar(outro["especie"])
                relato.append(f"{meu['especie']} derrubaria: entra {outro['especie']} para tirar vida ({r})")
                if r.startswith(combate.PRESO):  # segue com quem está em campo
                    continue
                if r != "batalha_menu":
                    return "; ".join(relato)
                meu = outro
                continue
        if p >= chance_minima or (not seguros and (hp <= 0.5 or p >= 0.25)):
            if bolas >= max_bolas or _bolas(estado) <= 0:
                return "; ".join(relato + [f"sem bolas para continuar (chance {p:.0%})"])
            bolas += 1
            r = batalha.capturar(
                posicao,
                bola=bola,
                master=especie in conhecimento.LENDARIOS,
                ao_arremessar=lambda: (
                    estado.ajustar_item(bola, -1, f"arremessada em {especie}"),
                    estado.contar("bolas_usadas"),
                ),
            )
            relato.append(f"HP {hp:.0%}, chance {p:.0%}: bola -> {r}")
            if r.startswith("na posição"):  # bola errada na posição: nada foi jogado
                return "; ".join(relato)
            if r == "capturou":
                estado.registrar_captura(especie, nivel, f"capturado com {bola} após enfraquecer")
                return "; ".join(relato)
            if r != "escapou":
                return "; ".join(relato)
            continue
        if not seguros:
            return "; ".join(
                relato
                + [
                    f"HP {hp:.0%}, chance {p:.0%}: nenhum golpe de {meu['especie']} é seguro "
                    "(todos podem derrubar). Troque para um Pokémon mais fraco ou use sono/paralisia"
                ]
            )
        _, i, nome = max(seguros)
        r = _lutar(estado, meu, i)
        relato.append(f"HP {hp:.0%}, chance {p:.0%}: {nome} (golpe {i})")
        if r == "mapa":
            return "; ".join(relato + ["o selvagem desmaiou ou fugiu antes da bola"])
        if r not in ("batalha_menu", "golpes", "batalha_texto"):
            return "; ".join(relato + [f"parou: tela {r}"])
    return "; ".join(relato + ["parei depois de 14 turnos"])


def _lutar(estado, meu, i):
    """batalha.lutar com a memória em dia: PP do golpe usado e HP de quem está em campo."""
    gastar_pp(estado, meu["especie"], i)
    r = batalha.lutar(i)
    if r == "batalha_menu":
        anotar_hp(estado, olhos.tela())
    return r


def _melhor_golpe(meu, especie, nivel, evitar=()):
    opcoes = []
    for i, g in enumerate(meu.get("golpes") or [], 1):
        pp = re.search(r"(\d+)\s*/\s*\d+", g)
        d = conhecimento.dano(g, meu["especie"], meu["nivel"], especie, nivel)
        if d and d[1] > 0 and not (pp and pp[1] == "0") and i not in evitar:
            opcoes.append(((d[0] + d[1]) / 2, i))
    return max(opcoes)[1] if opcoes else next((i for i in range(1, 5) if i not in evitar), 1)


def resolver_treinador(estado, mapa_atual):
    """Diálogo que parou a caminhada: passa o texto e, se virar luta de treinador comum, o combate luta sozinho.

    Devolve (resolvida, relato); luta importante, dupla, arriscada ou estranha volta para o modelo."""
    combate.ultima_abertura["texto"] = ""
    if not texto.ler_caixa(olhos.tela()) and batalha.LOC.localizar(olhos.tela(), global_=False):
        return True, ""  # o classificador viu diálogo no piso claro: segue andando
    e = batalha.avancar()
    if e == "mapa":
        return True, "diálogo no caminho"
    if e != "batalha_menu" or not combate.ultima_abertura["texto"]:
        return False, f"diálogo parou em {e}"
    ok, relato = combate.lutar_treinador(estado, mapa_atual, lambda p, i: _lutar(estado, p, i), trocar)
    if ok:
        estado.contar("batalhas_terminadas")
        estado.contar("vitorias")
        estado.evento("batalha", relato)
    return ok, relato


def trocar(especie):
    """Na batalha: POKéMON, a espécie (achada pelo nome na tela) e SHIFT, a primeira opção do submenu.

    Devolve o estado final. Também serve para a escolha depois de um desmaio (a tela do time já está aberta)."""
    if olhos.classificar(olhos.tela()) == "batalha_menu" and batalha.abrir("POKEMON") != "aberto":
        return "não consegui abrir POKéMON"
    posicao = menus.posicao_na_tela(olhos.assentar(0.8), especie)
    if posicao is None:
        maos.apertar("B")
        return f"{especie} não aparece na tela do time"
    for _ in range(3):
        if not menus.escolher_no_time(posicao):
            maos.apertar("B")
            return "não achei o cursor na tela do time"
        olhos.assentar(0.4, prazo=2.0)  # submenu SHIFT / SUMMARY / CANCEL
        maos.apertar("A")
        fim = time.monotonic() + 3.0
        while time.monotonic() < fim:  # a tela do time fecha quando a troca começa
            n = olhos.tela()
            if menus.cursor_time(n) is None:
                return batalha.avancar()
            # a caixa da tela do time começa mais à esquerda e a 1ª letra sai "?" ("?revents")
            if re.search(r"revents switching|be switched|an.t escape", " ".join(texto.ler_caixa(n).split())):
                maos.apertar("B", "B")  # fecha a mensagem e a tela do time: volta ao menu da batalha
                time.sleep(0.8)
                return f"{combate.PRESO}: o inimigo impede a troca (ARENA TRAP, MEAN LOOK, WRAP...); lute com quem está em campo"
            time.sleep(0.2)
        maos.apertar("B")  # toque perdido: fecha o submenu e tenta de novo
        time.sleep(0.6)
    return "não consegui trocar"


CAIXA_TEXTO = (100, 160, 0, 240)
TIME_VELHO_S, BATALHAS_VELHO, MOCHILA_VELHA_S = 30 * 60, 12, 60 * 60  # depois disso o código relê sozinho
_ultima_mensagem = {"chave": None}


def _no_time(estado, quem, **campos):
    estado.atualizar(time=[dict(p, **campos) if p["especie"] == quem else p for p in estado.dados["time"]])


def _especie_do_texto(estado, nome):
    """Espécie do time pelo nome escrito ('MR. MIME' -> MR_MIME); apelido de troca não casa e fica None."""
    eid = conhecimento._especie_id(nome).removeprefix("SPECIES_")
    return next((p["especie"] for p in estado.dados["time"] if p["especie"] == eid), None)


def ler_mensagem(estado, n):
    """Memória pelo texto da tela, sem abrir menu: nível que subiu, golpe aprendido, evolução, desmaio; troca e
    presente marcam time/mochila para reler. batalha.avancar chama a cada texto parado; texto repetido não conta."""
    lido = texto.ler_caixa(n)
    if not lido or lido == _ultima_mensagem["chave"]:
        return
    _ultima_mensagem["chave"] = lido
    frase = " ".join(lido.split())  # as duas linhas da caixa numa frase só
    if re.match(r"Wild .+ appeared", frase):  # luta selvagem: a abertura de treinador anterior não vale mais
        combate.ultima_abertura["texto"] = ""
        return
    if m := re.search(r"(.+?) would like to battle!", frase):
        combate.ultima_abertura["texto"] = m[1]
        return
    if m := re.search(r"got \D?(\d+) for winning", frase):
        combate.ultima_abertura["texto"] = ""  # luta de treinador acabou
        if estado.dados.get("dinheiro") is not None:
            estado.atualizar(dinheiro=estado.dados["dinheiro"] + int(m[1]))
        return
    for padrao, status in STATUS_TEXTO:
        if (m := re.match(rf"(.+?) {padrao}", frase)) and not re.match(r"(Wild|Foe) ", frase):
            if esp := _especie_do_texto(estado, m[1]):
                _no_time(estado, esp, status=status)
            return
    if re.search(r"good care|traded", frase):
        estado.atualizar(time_lido_ts=0, evento=("leitura", f"troca na tela ({frase}): time marcado para reler"))
    elif re.search(r"received|obtained", frase, re.I):
        estado.atualizar(time_lido_ts=0, mochila_lido_ts=0)
    elif m := re.search(r"(.+?) grew to LV\. ?(\d+)", frase):
        if esp := _especie_do_texto(estado, m[1]):
            _no_time(estado, esp, nivel=int(m[2]))
            estado.evento("treino", f"{esp} subiu para o nv {m[2]}")
    elif m := re.search(r"(.+?) learned (.+?)!", frase):
        esp, novo = _especie_do_texto(estado, m[1]), m[2].strip()
        p = next((q for q in estado.dados["time"] if q["especie"] == esp), None)
        if (
            p
            and conhecimento.pp_de(novo)
            and len(p.get("golpes") or []) < 4
            and novo not in map(_sem_pp, p.get("golpes") or [])
        ):
            pp = conhecimento.pp_de(novo)
            _no_time(estado, esp, golpes=(p.get("golpes") or []) + [f"{novo} {pp}/{pp}"])
            estado.evento("treino", f"{esp} aprendeu {novo}")
    elif m := re.search(r"Your (.+?) evolved into (.+?)!", frase):
        antes, depois = _especie_do_texto(estado, m[1]), conhecimento._especie_id(m[2]).removeprefix("SPECIES_")
        if antes and depois in conhecimento.numero_nacional().values():
            _no_time(estado, antes, especie=depois)
            d = estado.dados
            estado.atualizar(
                pokedex_capturados=sorted(set(d["pokedex_capturados"]) | {depois}),
                pokedex_vistos=sorted(set(d["pokedex_vistos"]) | {depois}),
                evento=("evolucao", f"{antes} evoluiu para {depois}"),
            )
    elif (m := re.match(r"(.+?) fainted!", frase)) and not re.match(r"(Wild|Foe) ", frase):
        if esp := _especie_do_texto(estado, m[1]):
            _no_time(estado, esp, hp=0.0)


def gastar_pp(estado, especie, posicao):
    """Desconta 1 de PP do golpe (1-4) usado pelo Pokémon em campo."""
    p = next((q for q in estado.dados["time"] if q["especie"] == especie), None)
    golpes = list((p or {}).get("golpes") or [])
    if not p or not 1 <= posicao <= len(golpes):
        return
    m = re.search(r"(\d+)\s*/\s*(\d+)\s*$", golpes[posicao - 1])
    if m:
        golpes[posicao - 1] = f"{_sem_pp(golpes[posicao - 1])} {max(int(m[1]) - 1, 0)}/{m[2]}"
        _no_time(estado, especie, golpes=golpes)


def anotar_hp(estado, n):
    """HP do Pokémon em campo pela barra, no menu da batalha."""
    hp = olhos.hp_meu(n)
    esp, nota = olhos.identificar_meu(n, [p["especie"] for p in estado.dados["time"]])
    if hp is not None and nota >= olhos.IDENTIFICOU:
        _no_time(estado, esp, hp=round(hp, 2))


def manutencao(estado):
    """Relê o time (e a mochila) quando a memória envelheceu: 30 min, muitas batalhas ou mochila de 1 h. Só no mapa."""
    d, agora_ = estado.dados, time.time()
    velho = agora_ - d.get("time_lido_ts", 0) > TIME_VELHO_S or d.get("batalhas_desde_leitura", 0) >= BATALHAS_VELHO
    mochila_velha = agora_ - d.get("mochila_lido_ts", 0) > MOCHILA_VELHA_S
    if not (velho or mochila_velha) or olhos.classificar(olhos.tela()) != "outro":
        return None
    feito = []
    if velho and isinstance(sincronizar_time(estado), list):
        feito.append("time")
    if mochila_velha:
        _, imagem = menus.ver_mochila()
        itens = imagem is not None and menus.ler_bolsos([imagem[i : i + 160] for i in range(0, imagem.shape[0], 160)])
        if itens:
            estado.definir_mochila(itens, completa=True)
            feito.append("mochila")
    return feito


# texto da batalha -> status na memória (battle_message.c); "" limpa
STATUS_TEXTO = [
    (r"(?:was|is badly) poisoned", "envenenado"),
    (r"was burned", "queimado"),
    (r"is paralyzed", "paralisado"),
    (r"(?:fell asleep|is fast asleep)", "dormindo"),
    (r"(?:was frozen|is frozen)", "congelado"),
    (r"(?:woke up|was thawed|thawed out)", ""),
    (r"(?:was cured|is cured)", ""),
]


def _sem_pp(golpe):
    return re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", golpe).strip()


def _quem_aprende(estado, novo):
    """Do time, quem tem 4 golpes e aprende 'novo' por nível perto do nível da memória (que atrasa até a próxima leitura)."""
    gid = conhecimento._id_golpe(novo)
    candidatos = []
    for p in estado.dados["time"]:
        e = conhecimento.especies().get(conhecimento._especie_id(p["especie"]), {})
        niveis = [n for n, g in e.get("golpes", []) if f"MOVE_{g}" == gid]
        if len(p.get("golpes") or []) >= 4 and niveis:
            candidatos.append((min(abs(n - (p.get("nivel") or 0) - 1) for n in niveis), p))
    return min(candidatos, key=lambda c: c[0])[1] if candidatos else None


def golpe_novo(estado, especie=None):
    """Na pergunta "Delete a move to make room for X?": decide pela nota (decidir_golpe_novo) e executa sozinho.

    Lê o golpe novo na caixa de texto; acha quem aprende pelo time da memória (ou 'especie'). Devolve o relato."""
    n = olhos.tela()
    novo = texto.ler_mais_longo(n, conhecimento.nomes_golpes(), CAIXA_TEXTO)
    if not novo:
        return "não li o golpe novo na caixa de texto"
    p = next((q for q in estado.dados["time"] if q["especie"] == (especie or "").upper()), None) or _quem_aprende(
        estado, novo
    )
    if not p:
        return f"não sei quem está aprendendo {novo}"
    aprender, sai, motivo = conhecimento.escolher_golpe_novo(
        p["especie"], p["nivel"], p["golpes"], novo, estado.dados["insignias"]
    )
    if not aprender:
        batalha.responder(False)  # "Stop learning X?" vem em seguida: YES desiste
        if olhos.classificar(olhos.tela()) == "sim_nao" or batalha.avancar(prazo=6) == "sim_nao":
            batalha.responder(True)
        estado.evento("treino", f"{p['especie']} não aprendeu {novo}: {motivo}")
        return f"{p['especie']} recusou {novo}: {motivo}"
    batalha.responder(True)  # abre a lista dos golpes (os 4 atuais e o novo embaixo) para escolher quem sai
    tela = olhos.assentar(1.0, prazo=4.0)
    nome_sai = next(g for g in p["golpes"] if conhecimento._id_golpe(g) == sai)
    # a ordem na tela pode ter mudado desde a última leitura: acha a linha de cada golpe pelo nome escrito
    achados = [(texto.achar(tela, _sem_pp(g), (0, 160, 100, 240)), g) for g in p["golpes"]]
    ordem = [g for (nota, _, y), g in sorted(achados, key=lambda a: a[0][2] or 0) if nota >= texto.ACHOU]
    if nome_sai not in ordem or len(ordem) < len(p["golpes"]):
        maos.apertar("B")
        return f"não achei os golpes de {p['especie']} na tela para esquecer {nome_sai}: decida com apertar"
    linha = ordem.index(nome_sai)
    if linha:
        maos.apertar(*["BAIXO"] * linha)
        time.sleep(0.3)
    maos.apertar("A")
    r = batalha.avancar(prazo=15)
    if r == "sim_nao":  # confirmação, em telas que pedem
        batalha.responder(True)
    pp = conhecimento.pp_de(novo)
    golpes = [f"{novo} {pp}/{pp}" if g == nome_sai else g for g in p["golpes"]]
    estado.atualizar(
        time=[dict(q, golpes=golpes) if q is p else q for q in estado.dados["time"]],
        evento=("treino", f"{p['especie']} aprendeu {novo} no lugar de {nome_sai}: {motivo}"),
    )
    return f"{p['especie']} aprendeu {novo} esquecendo {nome_sai}"


def _lutar_ate_o_fim(estado, meu, esp, nivel, relato):
    """Golpe mais forte até a batalha acabar; foge com HP baixo e manda a escolta se o nosso desmaiar."""
    recusados = set()  # golpes que o jogo recusou nesta luta (Disable, sem PP)
    for _ in range(12):
        hp = olhos.hp_meu(olhos.tela())
        if hp is not None and hp < 0.3:
            relato.append(f"HP do {meu['especie']} em {hp:.0%}: fugindo")
            return batalha.fugir()
        i = _melhor_golpe(meu, esp, nivel, recusados)
        r = _lutar(estado, meu, i)
        if isinstance(r, str) and "indisponível" in r:
            recusados.add(i)
            relato.append(r)
            continue
        if r == "golpes":  # o jogo voltou à lista: golpe sem PP (a memória do PP atrasou) ou bloqueado
            recusados.add(i)
            relato.append(f"golpe {i} recusado pelo jogo")
            maos.apertar("B")
            time.sleep(0.6)
            continue
        if r == "sim_nao" and not texto.tem(olhos.tela(), "next", (112, 160, 0, 240)):
            relato.append(golpe_novo(estado))  # "Delete a move to make room for X?"
            r = batalha.avancar()
        if r == "sim_nao":
            batalha.responder(True)  # "Use next POKéMON?": o nosso desmaiou
            escolta = _escolta(estado)
            if not escolta:
                return "desmaiou e não há escolta"
            relato.append(f"{meu['especie']} desmaiou: entra {escolta['especie']}")
            r, meu = trocar(escolta["especie"]), escolta
        if r != "batalha_menu":
            return r
    return "batalha longa demais"


def _escolta(estado):
    nome = (estado.dados.get("treino") or {}).get("escolta")
    return next((p for p in estado.dados["time"] if p["especie"] == nome and p.get("golpes")), None)


def treinar_na_batalha(estado, meu, esp, faixa, relato):
    """Treino: o alvo luta sozinho se os selvagens daqui não passam do nível dele +1; senão troca para a escolta no 1º
    turno e os dois dividem a experiência (Gen 3: metade para cada participante)."""
    alvos = (estado.dados.get("treino") or {}).get("alvos", {})
    escolta = _escolta(estado)
    nivel = faixa[1] if faixa else meu["nivel"]
    sem_dano = not any(
        (d := conhecimento.dano(g, meu["especie"], meu["nivel"], esp, nivel)) and d[1] > 0 for g in meu["golpes"]
    )
    if meu["especie"] in alvos and escolta and escolta is not meu and (nivel > meu["nivel"] + 1 or sem_dano):
        r = trocar(escolta["especie"])
        relato.append(f"{meu['especie']} começou e saiu para {escolta['especie']} (experiência dividida): {r}")
        if r == "batalha_menu":
            meu = escolta
        elif not r.startswith(combate.PRESO):  # preso (ARENA TRAP do Diglett): o treinado luta sozinho
            return r
    return _lutar_ate_o_fim(estado, meu, esp, nivel, relato)


def resolver_selvagem(estado, mapa_atual):
    """Resolve uma batalha selvagem que acabou de começar. Devolve (resolvida: bool, relato)."""
    combate.ultima_abertura["texto"] = ""
    e = batalha.avancar()
    if e == "batalha_menu" and combate.ultima_abertura["texto"]:  # "X would like to battle!": é treinador
        ok, relato = combate.lutar_treinador(estado, mapa_atual, lambda p, i: _lutar(estado, p, i), trocar)
        if ok:
            estado.contar("batalhas_terminadas")
            estado.contar("vitorias")
            estado.evento("batalha", relato)
        return ok, relato
    if e != "batalha_menu":
        return False, f"batalha parou em {e}"
    n = olhos.tela()
    selvagens = mapa.selvagens().get(mapa_atual, {})
    candidatas = sorted({esp for d in selvagens.values() for esp in d})
    esp, nota = olhos.identificar_inimigo(n, candidatas) if candidatas else (None, 0)
    if nota < olhos.IDENTIFICOU:
        esp, nota = olhos.identificar_inimigo(n, [conhecimento.numero_nacional()[i] for i in range(1, 152)])
    if nota < olhos.IDENTIFICOU:
        return False, "não reconheci o inimigo pela sprite"
    faixa = next((d[esp][:2] for d in selvagens.values() if esp in d), None)
    nivel = faixa[0] if faixa else 5  # o nível mais baixo da faixa é o caso de risco de derrubar sem querer
    meu = _meu(estado, n)
    relato = [f"selvagem {esp}" + (f" nv {faixa[0]}-{faixa[1]}" if faixa else "")]
    if esp not in estado.dados["pokedex_capturados"] and _bolas(estado) > 0 and meu and meu.get("golpes"):
        forte = max(
            (p for p in estado.dados["time"] if p.get("golpes") and (p.get("hp") is None or p["hp"] > 0.3)),
            key=lambda p: p.get("nivel") or 0,
            default=None,
        )
        if forte and forte is not meu and meu["nivel"] + 3 < (faixa[1] if faixa else nivel):
            r = trocar(forte["especie"])
            relato.append(f"{meu['especie']} fraco para enfraquecer: entra {forte['especie']} ({r})")
            if r == "batalha_menu":
                meu = forte
        relato.append("falta na Pokédex: " + enfraquecer_e_capturar(estado, esp, nivel, meu))
    elif estado.dados.get("modo_selvagens") == "treinar" and meu and meu.get("golpes"):
        relato.append(f"treino: {treinar_na_batalha(estado, meu, esp, faixa, relato)}")
        estado.contar("batalhas_treino")
    else:
        for _ in range(3):
            r = batalha.fugir()
            if r != "batalha_menu":
                break
            r = _lutar(estado, meu, _melhor_golpe(meu, esp, nivel)) if meu and meu.get("golpes") else r
            if r != "batalha_menu":
                break
        relato.append(f"já tem: fugiu/derrubou -> {r}")
    estado.atualizar(batalhas_desde_leitura=estado.dados.get("batalhas_desde_leitura", 0) + 1)
    n = olhos.assentar(0.5, prazo=3.0)
    final = olhos.classificar(n)
    # "outro" também é tela do time e resumo: só está resolvida com o mapa de volta na tela
    no_mapa = final == "outro" and batalha.LOC.localizar(n, global_=False) is not None
    return no_mapa, "; ".join(relato) + f" | tela final: {'mapa' if no_mapa else final}"


def sincronizar_time(estado):
    """Lê o time na tela e grava na memória. Devolve a lista lida ou o texto do erro."""
    lidos, _ = menus.ver_time()
    if isinstance(lidos, str):
        return lidos
    if not all(p["especie"] and p.get("nivel") for p in lidos):  # nível None derruba a simulação de batalha
        return "não consegui ler todo o time"
    antes = {p["especie"]: p.get("nivel") for p in estado.dados["time"]}
    subiu = [
        f"{p['especie']} {antes[p['especie']]}->{p['nivel']}"
        for p in lidos
        if antes.get(p["especie"]) and p["nivel"] and p["nivel"] > antes[p["especie"]]
    ]
    estado.atualizar(
        time=lidos,
        time_lido_ts=time.time(),
        batalhas_desde_leitura=0,
        evento=(
            "leitura",
            "time: "
            + "; ".join(f"{p['especie']} nv{p['nivel']}" for p in lidos)
            + (f" | subiu: {', '.join(subiu)}" if subiu else ""),
        ),
    )
    return lidos


def _um_passo(mundo, m, a, b):
    """Dá para ir de a até b com um passo comum (sem borda de pulo, elevação ou bloqueio de direção no meio)."""
    _, elev, _ = mapa.grade(m)
    z = int(elev[a[1], a[0]])
    return any(
        acao[0] == "passo" and novo[:3] == (m, *b) for _, novo, acao in mundo.vizinhos((m, *a, 0 if z == 15 else z))
    )


def _par_de_encontro(mundo, m, perto, evitar=()):
    """Dois tiles vizinhos onde aparecem selvagens a pé (grama alta; em caverna, qualquer chão), o mais perto,
    com passagem nos dois sentidos e fora de 'evitar' (tiles ocupados)."""
    col, _, comp = mapa.grade(m)
    if "grama/caverna" not in mapa.selvagens().get(m, {}):
        return None
    pode = (col == 0) & (comp == mapa.comportamentos()["MB_TALL_GRASS"])
    if not pode.any():
        pode = col == 0  # caverna: o chão todo tem encontro
    candidatos = []
    for y, x in zip(*np.nonzero(pode), strict=True):
        for vx, vy in ((1, 0), (0, 1)):
            if y + vy < pode.shape[0] and x + vx < pode.shape[1] and pode[y + vy, x + vx]:
                candidatos.append((abs(x - perto.x) + abs(y - perto.y), (int(x), int(y)), (int(x + vx), int(y + vy))))
    return next(
        (
            (a, b)
            for _, a, b in sorted(candidatos)
            if a not in evitar and b not in evitar and _um_passo(mundo, m, a, b) and _um_passo(mundo, m, b, a)
        ),
        None,
    )


def _alvos_atualizados(estado):
    """Tira dos alvos de treino quem chegou ao nível; troca o nome de quem evoluiu."""
    treino = dict(estado.dados.get("treino") or {})
    alvos, no_time = dict(treino.get("alvos", {})), {p["especie"]: p for p in estado.dados["time"]}
    for esp, alvo in list(alvos.items()):
        if esp not in no_time:
            evoluiu = next(
                (
                    p
                    for p in estado.dados["time"]
                    if any(
                        a == p["especie"]
                        for _, _, a in conhecimento.especies().get(f"SPECIES_{esp}", {}).get("evolucoes", [])
                    )
                ),
                None,
            )
            alvos.pop(esp)
            if evoluiu:
                alvos[evoluiu["especie"]] = alvo
                if treino.get("escolta") == esp:
                    treino["escolta"] = evoluiu["especie"]
        elif (no_time[esp].get("nivel") or 0) >= alvo:
            alvos.pop(esp)
    treino["alvos"] = alvos
    estado.atualizar(treino=treino)
    return alvos


def _por_alvo_na_frente(estado, alvos):
    """O primeiro alvo de treino vai para a posição 0 (quem começa a batalha ganha experiência)."""
    time_ = estado.dados["time"]
    if not alvos or not time_ or time_[0]["especie"] in alvos:
        return None
    i = next(i for i, p in enumerate(time_) if p["especie"] in alvos)
    r = menus.trocar_ordem(i, 0, time_[i].get("golpes") or [])
    sincronizar_time(estado)
    return r


def treinar(nav, estado, minutos=15, curar_abaixo=0.35, reler_a_cada=5):
    """Anda na grama do mapa atual e resolve cada selvagem com o piloto no modo treino (alvo começa, escolta entra se
    o selvagem for forte). Cura no Centro quando o HP cai e volta. Para no tempo, quando todos os alvos chegam ao
    nível, ou em algo que não é selvagem (treinador, golpe novo, tela estranha)."""
    m = nav.loc.ultima and nav.loc.ultima.mapa
    par = m and _par_de_encontro(nav.mundo, m, nav.loc.ultima)
    if not par:
        return f"{m} não tem selvagens a pé para treinar"
    sincronizar_time(estado)
    alvos = _alvos_atualizados(estado)
    if not alvos:
        return "nenhum alvo de treino abaixo do nível pedido (use definir_treino)"
    _por_alvo_na_frente(estado, alvos)
    modo_antes = estado.dados.get("modo_selvagens")
    estado.atualizar(modo_selvagens="treinar")
    fim, batalhas, relato, i = time.monotonic() + minutos * 60, 0, [], 0
    ocupados = set()  # tiles de grama onde um NPC parou: o par muda em vez de desistir
    try:
        while time.monotonic() < fim:
            r = nav.ir(("tile", m, *par[i % 2]), max_passos=40, piloto=False)  # aqui a batalha é o treino
            i += 1
            if r.startswith("chegou"):
                continue
            if not r.startswith("interrompido"):
                ocupados.add(par[(i - 1) % 2])  # o tile que não deu para alcançar
                novo = (
                    len(ocupados) <= 4 and nav.loc.ultima and _par_de_encontro(nav.mundo, m, nav.loc.ultima, ocupados)
                )
                if not novo:
                    return "; ".join(relato + [f"parei andando na grama: {r}"])
                par = novo
                continue
            n = olhos.tela()
            tela = olhos.classificar(n)
            # "Wild X appeared!" às vezes é lido como diálogo; treinador começa com diálogo sem "Wild"
            if not (tela.startswith("batalha") or tela == "preto" or texto.tem(n, "Wild", CAIXA_TEXTO)):
                return "; ".join(relato + [f"parei: {r} (treinador ou conversa: resolva e chame treinar de novo)"])
            ok, rel = resolver_selvagem(estado, m)
            batalhas += 1
            relato.append(rel)
            if not ok:
                return "; ".join(relato + ["parei: a batalha precisa de decisão"])
            if batalhas % reler_a_cada:
                continue
            sincronizar_time(estado)
            alvos = _alvos_atualizados(estado)
            if not alvos:
                return "; ".join(relato + ["todos os alvos chegaram ao nível"])
            fracos = [
                p
                for p in estado.dados["time"]
                if p["especie"] in alvos or p["especie"] == estado.dados["treino"].get("escolta")
            ]
            if any((p.get("hp") or 0) < curar_abaixo for p in fracos):
                relato.append(menus.curar(nav))
                volta = nav.ir(("tile", m, *par[0]))
                if not volta.startswith("chegou"):
                    return "; ".join(relato + [f"não voltei ao ponto de treino: {volta}"])
            _por_alvo_na_frente(estado, alvos)
        sincronizar_time(estado)
        return "; ".join(
            relato
            + [
                f"tempo de treino esgotado ({batalhas} batalhas); time: "
                + ", ".join(f"{p['especie']} nv{p['nivel']}" for p in estado.dados["time"])
            ]
        )
    finally:
        estado.atualizar(modo_selvagens=modo_antes)
        estado.evento("treino", f"{batalhas} batalhas de treino em {m}")
