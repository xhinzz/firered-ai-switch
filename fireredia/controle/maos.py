"""Mãos: manda botões ao Pro Controller emulado (controle/servidor_wsl.py rodando no WSL)."""

import os
import urllib.error
import urllib.request

import fireredia.caminhos  # noqa: F401  (carrega o .env: MAOS_URL)


def _url():
    # 127.0.0.1 e não localhost: localhost tenta IPv6 antes e custa 2 s por chamada. MAOS_URL=http://<IP do WSL>:8765/
    # quando o encaminhamento do localhost do WSL quebra (o servidor responde dentro do WSL e não fora)
    return os.environ.get("MAOS_URL", "http://127.0.0.1:8765/")


BOTOES = {
    "A": "A",
    "B": "B",
    "L": "L",
    "R": "R",
    "START": "PLUS",
    "SELECT": "MINUS",
    "CIMA": "DPAD_UP",
    "BAIXO": "DPAD_DOWN",
    "ESQUERDA": "DPAD_LEFT",
    "DIREITA": "DPAD_RIGHT",
}


def macro(texto, prazo=90.0):
    try:
        with urllib.request.urlopen(urllib.request.Request(_url(), data=texto.encode()), timeout=prazo) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"controle HTTP {e.code}: {e.read().decode()}") from None


def estado():
    try:
        with urllib.request.urlopen(_url(), timeout=3) as r:
            return r.read().decode()
    except OSError:
        return "offline"


def apertar(*botoes, segurar=0.08, pausa=0.12):
    # abaixo de ~50 ms o jogo perde toque (medido: 7/8 com 33 ms, 8/8 com 50 ms)
    macro("\n".join(f"{BOTOES[b]} {segurar}s\n{pausa}s" for b in botoes))


def andar(direcao, segundos, correr=True):
    """Segura a direção (e B, para correr) pelo tempo dado."""
    macro(f"{BOTOES[direcao]}{' B' if correr else ''} {segundos:.3f}s\n0.03s")
