"""Caminhos do projeto num lugar só: dados versionados, decomp baixado, memória e logs da campanha."""

import os
import sys
from pathlib import Path

# no .exe (PyInstaller) __file__ aponta para a pasta temporária; os dados ficam ao lado do executável
RAIZ = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent

DADOS = RAIZ / "dados"
MODELOS = DADOS / "modelos"
MEMORIA = RAIZ / "memoria"  # estado da campanha (não versionado)
LOGS = RAIZ / "logs"


def carregar_env(arquivo=RAIZ / ".env"):
    """CHAVE=valor do .env local para o ambiente; o que já está definido no ambiente vale mais."""
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        chave, _, valor = linha.strip().partition("=")
        if chave and not chave.startswith("#") and valor.strip():
            os.environ.setdefault(chave.strip(), valor.strip().strip("\"'"))


carregar_env()  # antes de qualquer módulo ler MAOS_URL, CAMERA_OBS, CLAUDE_CLI ou as chaves de API
DECOMP = Path(
    os.environ.get("FIRERED_DECOMP", DADOS / "pokefirered")
)  # clone do pret/pokefirered (scripts/baixar_decomp.py)
