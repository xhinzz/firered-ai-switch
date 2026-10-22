"""Gera as figuras técnicas da documentação (docs/img) a partir do decomp e das telas em tests/fixtures.

Uso: python scripts/figuras.py
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from fireredia.missoes import deoxys, gelo, planos  # noqa: E402
from fireredia.mundo import mapa  # noqa: E402
from fireredia.percepcao import olhos  # noqa: E402

SAIDA = RAIZ / "docs" / "img"
TILE, BORDA = 16, mapa.BORDA
ESCALA = 3
CORES = ["#ff5252", "#ffb300", "#64dd17", "#00b0ff", "#d500f9", "#ff6d00", "#1de9b6", "#f50057", "#76ff03", "#2979ff"]


def _px(x, y):
    """Canto superior esquerdo do tile (x, y) no desenho do mapa (que tem BORDA tiles de margem)."""
    return (x + BORDA) * TILE, (y + BORDA) * TILE


def _centro(x, y):
    px, py = _px(x, y)
    return px + TILE // 2, py + TILE // 2


def _ampliar(img):
    return img.resize((img.width * ESCALA, img.height * ESCALA), Image.NEAREST)


def localizacao():
    """Tela do Switch | mesmo trecho achado no mapa renderizado do decomp (janela 15x10 tiles em volta do jogador)."""
    quadro = np.array(Image.open(RAIZ / "tests/fixtures/mapa_cerulean_guarda.png").convert("RGB"))
    p = olhos.Localizador().localizar(quadro, global_=True)
    desenho = Image.fromarray(mapa.renderizar_mapa(p.mapa)).convert("RGB")
    jx, jy = _px(p.x, p.y)
    x0, y0 = jx - olhos.JOGADOR_PX[0], jy - olhos.JOGADOR_PX[1]
    recorte = desenho.crop((x0 - 64, y0 - 48, x0 + 240 + 64, y0 + 160 + 48))
    d = ImageDraw.Draw(recorte)
    d.rectangle((64, 48, 64 + 239, 48 + 159), outline="#ffeb3b", width=2)
    d.rectangle((64 + 112, 48 + 72, 64 + 127, 48 + 87), outline="#ff1744", width=2)
    lado = Image.new("RGB", (240 + 16 + recorte.width, recorte.height), "#0d0f13")
    lado.paste(Image.fromarray(quadro), (0, (recorte.height - 160) // 2))
    lado.paste(recorte, (256, 0))
    _ampliar(lado).save(SAIDA / "localizacao.png", optimize=True)
    return p


def plano_deoxys():
    """Os 10 trechos do triângulo da Birth Island sobre o mapa: números nas posições do triângulo, caminho colorido."""
    img = Image.fromarray(mapa.renderizar_mapa(deoxys.MAPA)).convert("RGB")
    d = ImageDraw.Draw(img)
    pos = deoxys.INICIO
    for k, (rota, _, tri) in enumerate(deoxys.plano()):
        pontos = [_centro(*pos)]
        for direcao in rota:
            vx, vy = planos.DIRECOES[direcao]
            pos = (pos[0] + vx, pos[1] + vy)
            pontos.append(_centro(*pos))
        d.line(pontos, fill=CORES[k], width=3)
        tx, ty = _px(*tri)
        d.rectangle((tx + 2, ty + 2, tx + TILE - 3, ty + TILE - 3), outline=CORES[k], width=2)
    x0, y0 = _px(9, 6)
    x1, y1 = _px(22, 17)
    _ampliar(img.crop((x0, y0, x1, y1))).save(SAIDA / "plano_deoxys.png", optimize=True)


def plano_gelo():
    """Os 4 deslizes do B1F da Icefall Cave até a escada da HM07."""
    mapa_id = "MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F"
    img = Image.fromarray(mapa.renderizar_mapa(mapa_id)).convert("RGB")
    colisao, superficie = gelo.grades(mapa_id)
    d = ImageDraw.Draw(img)
    pos = (16, 9)
    for k, direcao in enumerate(planos.plano_gelo(colisao, superficie, pos, (17, 13))):
        novo = planos.deslizar(colisao, superficie, pos, direcao)
        d.line([_centro(*pos), _centro(*novo)], fill=CORES[k], width=4)
        pos = novo
    x0, y0 = _px(12, 1)
    x1, y1 = _px(23, 18)
    _ampliar(img.crop((x0, y0, x1, y1))).save(SAIDA / "plano_gelo.png", optimize=True)


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    print("localização:", localizacao())
    plano_deoxys()
    plano_gelo()
    print("figuras em", SAIDA)
