"""Gera nomes de caixa a partir do catálogo do CodeGenerator do E-Sh4rk, com parâmetros, sem abrir o site.

Os arquivos do E-Sh4rk (motor js_of_ocaml, códigos de saída e catálogo) não vêm no repositório: são baixados na primeira
vez para dados/gerador/. Precisa do Node.js no PATH.

    nomes = gerar("Start wild battle with any Pokemon", PokemonHex=0xF5, PokemonLV=50)
"""

import json
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

from fireredia import caminhos

MOTOR_URL = "https://e-sh4rk.github.io/CodeGenerator/ace_js.bc.js"
CODIGOS_URL = "https://e-sh4rk.github.io/EmeraldACE_web/files_frlg/"  # exit.txt, list.json e os códigos-fonte
CACHE = caminhos.DADOS / "gerador"
LINGUA, JOGO = "eng10", "fr"  # FireRed inglês do Switch


def _baixar(url, destino, forcar=False):
    if forcar or not destino.exists():
        destino.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=60) as r:
            destino.write_bytes(r.read())
    return destino


def catalogo():
    """[{'name', 'eng10', 'cat', ...}] dos códigos de FireRed/LeafGreen."""
    return json.loads(_baixar(CODIGOS_URL + "list.json", CACHE / "list.json").read_text(encoding="utf-8"))


def fonte(nome):
    """Texto-fonte de um código pelo nome no catálogo ('Make any Pokémon Shiny') ou pelo caminho ('pkmn/x.txt')."""
    if not nome.endswith(".txt"):
        item = next((c for c in catalogo() if c["name"].lower() == nome.lower()), None)
        if item is None or not item.get(LINGUA):
            raise KeyError(f"código {nome!r} não existe no catálogo para {LINGUA}")
        nome = item[LINGUA]
    return _baixar(CODIGOS_URL + nome, CACHE / "codigos" / nome).read_text(encoding="utf-8")


def ajustar(texto, **parametros):
    """Troca o valor das linhas `nome = valor` do cabeçalho, mantendo comentários e marcações (@input, ;, %%)."""
    for nome, valor in parametros.items():
        valor = str(valor)
        texto, n = re.subn(
            rf"^(\s*{re.escape(nome)}\s*\??\s*=\s*)[^;@%\n]*?(\s*(?:[;@%].*)?)$",
            lambda m, v=valor: f"{m.group(1)}{v}{m.group(2)}",
            texto,
            count=1,
            flags=re.M,
        )
        if not n:
            raise KeyError(f"o código não tem o parâmetro {nome!r}")
    return texto


def nomes_de_caixa(saida):
    """Lista de nomes a partir da saída do gerador ('Box  1: / ? U n ...   [/?UnFE3n]')."""
    return [m.group(1) for m in re.finditer(r"^Box\s+\d+:.*\[(.*)\]\s*$", saida, flags=re.M)]


def gerar(nome_ou_arquivo, **parametros):
    """Nomes das caixas (índice 0 = Caixa 1) do código, com os parâmetros dados."""
    node = shutil.which("node")
    if not node:
        raise RuntimeError("o gerador precisa do Node.js no PATH")
    motor = _baixar(MOTOR_URL, CACHE / "ace_js.bc.js")
    saidas = _baixar(CODIGOS_URL + "exit.txt", CACHE / "exit.txt")
    arquivo = Path(nome_ou_arquivo)
    texto = arquivo.read_text(encoding="utf-8") if arquivo.is_file() else fonte(nome_ou_arquivo)
    pronto = CACHE / "ultimo_codigo.txt"
    pronto.write_text(ajustar(texto, **parametros), encoding="utf-8")
    r = subprocess.run(
        [node, str(Path(__file__).with_name("gerador.js")), str(motor), str(saidas), LINGUA, JOGO, str(pronto)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    nomes = nomes_de_caixa(r.stdout)
    if not nomes:
        raise RuntimeError(f"o gerador não devolveu nomes de caixa:\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return nomes
