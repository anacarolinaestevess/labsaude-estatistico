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

def test_amplitude_com_valores_conhecidos():
    resultado = ms.amplitude([2, 7, 10])

    assert resultado == 8


def test_amplitude_com_numeros_negativos():
    resultado = ms.amplitude([-5, 0, 7])

    assert resultado == 12


def test_amplitude_com_um_valor():
    resultado = ms.amplitude([4])

    assert resultado == 0


def test_amplitude_compara_com_numpy():
    resultado_proprio = ms.amplitude(DADOS)
    resultado_numpy = np.ptp(DADOS)

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_amplitude_lista_vazia():
    with pytest.raises(ValueError):
        ms.amplitude([])


def test_variancia_populacional_conhecida():
    resultado = ms.variancia(
        [1, 2, 3, 4, 5],
        amostral=False
    )

    assert resultado == 2.0


def test_variancia_amostral_conhecida():
    resultado = ms.variancia(
        [1, 2, 3, 4, 5],
        amostral=True
    )

    assert resultado == 2.5


def test_variancia_populacional_compara_numpy():
    resultado_proprio = ms.variancia(
        DADOS,
        amostral=False
    )

    resultado_numpy = np.var(
        DADOS,
        ddof=0
    )

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_variancia_amostral_compara_numpy():
    resultado_proprio = ms.variancia(
        DADOS,
        amostral=True
    )

    resultado_numpy = np.var(
        DADOS,
        ddof=1
    )

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_variancia_amostral_com_um_valor():
    with pytest.raises(ValueError):
        ms.variancia([5], amostral=True)


def test_variancia_lista_vazia():
    with pytest.raises(ValueError):
        ms.variancia([], amostral=False)


def test_desvio_padrao_populacional_compara_numpy():
    resultado_proprio = ms.desvio_padrao(
        DADOS,
        amostral=False
    )

    resultado_numpy = np.std(
        DADOS,
        ddof=0
    )

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_desvio_padrao_amostral_compara_numpy():
    resultado_proprio = ms.desvio_padrao(
        DADOS,
        amostral=True
    )

    resultado_numpy = np.std(
        DADOS,
        ddof=1
    )

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_desvio_padrao_amostral_com_um_valor():
    with pytest.raises(ValueError):
        ms.desvio_padrao([5], amostral=True)


def test_desvio_padrao_lista_vazia():
    with pytest.raises(ValueError):
        ms.desvio_padrao([], amostral=False)