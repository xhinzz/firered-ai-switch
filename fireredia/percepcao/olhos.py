"""Olhos: captura o OBS (câmera virtual ou janela de projetor), recorta a tela do GBA e diz o que há nela."""

import ctypes
import ctypes.wintypes as w
import dataclasses
import os
import struct
import threading
import time
from dataclasses import dataclass
from functools import lru_cache

import cv2
import numpy as np

from fireredia import caminhos
from fireredia.mundo import mapa
from fireredia.percepcao import texto

u, g = ctypes.windll.user32, ctypes.windll.gdi32
u.SetProcessDPIAware()
for f in (u.GetDC, g.CreateCompatibleDC, g.CreateCompatibleBitmap, g.SelectObject):
    f.restype = ctypes.c_void_p
u.GetDC.argtypes = [w.HWND]
u.ReleaseDC.argtypes = [w.HWND, ctypes.c_void_p]
u.PrintWindow.argtypes = [w.HWND, ctypes.c_void_p, w.UINT]
g.CreateCompatibleDC.argtypes = [ctypes.c_void_p]
g.CreateCompatibleBitmap.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
g.SelectObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
g.GetDIBits.argtypes = [ctypes.c_void_p, ctypes.c_void_p, w.UINT, w.UINT, ctypes.c_void_p, ctypes.c_void_p, w.UINT]
g.DeleteObject.argtypes = g.DeleteDC.argtypes = [ctypes.c_void_p]

# começo do título da janela de projetor do OBS: "Projetor" no OBS em português, "Windowed Projector" em inglês
TITULO = os.environ.get("OBS_PROJETOR", "Projetor")
PW_CLIENTONLY_RENDERFULLCONTENT = 3  # sem o RENDERFULLCONTENT janela renderizada por GPU sai preta
# Área do GBA dentro do projetor (FireRed do Switch, escala 8,66x em 2560x1440), em frações da janela
RECORTE = (241 / 2560, 8 / 1440, 2320 / 2560, 1394 / 1440)
JOGADOR_PX = (112, 72)  # canto do tile do jogador na tela nativa 240x160
CONFIANCA = 0.75  # no mapa esperado; perto de divisa o certo cai para ~0,77
# perto da última posição: chão quadriculado com 4 NPCs (ginásio de Fuchsia) dá 0,74 no tile certo
CONFIANCA_PERTO = 0.70
CONFIANCA_OUTRO = 0.85  # mapa inesperado: caverna escura casou 0,83 com o interior de um Centro Pokémon
CERTO = 0.95  # o encaixe certo dá 0,98-0,99: acima disso não precisa comparar com os vizinhos
# Pokémon Tower 3F-7F (WEATHER_FOG_HORIZONTAL): com névoa o encaixe certo dá 0,42-0,46 e os outros andares até 0,30;
# dividir por isto põe a nota na mesma escala dos limites acima
NEBLINA_ESCALA = 0.45
NEBLINA_CLARA = 190  # média do menor canal: névoa 208-225, telas normais até ~155
AZUL_BATALHA = np.array([28, 76, 101])


def _achar_janela():
    achadas = []

    def cb(h, _):
        n = u.GetWindowTextLengthW(h)
        b = ctypes.create_unicode_buffer(n + 1)
        u.GetWindowTextW(h, b, n + 1)
        if b.value.startswith(TITULO):
            achadas.append(h)
        return True

    u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, w.HWND, w.LPARAM)(cb), 0)
    if not achadas:
        raise RuntimeError("janela de projetor do OBS não encontrada (botão direito na prévia > Projetor em janela)")
    return achadas[0]


# ponytail: índice DirectShow fixo da "OBS Virtual Camera" (aqui o DroidCam vem antes); trocar por busca pelo nome se
# a ordem dos dispositivos mudar. CAMERA_OBS=-1 desliga e volta para a janela do projetor
CAMERA_OBS = int(os.environ.get("CAMERA_OBS", "2"))


class _Camera:
    """Lê a câmera virtual do OBS numa thread e guarda o último quadro: não depende de monitor nem de janela."""

    def __init__(self):
        self.quadro, self.instante = None, 0.0
        threading.Thread(target=self._ler, daemon=True).start()

    def _ler(self):
        cap = None
        while True:
            if cap is None:
                cap = cv2.VideoCapture(
                    CAMERA_OBS, cv2.CAP_DSHOW, [cv2.CAP_PROP_FRAME_WIDTH, 1920, cv2.CAP_PROP_FRAME_HEIGHT, 1080]
                )
                if not cap.isOpened():  # câmera virtual parada no OBS
                    cap = None
                    time.sleep(5)
                    continue
            ok, q = cap.read()
            if ok:
                self.quadro, self.instante = q, time.monotonic()
            else:
                cap.release()
                cap = None
                time.sleep(2)

    def ultimo(self):
        """Último quadro RGB, ou None sem quadro novo ou com a câmera parada no OBS (ele manda o próprio logo)."""
        if self.quadro is None or time.monotonic() - self.instante > 1.0:
            return None
        q = self.quadro[:, :, ::-1]
        mini = cv2.resize(q, (32, 18), interpolation=cv2.INTER_AREA).astype(np.int16)
        return None if np.abs(mini - _logo_obs()).mean() < 10 else q


@lru_cache
def _logo_obs():
    return np.load(caminhos.DADOS / "obs_camera_parada.npy").astype(np.int16)


_camera = None


def capturar():
    """Quadro do OBS, RGB. O projetor num monitor paisagem grande é a captura calibrada pixel a pixel; sem ele (monitor
    principal desligado põe o projetor em pé, ou janela fechada) vale a câmera virtual."""
    global _camera
    try:
        janela = capturar_janela()
    except RuntimeError:
        janela = None
    if janela is not None and janela.shape[1] >= 1800 and abs(janela.shape[1] / janela.shape[0] - CANVAS) < 0.05:
        return janela
    if CAMERA_OBS >= 0:
        if _camera is None:
            _camera = _Camera()
            fim = time.monotonic() + 3
            while _camera.ultimo() is None and time.monotonic() < fim:
                time.sleep(0.05)
        q = _camera.ultimo()
        if q is not None:
            return q
    if janela is None:
        raise RuntimeError("sem imagem do OBS: abra o projetor da prévia ou inicie a câmera virtual")
    return janela


def capturar_janela():
    """Janela do projetor inteira, RGB."""
    h = _achar_janela()
    r = w.RECT()
    u.GetClientRect(h, ctypes.byref(r))
    lw, lh = r.right, r.bottom
    hdc = u.GetDC(h)
    mdc = g.CreateCompatibleDC(hdc)
    bmp = g.CreateCompatibleBitmap(hdc, lw, lh)
    g.SelectObject(mdc, bmp)
    try:
        u.PrintWindow(h, mdc, PW_CLIENTONLY_RENDERFULLCONTENT)
        buf = ctypes.create_string_buffer(lw * lh * 4)
        bmi = ctypes.create_string_buffer(struct.pack("<IiiHHIIiiII", 40, lw, -lh, 1, 32, 0, 0, 0, 0, 0, 0), 64)
        g.GetDIBits(mdc, bmp, 0, lh, buf, bmi, 0)
        return np.frombuffer(buf, np.uint8).reshape(lh, lw, 4)[:, :, 2::-1]
    finally:
        g.DeleteObject(bmp)
        g.DeleteDC(mdc)
        u.ReleaseDC(h, hdc)


_trava = threading.Lock()
ultima_tela = None  # (instante, quadro): o painel reaproveita em vez de capturar de novo


CANVAS = 16 / 9  # o projetor centraliza o quadro 16:9 do OBS com barras pretas quando a janela tem outro formato


def recortar(a):
    """Tela do GBA (240x160) dentro da captura da janela do projetor, de qualquer tamanho e formato.

    Com o monitor 2560x1440 desligado o Windows leva o projetor ao monitor 1080x1920 em pé: o quadro vira uma faixa
    no meio da janela e as frações fixas pegavam a faixa achatada com as barras."""
    H, W = a.shape[:2]
    cw, ch = (W, W / CANVAS) if W / H < CANVAS else (H * CANVAS, H)
    ox, oy = (W - cw) / 2, (H - ch) / 2
    x0, x1 = round(ox + RECORTE[0] * cw), round(ox + RECORTE[2] * cw)
    y0, y1 = round(oy + RECORTE[1] * ch), round(oy + RECORTE[3] * ch)
    return cv2.resize(np.ascontiguousarray(a[y0:y1, x0:x1]), (240, 160), interpolation=cv2.INTER_AREA)


def tela():
    """Tela do GBA na resolução nativa 240x160, RGB."""
    global ultima_tela
    with _trava:  # ferramentas e painel capturam de threads diferentes
        n = recortar(capturar())
        ultima_tela = (time.monotonic(), n)
        return n


def assentar(minimo=0.4, prazo=3.0):
    """Espera a tela parar de mudar (fades, animações de menu) e devolve o quadro."""
    time.sleep(minimo)
    anterior, fim = tela(), time.monotonic() + prazo
    while time.monotonic() < fim:
        time.sleep(0.12)
        n = tela()
        if np.abs(n.astype(np.int16) - anterior).mean() < 1.5:
            return n
        anterior = n
    return anterior


def _branco(reg, minimo=200):
    return (reg.min(axis=2) > minimo).mean()


def _cor(reg, cor, tol=30):
    return (np.abs(reg.astype(int) - cor).max(axis=2) < tol).mean()


@lru_cache(maxsize=512)
def _sprite_frente(especie):
    """(RGB, máscara) da sprite oficial de frente, ou None."""
    pasta = mapa.RAIZ / "graphics" / "pokemon" / especie.lower()
    if not (pasta / "front.png").exists():
        return None
    from PIL import Image

    idx = np.array(Image.open(pasta / "front.png"))
    cores = np.array((pasta / "normal.pal").read_text().split()[3:], dtype=np.uint8).reshape(-1, 3)
    return cores[idx % 16], ((idx % 16) != 0).astype(np.uint8)


@lru_cache(maxsize=512)
def _sprite_costas(especie):
    pasta = mapa.RAIZ / "graphics" / "pokemon" / especie.lower()
    if not (pasta / "back.png").exists():
        return None
    from PIL import Image

    # só a metade de cima: a de baixo fica escondida atrás da caixa de texto da batalha
    idx = np.array(Image.open(pasta / "back.png"))[:34]
    cores = np.array((pasta / "normal.pal").read_text().split()[3:], dtype=np.uint8).reshape(-1, 3)
    return cores[idx % 16], ((idx % 16) != 0).astype(np.uint8)


IDENTIFICOU = 0.98  # espécie certa deu 0,994-0,996; sem Pokémon na tela o melhor chute (Ditto) fica em ~0,95


def identificar_meu(n, candidatas):
    """(espécie, nota) do nosso Pokémon em campo pela sprite de costas (embaixo à esquerda)."""
    return _identificar(n[36:116, 0:150], candidatas, _sprite_costas)


def identificar_inimigo(n, candidatas):
    """(espécie, nota) do Pokémon inimigo na batalha pela sprite oficial (área de cima à direita). Nota alta = certeza."""
    return _identificar(n[0:90, 120:240], candidatas, _sprite_frente)


@lru_cache(maxsize=512)
def _sprite_resumo(especie):
    """O resumo mostra a sprite de frente espelhada (CH'DING: 0,997 espelhada, 0,84 normal)."""
    s = _sprite_frente(especie)
    return s and (np.ascontiguousarray(s[0][:, ::-1]), np.ascontiguousarray(s[1][:, ::-1]))


def identificar_no_resumo(n, candidatas):
    """(espécie, nota) pelo retrato de frente no resumo do Pokémon (quadro da esquerda): serve para quem tem apelido."""
    return _identificar(n[30:104, 0:120], candidatas, _sprite_resumo)


def _identificar(regiao, candidatas, carregar):
    melhor = (None, -1.0)
    for esp in candidatas:
        s = carregar(esp)
        if s is None:
            continue
        rgb, masc = s
        r = cv2.matchTemplate(regiao, rgb, cv2.TM_CCORR_NORMED, mask=np.dstack([masc] * 3))
        nota = float(np.nanmax(r))
        if nota > melhor[1]:
            melhor = (esp, nota)
    return melhor


def hp_inimigo(n):
    """Fração do HP do inimigo pela barra da batalha (48 px em y=34) ou None se a barra não está na tela."""
    return _barra(n[34, 52:100])


def hp_meu(n):
    """Fração do HP do nosso Pokémon em campo (barra de 48 px em y=93)."""
    return _barra(n[93, 174:222])


def _barra(linha):
    linha = linha.astype(int)
    r, g, b = linha[:, 0], linha[:, 1], linha[:, 2]
    cheio = ((g > 190) & (r < 190)) | ((r > 200) & (g > 200) & (b < 120)) | ((r > 200) & (g < 150) & (b < 120))
    vazio = linha.max(axis=1) < 120
    if (cheio | vazio).mean() < 0.9:
        return None
    return float(cheio.mean())


def borda_sim_nao(n):
    """Coluna da borda esquerda da caixa Sim/Não ou None. Branco sozinho não basta: o chapéu da jogadora e o céu
    da batalha ficam nessa região; a caixa tem borda escura vertical contínua (batalha x=185, mapa x≈162)."""
    for x in range(150, 205):
        if n[72:102, x].max() < 110 and _branco(n[72:102, x + 5 : x + 30], 240) > 0.6:
            return x
    return None


def escuro(n):
    """Caverna sem FLASH (Rock Tunnel): tudo preto menos um círculo de luz em volta do jogador."""
    cantos = np.concatenate([n[:30, :40], n[:30, -40:], n[-30:, :40], n[-30:, -40:]])
    return cantos.mean() < 8 and n[60:100, 100:140].mean() > 40


def classificar(n):
    """preto | sim_nao | batalha_menu | batalha_texto | golpes | dialogo | outro (mapa é decidido pela localização)."""
    if n.mean() < 12 or n.min(axis=2).mean() > 230:  # escurecimento de porta ou clarão de transição
        return "preto"
    caixa_sim_nao = borda_sim_nao(n) is not None
    if _cor(n[124:152, 16:104], AZUL_BATALHA) > 0.4:
        if caixa_sim_nao:
            return "sim_nao"
        # a janela de atributos do level up também é branca à direita, mas sobe acima da caixa de texto;
        # acima do menu de ação fica o quadro de HP, creme (248, 248, 216), que não passa no branco puro
        menu = _branco(n[124:152, 136:224]) > 0.6 and _branco(n[100:110, 150:220], 240) < 0.5
        return "batalha_menu" if menu else "batalha_texto"
    if _branco(n[124:152, 16:224]) > 0.6:
        if n[124:152, 157:162].max(axis=2).mean() < 120:  # divisória entre golpes e quadro de PP
            return "golpes"
        return "sim_nao" if caixa_sim_nao else "dialogo"
    return "outro"


@dataclass
class Posicao:
    mapa: str
    x: int
    y: int
    confianca: float
    alinhado: bool  # False no meio de um passo


def _casar(img, n):
    r = cv2.matchTemplate(img, n, cv2.TM_CCOEFF_NORMED)
    _, conf, _, (px, py) = cv2.minMaxLoc(r)
    return conf, px, py


ANDARES = [f"{b}{k}F" for b in ("", "B") for k in range(1, 12)]
LETREIRO = (0, 22, 0, 176)  # caixa do nome do mapa no canto de cima (map_name_popup.c), letra escura no branco


def _tem_letreiro(n):
    y0, y1, x0, x1 = LETREIRO
    # caixa branca com o mapa logo abaixo; névoa da Pokémon Tower deixa as duas faixas brancas
    return _branco(n[y0 + 3 : y1 - 3, x0 + 8 : x1 - 30]) >= 0.5 and _branco(n[y1 + 2 : y1 + 8, x0 + 8 : x1 - 30]) < 0.5


def _andar_do_letreiro(n):
    """Andar escrito no letreiro de entrada do mapa ("SILPH CO. 2F" -> 2, "B1F" -> -1), ou None sem letreiro de andar."""
    if not _tem_letreiro(n):
        return None
    achado = texto.ler_mais_longo(n, ANDARES, LETREIRO)
    if not achado:
        return None
    return -int(achado[1:-1]) if achado.startswith("B") else int(achado[:-1])


@lru_cache
def _com_neblina():
    return {m for m, d in mapa.mapas().items() if d.get("weather") == "WEATHER_FOG_HORIZONTAL"}


def _passa_alta(a):
    a = a.astype(np.float32)
    return a - cv2.GaussianBlur(a, (0, 0), 3)  # tira as nuvens largas da névoa e fica com o contorno dos tiles


@lru_cache(maxsize=8)
def _desenho_com_neblina(mapa_id):
    # field_weather_effects.c: névoa em sprites com BLDALPHA 12/8 = 0,75*névoa + 0,5*mapa, estourando no branco
    return _passa_alta(np.clip(155 + 0.5 * mapa.renderizar_mapa(mapa_id).astype(np.float32), 0, 255))


class Localizador:
    """Acha (mapa, x, y) comparando a tela com os mapas desenhados; procura primeiro perto da última posição."""

    def __init__(self):
        self.ultima: Posicao | None = None
        self._miniaturas = None
        self._global_em = 0.0  # última busca global feita só para conferir um encaixe mediano

    def _no_mapa(self, n, mapa_id, perto=None, raio=6):
        neblina = mapa_id in _com_neblina() and n.min(axis=2).mean() > NEBLINA_CLARA
        img = _desenho_com_neblina(mapa_id) if neblina else mapa.renderizar_mapa(mapa_id)
        ox = oy = 0
        if perto:
            cx, cy = (perto[0] + mapa.BORDA) * 16 - JOGADOR_PX[0], (perto[1] + mapa.BORDA) * 16 - JOGADOR_PX[1]
            ox, oy = max(cx - raio * 16, 0), max(cy - raio * 16, 0)
            img = img[oy : cy + raio * 16 + 160, ox : cx + raio * 16 + 240]
        if img.shape[0] < 160 or img.shape[1] < 240:
            return None
        corte = LETREIRO[1] if _tem_letreiro(n) else 0  # o letreiro de entrada cobre o topo: compara só abaixo dele
        conf, px, py = _casar(img, _passa_alta(n[corte:])) if neblina else _casar(img, n[corte:])
        py -= corte
        if neblina:
            conf = min(conf / NEBLINA_ESCALA, 1.0)
        px, py = px + ox + JOGADOR_PX[0], py + oy + JOGADOR_PX[1]
        return Posicao(
            mapa_id, round(px / 16) - mapa.BORDA, round(py / 16) - mapa.BORDA, conf, px % 16 == 0 and py % 16 == 0
        )

    def _vizinhos(self, mapa_id):
        return [m for _, m, _, _ in mapa.conexoes(mapa_id)] + sorted({d for _, _, d, _, _ in mapa.warps(mapa_id)})

    def _global(self, n):
        # ponytail: busca grossa em 1/4 da resolução e refina os 6 melhores; ~1 s. Mapas com o mesmo layout
        # (Centros Pokémon, por exemplo) empatam e o primeiro vence — o contexto da última posição resolve antes.
        if self._miniaturas is None:
            self._miniaturas = {}
            for m in mapa.mapas():
                img = mapa.renderizar_mapa(m)
                if img.shape[0] >= 160 and img.shape[1] >= 240:
                    self._miniaturas[m] = cv2.resize(
                        img, (img.shape[1] // 4, img.shape[0] // 4), interpolation=cv2.INTER_AREA
                    )
        mini = cv2.resize(n, (60, 40), interpolation=cv2.INTER_AREA)
        notas = sorted(((_casar(img, mini)[0], m) for m, img in self._miniaturas.items()), reverse=True)[:6]
        p = max((self._no_mapa(n, m) for _, m in notas), key=lambda p: p.confianca)
        if self.ultima and not mapa.conexoes(p.mapa):
            # interiores com o mesmo layout são idênticos: fica com o que dá para alcançar de onde estava
            layout = mapa.mapas()[p.mapa]["layout"]
            for m in self._vizinhos(self.ultima.mapa):
                if mapa.mapas()[m]["layout"] == layout:
                    return Posicao(m, p.x, p.y, p.confianca, p.alinhado)
        return p

    def _fixar(self, p):
        # o desenho inclui a borda dos vizinhos: posição fora do mapa vira coordenada do mapa conectado
        w_, h_ = mapa.tamanho(p.mapa)
        if not (0 <= p.x < w_ and 0 <= p.y < h_):
            for _, viz, ox, oy in mapa.conexoes(p.mapa):
                wv, hv = mapa.tamanho(viz)
                if 0 <= p.x - ox < wv and 0 <= p.y - oy < hv:
                    p = Posicao(viz, p.x - ox, p.y - oy, p.confianca, p.alinhado)
                    break
        self.ultima = p
        return p

    def localizar(self, n, esperado: tuple | None = None, global_=True):
        """Posicao confiável ou None (tela que não é o mapa: menu, batalha, transição).

        esperado = (mapa, x, y) de onde o jogador deveria estar, para procurar ali primeiro."""
        p = self._localizar(n, esperado, global_)
        andar = _andar_do_letreiro(n) if p else None
        # andares do mesmo prédio são quase iguais (cantos da escada da Silph Co. casam 0,81-0,89 entre si): o letreiro
        # que aparece ao entrar ("SILPH CO. 2F") decide
        if andar is not None and mapa.mapas()[p.mapa].get("floor_number") != andar:
            secao = mapa.mapas()[p.mapa].get("region_map_section")
            certo = next(
                (
                    m
                    for m, d in mapa.mapas().items()
                    if d.get("region_map_section") == secao and d.get("floor_number") == andar
                ),
                None,
            )
            q = self._no_mapa(n, certo) if certo else None
            if q and q.confianca >= CONFIANCA_PERTO:
                return self._fixar(q)
        return p

    def conferir(self, n, p):
        """Confere um encaixe mediano com a busca global (1-2 s); fica com outro mapa só se ele for claramente melhor."""
        self._global_em = time.monotonic()
        g = self._global(n)
        return self._fixar(g if g.confianca >= CERTO and g.confianca > p.confianca + 0.03 else p)

    def _localizar(self, n, esperado, global_):
        tentativas = []  # (mapa, perto, confiança mínima)
        if esperado:
            tentativas.append((esperado[0], tuple(esperado[1:]), CONFIANCA_PERTO))
        if self.ultima:
            tentativas.append((self.ultima.mapa, (self.ultima.x, self.ultima.y), CONFIANCA_PERTO))
        if esperado:
            tentativas.append((esperado[0], None, CONFIANCA))
        if self.ultima:
            tentativas.append((self.ultima.mapa, None, CONFIANCA))
        vistos, mediano = set(), None
        for m, perto, minimo in tentativas:
            if (m, perto) in vistos:
                continue
            vistos.add((m, perto))
            p = self._no_mapa(n, m, perto)
            if p and p.confianca >= CERTO:
                return self._fixar(p)
            if p and p.confianca >= minimo and (mediano is None or p.confianca > mediano.confianca):
                mediano = p  # passa, mas pode ser o andar antigo com o mesmo piso: disputa com os vizinhos
        if self.ultima:
            # vizinhos: o melhor, não o primeiro que passa (o piso da loja de Celadon dá 0,88 dentro do Centro, que dá 0,99;
            # no Rocket Hideout o B2F casou 0,8 com a tela do B3F logo depois da escada)
            p = max(
                (q for m in self._vizinhos(self.ultima.mapa) if (q := self._no_mapa(n, m, None))),
                key=lambda q: q.confianca,
                default=None,
            )
            if p and p.confianca >= CONFIANCA_OUTRO and (mediano is None or p.confianca > mediano.confianca):
                return self._fixar(p)
        if mediano:
            # contexto errado gruda: com a última posição no Mt Moon B2F o ginásio de Fuchsia casava 0,90 lá e a busca
            # global (0,98 no ginásio) nunca rodava. Confere no máximo a cada 10 s: a global custa 1-2 s
            if global_ and mediano.confianca < CERTO and time.monotonic() - self._global_em > 10:
                return self.conferir(n, mediano)
            return self._fixar(mediano)
        if not global_:
            return None
        p = self._global(n)
        if p.confianca < CONFIANCA_OUTRO:
            return None
        # layout igual empata (todo Centro Pokémon): vale o esperado, o último mapa ou um vizinho dele. Sem isso o de
        # Celadon virou o de Viridian e a caminhada nunca "chegava" ao mapa planejado
        contexto = ([esperado[0]] if esperado else []) + (
            [self.ultima.mapa] + self._vizinhos(self.ultima.mapa) if self.ultima else []
        )
        layout = mapa.mapas()[p.mapa].get("layout")
        mesmo = next((m for m in contexto if m in mapa.mapas() and mapa.mapas()[m].get("layout") == layout), None)
        return self._fixar(dataclasses.replace(p, mapa=mesmo) if mesmo else p)
