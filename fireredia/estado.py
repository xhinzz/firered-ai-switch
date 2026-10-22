"""Memória da partida: estado atual (memoria/estado.json) e histórico completo só de acréscimo (memoria/eventos.jsonl).

O estado é o que se sabe agora (time, mochila com quantidades, plano...). O histórico guarda o caminho inteiro:
cada decisão, plano, batalha, captura, item ganho ou gasto, mapa visitado. Nada do histórico é apagado.
"""

import json
import re
import threading
import time

from fireredia import caminhos

PASTA = caminhos.MEMORIA
ARQUIVO = PASTA / "estado.json"
EVENTOS = PASTA / "eventos.jsonl"
PADRAO = {
    "status": "parado",
    "modelo": "",
    "episodios": 0,
    "acoes_total": 0,
    "custo_usd": 0.0,
    "objetivo": "",
    "restricao": "",
    "pensamento": "",
    "plano": [],
    "plano_motivo": "",
    "estrategia": "",
    "metas": [],
    "replanejar": True,
    "local": None,
    "time": [],
    "pc": [],
    "pc_lido_em": "",
    "capturados": [],
    "pokedex_capturados": [],
    "pokedex_vistos": [],
    "pokedex_lida_em": "",
    "visitados": [],
    "itens_coletados": [],
    "marcos": {},
    "modo_selvagens": "fugir",
    "mochila": {},
    "mochila_lida_em": "",
    "dinheiro": None,
    "insignias": [],
    "tempo_jogo": "",
    "pokedex": None,
    "contadores": {},
    "diario": [],
    "acoes": [],
    "eventos": [],
}
MAX_ACOES, MAX_DIARIO, MAX_EVENTOS_RECENTES = 60, 300, 150


def agora():
    return time.strftime("%d/%m %H:%M:%S")


class Estado:
    def __init__(self):
        self._trava = threading.Lock()
        PASTA.mkdir(exist_ok=True)
        salvo = json.loads(ARQUIVO.read_text(encoding="utf-8")) if ARQUIVO.exists() else {}
        self.dados = {**PADRAO, **salvo}
        if isinstance(self.dados["mochila"], str):  # versão anterior guardava texto livre
            self.dados["mochila"] = {}
        self.inicio_sessao = time.time()

    def _salvar(self):
        tmp = ARQUIVO.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.dados, ensure_ascii=False, indent=1), encoding="utf-8")
        for tentativa in range(20):
            try:
                tmp.replace(ARQUIVO)
                return
            except PermissionError:  # painel lendo o arquivo no mesmo instante: o Windows não troca arquivo aberto
                if tentativa == 19:
                    raise
                time.sleep(0.05)

    def _evento(self, tipo, texto, dados):
        """Chamar com a trava: grava no histórico permanente e na lista recente do painel."""
        e = {
            "t": agora(),
            "ep": self.dados["episodios"],
            "tipo": tipo,
            "texto": texto,
            "local": self.dados["local"],
            **dados,
        }
        with EVENTOS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
        self.dados["eventos"] = (self.dados["eventos"] + [e])[-MAX_EVENTOS_RECENTES:]

    def evento(self, tipo, texto, **dados):
        with self._trava:
            self._evento(tipo, texto, dados)
            self._salvar()

    def contar(self, chave, n=1):
        with self._trava:
            self.dados["contadores"][chave] = self.dados["contadores"].get(chave, 0) + n
            self._salvar()

    def atualizar(self, evento=None, **campos):
        """Troca campos do estado; com evento=(tipo, texto) também registra no histórico."""
        with self._trava:
            self.dados.update(campos)
            if evento:
                self._evento(*evento, {})
            self._salvar()

    def acao(self, ferramenta, resumo):
        with self._trava:
            self.dados["acoes"] = (
                self.dados["acoes"] + [{"t": time.strftime("%H:%M:%S"), "f": ferramenta, "r": resumo[:240]}]
            )[-MAX_ACOES:]
            self.dados["acoes_total"] += 1
            self._evento("acao", f"{ferramenta}: {resumo}", {})
            self._salvar()

    def anotar(self, texto):
        with self._trava:
            self.dados["diario"] = (self.dados["diario"] + [{"t": agora(), "texto": texto}])[-MAX_DIARIO:]
            self._evento("nota", texto, {})
            self._salvar()

    # --- mochila: quantidades exatas, ajustadas a cada uso e conferidas a cada leitura ---

    @staticmethod
    def _chave_item(nome):
        return nome.strip().upper().replace("É", "E").replace("é", "E")

    def definir_mochila(self, itens: dict, completa: bool):
        """Leitura da mochila: completa=True substitui tudo; False só atualiza os itens informados."""
        with self._trava:
            lidos = {self._chave_item(k): int(v) for k, v in itens.items()}
            antes = dict(self.dados["mochila"])
            novo = lidos if completa else {**antes, **lidos}
            self.dados["mochila"] = {k: v for k, v in novo.items() if v > 0}
            self.dados["mochila_lida_em"] = agora()
            if completa:
                self.dados["mochila_lido_ts"] = time.time()
            mudou = {k: (antes.get(k, 0), v) for k, v in novo.items() if antes.get(k, 0) != v}
            if completa:
                mudou |= {k: (q, 0) for k, q in antes.items() if k not in novo}
            if mudou:
                self._evento(
                    "mochila",
                    "leitura da mochila: " + ", ".join(f"{k} {a}->{b}" for k, (a, b) in mudou.items()),
                    {"mudancas": mudou},
                )
            self._salvar()

    def ajustar_item(self, nome, delta, motivo):
        with self._trava:
            k = self._chave_item(nome)
            antes = self.dados["mochila"].get(k, 0)
            depois = max(antes + delta, 0)
            if depois:
                self.dados["mochila"][k] = depois
            else:
                self.dados["mochila"].pop(k, None)
            self._evento("item", f"{k} {antes}->{depois} ({motivo})", {"item": k, "delta": delta})
            self._salvar()
            return antes, depois

    # --- Pokémon ---

    def registrar_captura(self, especie, nivel, como):
        with self._trava:
            reg = {
                "especie": especie.upper(),
                "nivel": nivel,
                "quando": agora(),
                "local": (self.dados["local"] or {}).get("mapa"),
                "como": como,
            }
            self.dados["capturados"].append(reg)
            if len(self.dados["time"]) >= 6:  # time cheio: o jogo manda a captura para o PC
                self.dados["pc"] = self.dados["pc"] + [{"especie": reg["especie"], "nivel": nivel}]
            self.dados["contadores"]["capturas"] = self.dados["contadores"].get("capturas", 0) + 1
            for lista in ("pokedex_capturados", "pokedex_vistos"):
                if reg["especie"] not in self.dados[lista]:
                    self.dados[lista].append(reg["especie"])
            self.dados["pokedex"] = len(self.dados["pokedex_capturados"]) or self.dados["pokedex"]
            self._evento("captura", f"{especie.upper()} nv {nivel} ({como})", reg)
            self._salvar()

    # --- plano do estrategista ---

    def definir_plano(self, passos, motivo, estrategia=""):
        with self._trava:
            self.dados["plano"] = [{"passo": p, "feito": False, "resultado": ""} for p in passos]
            self.dados["plano_motivo"] = motivo
            if estrategia:
                self.dados["estrategia"] = estrategia
            self.dados["replanejar"] = False
            self._evento(
                "plano",
                motivo + " | " + " / ".join(f"{i + 1}. {p}" for i, p in enumerate(passos)),
                {"passos": passos, "estrategia": estrategia},
            )
            self._salvar()

    def marco_concluido(self, marco, resultado):
        """Registra o marco, marca os passos do plano que o citam e pede plano novo (o contexto da história mudou)."""
        with self._trava:
            self.dados["marcos"] = {**self.dados["marcos"], marco: {"quando": agora(), "resultado": resultado}}
            for p in self.dados["plano"]:
                if not p["feito"] and re.search(rf"\b{re.escape(marco)}\b", p["passo"]):
                    p["feito"], p["resultado"] = True, f"marco {marco}: {resultado}"
            self.dados["replanejar"] = True
            self._evento("historia", f"marco {marco} concluído: {resultado}", {"marco": marco})
            self._salvar()

    def concluir_passo(self, numero, resultado):
        with self._trava:
            p = self.dados["plano"][numero - 1]
            p["feito"], p["resultado"] = True, resultado
            self._evento("passo", f"passo {numero} concluído: {p['passo']} -> {resultado}", {"numero": numero})
            self._salvar()

    def foto(self):
        with self._trava:
            return {**json.loads(json.dumps(self.dados)), "sessao_s": int(time.time() - self.inicio_sessao)}


def ler_disco():
    """Estado como está no disco (para o painel rodando fora do processo do jogador)."""
    try:
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return dict(PADRAO)
