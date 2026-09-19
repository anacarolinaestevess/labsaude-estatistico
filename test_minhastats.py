import numpy as np
import pytest
from scipy import stats

import minhastats as ms


DADOS = np.random.default_rng(0).gamma(
    shape=2,
    scale=9,
    size=500
).tolist()


def test_media_com_valores_conhecidos():
    resultado = ms.media([10, 20, 30, 40])

    assert resultado == 25.0


def test_media_compara_com_numpy():
    resultado_proprio = ms.media(DADOS)
    resultado_numpy = np.mean(DADOS)

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_media_lista_vazia():
    with pytest.raises(ValueError):
        ms.media([])

def test_mediana_quantidade_impar():
    resultado = ms.mediana([5, 1, 3])

    assert resultado == 3


def test_mediana_quantidade_par():
    resultado = ms.mediana([7, 1, 5, 3])

    assert resultado == 4.0


def test_mediana_compara_com_numpy():
    resultado_proprio = ms.mediana(DADOS)
    resultado_numpy = np.median(DADOS)

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_mediana_lista_vazia():
    with pytest.raises(ValueError):
        ms.mediana([])

def test_moda_unica():
    resultado = ms.moda([1, 2, 2, 3])

    assert resultado == [2]


def test_moda_compara_com_scipy():
    dados = [4, 2, 4, 3, 4, 2]

    resultado_proprio = ms.moda(dados)[0]
    resultado_scipy = stats.mode(dados).mode

    assert resultado_proprio == resultado_scipy


def test_moda_multimodal():
    resultado = ms.moda([1, 1, 2, 2, 3])

    assert resultado == [1, 2]


def test_moda_amodal():
    resultado = ms.moda([1, 2, 3])

    assert resultado == []


def test_moda_lista_vazia():
    with pytest.raises(ValueError):
        ms.moda([])

