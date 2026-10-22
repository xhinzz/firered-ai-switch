"""Percepção sobre telas reais capturadas do Switch durante a campanha (tests/fixtures, 240x160)."""

import pytest
from conftest import quadro, requer_decomp

from fireredia.habilidades import menus
from fireredia.percepcao import olhos, texto

pytestmark = requer_decomp


@pytest.mark.parametrize(
    ("fixture", "esperado"),
    [
        ("mapa_viridian_centro", ("MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F", 11, 2)),
        ("mapa_cerulean_guarda", ("MAP_CERULEAN_CITY", 1, 14)),
        ("mapa_icefall_b1f", ("MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F", 8, 9)),
        ("mapa_birth_island", ("MAP_BIRTH_ISLAND_EXTERIOR", 15, 22)),
        ("mapa_navel_cume", ("MAP_NAVEL_ROCK_SUMMIT", 10, 18)),
        ("mapa_four_island", ("MAP_FOUR_ISLAND", 9, 28)),
    ],
)
def test_localiza_o_jogador_no_mapa(fixture, esperado):
    p = olhos.Localizador().localizar(quadro(fixture), global_=True)
    assert p is not None and (p.mapa, p.x, p.y) == esperado


def test_classifica_telas():
    assert olhos.classificar(quadro("batalha_menu")) == "batalha_menu"
    assert olhos.classificar(quadro("dialogo_balsa")) == "dialogo"
    assert olhos.classificar(quadro("mapa_four_island")) == "outro"


def test_le_a_caixa_de_dialogo_com_a_fonte_do_jogo():
    assert texto.ler_caixa(quadro("dialogo_balsa")) == "Ahoy, there!\nWhere do you want to sail?"


def test_estrela_de_shiny_no_resumo():
    assert menus._tem_estrela(quadro("resumo_shiny"))
    assert not menus._tem_estrela(quadro("resumo_golpes"))


def test_titulo_da_caixa_do_ace_e_casas_ocupadas():
    n = quadro("pc_caixa10")
    assert menus._na_caixa(10, n) and not menus._na_caixa(1, n)
    assert menus._ocupadas(n) == [7]


def test_painel_le_mewtwo_e_nao_o_prefixo_mew():
    assert menus._no_painel(quadro("pc_painel_mewtwo")) == ("MEWTWO", 70)
