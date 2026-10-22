"""Painel (http://127.0.0.1:8770): memória da partida lida do disco, tela ao vivo, sprites oficiais e liga/desliga da IA.

Sobe junto com a IA (python -m fireredia) ou sozinho na janela (python -m fireredia.painel.app). Também serve como fonte
de navegador no OBS.
"""

import ctypes
import io
import json
import re
import subprocess
import sys
import threading
import time
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import numpy as np
from PIL import Image

from fireredia import caminhos, estado
from fireredia.mundo import conhecimento, roteiro
from fireredia.mundo.mapa import RAIZ
from fireredia.percepcao import olhos

PORTA = 8770
GRAFICOS = RAIZ / "graphics"
PID = estado.PASTA / "jogador.pid"
PYTHON = Path(sys.executable).with_name("pythonw.exe")  # sem janela de console


# ---------------- sprites oficiais (gráficos do pokefirered com a paleta certa) ----------------


def _pal(caminho):
    return np.array(caminho.read_text().split()[3:], dtype=np.uint8).reshape(-1, 3)


def _rgba(png, pal=None):
    """PNG indexado do jogo -> RGBA com a cor 0 transparente; sem .pal usa a paleta embutida (vira .gbapal no build)."""
    im = Image.open(png)
    idx = np.array(im)
    cores = _pal(pal) if pal and pal.exists() else np.array(im.getpalette()[:48], np.uint8).reshape(-1, 3)
    rgba = np.zeros((*idx.shape, 4), np.uint8)
    rgba[..., :3] = cores[idx % len(cores)]
    rgba[..., 3] = np.where(idx % 16 == 0, 0, 255)
    buf = io.BytesIO()
    Image.fromarray(rgba).save(buf, "PNG")
    return buf.getvalue()


def _pasta_especie(nome):
    n = nome.upper().replace("♀", "_F").replace("♂", "_M").replace(".", "").replace("'", "").replace("-", "_")
    return re.sub(r"[\s_]+", "_", n).strip("_").removeprefix("SPECIES_").lower()


@lru_cache(maxsize=512)
def sprite_pokemon(nome):
    pasta = GRAFICOS / "pokemon" / _pasta_especie(nome)
    return _rgba(pasta / "front.png", pasta / "normal.pal") if (pasta / "front.png").exists() else None


@lru_cache
def _arquivo_item():
    """nome do item como aparece no jogo (normalizado) -> nome do arquivo do ícone"""
    res = {}
    for item_id, (nome, _, _) in conhecimento.itens().items():
        res[estado.Estado._chave_item(nome)] = item_id.removeprefix("ITEM_").lower()
    return res


@lru_cache(maxsize=512)
def sprite_item(nome):
    arq = _arquivo_item().get(estado.Estado._chave_item(nome))
    png = arq and GRAFICOS / "items" / "icons" / f"{arq}.png"
    return _rgba(png, GRAFICOS / "items" / "icon_palettes" / f"{arq}.pal") if png and png.exists() else None


@lru_cache(maxsize=64)
def sprite_treinador(pic):
    png = GRAFICOS / "trainers" / "front_pics" / f"{pic}_front_pic.png"
    return _rgba(png, GRAFICOS / "trainers" / "palettes" / f"{pic}.pal") if png.exists() else None


@lru_cache
def sprite_insignias():
    return _rgba(GRAFICOS / "trainer_card" / "badges.png")


# ---------------- processo do jogador ----------------


def _vivo(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    codigo = ctypes.c_ulong()
    ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(codigo))
    ctypes.windll.kernel32.CloseHandle(h)
    return codigo.value == 259  # STILL_ACTIVE


def jogador_pid():
    try:
        pid = int(PID.read_text())
    except (OSError, ValueError):
        return None
    return pid if _vivo(pid) else None


def iniciar_jogador():
    if jogador_pid():
        return "já está jogando"
    subprocess.Popen(
        [str(PYTHON), "-m", "fireredia"],
        cwd=caminhos.RAIZ,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    return "iniciando"


def parar_jogador():
    pid = jogador_pid()
    if not pid:
        return "não estava jogando"
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)  # leva junto o Claude Code filho
    d = estado.ler_disco()
    if d.get("status") != "parado":
        d["status"] = "parado"
        (estado.ARQUIVO).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return "parado"


# ---------------- dados para a página ----------------


def foto_estado():
    d = estado.ler_disco()
    d["jogador_rodando"] = bool(jogador_pid())
    d["sessao_s"] = int(time.time() - d["inicio_sessao"]) if d.get("inicio_sessao") and d["jogador_rodando"] else 0
    d["proximo_lider"] = conhecimento.proximo_lider(d.get("insignias") or [])
    d["kanto"] = [conhecimento.numero_nacional()[i] for i in range(1, 152)]
    feitos = d.get("marcos") or {}
    d["roteiro"] = [
        {"id": i, "desc": desc, "feito": i in feitos, "pronto": all(r in feitos for r in req)}
        for i, desc, _, req, _ in roteiro.MARCOS
    ]
    d["itens_total"] = sum(len(v) for v in conhecimento.itens_dos_mapas().values())
    d.pop("acoes", None)
    return d


def ultimos_eventos(n):
    try:
        linhas = estado.EVENTOS.read_text(encoding="utf-8").splitlines()[-n:]
    except OSError:
        return []
    return [json.loads(linha) for linha in linhas if linha.strip()]


_tela = {"t": 0.0, "png": b""}
_trava_tela = threading.Lock()


def tela_png():
    with _trava_tela:
        if time.monotonic() - _tela["t"] > 0.5:
            ultima = olhos.ultima_tela
            n = ultima[1] if ultima and time.monotonic() - ultima[0] < 0.7 else olhos.tela()
            buf = io.BytesIO()
            Image.fromarray(n).save(buf, "PNG")
            _tela.update(t=time.monotonic(), png=buf.getvalue())
        return _tela["png"]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def _enviar(self, corpo, tipo, codigo=200, cache=False):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", "max-age=86400" if cache else "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def _json(self, obj):
        self._enviar(json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        url = urlparse(self.path)
        partes = [unquote(p) for p in url.path.strip("/").split("/")]
        try:
            if url.path == "/estado":
                return self._json(foto_estado())
            if url.path == "/eventos":
                return self._json(ultimos_eventos(int(parse_qs(url.query).get("n", ["300"])[0])))
            if url.path == "/tela.png":
                return self._enviar(tela_png(), "image/png")
            if partes[0] == "sprite" and len(partes) == 3:
                tipo, nome = partes[1], partes[2].removesuffix(".png")
                png = {"pokemon": sprite_pokemon, "item": sprite_item, "treinador": sprite_treinador}.get(
                    tipo, lambda _: None
                )(nome)
                if tipo == "insignias":
                    png = sprite_insignias()
                return self._enviar(png, "image/png", cache=True) if png else self._enviar(b"", "text/plain", 404)
            return self._enviar(Path(__file__).with_name("painel.html").read_bytes(), "text/html; charset=utf-8")
        except Exception as exc:  # janela do OBS fechada, arquivo sendo gravado: a página tenta de novo
            return self._enviar(str(exc).encode(), "text/plain; charset=utf-8", 503)

    def do_POST(self):
        acoes = {"/jogador/iniciar": iniciar_jogador, "/jogador/parar": parar_jogador}
        if self.path in acoes:
            return self._json({"resultado": acoes[self.path]()})
        self._enviar(b"", "text/plain", 404)


def iniciar(porta=PORTA):
    """Sobe o servidor numa thread; devolve None se a porta já está em uso (outro painel já serve a mesma memória)."""
    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
    except OSError:
        return None
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


if __name__ == "__main__":
    if not iniciar():
        raise SystemExit(f"porta {PORTA} em uso: o painel já está aberto")
    print(f"painel em http://127.0.0.1:{PORTA}")
    threading.Event().wait()
