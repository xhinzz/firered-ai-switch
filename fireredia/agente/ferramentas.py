"""Ferramentas do cérebro: o modelo decide, o código executa rápido e devolve a tela; cada ação alimenta a memória."""

import asyncio
import base64
import collections
import difflib
import io
import re
import time

import numpy as np
from claude_agent_sdk import create_sdk_mcp_server, tool
from PIL import Image

from fireredia import contexto
from fireredia.controle import maos
from fireredia.habilidades import batalha, coleta, combate, menus, navegacao, piloto
from fireredia.mundo import conhecimento, mapa, roteiro
from fireredia.percepcao import olhos, texto

SERVIDOR = "jogo"
MAX_BOTOES = 12
TIPOS_EVENTO = ["batalha", "historia", "compra", "presente", "evolucao", "treino", "troca_pc", "derrota", "outro"]


def _imagem(n):
    """(base64, mime). Uma tela: PNG 2x (fonte do GBA ainda legível; 3x custava o dobro de tokens). Pilha de telas (time, mochila): grade de 2 colunas
    em 2x e JPEG — em PNG uma pilha de 7 telas passou de 1 MB e derrubou a mensagem do SDK."""
    buf = io.BytesIO()
    if n.shape[0] <= 160:
        Image.fromarray(n).resize((480, 320), Image.NEAREST).save(buf, "PNG")
        return base64.b64encode(buf.getvalue()).decode("ascii"), "image/png"
    telas = [n[i : i + 160] for i in range(0, n.shape[0], 160)]
    linhas = (len(telas) + 1) // 2
    grade = Image.new("RGB", (480, 160 * linhas), (0, 0, 0))
    for i, t in enumerate(telas):
        grade.paste(Image.fromarray(t), ((i % 2) * 240, (i // 2) * 160))
    grade.resize((960, 320 * linhas), Image.NEAREST).save(buf, "JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode("ascii"), "image/jpeg"


def _ok(texto, n=None):
    conteudo = [{"type": "text", "text": texto}]
    if n is not None:
        dados, mime = _imagem(n)
        conteudo.append({"type": "image", "data": dados, "mimeType": mime})
    return {"content": conteudo}


def _erro(texto):
    return {"content": [{"type": "text", "text": texto}], "is_error": True}


def _esquema(props, obrigatorios):
    return {"type": "object", "properties": props, "required": obrigatorios, "additionalProperties": False}


def _mapa_valido(nome):
    nome = nome.strip().upper()
    if not nome.startswith("MAP_"):
        nome = "MAP_" + nome
    if nome in mapa.mapas():
        return nome, None
    parecidos = difflib.get_close_matches(nome, list(mapa.mapas()), n=5, cutoff=0.6)
    return None, f"mapa {nome} não existe. Parecidos: {', '.join(parecidos) or 'nenhum'}"


POKEMON = {
    "type": "object",
    "properties": {
        "especie": {"type": "string"},
        "apelido": {"type": "string"},
        "nivel": {"type": "integer"},
        "hp": {"type": "integer"},
        "hp_max": {"type": "integer"},
        "status": {"type": "string"},
        "golpes": {"type": "array", "items": {"type": "string", "description": "nome PP atual/máx, ex.: EMBER 9/25"}},
    },
    "required": ["especie", "nivel"],
    "additionalProperties": False,
}


def criar(estado, loc: olhos.Localizador):
    if (local := estado.dados.get("local")) and loc.ultima is None:
        # contexto ao reiniciar: dentro de um Centro Pokémon todos os mapas empatam e só a última posição desempata
        loc.ultima = olhos.Posicao(local["mapa"], local["x"], local["y"], 1.0, True)
    nav = contexto.montar_navegador(estado, loc)  # caminhada resolve selvagens, acende FLASH e voa sozinha
    batalha.ao_texto = lambda n: piloto.ler_mensagem(estado, n)  # nível, golpe aprendido e evolução pelo texto
    vez = asyncio.Lock()  # o modelo às vezes pede duas ações juntas; em paralelo os botões se misturariam

    def situacao():
        """Tela atual e texto curto com o tipo de tela e a posição; registra troca de mapa no histórico."""
        n = olhos.tela()
        tipo = olhos.classificar(n)
        if tipo == "dialogo" and not texto.legivel(texto.ler_caixa(n)):
            tipo = "outro"  # chão claro de cidade na faixa da caixa de texto: sem letra não é diálogo
        resumo = f"tela: {tipo}"
        if tipo == "outro":
            p = loc.localizar(n, global_=loc.ultima is None)
            if p:
                resumo = f"tela: mapa; você está em {p.mapa} ({p.x},{p.y})"
                antes = (estado.dados.get("local") or {}).get("mapa")
                campos = {"local": {"mapa": p.mapa, "x": p.x, "y": p.y}}
                if p.mapa not in estado.dados["visitados"]:  # cidades visitadas são os destinos do Fly
                    campos["visitados"] = estado.dados["visitados"] + [p.mapa]
                estado.atualizar(evento=("mapa", f"{antes} -> {p.mapa}") if antes != p.mapa else None, **campos)
        return resumo, n

    def _portoes():
        return roteiro.portoes(frozenset(estado.dados["marcos"]), frozenset(estado.dados["insignias"]))

    vistos = collections.deque(maxlen=8)  # (texto, posição, miniatura) depois de cada ação: detecta situação parada
    ultimo_dialogo = {"texto": ""}

    # só leem ou voltam à mesma tela de propósito: não contam como ação sem efeito no detector de situação parada
    LEITURAS = {
        "ver_tela",
        "ver_time",
        "ver_mochila",
        "ver_pc",
        "ver_pokedex",
        "ver_golpes",
        "salvar",
        "guardar_no_pc",
        "tirar_do_pc",
        "tornar_shiny",
        "mudar_ordem",
        "usar_item",
        "dar_item",
        "tirar_item",
    }

    def entender(n, texto_sit, nome=""):
        """Texto legível na tela e alerta se nada muda há algumas ações (o modelo precisa parar e pensar)."""
        lido = texto.ler_caixa(n)
        piloto.ler_mensagem(estado, n)  # memória pelo texto também fora do piloto (abertura de luta, nível, desmaio)
        if lido and lido != ultimo_dialogo["texto"]:
            estado.evento("dialogo", lido.replace("\n", " ")[:200])
        ultimo_dialogo["texto"] = lido
        pos = (loc.ultima.mapa, loc.ultima.x, loc.ultima.y) if "você está em" in texto_sit and loc.ultima else None
        mini = n[::8, ::8].astype(np.int16)
        parado = 0
        if nome and nome.split()[0] in LEITURAS:
            return f'texto na tela: "{" / ".join(lido.splitlines())}"' if lido else ""
        for t, p, m in reversed(vistos):
            if t != lido or p != pos or np.abs(m - mini).mean() > 3:
                break
            parado += 1
        vistos.append((lido, pos, mini))
        partes = [
            f'texto na tela: "{" / ".join(lido.splitlines())}"'
            if lido
            else ("sem texto legível na caixa (a tela pode não ser um diálogo)" if "dialogo" in texto_sit else "")
        ]
        if parado >= 2:
            partes.append(
                f"ATENÇÃO: nada mudou nas últimas {parado + 1} ações (mesma tela, mesmo texto, mesma posição). "
                "O que está sendo feito não funciona: leia o texto e a imagem, pense no que está bloqueando e "
                "tente outra coisa (A em vez de B ou o contrário, outro caminho, falar com alguém, sair do menu "
                "com B, pedir_replanejamento)."
            )
        if parado >= 5:
            estado.atualizar(
                replanejar=True, evento=("replanejar", f"situação parada há {parado + 1} ações: {lido[:120]}")
            )
            partes.append("Preso há muitas ações: o estrategista vai replanejar; termine o episódio.")
        return " | ".join(p for p in partes if p)

    async def executar(nome, func, *args):
        async with vez:
            nav.mundo.golpes = conhecimento.capacidades(estado.dados["time"], estado.dados["insignias"])
            nav.mundo.portoes = _portoes()
            nav.relato = []
            inicio = time.monotonic()
            try:
                resultado = await asyncio.to_thread(func, *args)
            except Exception as exc:  # controle fora do ar, janela do OBS fechada: o modelo precisa saber
                estado.acao(nome, f"ERRO {exc}")
                return _erro(f"{nome} falhou: {exc}")
            imagem = None
            if isinstance(resultado, tuple):  # ferramentas que fotografam menus devolvem a própria imagem
                resultado, imagem = resultado
            if nav.relato:  # selvagens que o piloto resolveu no caminho
                resultado = f"{resultado} | piloto no caminho: {'; '.join(nav.relato)}"
            texto_sit, n = await asyncio.to_thread(situacao)
            try:
                leitura = await asyncio.to_thread(entender, n, texto_sit, nome)
            except Exception as exc:  # leitura auxiliar: um erro aqui não pode esconder a tela do modelo
                leitura = f"(texto da tela ilegível: {exc})"
            if resultado == "parado":
                resultado = "o texto não sai nem com B nem com A"
            resumo = (
                f"{resultado} | {texto_sit}"
                + (f" | {leitura}" if leitura else "")
                + f" | {time.monotonic() - inicio:.1f}s"
            )
            estado.acao(nome, resumo)
            return _ok(resumo, n if imagem is None else imagem)

    # ---------------- ações no jogo ----------------

    @tool("ver_tela", "Mostra a tela atual do jogo, o tipo de tela e sua posição no mapa (quando no mapa).", {})
    async def ver_tela(_args):
        return await executar("ver_tela", lambda: "olhando")

    @tool(
        "apertar",
        "Aperta botões em sequência e devolve a tela. Botões: A, B, START, SELECT, L, R, CIMA, BAIXO, ESQUERDA, "
        "DIREITA. Ex.: 'BAIXO BAIXO A'. Para menus sem ferramenta própria (loja, PC, golpe novo, nomes, TM). "
        f"Até {MAX_BOTOES} botões. espera = segundos depois (padrão 0.5).",
        _esquema({"botoes": {"type": "string"}, "espera": {"type": "number"}}, ["botoes"]),
    )
    async def apertar(args):
        botoes = args["botoes"].upper().replace(",", " ").split()
        invalidos = [b for b in botoes if b not in maos.BOTOES]
        if invalidos or not botoes or len(botoes) > MAX_BOTOES:
            return _erro(f"botões inválidos {invalidos} (use {', '.join(maos.BOTOES)}; até {MAX_BOTOES})")
        espera = min(max(float(args.get("espera", 0.5)), 0.2), 5.0)
        return await executar(
            f"apertar {' '.join(botoes)}", lambda: (maos.apertar(*botoes), time.sleep(espera), "ok")[-1]
        )

    @tool(
        "ir_para",
        "Anda sozinho até o destino, atravessando portas e divisas, correndo e desviando de obstáculos. Sem x/y vai até o "
        "mapa; com x/y vai até o tile. Selvagem no caminho é resolvido sozinho pelo piloto (espécie que falta na Pokédex "
        "é enfraquecida e capturada; as outras fogem ou servem de treino, conforme modo_selvagens) e a caminhada segue. "
        "Para ao chegar, em treinador ou diálogo, em batalha que precisa de decisão ou se não houver caminho. Ids do "
        "jogo: MAP_PEWTER_CITY, MAP_ROUTE3... Item no chão, NPC e placa ocupam o tile: use falar_com ou coletar_itens.",
        _esquema({"mapa": {"type": "string"}, "x": {"type": "integer"}, "y": {"type": "integer"}}, ["mapa"]),
    )
    async def ir_para(args):
        m, erro = _mapa_valido(args["mapa"])
        if erro:
            return _erro(erro)
        destino = ("tile", m, args["x"], args["y"]) if "x" in args and "y" in args else ("mapa", m)
        return await executar(f"ir_para {destino[1:]}", nav.ir, destino)

    @tool(
        "empurrar_pedra",
        "Quebra-cabeça de pedra com STRENGTH (Victory Road...): leva a pedra que está em (x, y) até (alvo_x, alvo_y), "
        "planejando os empurrões e andando até atrás dela a cada um; pede o STRENGTH sozinho no primeiro. Passe a "
        "posição ATUAL da pedra (sair do mapa a devolve à inicial, que info_mapa mostra) e as das outras pedras que você "
        "já tirou do lugar em 'outras' ([[x, y], ...]). Alvo típico: o botão do chão (MB_STRENGTH_BUTTON).",
        _esquema(
            {
                "mapa": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "alvo_x": {"type": "integer"},
                "alvo_y": {"type": "integer"},
                "outras": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}},
            },
            ["mapa", "x", "y", "alvo_x", "alvo_y"],
        ),
    )
    async def empurrar_pedra(args):
        m, erro = _mapa_valido(args["mapa"])
        if erro:
            return _erro(erro)
        return await executar(
            f"empurrar_pedra {m} ({args['x']},{args['y']}) -> ({args['alvo_x']},{args['alvo_y']})",
            nav.empurrar_pedra,
            m,
            (args["x"], args["y"]),
            (args["alvo_x"], args["alvo_y"]),
            [tuple(o) for o in args.get("outras") or []],
        )

    @tool(
        "falar_com",
        "Vai até o lado do tile (x, y) de um NPC, placa ou item, vira para ele e aperta A; depois use avancar_texto. "
        "Atendente de loja fica atrás do balcão: passe o tile do balcão (uma casa à frente dela).",
        _esquema({"mapa": {"type": "string"}, "x": {"type": "integer"}, "y": {"type": "integer"}}, ["mapa", "x", "y"]),
    )
    async def falar_com(args):
        m, erro = _mapa_valido(args["mapa"])
        if erro:
            return _erro(erro)

        def falar():
            r = nav.ir(("vizinho", m, args["x"], args["y"]))
            if r.startswith("chegou"):
                maos.apertar("A")
                time.sleep(0.6)
            return r

        return await executar(f"falar_com {m} ({args['x']},{args['y']})", falar)

    @tool(
        "avancar_texto",
        "Passa diálogos e textos de batalha até uma decisão (menu, golpes, Sim/Não), o mapa ou "
        "outra tela. Nunca responde Sim/Não sozinho.",
        {},
    )
    async def avancar_texto(_args):
        return await executar("avancar_texto", batalha.avancar)

    @tool(
        "lutar",
        "Na batalha: FIGHT e o golpe (1 cima-esq, 2 cima-dir, 3 baixo-esq, 4 baixo-dir), passando o texto "
        "até a próxima decisão ou o fim.",
        _esquema({"golpe": {"type": "integer", "minimum": 1, "maximum": 4}}, ["golpe"]),
    )
    async def lutar(args):
        def lutar_():
            n = olhos.tela()
            esp, nota = olhos.identificar_meu(n, [p["especie"] for p in estado.dados["time"]])
            if nota >= olhos.IDENTIFICOU:
                piloto.gastar_pp(estado, esp, args["golpe"])
            r = batalha.lutar(args["golpe"])
            if r == "batalha_menu":
                piloto.anotar_hp(estado, olhos.tela())
            if r == "mapa":
                estado.contar("batalhas_terminadas")
                estado.atualizar(batalhas_desde_leitura=estado.dados.get("batalhas_desde_leitura", 0) + 1)
            return r

        return await executar(f"lutar {args['golpe']}", lutar_)

    @tool("ver_golpes", "Na batalha: abre a lista de golpes (nomes; PP e tipo do selecionado) e a deixa aberta.", {})
    async def ver_golpes(_args):
        return await executar("ver_golpes", batalha.ver_golpes)

    @tool("fugir", "Na batalha contra selvagem: RUN e passa o texto.", {})
    async def fugir(_args):
        def fugir_():
            estado.contar("fugas")
            return batalha.fugir()

        return await executar("fugir", fugir_)

    @tool(
        "abrir_menu_batalha",
        "Na batalha: abre BAG (itens) ou POKEMON (trocar); navegue dentro com apertar.",
        _esquema({"opcao": {"type": "string", "enum": ["BAG", "POKEMON"]}}, ["opcao"]),
    )
    async def abrir_menu_batalha(args):
        return await executar(f"abrir {args['opcao']}", batalha.abrir, args["opcao"])

    @tool(
        "responder",
        "Responde a caixa Sim/Não na tela (sim=true para YES), conferindo a setinha, e passa o texto.",
        _esquema({"sim": {"type": "boolean"}}, ["sim"]),
    )
    async def responder(args):
        return await executar(f"responder {'sim' if args['sim'] else 'não'}", batalha.responder, args["sim"])

    def _de_treinador(especie):
        """Motivo para recusar a captura se a espécie não aparece selvagem no mapa atual (então é de treinador)."""
        if combate.ultima_abertura["texto"]:
            return (
                f'esta luta começou com "{combate.ultima_abertura["texto"]} would like to battle!": Pokémon de '
                "treinador não pode ser capturado. Lute normalmente (batalha_automatica)"
            )
        m = nav.loc.ultima.mapa if nav.loc.ultima else None
        selvagens = mapa.selvagens().get(m) if m else None
        # encontros fixos (Snorlax, Zapdos, Electrode da usina) vêm de setwildbattle no script do mapa
        fixos = (
            set(re.findall(r"setwildbattle SPECIES_(\w+)", "\n".join(conhecimento._scripts(m)[0].values())))
            if m
            else set()
        )
        if selvagens and especie.upper() not in {e for d in selvagens.values() for e in d} | fixos:
            return (
                f"{especie} não aparece selvagem em {m} (nem pescando nem com Rock Smash): é Pokémon de treinador, "
                "não dá para capturar. Lute normalmente (batalha_automatica)"
            )
        return None

    def _master_a_toa(especie, bola):
        if "MASTER" in bola.upper() and especie.upper() not in conhecimento.LENDARIOS:
            return (
                f"a MASTER BALL é só para lendário (Mewtwo, aves, cães, Lugia/Ho-Oh): não gaste em {especie}. "
                "Confira a posição de cada bola no bolso com ver_mochila e use outra"
            )
        return None

    @tool(
        "capturar",
        "Na batalha contra selvagem: joga a bola da posição dada no bolso POKé BALLS (1 = primeira da lista) e "
        "acompanha até o resultado (capturou | escapou). Desconta a bola da mochila e registra a captura sozinha. "
        "Enfraqueça antes (HP vermelho, ou sono/paralisia) para não gastar bolas.",
        _esquema(
            {
                "especie": {"type": "string"},
                "nivel": {"type": "integer"},
                "bola": {"type": "string", "description": "nome da bola, ex.: POKé BALL, GREAT BALL"},
                "posicao": {"type": "integer", "minimum": 1},
            },
            ["especie", "nivel"],
        ),
    )
    async def capturar(args):
        if motivo := _de_treinador(args["especie"]) or _master_a_toa(args["especie"], args.get("bola", "")):
            return _erro(motivo)
        bola = args.get("bola", "POKé BALL")

        def capturar_():
            r = batalha.capturar(
                args.get("posicao", 1),
                bola=bola,
                master=args["especie"].upper() in conhecimento.LENDARIOS,
                ao_arremessar=lambda: (
                    estado.ajustar_item(bola, -1, f"arremessada em {args['especie']}"),
                    estado.contar("bolas_usadas"),
                ),
            )
            if r == "capturou":
                estado.registrar_captura(args["especie"], args["nivel"], f"capturado com {bola}")
            return r

        return await executar(f"capturar {args['especie']}", capturar_)

    @tool(
        "abrir_menu",
        "Fora da batalha: abre o menu START e entra na opção, conferindo a setinha (o cursor do START "
        "lembra a última posição, então não conte toques). JOGADOR é o cartão de treinador.",
        _esquema({"opcao": {"type": "string", "enum": menus.START}}, ["opcao"]),
    )
    async def abrir_menu(args):
        def abrir():
            if not menus.abrir_start(args["opcao"]):
                return f"não consegui abrir {args['opcao']}"
            olhos.assentar(0.8)
            return f"{args['opcao']} aberto"

        return await executar(f"abrir_menu {args['opcao']}", abrir)

    @tool(
        "enfraquecer_e_capturar",
        "Captura como jogador: a cada turno lê o HP do inimigo na barra, calcula a chance de captura (fórmula da Gen 3) "
        "e o dano de cada golpe seu (fórmula de dano do jogo). Enquanto a chance for baixa, usa o golpe mais forte que NÃO "
        "derruba; se o seu em campo derrubaria com qualquer golpe, troca sozinho para um mais fraco do time que tire vida; "
        "quando a chance passa de 'chance_minima', joga a bola. Use em toda espécie que falta na Pokédex.",
        _esquema(
            {
                "especie": {"type": "string"},
                "nivel": {"type": "integer"},
                "meu": {"type": "string", "description": "espécie do seu Pokémon em campo"},
                "status_inimigo": {"type": "string", "enum": list(conhecimento.STATUS_CAPTURA)},
                "bola": {"type": "string"},
                "posicao_bola": {"type": "integer", "minimum": 1},
                "chance_minima": {"type": "number"},
                "max_bolas": {"type": "integer", "minimum": 1},
            },
            ["especie", "nivel", "meu"],
        ),
    )
    async def enfraquecer_e_capturar(args):
        if motivo := _de_treinador(args["especie"]) or _master_a_toa(args["especie"], args.get("bola", "")):
            return _erro(motivo)
        meu = next((p for p in estado.dados["time"] if p["especie"].upper() == args["meu"].upper()), None)
        if not meu or not meu.get("golpes"):
            return _erro(f"não sei nível e golpes de {args['meu']}: use ver_time antes")
        return await executar(
            f"enfraquecer_e_capturar {args['especie']}",
            piloto.enfraquecer_e_capturar,
            estado,
            args["especie"].upper(),
            args["nivel"],
            meu,
            args.get("bola", "POKE BALL"),
            args.get("posicao_bola", 1),
            args.get("chance_minima", 0.55),
            args.get("max_bolas", 6),
            args.get("status_inimigo", ""),
        )

    def _hp(p):
        return "?" if p.get("hp") is None else f"{p['hp']:.0%}"

    def _resumo_time(lidos):
        return "; ".join(
            f"{i}. {p['especie']} nv{p['nivel']} HP {_hp(p)} [{', '.join(p['golpes'])}]" for i, p in enumerate(lidos, 1)
        )

    @tool(
        "ver_time",
        "Fora da batalha: lê do jogo o time inteiro, na ordem (espécie, nível, HP, golpes com PP), e grava "
        "na memória sozinho.",
        {},
    )
    async def ver_time(_args):
        def ver():
            r = piloto.sincronizar_time(estado)
            return r if isinstance(r, str) else "time: " + _resumo_time(r)

        return await executar("ver_time", ver)

    @tool(
        "ver_mochila",
        "Lê os três bolsos da mochila (ITEMS, KEY ITEMS, POKé BALLS), no mapa ou na batalha, e grava "
        "itens e quantidades na memória sozinho.",
        {},
    )
    async def ver_mochila(_args):
        def ver():
            texto_, imagem = menus.ver_mochila(olhos.classificar(olhos.tela()) == "batalha_menu")
            if imagem is None:
                return texto_
            itens = menus.ler_bolsos([imagem[i : i + 160] for i in range(0, imagem.shape[0], 160)])
            if not itens:
                return texto_, imagem  # leitura falhou: o modelo confere na imagem
            estado.definir_mochila(itens, completa=True)
            return "mochila: " + ", ".join(f"{k} x{v}" for k, v in itens.items())

        return await executar("ver_mochila", ver)

    @tool(
        "comprar",
        "No Poké Mart (mapa da loja): compra {item: quantidade} falando com a atendente pelo balcão; confere "
        "a quantidade na tela (para no que o dinheiro paga) e soma na mochila. Cada loja tem estoque próprio "
        "e fixo: veja com a ferramenta loja.",
        _esquema({"itens": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 1}}}, ["itens"]),
    )
    async def comprar(args):
        def comprar_():
            comprados, relato = menus.comprar(nav, args["itens"])
            precos = dict(conhecimento.lojas().get(nav.loc.ultima.mapa, []))
            for item, qtd in comprados.items():
                estado.ajustar_item(item, qtd, "compra")
            gasto = sum(precos.get(i, 0) * q for i, q in comprados.items())
            if comprados:
                if estado.dados.get("dinheiro") is not None:
                    estado.atualizar(dinheiro=max(estado.dados["dinheiro"] - gasto, 0))
                estado.evento("compra", f"{relato} (₽{gasto})")
            return relato

        return await executar(f"comprar {args['itens']}", comprar_)

    @tool(
        "vender",
        "No Poké Mart: vende {item: quantidade} da mochila (a loja paga metade do preço). Use para NUGGET, "
        "STAR PIECE e itens sem uso quando faltar dinheiro.",
        _esquema({"itens": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 1}}}, ["itens"]),
    )
    async def vender(args):
        def vender_():
            vendidos, relato = menus.vender(nav, args["itens"])
            ganho = 0
            for item, qtd in vendidos.items():
                estado.ajustar_item(item, -qtd, "venda")
                info = next((v for v in conhecimento.itens().values() if v[0] == item), None)
                ganho += (info[1] // 2 * qtd) if info else 0
            if vendidos:
                if estado.dados.get("dinheiro") is not None:
                    estado.atualizar(dinheiro=estado.dados["dinheiro"] + ganho)
                estado.evento("compra", f"{relato} (+₽{ganho})")
            return relato

        return await executar(f"vender {args['itens']}", vender_)

    @tool(
        "batalha_automatica",
        "Na batalha contra treinador comum (depois de falar com ele ou se a luta já começou): "
        "o piloto identifica o treinador, simula e luta sozinho até o fim — golpe que derruba "
        "mais rápido pela tabela de tipos, troca quando o confronto vira, Potion quando salva. "
        "Devolve a vez se a luta for importante (líder, rival, Elite), dupla ou arriscada.",
        {},
    )
    async def batalha_automatica(_args):
        def lutar_sozinho():
            m = nav.loc.ultima.mapa if nav.loc.ultima else None
            ok, relato = combate.lutar_treinador(estado, m, lambda p, i: piloto._lutar(estado, p, i), piloto.trocar)
            if ok:
                estado.contar("batalhas_terminadas")
                estado.contar("vitorias")
                estado.evento("batalha", relato)
            return relato if ok else f"{relato} (a decisão é sua)"

        return await executar("batalha_automatica", lutar_sozinho)

    @tool(
        "golpe_novo",
        "Quando aparecer 'Delete a move to make room for X?' (golpe novo por nível, Rare Candy ou TM): "
        "decide pela nota e cobertura (decidir_golpe_novo) e executa sozinho, escolhendo quem esquecer "
        "ou recusando. 'pokemon' só se não for óbvio quem está aprendendo.",
        _esquema({"pokemon": {"type": "string"}}, []),
    )
    async def golpe_novo(args):
        return await executar("golpe_novo", piloto.golpe_novo, estado, args.get("pokemon"))

    @tool(
        "ver_pc",
        "Num Centro Pokémon: lê as 14 caixas do PC (espécie, nível e caixa de cada Pokémon) e grava na "
        "memória sozinho.",
        {},
    )
    async def ver_pc(_args):
        def ver():
            texto, lista = menus.ver_pc(nav)
            if lista is not None:
                estado.atualizar(pc=lista, pc_lido_em=time.strftime("%d/%m %H:%M"), evento=("pc", texto))
            return texto

        return await executar("ver_pc", ver)

    def _posicao(nome):
        return next((i for i, p in enumerate(estado.dados["time"]) if p["especie"] == nome.strip().upper()), None)

    @tool(
        "guardar_no_pc",
        "Num Centro Pokémon: guarda no PC os Pokémon do time com essas espécies (abre vaga para "
        "captura nova ou tira quem não serve ao plano). Atualiza time e PC na memória.",
        _esquema({"especies": {"type": "array", "items": {"type": "string"}, "minItems": 1}}, ["especies"]),
    )
    async def guardar_no_pc(args):
        def guardar():
            guardados, relato = menus.depositar(nav, args["especies"])
            if guardados:
                estado.atualizar(
                    pc=estado.dados["pc"] + [{"especie": e, "nivel": nv} for e, nv in guardados],
                    evento=("troca_pc", relato),
                )
                piloto.sincronizar_time(estado)
            return relato

        return await executar(f"guardar_no_pc {args['especies']}", guardar)

    @tool(
        "tirar_do_pc",
        "Num Centro Pokémon: tira do PC para o time essas espécies (o time precisa ter vaga: guarde "
        "antes). Atualiza time e PC na memória.",
        _esquema({"especies": {"type": "array", "items": {"type": "string"}, "minItems": 1}}, ["especies"]),
    )
    async def tirar_do_pc(args):
        def tirar():
            retirados, relato = menus.retirar(nav, args["especies"])
            if retirados:
                pc = list(estado.dados["pc"])
                for e, _ in retirados:
                    i = next((i for i, p in enumerate(pc) if p["especie"] == e), None)
                    if i is not None:
                        pc.pop(i)
                estado.atualizar(pc=pc, evento=("troca_pc", relato))
                piloto.sincronizar_time(estado)
            return relato

        return await executar(f"tirar_do_pc {args['especies']}", tirar)

    @tool(
        "dar_item",
        "Fora da batalha: dá um item do bolso ITEMS (EXP. SHARE, LEFTOVERS...) para um Pokémon do time "
        "segurar. Se ele já segura outro, só troca com trocar=true (o antigo volta à mochila).",
        _esquema(
            {"item": {"type": "string"}, "pokemon": {"type": "string"}, "trocar": {"type": "boolean"}},
            ["item", "pokemon"],
        ),
    )
    async def dar_item(args):
        def dar():
            deu, relato = menus.dar_item(args["item"], args["pokemon"], args.get("trocar", False))
            if deu:
                estado.ajustar_item(args["item"], -1, f"dado a {args['pokemon']} para segurar")
                estado.anotar(f"{args['pokemon'].upper()} segura {args['item'].upper()}")
            return relato

        return await executar(f"dar_item {args['item']} {args['pokemon']}", dar)

    @tool(
        "tirar_item",
        "Fora da batalha: tira o item que um Pokémon do time segura (volta à mochila). Carta (MAIL) vai "
        "para o PC: assim o Pokémon pode ser guardado no PC.",
        _esquema({"pokemon": {"type": "string"}}, ["pokemon"]),
    )
    async def tirar_item(args):
        i = _posicao(args["pokemon"])
        if i is None:
            return _erro(f"{args['pokemon']} não está no time")

        def tirar():
            tirou, relato = menus.tirar_item(args["pokemon"].upper(), estado.dados["time"][i].get("golpes") or [])
            if tirou:
                estado.anotar(f"{args['pokemon'].upper()} não segura mais item: {relato}")
            return relato

        return await executar(f"tirar_item {args['pokemon']}", tirar)

    @tool(
        "tornar_shiny",
        "Num Centro Pokémon: deixa SHINY, pelo ACE, um Pokémon do TIME. Use em todo lendário e mítico "
        "logo depois de capturá-lo. Leva-o à Caixa 10, salva, dispara o código, confere a estrela no "
        "resumo e o devolve ao time (no fim da lista). Um por vez, uns 2 minutos.",
        _esquema({"especie": {"type": "string"}}, ["especie"]),
    )
    async def tornar_shiny(args):
        def fazer():
            r = menus.tornar_shiny(nav, args["especie"])
            estado.atualizar(evento=("ace_shiny", r))
            piloto.sincronizar_time(estado)
            return r

        return await executar(f"tornar_shiny {args['especie']}", fazer)

    @tool(
        "mudar_ordem",
        "Fora da batalha: põe um Pokémon do time na posição (1 = quem entra primeiro na batalha).",
        _esquema(
            {"pokemon": {"type": "string"}, "posicao": {"type": "integer", "minimum": 1, "maximum": 6}},
            ["pokemon", "posicao"],
        ),
    )
    async def mudar_ordem(args):
        i = _posicao(args["pokemon"])
        if i is None:
            return _erro(f"{args['pokemon']} não está no time da memória: use ver_time")

        def mudar():
            r = menus.trocar_ordem(i, args["posicao"] - 1, estado.dados["time"][i].get("golpes") or [])
            lidos = piloto.sincronizar_time(estado)
            return r if isinstance(lidos, str) else f"{r} | time: {_resumo_time(lidos)}"

        return await executar(f"mudar_ordem {args['pokemon']} -> {args['posicao']}", mudar)

    @tool(
        "trocar_na_batalha",
        "Na batalha: troca o Pokémon em campo por outro do time (gasta o turno). Também serve "
        "quando o seu desmaiou e o jogo abriu a tela do time para escolher quem entra.",
        _esquema({"pokemon": {"type": "string"}}, ["pokemon"]),
    )
    async def trocar_na_batalha(args):
        if _posicao(args["pokemon"]) is None:
            return _erro(f"{args['pokemon']} não está no time da memória")
        return await executar(f"trocar_na_batalha {args['pokemon']}", piloto.trocar, args["pokemon"].strip().upper())

    @tool(
        "preparar_batalha",
        "Simula a luta contra um treinador (sem 'adversario': a próxima luta obrigatória do roteiro, "
        "como rival ou líder) com o time atual, pelas fórmulas do jogo: quem enfrenta quem, HP que "
        "sobra e veredito (VENCE, NO LIMITE, PERDE). Se não vencer com folga, mostra o nível que "
        "cada um seu precisaria e quais capturáveis agora vencem cada adversário. Rode antes de "
        "toda luta obrigatória e não entre nela sem VENCE com folga.",
        _esquema({"adversario": {"type": "string", "description": "id ou nome: RIVAL_CERULEAN, MISTY..."}}, []),
    )
    async def preparar_batalha(args):
        def calcular():
            minhas = [p["especie"] for p in estado.dados["time"] + estado.dados["pc"]]
            if args.get("adversario"):
                busca = args["adversario"].strip().upper().replace(" ", "_")
                ids = [t for t, d in conhecimento.treinadores().items() if busca in t or busca == d["nome"].upper()]
                rival = conhecimento.inicial_do_rival(minhas)
                ids = [t for t in ids if "RIVAL" not in t and "CHAMPION" not in t or (rival and t.endswith(rival))][:3]
                marco = None
            else:
                marco, ids = conhecimento.proxima_luta(estado.dados["marcos"], minhas)
            if not ids:
                return (
                    "nenhuma luta obrigatória liberada no roteiro"
                    if not args.get("adversario")
                    else "treinador não achado"
                )
            alc, golpes = _alcance()
            cands = conhecimento.candidatos_de_captura(alc, golpes, estado.dados["mochila"], set(minhas))
            return (f"luta do marco {marco}\n" if marco else "") + "\n\n".join(
                conhecimento.preparar_batalha(t, estado.dados["time"], cands) for t in ids
            )

        return _ok(await asyncio.to_thread(calcular))

    @tool(
        "usar_item",
        "Fora da batalha: usa um item da mochila (POTION, RARE CANDY, ANTIDOTE, REPEL, ESCAPE ROPE, pedra "
        "de evolução, BICYCLE...). Itens que pedem um Pokémon precisam de 'pokemon'. Desconta da mochila.",
        _esquema({"item": {"type": "string"}, "pokemon": {"type": "string"}}, ["item"]),
    )
    async def usar_item(args):
        i = _posicao(args["pokemon"]) if args.get("pokemon") else None
        if args.get("pokemon") and i is None:
            return _erro(f"{args['pokemon']} não está no time da memória")

        def usar():
            r = menus.usar_item(args["item"], i)
            if r.endswith(" usado"):
                chave = conhecimento._chave(args["item"])
                bolso = next((v[2] for v in conhecimento.itens().values() if conhecimento._chave(v[0]) == chave), "")
                if bolso != "KEY_ITEMS":
                    estado.ajustar_item(
                        args["item"], -1, f"usado{' em ' + args['pokemon'] if args.get('pokemon') else ''}"
                    )
            return r

        return await executar(f"usar_item {args['item']}", usar)

    @tool(
        "pescar",
        "De frente para a água: usa a vara (OLD ROD, GOOD ROD, SUPER ROD) e puxa no 'Oh! A bite!'. "
        "Devolve batalha (selvagem fisgado) ou nada; repita para tentar de novo.",
        _esquema({"vara": {"type": "string", "enum": ["OLD ROD", "GOOD ROD", "SUPER ROD"]}}, ["vara"]),
    )
    async def pescar(args):
        return await executar(f"pescar {args['vara']}", menus.pescar, args["vara"])

    @tool(
        "coletar_itens",
        "Pega todos os itens do mapa atual que ainda não foram pegos (do chão e escondidos), do mais "
        "perto ao mais longe, e soma cada um na mochila. Use em todo mapa novo e ao voltar com HM nova.",
        _esquema({"limite": {"type": "integer", "minimum": 1}}, []),
    )
    async def coletar_itens(args):
        return await executar("coletar_itens", coleta.coletar_itens, nav, estado, args.get("limite", 25))

    @tool(
        "obter_pokemon",
        "Vai até quem dá a espécie (presente, compra como o Magikarp da Rota 4, troca, prêmio) e "
        "conduz a conversa: aceita, recusa só o apelido e, na troca, entrega a espécie pedida.",
        _esquema({"especie": {"type": "string"}}, ["especie"]),
    )
    async def obter_pokemon(args):
        def escolher(pede):
            i = _posicao(pede)
            if i is None:
                return f"não tenho {pede} no time para a troca"
            return f"entregou {pede}" if menus.escolher_no_time(i) else "não achei o cursor do time"

        def obter():
            r = coleta.obter_pokemon(nav, estado, args["especie"], escolher)
            if r.endswith("recebido"):
                piloto.sincronizar_time(estado)
            return r

        return await executar(f"obter_pokemon {args['especie']}", obter)

    @tool(
        "treinar",
        "Treino automático no mapa atual (ou em 'mapa'): anda na grama e o piloto luta cada selvagem. Quem "
        "está em 'alvos' começa a batalha; se o selvagem for forte para ele, troca para a 'escolta' no 1º "
        "turno e os dois dividem a experiência. Cura no Centro quando o HP cai e volta. Para no tempo, quando "
        "todos os alvos chegam ao nível, em treinador ou em golpe novo. Escolha o lugar com avaliar_time / "
        "onde_treinar.",
        _esquema(
            {
                "alvos": {
                    "type": "object",
                    "additionalProperties": {"type": "integer"},
                    "description": 'espécie -> nível desejado, ex.: {"ODDISH": 20}',
                },
                "escolta": {"type": "string", "description": "Pokémon forte do time que entra no lugar do alvo"},
                "minutos": {"type": "integer", "minimum": 1, "maximum": 60},
                "mapa": {"type": "string"},
            },
            ["alvos"],
        ),
    )
    async def treinar(args):
        alvos = {k.strip().upper(): v for k, v in args["alvos"].items()}
        fora = [k for k in list(alvos) + ([args["escolta"]] if args.get("escolta") else []) if _posicao(k) is None]
        if fora:
            return _erro(f"fora do time da memória: {fora} (use ver_time ou tirar_do_pc)")
        m = None
        if args.get("mapa"):
            m, erro = _mapa_valido(args["mapa"])
            if erro:
                return _erro(erro)
        estado.atualizar(
            treino={"alvos": alvos, "escolta": (args.get("escolta") or "").strip().upper()},
            evento=("treino", f"treinar {alvos} com escolta {args.get('escolta') or 'nenhuma'}"),
        )

        def treinar_():
            if m:
                r = nav.ir(("mapa", m))
                if not r.startswith("chegou"):
                    return f"não cheguei ao lugar de treino: {r}"
            return piloto.treinar(nav, estado, args.get("minutos", 15))

        return await executar(f"treinar {alvos}", treinar_)

    @tool(
        "modo_selvagens",
        "Como o piloto trata selvagens de espécies que você já tem: fugir (padrão, viagem rápida) "
        "ou treinar (luta com o time na ordem atual). Espécie que falta é sempre capturada.",
        _esquema({"modo": {"type": "string", "enum": ["fugir", "treinar"]}}, ["modo"]),
    )
    async def modo_selvagens(args):
        estado.atualizar(modo_selvagens=args["modo"], evento=("treino", f"selvagens: {args['modo']}"))
        return _ok(f"selvagens: {args['modo']}")

    @tool(
        "ver_pokedex",
        "Lista das espécies que você REALMENTE já teve (capturas, presentes, trocas e evoluções, que a "
        "memória registra sozinha). A Pokédex do jogo foi preenchida inteira por um código ACE e não "
        "serve para saber o que falta: não abra a Pokédex do jogo para isso.",
        {},
    )
    async def ver_pokedex(_args):
        cap = estado.dados["pokedex_capturados"]
        return _ok(f"{len(cap)} espécies de verdade: {', '.join(cap)}")

    @tool("curar", "Vai ao Centro Pokémon mais próximo, fala com a atendente e cura o time.", {})
    async def curar(_args):
        def curar_():
            r = menus.curar(nav)
            if r.startswith("time curado"):
                estado.evento("cura", r)
            return r

        return await executar("curar", curar_)

    @tool("salvar", "Salva o jogo (START, SAVE, YES). A tela de salvar mostra insígnias, Pokédex e tempo de jogo.", {})
    async def salvar(_args):
        def salvar_():
            r = menus.salvar()
            estado.evento("save", r)
            return r

        return await executar("salvar", salvar_)

    # ---------------- conhecimento do jogo (dados do código-fonte) ----------------

    @tool(
        "info_mapa",
        "Dados de um mapa: divisas, portas (com destino), NPCs e treinadores (posição inicial, visão), "
        "itens, placas e selvagens com nível e chance.",
        _esquema({"mapa": {"type": "string"}}, ["mapa"]),
    )
    async def info_mapa(args):
        m, erro = _mapa_valido(args["mapa"])
        return _erro(erro) if erro else _ok(mapa.descrever(m))

    @tool(
        "onde_encontrar",
        "Mapas onde uma espécie aparece selvagem no FireRed, com método, níveis e chance.",
        _esquema({"especie": {"type": "string"}}, ["especie"]),
    )
    async def onde_encontrar(args):
        locais = mapa.onde_encontrar(args["especie"])
        if not locais:
            return _ok(f"{args['especie']} não aparece selvagem (presente, troca, evolução, fóssil ou evento).")
        return _ok("\n".join(f"{m}: {met}, nível {a}-{b}, {c}%" for m, met, a, b, c in locais[:15]))

    @tool(
        "info_pokemon",
        "Tipos, atributos base, taxa de captura, evolução, golpes por nível e HMs de uma espécie.",
        _esquema({"especie": {"type": "string"}}, ["especie"]),
    )
    async def info_pokemon(args):
        return _ok(conhecimento.info_pokemon(args["especie"]) or f"espécie {args['especie']} não encontrada")

    @tool(
        "info_treinador",
        "Time (espécies, níveis e golpes) de treinadores pelo nome ou id: BROCK, MISTY, "
        "RIVAL_ROUTE22, ELITE_FOUR_LORELEI...",
        _esquema({"nome": {"type": "string"}}, ["nome"]),
    )
    async def info_treinador(args):
        return _ok(conhecimento.info_treinador(args["nome"]) or "nenhum treinador com esse nome")

    @tool(
        "desafios",
        "Todos os líderes na ordem da história (marcando os já vencidos), a Elite dos 4 e o Campeão, "
        "com o nível dos Pokémon de cada um.",
        {},
    )
    async def desafios(_args):
        return _ok(conhecimento.proximos_desafios(estado.dados["insignias"]))

    @tool(
        "analisar_golpes",
        "Batalha: ranking dos golpes do seu Pokémon contra a espécie inimiga (tipo, físico/especial, poder, multiplicador "
        "da tabela de tipos do jogo, bônus de mesmo tipo) e o risco dos tipos dela contra você. Sem 'golpes', usa os "
        "golpes do Pokémon na memória do time.",
        _esquema(
            {
                "inimigo": {"type": "string"},
                "meu": {"type": "string"},
                "golpes": {"type": "array", "items": {"type": "string"}},
            },
            ["inimigo", "meu"],
        ),
    )
    async def analisar_golpes(args):
        golpes = args.get("golpes") or next(
            (p.get("golpes") or [] for p in estado.dados["time"] if p["especie"].upper() == args["meu"].upper()), []
        )
        if not golpes:
            return _erro(f"não sei os golpes de {args['meu']}: passe 'golpes' ou use ver_golpes/ver_time antes")
        return _ok(conhecimento.analisar_golpes(golpes, args["meu"], args["inimigo"]))

    def _membro(nome):
        return next(
            (
                p
                for p in estado.dados["time"] + estado.dados["pc"]
                if p["especie"].upper() == nome.upper() or (p.get("apelido") or "").upper() == nome.upper()
            ),
            None,
        )

    def _tms_na_mochila():
        return [k for k in estado.dados["mochila"] if re.match(r"^(TM|HM)\d\d", k)]

    @tool(
        "avaliar_golpes",
        "Avalia o conjunto de golpes de um Pokémon do time: nota de cada golpe (poder efetivo, mesmo tipo, atributo, "
        "efeito), cobertura contra o próximo líder, golpes repetidos ou fracos, o que aprende nos próximos níveis, "
        "evolução e as melhores TM/HM compatíveis (marca as que estão na mochila). Use ao planejar o time.",
        _esquema({"pokemon": {"type": "string"}}, ["pokemon"]),
    )
    async def avaliar_golpes(args):
        p = _membro(args["pokemon"])
        if not p or not p.get("golpes"):
            return _erro(f"não sei os golpes de {args['pokemon']}: use ver_time antes")
        return _ok(
            conhecimento.avaliar_golpes(
                p["especie"], p["nivel"], p["golpes"], estado.dados["insignias"], _tms_na_mochila()
            )
        )

    @tool(
        "decidir_golpe_novo",
        "Quando o jogo perguntar se um Pokémon deve aprender um golpe (subida de nível ou TM/HM): diz se vale aprender e "
        "qual golpe esquecer, pela nota e pela cobertura contra o próximo líder. Nunca esquece golpe de HM nem o único "
        "golpe de dano.",
        _esquema({"pokemon": {"type": "string"}, "golpe_novo": {"type": "string"}}, ["pokemon", "golpe_novo"]),
    )
    async def decidir_golpe_novo(args):
        p = _membro(args["pokemon"])
        if not p or not p.get("golpes"):
            return _erro(f"não sei os golpes de {args['pokemon']}: use ver_time antes")
        return _ok(
            conhecimento.decidir_golpe_novo(
                p["especie"], p["nivel"], p["golpes"], args["golpe_novo"], estado.dados["insignias"]
            )
        )

    alcance = {}  # (mapa, golpes, portões) -> mapas alcançáveis; a busca no mundo inteiro leva alguns segundos

    def _alcance():
        """({mapa: distância} a pé daqui com os golpes de campo e os portões da história atuais, golpes)."""
        golpes = conhecimento.capacidades(estado.dados["time"], estado.dados["insignias"])
        local = estado.dados.get("local")
        if not local:
            return None, golpes
        portoes = _portoes() | roteiro.lutas_no_caminho(frozenset(estado.dados["marcos"]))
        chave = (local["mapa"], frozenset(golpes), portoes)
        if chave not in alcance:
            _, elev, _ = mapa.grade(local["mapa"])
            z = int(elev[local["y"], local["x"]])
            mundo = navegacao.Mundo()  # separado do navegador: os gatilhos de luta só fecham o planejamento
            mundo.golpes, mundo.portoes = golpes, portoes
            alcance[chave] = mundo.alcancaveis((local["mapa"], local["x"], local["y"], 0 if z == 15 else z))
        return alcance[chave], golpes

    @tool(
        "avaliar_time",
        "Planejamento do time como um jogador experiente: próximo desafio e nível alvo; nota de cada Pokémon seu (time e "
        "PC) pela forma final e pela vantagem de tipo até a Liga; time sugerido de 6 juntando os seus e os que dá para "
        "capturar AGORA (com mapa e nível — capturar um de nível alto costuma sair mais barato que treinar um fraco); quem "
        "guardar no PC; e onde treinar cada um (sozinho ou escoltado) com a estimativa de batalhas.",
        {},
    )
    async def avaliar_time(_args):
        def calcular():
            alc, golpes = _alcance()
            texto = conhecimento.avaliar_time(
                estado.dados["time"],
                estado.dados["pc"],
                estado.dados["insignias"],
                alc,
                golpes,
                estado.dados["mochila"],
                estado.dados.get("restricao", ""),
            )
            minhas = [p["especie"] for p in estado.dados["time"] + estado.dados["pc"]]
            marco, ids = conhecimento.proxima_luta(estado.dados["marcos"], minhas)
            if ids:  # a luta obrigatória mais próxima manda no curto prazo (o rival vem antes do líder)
                cands = conhecimento.candidatos_de_captura(alc, golpes, estado.dados["mochila"], set(minhas))
                texto = (
                    f"LUTA OBRIGATÓRIA MAIS PRÓXIMA (marco {marco}):\n"
                    + conhecimento.preparar_batalha(ids[0], estado.dados["time"], cands)
                    + "\n\n"
                    + texto
                )
            return texto

        return _ok(await asyncio.to_thread(calcular))

    @tool(
        "onde_treinar",
        "Lugares alcançáveis agora para subir um Pokémon até um nível: selvagens no nível dele "
        "(sozinho) ou mais fortes com escolta (o mais forte do time), com estimativa de batalhas.",
        _esquema({"pokemon": {"type": "string"}, "nivel_alvo": {"type": "integer"}}, ["pokemon", "nivel_alvo"]),
    )
    async def onde_treinar(args):
        p = _membro(args["pokemon"])
        if not p:
            return _erro(f"{args['pokemon']} não está na memória do time/PC")

        def calcular():
            alc, golpes = _alcance()
            forte = max(
                (q for q in estado.dados["time"] if q is not p), key=lambda q: q.get("nivel") or 0, default=None
            )
            ops = conhecimento.onde_treinar(
                p["especie"],
                p["nivel"],
                args["nivel_alvo"],
                forte and (forte["especie"], forte["nivel"]),
                alc or {},
                golpes,
                6,
            )
            return (
                "\n".join(f"{m} ({met} nv {a}-{b}, {modo}, ~{bt:.0f} batalhas)" for _, m, met, a, b, modo, bt in ops)
                or "nenhum lugar alcançável serve: treine em treinadores ou com um Pokémon mais forte de escolta"
            )

        return _ok(await asyncio.to_thread(calcular))

    @tool(
        "roteiro",
        "A história do FireRed em marcos (feitos, prontos para fazer e travados), com onde acontece cada um, "
        "o que exige e o que libera.",
        {},
    )
    async def roteiro_(_args):
        return _ok(roteiro.texto(estado.dados["marcos"]))

    @tool(
        "detonado",
        "Detonado do FireRed (passo a passo da história, lutas obrigatórias com times, itens visíveis e "
        "escondidos, NPCs que dão Pokémon/itens, Pokémon de cada mapa e solução dos quebra-cabeças). Sem "
        "argumentos: a seção do próximo marco do roteiro. Com 'marco' (id do roteiro) ou 'mapa' (MAP_...): "
        "a seção que cobre.",
        _esquema({"marco": {"type": "string"}, "mapa": {"type": "string"}}, []),
    )
    async def detonado(args):
        chave = args.get("mapa") or args.get("marco") or roteiro.proximo_marco(estado.dados["marcos"])
        if args.get("mapa"):
            chave, erro = _mapa_valido(args["mapa"])
            if erro:
                return _erro(erro)
        secoes = roteiro.detonado(chave or "")
        if not secoes:
            return _ok(
                f"nenhuma seção do detonado cita {chave} (o detonado está em dados/detonado; use info_mapa e roteiro)"
            )
        return _ok(f"detonado para {chave}:\n\n" + "\n\n".join(t for _, t in secoes[:2]))

    @tool(
        "concluir_marco",
        "Marca um marco da história como feito (id do roteiro) quando ele aconteceu de verdade.",
        _esquema({"marco": {"type": "string", "enum": roteiro.IDS}, "resultado": {"type": "string"}}, ["marco"]),
    )
    async def concluir_marco(args):
        estado.marco_concluido(args["marco"], args.get("resultado", ""))
        return _ok(
            f"marco {args['marco']} concluído; passos do plano que o citam marcados; o próximo episódio replaneja "
            "(termine este episódio depois de salvar)"
        )

    @tool(
        "pokemon_faltando",
        "Todas as espécies de Kanto que faltam na Pokédex e como conseguir: mapas onde dá para capturar AGORA (a pé, com "
        "os golpes de campo atuais), as que precisam de algo antes (SURF, vara de pesca, HM, evento), as que vêm por "
        "evolução e as que não aparecem selvagens. Use para planejar rotas de captura e voltas com Fly.",
        {},
    )
    async def pokemon_faltando(_args):
        def calcular():
            alc, golpes = _alcance()
            texto = conhecimento.pokemon_faltando(
                estado.dados["pokedex_capturados"], golpes, estado.dados["mochila"], alc
            )
            visitadas = [m for m in estado.dados["visitados"] if "CITY" in m or "TOWN" in m or "ISLAND" in m]
            return (
                f"golpes de campo utilizáveis: {', '.join(sorted(golpes)) or 'nenhum'} | cidades visitadas (destinos do "
                f"Fly): {', '.join(visitadas) or '?'}\n{texto}"
            )

        return _ok(await asyncio.to_thread(calcular))

    @tool(
        "loja",
        "O que o Poké Mart de um mapa vende e por quanto (ex.: MAP_PEWTER_CITY_MART). Sem mapa lista as lojas.",
        _esquema({"mapa": {"type": "string"}}, []),
    )
    async def loja(args):
        lojas = conhecimento.lojas()
        if not args.get("mapa"):
            return _ok("lojas: " + ", ".join(lojas))
        m, erro = _mapa_valido(args["mapa"])
        if erro or m not in lojas:
            return _erro(erro or f"{m} não é loja. Lojas: {', '.join(lojas)}")
        return _ok(f"{m}: " + ", ".join(f"{n} ₽{p}" for n, p in lojas[m]))

    @tool(
        "quem_aprende_hm",
        "Espécies do FireRed que aprendem um HM (CUT, FLY, SURF, STRENGTH, FLASH, ROCK_SMASH, WATERFALL).",
        _esquema({"hm": {"type": "string"}}, ["hm"]),
    )
    async def quem_aprende_hm(args):
        return _ok(", ".join(conhecimento.quem_aprende_hm(args["hm"])) or "ninguém")

    # ---------------- memória ----------------

    @tool(
        "atualizar_memoria",
        "Grava o que você LEU agora no jogo (só os campos lidos). time: equipe na ordem; pc: Pokémon guardados que você "
        "viu; mochila: {item: quantidade}; mochila_completa=true quando leu os três bolsos (itens ausentes viram zero).",
        _esquema(
            {
                "time": {"type": "array", "items": POKEMON},
                "pc": {"type": "array", "items": POKEMON},
                "mochila": {"type": "object", "additionalProperties": {"type": "integer"}},
                "mochila_completa": {"type": "boolean"},
                "insignias": {"type": "array", "items": {"type": "string"}},
                "dinheiro": {"type": "integer"},
                "tempo_jogo": {"type": "string"},
                "pokedex": {"type": "integer"},
            },
            [],
        ),
    )
    async def atualizar_memoria(args):
        if "mochila" in args:
            estado.definir_mochila(args["mochila"], args.get("mochila_completa", False))
        campos = {
            k: v for k, v in args.items() if k in ("time", "pc", "insignias", "dinheiro", "tempo_jogo", "pokedex")
        }
        if "time" in campos:  # o modelo costuma mandar só espécie e nível: golpes e HP já lidos não podem sumir
            velhos = {p["especie"]: p for p in estado.dados["time"]}
            campos["time"] = [{**velhos.get(p["especie"], {}), **p} for p in campos["time"]]
        if campos:
            resumo = ", ".join(
                f"{k}={v}"
                if k not in ("time", "pc")
                else f"{k}=" + "; ".join(f"{p['especie']} nv{p['nivel']}" for p in v)
                for k, v in campos.items()
            )
            antes = set(estado.dados["insignias"])
            estado.atualizar(evento=("leitura", resumo), **campos)
            for nova in set(campos.get("insignias", [])) - antes:
                estado.evento("insignia", f"insígnia {nova} registrada")
        return _ok("memória atualizada")

    @tool(
        "ajustar_item",
        "Soma ou subtrai itens da mochila quando ganhar, comprar, usar ou vender (ex.: delta=-1 ao "
        "usar uma Potion; +5 ao comprar 5 Poké Balls).",
        _esquema(
            {"item": {"type": "string"}, "delta": {"type": "integer"}, "motivo": {"type": "string"}},
            ["item", "delta", "motivo"],
        ),
    )
    async def ajustar_item(args):
        antes, depois = estado.ajustar_item(args["item"], args["delta"], args["motivo"])
        return _ok(f"{args['item']}: {antes} -> {depois}")

    @tool(
        "registrar_evento",
        "Registra no histórico algo que aconteceu: batalha importante (vitória/derrota e contra quem), evento da "
        "história, compra (com o gasto), Pokémon recebido de presente, evolução, treino, troca no PC.",
        _esquema(
            {
                "tipo": {"type": "string", "enum": TIPOS_EVENTO},
                "texto": {"type": "string"},
                "especie": {"type": "string"},
                "nivel": {"type": "integer"},
            },
            ["tipo", "texto"],
        ),
    )
    async def registrar_evento(args):
        if args["tipo"] == "presente" and args.get("especie"):
            estado.registrar_captura(args["especie"], args.get("nivel", 0), "presente: " + args["texto"])
        else:
            estado.evento(args["tipo"], args["texto"])
        if args["tipo"] in ("batalha", "derrota"):
            estado.contar("vitorias" if args["tipo"] == "batalha" else "derrotas")
        return _ok("registrado")

    @tool(
        "anotar",
        "Nota importante para os próximos episódios (o que lembrar, onde parou, próximo passo).",
        _esquema({"texto": {"type": "string"}}, ["texto"]),
    )
    async def anotar(args):
        estado.anotar(args["texto"])
        return _ok("anotado")

    @tool(
        "definir_objetivo",
        "Objetivo atual em uma frase (aparece no painel).",
        _esquema({"objetivo": {"type": "string"}}, ["objetivo"]),
    )
    async def definir_objetivo(args):
        estado.atualizar(objetivo=args["objetivo"], evento=("objetivo", args["objetivo"]))
        return _ok("objetivo definido")

    @tool(
        "definir_plano",
        "Substitui o plano por uma lista ordenada de passos concretos e verificáveis, com o motivo e a "
        "estratégia de longo prazo (aparece no painel e guia o executor entre os planos).",
        _esquema(
            {
                "passos": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "motivo": {"type": "string"},
                "estrategia": {
                    "type": "string",
                    "description": "Time-alvo até a Liga (quem, papel e por quê); quem está atrasado e até que nível treinar "
                    "agora (com escolta); capturas que faltam para o time; uso de itens raros (Rare Candy, "
                    "pedras, TMs) e a próxima luta obrigatória com o que a simulação pede.",
                },
            },
            ["passos", "motivo", "estrategia"],
        ),
    )
    async def definir_plano(args):
        estado.definir_plano(args["passos"], args["motivo"], args["estrategia"])
        return _ok("plano definido")

    @tool(
        "concluir_passo",
        "Marca um passo do plano como feito (número a partir de 1) com o resultado.",
        _esquema(
            {"numero": {"type": "integer", "minimum": 1}, "resultado": {"type": "string"}}, ["numero", "resultado"]
        ),
    )
    async def concluir_passo(args):
        if args["numero"] > len(estado.dados["plano"]):
            return _erro("esse passo não existe")
        estado.concluir_passo(args["numero"], args["resultado"])
        return _ok("passo concluído")

    @tool(
        "pedir_replanejamento",
        "Pede um plano novo ao estrategista quando o atual não serve mais (derrota, "
        "obstáculo, situação nova). Termine o episódio depois.",
        _esquema({"motivo": {"type": "string"}}, ["motivo"]),
    )
    async def pedir_replanejamento(args):
        estado.atualizar(replanejar=True, evento=("replanejar", args["motivo"]))
        return _ok("o próximo episódio começa com o estrategista")

    acoes = [
        ver_tela,
        apertar,
        ir_para,
        empurrar_pedra,
        falar_com,
        avancar_texto,
        lutar,
        ver_golpes,
        fugir,
        abrir_menu_batalha,
        responder,
        enfraquecer_e_capturar,
        capturar,
        trocar_na_batalha,
        abrir_menu,
        ver_time,
        ver_mochila,
        ver_pc,
        ver_pokedex,
        curar,
        salvar,
        guardar_no_pc,
        tirar_do_pc,
        tornar_shiny,
        mudar_ordem,
        usar_item,
        dar_item,
        tirar_item,
        pescar,
        coletar_itens,
        obter_pokemon,
        treinar,
        modo_selvagens,
        comprar,
        vender,
        golpe_novo,
        batalha_automatica,
    ]
    saber = [
        info_mapa,
        onde_encontrar,
        info_pokemon,
        info_treinador,
        desafios,
        analisar_golpes,
        avaliar_golpes,
        decidir_golpe_novo,
        pokemon_faltando,
        avaliar_time,
        preparar_batalha,
        onde_treinar,
        roteiro_,
        detonado,
        loja,
        quem_aprende_hm,
    ]
    memoria = [
        atualizar_memoria,
        ajustar_item,
        registrar_evento,
        anotar,
        definir_objetivo,
        definir_plano,
        concluir_passo,
        concluir_marco,
        pedir_replanejamento,
    ]
    global ULTIMAS
    ULTIMAS = {t.name: t for t in acoes + saber + memoria}  # testes chamam t.handler(args) direto, sem o SDK
    return create_sdk_mcp_server(name=SERVIDOR, version="2.0", tools=acoes + saber + memoria)


ULTIMAS = {}
