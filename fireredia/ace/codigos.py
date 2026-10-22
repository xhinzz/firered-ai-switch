"""Nomes de caixa (Caixas 1-11) gerados pelo CodeGenerator do E-Sh4rk para FireRed inglês do Switch (eng10).

Índice 0 = Caixa 1. Caracteres especiais: “ ” ‘ ’ … ♂ ♀ estão na página de símbolos do teclado; o gerador escreve o
hífen como – (U+2013) e o apóstrofo como ’, que se digitam nas teclas - e '. Para gerar outros: fireredia.ace.gerador.
"""

GIFT_VENUSAUR = [
    "/?UnFE3n",
    "AAAa“9q",
    "AA’K.o",
    "AgU?n",
    "VH?n F!q",
    "AAA F.o",
    "AA–R!s",
    "A–R!s",
    "–R!sFI?n",
    "AAA FRn",
    "AA–R!s",
    "A",
    "A",
]
GIFT_BLASTOISE = [
    "/?UnFE3n",
    "AAAa“9q",
    "AA’K.o",
    "AzU?n",
    "RU?n0U?n",
    "AAAVH?n",
    "AA F!q",
    "A F.o",
    "–R!s–R!s",
    "AAA–R!s",
    "AAFI?n",
    "A FRn",
    "–R!s",
]
LER_PID = ["B6.op9/n", "AAAAE/n", "AAsHfq", "A”KQm", "rHfq’KQm", "AAAqHfq", "AA,KQm", "ApHfq", "/KQm", " FoHIoor", "xn"]
SHINY = ["C.kn5 9n", "Q.oDIhn", "AAVS?n", "A2F?n", "A", "E.o mEn3", "QoTzCs", "AFYCn", "6…/q", " FoTB9Ma", ".o"]
# leitura do campo de IVs (igual para os dois: PID % 24 = 13)
LER_IVEA = [
    "BM\u2026oo9Bn",
    "\u2013/n3E/n",
    "AARHfp",
    "ATSfr",
    "DQQmTSfr",
    "AAA\u2026RQm",
    "AATSfr",
    "A\u2019RQm",
    "TSfr\u2640RQm",
    "AAA  .oa",
    ".o",
]
# IVs 31 na Caixa 10 slot 19 (pid, otid = pid depois do shiny, IVEA lido)
IVS_VENUSAUR = [
    "4CUn\u2018Ggm",
    "AAA2R?n",
    "AAhURn",
    "A\u2018GQm",
    "FJloZ\u201c!n",
    "AAA F!q",
    "A",
    "A",
    "A",
    "A",
    "A",
    "A",
    "A",
]
IVS_BLASTOISE = [
    "4CUn\u2018Ggm",
    "AAA0R?n",
    "AAlFRn",
    "A0FRn",
    "\u2018GQmFJlo",
    "AAAZ\u201c!n",
    "AA F!q",
    "A",
    "A",
    "A",
    "A",
    "A",
    "A",
]
# Get any item (vai para o último espaço do PC de itens): RARE CANDY x150 e MASTER BALL x5; diferem só nas caixas 2, 3, 5
ITEM_CANDY = [
    "xFUnDRRn",
    "AAA1\u2026.o",
    "AA\u2026\u201dQn",
    "A\u2640BRm",
    "p\u201c.o\u2026\u201d!n",
    "AAA\u2019BRm",
    "A",
    "A",
    "A",
    "AAA  .oa",
    ".o",
]
ITEM_MASTER = [
    "xFUnDRRn",
    "AAAB\u201c.o",
    "AA3\u201cQn",
    "A\u2640BRm",
    "V\u201d.o\u2026\u201dQn",
    "AAA\u2019BRm",
    "A",
    "A",
    "A",
    "AAA  .oa",
    ".o",
]
# Start wild battle with any Pokémon (Theocatic/final), nv 50, NPC 2 = senhor do Centro de Viridian; diferem só na caixa 4
WILD_SUICUNE = [
    "/?UnFE3n",
    "AAAa“9q",
    "AANK.o",
    "AwR?n",
    "7T?ndG?n",
    "AAA F!q",
    "AA.M.o",
    "AFQ?n",
    "–R!s",
    "AAA  .oa",
    ".o",
]
WILD_ENTEI = WILD_SUICUNE[:3] + ["AvR?n"] + WILD_SUICUNE[4:]
WILD_RAIKOU = WILD_SUICUNE[:3] + ["AuR?n"] + WILD_SUICUNE[4:]


CODIGOS = {nome: valor for nome, valor in dict(globals()).items() if nome.isupper() and isinstance(valor, list)}
