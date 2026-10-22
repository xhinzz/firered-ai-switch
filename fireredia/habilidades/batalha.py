"""Batalha: navega os menus conferindo a setinha na tela antes de confirmar (o jogo ignora toque enquanto a caixa abre)."""

import re
import time

import numpy as np

from fireredia.controle import maos
from fireredia.percepcao import olhos, texto

# caixas (y0, y1, x0, x1) da setinha em cada opção, na tela nativa 240x160
ACOES = {
    "FIGHT": (123, 135, 128, 136),
    "BAG": (123, 135, 183, 191),
    "POKEMON": (139, 151, 128, 136),
    "RUN": (139, 151, 183, 191),
}
GOLPES = {1: (123, 135, 7, 15), 2: (123, 135, 79, 87), 3: (139, 151, 7, 15), 4: (139, 151, 79, 87)}
SIM_NAO = {"sim": (74, 88, 190, 200), "nao": (91, 105, 190, 200)}
DECISAO = ("batalha_menu", "golpes", "sim_nao")


def _seta(n, caixas):
    # a setinha é um triângulo de ~16 px; o texto das opções é cinza claro e não passa no limiar
    escuro = {k: (n[y0:y1, x0:x1].max(axis=2) < 110).mean() for k, (y0, y1, x0, x1) in caixas.items()}
    k = max(escuro, key=escuro.get)
    return k if escuro[k] > 0.06 else None


def _ir_ate(estado, caixas, alvo):
    """Move a setinha até alvo e confirma com A. False se a tela saiu do estado esperado."""
    (ay, ax) = (caixas[alvo][0], caixas[alvo][2])
    for _ in range(8):
        n = olhos.tela()
        if olhos.classificar(n) != estado:
            return False
        atual = _seta(n, caixas)
        if atual == alvo:
            maos.apertar("A")
            for _ in range(10):
                time.sleep(0.15)
                n = olhos.tela()
                if olhos.classificar(n) != estado:
                    lido = texto.ler_caixa(n)
                    if re.search(r"is disabled|no PP left", lido):  # o jogo recusa e volta para a lista de golpes
                        recusa["texto"] = " ".join(lido.split())
                        maos.apertar("B")
                        time.sleep(0.6)
                        return False
                    return True
            continue  # A perdido: confere a setinha de novo e repete
        if atual:
            cy, cx = caixas[atual][0], caixas[atual][2]
            botoes = (["BAIXO"] if ay > cy else ["CIMA"] if ay < cy else []) + (
                ["DIREITA"] if ax > cx else ["ESQUERDA"] if ax < cx else []
            )
            maos.apertar(*botoes)
        time.sleep(0.35)  # a tela mostra o toque ~0,25 s depois; ler antes disso repete o toque
    return False


LOC = olhos.Localizador()  # compartilhado com quem navega, para reconhecer a volta ao mapa
ao_texto = None  # ao_texto(tela) a cada texto parado: quem guarda memória lê nível, golpe novo, evolução
recusa = {"texto": ""}  # por que o último golpe foi recusado (Disable, sem PP)


def avancar(prazo=45.0):
    """Passa o texto (B) até a batalha pedir decisão, voltar ao mapa ou parar numa tela desconhecida.

    Devolve batalha_menu | golpes | sim_nao | mapa | outro | parado (texto que não sai nem com B nem com A)."""
    fim = time.monotonic() + prazo
    desde = None  # quando começou a sequência de telas "outro" (transição, evolução, golpe novo)
    caixa, parada = None, None  # texto atual e desde quando está parado
    apertado, sem_efeito = None, 0  # texto em que o B foi apertado; B que não mudou nada (fim da troca só aceita A)
    primeiro_toque = 0.0  # quando o texto atual levou o primeiro toque: "Go! X!" fica parado na animação de entrada
    while time.monotonic() < fim:
        n = olhos.tela()
        estado = olhos.classificar(n)
        if estado in DECISAO:
            return estado
        if estado in ("batalha_texto", "dialogo"):
            desde = None
            atual = n[112:160].astype(np.int16)
            if caixa is None or np.abs(atual - caixa).mean() > 2:
                caixa, parada = atual, time.monotonic()
            elif (
                time.monotonic() - parada > 0.45
                and not texto.legivel(texto.ler_caixa(n))
                and LOC.localizar(n, global_=False)
            ):
                return "mapa"  # o classificador viu diálogo no piso claro do mapa: não há texto nenhum
            elif time.monotonic() - parada > 0.45:
                # B só com o texto parado: B apertado enquanto a pergunta imprime chega (~0,2 s depois)
                # justo quando a caixa Sim/Não abre e responde "Não" sozinho
                if ao_texto:
                    try:
                        ao_texto(n)
                    except Exception:  # ponytail: leitura de memória nunca pode travar a batalha
                        pass
                # evolução: B cancela (evolution_scene.c) e a animação deixa o texto parado ~10 s sem contar como travado.
                # A caixa é a da batalha, letra branca: texto.tem (letra escura) não via o "evolving"
                if "evolving" in texto.ler_caixa(n):
                    apertado, caixa = None, None
                    time.sleep(0.3)
                    continue
                sem_efeito = sem_efeito + 1 if apertado is not None and np.abs(atual - apertado).mean() <= 2 else 0
                if not sem_efeito:
                    primeiro_toque = time.monotonic()
                # por tempo e não por toques: a animação de entrada (com status) passa de 2 s com o texto parado
                if sem_efeito >= 4 and time.monotonic() - primeiro_toque > 8:
                    return "parado"  # nem B nem A mudam o texto: quem decide é quem lê a tela
                # texto que não sai com B (tela final da troca com NPC, trade_scene.c) sai com A
                maos.apertar("A" if time.monotonic() - primeiro_toque > 4 else "B")
                apertado, caixa = atual, None
            time.sleep(0.08)
            continue
        if estado == "outro":
            if LOC.localizar(n, global_=False):
                return "mapa"
            desde = desde or time.monotonic()
            if time.monotonic() - desde > 2.5:  # tela parada que não é mapa nem batalha: quem vê a tela decide
                return "mapa" if LOC.localizar(n) else "outro"
        time.sleep(0.2)
    return olhos.classificar(olhos.tela())


def lutar(golpe: int):
    """Usa o golpe (1 a 4, na ordem da tela) e avança até a próxima decisão. Devolve o estado final."""
    if olhos.classificar(olhos.tela()) == "batalha_menu" and not _ir_ate("batalha_menu", ACOES, "FIGHT"):
        return f"não consegui abrir FIGHT (tela: {olhos.classificar(olhos.tela())})"
    recusa["texto"] = ""
    if not _ir_ate("golpes", GOLPES, golpe):
        if recusa["texto"]:
            return f"golpe {golpe} indisponível: {recusa['texto']} — escolha outro golpe"
        return f"não consegui escolher o golpe {golpe} (tela: {olhos.classificar(olhos.tela())})"
    return avancar()


def ver_golpes():
    """Deixa a lista de golpes aberta para quem decide ler nomes, PP e tipo."""
    if olhos.classificar(olhos.tela()) == "golpes":
        return "lista de golpes aberta"
    return "lista de golpes aberta" if _ir_ate("batalha_menu", ACOES, "FIGHT") else "não consegui abrir FIGHT"


def fugir():
    if not _ir_ate("batalha_menu", ACOES, "RUN"):
        return f"não consegui escolher RUN (tela: {olhos.classificar(olhos.tela())})"
    return avancar()


def abrir(acao: str):
    """Abre BAG ou POKEMON no menu de ação; o resto da navegação fica com quem vê a tela."""
    return "aberto" if _ir_ate("batalha_menu", ACOES, acao) else f"não consegui abrir {acao}"


def _espera(condicao, prazo):
    """Lê a tela até condicao(tela) ser verdade ou o prazo acabar."""
    fim = time.monotonic() + prazo
    while time.monotonic() < fim:
        if condicao(olhos.tela()):
            return True
        time.sleep(0.15)
    return False


def capturar(posicao=1, ao_arremessar=None, bola=None, master=False):
    """Joga a bola da posição dada no bolso POKé BALLS e acompanha até o resultado.

    bola: nome pedido, conferido no "X is selected." antes de usar (a posição muda quando um tipo acaba); MASTER BALL
    só sai com master=True. ao_arremessar() é chamado quando a bola sai. Devolve capturou | escapou | texto de erro."""
    if abrir("BAG") != "aberto":
        return f"não consegui abrir a BAG (tela: {olhos.classificar(olhos.tela())})"
    olhos.assentar(0.8)
    maos.apertar("DIREITA", "DIREITA")  # bolsos não dão a volta: POKé BALLS é o último
    time.sleep(0.5)
    maos.apertar(*["CIMA"] * 8, *["BAIXO"] * (posicao - 1))
    time.sleep(0.3)
    # A na bola abre "X is selected." com USE/CANCEL; toque durante a animação da mochila se perde
    for _ in range(3):
        maos.apertar("A")
        if _espera(lambda n: texto.tem(n, "selected", (100, 160, 0, 240)), 1.5):
            break
    tela = olhos.classificar(olhos.tela())
    n = olhos.tela()
    if texto.tem(n, "selected", (100, 160, 0, 240)):
        errada = (not master and texto.tem(n, "MASTER", (100, 160, 0, 240))) or (
            bola and not texto.tem(n, bola.upper()[:3], (100, 160, 0, 240))
        )  # POK / GRE / ULT / MAS / SAF
        if errada:
            maos.apertar("B", "B")  # CANCEL e fecha a mochila
            return (
                f"na posição {posicao} do bolso não está a {bola or 'bola pedida'} (ou é a MASTER BALL, só para "
                "lendário): nada foi jogado; confira as posições com ver_mochila"
            )
        maos.apertar("A")  # USE é a primeira opção
        # a volta da mochila para a batalha tem transição; o texto "X used POKé BALL!" aparece em até ~2 s
        _espera(lambda n: olhos.classificar(n) in ("batalha_texto", "batalha_menu"), 3.0)
        tela = olhos.classificar(olhos.tela())
    # só conta arremesso com o texto do arremesso na tela; voltar direto ao menu é bola não usada
    if tela != "batalha_texto":
        if tela in ("outro", "dialogo"):
            maos.apertar("B", "B", "B")
        return f"a bola não saiu (tela: {tela}); nada foi descontado da mochila"
    if ao_arremessar:
        ao_arremessar()
    capturou = False
    for _ in range(6):
        estado = avancar(prazo=40)
        if estado == "sim_nao":
            # "Use next POKéMON?" (o seu desmaiou) também é Sim/Não: o NÃO foge da batalha e o lendário fica no mapa
            if texto.tem(olhos.tela(), "next", (100, 160, 0, 240)):
                return (
                    'não capturou: seu Pokémon desmaiou e o jogo pergunta "Use next POKéMON?" (responda SIM e troque)'
                )
            capturou = True  # "Give a nickname to the captured X?"
            responder(False)
            continue
        if estado == "outro":  # ficha nova da Pokédex
            capturou = True
            maos.apertar("B")
            time.sleep(0.6)
            continue
        if estado == "mapa":
            # captura sempre passa pela pergunta do apelido; sem ela, o inimigo caiu de queimadura/veneno no fim do turno
            return "capturou" if capturou else "não capturou: a batalha acabou sem captura (o inimigo desmaiou)"
        if estado in ("batalha_menu", "golpes"):
            return "escapou"
    return f"resultado incerto (tela: {olhos.classificar(olhos.tela())})"


def responder(sim: bool):
    """Responde a caixa Sim/Não conferindo a setinha."""
    x = olhos.borda_sim_nao(olhos.tela())
    # a caixa fica em x=185 na batalha e x≈161 no mapa; a setinha fica 5 a 13 px depois da borda
    caixas = {k: (y0, y1, x + 5, x + 13) for k, (y0, y1, _, _) in SIM_NAO.items()} if x else SIM_NAO
    if not _ir_ate("sim_nao", caixas, "sim" if sim else "nao"):
        return f"não consegui responder (tela: {olhos.classificar(olhos.tela())})"
    return avancar()
