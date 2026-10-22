"""Cérebro: episódios do Claude Agent SDK em dois papéis — o estrategista monta o plano, o executor joga seguindo o plano.

A memória entre episódios fica no estado (memoria/); cada episódio recebe o resumo dela e mantém o contexto pequeno.
"""

import asyncio
import json
import logging
import os
import time

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)

from fireredia import caminhos
from fireredia.agente import ferramentas, provedores
from fireredia.habilidades import piloto
from fireredia.mundo import conhecimento, mapa, roteiro

log = logging.getLogger("cerebro")
# CLI do Claude Code usado pelo Agent SDK; sem CLAUDE_CLI vale o que vem com o SDK ou o do PATH
CLI = os.environ.get("CLAUDE_CLI")
TURNOS = {"estrategista": 30, "executor": 60}  # episódio curto mantém o contexto (cheio de imagens) pequeno
REPLANEJAR_A_CADA = 4  # episódios do executor sem passar pelo estrategista
PARADO_A_CADA = 2  # episódios do executor sem nenhum passo concluído: o plano provavelmente envelheceu

COMUM = """\
Você faz parte de uma IA que joga Pokémon FireRed (versão em inglês) num Nintendo Switch de verdade, sozinha, sem \
nenhuma ajuda humana. Meta final: vencer a Elite dos 4 e o Campeão, seguindo a história, capturando espécies novas e \
mantendo um time forte. Ninguém responde perguntas: decida e aja como um jogador experiente de FireRed.

Como enxergar e agir
- Toda ferramenta de ação devolve a tela depois de agir (GBA 240x160 ampliado) e, no mapa, sua posição (mapa, x, y). \
Coordenadas são tiles dos dados do jogo (ids como MAP_VIRIDIAN_CITY). Numa tela simples 480x320 cada tile tem 32 px e \
você ocupa as colunas 224-255 e linhas 144-175: um ponto (X, Y) fica no tile (x + floor(X/32) - 7, y + floor((Y-144)/32)).
- Prefira as ferramentas de alto nível (ir_para, falar_com, curar, salvar, ver_time, ver_mochila, ver_pc, \
guardar_no_pc, tirar_do_pc, mudar_ordem, usar_item, pescar, coletar_itens, obter_pokemon, treinar, avancar_texto, lutar, \
capturar, trocar_na_batalha, fugir, responder). Use apertar só em menus sem ferramenta própria (loja, TM, golpe novo).
- Dados do jogo, sem chute: info_mapa (portas, NPCs, treinadores e alcance de visão, itens, selvagens), onde_encontrar, \
info_pokemon, info_treinador, desafios (líderes e Liga com níveis), loja (o que cada Poké Mart vende e o preço), \
quem_aprende_hm, roteiro (história em marcos), avaliar_time e onde_treinar.
- Uma ação de jogo por resposta: cada uma muda a tela e a próxima decisão depende da imagem que ela devolve.
- Todo resultado traz o texto lido na caixa de diálogo ou de batalha ("texto na tela: ..."). Leia e entenda: o que \
o NPC disse, o que o jogo está pedindo, por que algo não deu certo. Os diálogos ficam no histórico.
- Se vier "ATENÇÃO: nada mudou", pare de repetir: descreva para si o que a tela mostra, pense no que um jogador faria \
(apertar A em vez de B, sair de um menu, outro caminho, falar com alguém) e tente algo diferente. As rotinas \
automáticas devolvem a vez quando não reconhecem a situação; aí a decisão é sua.

Interface do FireRed
- START: POKéDEX, POKéMON, BAG, nome do jogador (cartão de treinador: dinheiro e insígnias), SAVE, OPTION, EXIT. O cursor \
lembra a última posição.
- Mochila com 3 bolsos trocados com ESQUERDA/DIREITA: ITEMS (Potion, Antidote, Repel, Escape Rope...), KEY ITEMS (Bike, \
TM CASE com TMs e HMs, varas de pesca...), POKé BALLS. Nunca conclua que falta um item olhando um bolso só: use ver_mochila.
- Poké Mart: comprar {{item: quantidade}} e vender {{item: quantidade}} dentro da loja fazem tudo (balcão, lista, \
quantidade conferida na tela) e já atualizam mochila e dinheiro. Cada loja tem estoque próprio e fixo (loja mostra o \
de cada uma; Great Ball a partir de Lavender, Ultra Ball em Fuchsia). Guarde uma reserva de dinheiro.
- Centro Pokémon: curar faz tudo. PC: guardar_no_pc e tirar_do_pc (leem nome e nível na tela e atualizam a memória). \
Time tem no máximo 6; captura com time cheio vai para o PC. Lendário ou mítico capturado: leve-o ao time e use \
tornar_shiny num Centro.
- Ordem do time: mudar_ordem (o primeiro entra na batalha). Itens fora da batalha: usar_item (POTION, RARE CANDY, \
REPEL, pedras de evolução, BICYCLE para andar mais rápido); item para segurar (EXP. SHARE): dar_item; tirar o item ou a carta (MAIL) de alguém: tirar_item. Pesca: pescar com a vara, de frente para a água.
- TM/HM: BAG > KEY ITEMS > TM CASE > escolha > USE > Pokémon; com 4 golpes, escolha qual esquecer. Os HMs (HM01 a HM08) ficam no TOPO da lista do TM CASE, antes do TM01 (o jogo os põe primeiro): suba até o topo para achá-los.
- Golpe novo ("Delete a move to make room for Y?"): golpe_novo decide pela nota e cobertura e executa sozinho \
(aprende esquecendo o pior, ou recusa) e atualiza o time na memória. O piloto já faz isso nas batalhas dele.
- Ao planejar o time, use avaliar_golpes em cada Pokémon: mostra golpes fracos ou repetidos, falta de cobertura contra \
o próximo líder, o que vem nos próximos níveis e quais TMs valem a pena.
- Evolução: deixe acontecer, a não ser que haja motivo para segurar (B durante a animação cancela).
- Golpes de campo e a insígnia que libera cada um: FLASH Boulder, CUT Cascade, FLY Thunder, STRENGTH Rainbow, SURF \
Soul, ROCK SMASH Marsh, WATERFALL Volcano. Quando alguém do time sabe CUT, ROCK SMASH ou SURF e a insígnia já foi \
ganha, o ir_para usa sozinho (corta a árvore, quebra a pedra, entra e sai da água). STRENGTH (empurrar pedras) e \
FLASH (cavernas escuras) você usa pelo menu do Pokémon.
- HM recebido (CUT no S.S. Anne, FLASH com o assistente do Oak, SURF e STRENGTH na Safari Zone/Fuchsia, FLY na \
Rota 16): decida quem aprende com quem_aprende_hm e avaliar_golpes, de preferência quem não perde um golpe \
importante, ensine pelo TM CASE e registre o novo golpe com atualizar_memoria.
- FLY: no mapa, START > POKéMON > quem sabe FLY > FLY > escolha a cidade no mapa da região (só cidades já \
visitadas). Use para voltar a lugares com espécies que faltam e para curar rápido.

Batalha
- Selvagens no caminho o ir_para resolve sozinho (piloto): espécie que falta é enfraquecida e capturada; as outras \
fogem (modo_selvagens fugir) ou viram treino (treinar). Treinador comum que te vê no caminho também: o piloto \
identifica, simula e luta pela tabela de tipos (troca e Potion incluídas). Se você mesmo começar uma luta de \
treinador comum (falar_com), use batalha_automatica. Você decide líder, rival, Elite dos 4, chefe, luta dupla e \
o que o piloto devolver (ele explica o porquê).
- Contra cada oponente novo, analisar_golpes antes de escolher (tabela de tipos do jogo; não confie de cabeça: aço \
é fraco a fogo, pedra e terra resistem a fogo...). Leia HP e nível na tela. Não chute a ordem dos golpes: use \
ver_golpes se não estiver na memória. Para trocar de Pokémon no meio da luta: trocar_na_batalha.
- De treinador não dá para fugir.

Time forte (como um jogador hardcore)
- Rode avaliar_time ao planejar: mostra o nível alvo do próximo líder, a nota de cada Pokémon pela forma final e pelos \
tipos até a Liga, o time sugerido (seus e os que dá para capturar agora, com mapa e nível), quem é peso morto e onde \
treinar. Monte o time com isso: capture os bons que estão perto, guarde no PC os inúteis (casulos, linhas fracas, \
tipos repetidos) quando precisar da vaga, e tire do PC quem voltou a servir.
- Nunca coloque um Pokémon de nível muito baixo para lutar sozinho contra selvagens ou treinadores bem mais fortes. \
Para subir um fraco que vale a pena: treinar com ele em 'alvos' e o mais forte do time de 'escolta' (ele começa a \
batalha e a escolta entra no 1º turno; a experiência é dividida), no lugar que avaliar_time/onde_treinar indicar. \
Se capturar um da mesma linha num nível bem maior sai mais barato que treinar, capture.
- Lutas obrigatórias (rival, líder, chefe Rocket, Elite dos 4): rode preparar_batalha antes. Só entre com VENCE com \
folga. Com PERDE ou NO LIMITE, prepare primeiro com o que a simulação aponta: treinar quem ela diz (até o nível \
indicado, com escolta), capturar quem vence o adversário que te derruba, trocar golpes (avaliar_golpes, TMs), levar \
Potions. Depois simule de novo. O rival intercepta em lugares fixos (ponte ao norte de Cerulean, S.S. Anne, Pokémon \
Tower, Silph Co., Rota 22): não pise lá antes de estar pronto. Derrota custa metade do dinheiro e o caminho de volta.
- Golpes: o Pokémon pode estar com os mesmos golpes há muito tempo. Confira com avaliar_golpes ao planejar (golpes \
fracos ou repetidos, o que aprende nos próximos níveis, TMs da mochila) e troque quando valer a pena.

Mundo
- Itens: em todo mapa novo (e ao voltar com HM nova), coletar_itens pega tudo que falta, inclusive escondidos.
- Pokémon de NPC (presente, compra como o Magikarp da Rota 4, troca, prêmio): obter_pokemon. Eles contam na Pokédex.
- História: roteiro mostra os marcos e o que liberam. Quando um marco acontecer de verdade, concluir_marco: os \
caminhos que a história fecha (guardas de Saffron, Snorlax, Cycling Road, Rota 23) só abrem para o ir_para depois.
- Detonado: ao planejar e ao chegar a uma área nova, leia a seção com detonado (passo a passo, o que bloqueia o \
caminho até quando, lutas obrigatórias, itens escondidos, NPCs, Pokémon da área, quebra-cabeças). Siga a ordem dele e \
não saia de uma área deixando para trás o que um jogador 100% pegaria.

Pokédex (meta permanente, como um jogador completista)
- Capture pelo menos um de cada espécie que ainda não está em "Pokédex capturados" no resumo. Selvagem que falta: \
use enfraquecer_e_capturar (lê o HP, calcula o golpe que tira vida sem derrubar e só joga a bola quando a chance é \
boa). Se ele disser que nenhum golpe é seguro, troque para um Pokémon mais fraco ou use sono/paralisia e tente de novo.
- Nunca deixe de capturar uma espécie nova por pressa. Só não capture se não houver bolas: aí anote e compre na \
próxima loja. Mantenha 10 ou mais bolas (Great Ball quando a loja vender).
- Evolução também registra na Pokédex. Rode ver_pokedex se a leitura estiver velha ou depois de evoluções.
- "What? X is evolving!": NUNCA aperte B (cancela a evolução). Use avancar_texto, que espera a animação. Se uma \
evolução for cancelada, ela volta a acontecer no próximo nível.
- Com o time cheio, a captura vai para o PC sozinha; decida no Centro quem fica no time.
- HP baixo: troque, use poção ou cure no Centro. Time todo desmaiado volta ao último Centro e perde metade do dinheiro.
- Nunca: soltar Pokémon (RELEASE), apagar o save, trocar ou batalhar online, gastar todo o dinheiro.

Memória (você só sabe o que vier no resumo; o histórico guarda tudo)
- ver_time, ver_pc e ver_pokedex leem a tela e gravam sozinhos. Mochila, dinheiro, insígnias e tempo que você ler: \
atualizar_memoria. Item ganho, comprado ou vendido: ajustar_item (usar_item e as bolas já descontam). Batalha \
importante, compra, presente, evolução, evento da história: registrar_evento. Decisão que importa depois: anotar.
{restricao}"""

ESTRATEGISTA = (
    COMUM
    + """

Seu papel neste episódio: ESTRATEGISTA. Entenda a situação real e monte o plano que o executor vai seguir.
1. O resumo diz se time e mochila estão ATUAIS (a memória se atualiza pelo texto das batalhas e o código relê sozinho \
a cada 30 min): só use ver_time/ver_mochila no que estiver DESATUALIZADO ou depois de algo que a memória não \
acompanha. ver_pc quando estiver num Centro e o PC nunca tiver sido lido. Confira o roteiro e marque com \
concluir_marco o que já aconteceu e ainda não está marcado.
2. Pense como um jogador experiente:
   - Próximo marco da história (roteiro) e o que ele exige (desafios, info_treinador, HMs, itens-chave).
   - Time: avaliar_time. Quem fica, quem vai para o PC, quem capturar e onde, quem treinar (alvos e escolta), onde \
e até que nível. Nada de levar um nível 4 para apanhar de um nível 15.
   - Pokédex: pokemon_faltando (o que dá para capturar agora e onde; o que ficou liberado por HM, vara ou insígnia \
nova) e obter_pokemon para os de NPC. Planeje capturar tudo no caminho e voltar (com FLY quando tiver) aos lugares \
liberados. Garanta bolas suficientes.
   - Itens: coletar_itens em cada mapa novo do caminho.
   - HMs: quem do time vai aprender cada HM, sem estragar o time principal.
   - O que comprar e onde (loja): bolas, Potions, Repels, curas de status.
   - Riscos: PP baixo, status, mochila sem cura.
3. definir_plano com 4 a 12 passos concretos e verificáveis, em ordem, cada um com meta clara. Exemplos: "Comprar 10 \
POKé BALL e 5 POTION no MAP_PEWTER_CITY_MART (~3500)"; "Capturar ODDISH nv 13+ na MAP_ROUTE24"; "guardar_no_pc WEEDLE e \
RATTATA"; "treinar alvos ODDISH 20 escolta CHARMELEON na MAP_ROUTE24"; "Vencer MISTY (Starmie 21) com ODDISH nv 20+". \
Motivo em uma ou duas frases.
   A 'estrategia' do definir_plano é o que o executor e o painel leem entre um plano e outro: o time-alvo até a Liga \
(quem e por quê), quem está atrasado e até que nível treinar agora, capturas que faltam para o time, como usar \
itens raros e o que a próxima luta obrigatória pede. Experiência se distribui: o mais forte escolta, os atrasados \
lutam (treinar com alvos e escolta); Rare Candy vai para quem está atrasado ou para uma evolução-chave, não para \
quem já está no nível. Plano velho (meta já atingida, passos que a história já passou) é refeito do zero.
4. definir_objetivo e anotar o raciocínio que importa. Não execute o plano: termine depois de definir."""
)

EXECUTOR = (
    COMUM
    + """

Seu papel neste episódio: EXECUTOR. Siga o plano do resumo, passo a passo, jogando rápido, dentro da estratégia.
- Antes de agir, confira o plano contra o resumo (níveis do time, marcos, mochila, local): passo que já está \
cumprido (ex.: a meta de nível já foi passada) recebe concluir_passo na hora, com o que aconteceu. Ao terminar um \
passo, concluir_passo com o resultado. Se um passo ficar impossível, sem sentido ou houver um caminho melhor \
(derrota, obstáculo, oportunidade), pedir_replanejamento e termine o episódio.
- Treino é do time, não só do mais forte: selvagem e treinador servem para subir quem está atrasado (treinar com \
alvos e escolta), como a estratégia mandar.
- Decida com o que a tela já mostra, sem olhar de novo à toa. Faça progresso real. Não abra time nem mochila só \
para conferir: o resumo diz se a memória está ATUAL.
- Termine o episódio depois de um marco ou de umas 40 ações: antes, salvar e anotar onde está e o próximo passo."""
)


def _faltam_por_perto(d):
    """Selvagens do mapa atual e dos vizinhos por divisa que ainda não estão na Pokédex."""
    if not d.get("local"):
        return "?"
    atual = d["local"]["mapa"]
    tem = set(d.get("pokedex_capturados") or [])
    linhas = []
    for m in [atual] + [viz for _, viz, _, _ in mapa.conexoes(atual)]:
        faltam = sorted(
            {
                (e, met, a, b, c)
                for met, esp in mapa.selvagens().get(m, {}).items()
                for e, (a, b, c) in esp.items()
                if e not in tem
            },
            key=lambda r: -r[4],
        )
        if faltam:
            linhas.append(f"  {m}: " + ", ".join(f"{e} ({met} nv {a}-{b}, {c}%)" for e, met, a, b, c in faltam))
    return "\n".join(linhas) or "  nada que falte por aqui"


def _pedido(d, n, papel):
    def lista(itens, fmt, vazio="  (nada)"):
        return "\n".join(fmt(i) for i in itens) or vazio

    def pkm(p):
        hp = p.get("hp")
        hp = f"{hp:.0%}" if isinstance(hp, float) else f"{hp if hp is not None else '?'}/{p.get('hp_max', '?')}"
        return (
            f"  {p.get('apelido') or p['especie']} ({p['especie']}) nv {p['nivel']} HP {hp}"
            f"{' ' + p['status'] if p.get('status') else ''} | golpes: {', '.join(p.get('golpes') or []) or '?'}"
        )

    treino = d.get("treino") or {}
    m_atual = d["local"] and d["local"]["mapa"]
    fora, golpes = d.get("itens_fora") or {}, ",".join(sorted(conhecimento.capacidades(d["time"], d["insignias"])))
    itens_aqui = (
        [
            i["item"]
            for i in conhecimento.itens_dos_mapas().get(m_atual, [])
            if (k := f"{m_atual}:{i['x']},{i['y']}") not in set(d.get("itens_coletados") or [])
            and fora.get(k) != golpes
        ]
        if m_atual
        else []
    )
    proximos_marcos = roteiro.texto(d.get("marcos") or {}).splitlines()[0]

    def ha(ts):
        return f"há {int((time.time() - ts) // 60)} min" if ts else "nunca"

    batalhas = d.get("batalhas_desde_leitura", 0)
    velho = (
        not d.get("time_lido_ts")
        or time.time() - d["time_lido_ts"] > piloto.TIME_VELHO_S
        or batalhas >= piloto.BATALHAS_VELHO
    )
    frescor_time = (
        f"lido na tela {ha(d.get('time_lido_ts'))}, {batalhas} batalha(s) depois; nível, golpe aprendido, "
        f"evolução, PP e HP se atualizam pelo texto das batalhas: "
        + ("DESATUALIZADO, use ver_time" if velho else "ATUAL, não precisa reler")
    )
    frescor_mochila = f"lida na tela {ha(d.get('mochila_lido_ts'))}, ajustada a cada compra, uso e captura: " + (
        "DESATUALIZADA, use ver_mochila"
        if not d.get("mochila_lido_ts") or time.time() - d["mochila_lido_ts"] > piloto.MOCHILA_VELHA_S
        else "ATUAL"
    )
    prox = roteiro.proximo_marco(d.get("marcos") or {})
    secoes = ", ".join(f"{a} ({t.splitlines()[0].lstrip('# ')})" for a, t in roteiro.detonado(prox or "")) + (
        " — leia com detonado" if prox and roteiro.detonado(prox) else ""
    )
    marco, ids = conhecimento.proxima_luta(d.get("marcos") or {}, [p["especie"] for p in d["time"] + d["pc"]])
    luta = "nenhuma liberada"
    if ids and d["time"]:
        t = conhecimento.treinadores()[ids[0]]
        venceu, folga, _ = conhecimento.simular_batalha(d["time"], t["time"])
        veredito = (
            "VENCE com folga" if venceu and folga >= conhecimento.FOLGA else "VENCE NO LIMITE" if venceu else "PERDE"
        )
        luta = (
            f"{marco} ({t['classe']} {t['nome']}): simulação com o time atual: {veredito} (detalhes: preparar_batalha)"
        )

    plano = lista(
        enumerate(d["plano"], 1),
        lambda ip: (
            f"  {ip[0]}. [{'x' if ip[1]['feito'] else ' '}] {ip[1]['passo']}"
            + (f" -> {ip[1]['resultado']}" if ip[1]["resultado"] else "")
        ),
        "  (sem plano)",
    )
    importantes = [e for e in d["eventos"] if e["tipo"] not in ("acao", "mapa")][-20:]
    local = d["local"] and f"{d['local']['mapa']} ({d['local']['x']},{d['local']['y']})"
    capturados = ", ".join(f"{c['especie']}" for c in d["capturados"]) or "nenhum registrado"
    return f"""Episódio {n} — papel: {papel.upper()}.
Objetivo: {d["objetivo"] or "(nenhum)"}
Metas do dono da partida (sempre valem; o plano e a estratégia devem incluí-las no momento certo):
{lista(d.get("metas") or [], lambda m: f"  - {m}", "  (nenhuma)")}
Estratégia (do estrategista; guia as decisões entre os passos): {d.get("estrategia") or "(nenhuma ainda)"}
Plano ({d["plano_motivo"] or "sem motivo registrado"}):
{plano}
Último local: {local or "?"}
Roteiro: {proximos_marcos} (feitos: {", ".join(d.get("marcos") or {}) or "nenhum marcado"})
Próxima luta obrigatória: {luta}
Detonado do próximo marco: {secoes or "sem seção (use info_mapa e roteiro)"}
Itens ainda não pegos neste mapa: {", ".join(itens_aqui) or "nenhum"}{" (coletar_itens)" if itens_aqui else ""}
Selvagens: {d.get("modo_selvagens", "fugir")} | treino: {json.dumps(treino.get("alvos") or {}, ensure_ascii=False)} escolta {treino.get("escolta") or "-"}
Insígnias: {", ".join(d["insignias"]) or "nenhuma registrada"} | dinheiro: {d["dinheiro"]} | tempo de jogo: {d["tempo_jogo"] or "?"} | Pokédex: {d["pokedex"]}
Golpes de campo utilizáveis agora: {", ".join(sorted(conhecimento.capacidades(d["time"], d["insignias"]))) or "nenhum"}
Mochila ({frescor_mochila}): {json.dumps(d["mochila"], ensure_ascii=False) if d["mochila"] else "desconhecida: use ver_mochila"}
Time ({frescor_time}):
{lista(d["time"], pkm, "  (desconhecido: use ver_time)")}
PC (lido em {d.get("pc_lido_em") or "nunca"}): {", ".join(f"{p['especie']} nv{p['nivel']}" for p in d["pc"]) or ("vazio" if d.get("pc_lido_em") else "? (use ver_pc num Centro)")}
Capturados pela IA nesta partida: {capturados}
Pokédex (lida em {d.get("pokedex_lida_em") or "nunca: use ver_pokedex"}): {len(d.get("pokedex_capturados") or [])} capturados: {", ".join(d.get("pokedex_capturados") or []) or "?"}
Vistos mas ainda não capturados: {", ".join(v for v in d.get("pokedex_vistos") or [] if v not in (d.get("pokedex_capturados") or [])) or "?"}
Selvagens por perto que FALTAM na Pokédex (capture com enfraquecer_e_capturar):
{_faltam_por_perto(d)}
Contadores: {json.dumps(d["contadores"], ensure_ascii=False)}
Eventos importantes recentes:
{lista(importantes, lambda e: f"  [{e['t']}] {e['tipo']}: {e['texto'][:200]}")}
Diário:
{lista(d["diario"][-15:], lambda e: f"  [{e['t']}] {e['texto']}")}
Últimas ações:
{lista(d["acoes"][-8:], lambda a: f"  {a['t']} {a['f']}: {a['r']}")}

{"Analise e defina o plano." if papel == "estrategista" else "Continue jogando pelo plano."}"""


def papel_do_episodio(d):
    plano = d["plano"]
    sem_planejar = d["episodios"] - d.get("ultimo_plano_ep", 0)
    parado = sem_planejar >= PARADO_A_CADA and not any(p["feito"] for p in plano)
    if d["replanejar"] or not plano or all(p["feito"] for p in plano) or sem_planejar >= REPLANEJAR_A_CADA or parado:
        return "estrategista"
    return "executor"


async def _episodio_outro(provedor, estado, n, papel, sistema, pedido, modelo, esforco):
    """Episódio com GPT ou Gemini pelo laço de provedores.py; registra pensamento, chamadas e tokens como o de Claude."""
    if provedor not in provedores.EPISODIOS:
        raise RuntimeError(f"IA_PROVEDOR={provedor} desconhecido (use anthropic, openai ou gemini)")

    def pensar(texto):
        estado.atualizar(pensamento=texto[:800], evento=("decisao", texto))
        log.info("IA: %s", texto[:300])

    def chamar(nome, args):
        log.info("-> %s %s", nome, json.dumps(args, ensure_ascii=False)[:160])

    turnos, entra, sai = await provedores.EPISODIOS[provedor](
        sistema, pedido, modelo, esforco, TURNOS[papel], pensar, chamar
    )
    estado.contar("tokens_entrada", entra)
    estado.contar("tokens_saida", sai)
    log.info(
        "episódio %d (%s, %s %s): %d turnos, %d tokens de entrada e %d de saída",
        n,
        papel,
        provedor,
        modelo,
        turnos,
        entra,
        sai,
    )


async def episodio(estado, servidor, modelos):
    """modelos = {"estrategista": (modelo, esforço), "executor": (modelo, esforço)}"""
    relido = await asyncio.to_thread(piloto.manutencao, estado)  # varredura só quando a memória envelheceu
    if relido:
        log.info("memória relida antes do episódio: %s", ", ".join(relido))
    d = estado.foto()
    n = d["episodios"] + 1
    papel = papel_do_episodio(d)
    modelo, esforco = modelos[papel]
    campos = {"episodios": n, "status": "jogando", "modelo": f"{papel}: {modelo}"}
    if papel == "estrategista":
        campos["ultimo_plano_ep"] = n
    estado.atualizar(evento=("episodio", f"episódio {n} ({papel}, {modelo})"), **campos)
    restricao = f"\nRegra extra desta partida: {d['restricao']}" if d["restricao"] else ""
    sistema = (ESTRATEGISTA if papel == "estrategista" else EXECUTOR).format(restricao=restricao)
    provedor = os.environ.get("IA_PROVEDOR", "anthropic").strip().lower()
    if provedor != "anthropic":
        await _episodio_outro(provedor, estado, n, papel, sistema, _pedido(d, n, papel), modelo, esforco)
        return
    opcoes = ClaudeAgentOptions(
        system_prompt=sistema,
        model=modelo,
        effort=esforco,
        cli_path=CLI,
        cwd=str(caminhos.RAIZ),
        # sem isso o CLI carrega CLAUDE.md, skills e MCPs pessoais do usuário no jogador
        setting_sources=[],
        strict_mcp_config=True,
        skills=[],
        tools=[],
        mcp_servers={ferramentas.SERVIDOR: servidor},
        permission_mode="bypassPermissions",
        max_turns=TURNOS[papel],
        max_buffer_size=16 * 1024 * 1024,  # resultado com imagens passa fácil do 1 MB padrão
        env={"CLAUDE_AGENT_SDK_CLIENT_APP": "firered-ia/0.2"},
        stderr=lambda linha: log.debug("cli: %s", linha),
    )
    async with ClaudeSDKClient(options=opcoes) as cliente:
        await cliente.query(_pedido(d, n, papel))
        async for msg in cliente.receive_response():
            if isinstance(msg, AssistantMessage):
                for bloco in msg.content:
                    if isinstance(bloco, TextBlock) and bloco.text.strip():
                        texto = bloco.text.strip()
                        estado.atualizar(pensamento=texto[:800], evento=("decisao", texto))
                        log.info("IA: %s", texto[:300])
                    elif isinstance(bloco, ToolUseBlock):
                        log.info(
                            "-> %s %s", bloco.name.split("__")[-1], json.dumps(bloco.input, ensure_ascii=False)[:160]
                        )
            elif isinstance(msg, ResultMessage):
                custo = msg.total_cost_usd or 0
                estado.atualizar(custo_usd=round(estado.foto()["custo_usd"] + custo, 4))
                log.info(
                    "episódio %d (%s): %s em %d turnos, equivalente a US$ %.3f",
                    n,
                    papel,
                    msg.subtype,
                    msg.num_turns,
                    custo,
                )
                if msg.is_error and msg.subtype != "error_max_turns":
                    raise RuntimeError(f"episódio terminou com erro: {msg.subtype} {msg.result or ''}")
