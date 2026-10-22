"""Menus fora da batalha: START, time com golpes, mochila, salvar e curar no Centro Pokémon."""

import re
import time
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image

from fireredia import caminhos
from fireredia.controle import maos
from fireredia.habilidades import batalha
from fireredia.mundo import conhecimento, mapa
from fireredia.percepcao import olhos, texto

START = ["POKEDEX", "POKEMON", "BAG", "JOGADOR", "SAVE", "OPTION", "EXIT"]


def _diferenca(a, b):
    return np.abs(a.astype(np.int16) - b).mean()


def _linha_start(n):
    """Linha da setinha no menu START (0 = POKéDEX) ou None se o menu não está aberto."""
    escuro = [(n[11 + 15 * i : 18 + 15 * i, 177:182].max(axis=2) < 100).mean() for i in range(len(START))]
    i = int(np.argmax(escuro))
    return i if escuro[i] > 0.2 and olhos._branco(n[4:110, 186:236]) > 0.5 else None


def abrir_start(opcao):
    """Abre o menu START e escolhe a opção conferindo a setinha."""
    alvo = START.index(opcao)
    for _ in range(10):
        n = olhos.tela()
        atual = _linha_start(n)
        if atual is None:
            maos.apertar("START")
            time.sleep(0.5)
            continue
        if atual == alvo:
            maos.apertar("A")
            return True
        maos.apertar(*(["BAIXO"] * (alvo - atual) if alvo > atual else ["CIMA"] * (atual - alvo)))
        time.sleep(0.35)
    return False


def fechar_tudo(prazo=6.0):
    """Aperta B até voltar ao mapa (menus, mochila, resumo)."""
    fim = time.monotonic() + prazo
    while time.monotonic() < fim:
        n = olhos.tela()
        if (
            olhos.classificar(n) == "outro"
            and _linha_start(n) is None
            and batalha.LOC.localizar(n, global_=batalha.LOC.ultima is None)
        ):
            return True
        maos.apertar("B")
        time.sleep(0.6)
    return False


# posições da tela do time (0 = cartão grande à esquerda, 1-5 = lista à direita, 6 = CANCEL): (y0, y1, x0, x1)
SLOTS_TIME = [(20, 76, 2, 86)] + [(10 + 24 * i, 34 + 24 * i, 86, 240) for i in range(5)] + [(130, 156, 182, 240)]


def cursor_time(n):
    """Posição selecionada na tela do time pela borda laranja (255,115,49 no bg.pal; capturada ~250,118,45).

    O cartão do desmaiado é mostarda (213,164,32) e não pode passar: com ele no time o cursor parecia nunca sair dali."""
    laranja = [
        ((r := n[y0:y1, x0:x1].astype(int))[..., 0] > 225) & (r[..., 1] > 85) & (r[..., 1] < 145) & (r[..., 2] < 85)
        for y0, y1, x0, x1 in SLOTS_TIME
    ]
    contas = [int(m.sum()) for m in laranja]
    i = int(np.argmax(contas))
    return i if contas[i] > 150 else None


def posicao_na_tela(n, especie):
    """Posição (0-5) da espécie na tela do time pelo nome escrito: na batalha a ordem muda a cada troca."""
    nomes = conhecimento.nomes_na_tela(especie.upper())  # MR_MIME aparece como MR. MIME ou MIMIEN (troca)
    for i, regiao in enumerate(SLOTS_TIME[:6]):
        if any(texto.achar(n, nome, regiao, claro=True, fonte="pequena")[0] >= texto.ACHOU for nome in nomes):
            return i
    return None


def escolher_no_time(posicao):
    """Move o cursor da tela do time até a posição (0-5) conferindo a borda laranja e aperta A."""
    sem_cursor = 0
    for _ in range(12):
        atual = cursor_time(olhos.tela())
        if atual is None:
            sem_cursor += 1
            if sem_cursor % 3 == 0:  # cursor num desmaiado (borda de outra cor): sai dele
                maos.apertar("BAIXO")
            time.sleep(0.4)
            continue
        if atual == posicao:
            maos.apertar("A")
            time.sleep(0.6)
            return True
        maos.apertar("BAIXO" if posicao > atual else "CIMA")
        time.sleep(0.45)
    # ponytail: guarda o quadro para calibrar a cor da borda quando ela some (visto na batalha com o time desmaiado)
    Image.fromarray(olhos.tela()).save(caminhos.LOGS / "cursor_sumiu.png")
    return False


# golpes que aparecem no submenu do Pokémon fora da batalha (sFieldMoves): SUMMARY, estes, SWITCH, ITEM, CANCEL
GOLPES_CAMPO = {
    "FLASH",
    "CUT",
    "FLY",
    "STRENGTH",
    "SURF",
    "ROCK SMASH",
    "WATERFALL",
    "TELEPORT",
    "DIG",
    "MILK DRINK",
    "SOFTBOILED",
    "SWEET SCENT",
}


def _sem_pp(golpe):
    return re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", golpe).strip().upper()


def trocar_ordem(origem, destino, golpes_origem):
    """Fora da batalha: SWITCH na tela do time, levando o Pokémon da posição origem (0-5) para destino."""
    if origem == destino:
        return "já está nessa posição"
    if not abrir_start("POKEMON"):
        return "não consegui abrir o menu POKéMON"
    olhos.assentar(0.8)
    if not escolher_no_time(origem):
        fechar_tudo()
        return "não achei o cursor na tela do time"
    campo = sum(_sem_pp(g) in GOLPES_CAMPO for g in golpes_origem)
    maos.apertar(*["BAIXO"] * (1 + campo))
    time.sleep(0.3)
    maos.apertar("A")
    time.sleep(0.6)
    ok = escolher_no_time(destino)
    olhos.assentar(1.5, prazo=4.0)  # as duas linhas saem e voltam trocadas
    fechar_tudo()
    return f"posições {origem} e {destino} trocadas" if ok else "não consegui escolher o destino da troca"


def usar_golpe_campo(especie, golpe, golpes):
    """START > POKéMON > o Pokémon > golpe de campo (FLASH, ...). No submenu eles vêm logo depois de SUMMARY, na
    ordem em que o Pokémon os conhece."""
    campo = [_sem_pp(g) for g in golpes if _sem_pp(g) in GOLPES_CAMPO]
    if golpe not in campo:
        return f"{especie} não sabe {golpe}"
    if not abrir_start("POKEMON"):
        return "não consegui abrir o menu POKéMON"
    pos = posicao_na_tela(olhos.assentar(0.8), especie)
    if pos is None or not escolher_no_time(pos):
        fechar_tudo()
        return f"não achei {especie} na tela do time"
    olhos.assentar(0.4, prazo=2.0)
    maos.apertar(*["BAIXO"] * (1 + campo.index(golpe)))
    time.sleep(0.3)
    maos.apertar("A")
    olhos.assentar(1.5, prazo=6.0)  # menu fecha e a animação do golpe roda no mapa
    return f"{especie} usou {golpe}"


LETREIRO_VOO = (0, 34, 20, 140)  # nome do lugar sob o cursor no mapa do FLY (letra clara)


def voar(especie, golpes, celula, nome):
    """FLY até a cidade na célula (coluna, linha) do mapa de Kanto. O cursor para nas bordas (region_map.c): empurrado
    para o canto fica em (0, 0) e dali anda até a célula; confere o nome no letreiro antes de confirmar."""
    r = usar_golpe_campo(especie, "FLY", golpes)
    if "usou" not in r:
        return r
    olhos.assentar(1.0, prazo=4.0)
    maos.apertar(*["ESQUERDA"] * 22, *["CIMA"] * 15)
    maos.apertar(*["DIREITA"] * celula[0], *["BAIXO"] * celula[1])
    n = olhos.assentar(0.6, prazo=3.0)
    # toque perdido ou a mais na rolagem do cursor deixa a uma célula do alvo: testa as quatro vizinhas e volta
    for ida, volta in (
        (None, None),
        ("CIMA", "BAIXO"),
        ("BAIXO", "CIMA"),
        ("ESQUERDA", "DIREITA"),
        ("DIREITA", "ESQUERDA"),
    ):
        if ida:
            maos.apertar(ida)
            n = olhos.assentar(0.6, prazo=3.0)
        if texto.ler_mais_longo(n, [nome], LETREIRO_VOO, claro=True) == nome:
            break
        if volta:
            maos.apertar(volta)
    else:
        fechar_tudo()
        return f"o cursor do FLY não parou em {nome}"
    maos.apertar("A")
    olhos.assentar(3.0, prazo=10.0)  # animação do voo e o pouso
    return f"voou para {nome}"


def _empilhar(quadros):
    return np.vstack(quadros)


# página KNOWN MOVES do resumo (tela nativa): nível e nome no topo (letra branca), golpe i e o PP dele à direita
NIVEL_RESUMO, NOME_RESUMO = (18, 34, 0, 36), (18, 34, 36, 118)
# barra de HP (48 px) na tela do time: (y, x) do cartão grande e das 5 linhas da direita
BARRA_TIME = [(60, 32)] + [(19 + 24 * k, 184) for k in range(5)]


def _golpe_regiao(i):
    return (20 + 28 * i, 38 + 28 * i, 155, 240), (30 + 28 * i, 47 + 28 * i, 170, 240)


def _ler_pp(n, regiao, base):
    """PP 'atual/máximo'; o máximo é o do golpe ou o aumentado por PP UP (+20% cada)."""
    for maximo in (base, base * 6 // 5, base * 7 // 5, base * 8 // 5):
        nota, atual = max((texto.achar(n, f"{a}/{maximo}", regiao)[0], a) for a in range(maximo + 1))
        if nota >= texto.ACHOU:
            return atual, maximo
    return None


def _ler_resumo(n):
    """Espécie, nível e golpes ('NOME pp/máx') da página KNOWN MOVES do resumo."""
    nota, esp = texto.ler(n, _kanto(), NOME_RESUMO, claro=True)
    golpes = []
    for i in range(4):
        r_nome, r_pp = _golpe_regiao(i)
        nota_g, g = texto.ler(n, conhecimento.nomes_golpes(), r_nome)
        if nota_g < texto.ACHOU:
            continue
        pp = conhecimento.pp_de(g) and _ler_pp(n, r_pp, conhecimento.pp_de(g))
        golpes.append(f"{g} {pp[0]}/{pp[1]}" if pp else g)
    if nota < texto.ACHOU:  # apelido (Pokémon de troca: CH'DING, MIMIEN): a espécie sai pelo retrato
        esp, nota_retrato = olhos.identificar_no_resumo(n, _kanto())
        esp = esp if nota_retrato >= olhos.IDENTIFICOU else None
        nota = texto.ACHOU if esp else nota
    return {
        "especie": esp if nota >= texto.ACHOU else None,
        "nivel": texto.numero(n, NIVEL_RESUMO, claro=True),
        "golpes": golpes,
    }


def _hp_time(n, i):
    """Fração do HP da posição i na tela do time (os números usam outra fonte; a barra basta)."""
    y, x = BARRA_TIME[i]
    return olhos._barra(n[y, x : x + 48])


def ver_time():
    """Lê do jogo o time inteiro (espécie, nível, HP, golpes com PP) pela tela do time e a página de golpes do resumo.

    Devolve (lista de dicts, quadros) ou (texto de erro, None). Item com especie None não foi lido: confira no quadro."""
    if not abrir_start("POKEMON"):
        return "não consegui abrir o menu POKéMON", None
    time_ = olhos.assentar(1.0)
    tamanho = sum(_hp_time(time_, i) is not None for i in range(6))
    if not escolher_no_time(0):  # o cursor lembra a última posição; o resumo começa de quem está selecionado
        fechar_tudo()
        return "não achei o cursor na tela do time", None
    maos.apertar("A")  # SUMMARY é a primeira opção do submenu
    olhos.assentar(1.0)
    maos.apertar("DIREITA")
    time.sleep(0.5)
    maos.apertar("DIREITA")  # página KNOWN MOVES
    golpes = [olhos.assentar(0.6)]
    lidos = [_ler_resumo(golpes[0])]
    for _ in range(3 * tamanho):  # BAIXO passa ao próximo do time na mesma página
        if len(lidos) >= tamanho:
            break
        maos.apertar("BAIXO")
        time.sleep(0.3)
        n = olhos.assentar(0.6)
        p = _ler_resumo(n)
        # pela leitura e não pelos pixels: quadro do meio da animação também difere do anterior
        if p == lidos[-1]:  # toque perdido: aperta de novo
            continue
        if p == lidos[0]:  # deu a volta
            break
        golpes.append(n)
        lidos.append(p)
    fechar_tudo()
    for i, p in enumerate(lidos):
        hp = _hp_time(time_, i)
        p["hp"] = None if hp is None else round(hp, 2)
    return lidos, [time_] + golpes


def _paginas_do_bolso():
    """Fotografa o bolso atual do topo ao fim; se a lista passa de uma tela, rola e fotografa de novo."""
    # a mochila lembra a rolagem de cada bolso: começar do meio perdia os itens de cima, e a leitura completa os zerava
    topo = olhos.assentar(0.4)
    for _ in range(8):
        maos.apertar(*["CIMA"] * 6)
        n = olhos.assentar(0.4)
        if _diferenca(n[0:110, 95:160], topo[0:110, 95:160]) < 1.0:
            break
        topo = n
    paginas = [topo]
    for _ in range(7):  # bolso ITEMS do FRLG guarda até 42 itens
        maos.apertar(*["BAIXO"] * 6)
        n = olhos.assentar(0.4)
        # só o texto dos itens (x>=95): a setinha andando até CANCEL não é rolagem
        if _diferenca(n[0:110, 95:160], paginas[-1][0:110, 95:160]) < 1.0:
            break
        paginas.append(n)
    if len(paginas) > 1:
        maos.apertar(*["CIMA"] * (6 * len(paginas)))
    return paginas


@lru_cache
def _nomes_itens():
    return sorted({v[0] for v in conhecimento.itens().values() if v[0] and "?" not in v[0]})


def ler_bolsos(quadros):
    """{item: quantidade} das telas dos bolsos; quantidade na fonte pequena, item-chave sem número conta 1."""
    res = {}
    for n in quadros:
        for i in range(6):
            nome = texto.ler_mais_longo(n, _nomes_itens(), (11 + 16 * i, 29 + 16 * i, 95, 190))
            if nome:
                res[nome] = texto.numero(n, (11 + 16 * i, 29 + 16 * i, 186, 236), 999, fonte="pequena") or 1
    return res


def ver_mochila(na_batalha=False):
    """Fotografa os três bolsos (ITEMS, KEY ITEMS, POKé BALLS). Devolve (texto, imagem empilhada)."""
    if na_batalha:
        if batalha.abrir("BAG") != "aberto":
            return "não consegui abrir a BAG na batalha", None
    elif not abrir_start("BAG"):
        return "não consegui abrir a BAG", None
    olhos.assentar(1.0)
    maos.apertar("ESQUERDA", "ESQUERDA")  # os bolsos não dão a volta: duas vezes para a esquerda é sempre ITEMS
    quadros = []
    for i in range(3):
        if i:
            maos.apertar("DIREITA")
        quadros += _paginas_do_bolso()
    if na_batalha:
        maos.apertar("B")
        time.sleep(0.8)
    else:
        fechar_tudo()
    return (
        "bolsos ITEMS, KEY ITEMS e POKé BALLS, de cima para baixo (bolso com várias telas aparece em sequência)",
        _empilhar(quadros),
    )


BOLSOS = {"ITEMS": 0, "KEY_ITEMS": 1, "POKE_BALLS": 2}
LISTA_BOLSA = (4, 108, 95, 200)  # nomes dos itens; a linha i começa em y = 13 + 16i


def _linha_bolsa(n):
    escuro = [(n[17 + 16 * i - 5 : 17 + 16 * i + 5, 86:97].max(axis=2) < 110).mean() for i in range(6)]
    i = int(np.argmax(escuro))
    return i if escuro[i] > 0.08 else None  # medido: 0,16 na linha da setinha, 0 nas outras


def _apontar_item(nome, bolso):
    """Na mochila aberta: vai ao bolso, procura o item subindo e depois descendo a lista e aperta A nele."""
    maos.apertar("ESQUERDA", "ESQUERDA")  # os bolsos não dão a volta: duas vezes para a esquerda é sempre ITEMS
    if bolso:
        maos.apertar(*["DIREITA"] * bolso)
    direcao, anterior = "CIMA", None
    # só no começo da linha (x=97): solto, "POTION" casava dentro de "SUPER POTION"
    y0, y1, x0, _ = LISTA_BOLSA
    regiao = (y0, y1, x0, x0 + texto.desenhar(nome).shape[1] + 6)
    for _ in range(20):
        n = olhos.assentar(0.3, prazo=1.5)
        nota, _, y = texto.achar(n, nome, regiao)
        atual = _linha_bolsa(n)
        if nota >= texto.ACHOU and atual is not None:
            alvo = (y - 13 + 8) // 16
            if alvo == atual:
                maos.apertar("A")
                return True
            maos.apertar(*(["BAIXO"] * (alvo - atual) if alvo > atual else ["CIMA"] * (atual - alvo)))
            continue
        if anterior is not None and _diferenca(n[0:110, 95:200], anterior[0:110, 95:200]) < 1.0:
            if direcao == "BAIXO":
                return False  # percorreu a lista toda
            direcao = "BAIXO"  # chegou ao topo
        anterior = n
        maos.apertar(*[direcao] * 5)
    return False


def usar_item(nome, posicao=None):
    """START > BAG > item > USE; se o jogo pedir um Pokémon, escolhe a posição (0-5) no time.

    Devolve o estado final (mapa, sim_nao para golpe novo...) ou o texto do erro."""
    chave = conhecimento._chave(nome)
    info = next((v for v in conhecimento.itens().values() if conhecimento._chave(v[0]) == chave), None)
    if not info or info[2] not in BOLSOS:
        return f"item {nome} desconhecido ou fora dos bolsos ITEMS/KEY ITEMS/POKé BALLS (TM: use o TM CASE)"
    if not abrir_start("BAG"):
        return "não consegui abrir a BAG"
    olhos.assentar(1.0)
    if not _apontar_item(info[0], BOLSOS[info[2]]):
        fechar_tudo()
        return f"{info[0]} não está na mochila"
    time.sleep(0.6)
    maos.apertar("A")  # USE é a primeira opção do submenu
    n = olhos.assentar(0.8, prazo=4.0)
    if cursor_time(n) is not None:
        if posicao is None:
            fechar_tudo()
            return f"{info[0]} precisa de um Pokémon: passe a posição no time"
        escolher_no_time(posicao)
        if texto.tem(olhos.assentar(0.8, prazo=3.0), "effect", (100, 160, 0, 240)):  # "It won't have any effect."
            fechar_tudo()
            return "sem efeito (nada foi gasto)"
    r = batalha.avancar(prazo=25)
    if r == "sim_nao":
        return "pergunta na tela (golpe novo ou evolução?): decida"
    fechar_tudo()
    return f"{info[0]} usado"


def tirar_item(especie, golpes):
    """START > POKéMON > o Pokémon > ITEM > TAKE; carta (MAIL) vai para a caixa de cartas do PC. (tirou?, relato)."""
    if not abrir_start("POKEMON"):
        return False, "não consegui abrir o menu POKéMON"
    pos = posicao_na_tela(olhos.assentar(0.8), especie)
    if pos is None or not escolher_no_time(pos):
        fechar_tudo()
        return False, f"não achei {especie} na tela do time"
    olhos.assentar(0.4, prazo=2.0)
    campo = sum(_sem_pp(g) in GOLPES_CAMPO for g in golpes)
    maos.apertar(*["BAIXO"] * (2 + campo))  # SUMMARY, golpes de campo, SWITCH, ITEM
    time.sleep(0.3)
    maos.apertar("A")
    time.sleep(0.6)
    maos.apertar("BAIXO")  # GIVE / TAKE / CANCEL, ou READ / TAKE / CANCEL com carta (party_menu.h)
    time.sleep(0.3)
    maos.apertar("A")
    lido = texto.ler_caixa(olhos.assentar(0.8, prazo=3.0))
    if "MAIL" in lido:  # "Send the removed MAIL to your PC?"
        r = batalha.responder(True) if batalha.avancar(prazo=10) == "sim_nao" else "a pergunta da carta não apareceu"
        fechar_tudo()
        ok = not r.startswith(("não consegui", "a pergunta"))
        return ok, f"a carta de {especie} foi para o PC" if ok else r
    fechar_tudo()
    return "eceived" in lido, f"texto na tela: {lido!r}"  # a 1ª letra da caixa costuma sair "?"


def dar_item(nome, especie, trocar=False):
    """START > BAG > item > GIVE > o Pokémon do time. Se ele já segura algo, só troca com trocar=True.

    Devolve (deu?, relato)."""
    chave = conhecimento._chave(nome)
    info = next((v for v in conhecimento.itens().values() if conhecimento._chave(v[0]) == chave), None)
    if not info or info[2] != "ITEMS":
        return False, f"{nome}: só itens do bolso ITEMS podem ser dados para segurar"
    if not abrir_start("BAG"):
        return False, "não consegui abrir a BAG"
    olhos.assentar(1.0)
    if not _apontar_item(info[0], BOLSOS["ITEMS"]):
        fechar_tudo()
        return False, f"{info[0]} não está na mochila"
    time.sleep(0.6)
    maos.apertar("BAIXO")  # USE / GIVE / TOSS / CANCEL (item_menu.c, sContextMenuItems_Field)
    time.sleep(0.3)
    maos.apertar("A")
    n = olhos.assentar(0.8, prazo=4.0)
    pos = posicao_na_tela(n, especie)
    if cursor_time(n) is None or pos is None or not escolher_no_time(pos):
        fechar_tudo()
        return False, f"não achei {especie} na tela do time"
    n = olhos.assentar(0.8, prazo=3.0)
    if texto.tem(n, "already holding", CAIXA_DIALOGO):
        # responder já avança o "was taken and replaced with" que vem depois do YES
        r = batalha.responder(trocar) if batalha.avancar(prazo=10) == "sim_nao" else "a pergunta de troca não apareceu"
        fechar_tudo()
        if not trocar:
            return False, f"{especie} já segura outro item: nada mudou (trocar=true para trocar)"
        ok = not r.startswith(("não consegui", "a pergunta"))
        return ok, f"{especie} agora segura {info[0]}; o item antigo voltou à mochila" if ok else r
    lido = texto.ler_caixa(n)
    deu = "hold" in lido or "replaced" in lido  # "was given the X to hold" / "was taken and replaced with"
    fechar_tudo()
    return deu, f"texto na tela: {lido!r}"


CAIXA_DIALOGO = (100, 160, 0, 240)

# Poké Mart (tela nativa): menu BUY/SELL/SEE YA no canto, lista de compra à direita, quantidade "×NN" no meio
MENU_LOJA, LISTA_LOJA, QTD_LOJA = (0, 64, 0, 120), (8, 108, 92, 185), (80, 100, 132, 176)


def _seta_linha(n, x0, x1, linhas, limiar=0.08):
    """Linha (0..) da setinha num menu de linhas de 16 px a partir de y=17, ou None."""
    escuro = [(n[12 + 16 * i : 22 + 16 * i, x0:x1].max(axis=2) < 110).mean() for i in range(linhas)]
    i = int(np.argmax(escuro))
    return i if escuro[i] > limiar else None


def _ir_ao_balconista(nav, m):
    """Para de frente para o balcão da loja (a atendente fica do outro lado) e aperta A."""
    col, _, comp = mapa.grade(m)
    balcao = mapa.comportamentos()["MB_COUNTER"]
    for cx, cy, gfx, *_ in mapa.objetos(m):
        if "CLERK" not in gfx:
            continue
        for d, (dx, dy) in mapa.DIRECOES.items():
            if 0 <= cy + dy < comp.shape[0] and 0 <= cx + dx < comp.shape[1] and comp[cy + dy, cx + dx] == balcao:
                if nav.ir(("tile", m, cx + 2 * dx, cy + 2 * dy)).startswith("chegou"):
                    oposta = {"CIMA": "BAIXO", "BAIXO": "CIMA", "ESQUERDA": "DIREITA", "DIREITA": "ESQUERDA"}[d]
                    maos.apertar(oposta, segurar=0.03)  # o balcão não deixa andar: só vira
                    time.sleep(0.3)
                    maos.apertar("A")
                    return None
    return f"não cheguei ao balcão de {m}"


def _menu_loja(opcao):
    """Espera o menu BUY/SELL/SEE YA (0/1/2) e escolhe conferindo a setinha."""
    for _ in range(25):
        n = olhos.tela()
        if not (texto.tem(n, "SELL", MENU_LOJA) and texto.tem(n, "BUY", MENU_LOJA)):
            time.sleep(0.25)
            continue
        atual = _seta_linha(n, 12, 20, 3)
        if atual == opcao:
            maos.apertar("A")
            return True
        if atual is not None:
            maos.apertar(*(["BAIXO"] * (opcao - atual) if opcao > atual else ["CIMA"] * (atual - opcao)))
        time.sleep(0.35)
    return False


def _quantidade(qtd):
    """Na caixa ×01: CIMA soma 1, DIREITA soma 10; confere na tela e corrige toque perdido. O jogo para no que o
    dinheiro ou a mochila permitem: se o número não sobe, é o teto."""

    def ler():
        return texto.numero(olhos.assentar(0.3, prazo=1.5), QTD_LOJA, 99, fonte="pequena")

    atual = ler() or 1
    for _ in range(12):
        if atual == qtd:
            break
        falta = qtd - atual
        botao = ("DIREITA" if falta >= 10 else "CIMA") if falta > 0 else ("ESQUERDA" if falta <= -10 else "BAIXO")
        maos.apertar(botao)
        novo = ler()
        if novo is None or (novo <= atual and falta > 0):  # não subiu: teto do dinheiro ou da mochila
            if novo is not None and novo < atual:
                maos.apertar("BAIXO")  # no teto o CIMA dá a volta para 1; BAIXO no 1 volta ao teto
            break
        atual = novo
    return atual


def _apontar_na_loja(nome, nomes):
    """Na lista de compra: acha a linha do item (pelo nome mais longo de cada linha), leva a setinha e aperta A."""
    direcao, anterior = "CIMA", None
    for _ in range(20):
        n = olhos.assentar(0.3, prazo=1.5)
        linhas = [texto.ler_mais_longo(n, nomes, (11 + 16 * i, 29 + 16 * i, 92, 185)) for i in range(6)]
        atual = _seta_linha(n, 84, 94, 6, 0.1)
        if nome in linhas and atual is not None:
            alvo = linhas.index(nome)
            if alvo == atual:
                maos.apertar("A")
                return True
            maos.apertar(*(["BAIXO"] * (alvo - atual) if alvo > atual else ["CIMA"] * (atual - alvo)))
            continue
        if anterior is not None and _diferenca(n[0:110, 92:185], anterior[0:110, 92:185]) < 1.0:
            if direcao == "BAIXO":
                return False
            direcao = "BAIXO"
        anterior = n
        maos.apertar(*[direcao] * 5)
    return False


def _sair_da_loja():
    maos.apertar("B")  # fecha a lista ou a mochila
    _menu_loja(2)  # SEE YA!
    batalha.avancar(prazo=6)
    fechar_tudo()


def comprar(nav, pedidos):
    """Compra {item: quantidade} na loja do mapa atual. Devolve ({item: comprado}, relato)."""
    m = nav.loc.ultima and nav.loc.ultima.mapa
    estoque = [n for n, _ in conhecimento.lojas().get(m, [])]
    if not estoque:
        return {}, f"{m} não é uma loja (use a ferramenta loja para ver onde vende)"
    faltam = [i for i in pedidos if conhecimento._chave(i) not in {conhecimento._chave(e) for e in estoque}]
    if faltam:
        return {}, f"{m} não vende {', '.join(faltam)}; vende: {', '.join(estoque)}"
    erro = _ir_ao_balconista(nav, m)
    if erro or not _menu_loja(0):
        fechar_tudo()
        return {}, erro or "o menu da loja não abriu"
    comprados, relato = {}, []
    for pedido, qtd in pedidos.items():
        nome = next(e for e in estoque if conhecimento._chave(e) == conhecimento._chave(pedido))
        if not _apontar_na_loja(nome, estoque):
            relato.append(f"não achei {nome} na lista")
            continue
        if not batalha._espera(lambda n: texto.tem(n, "How many", CAIXA_DIALOGO), 4.0):
            relato.append(f"{nome}: a pergunta de quantidade não apareceu (sem dinheiro?)")
            batalha.avancar(prazo=4)
            continue
        qtd_real = _quantidade(qtd) or qtd
        maos.apertar("A")
        if batalha.avancar(prazo=8) == "sim_nao":  # "... That will be ₽X. Okay?"
            batalha.responder(True)
            comprados[nome] = qtd_real
            relato.append(
                f"comprou {qtd_real} {nome}" + (f" (pediu {qtd}: o dinheiro não deu)" if qtd_real < qtd else "")
            )
        batalha._espera(lambda n: _seta_linha(n, 84, 94, 6, 0.1) is not None, 6.0)
    _sair_da_loja()
    return comprados, "; ".join(relato) or "nada comprado"


def vender(nav, itens):
    """Vende {item: quantidade} na loja do mapa atual (metade do preço de compra). Devolve ({item: vendido}, relato)."""
    m = nav.loc.ultima and nav.loc.ultima.mapa
    if m not in conhecimento.lojas():
        return {}, f"{m} não é uma loja"
    erro = _ir_ao_balconista(nav, m)
    if erro or not _menu_loja(1):
        fechar_tudo()
        return {}, erro or "o menu da loja não abriu"
    vendidos, relato = {}, []
    for pedido, qtd in itens.items():
        chave = conhecimento._chave(pedido)
        info = next((v for v in conhecimento.itens().values() if conhecimento._chave(v[0]) == chave), None)
        if not info or info[2] not in BOLSOS:
            relato.append(f"{pedido}: item desconhecido ou que não se vende")
            continue
        olhos.assentar(0.8, prazo=3)
        if not _apontar_item(info[0], BOLSOS[info[2]]):
            relato.append(f"{info[0]} não está na mochila")
            continue
        if batalha._espera(lambda n: texto.tem(n, "How many", CAIXA_DIALOGO), 2.5):
            qtd = _quantidade(qtd) or qtd
            maos.apertar("A")
        else:
            qtd = 1  # item único: o jogo pula a quantidade
        if batalha.avancar(prazo=8) == "sim_nao":  # "I can pay ₽X. Would that be OK?"
            batalha.responder(True)
            vendidos[info[0]] = qtd
            relato.append(f"vendeu {qtd} {info[0]} por ₽{info[1] // 2 * qtd}")
    _sair_da_loja()
    return vendidos, "; ".join(relato) or "nada vendido"


def pescar(vara="OLD ROD"):
    """Usa a vara (de frente para a água) e puxa com A assim que aparece "Oh! A bite!".

    Devolve batalha | nada | o texto do erro."""
    if not abrir_start("BAG"):
        return "não consegui abrir a BAG"
    olhos.assentar(1.0)
    if not _apontar_item(vara, BOLSOS["KEY_ITEMS"]):
        fechar_tudo()
        return f"{vara} não está na mochila"
    time.sleep(0.6)
    maos.apertar("A")  # USE
    fim = time.monotonic() + 20
    while time.monotonic() < fim:
        n = olhos.tela()
        if texto.tem(n, "bite", CAIXA_DIALOGO):
            maos.apertar("A")  # a janela para puxar é curta: sem esperar o texto assentar
            return "batalha" if batalha.avancar(prazo=15).startswith("batalha") else "o Pokémon escapou"
        if texto.tem(n, "nibble", CAIXA_DIALOGO) or texto.tem(n, "got away", CAIXA_DIALOGO):
            batalha.avancar(prazo=5)
            return "nada"
        if texto.tem(n, "time to use", CAIXA_DIALOGO):
            batalha.avancar(prazo=5)
            return "aqui não dá para pescar: fique de frente para a água"
        time.sleep(0.03)
    fechar_tudo()
    return "não vi o resultado da pescaria"


def salvar():
    """START > SAVE > Yes (e Yes para sobrescrever)."""
    if not abrir_start("SAVE"):
        return "não consegui abrir SAVE"
    for _ in range(4):
        estado = batalha.avancar(prazo=15)
        if estado != "sim_nao":
            break
        batalha.responder(True)
    fechar_tudo()
    return "jogo salvo"


MODELOS = caminhos.MODELOS
# recortes de referência (tela nativa) que identificam cada tela do PC: (arquivo, y, x)
TELAS_PC = {
    "lista": ("pc_lista.png", 8, 14),
    "armazenamento": ("pc_armazenamento.png", 8, 14),
    "caixas": ("pc_caixas.png", 2, 10),
}
CAIXAS_PC = 14


@lru_cache
def _modelo(arquivo):
    return np.asarray(Image.open(MODELOS / arquivo).convert("RGB"))


def _tela_pc(n):
    """lista (qual PC acessar) | armazenamento (WITHDRAW/DEPOSIT/MOVE) | caixas | None"""
    for nome, (arquivo, y, x) in TELAS_PC.items():
        m = _modelo(arquivo)
        if cv2.matchTemplate(n[y : y + m.shape[0], x : x + m.shape[1]], m, cv2.TM_CCOEFF_NORMED)[0, 0] > 0.8:
            return nome
    return None


def _linha_menu_pc(n, linhas):
    """Linha da setinha nos menus do PC (16 px entre opções)."""
    escuro = [(n[12 + 16 * i : 22 + 16 * i, 7:14].max(axis=2) < 110).mean() for i in range(linhas)]
    i = int(np.argmax(escuro))
    return i if escuro[i] > 0.1 else None


def _tile_pc(m):
    _, _, comp = mapa.grade(m)
    ys, xs = np.nonzero(comp == mapa.comportamentos()["MB_PC"])
    return (int(xs[0]), int(ys[0])) if len(xs) else None


ARMAZENAMENTO = {"WITHDRAW": 0, "DEPOSIT": 1, "MOVE": 2}


def abrir_armazenamento(nav, opcao):
    """Vai ao PC do Centro, entra em SOMEONE'S PC e escolhe WITHDRAW/DEPOSIT/MOVE conferindo a setinha.

    Devolve None se abriu (a tela da opção está aparecendo) ou o texto do erro."""
    m = nav.loc.ultima and nav.loc.ultima.mapa
    pc = m and _tile_pc(m)
    if not pc:
        return f"não há PC em {m}: vá a um Centro Pokémon"
    r = nav.ir(("vizinho", m, *pc))
    if not r.startswith("chegou"):
        return f"não cheguei ao PC: {r}"
    maos.apertar("A")
    escolheu = False
    for _ in range(15):
        n = olhos.assentar(0.6, prazo=2.5)
        tela = _tela_pc(n)
        if escolheu and tela != "armazenamento":
            return None
        if tela in ("lista", "armazenamento"):
            alvo = 0 if tela == "lista" else ARMAZENAMENTO[opcao]  # SOMEONE'S PC é a primeira da lista
            atual = _linha_menu_pc(n, 4 if tela == "lista" else 5)
            if atual is not None and atual != alvo:
                maos.apertar(*(["BAIXO"] * (alvo - atual) if alvo > atual else ["CIMA"] * (atual - alvo)))
                time.sleep(0.4)
                continue
            escolheu = tela == "armazenamento"
        elif tela == "caixas":
            return None
        maos.apertar("A")  # textos "booted up the PC", "Accessed someone's PC"...
    fechar_tudo()
    return f"não consegui abrir {opcao} no PC"


# painel PKMN DATA (letra branca) das telas do PC e título da caixa ("BOX5"), na tela nativa
NOME_PAINEL, NIVEL_PAINEL, TITULO_CAIXA = (84, 106, 0, 80), (112, 132, 10, 70), (20, 38, 135, 190)


@lru_cache
def _kanto():
    return [conhecimento.numero_nacional()[i] for i in range(1, 152)]


@lru_cache
def _nomes_painel():
    """Nome escrito no painel -> espécie: MR. MIME e o apelido de troca MIMIEN -> MR_MIME."""
    # 1-251: os cães e Lugia/Ho-Oh também passam pelo PC
    # ponytail: de Hoenn só o Deoxys (evento da Birth Island); mapear os índices internos se precisar dos outros
    nomes = {nome: esp for esp in conhecimento.numero_nacional().values() for nome in conhecimento.nomes_na_tela(esp)}
    return nomes | {"DEOXYS": "DEOXYS"}


def _no_painel(n):
    """(espécie, nível) do Pokémon sob o cursor nas telas do PC, ou None se a casa está vazia."""
    nome = texto.ler_mais_longo(n, list(_nomes_painel()), NOME_PAINEL, claro=True)  # MEWTWO, não o prefixo MEW
    return (_nomes_painel()[nome], texto.numero(n, NIVEL_PAINEL, claro=True)) if nome else None


def _ocupadas(n):
    """Casas (0-29) com ícone. Ícone tem bem mais cores que o papel de parede (medido: 37-94 contra 8-19)."""
    contas = [
        len(
            np.unique(
                (n[46 + 24 * r - 10 : 46 + 24 * r + 10, 100 + 24 * c - 10 : 100 + 24 * c + 10] // 16).reshape(-1, 3),
                axis=0,
            )
        )
        for r in range(5)
        for c in range(6)
    ]
    # ponytail: limiar pela casa mais lisa; caixa sem nenhuma casa vazia (30/30) conta como cheia
    base = min(contas)
    return list(range(30)) if base > 25 else [i for i, k in enumerate(contas) if k > base + 15]


def _mover_na_caixa(de, para):
    (r0, c0), (r1, c1) = divmod(de, 6), divmod(para, 6)
    botoes = (["BAIXO"] * (r1 - r0) if r1 > r0 else ["CIMA"] * (r0 - r1)) + (
        ["DIREITA"] * (c1 - c0) if c1 > c0 else ["ESQUERDA"] * (c0 - c1)
    )
    if botoes:
        maos.apertar(*botoes)


def _percorrer_caixas(ao_ver):
    """Na grade das caixas: passa pelas 14 e chama ao_ver(caixa, casa, especie, nivel) em cada Pokémon.

    ao_ver devolve True para parar. START põe o cursor no título; do título, BAIXO cai na casa 2 (pokemon_storage_system)."""
    maos.apertar("START")
    for _ in range(CAIXAS_PC):
        n = olhos.assentar(0.5, prazo=2.0)
        caixa, pos = texto.numero(n, TITULO_CAIXA, CAIXAS_PC, claro=True), None
        for casa in _ocupadas(n):
            if pos is None:
                maos.apertar("BAIXO")
                pos = 2
            _mover_na_caixa(pos, casa)
            pos = casa
            p = _no_painel(olhos.assentar(0.3, prazo=1.5))
            if p and ao_ver(caixa, casa, *p):
                return True
        if pos is not None:
            maos.apertar("START")
        _andar_caixas(1)  # a seta solta perdia toque na rolagem e pulava caixas
    return False


def ver_pc(nav):
    """Abre o PC (MOVE POKéMON, que funciona com o time cheio) e lê espécie e nível de tudo nas 14 caixas.

    Devolve (texto, [{"especie", "nivel", "caixa"}]) ou (erro, None)."""
    erro = abrir_armazenamento(nav, "MOVE")
    if erro:
        return erro, None
    olhos.assentar(1.0)
    achados = []
    _percorrer_caixas(lambda caixa, casa, esp, nv: achados.append({"especie": esp, "nivel": nv, "caixa": caixa}))
    _voltar_caixa1()
    fechar_tudo(prazo=10)
    return (
        f"PC: {len(achados)} Pokémon: "
        + ", ".join(f"{p['especie']} nv{p['nivel']} (caixa {p['caixa']})" for p in achados)
        if achados
        else "PC sem Pokémon"
    ), achados


def depositar(nav, especies):
    """Guarda no PC as espécies pedidas (uma de cada por nome). Devolve (guardados [(especie, nivel)], relato)."""
    erro = abrir_armazenamento(nav, "DEPOSIT")
    if erro:
        return [], erro
    olhos.assentar(1.0)
    pendentes, guardados, relato = [e.upper() for e in especies], [], []
    for _ in range(7 * (len(pendentes) + 1)):  # BAIXO percorre as 6 posições e CANCEL, dando a volta
        if not pendentes:
            break
        p = _no_painel(olhos.assentar(0.3, prazo=1.5))
        if not p or p[0] not in pendentes:
            maos.apertar("BAIXO")
            continue
        maos.apertar("A")  # menu STORE / SUMMARY / MARK / RELEASE: STORE é o primeiro
        time.sleep(0.6)
        maos.apertar("A")
        n = olhos.assentar(0.6, prazo=2.5)
        if not texto.tem(n, "Deposit in which", (128, 160, 0, 240)):
            motivo = (
                "segura uma carta (MAIL): o jogo não guarda"
                if texto.tem(n, "MAIL", (128, 160, 0, 240))
                else "último Pokémon do time?"
            )
            relato.append(f"{p[0]} não pôde ser guardado ({motivo})")
            maos.apertar("B", "B")
            pendentes.remove(p[0])
            continue
        maos.apertar("A")  # caixa atual
        n = olhos.assentar(1.0, prazo=4.0)
        if texto.tem(n, "full", (128, 160, 0, 240)):
            relato.append(f"caixa cheia: {p[0]} ficou no time")
            maos.apertar("B", "B")
            break
        pendentes.remove(p[0])
        guardados.append(p)
    fechar_tudo(prazo=10)
    relato += [f"não achei {e} no time" for e in pendentes]
    return guardados, "; ".join([f"guardou {', '.join(f'{e} nv{nv}' for e, nv in guardados) or 'nada'}"] + relato)


def retirar(nav, especies):
    """Tira do PC as espécies pedidas (o primeiro de cada que achar). Devolve (retirados [(especie, nivel)], relato)."""
    erro = abrir_armazenamento(nav, "WITHDRAW")
    if erro:
        return [], erro
    olhos.assentar(1.0)
    pendentes, retirados, relato = [e.upper() for e in especies], [], []

    def ao_ver(caixa, casa, esp, nv):
        if esp not in pendentes:
            return False
        maos.apertar("A")  # menu WITHDRAW / SUMMARY / MARK / RELEASE: WITHDRAW é o primeiro
        time.sleep(0.6)
        maos.apertar("A")
        n = olhos.assentar(1.0, prazo=4.0)
        if _no_painel(n):  # a casa continua ocupada: time cheio
            relato.append(f"time cheio: {esp} ficou no PC")
            maos.apertar("B", "B")
            return True
        pendentes.remove(esp)
        retirados.append((esp, nv))
        return not pendentes

    _percorrer_caixas(ao_ver)
    _voltar_caixa1()  # a caixa aberta ao sair vira a das capturas
    fechar_tudo(prazo=10)
    relato += [f"não achei {e} no PC" for e in pendentes]
    return retirados, "; ".join([f"tirou {', '.join(f'{e} nv{nv}' for e, nv in retirados) or 'nada'}"] + relato)


# ACE "Make any Pokémon shiny" digitado nos nomes das caixas 1-11: age na Caixa 10, casa 2, e dispara quando o Weedle
# (Caixa 1, casa 3) é trocado duas vezes, na mão laranja, com a espécie glitch 0x0351 (Caixa 3, casa 1)
TITULO_ACE = (20, 38, 120, 200)
NOME_CAIXA = {1: "C.kn5 9n", 10: "FoTB9Ma"}
ESTRELA = (35, 46, 100, 112)  # estrela de shiny do resumo (sprite em 106,40)
DISPARO = [
    ("BAIXO", 0.8),
    ("SELECT", 0.8),
    ("A", 1.2),
    ("CIMA", 0.8),
    ("DIREITA", 1.4),
    ("DIREITA", 1.4),
    ("BAIXO", 0.8),
    ("ESQUERDA", 0.6),
    ("ESQUERDA", 0.8),
    ("A", 2.0),
    ("A", 3.5),
    ("CIMA", 0.8),
    ("ESQUERDA", 1.4),
    ("ESQUERDA", 1.4),
    ("BAIXO", 0.8),
    ("A", 1.2),
    ("SELECT", 0.6),
    ("START", 0.8),
]


def _ap(*passos):
    for botao, espera in passos:
        maos.apertar(botao)
        time.sleep(espera)


def _na_caixa(k, n=None):
    n = olhos.assentar(0.5, prazo=2.0) if n is None else n
    # papel de parede claro (céu da Caixa 10) suja a máscara da letra branca: medido 0,84 no certo, até 0,34 nos outros
    return texto.achar(n, NOME_CAIXA[k], TITULO_ACE, claro=True)[0] >= 0.7


def _andar_caixas(passos):
    """No título: troca de caixa uma a uma (positivo = DIREITA) e devolve a tela assentada.

    A seta apertada durante a rolagem se perde: repete até o título mudar (caixas vizinhas nunca têm o mesmo papel de
    parede)."""
    y0, y1, x0, x1 = TITULO_ACE
    n = olhos.assentar(0.3, prazo=2.0)
    for _ in range(abs(passos)):
        for _ in range(3):
            _ap(("DIREITA" if passos > 0 else "ESQUERDA", 1.0))
            novo = olhos.assentar(0.3, prazo=2.0)
            if np.abs(novo[y0:y1, x0:x1].astype(np.int16) - n[y0:y1, x0:x1]).mean() > 6:
                break
        n = novo
    return n


def _voltar_caixa1():
    """A caixa aberta ao sair do PC vira a das capturas: sai sempre da Caixa 1."""
    _ap(("START", 0.6))
    n = olhos.assentar(0.5, prazo=2.0)
    for _ in range(CAIXAS_PC):
        if _na_caixa(1, n):
            return True
        n = _andar_caixas(1)
    return False


def _tem_estrela(n):
    y0, y1, x0, x1 = ESTRELA
    r = n[y0:y1, x0:x1].astype(int)
    return (
        int(((r[..., 0] > 200) & (r[..., 1] > 150) & (r[..., 2] < 150)).sum()) >= 6
    )  # amarelo; o fundo é branco (B > 220)


def _levar_ao_alvo(especie):
    """Tela das caixas recém-aberta: confere as caixas do ACE e leva o Pokémon do time à Caixa 10, casa 2.

    Devolve None ou o erro; nos dois casos o cursor fica no título de alguma caixa."""
    if not _voltar_caixa1():
        return "os nomes das caixas não são os do código de shiny"
    if _ocupadas(_andar_caixas(-1)):
        return "a Caixa 14 precisa estar vazia para o ACE"
    if any(i >= 6 for i in _ocupadas(_andar_caixas(-1))):
        return "a Caixa 13 tem algo da casa 7 em diante (bad egg?): o ACE travaria"
    n = _andar_caixas(-3)
    if not _na_caixa(10, n) or 1 in _ocupadas(n):
        return "a Caixa 10, casa 2, precisa estar vazia"
    _ap(("CIMA", 0.6), ("A", 0.4))  # do título, CIMA vai ao botão PARTY POKéMON
    for _ in range(7):
        p = _no_painel(olhos.assentar(0.6, prazo=2.0))
        if p and p[0] == especie:
            break
        _ap(("BAIXO", 0.2))
    else:
        _ap(("B", 1.2))
        return f"{especie} não está no time"
    # MOVE (1ª opção) pega; B esconde o time com o Pokémon na mão; START > BAIXO > ESQUERDA = título > casa 3 > casa 2
    _ap(("A", 0.6), ("A", 1.0), ("B", 1.2), ("START", 0.6), ("BAIXO", 0.5), ("ESQUERDA", 0.6), ("A", 0.6), ("A", 0.4))
    p = _no_painel(olhos.assentar(1.0, prazo=2.5))
    if not p or p[0] != especie:
        return f"não consegui pôr {especie} na Caixa 10, casa 2 (ficou na mão? confira a tela)"
    return None


def _conferir_e_retirar(especie):
    """Título da Caixa 10: lê a estrela no resumo da casa 2 e retira o Pokémon para o time. (shiny, voltou) ou erro."""
    _ap(("BAIXO", 0.4), ("ESQUERDA", 0.4))
    if (_no_painel(olhos.assentar(0.6, prazo=2.0)) or ("",))[0] != especie:
        return f"{especie} não está na Caixa 10, casa 2, depois do disparo"
    _ap(("A", 0.6), ("BAIXO", 0.3), ("A", 0.4))  # MOVE / SUMMARY / WITHDRAW / MARK / RELEASE
    shiny = _tem_estrela(olhos.assentar(1.5, prazo=3.0))
    _ap(("B", 0.4))
    olhos.assentar(1.5, prazo=3.0)
    _ap(("A", 0.6), ("BAIXO", 0.3), ("BAIXO", 0.3), ("A", 0.4))  # WITHDRAW: volta ao time
    return shiny, _no_painel(olhos.assentar(1.5, prazo=3.0)) is None


def tornar_shiny(nav, especie):
    """Pokémon do time fica shiny pelo ACE: vai à Caixa 10 casa 2, salva, dispara, confere a estrela no resumo e volta
    ao time (no fim da lista). Devolve o relato."""
    especie = especie.strip().upper()
    erro = abrir_armazenamento(nav, "MOVE")
    if erro:
        return erro
    olhos.assentar(1.0)
    erro = _levar_ao_alvo(especie)
    _voltar_caixa1()
    fechar_tudo(prazo=10)
    if erro:
        return erro
    salvar()  # se o disparo travar o jogo, o Pokémon já está guardado na Caixa 10
    erro = abrir_armazenamento(nav, "MOVE")
    if erro:
        return f"{especie} ficou na Caixa 10, casa 2: {erro}"
    olhos.assentar(1.0)
    _ap(("START", 0.6))
    if not _na_caixa(1):
        _voltar_caixa1()
        fechar_tudo(prazo=10)
        return f"{especie} ficou na Caixa 10, casa 2: o PC não abriu na Caixa 1"
    _ap(DISPARO[0])
    if (_no_painel(olhos.assentar(0.6, prazo=2.0)) or ("",))[0] != "WEEDLE":  # toque perdido pegava outro Pokémon
        _voltar_caixa1()
        fechar_tudo(prazo=10)
        return f"{especie} ficou na Caixa 10, casa 2: o cursor não parou no WEEDLE (Caixa 1, casa 3); tente de novo"
    _ap(*DISPARO[1:])
    n = olhos.assentar(1.0, prazo=3.0)
    if not _na_caixa(1, n) or 2 not in _ocupadas(n):
        return "o disparo não terminou como esperado (Weedle fora da Caixa 1?): confira a tela antes de salvar"
    if not _na_caixa(10, _andar_caixas(9)):
        return "não cheguei à Caixa 10 depois do disparo"
    r = _conferir_e_retirar(especie)
    _voltar_caixa1()
    fechar_tudo(prazo=10)
    if isinstance(r, str):
        return r
    shiny, volta = r
    if not volta:
        return f"{especie} {'ficou' if shiny else 'NÃO ficou'} shiny mas continua na Caixa 10, casa 2 (time cheio?)"
    if not shiny:
        return f"{especie} voltou ao time SEM a estrela de shiny: o código não fez efeito; não salvei"
    salvar()
    return f"{especie} agora é SHINY (estrela no resumo) e voltou ao time, no fim da lista; jogo salvo"


KANTO = 151
LINHA_CURSOR = 5  # depois de DIREITA (desce 9) a lista rola e deixa o cursor na 6ª linha


def _linhas_pokedex(n):
    """Por linha visível (9): (tem_bola, tem_nome, tem_setinha). Bola vermelha = capturado; nome sem bola = visto."""
    res = []
    for i in range(9):
        c = 25 + 14 * i
        reg = n[c - 6 : c + 6].astype(int)
        bola = (
            (reg[:, 55:69, 0] > 180) & (reg[:, 55:69, 1] < 90) & (reg[:, 55:69, 2] < 90)
        ).sum() > 20  # medido: 46 ou 0
        nome = (reg[:, 72:136].max(axis=2) < 120).sum() > 60  # nome >100, "-----" 25
        seta = (reg[:, 18:28].max(axis=2) < 120).sum() > 12
        res.append((bola, nome, seta))
    return res


def ver_pokedex():
    """Lê a Pokédex em modo numérico: devolve (capturados, vistos) como listas de números, ou texto de erro."""
    if not abrir_start("POKEDEX"):
        return "não consegui abrir a POKéDEX"
    olhos.assentar(1.0)
    maos.apertar("A")  # NUMERICAL MODE é a primeira opção do índice
    olhos.assentar(1.0)
    maos.apertar(*["ESQUERDA"] * 20)  # ESQUERDA sobe 9 por toque e a lista não dá a volta: garante o topo
    capturados, vistos = set(), set()
    num, anterior = 1, None
    for _ in range(KANTO // 9 + 3):
        n = olhos.assentar(0.4, prazo=2.0)
        if anterior is not None and _diferenca(n, anterior) < 1.0:
            break  # DIREITA não andou: fim da lista
        linhas = _linhas_pokedex(n)
        cursor = next((i for i, (_, _, s) in enumerate(linhas) if s), None)
        if cursor is None:
            fechar_tudo()
            return "não achei a setinha na lista da POKéDEX"
        if anterior is not None and cursor != LINHA_CURSOR:
            # ponytail: no fim da lista a DIREITA anda menos de 9 e para no último (151 antes da Pokédex nacional)
            num = KANTO
        for i, (bola, nome, _) in enumerate(linhas):
            numero = num + i - cursor
            if 1 <= numero <= KANTO:
                if bola:
                    capturados.add(numero)
                if bola or nome:
                    vistos.add(numero)
        anterior = n
        maos.apertar("DIREITA")
        num += 9
    fechar_tudo()
    return sorted(capturados), sorted(vistos)


def centros_pokemon():
    return [m for m in mapa.mapas() if m.endswith("POKEMON_CENTER_1F")]


def curar(nav):
    """Vai ao Centro Pokémon mais próximo, fala com a atendente pelo balcão e aceita a cura."""
    centros = set(centros_pokemon())
    # a pé primeiro: com FLY, "algum Centro" vira qualquer cidade (voava a Cinnabar no meio do treino da Victory Road)
    r = nav.ir(("algum", centros), voar=False)
    if r.startswith("sem caminho"):
        r = nav.ir(("algum", centros))
    if not r.startswith("chegou"):
        return f"não cheguei a um Centro Pokémon: {r}"
    centro = nav.loc.ultima.mapa
    enfermeira = next(((x, y) for x, y, gfx, *_ in mapa.objetos(centro) if gfx == "NURSE"), None)
    if not enfermeira:
        return f"não achei a atendente em {centro}"
    balcao = (enfermeira[0], enfermeira[1] + 1)
    r = nav.ir(("vizinho", centro, *balcao))
    if not r.startswith("chegou"):
        return f"não cheguei ao balcão: {r}"
    maos.apertar("A")
    for _ in range(4):
        estado = batalha.avancar(prazo=20)
        if estado != "sim_nao":
            break
        batalha.responder(True)
    return f"time curado em {centro}"
