"""Põe a IA para jogar: sobe o controle no WSL, o painel e os episódios (estrategista e executor), até parar.

Uso: python -m fireredia [--restricao "só Pokémon tipo fogo"]
     (o painel faz o mesmo pelo botão Jogar)
"""

import argparse
import asyncio
import ctypes
import logging
import os
import subprocess
import sys
import time

from fireredia import caminhos
from fireredia.agente import cerebro, ferramentas
from fireredia.controle import maos
from fireredia.estado import PASTA, Estado
from fireredia.habilidades import batalha
from fireredia.painel import painel
from fireredia.percepcao import olhos

DISTRO = os.environ.get("WSL_DISTRO", "Ubuntu-22.04")  # NXBT fixa dbus-python 1.2.16: Python 3.10 do 22.04
SERVIDOR = caminhos.RAIZ / "fireredia" / "controle" / "servidor_wsl.py"  # roda no WSL como root
DONGLE = os.environ.get("BLUETOOTH_DONGLE", "0a12:0001")  # VID:PID do adaptador USB repassado ao WSL (usbipd)
USBIPD = r"C:\Program Files\usbipd-win\usbipd.exe"
# estrategista pensa com calma de vez em quando; executor decide em poucos segundos a cada ação
ESTRATEGISTA = ("claude-opus-5-5", "medium")
EXECUTOR = ("claude-sonnet-5-5", "low")
SEM_JANELA = subprocess.CREATE_NO_WINDOW
log = logging.getLogger("jogar")


def _no_wsl(caminho):
    return f"/mnt/{caminho.drive[0].lower()}{caminho.as_posix()[2:]}"


def subir_controle():
    """Garante o Pro Controller emulado conectado; devolve o processo do servidor (None se já estava no ar)."""
    situacao = maos.estado()
    if situacao == "connected":
        return None
    proc = None
    if situacao == "crashed":  # NXBT morreu por dentro e não volta sozinho: derruba o servidor e sobe outro
        log.info("controle travado (crashed): reiniciando o servidor no WSL")
        subprocess.run(
            ["wsl", "-d", DISTRO, "-u", "root", "--", "pkill", "-f", "[s]ervidor_wsl.py"],
            capture_output=True,
            creationflags=SEM_JANELA,
        )
        time.sleep(2)
        situacao = maos.estado()
    if situacao == "offline":
        # o servidor só abre a porta depois de conectar: "offline" também é um servidor preso reconectando, que
        # seguraria o Bluetooth do novo
        subprocess.run(
            ["wsl", "-d", DISTRO, "-u", "root", "--", "pkill", "-f", "[s]ervidor_wsl.py"],
            capture_output=True,
            creationflags=SEM_JANELA,
        )
        log.info("subindo o controle: WSL, adaptador Bluetooth e NXBT")
        subprocess.run(["wsl", "-d", DISTRO, "-u", "root", "--", "true"], capture_output=True, creationflags=SEM_JANELA)
        subprocess.run(
            [USBIPD, "attach", "--wsl", "--hardware-id", DONGLE], capture_output=True, creationflags=SEM_JANELA
        )
        time.sleep(2)  # attach com o dongle já anexado dá erro inofensivo
        saida = open(caminhos.LOGS / "controle.log", "a", encoding="utf-8")  # noqa: SIM115 (fica aberto com o servidor)
        proc = subprocess.Popen(
            ["wsl", "-d", DISTRO, "-u", "root", "--", "python3", "-u", _no_wsl(SERVIDOR)],
            stdout=saida,
            stderr=subprocess.STDOUT,
            creationflags=SEM_JANELA,
        )
    for _ in range(90):
        if maos.estado() == "connected":
            log.info("controle conectado")
            return proc
        if proc and proc.poll() is not None:
            raise RuntimeError("o servidor do controle saiu; veja logs/controle.log")
        time.sleep(1)
    # o controle emulado não acorda o console: com ele dormindo a reconexão nunca fecha
    raise RuntimeError("o controle não conectou em 90 s: o Switch está dormindo ou desligado? Acorde o console")


async def garantir_controle(estado, proc):
    """Insiste no controle até conectar, avisando no painel; devolve o processo do servidor."""
    while True:
        try:
            return await asyncio.to_thread(subir_controle) or proc
        except RuntimeError as exc:
            log.warning("%s; nova tentativa em 60 s", exc)
            estado.atualizar(status="esperando o Switch: acorde o console", evento=("erro", str(exc)))
            await asyncio.sleep(60)


CHAVES = {
    "anthropic": ["ANTHROPIC_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "gemini": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
}


def escolher_modelos():
    """(provedor, {papel: (modelo, esforço)}) do .env: IA_PROVEDOR, IA_MODELO_<PAPEL>, IA_ESFORCO_<PAPEL> ("nenhum" tira)."""

    def falhar(motivo):
        log.error(motivo)  # aberto pelo painel (pythonw) não há console: o motivo fica no jogo.log
        raise SystemExit(motivo)

    provedor = os.environ.get("IA_PROVEDOR", "anthropic").strip().lower()
    if provedor not in CHAVES:
        falhar(f"IA_PROVEDOR={provedor} desconhecido: use anthropic, openai ou gemini")
    padrao = {"estrategista": ESTRATEGISTA, "executor": EXECUTOR} if provedor == "anthropic" else {}
    modelos = {}
    for papel in ("estrategista", "executor"):
        modelo = os.environ.get(f"IA_MODELO_{papel.upper()}") or padrao.get(papel, (None,))[0]
        if not modelo:
            falhar(f"IA_PROVEDOR={provedor}: defina IA_MODELO_{papel.upper()} no .env")
        esforco = os.environ.get(f"IA_ESFORCO_{papel.upper()}", "medium" if papel == "estrategista" else "low")
        modelos[papel] = (modelo, None if esforco.lower() == "nenhum" else esforco)
    chave = next((c for c in CHAVES[provedor] if os.environ.get(c)), None)
    if os.environ.get("ANTHROPIC_WORKSPACE_ID") and not os.environ.get("ANTHROPIC_CUSTOM_HEADERS"):
        # chave da organização (sem workspace) exige o cabeçalho; o Claude Code envia o que estiver nesta variável
        os.environ["ANTHROPIC_CUSTOM_HEADERS"] = f"anthropic-workspace-id: {os.environ['ANTHROPIC_WORKSPACE_ID']}"
    if provedor != "anthropic" and not chave:
        falhar(f"IA_PROVEDOR={provedor}: falta {' ou '.join(CHAVES[provedor])} no .env")
    # anthropic sem chave usa a assinatura do Claude Code (com limite de sessão); com chave, cobrança por uso na API
    log.info(
        "provedor %s (%s): estrategista %s, executor %s",
        provedor,
        "chave de API" if chave else "assinatura do Claude",
        modelos["estrategista"],
        modelos["executor"],
    )
    return provedor, modelos


PARADO_LIMIAR, EPISODIOS_PARADOS = 4, 3  # diferença média da tela (0-255) abaixo da qual o episódio não mexeu no jogo


def _miniatura():
    try:
        return olhos.tela()[::8, ::8].astype("int16")
    except Exception:  # janela do OBS fechada: conta como tela parada
        return None


def _mexeu(antes, depois):
    return antes is not None and depois is not None and abs(depois - antes).mean() >= PARADO_LIMIAR


async def main(args):
    caminhos.carregar_env()
    provedor, modelos = escolher_modelos()
    estado = Estado()
    # monitor desligado (10 min sem uso) estraga a captura do projetor do OBS: imagem achatada e escura.
    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED vale até o processo sair
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000003)
    (PASTA / "jogador.pid").write_text(str(os.getpid()))
    estado.atualizar(
        inicio_sessao=time.time(),
        status="iniciando",
        evento=("sessao", "sessão iniciada"),
        **({"restricao": args.restricao} if args.restricao is not None else {}),
    )
    if painel.iniciar():
        log.info("painel em http://127.0.0.1:%d", painel.PORTA)
    proc = None
    falhas, parados = 0, 0
    try:
        proc = await garantir_controle(estado, proc)
        servidor = ferramentas.criar(estado, batalha.LOC)
        while True:
            antes = await asyncio.to_thread(_miniatura)
            try:
                await cerebro.episodio(estado, servidor, modelos)
                falhas = 0
            except Exception as exc:
                falhas += 1
                espera = min(30 * falhas, 600)  # limite de uso do plano também cai aqui: espera e tenta de novo
                log.exception("episódio falhou; nova tentativa em %d s", espera)
                estado.atualizar(status=f"erro, tentando de novo em {espera} s", evento=("erro", str(exc)[:300]))
                await asyncio.sleep(espera)
            if maos.estado() != "connected":  # Switch dormiu ou o Bluetooth caiu no meio do episódio
                proc = await garantir_controle(estado, proc)
            # imagem com defeito (OBS achatado) ou modelo sem agir: episódio atrás de episódio só gasta. Espera crescente
            parados = 0 if _mexeu(antes, await asyncio.to_thread(_miniatura)) else parados + 1
            if parados >= EPISODIOS_PARADOS:
                espera = min(60 * 2 ** (parados - EPISODIOS_PARADOS), 600)
                log.warning("tela sem mudança em %d episódios seguidos; próximo em %d s", parados, espera)
                estado.atualizar(status=f"pausado {espera} s: a tela não muda há {parados} episódios (imagem do OBS?)")
                await asyncio.sleep(espera)
    except BaseException:
        log.exception("jogador encerrado")  # aberto pelo painel (pythonw) não há console: o motivo fica no jogo.log
        raise
    finally:
        estado.atualizar(status="parado", evento=("sessao", "sessão encerrada"))
        (PASTA / "jogador.pid").unlink(missing_ok=True)
        if proc:
            proc.terminate()


def executar(argv=None):
    p = argparse.ArgumentParser(
        prog="python -m fireredia", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--restricao", help='regra extra para a partida, ex.: "só Pokémon tipo fogo"')
    caminhos.LOGS.mkdir(exist_ok=True)
    saidas = [logging.FileHandler(caminhos.LOGS / "jogo.log", encoding="utf-8")]
    if sys.stderr:  # pythonw (aberto pelo painel) não tem console
        saidas.append(logging.StreamHandler())
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)s %(message)s", datefmt="%H:%M:%S", handlers=saidas
    )
    try:
        asyncio.run(main(p.parse_args(argv)))
    except KeyboardInterrupt:
        log.info("parado pelo usuário")


if __name__ == "__main__":
    executar()
