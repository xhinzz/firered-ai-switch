"""Acha texto na tela desenhando a string com a fonte do próprio jogo (folha de glifos, larguras e charmap do pokefirered)."""

import re
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image

from fireredia.mundo import mapa

FONTES = {
    "normal": ("latin_normal.png", "sFontNormalLatinGlyphWidths"),
    "pequena": ("latin_small.png", "sFontSmallLatinGlyphWidths"),
}
ACHOU = 0.9  # medido com luminância: texto presente 1,0; ausente até 0,72


def tem(n, s, regiao=(0, 160, 0, 240)):
    return achar(n, s, regiao)[0] >= ACHOU


@lru_cache
def _charmap():
    pares = re.findall(
        r"^'(.+?)'\s*=\s*([0-9A-F]{2})\s*$", (mapa.RAIZ / "charmap.txt").read_text(encoding="utf-8"), re.M
    )
    return {c.replace("\\'", "'"): int(h, 16) for c, h in pares}  # o apóstrofo vem escapado: '\'' = B4


@lru_cache
def _larguras(fonte="normal"):
    texto = (
        (mapa.RAIZ / "src" / "text.c").read_text(encoding="utf-8", errors="replace")
        if (mapa.RAIZ / "src" / "text.c").exists()
        else _git_show("src/text.c")
    )
    bloco = re.search(rf"{FONTES[fonte][1]}\[\] =\s*\{{(.*?)\}};", texto, re.S)[1]
    return [int(v) for v in re.findall(r"\d+", bloco)]


def _git_show(caminho):
    import subprocess

    return subprocess.run(
        ["git", "-C", str(mapa.RAIZ), "show", f"HEAD:{caminho}"], capture_output=True, check=True
    ).stdout.decode("utf-8", "replace")


@lru_cache
def _folha(fonte="normal"):
    return np.array(Image.open(mapa.RAIZ / "graphics" / "fonts" / FONTES[fonte][0]))


@lru_cache(maxsize=2048)
def desenhar(s, fonte="normal"):
    """Máscara (16 x largura) dos pixels de letra da string na fonte do jogo (normal ou pequena: tela do time)."""
    cm, larg, folha = _charmap(), _larguras(fonte), _folha(fonte)
    celula = 8 if fonte == "pequena" else 16  # a folha pequena tem glifos de 8x16, 32 por linha
    por_linha = folha.shape[1] // celula
    colunas = []
    for ch in s:
        cod = cm.get(ch, cm.get(ch.upper(), 0))
        lin, col = divmod(cod, por_linha)
        w = larg[cod] if cod < len(larg) else 6
        colunas.append(folha[lin * 16 : (lin + 1) * 16, col * celula : col * celula + w] == 1)
    return np.hstack(colunas) if colunas else np.zeros((16, 1), bool)


def achar(n, s, regiao=(0, 160, 0, 240), claro=False, fonte="normal"):
    """(nota 0..1, x, y) do melhor lugar onde a string aparece na tela nativa, procurando só na região (y0, y1, x0, x1).

    claro=True para letra branca com contorno escuro (painéis do PC e da tela do time)."""
    y0, y1, x0, x1 = regiao
    # luminância: pega texto escuro e colorido (item registrado sai azul); sombra cinza clara e fundo ficam de fora
    reg = n[y0:y1, x0:x1].astype(np.float32)
    lum = 0.299 * reg[..., 0] + 0.587 * reg[..., 1] + 0.114 * reg[..., 2]
    # letra branca ~245; o fundo dos painéis claros chega a ~205
    escuro = (lum > 225 if claro else lum < 150).astype(np.float32)
    modelo = desenhar(s, fonte)
    alt = np.flatnonzero(modelo.any(axis=1))
    modelo = modelo[alt[0] : alt[-1] + 1].astype(np.float32) if len(alt) else modelo.astype(np.float32)
    if escuro.shape[0] < modelo.shape[0] or escuro.shape[1] < modelo.shape[1]:
        return 0.0, None, None
    r = cv2.matchTemplate(escuro, modelo, cv2.TM_CCOEFF_NORMED)
    _, nota, _, (x, y) = cv2.minMaxLoc(r)
    return float(nota), x + x0, y + y0


def ler(n, candidatos, regiao, claro=False, fonte="normal"):
    """(nota, candidato) do texto da lista que melhor aparece na região."""
    return max((achar(n, c, regiao, claro, fonte)[0], c) for c in candidatos)


def ler_mais_longo(n, candidatos, regiao, claro=False, fonte="normal"):
    """O candidato mais longo que aparece na região ('THUNDER WAVE' e não 'THUNDER', que também aparece), ou None."""
    achados = [c for c in candidatos if achar(n, c, regiao, claro, fonte)[0] >= ACHOU]
    return max(achados, key=len) if achados else None


def numero(n, regiao, maximo=100, claro=False, fonte="normal"):
    """Número escrito na região (nível, HP): o de mais dígitos que aparece, porque '2' e '3' também aparecem em '23'."""
    achados = [
        (len(str(k)), nota, k)
        for k in range(1, maximo + 1)
        if (nota := achar(n, str(k), regiao, claro, fonte)[0]) >= ACHOU
    ]
    return max(achados)[2] if achados else None


# ---------------- leitura de texto livre (caixas de diálogo e de batalha) ----------------

CARACTERES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?.,'-/:;()&é♂♀…“”‘’"
CAIXA = (108, 160, 4, 236)  # caixa de texto da batalha e do mapa, sem a moldura
ESPACO = 4  # colunas vazias entre duas letras a partir das quais é espaço (letra a letra a folga é 1-2)
CONFIANCA_LETRA = 0.85


@lru_cache(maxsize=2)
def _glifos(fonte="normal"):
    """[(caractere, máscara 16 x largura da tinta)] dos caracteres que aparecem em diálogos."""
    res = []
    for c in CARACTERES:
        if c not in _charmap():
            continue
        m = desenhar(c, fonte)
        cols = np.flatnonzero(m.any(axis=0))
        if len(cols):
            res.append((c, m[:, cols[0] : cols[-1] + 1]))
    return res


def _letra(faixa, x0, x1, glifos):
    """(caractere, largura usada, nota) do glifo que melhor cobre a tinta a partir de x0 (até x1)."""
    melhor = ("?", x1 - x0, 0.0)
    for c, g in glifos:
        w = g.shape[1]
        if w > x1 - x0 + 1:
            continue
        janela = faixa[:, x0 : x0 + w]
        if janela.shape[1] < w:
            continue
        nota = 1.0 - np.logical_xor(janela, g).sum() / max(g.sum() + janela.sum(), 1)
        # empate: o glifo mais largo explica mais tinta ('m' e não 'r' seguido de sobra)
        if nota > melhor[2] + 1e-6 or (abs(nota - melhor[2]) <= 1e-6 and w > melhor[1]):
            melhor = (c, w, nota)
    return melhor


def _ler_linha(faixa, glifos):
    """(texto, nota média) de uma faixa de 16 linhas: corrida de colunas com tinta = letra(s); folga larga = espaço."""
    tinta = faixa.any(axis=0)
    x, fim, saida, notas, vazio = 0, faixa.shape[1], [], [], 0
    while x < fim:
        if not tinta[x]:
            vazio += 1
            x += 1
            continue
        if saida and vazio >= ESPACO:
            saida.append(" ")
        vazio = 0
        x1 = x
        while x1 < fim and tinta[x1]:
            x1 += 1
        c, w, nota = _letra(faixa, x, x1, glifos)
        saida.append(c if nota >= CONFIANCA_LETRA else "?")
        notas.append(nota)
        x += max(w, 1)
    return "".join(saida), (sum(notas) / len(notas) if notas else 0.0)


def _linhas_de(mascara):
    """[(topo, base)] dos blocos de linhas com tinta (cada linha de texto tem 7 a 14 px de tinta)."""
    tem = mascara.sum(axis=1) >= 2
    blocos, y = [], 0
    while y < len(tem):
        if tem[y]:
            y1 = y
            while y1 < len(tem) and (tem[y1] or (y1 + 1 < len(tem) and tem[y1 + 1])):
                y1 += 1
            if 5 <= y1 - y <= 16:
                blocos.append((y, y1))
            y = y1
        y += 1
    return blocos


def legivel(s):
    """Texto de verdade na caixa: chão claro (Power Plant) lido como caixa vira "?????iiii", sem palavra."""
    return bool(re.search(r"[A-HJ-Za-hj-z]{2}", s))


def ler_caixa(n, regiao=CAIXA):
    """Texto da caixa de diálogo ou de batalha ("" se não há texto), lido letra a letra com a fonte do jogo.

    Testa letra clara (batalha, troca) e escura (mapa) e fica com a leitura mais confiável."""
    y0, y1, x0, x1 = regiao
    reg = n[y0:y1, x0:x1].astype(np.float32)
    lum = 0.299 * reg[..., 0] + 0.587 * reg[..., 1] + 0.114 * reg[..., 2]
    glifos, melhor = _glifos(), ("", 0.0)
    for claro in (True, False):
        m = lum > 225 if claro else lum < 150
        m[m.mean(axis=1) > 0.6] = False  # moldura horizontal
        m[:, m.mean(axis=0) > 0.6] = False  # moldura vertical
        m[:, :6] = m[:, -6:] = False  # cantos arredondados da caixa do mapa grudariam nas linhas de texto
        # linha perto da base da região: a janela de 16 px passaria do fim e não casaria com os glifos
        m = np.vstack([m, np.zeros((16, m.shape[1]), bool)])
        linhas, notas = [], []
        for topo, _base in _linhas_de(m):
            # a tinta da letra mais alta começa 1 a 4 px abaixo do topo da célula de 16 px
            texto_, nota = max(
                (_ler_linha(m[t : t + 16], glifos) for t in range(max(topo - 4, 0), topo + 1)), key=lambda r: r[1]
            )
            # cenário vira linha de '?' (nota baixa) ou de '!' (piso listrado da cabine do S.S. Anne): sem letra, fora
            if re.search(r"[A-Za-z0-9]", texto_) and nota >= CONFIANCA_LETRA:
                linhas.append(texto_.strip())
                notas.append(nota)
        nota = sum(notas) / len(notas) if notas else 0.0
        if nota > melhor[1]:
            melhor = ("\n".join(linhas), nota)
    return melhor[0] if melhor[1] >= CONFIANCA_LETRA else ""
