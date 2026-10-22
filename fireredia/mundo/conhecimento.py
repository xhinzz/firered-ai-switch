"""Conhecimento do FireRed tirado do código-fonte (pokefirered): espécies, treinadores, lojas e itens."""

import json
import math
import re
from functools import lru_cache

from fireredia.mundo import mapa

RAIZ = mapa.RAIZ
# ordem da história: (insígnia, líder) e depois a Liga
LIDERES = [
    ("Boulder", "TRAINER_LEADER_BROCK"),
    ("Cascade", "TRAINER_LEADER_MISTY"),
    ("Thunder", "TRAINER_LEADER_LT_SURGE"),
    ("Rainbow", "TRAINER_LEADER_ERIKA"),
    ("Soul", "TRAINER_LEADER_KOGA"),
    ("Marsh", "TRAINER_LEADER_SABRINA"),
    ("Volcano", "TRAINER_LEADER_BLAINE"),
    ("Earth", "TRAINER_LEADER_GIOVANNI"),
]
LIGA = [
    "TRAINER_ELITE_FOUR_LORELEI",
    "TRAINER_ELITE_FOUR_BRUNO",
    "TRAINER_ELITE_FOUR_AGATHA",
    "TRAINER_ELITE_FOUR_LANCE",
    "TRAINER_CHAMPION_FIRST_SQUIRTLE",
    "TRAINER_CHAMPION_FIRST_BULBASAUR",
    "TRAINER_CHAMPION_FIRST_CHARMANDER",
]
HMS = ("CUT", "FLY", "SURF", "STRENGTH", "FLASH", "ROCK_SMASH", "WATERFALL")


def _ler(caminho):
    return (RAIZ / caminho).read_text(encoding="utf-8", errors="replace")


@lru_cache
def _nomes_e_apelidos():
    """({ESPÉCIE: nome escrito no jogo}, {ESPÉCIE: apelido da troca com NPC}) dos dados do jogo."""
    nomes = dict(re.findall(r'\[SPECIES_(\w+)\] = _\("(.+?)"\)', _ler("src/data/text/species_names.h")))
    apelidos = {
        e: a
        for a, e in re.findall(
            r'\.nickname = _\("(.+?)"\),\s*\.species = SPECIES_(\w+)', _ler("src/data/ingame_trades.h")
        )
    }
    return nomes, apelidos


def nomes_na_tela(especie):
    """Como a espécie pode estar escrita na tela: MR_MIME -> ('MR. MIME', 'MIMIEN'); NIDORAN_M -> ('NIDORAN♂', ...)."""
    nomes, apelidos = _nomes_e_apelidos()
    return tuple(n for n in (nomes.get(especie, especie), apelidos.get(especie)) if n)


def _nome(id_, prefixo):
    return id_.removeprefix(prefixo)


@lru_cache
def itens():
    """ITEM_X -> (nome, preço, bolso)"""
    return {
        i["itemId"]: (i["english"].replace("�", "E"), i["price"], i["pocket"].removeprefix("POCKET_"))
        for i in json.loads(_ler("src/data/items.json"))["items"]
    }


@lru_cache
def especies():
    """SPECIES_X -> dados de batalha, evolução e golpes."""
    res = {}
    # "{" na linha seguinte: "[SPECIES_NONE] = {0}," na mesma linha engoliria a entrada do Bulbasaur
    for esp, corpo in re.findall(
        r"\[(SPECIES_\w+)\] =\s*\n\s*\{(.*?)\n    \},", _ler("src/data/pokemon/species_info.h"), re.S
    ):

        def campo(n, corpo=corpo):
            return (re.search(rf"\.{n} = ([^,\n]+)", corpo) or [None, None])[1]

        tipos = re.search(r"\.types = \{(\w+), (\w+)\}", corpo)
        if not tipos:
            continue
        res[esp] = {
            "tipos": list(dict.fromkeys(_nome(t, "TYPE_") for t in tipos.groups())),
            "base": {
                k: int(campo(f"base{k}") or 0) for k in ("HP", "Attack", "Defense", "SpAttack", "SpDefense", "Speed")
            },
            "captura": int(campo("catchRate") or 0),
            "xp": int(campo("expYield") or 0),
            "crescimento": (campo("growthRate") or "GROWTH_MEDIUM_FAST").removeprefix("GROWTH_"),
            "evolucoes": [],
            "golpes": [],
            "hms": [],
        }
    atual = None
    for linha in _ler("src/data/pokemon/evolution.h").splitlines():
        m = re.search(r"\[(SPECIES_\w+)\]", linha)
        if m:
            atual = m[1]
        for metodo, param, alvo in re.findall(r"\{(EVO_\w+), (\w+), (SPECIES_\w+)\}", linha):
            if atual in res:
                res[atual]["evolucoes"].append((_nome(metodo, "EVO_"), _nome(param, "ITEM_"), _nome(alvo, "SPECIES_")))
    listas = dict(
        re.findall(r"static const u16 (\w+)\[\] = \{(.*?)\};", _ler("src/data/pokemon/level_up_learnsets.h"), re.S)
    )
    for esp, lista in re.findall(r"\[(SPECIES_\w+)\] = (\w+),", _ler("src/data/pokemon/level_up_learnset_pointers.h")):
        if esp in res and lista in listas:
            res[esp]["golpes"] = [
                (int(n), _nome(g, "MOVE_"))
                for n, g in re.findall(r"LEVEL_UP_MOVE\(\s*(\d+), (MOVE_\w+)\)", listas[lista])
            ]
    for esp, corpo in re.findall(
        r"\[(SPECIES_\w+)\]\s*=\s*TMHM_LEARNSET\((.*?)\)\s*,", _ler("src/data/pokemon/tmhm_learnsets.h"), re.S
    ):
        if esp in res:
            res[esp]["hms"] = [h for h in HMS if re.search(rf"HM\d+_{h}\b", corpo)]
    return res


@lru_cache
def treinadores():
    """TRAINER_X -> {nome, classe, time: [(espécie, nível, golpes)]}"""
    partes, fonte = {}, _ler("src/data/trainer_parties.h")
    inicios = list(re.finditer(r"sParty_(\w+)\[\] = \{", fonte))
    # bloco a bloco: um regex só engolia o time seguinte a um comentário ("Start of actual trainer data")
    blocos = [
        (m[1], fonte[m.end() : inicios[k + 1].start() if k + 1 < len(inicios) else len(fonte)])
        for k, m in enumerate(inicios)
    ]
    for nome, corpo in blocos:
        partes[nome] = [
            (
                _nome(e, "SPECIES_"),
                int(n),
                [_nome(g.strip(), "MOVE_") for g in (gs or "").split(",") if g.strip() and g.strip() != "MOVE_NONE"],
            )
            for n, e, gs in re.findall(
                r"\.lvl = (\d+),\s*\.species = (SPECIES_\w+)(?:,\s*\.heldItem = \w+)?(?:,\s*\.moves = \{([^}]*)\})?",
                corpo,
            )
        ]
    res = {}
    for tid, corpo in re.findall(r"\[(TRAINER_\w+)\] = \{(.*?)\n    \},", _ler("src/data/trainers.h"), re.S):
        nome = re.search(r'\.trainerName = _\("([^"]*)"\)', corpo)
        classe = re.search(r"\.trainerClass = TRAINER_CLASS_(\w+)", corpo)
        party = re.search(r"\.party = \w+\(sParty_(\w+)\)", corpo)
        pic = re.search(r"\.trainerPic = TRAINER_PIC_(\w+)", corpo)
        if nome and party:
            res[tid] = {
                "nome": nome[1],
                "classe": classe[1] if classe else "",
                "time": partes.get(party[1], []),
                "pic": pic[1].lower() if pic else "",
            }
    return res


@lru_cache
def lojas():
    """MAP_X -> [(item, preço)] de cada balcão de Poké Mart (mapas com mais de um balcão juntam as listas)."""
    por_nome = {m["name"]: mid for mid, m in mapa.mapas().items()}
    res = {}
    for arq in (RAIZ / "data/maps").glob("*/scripts.inc"):
        texto = arq.read_text(encoding="utf-8", errors="replace")
        for rotulo in re.findall(r"pokemart (\w+)", texto):
            bloco = re.search(rf"{rotulo}::\s*((?:\.2byte ITEM_\w+\s*)+)", texto)
            if bloco and arq.parent.name in por_nome:
                lista = [i for i in re.findall(r"ITEM_\w+", bloco[1]) if i != "ITEM_NONE"]
                res.setdefault(por_nome[arq.parent.name], []).extend(
                    (itens()[i][0], itens()[i][1]) for i in lista if i in itens()
                )
    return res


ESPECIAIS = {"FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE", "DRAGON", "DARK"}  # Gen 3: categoria vem do tipo


@lru_cache
def golpes():
    """MOVE_X -> {tipo, poder, precisao, pp}"""
    res = {}
    for mid, corpo in re.findall(r"\[(MOVE_\w+)\] =\s*\n\s*\{(.*?)\n    \},", _ler("src/data/battle_moves.h"), re.S):

        def campo(n, corpo=corpo):
            return (re.search(rf"\.{n} = (\w+)", corpo) or [None, "0"])[1]

        res[mid] = {
            "tipo": campo("type").removeprefix("TYPE_"),
            "poder": int(campo("power")),
            "precisao": int(campo("accuracy")),
            "pp": int(campo("pp")),
        }
    return res


@lru_cache
def efeitos():
    """MOVE_X -> EFFECT_X (sem o prefixo)"""
    return {
        mid: (re.search(r"\.effect = EFFECT_(\w+)", corpo) or [None, "HIT"])[1]
        for mid, corpo in re.findall(r"\[(MOVE_\w+)\] =\s*\n\s*\{(.*?)\n    \},", _ler("src/data/battle_moves.h"), re.S)
    }


@lru_cache
def tms():
    """'TM39' / 'HM01' -> nome do golpe (ROCK_TOMB, CUT)"""
    return {
        f"{t}{n}": g for t, n, g in re.findall(r"\b(TM|HM)(\d\d)_(\w+?)\)", _ler("src/data/pokemon/tmhm_learnsets.h"))
    }


@lru_cache
def tms_da_especie():
    """SPECIES_X -> ['TM01', ..., 'HM01'] que a espécie aprende"""
    return {
        esp: sorted(set(re.findall(r"\b((?:TM|HM)\d\d)_", corpo)))
        for esp, corpo in re.findall(
            r"\[(SPECIES_\w+)\]\s*=\s*TMHM_LEARNSET\((.*?)\)\s*,", _ler("src/data/pokemon/tmhm_learnsets.h"), re.S
        )
    }


@lru_cache
def tabela_tipos():
    """(tipo do golpe, tipo do alvo) -> multiplicador; o que não está na tabela vale 1."""
    texto = re.search(r"gTypeEffectiveness\[\d*\] =\s*\{(.*?)\};", _ler_battle_main(), re.S)[1]
    mult = {
        "TYPE_MUL_NO_EFFECT": 0.0,
        "TYPE_MUL_NOT_EFFECTIVE": 0.5,
        "TYPE_MUL_SUPER_EFFECTIVE": 2.0,
        "TYPE_MUL_NORMAL": 1.0,
    }
    return {
        (a.removeprefix("TYPE_"), d.removeprefix("TYPE_")): mult[m]
        for a, d, m in re.findall(r"(TYPE_\w+), (TYPE_\w+), (TYPE_MUL_\w+)", texto)
        if "FORESIGHT" not in a
    }


@lru_cache
def _ler_battle_main():
    caminho = RAIZ / "src/battle_main.c"
    if not caminho.exists():  # fora do checkout esparso: só a tabela de tipos interessa
        import subprocess

        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_bytes(
            subprocess.run(
                ["git", "-C", str(RAIZ), "show", "HEAD:src/battle_main.c"], capture_output=True, check=True
            ).stdout
        )
    return caminho.read_text(encoding="utf-8", errors="replace")


def _chave(nome):
    return re.sub(r"[^A-Z0-9]", "", nome.upper().replace("É", "E"))  # POKé BALL == POKE BALL


@lru_cache
def _golpe_por_nome():
    """Nome como aparece na tela (THUNDERSHOCK, VICEGRIP) ou como id (THUNDER_SHOCK) -> MOVE_X."""
    res = {_chave(m.removeprefix("MOVE_")): m for m in golpes()}
    for mid, nome in re.findall(r'\[(MOVE_\w+)\]\s*=\s*_\("([^"]*)"\)', _ler("src/data/text/move_names.h")):
        res[_chave(nome)] = mid
    return res


@lru_cache
def nomes_golpes():
    """Nomes dos golpes como aparecem na tela (THUNDERSHOCK, VICEGRIP)."""
    return [
        nome
        for _, nome in re.findall(r'\[(MOVE_\w+)\]\s*=\s*_\("([^"]*)"\)', _ler("src/data/text/move_names.h"))
        if nome and not nome.startswith("-")
    ]


def pp_de(nome):
    g = golpes().get(_golpe_por_nome().get(_chave(nome), ""))
    return g["pp"] if g else None


def multiplicador(tipo_golpe, tipos_alvo):
    m = 1.0
    for t in tipos_alvo:
        m *= tabela_tipos().get((tipo_golpe, t), 1.0)
    return m


def analisar_golpes(golpes_meus, minha, inimiga):
    """Texto com cada golpe meu contra a espécie inimiga (tipo, categoria, poder, multiplicador, mesmo tipo) e o risco
    que os tipos dela representam para a minha."""
    eu, ela = especies().get(_especie_id(minha)), especies().get(_especie_id(inimiga))
    if not ela:
        return f"espécie {inimiga} não encontrada"
    linhas = [f"{_nome(_especie_id(inimiga), 'SPECIES_')}: tipos {'/'.join(ela['tipos'])}"]
    ranking = []
    for g in golpes_meus:
        nome = re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", g).strip().upper()  # tira o "PP 9/25" que a memória guarda junto
        dados = golpes().get(_golpe_por_nome().get(_chave(nome), ""))
        if not dados:
            ranking.append((-1, f"{nome}: golpe desconhecido"))
            continue
        m = multiplicador(dados["tipo"], ela["tipos"])
        stab = 1.5 if eu and dados["tipo"] in eu["tipos"] else 1.0
        forca = dados["poder"] * m * stab
        cat = "especial" if dados["tipo"] in ESPECIAIS else "físico"
        txt = (
            f"{nome}: {dados['tipo']} {cat}, poder {dados['poder'] or 'status'}, x{m:g} contra ela"
            f"{', mesmo tipo x1.5' if stab > 1 else ''}, precisão {dados['precisao']} -> força {forca:g}"
        )
        ranking.append((forca, txt))
    linhas += [t for _, t in sorted(ranking, reverse=True)]
    if eu:
        risco = ", ".join(f"{t} x{multiplicador(t, eu['tipos']):g}" for t in ela["tipos"])
        linhas.append(
            f"golpes do tipo dela contra {_nome(_especie_id(minha), 'SPECIES_')} ({'/'.join(eu['tipos'])}): {risco}"
        )
    return "\n".join(linhas)


@lru_cache
def numero_nacional():
    """número da Pokédex -> espécie (de 1 a 251 a constante SPECIES_ é o próprio número nacional)"""
    texto = _ler("include/constants/species.h")
    return {
        int(n): e.removeprefix("SPECIES_")
        for e, n in re.findall(r"#define (SPECIES_\w+)\s+(\d+)", texto)
        if 1 <= int(n) <= 251 and not e.startswith("SPECIES_OLD_UNOWN")
    }


def _atributo(base, nivel, hp=False, iv=15):
    """Fórmula de atributo da Gen 3 com IV médio e sem EV (selvagem é aleatório; o nosso varia ~10%)."""
    v = (2 * base + iv) * nivel // 100
    return v + nivel + 10 if hp else v + 5


def dano(golpe, atacante, nivel_a, alvo, nivel_d):
    """(dano mínimo, dano máximo, HP máximo estimado do alvo) pela fórmula da Gen 3, sem crítico."""
    g = golpes().get(_golpe_por_nome().get(_chave(re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", golpe)), ""))
    a, d = especies().get(_especie_id(atacante)), especies().get(_especie_id(alvo))
    if not (g and a and d):
        return None
    hp_alvo = _atributo(d["base"]["HP"], nivel_d, hp=True)
    if not g["poder"]:
        return 0, 0, hp_alvo
    especial = g["tipo"] in ESPECIAIS
    ataque = _atributo(a["base"]["SpAttack" if especial else "Attack"], nivel_a)
    defesa = _atributo(d["base"]["SpDefense" if especial else "Defense"], nivel_d)
    base = ((2 * nivel_a // 5 + 2) * g["poder"] * ataque // max(defesa, 1)) // 50 + 2
    maximo = int(base * (1.5 if g["tipo"] in a["tipos"] else 1) * multiplicador(g["tipo"], d["tipos"]))
    return int(maximo * 0.85), maximo, hp_alvo


LENDARIOS = {"ARTICUNO", "ZAPDOS", "MOLTRES", "MEWTWO", "MEW", "RAIKOU", "ENTEI", "SUICUNE", "LUGIA", "HO_OH", "DEOXYS"}
BOLAS = {"POKE BALL": 1.0, "GREAT BALL": 1.5, "ULTRA BALL": 2.0, "SAFARI BALL": 1.5, "MASTER BALL": 255.0}
STATUS_CAPTURA = {"": 1.0, "sono": 2.0, "congelado": 2.0, "paralisia": 1.5, "veneno": 1.5, "queimadura": 1.5}


def chance_captura(especie, hp_fracao, bola="POKE BALL", status=""):
    """Probabilidade de capturar numa bola, pela fórmula da Gen 3 (4 checagens de balanço)."""
    e = especies().get(_especie_id(especie))
    if not e:
        return None
    mult_bola = BOLAS.get(bola.upper().replace("É", "E").replace("é", "E"), 1.0)
    a = (3 - 2 * max(hp_fracao, 0.01)) / 3 * e["captura"] * mult_bola * STATUS_CAPTURA.get(status, 1.0)
    if a >= 255:
        return 1.0
    b = 1048560 / (16711680 / a) ** 0.25
    return min((b / 65536) ** 4, 1.0)


# golpes sem dano: quanto valem para um jogador (sono e paralisia ainda ajudam a capturar)
VALOR_STATUS = {
    "SLEEP": 60,
    "PARALYZE": 50,
    "TOXIC": 35,
    "LEECH_SEED": 30,
    "ATTACK_UP_2": 40,
    "SPECIAL_ATTACK_UP_2": 40,
    "SPEED_UP_2": 30,
    "CONFUSE": 25,
    "POISON": 25,
    "REST": 30,
    "SUBSTITUTE": 25,
    "DEFENSE_UP_2": 20,
    "SPECIAL_DEFENSE_UP_2": 20,
    "REFLECT": 20,
    "LIGHT_SCREEN": 20,
    "HAZE": 15,
    "RESTORE_HP": 35,
}
DANO_FIXO = {"LEVEL_DAMAGE": 60, "DRAGON_RAGE": 45, "SONICBOOM": 25, "OHKO": 30, "SUPER_FANG": 40}
AJUSTE_EFEITO = {
    "RECHARGE": 0.6,
    "MULTI_HIT": 3.0,
    "DOUBLE_HIT": 2.0,
    "EXPLOSION": 0.2,
    "RECOIL": 0.9,
    "HIGH_CRITICAL": 1.1,
    "ABSORB": 1.1,
    "SEMI_INVULNERABLE": 0.9,
    "RAZOR_WIND": 0.5,
    "SKY_ATTACK": 0.5,
    "SOLAR_BEAM": 0.7,
    "SKULL_BASH": 0.5,
    "TRAP": 0.9,
    "FOCUS_PUNCH": 0.4,
    "OVERHEAT": 0.7,
    "SUPERPOWER": 0.8,
    "FUTURE_SIGHT": 0.6,
}
GOLPES_DE_HM = {"CUT", "FLY", "SURF", "STRENGTH", "FLASH", "ROCK_SMASH", "WATERFALL", "DIVE"}


def _id_golpe(nome):
    return _golpe_por_nome().get(_chave(re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", nome)))


def valor_golpe(mid, especie):
    """Nota do golpe para essa espécie: poder efetivo (precisão, mesmo tipo, atributo de ataque usado) ou valor do status."""
    g, ef, e = golpes()[mid], efeitos().get(mid, "HIT"), especies()[_especie_id(especie)]
    if ef in DANO_FIXO:
        return DANO_FIXO[ef]
    if g["poder"] <= 1:
        return VALOR_STATUS.get(ef, 8)
    atributo = e["base"]["SpAttack" if g["tipo"] in ESPECIAIS else "Attack"]
    stab = 1.5 if g["tipo"] in e["tipos"] else 1.0
    return round(g["poder"] * g["precisao"] / 100 * stab * atributo / 80 * AJUSTE_EFEITO.get(ef, 1.0), 1)


def _descricao(mid, especie):
    g, ef = golpes()[mid], efeitos().get(mid, "HIT")
    cat = "status" if g["poder"] <= 1 and ef not in DANO_FIXO else ("especial" if g["tipo"] in ESPECIAIS else "físico")
    return (
        f"{mid.removeprefix('MOVE_')} ({g['tipo']} {cat}, poder {g['poder']}, precisão {g['precisao']}, PP {g['pp']}"
        f"{', efeito ' + ef if ef != 'HIT' else ''}) nota {valor_golpe(mid, especie):g}"
    )


def avaliar_golpes(especie, nivel, golpes_atuais, insignias=(), tms_na_mochila=()):
    """Avaliação do moveset como um jogador faria: nota de cada golpe, cobertura contra o próximo líder, golpes
    repetidos ou fracos, o que vem pelos próximos níveis e por TM/HM, e o que trocar."""
    esp = _especie_id(especie)
    if esp not in especies():
        return f"espécie {especie} não encontrada"
    atuais = [m for m in (_id_golpe(g) for g in golpes_atuais) if m]
    linhas = [f"{esp.removeprefix('SPECIES_')} nv {nivel} ({'/'.join(especies()[esp]['tipos'])})", "Golpes atuais:"]
    linhas += [f"  {_descricao(m, especie)}" for m in atuais]
    lider = proximo_lider(insignias)
    if lider:
        linhas.append(f"Contra o próximo líder {lider['nome']}:")
        for alvo, nv in lider["time"]:
            tipos_alvo = especies()[_especie_id(alvo)]["tipos"]
            melhor = max(
                ((multiplicador(golpes()[m]["tipo"], tipos_alvo), m) for m in atuais if golpes()[m]["poder"] > 1),
                default=(0, None),
            )
            linhas.append(
                f"  {alvo} nv {nv} ({'/'.join(tipos_alvo)}): melhor golpe "
                f"{melhor[1].removeprefix('MOVE_') + f' x{melhor[0]:g}' if melhor[1] else 'nenhum de dano'}"
            )
    tipos_dano = {}
    for m in atuais:
        if golpes()[m]["poder"] > 1:
            tipos_dano.setdefault(golpes()[m]["tipo"], []).append(m)
    for tipo, ms in tipos_dano.items():
        if len(ms) > 1:
            linhas.append(
                f"Repetidos ({tipo}): " + ", ".join(m.removeprefix("MOVE_") for m in ms) + " — vale trocar o mais fraco"
            )
    trocaveis = [m for m in atuais if m.removeprefix("MOVE_") not in GOLPES_DE_HM]
    pior = min(trocaveis, key=lambda m: valor_golpe(m, especie), default=None)
    if pior:
        linhas.append(
            f"Golpe mais fraco (candidato a sair): {pior.removeprefix('MOVE_')} nota {valor_golpe(pior, especie):g}"
        )
    futuros = [(n, "MOVE_" + g) for n, g in especies()[esp]["golpes"] if n > nivel and "MOVE_" + g in golpes()]
    if futuros:
        linhas.append("Próximos por nível: " + "; ".join(f"nv {n} {_descricao(m, especie)}" for n, m in futuros[:6]))
    for evo_metodo, evo_param, evo_alvo in especies()[esp]["evolucoes"]:
        linhas.append(f"Evolui: {evo_metodo.lower()} {evo_param} -> {evo_alvo}")
    compat = [(t, "MOVE_" + tms()[t]) for t in tms_da_especie().get(esp, []) if "MOVE_" + tms()[t] in golpes()]
    tem = {t.upper().replace(" ", "") for t in tms_na_mochila}
    if compat:
        bons = sorted(compat, key=lambda tm: -valor_golpe(tm[1], especie))[:8]
        linhas.append(
            "TM/HM que aprende (melhores): "
            + "; ".join(
                f"{t}{' [NA MOCHILA]' if t in tem else ''} {m.removeprefix('MOVE_')} nota {valor_golpe(m, especie):g}"
                for t, m in bons
            )
        )
    return "\n".join(linhas)


def decidir_golpe_novo(especie, nivel, golpes_atuais, novo, insignias=()):
    """Texto da decisão sobre o golpe novo (para o modelo)."""
    return escolher_golpe_novo(especie, nivel, golpes_atuais, novo, insignias)[2]


PROTEGIDOS = {"FARFETCHD": ("KNOCK_OFF",), "MR_MIME": ("RECYCLE",)}  # golpes que o ACE usa: nem nível nem TM/HM apagam


def escolher_golpe_novo(especie, nivel, golpes_atuais, novo, insignias=(), protegidos=None):
    """(aprender, MOVE_ a esquecer ou None, texto). Leva em conta a nota e a cobertura contra o próximo líder; nunca
    esquece golpe de HM, o único golpe de dano nem os 'protegidos' (ex.: KNOCK_OFF guardado para o ACE)."""
    novo_id = _id_golpe(novo)
    atuais = [m for m in (_id_golpe(g) for g in golpes_atuais) if m]
    if not novo_id:
        return False, None, f"golpe {novo} desconhecido"
    lider = proximo_lider(insignias)
    tipos_lider = [especies()[_especie_id(a)]["tipos"] for a, _ in (lider["time"] if lider else [])]

    def nota(m, conjunto):
        cobre = any(multiplicador(golpes()[m]["tipo"], t) > 1 for t in tipos_lider) and golpes()[m]["poder"] > 1
        sozinho = cobre and not any(
            multiplicador(golpes()[o]["tipo"], t) > 1
            for o in conjunto
            if o != m and golpes()[o]["poder"] > 1
            for t in tipos_lider
        )
        return valor_golpe(m, especie) + (30 if sozinho else 0)

    if len(atuais) < 4:
        return True, None, f"aprenda {novo_id.removeprefix('MOVE_')}: ainda há espaço"
    fixos = GOLPES_DE_HM | {
        p.upper().replace(" ", "_") for p in (PROTEGIDOS.get(especie, ()) if protegidos is None else protegidos)
    }
    trocaveis = [m for m in atuais if m.removeprefix("MOVE_") not in fixos]

    def dano_restante(sai):
        return any(golpes()[m]["poder"] > 1 for m in atuais + [novo_id] if m != sai)

    pior = min((m for m in trocaveis if dano_restante(m)), key=lambda m: nota(m, atuais), default=None)
    nova = nota(novo_id, [m for m in atuais if m != pior] + [novo_id]) if pior else 0
    if pior and nova > nota(pior, atuais) * 1.1:
        return (
            True,
            pior,
            (
                f"aprenda {novo_id.removeprefix('MOVE_')} (nota {nova:g}) esquecendo "
                f"{pior.removeprefix('MOVE_')} (nota {nota(pior, atuais):g})"
            ),
        )
    return (
        False,
        None,
        (
            f"não aprenda {novo_id.removeprefix('MOVE_')} (nota {nova:g}): o golpe mais fraco que poderia "
            f"sair, {pior.removeprefix('MOVE_') if pior else '-'}, vale mais ou é o único de dano"
        ),
    )


@lru_cache
def _scripts(mapa_id):
    """(rótulos -> corpo, quem chama cada rótulo) do scripts.inc do mapa."""
    arq = RAIZ / "data/maps" / mapa.mapas()[mapa_id]["name"] / "scripts.inc"
    texto = arq.read_text(encoding="utf-8", errors="replace") if arq.exists() else ""
    corpos = dict(re.findall(r"^(\w+)::\s*\n(.*?)(?=^\w+::|\Z)", texto, re.S | re.M))
    chamadores = {}
    for rotulo, corpo in corpos.items():
        for alvo in re.findall(r"\b(?:goto|call|goto_if_\w+|call_if_\w+)\b[^\n]*?\b(\w+_EventScript_\w+)", corpo):
            chamadores.setdefault(alvo, set()).add(rotulo)
    return corpos, chamadores


def _quem_dispara(mapa_id, rotulo):
    """(x, y) do objeto ou placa do mapa cujo script chega até o rótulo (subindo por goto/call)."""
    corpos, chamadores = _scripts(mapa_id)
    m = mapa.mapas()[mapa_id]
    origem = {
        o.get("script"): (o["x"], o["y"])
        for o in (m.get("object_events") or []) + (m.get("bg_events") or [])
        if o.get("script")
    }
    fila, vistos = [rotulo], {rotulo}
    while fila:
        r = fila.pop(0)
        if r in origem:
            return origem[r]
        for c in chamadores.get(r, ()):
            if c not in vistos:
                vistos.add(c)
                fila.append(c)
    return None


@lru_cache
def itens_dos_mapas():
    """MAP_X -> [{x, y, item, tipo: chao|escondido, debaixo}] — todos os itens do chão e escondidos do jogo."""
    # os scripts das bolinhas de item ficam todos num arquivo global
    bolinhas = dict(
        re.findall(r"^(\w+)::\s*\n\s*finditem (ITEM_\w+)", _ler("data/scripts/item_ball_scripts.inc"), re.M)
    )
    res = {}
    for mid, m in mapa.mapas().items():
        corpos, _ = _scripts(mid)
        lista = []
        for o in m.get("object_events") or []:
            if o.get("graphics_id") == "OBJ_EVENT_GFX_ITEM_BALL":
                achado = (
                    bolinhas.get(o.get("script", ""))
                    or (re.search(r"finditem (ITEM_\w+)", corpos.get(o.get("script", ""), "")) or [None, None])[1]
                )
                item = [None, achado] if achado else None
                lista.append(
                    {
                        "x": o["x"],
                        "y": o["y"],
                        "item": itens().get(item[1], (item[1],))[0] if item else "?",
                        "tipo": "chao",
                        "debaixo": False,
                    }
                )
        for b in m.get("bg_events") or []:
            if b.get("type") == "hidden_item":
                lista.append(
                    {
                        "x": b["x"],
                        "y": b["y"],
                        "item": itens().get(b["item"], (b["item"],))[0],
                        "tipo": "escondido",
                        "debaixo": bool(b.get("underfoot")),
                    }
                )
        if lista:
            res[mid] = lista
    return res


@lru_cache
def obtencoes():
    """Pokémon conseguidos falando com alguém: presentes, prêmios, trocas, ovo e encontros fixos (Snorlax, lendários).

    [{especie, nivel, tipo, mapa, x, y, pede}] — x/y é o NPC/objeto que dispara; pede = espécie pedida na troca."""
    trocas = {
        t: (e.removeprefix("SPECIES_"), p.removeprefix("SPECIES_"))
        for t, e, p in re.findall(
            r"\[(INGAME_TRADE_\w+)\]\s*=\s*\{.*?\.species = (SPECIES_\w+).*?\.requestedSpecies = (SPECIES_\w+)",
            _ler("src/data/ingame_trades.h"),
            re.S,
        )
    }
    res = []
    for mid in mapa.mapas():
        corpos, _ = _scripts(mid)
        for rotulo, corpo in corpos.items():
            achados = [(e, int(n), "presente") for e, n in re.findall(r"givemon (SPECIES_\w+), (\d+)", corpo)]
            achados += [
                (e, int(n), "encontro fixo (batalha)")
                for e, n in re.findall(r"setwildbattle (SPECIES_\w+), (\d+)", corpo)
            ]
            achados += [(e, 5, "ovo") for e in re.findall(r"giveegg (SPECIES_\w+)", corpo)]
            if "givemon VAR_TEMP_1" in corpo or re.search(r"setvar VAR_TEMP_1, SPECIES_\w+", corpo):
                achados += [(e, 0, "prêmio/escolha") for e in re.findall(r"setvar VAR_TEMP_1, (SPECIES_\w+)", corpo)]
            for t in re.findall(r"\b(INGAME_TRADE_\w+)\b", corpo):
                if t in trocas:
                    achados.append(("SPECIES_" + trocas[t][0], 0, f"troca por {trocas[t][1]}"))
            for esp, nivel, tipo in achados:
                pos = _quem_dispara(mid, rotulo)
                res.append(
                    {
                        "especie": esp.removeprefix("SPECIES_"),
                        "nivel": nivel,
                        "tipo": tipo,
                        "mapa": mid,
                        "x": pos[0] if pos else None,
                        "y": pos[1] if pos else None,
                        "pede": tipo.removeprefix("troca por ") if tipo.startswith("troca") else None,
                    }
                )
    unicos = {}
    for o in res:  # scripts repetem a mesma entrega em ramos diferentes; "presente" com nível vence "prêmio/escolha"
        chave = (o["especie"], o["mapa"])
        if chave not in unicos or (o["tipo"] == "presente" and unicos[chave]["tipo"] != "presente"):
            unicos[chave] = o
    return list(unicos.values())


def obtencao_de(especie):
    """Como conseguir uma espécie falando com alguém (presente, troca, prêmio, ovo, encontro fixo)."""
    alvo = _especie_id(especie).removeprefix("SPECIES_")
    return [o for o in obtencoes() if o["especie"] == alvo]


# party_menu.c: o golpe de campo de índice i exige a insígnia i+1 (FlagGet(FLAG_BADGE01_GET + fieldMove))
INSIGNIA_DO_CAMPO = {
    "FLASH": "Boulder",
    "CUT": "Cascade",
    "FLY": "Thunder",
    "STRENGTH": "Rainbow",
    "SURF": "Soul",
    "ROCK_SMASH": "Marsh",
    "WATERFALL": "Volcano",
}
VARAS = {"old rod": "OLD ROD", "good rod": "GOOD ROD", "super rod": "SUPER ROD"}


def capacidades(time_, insignias):
    """Golpes de campo que o time pode usar agora: alguém sabe o golpe e a insígnia que libera já foi ganha."""
    tem = " ".join(insignias).lower()
    sabe = {_id_golpe(g) for p in time_ for g in (p.get("golpes") or [])}
    return {g.lower() for g, ins in INSIGNIA_DO_CAMPO.items() if f"MOVE_{g}" in sabe and ins.lower() in tem}


def pokemon_faltando(capturados, capacidades_, mochila, alcancaveis=None):
    """Espécies de Kanto que faltam, agrupadas por como conseguir: dá agora, precisa de algo, por evolução, outros.

    alcancaveis = {mapa: distância} de navegacao.Mundo.alcancaveis; cada espécie aparece no lugar mais perto."""
    perto = (lambda r: (alcancaveis.get(r[0], 1 << 30), -r[4])) if alcancaveis else (lambda r: -r[4])
    tem = {c.upper() for c in capturados}
    itens_chave = {k.upper() for k in mochila}
    agora, depois, evolucao, outros = {}, [], [], []
    for num in range(1, 152):
        esp = numero_nacional()[num]
        if esp in tem:
            continue
        locais = mapa.onde_encontrar(esp)
        pre_todas = [
            s.removeprefix("SPECIES_")
            for s, e in especies().items()
            if any(alvo == esp for _, _, alvo in e["evolucoes"]) and s in obteniveis()
        ]
        pre = [p for p in pre_todas if p in tem] or pre_todas
        livres, presos = [], []
        for m, met, a, b, c in locais:
            falta = (
                "SURF"
                if met == "surf" and "surf" not in capacidades_
                else "ROCK SMASH"
                if met == "rock smash" and "rock_smash" not in capacidades_
                else VARAS[met]
                if met in VARAS and VARAS[met] not in itens_chave
                else "caminho (HM ou evento da história)"
                if alcancaveis is not None and m not in alcancaveis
                else None
            )
            (presos if falta else livres).append((m, met, a, b, c, falta))
        if livres:
            m, met, a, b, c, _ = min(livres, key=perto)
            agora.setdefault(m, []).append(f"{esp} ({met} nv {a}-{b}, {c}%)")
        elif pre:
            e = especies()["SPECIES_" + pre[0]]
            como = next(f"{mt.lower()} {p}" for mt, p, alvo in e["evolucoes"] if alvo == esp)
            evolucao.append(f"{esp}: evoluir {pre[0]} ({como}){'' if pre[0] in tem else f' — capture {pre[0]} antes'}")
        elif presos:
            m, met, a, b, c, falta = presos[0]
            depois.append(f"{esp}: {m} ({met} nv {a}-{b}) — precisa de {falta}")
        else:
            outros.append(esp)
    linhas = [f"Faltam {151 - len(tem & set(numero_nacional()[i] for i in range(1, 152)))} de 151."]
    if agora:
        linhas.append(
            "Alcançáveis a pé com os golpes de campo atuais, do mais perto ao mais longe (guardas e eventos da "
            "história podem fechar alguns — ex.: Safari Zone, Rota 23, Pokémon Tower):"
        )
        ordem = (lambda kv: alcancaveis.get(kv[0], 1 << 30)) if alcancaveis else (lambda kv: -len(kv[1]))
        linhas += [f"  {m}: {', '.join(es)}" for m, es in sorted(agora.items(), key=ordem)]
    if evolucao:
        linhas.append("Por evolução de quem você já tem: " + "; ".join(evolucao))
    if depois:
        linhas.append("Precisam de algo antes: " + "; ".join(depois))
    if outros:
        linhas.append("Não aparecem selvagens (presente, troca, fóssil, evento ou lendário): " + ", ".join(outros))
    return "\n".join(linhas)


def _especie_id(nome):
    """NIDORAN♀ -> SPECIES_NIDORAN_F, MR. MIME -> SPECIES_MR_MIME, FARFETCH'D -> SPECIES_FARFETCHD"""
    n = nome.strip().upper().replace("♀", "_F").replace("♂", "_M").replace(".", "").replace("'", "").replace("-", "_")
    return "SPECIES_" + re.sub(r"[\s_]+", "_", n).strip("_").removeprefix("SPECIES_")


def info_pokemon(nome):
    e = especies().get(_especie_id(nome))
    if not e:
        return None
    b = e["base"]
    evo = "; ".join(f"{m.lower()} {p} -> {a}" for m, p, a in e["evolucoes"]) or "não evolui"
    golpes = ", ".join(f"{n}:{g}" for n, g in e["golpes"])
    return (
        f"{_nome(_especie_id(nome), 'SPECIES_')}: tipos {'/'.join(e['tipos'])}; base HP {b['HP']} Atk {b['Attack']} "
        f"Def {b['Defense']} SpA {b['SpAttack']} SpD {b['SpDefense']} Spe {b['Speed']} (total {sum(b.values())}); "
        f"taxa de captura {e['captura']}/255; evolução: {evo}; golpes por nível: {golpes}; "
        f"HMs que aprende: {', '.join(e['hms']) or 'nenhum'}"
    )


def info_treinador(busca):
    """Treinadores cujo id ou nome contém o texto, com o time."""
    busca = busca.strip().upper().replace(" ", "_")
    achados = [(tid, t) for tid, t in treinadores().items() if busca in tid or busca == t["nome"].upper()]
    return "\n".join(
        f"{tid} ({t['classe']} {t['nome']}): "
        + "; ".join(f"{e} nv {n}" + (f" [{', '.join(g)}]" if g else "") for e, n, g in t["time"])
        for tid, t in achados[:12]
    )


def proximos_desafios(insignias):
    """Próximo líder (pela ordem da história) e o caminho até a Liga, com o nível do Pokémon mais forte de cada um."""
    tem = {i.lower() for i in insignias}
    linhas = []
    for insignia, tid in LIDERES:
        t = treinadores()[tid]
        marca = "feito" if any(insignia.lower() in i for i in tem) else "falta"
        linhas.append(f"{insignia} Badge — {t['nome']} [{marca}]: " + "; ".join(f"{e} {n}" for e, n, _ in t["time"]))
    for tid in LIGA[:4]:
        t = treinadores()[tid]
        linhas.append(f"Elite dos 4 {t['nome']}: " + "; ".join(f"{e} {n}" for e, n, _ in t["time"]))
    t = treinadores()[LIGA[4]]
    linhas.append(f"Campeão (rival; time muda conforme o inicial dele): ás nível {max(n for _, n, _ in t['time'])}")
    return "\n".join(linhas)


@lru_cache
def obteniveis():
    """Espécies selvagens no FireRed e suas evoluções (o resto da Pokédex nacional não aparece no jogo normal)."""
    base = {"SPECIES_" + e for metodos in mapa.selvagens().values() for d in metodos.values() for e in d}
    base |= {
        "SPECIES_" + e
        for e in (
            "BULBASAUR",
            "CHARMANDER",
            "SQUIRTLE",
            "EEVEE",
            "LAPRAS",
            "HITMONLEE",
            "HITMONCHAN",
            "OMANYTE",
            "KABUTO",
            "AERODACTYL",
            "SNORLAX",
            "PORYGON",
            "MAGIKARP",
            "KOFFING",
        )
    }
    mudou = True
    while mudou:
        novos = {"SPECIES_" + alvo for s in base if s in especies() for _, _, alvo in especies()[s]["evolucoes"]} - base
        base |= novos
        mudou = bool(novos)
    return base


def proximo_lider(insignias):
    """{insignia, nome, pic, time} do primeiro líder ainda sem insígnia, ou None depois das oito."""
    tem = " ".join(i.lower() for i in insignias)
    for insignia, tid in LIDERES:
        if insignia.lower() not in tem:
            t = treinadores()[tid]
            return {"insignia": insignia, "nome": t["nome"], "pic": t["pic"], "time": [(e, n) for e, n, _ in t["time"]]}
    return None


def quem_aprende_hm(hm):
    hm = hm.strip().upper().replace(" ", "_")
    return sorted(_nome(s, "SPECIES_") for s, e in especies().items() if hm in e["hms"] and s in obteniveis())


# ---------------- planejamento do time ----------------

# experiência total por nível (pokemon.c, gExperienceTables)
XP_NIVEL = {
    "FAST": lambda n: 4 * n**3 // 5,
    "MEDIUM_FAST": lambda n: n**3,
    "MEDIUM_SLOW": lambda n: 6 * n**3 // 5 - 15 * n**2 + 100 * n - 140,
    "SLOW": lambda n: 5 * n**3 // 4,
}
METODOS_TREINO = {"grama/caverna": None, "surf": "surf"}


def xp_para(especie, de, ate):
    e = especies().get(_especie_id(especie))
    curva = XP_NIVEL.get(e["crescimento"] if e else "", XP_NIVEL["MEDIUM_FAST"])
    return max(curva(ate) - curva(max(de, 2)), 0)


def forma_final(esp_id):
    """(espécie final sem precisar de troca, ['nv 16 -> CHARMELEON', 'thunder_stone -> RAICHU'])."""
    atual, passos = esp_id, []
    while True:
        evs = [e for e in especies().get(atual, {}).get("evolucoes", []) if not e[0].startswith("TRADE")]
        if not evs:
            return atual, passos
        metodo, param, alvo = evs[0]
        passos.append(
            f"{'nv ' + param if metodo == 'LEVEL' else param.lower() if metodo == 'ITEM' else metodo.lower()} -> {alvo}"
        )
        atual = "SPECIES_" + alvo


@lru_cache
def _raiz():
    """SPECIES_X -> primeira forma da linha evolutiva (para não contar Pidgey e Pidgeotto como duas opções)."""
    pai = {"SPECIES_" + alvo: s for s, e in especies().items() for _, _, alvo in e["evolucoes"]}
    res = {}
    for s in especies():
        r = s
        while r in pai:
            r = pai[r]
        res[s] = r
    return res


def _adversarios(insignias):
    """(próximo líder, [os que vêm depois até o Campeão]) como listas de (espécie, nível)."""
    tem = " ".join(i.lower() for i in insignias)
    fila = [tid for ins, tid in LIDERES if ins.lower() not in tem] + LIGA[:5]
    times = [[(e, n) for e, n, _ in treinadores()[tid]["time"]] for tid in fila]
    return (fila[0], times[0]), times[1:]


def _valor(final, prox, resto):
    """Nota da forma final para o time: atributos totais e vantagem de tipo contra o próximo líder e o resto."""
    e = especies()[final]

    def contar(times):
        bom = ruim = 0
        for time_ in times:
            for esp, _ in time_:
                alvo = especies().get("SPECIES_" + esp)
                if alvo:
                    bom += max(multiplicador(t, alvo["tipos"]) for t in e["tipos"]) >= 2
                    ruim += max(multiplicador(t, e["tipos"]) for t in alvo["tipos"]) >= 2
        return bom, ruim

    bom_p, ruim_p = contar([prox])
    bom_r, ruim_r = contar(resto)
    # o longo prazo pesa mais que o próximo líder: o time vai até a Liga
    return sum(e["base"].values()) / 100 + 0.4 * bom_p - 0.25 * ruim_p + 0.12 * bom_r - 0.06 * ruim_r


def _onde_capturar(alcancaveis, capacidades_, mochila, donos=()):
    """{linha (raiz): (espécie, mapa, método, nív mín, nív máx, ordem)} do lugar mais perto onde dá para pegar agora."""
    varas = {k.upper() for k in mochila}
    res = {}
    for m, ordem in sorted(alcancaveis.items(), key=lambda kv: kv[1]):
        for met, dados in mapa.selvagens().get(m, {}).items():
            if (
                (met == "surf" and "surf" not in capacidades_)
                or (met == "rock smash" and "rock_smash" not in capacidades_)
                or (met in VARAS and VARAS[met] not in varas)
            ):
                continue
            for esp, (a, b, _) in dados.items():
                linha = _raiz().get("SPECIES_" + esp)
                atual = res.get(linha)
                if linha and (not atual or (atual[5] == ordem and b > atual[4])):
                    res[linha] = (esp, m, met, a, b, ordem)
    for o in obtencoes():  # presentes e compras (Magikarp, Eevee, Lapras...) onde dá para chegar
        linha = _raiz().get("SPECIES_" + o["especie"])
        if (o["pede"] and o["pede"] not in donos) or o["tipo"].startswith("encontro"):
            continue  # troca exige ter a espécie pedida; encontro fixo (Snorlax, lendários) depende de evento da história
        if linha and o["mapa"] in alcancaveis and linha not in res:
            res[linha] = (o["especie"], o["mapa"], o["tipo"], o["nivel"] or 0, o["nivel"] or 0, alcancaveis[o["mapa"]])
    return res


# ARENA TRAP / SHADOW TAG (species_info.h): o treinado não consegue sair para a escolta nem fugir
PRENDEM = {"DIGLETT", "DUGTRIO", "TRAPINCH", "WYNAUT", "WOBBUFFET"}


def onde_treinar(especie, nivel, alvo, escolta, alcancaveis, capacidades_=(), max_opcoes=3):
    """Mapas alcançáveis para subir de nivel até alvo, com a estimativa de batalhas.

    Sozinho: selvagens até nivel+1. Escoltado (escolta = (espécie, nível)): o treinado começa a batalha e troca para
    a escolta no 1º turno; a experiência é dividida por 2 (Gen 3: metade para cada participante)."""
    falta = xp_para(especie, nivel, alvo)
    if not falta:
        return []
    opcoes = []
    for m, ordem in alcancaveis.items():
        for met, dados in mapa.selvagens().get(m, {}).items():
            if met not in METODOS_TREINO or (METODOS_TREINO[met] and METODOS_TREINO[met] not in capacidades_):
                continue
            total = sum(c for _, _, c in dados.values())
            xp = (
                sum(
                    especies().get("SPECIES_" + e, {}).get("xp", 0) * (a + b) / 2 / 7 * c
                    for e, (a, b, c) in dados.items()
                )
                / total
            )
            alto = max(b for _, b, _ in dados.values())
            if alto <= nivel + 1:
                modo, ganho = "sozinho", xp
            elif escolta and alto + 4 <= escolta[1] and not PRENDEM & set(dados):
                modo, ganho = f"escoltado por {escolta[0]}", xp / 2
            else:
                continue
            batalhas = falta / max(ganho, 1)
            opcoes.append(
                (batalhas * (1 + ordem / 15), m, met, min(a for a, _, _ in dados.values()), alto, modo, batalhas)
            )
    return sorted(opcoes)[:max_opcoes]


def avaliar_time(time_, pc, insignias, alcancaveis, capacidades_=(), mochila=(), restricao=""):
    """Relatório para montar o time: o próximo desafio e o nível alvo, a nota de cada Pokémon (forma final, tipos contra
    os próximos adversários), o time sugerido de 6 (seus e capturáveis agora), quem guardar e onde treinar quem fica."""
    (lider_id, prox), resto = _adversarios(insignias)
    lider = treinadores()[lider_id]
    as_ = max(n for _, n in prox)
    alvo = as_ + 2
    tipo_restrito = (
        restricao.strip().upper()
        if restricao and restricao.strip().upper() in {t for e in especies().values() for t in e["tipos"]}
        else None
    )
    linhas = [
        f"Próximo desafio: {lider['nome']} ({', '.join(f'{e} {n}' for e, n in prox)}). Nível alvo do time: {alvo} "
        f"(ás {as_} + 2); quem só entra contra um tipo específico pode ficar uns 3 níveis abaixo."
    ]

    def ficha(esp, nivel, origem):
        eid = _especie_id(esp)
        final, passos = forma_final(eid)
        ok_restricao = not tipo_restrito or tipo_restrito in especies()[final]["tipos"]
        return {
            "esp": eid.removeprefix("SPECIES_"),
            "nivel": nivel,
            "origem": origem,
            "final": final.removeprefix("SPECIES_"),
            "passos": passos,
            "linha": _raiz().get(eid),
            "tipos": especies()[final]["tipos"],
            "nota": _valor(final, prox, resto) if ok_restricao else -99,
            "restricao_ok": ok_restricao,
        }

    meus = [ficha(p["especie"], p.get("nivel") or 0, "time") for p in time_ if p.get("especie")] + [
        ficha(p["especie"], p.get("nivel") or 0, "pc") for p in pc if p.get("especie")
    ]
    meus = [m for m in meus if m["linha"]]
    capturaveis = _onde_capturar(alcancaveis, capacidades_, mochila, {f["esp"] for f in meus}) if alcancaveis else {}
    novos = []
    for esp, m, met, a, b, ordem in capturaveis.values():
        f = ficha(esp, b, f"capturar em {m} ({met} nv {a}-{b})")
        f["ordem"] = ordem
        novos.append(f)

    # por linha evolutiva fica a melhor opção: o seu de maior nível ou um capturável bem acima dele
    por_linha = {}
    for f in sorted(meus, key=lambda f: -f["nivel"]):
        por_linha.setdefault(f["linha"], f)
    substitui = {}
    for f in novos:
        meu = por_linha.get(f["linha"])
        if not meu:
            por_linha[f["linha"]] = f
        elif f["nivel"] >= meu["nivel"] + 6:
            substitui[f["linha"]] = (meu, f)
    escolhidos = []
    pool = list(por_linha.values())
    while pool and len(escolhidos) < 6:

        def marginal(f):
            repetidos = sum(t in g["tipos"] for g in escolhidos for t in f["tipos"])
            nivel = min(f["nivel"], alvo) / max(alvo, 1)  # quem já está no nível poupa dezenas de batalhas
            return f["nota"] - 0.8 * repetidos + 2.5 * nivel - (0.03 * f.get("ordem", 0))

        melhor = max(pool, key=marginal)
        if melhor["nota"] < -50:
            break
        escolhidos.append(melhor)
        pool.remove(melhor)

    linhas.append("Time sugerido (nota = atributos da forma final + vantagem de tipo; a ordem não importa):")
    for f in escolhidos:
        evo = f" -> {' / '.join(f['passos'])}" if f["passos"] else ""
        sub = substitui.get(f["linha"])
        extra = (
            f" | há {sub[1]['esp']} nv {sub[1]['nivel']} para {sub[1]['origem']}: capturar sai mais barato que treinar "
            f"o seu nv {sub[0]['nivel']}"
            if sub and f is sub[0]
            else ""
        )
        linhas.append(
            f"  {f['esp']} nv {f['nivel']} [{f['origem']}] {'/'.join(f['tipos'])}{evo} nota {f['nota']:.1f}{extra}"
        )
    nomes = {id(f) for f in escolhidos}
    fora = [f for f in meus if id(f) not in nomes]
    if fora:
        linhas.append("Fora do time sugerido (guardar no PC quando o time estiver cheio e precisar da vaga):")
        for f in fora:
            motivo = (
                "fora da restrição"
                if not f["restricao_ok"]
                else "linha repetida (fica o de nível maior)"
                if por_linha.get(f["linha"]) is not f
                else f"nota {f['nota']:.1f}: forma final {f['final']} fraca ou tipo repetido"
            )
            linhas.append(f"  {f['esp']} nv {f['nivel']} [{f['origem']}]: {motivo}")
    escolta = max(((f["esp"], f["nivel"]) for f in meus if f["origem"] == "time"), key=lambda e: e[1], default=None)
    treino = []
    for f in escolhidos:
        if f["origem"] in ("time", "pc") and f["nivel"] < alvo and alcancaveis:
            ops = onde_treinar(
                f["esp"],
                f["nivel"],
                alvo,
                escolta if escolta and escolta[0] != f["esp"] else None,
                alcancaveis,
                capacidades_,
            )
            if ops:
                treino.append(
                    f"  {f['esp']} nv {f['nivel']} -> {alvo}: "
                    + "; ".join(
                        f"{m} ({met} nv {a}-{b}, {modo}, ~{bt:.0f} batalhas)" for _, m, met, a, b, modo, bt in ops
                    )
                )
            else:
                treino.append(
                    f"  {f['esp']} nv {f['nivel']} -> {alvo}: nenhum lugar seguro alcançável agora; treine em "
                    "treinadores ou espere ter um Pokémon mais forte para escoltar"
                )
    if treino:
        linhas.append("Onde treinar (selvagens; treinadores dão 1,5x):")
        linhas += treino
    donos = {f["esp"] for f in meus}
    trocas = [o for o in obtencoes() if o["pede"]]
    if trocas:
        linhas.append(
            "Trocas com NPC (espécies que só vêm assim; guarde quem é pedido, nunca solte; obter_pokemon faz a "
            "troca com o pedido no time):"
        )
        linhas += [
            f"  {o['especie']} em {o['mapa']} pede {o['pede']}: "
            + ("você TEM" if o["pede"] in donos else "capture um antes")
            for o in trocas
        ]
    return "\n".join(linhas)


# ---------------- simulação de batalha contra treinador ----------------

INICIAIS = {"BULBASAUR": "CHARMANDER", "CHARMANDER": "SQUIRTLE", "SQUIRTLE": "BULBASAUR"}  # meu -> o do rival
FOLGA = 0.25  # vitória com menos HP que isso sobrando é arriscada (crítico, Growl/Tail Whip, poção do treinador)


def inicial_do_rival(especies_minhas):
    for esp in especies_minhas:
        raiz = _raiz().get(_especie_id(esp), "").removeprefix("SPECIES_")
        if raiz in INICIAIS:
            return INICIAIS[raiz]
    return None


def golpes_padrao(esp, nivel):
    """Os 4 últimos golpes aprendidos até o nível (o que o jogo dá a Pokémon de treinador sem golpes definidos)."""
    e = especies().get(_especie_id(esp))
    return list(dict.fromkeys(g for n, g in (e["golpes"] if e else []) if n <= nivel))[-4:]


def _dano_esperado(golpes_, atacante, nivel_a, alvo, nivel_d):
    """(dano médio por turno do melhor golpe, nome) considerando precisão; golpe sem PP não conta."""
    melhor = (0.0, None)
    for g in golpes_:
        pp = re.search(r"(\d+)\s*/\s*\d+\s*$", g)
        if pp and pp[1] == "0":
            continue
        nome = re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", g).strip()
        d = dano(nome, atacante, nivel_a, alvo, nivel_d)
        info = golpes().get(_golpe_por_nome().get(_chave(nome), ""))
        if d and info:
            media = (d[0] + d[1]) / 2 * ((info["precisao"] or 100) / 100)
            if media > melhor[0]:
                melhor = (media, nome)
    return melhor


def _duelo(meu, hp_meu, dele, hp_dele):
    """Luta até alguém cair. meu/dele = (espécie, nível, golpes). Devolve (venci, hp_meu_depois, hp_dele_depois, golpe)."""
    d_meu, golpe = _dano_esperado(meu[2], meu[0], meu[1], dele[0], dele[1])
    d_dele, _ = _dano_esperado(dele[2], dele[0], dele[1], meu[0], meu[1])

    def vel(p):
        return _atributo(especies()[_especie_id(p[0])]["base"]["Speed"], p[1])

    rapido = vel(meu) >= vel(dele)
    t_meu = math.ceil(hp_dele / d_meu) if d_meu else math.inf
    t_dele = math.ceil(hp_meu / d_dele) if d_dele else math.inf
    if t_meu < t_dele or (t_meu == t_dele and rapido):
        apanha = t_meu - 1 if rapido else t_meu
        return True, hp_meu - apanha * d_dele, 0, golpe
    bate = t_dele if rapido else t_dele - 1
    return False, 0, max(hp_dele - bate * d_meu, 0), golpe


def _hp_max(esp, nivel):
    return _atributo(especies()[_especie_id(esp)]["base"]["HP"], nivel, hp=True)


def simular_batalha(meus, adversario):
    """Simula a luta contra um treinador: meus = [{especie, nivel, hp (fração), golpes}] na ordem do time.

    A cada Pokémon dele, entra quem vence com mais HP sobrando (trocar custa um golpe dele de graça). Devolve
    (venceu, folga_minima, linhas). Aproximado: sem crítico, sem mudança de atributo, sem itens do treinador."""
    hp = {
        i: (p.get("hp") if p.get("hp") is not None else 1.0) * _hp_max(p["especie"], p["nivel"])
        for i, p in enumerate(meus)
    }
    eu = {
        i: (p["especie"], p["nivel"], p.get("golpes") or golpes_padrao(p["especie"], p["nivel"]))
        for i, p in enumerate(meus)
    }
    ativo, linhas, folga = 0, [], 1.0
    for esp, nivel, gs in adversario:
        dele = (esp, nivel, gs or golpes_padrao(esp, nivel))
        hp_dele = _hp_max(esp, nivel)
        while hp_dele > 0:
            vivos = [i for i in hp if hp[i] > 0]
            if not vivos:
                linhas.append(f"  {esp} {nivel} sobra com {hp_dele / _hp_max(esp, nivel):.0%} de HP: VOCÊ PERDE")
                return False, 0.0, linhas
            opcoes = []
            for i in vivos:
                custo = (
                    0
                    if i == ativo or hp.get(ativo, 0) <= 0
                    else _dano_esperado(dele[2], esp, nivel, eu[i][0], eu[i][1])[0]
                )
                if hp[i] - custo <= 0:
                    continue  # cairia só de entrar na troca
                venci, sobra, resto, golpe = _duelo(eu[i], hp[i] - custo, dele, hp_dele)
                opcoes.append((venci, sobra / _hp_max(eu[i][0], eu[i][1]), -resto, i, golpe or "-", custo))
            if not opcoes:  # só sobrou quem cairia na troca: o ativo luta
                opcoes = [(*_duelo(eu[ativo], hp[ativo], dele, hp_dele)[:1], 0, 0, ativo, "-", 0)]
            venci, sobra, resto, i, golpe, custo = max(opcoes)
            if venci and sobra > 0:
                folga = min(folga, sobra)
                linhas.append(
                    f"  {esp} {nivel}: {eu[i][0]} vence com {golpe}{' (entrando na troca)' if custo else ''} e "
                    f"fica com {sobra:.0%} de HP"
                )
                hp[i], hp_dele = sobra * _hp_max(eu[i][0], eu[i][1]), 0
            else:
                linhas.append(
                    f"  {esp} {nivel}: {eu[i][0]} cai depois de tirar {1 + resto / _hp_max(esp, nivel):.0%} dele"
                )
                hp[i], hp_dele = 0, -resto
            ativo = i
    return True, folga, linhas


def adversarios_do_marco(marco, especies_minhas):
    """Treinadores da luta obrigatória de um marco do roteiro (o rival muda conforme o inicial)."""
    rival = inicial_do_rival(especies_minhas) or "SQUIRTLE"
    ids = {
        "brock": ["TRAINER_LEADER_BROCK"],
        "misty": ["TRAINER_LEADER_MISTY"],
        "surge": ["TRAINER_LEADER_LT_SURGE"],
        "erika": ["TRAINER_LEADER_ERIKA"],
        "koga": ["TRAINER_LEADER_KOGA"],
        "sabrina": ["TRAINER_LEADER_SABRINA"],
        "blaine": ["TRAINER_LEADER_BLAINE"],
        "giovanni": ["TRAINER_LEADER_GIOVANNI"],
        "rival_cerulean": [f"TRAINER_RIVAL_CERULEAN_{rival}"],
        "ss_anne": [f"TRAINER_RIVAL_SS_ANNE_{rival}"],
        "torre": [f"TRAINER_RIVAL_POKEMON_TOWER_{rival}"],
        "silph": [f"TRAINER_RIVAL_SILPH_{rival}"],
        "rival_22": [f"TRAINER_RIVAL_ROUTE22_LATE_{rival}"],
        "liga": LIGA[:4] + [f"TRAINER_CHAMPION_FIRST_{rival}"],
    }
    return [t for t in ids.get(marco, []) if t in treinadores()]


def preparar_batalha(tid, time_, candidatos=()):
    """Texto: simulação contra o treinador, veredito e, se perder ou ficar no limite, o que resolve (nível que cada um
    precisaria para vencer sozinho o que o derruba, e capturáveis agora que vencem). candidatos = [(espécie, nível, onde)]."""
    t = treinadores()[tid]
    adv = [(e, n, g) for e, n, g in t["time"]]
    venceu, folga, linhas = simular_batalha(time_, adv)
    veredito = "VENCE com folga" if venceu and folga >= FOLGA else "VENCE NO LIMITE (arriscado)" if venceu else "PERDE"
    saida = [
        f"{t['classe']} {t['nome']} ({tid}): "
        + "; ".join(f"{e} {n} [{', '.join(g or golpes_padrao(e, n))}]" for e, n, g in adv),
        f"Simulação com o time atual: {veredito}",
    ] + linhas
    if venceu and folga >= FOLGA:
        return "\n".join(saida)
    saida.append(
        "O que resolve (cada adversário, de HP cheio contra um seu sozinho; nível projetado mantém os golpes "
        "atuais e soma os que aprende no caminho):"
    )
    for e, n, g in adv:
        dele = (e, n, g or golpes_padrao(e, n))
        quem = []
        for p in time_:
            atuais = p.get("golpes") or golpes_padrao(p["especie"], p["nivel"])
            aprende = especies().get(_especie_id(p["especie"]), {}).get("golpes", [])
            for nv in range(p["nivel"], p["nivel"] + 21):
                golpes_ = atuais + [m for lv, m in aprende if p["nivel"] < lv <= nv]
                venci, sobra, _, golpe = _duelo(
                    (p["especie"], nv, golpes_), _hp_max(p["especie"], nv), dele, _hp_max(e, n)
                )
                if venci and sobra / _hp_max(p["especie"], nv) >= FOLGA:
                    quem.append(f"{p['especie']} {'já vence' if nv == p['nivel'] else f'no nv {nv}'} ({golpe})")
                    break
        bons = []
        for esp, nv, onde in candidatos:
            venci, sobra, _, golpe = _duelo((esp, nv, golpes_padrao(esp, nv)), _hp_max(esp, nv), dele, _hp_max(e, n))
            if venci and sobra / _hp_max(esp, nv) >= FOLGA:
                bons.append(f"{esp} nv {nv} de {onde} ({golpe})")
        saida.append(
            f"  {e} {n}: "
            + ("; ".join(quem) or "nenhum seu até +20 níveis")
            + (f" | capturáveis que vencem: {'; '.join(bons[:4])}" if bons else "")
        )
    return "\n".join(saida)


def proxima_luta(marcos, especies_minhas):
    """(marco, [treinadores]) da primeira luta obrigatória do roteiro que já está liberada e não foi feita."""
    from fireredia.mundo import roteiro

    for id_, _, _, req, _ in roteiro.MARCOS:
        if id_ not in marcos and all(r in marcos for r in req):
            ids = adversarios_do_marco(id_, especies_minhas)
            if ids:
                return id_, ids
    return None, []


def candidatos_de_captura(alcancaveis, capacidades_, mochila, donos=()):
    """[(espécie, nível provável, onde)] capturáveis agora, para as simulações (nível do meio da faixa)."""
    return [
        (esp, max((a + b) // 2, 2), m)
        for esp, m, _, a, b, _ in _onde_capturar(alcancaveis or {}, capacidades_, mochila, donos).values()
    ]
