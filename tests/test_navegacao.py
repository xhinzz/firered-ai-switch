"""Regras de movimento do navegador sobre os mapas reais do decomp."""

from conftest import requer_decomp

from fireredia.habilidades import navegacao
from fireredia.missoes import planos

pytestmark = requer_decomp


def _mundo(*golpes):
    m = navegacao.Mundo()
    m.golpes = set(golpes)
    return m


def test_desembarque_do_surf_so_em_elevacao_3():
    # Cerulean Cave 1F: da água (elevação 1) a margem logo abaixo tem elevação 4; o jogo não deixa descer ali
    vizinhos = {novo[:3] for _, novo, _ in _mundo("surf").vizinhos(("MAP_CERULEAN_CAVE_1F", 20, 5, 1))}
    assert ("MAP_CERULEAN_CAVE_1F", 20, 6) not in vizinhos


def test_porta_aberta_por_script_leva_ao_ruby_path():
    alcancaveis = _mundo("surf", "strength", "rock_smash").alcancaveis(("MAP_MT_EMBER_EXTERIOR", 42, 41, 3))
    assert "MAP_MT_EMBER_RUBY_PATH_1F" in alcancaveis


def test_caminho_ate_o_mewtwo_com_o_guarda_liberado():
    m = _mundo("surf", "strength", "rock_smash", "cut")
    m.liberados = {("MAP_CERULEAN_CITY", 1, 13)}
    plano = m.caminho(("MAP_CERULEAN_CITY", 1, 14, 3), navegacao.objetivo(("tile", "MAP_CERULEAN_CAVE_B1F", 7, 13)))
    assert plano and plano[-1][1][:3] == ("MAP_CERULEAN_CAVE_B1F", 7, 13)


def test_plano_de_pedra_do_ruby_path():
    plano = navegacao.plano_da_pedra(
        _mundo("strength"), "MAP_MT_EMBER_RUBY_PATH_B2F", (9, 3), (11, 3), (8, 3), {(12, 5), (12, 2)}
    )
    assert [d for _, d in plano] == ["DIREITA", "DIREITA"]


def test_triangulo_do_deoxys_no_mapa_real():
    from fireredia.missoes import deoxys

    plano = deoxys.plano()
    assert plano is not None and len(plano) == 10
    assert all(len(rota) <= limite for (rota, _, _), limite in zip(plano, planos.DEOXYS_PASSOS, strict=True))


def test_gelo_da_icefall_cave():
    from fireredia.missoes import gelo

    colisao, superficie = gelo.grades("MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F")
    assert planos.plano_gelo(colisao, superficie, (16, 9), (17, 13)) == ["CIMA", "DIREITA", "BAIXO", "ESQUERDA"]
