"""Testes offline: lógica pura roda em qualquer lugar; o que lê o decomp (mapas, fonte do jogo) pula sem ele."""

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from fireredia import caminhos

FIXTURES = Path(__file__).parent / "fixtures"

requer_decomp = pytest.mark.skipif(
    not (caminhos.DECOMP / "data" / "maps").is_dir(),
    reason="decomp ausente: python scripts/baixar_decomp.py",
)


def quadro(nome):
    """Tela nativa 240x160 RGB capturada do Switch durante a campanha."""
    return np.array(Image.open(FIXTURES / f"{nome}.png").convert("RGB"))
