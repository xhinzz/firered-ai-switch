"""Batalha contra treinador sem o modelo: identifica o treinador pelo texto de abertura, simula a luta com as fórmulas
do jogo e decide cada turno — o golpe que derruba mais rápido, a troca quando o confronto vira contra, a Potion quando
salva. Líder, rival, Elite dos 4, chefe, luta dupla, simulação que não dá vitória folgada e tela estranha ficam com o
modelo.
"""

import functools
import math
import re

from fireredia.controle import maos
from fireredia.habilidades import batalha, menus
from fireredia.mundo import conhecimento
from fireredia.percepcao import olhos

IMPORTANTES = ("TRAINER_LEADER_", "TRAINER_RIVAL_", "TRAINER_ELITE_FOUR", "TRAINER_CHAMPION", "TRAINER_BOSS_")
FOLGA_SIMULACAO = 0.25  # a simulação da luta inteira precisa deixar pelo menos isso de HP para o piloto aceitar
FOLGA_LUTAR = 0.2  # em campo, vencendo o duelo com essa sobra, segue lutando sem trocar
GANHO_TROCA = 0.25  # a troca precisa deixar tanto a mais de HP sobrando (ela custa um golpe de graça do inimigo)
POCAO_ABAIXO = 0.35
CURA = {"POTION": 20, "SUPER POTION": 50, "HYPER POTION": 200}
SEM_AGIR = ("dormindo", "congelado")
MAX_TURNOS = 40
PRESO = "troca bloqueada"  # começo do retorno de piloto.trocar quando o inimigo impede a troca
ultima_abertura = {"texto": ""}  # "BUG CATCHER SAMMY", gravado por piloto.ler_mensagem


# ---------------- decisão (sem tela: dá para testar) ----------------


def _maximo(p):
    return conhecimento._hp_max(p["especie"], p["nivel"])


def _vivo(p):
    return p.get("hp") is None or p["hp"] > 0


def _golpes(p):
    return p.get("golpes") or conhecimento.golpes_padrao(p["especie"], p["nivel"])


def golpe_do_turno(p, inimigo, nivel, hp_dele, evitar=()):
    """(posição 1-4, nome, turnos para derrubar) do golpe que derruba em menos turnos; empate: o mais preciso e, depois,
    o mais fraco (guarda o PP do golpe forte)."""
    opcoes = []
    for i, g in enumerate(_golpes(p)[:4], 1):
        pp = re.search(r"(\d+)\s*/\s*\d+\s*$", g)
        if (pp and pp[1] == "0") or i in evitar:  # sem PP ou recusado nesta batalha (Disable)
            continue
        nome = re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", g).strip()
        d = conhecimento.dano(nome, p["especie"], p["nivel"], inimigo, nivel)
        info = conhecimento.golpes().get(conhecimento._golpe_por_nome().get(conhecimento._chave(nome), ""))
        if not d or not info or d[1] <= 0:
            continue
        precisao = (info["precisao"] or 100) / 100
        media = (d[0] + d[1]) / 2 * precisao
        opcoes.append((math.ceil(hp_dele / media), -precisao, info["poder"], i, nome))
    if not opcoes:
        return None
    turnos, _, _, i, nome = min(opcoes)
    return i, nome, turnos


def escolher(time_, ativo, inimigo, nivel, hp_inimigo, golpes_inimigo, mochila, evitar=()):
    """Ação do turno: ("golpe", posição, motivo) | ("trocar", espécie, motivo) | ("item", item, motivo) |
    ("devolver", motivo). time_ = [{especie, nivel, hp (fração), golpes, status}]; hp_inimigo = fração da barra."""
    dele = (inimigo, nivel, golpes_inimigo or conhecimento.golpes_padrao(inimigo, nivel))
    hp_dele = max(hp_inimigo, 0.01) * conhecimento._hp_max(inimigo, nivel)
    eu = next((p for p in time_ if p["especie"] == ativo), None)
    if not eu:
        return ("devolver", f"não sei quem está em campo ({ativo})")
    hp_eu = (eu.get("hp") if eu.get("hp") is not None else 1.0) * _maximo(eu)
    venci, sobra, _, _ = conhecimento._duelo((eu["especie"], eu["nivel"], _golpes(eu)), hp_eu, dele, hp_dele)
    sobra_eu = sobra / _maximo(eu) if venci else -1.0
    parado = eu.get("status") in SEM_AGIR

    alternativas = []
    for p in time_:
        if p is eu or not _vivo(p) or p.get("status") in SEM_AGIR:
            continue
        custo = conhecimento._dano_esperado(dele[2], inimigo, nivel, p["especie"], p["nivel"])[0]
        hp_p = (p.get("hp") if p.get("hp") is not None else 1.0) * _maximo(p) - custo
        if hp_p <= 0:
            continue  # cairia só de entrar
        v, s, _, _ = conhecimento._duelo((p["especie"], p["nivel"], _golpes(p)), hp_p, dele, hp_dele)
        if v:
            alternativas.append((s / _maximo(p), p))
    troca = max(alternativas, key=lambda a: a[0], default=None)

    if venci and sobra_eu >= FOLGA_LUTAR and not parado:
        g = golpe_do_turno(eu, inimigo, nivel, hp_dele, evitar)
        if g:
            return ("golpe", g[0], f"{g[1]} derruba {inimigo} em {g[2]} turno(s); sobra {sobra_eu:.0%} de HP")
    if troca and (not venci or parado or troca[0] >= sobra_eu + GANHO_TROCA):
        p = troca[1]
        return (
            "trocar",
            p["especie"],
            f"{p['especie']} vence {inimigo} com {troca[0]:.0%} de HP sobrando"
            + (f" ({eu['especie']} {eu['status']})" if parado else ""),
        )
    if not venci and eu.get("hp") is not None and eu["hp"] < POCAO_ABAIXO:
        golpe_dele = conhecimento._dano_esperado(dele[2], inimigo, nivel, eu["especie"], eu["nivel"])[0]
        for item, cura in sorted(CURA.items(), key=lambda kv: kv[1]):
            if mochila.get(item, 0) <= 0:
                continue
            curado = min(hp_eu + cura, _maximo(eu)) - golpe_dele  # o turno da poção leva um golpe de graça
            if curado <= 0:
                continue
            v, s, _, _ = conhecimento._duelo((eu["especie"], eu["nivel"], _golpes(eu)), curado, dele, hp_dele)
            if v:
                return ("item", item, f"{item} no {eu['especie']} vira o duelo contra {inimigo}")
    if venci and not parado:
        g = golpe_do_turno(eu, inimigo, nivel, hp_dele, evitar)
        if g:
            return ("golpe", g[0], f"{g[1]} em {inimigo}: vitória apertada ({sobra_eu:.0%} de HP sobrando)")
    return ("devolver", f"ninguém do time vence {inimigo} nv {nivel} com segurança: decida (item, troca, golpe)")


def escolher_quem_entra(time_, inimigo, nivel, golpes_inimigo, hp_inimigo=1.0):
    """Depois de um desmaio: quem do time vence o inimigo em campo com mais HP sobrando (ou o que mais aguenta)."""
    dele = (inimigo, nivel, golpes_inimigo or conhecimento.golpes_padrao(inimigo, nivel))
    hp_dele = max(hp_inimigo, 0.01) * conhecimento._hp_max(inimigo, nivel)
    melhor = None
    for p in time_:
        if not _vivo(p):
            continue
        hp_p = (p.get("hp") if p.get("hp") is not None else 1.0) * _maximo(p)
        v, s, resto, _ = conhecimento._duelo((p["especie"], p["nivel"], _golpes(p)), hp_p, dele, hp_dele)
        chave = (v, s / _maximo(p) if v else -resto)
        if melhor is None or chave > melhor[0]:
            melhor = (chave, p["especie"])
    return melhor and melhor[1]


# ---------------- identificação do treinador ----------------


@functools.lru_cache
def _scripts_globais():
    """rótulo -> corpo dos scripts de treinador compartilhados (data/scripts/trainers.inc)."""
    txt = conhecimento._ler("data/scripts/trainers.inc")
    return dict(re.findall(r"^(\w+)::\s*\n(.*?)(?=^\w+::|\Z)", txt, re.S | re.M))


@functools.lru_cache(maxsize=256)
def treinadores_do_mapa(mapa_id):
    """({TRAINER_ do mapa}, {os de luta dupla}): pelos scripts do mapa e pelos rótulos dos NPCs no arquivo global."""
    if mapa_id not in conhecimento.mapa.mapas():
        return set(), set()
    corpos = conhecimento._scripts(mapa_id)[0]
    rotulos = {o.get("script") for o in conhecimento.mapa.mapas()[mapa_id].get("object_events") or []}
    juntos = "\n".join(list(corpos.values()) + [c for r, c in _scripts_globais().items() if r in rotulos])
    return set(re.findall(r"trainerbattle\w* (TRAINER_\w+)", juntos)), set(
        re.findall(r"trainerbattle_double (TRAINER_\w+)", juntos)
    )


def identificar(abertura, mapa_id):
    """TRAINER_ pelo texto de abertura ("BUG CATCHER SAMMY"), preferindo quem tem batalha nos scripts do mapa."""
    alvo = " ".join(abertura.upper().replace("’", "'").split())
    do_mapa, _ = treinadores_do_mapa(mapa_id)
    nomes = [(tid, t) for tid, t in conhecimento.treinadores().items() if t["nome"] and t["nome"].upper() in alvo]
    completos = [tid for tid, t in nomes if t["classe"].replace("_", " ") in alvo]
    for grupo in (completos, [tid for tid, _ in nomes]):
        no_mapa = [tid for tid in grupo if tid in do_mapa]
        if no_mapa:
            return no_mapa[0]
    return completos[0] if completos else None


# ---------------- execução na tela ----------------


def _pocao(estado, item, especie):
    """BAG > item > USE > Pokémon na batalha. Devolve o estado da tela depois."""
    if batalha.abrir("BAG") != "aberto":
        return "não abriu a BAG"
    olhos.assentar(0.8, prazo=3)
    if not menus._apontar_item(item, menus.BOLSOS["ITEMS"]):
        maos.apertar("B", "B")
        return f"{item} não está na mochila"
    olhos.assentar(0.5, prazo=2)
    maos.apertar("A")  # USE
    n = olhos.assentar(0.8, prazo=3)
    pos = menus.posicao_na_tela(n, especie)
    if pos is None or not menus.escolher_no_time(pos):
        maos.apertar("B", "B", "B")
        return "não achei o Pokémon para a poção"
    estado.ajustar_item(item, -1, f"usada no {especie} na batalha")
    return batalha.avancar()


def _hp_da_tela(estado, n):
    """Na tela do time, a barra de cada um corrige a memória: desmaio que o texto da batalha não pegou."""
    novo = []
    for p in estado.dados["time"]:
        i = menus.posicao_na_tela(n, p["especie"])  # apelido não casa com a espécie: fica a memória
        hp = menus._hp_time(n, i) if i is not None else None
        novo.append(dict(p, hp=round(hp, 2)) if hp is not None else p)
    estado.atualizar(time=novo)


def lutar_treinador(estado, mapa_id, golpear, trocar, abertura=None):
    """Luta contra treinador comum até o fim. golpear(p, i) e trocar(espécie) são as rotinas do piloto (memória de PP e
    HP em dia). Devolve (resolvida, relato): resolvida=False devolve a vez ao modelo com o motivo."""
    e = batalha.avancar()  # luta pega no começo: o "X would like to battle!" ainda na tela só é lido ao passar o texto
    if e in ("mapa", "outro") and batalha._espera(
        lambda n: olhos.classificar(n) in ("batalha_texto", "batalha_menu"), 5.0
    ):
        e = batalha.avancar()  # chamado no diálogo de antes da luta: a transição mostra o mapa por um instante
    if e != "batalha_menu" and not (e == "outro" and menus.cursor_time(olhos.tela()) is not None):
        return False, f"nenhuma luta de treinador na tela ({e})"
    abertura = abertura or ultima_abertura["texto"]
    tid = identificar(abertura, mapa_id) if abertura else None
    _, duplas = treinadores_do_mapa(mapa_id)
    if tid and (tid.startswith(IMPORTANTES) or tid in duplas):
        return False, f"luta importante ou dupla ({tid}): decida você (rode preparar_batalha)"
    adversario = list(conhecimento.treinadores()[tid]["time"]) if tid else None
    nome = (
        f"{conhecimento.treinadores()[tid]['classe']} {conhecimento.treinadores()[tid]['nome']}"
        if tid
        else (abertura or "treinador")
    )
    if adversario:
        venceu, folga, _ = conhecimento.simular_batalha(estado.dados["time"], adversario)
        if not venceu or folga < FOLGA_SIMULACAO:
            return False, (
                f"{nome}: a simulação não dá vitória folgada "
                f"({'vence no limite' if venceu else 'perde'}); decida você (preparar_batalha)"
            )
    relato, turnos = [f"luta com {nome}" + (f" ({tid})" if tid else " (time desconhecido)")], 0
    recusados = {}  # espécie -> posições de golpe que o jogo recusou nesta luta (Disable, sem PP)
    preso = False  # ARENA TRAP, MEAN LOOK: só a troca forçada (desmaio) funciona
    nao_entram = set()  # o jogo recusou na escolha depois do desmaio: desmaiados que a memória não sabia
    ultimo_inimigo = (adversario[0][0], adversario[0][1], adversario[0][2], 1.0) if adversario else None
    candidatas = (
        sorted({e for e, _, _ in adversario})
        if adversario
        else [conhecimento.numero_nacional()[i] for i in range(1, 152)]
    )
    while turnos < MAX_TURNOS:
        e = batalha.avancar()
        n = olhos.tela()
        if e == "mapa":
            ultima_abertura["texto"] = ""
            return True, "; ".join(relato + ["venceu"])
        if e == "outro" and menus.cursor_time(n) is not None:  # nosso caiu: tela do time para escolher quem entra
            turnos += 1  # conta no limite: escolha recusada em laço já prendeu a IA 40 min
            _hp_da_tela(estado, n)
            vivos = [p for p in estado.dados["time"] if p["especie"] not in nao_entram]
            # o inimigo não aparece na tela do time: vale o último visto na batalha
            quem = (
                escolher_quem_entra(vivos, *ultimo_inimigo)
                if ultimo_inimigo
                else max((p for p in vivos if _vivo(p)), key=lambda p: p["nivel"], default={}).get("especie")
            )
            if not quem:
                return False, "; ".join(relato + ["não sobrou ninguém para entrar"])
            relato.append(f"entra {quem}")
            r = trocar(quem)
            if " " in r:  # mensagem de recusa (os estados da tela são uma palavra só)
                nao_entram.add(quem)
                estado.atualizar(time=[dict(p, hp=0.0) if p["especie"] == quem else p for p in estado.dados["time"]])
                relato.append(f"{quem} recusado ({r})")
            continue
        if e != "batalha_menu":
            return False, "; ".join(relato + [f"parou em '{e}': decida você"])
        esp_inimigo, nota = olhos.identificar_inimigo(n, candidatas)
        if nota < olhos.IDENTIFICOU:
            return False, "; ".join(relato + ["não reconheci o Pokémon do treinador"])
        ent = adversario and next(((e_, n_, g) for e_, n_, g in adversario if e_ == esp_inimigo), None)
        nivel = ent[1] if ent else max((p.get("nivel") or 5) for p in estado.dados["time"])
        golpes_inimigo = (ent[2] if ent else []) or conhecimento.golpes_padrao(esp_inimigo, nivel)
        ultimo_inimigo = (esp_inimigo, nivel, golpes_inimigo, olhos.hp_inimigo(n) or 1.0)
        meu_esp, nota_meu = olhos.identificar_meu(n, [p["especie"] for p in estado.dados["time"]])
        if nota_meu < olhos.IDENTIFICOU:
            return False, "; ".join(relato + ["não reconheci o nosso Pokémon em campo"])
        hp = olhos.hp_meu(n)
        if hp is not None:
            estado.atualizar(
                time=[dict(p, hp=round(hp, 2)) if p["especie"] == meu_esp else p for p in estado.dados["time"]]
            )
        disponiveis = [p for p in estado.dados["time"] if not preso or p["especie"] == meu_esp]
        acao = escolher(
            disponiveis,
            meu_esp,
            esp_inimigo,
            nivel,
            olhos.hp_inimigo(n) or 1.0,
            golpes_inimigo,
            estado.dados["mochila"],
            recusados.get(meu_esp, set()),
        )
        turnos += 1
        if acao[0] == "devolver":
            return False, "; ".join(relato + [acao[1]])
        relato.append(acao[2])
        if acao[0] == "golpe":
            r = golpear(next(p for p in estado.dados["time"] if p["especie"] == meu_esp), acao[1])
            if isinstance(r, str) and "indisponível" in r:
                recusados.setdefault(meu_esp, set()).add(acao[1])
                relato.append(r)
        elif acao[0] == "trocar":
            r = trocar(acao[1])
            if isinstance(r, str) and r.startswith(PRESO):
                preso = True
                relato.append(r)
        else:
            _pocao(estado, acao[1], meu_esp)
    return False, "; ".join(relato + [f"luta passou de {MAX_TURNOS} turnos: decida você"])


if __name__ == "__main__":  # cenários de decisão com o motor de dano do jogo (sem tela)
    char = {
        "especie": "CHARMELEON",
        "nivel": 29,
        "hp": 1.0,
        "golpes": ["SCRATCH 35/35", "DIG 10/10", "EMBER 25/25", "METAL CLAW 35/35"],
    }
    pika = {
        "especie": "PIKACHU",
        "nivel": 22,
        "hp": 1.0,
        "golpes": ["THUNDERSHOCK 30/30", "QUICK ATTACK 30/30", "THUNDER WAVE 20/20", "DOUBLE TEAM 15/15"],
    }
    gloom = {
        "especie": "GLOOM",
        "nivel": 22,
        "hp": 1.0,
        "golpes": ["ABSORB 20/20", "ACID 30/30", "STUN SPORE 30/30", "SLEEP POWDER 15/15"],
    }
    time_ = [char, pika, gloom]
    a = escolher(time_, "CHARMELEON", "CATERPIE", 10, 1.0, [], {})
    assert a[0] == "golpe" and "1 turno" in a[2], a  # derruba num turno (empate: o golpe que poupa PP do mais forte)
    a = escolher(time_, "CHARMELEON", "CATERPIE", 10, 1.0, [], {}, {1})
    assert a[0] == "golpe" and a[1] != 1, a  # golpe recusado (Disable) não volta a ser escolhido
    fraco_fogo = dict(
        char, nivel=18, hp=0.6, golpes=["SCRATCH 35/35", "EMBER 25/25", "METAL CLAW 35/35", "GROWL 40/40"]
    )
    a = escolher([fraco_fogo, pika, gloom], "CHARMELEON", "PSYDUCK", 20, 1.0, [], {})
    assert a[:2] == ("trocar", "PIKACHU"), a  # água contra fogo: entra o elétrico
    a = escolher([fraco_fogo, pika, gloom], "CHARMELEON", "POLIWAG", 18, 1.0, [], {})
    assert a[:2] == ("trocar", "GLOOM"), a
    a = escolher(time_, "CHARMELEON", "STARMIE", 21, 1.0, ["SWIFT", "RECOVER", "RAPID_SPIN", "WATER_PULSE"], {})
    assert a[0] == "devolver", a  # Starmie da Misty: ninguém vence com folga, o modelo decide
    a = escolher(time_, "CHARMELEON", "GEODUDE", 20, 1.0, [], {})
    assert a[0] == "golpe" and a[1] in (2, 4), a  # pedra resiste a fogo: DIG ou METAL CLAW
    fraco = dict(char, hp=0.15)
    a = escolher([fraco], "CHARMELEON", "PIDGEOTTO", 22, 1.0, [], {"POTION": 2, "SUPER POTION": 1})
    assert a[0] == "item", a  # poção só quando vira o duelo (já contando o golpe de graça do turno)
    a = escolher([fraco], "CHARMELEON", "RATICATE", 24, 1.0, [], {"SUPER POTION": 1})
    assert a[0] == "devolver", a  # Raticate 24 é mais rápido e vence até com a poção: o modelo decide
    a = escolher([dict(pika, nivel=8)], "PIKACHU", "GOLEM", 40, 1.0, [], {})
    assert a[0] == "devolver", a  # ninguém vence: o modelo decide
    assert escolher_quem_entra(time_, "ONIX", 14, []) == "GLOOM"  # planta contra pedra/terra
    print("combate: cenários ok")
