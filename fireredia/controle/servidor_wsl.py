"""Servidor HTTP no WSL que mantém o Pro Controller emulado (NXBT) e executa macros.

POST /  corpo = macro NXBT (ex.: "A 0.1s\\n0.3s")  -> executa e responde quando terminar
GET  /  -> estado da conexão
Rodar como root: o NXBT precisa controlar o BlueZ.
"""

import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import nxbt

PORTA = 8765
PRAZO_MACRO = 60
# o BlueZ não grava chave do pareamento e esquece o Switch quando a conexão cai; o endereço fica guardado aqui
ENDERECO = Path(__file__).resolve().parents[2] / "memoria" / "switch_endereco.txt"


class Handler(BaseHTTPRequestHandler):
    def _responder(self, codigo, texto):
        self.send_response(codigo)
        self.end_headers()
        self.wfile.write(texto.encode())

    def do_GET(self):
        self._responder(200, nx.state[idx]["state"])

    def do_POST(self):
        macro = self.rfile.read(int(self.headers["Content-Length"])).decode()
        # nx.macro(block=True) espera para sempre se o processo do controle cair
        mid = nx.macro(idx, macro, block=False)
        prazo = time.monotonic() + PRAZO_MACRO
        while True:
            estado = nx.state[idx]
            if mid in estado["finished_macros"]:
                return self._responder(200, "ok")
            if estado["state"] != "connected":
                return self._responder(503, f"controle {estado['state']}: {estado['errors']}")
            if time.monotonic() > prazo:
                nx.stop_macro(idx, mid)
                return self._responder(504, f"macro passou de {PRAZO_MACRO}s")
            time.sleep(1 / 120)


if __name__ == "__main__":
    nx = nxbt.Nxbt()
    enderecos = nx.get_switch_addresses() or ([ENDERECO.read_text().strip()] if ENDERECO.exists() else [])
    print("reconectando em", enderecos or "(nenhum: abra Controles > Alterar empunhadura/ordem no Switch)", flush=True)
    idx = nx.create_controller(nxbt.PRO_CONTROLLER, reconnect_address=enderecos)
    nx.wait_for_connection(idx)
    if nx.state[idx].get("last_connection"):
        ENDERECO.write_text(nx.state[idx]["last_connection"])
    print("conectado; ouvindo na porta", PORTA, flush=True)
    # ponytail: servidor single-thread serializa as macros de propósito — um controle, uma fila
    HTTPServer(("0.0.0.0", PORTA), Handler).serve_forever()
