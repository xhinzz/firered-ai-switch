"""Planejamento puro sobre a grade de colisão (sem tela nem controle): triângulo do Deoxys e gelo deslizante.

Grades são arrays numpy indexados [y, x]; `colisao` verdadeiro = parede. Testável com grades sintéticas.
"""

from collections import deque

DIRECOES = {"CIMA": (0, -1), "BAIXO": (0, 1), "ESQUERDA": (-1, 0), "DIREITA": (1, 0)}

# field_specials.c: posições do triângulo (sDeoxysCoords) e passos permitidos até cada toque (sDeoxysStepCaps)
DEOXYS_POSICOES = [
    (15, 12),
    (11, 14),
    (15, 8),
    (19, 14),
    (12, 11),
    (18, 11),
    (15, 14),
    (11, 14),
    (19, 14),
    (15, 15),
    (15, 10),
]
DEOXYS_PASSOS = [4, 8, 8, 8, 4, 4, 4, 6, 3, 3]


def _livre(colisao, x, y, bloqueado=()):
    h, w = colisao.shape
    return 0 <= x < w and 0 <= y < h and not colisao[y, x] and (x, y) not in bloqueado


def _arvore(colisao, inicio, bloqueado=()):
    """{tile: (anterior, direção)} da busca em largura a pé."""
    pai = {inicio: None}
    fila = deque([inicio])
    while fila:
        s = fila.popleft()
        for d, (vx, vy) in DIRECOES.items():
            n = (s[0] + vx, s[1] + vy)
            if n not in pai and _livre(colisao, *n, bloqueado):
                pai[n] = (s, d)
                fila.append(n)
    return pai


def _rota(pai, alvo):
    passos = []
    while pai[alvo]:
        alvo, d = pai[alvo]
        passos.append(d)
    return passos[::-1]


def plano_deoxys(colisao, inicio=(15, 13), toque=1):
    """[(passos, direção do toque, posição do triângulo)] do toque `toque` ao 10º, ou None.

    O 1º toque é em (15,12), feito de `inicio`. Depois de cada toque o triângulo pula para a próxima posição e o
    jogador tem um limite de passos até tocá-lo de novo; estourar o limite manda o triângulo de volta ao início.
    Busca em profundidade nos quatro lados do triângulo: o lado escolhido decide a distância até o toque seguinte."""
    if toque > 10:
        return []
    triangulo, limite = DEOXYS_POSICOES[toque], DEOXYS_PASSOS[toque - 1]
    pai = _arvore(colisao, inicio, {triangulo})
    for d, (vx, vy) in sorted(DIRECOES.items()):
        lado = (triangulo[0] - vx, triangulo[1] - vy)
        if lado in pai and len(rota := _rota(pai, lado)) <= limite:
            resto = plano_deoxys(colisao, lado, toque + 1)
            if resto is not None:
                return [(rota, d, triangulo)] + resto
    return None


def deslizar(colisao, gelo, pos, d):
    """Onde o jogador para ao andar na direção d: no gelo segue até bater; fora do gelo anda um tile. None se bloqueado."""
    vx, vy = DIRECOES[d]
    x, y = pos[0] + vx, pos[1] + vy
    if not _livre(colisao, x, y):
        return None
    while gelo[y, x] and _livre(colisao, x + vx, y + vy):
        x, y = x + vx, y + vy
    return x, y


def plano_gelo(colisao, gelo, inicio, alvo):
    """Menor sequência de direções (cada uma é um toque: anda ou desliza) de `inicio` até `alvo`, ou None."""
    pai = {inicio: None}
    fila = deque([inicio])
    while fila:
        s = fila.popleft()
        if s == alvo:
            return _rota(pai, alvo)
        for d in DIRECOES:
            n = deslizar(colisao, gelo, s, d)
            if n and n not in pai:
                pai[n] = (s, d)
                fila.append(n)
    return None
