"""Códigos ACE guardados e o adaptador do gerador do E-Sh4rk (sem Node nem rede)."""

import pytest

from fireredia.ace import gerador, teclado
from fireredia.ace.caixas import NORMALIZA
from fireredia.ace.codigos import CODIGOS, WILD_ENTEI, WILD_RAIKOU, WILD_SUICUNE


@pytest.mark.parametrize("nome", sorted(CODIGOS))
def test_nomes_cabem_e_se_digitam(nome):
    for caixa in CODIGOS[nome]:
        assert 1 <= len(caixa) <= 8, f"{nome}: {caixa!r} passa de 8 caracteres"
        for ch in caixa:
            teclado.onde(NORMALIZA.get(ch, ch))  # levanta se o caractere não está no teclado do jogo


def test_caes_diferem_so_na_caixa_4():
    for outro in (WILD_ENTEI, WILD_RAIKOU):
        diferentes = [k + 1 for k, (a, b) in enumerate(zip(WILD_SUICUNE, outro, strict=True)) if a != b]
        assert diferentes == [4]


def test_ajustar_troca_so_o_valor():
    fonte = "PokemonHex = 0x00C4 @input:species\nPokemonLV = 25\nNPC = 2 ;sets which NPC\n"
    pronto = gerador.ajustar(fonte, PokemonHex=0xF5, PokemonLV=50)
    assert pronto == "PokemonHex = 245 @input:species\nPokemonLV = 50\nNPC = 2 ;sets which NPC\n"
    with pytest.raises(KeyError):
        gerador.ajustar(fonte, Inexistente=1)


def test_le_nomes_da_saida_do_gerador():
    saida = "0xE2CFACBA ; ...\n\nBox  1: / ? U n F E 3 n   [/?UnFE3n]\nBox 10: A A A _ _ . o a   [AAA  .oa]\n"
    assert gerador.nomes_de_caixa(saida) == ["/?UnFE3n", "AAA  .oa"]
