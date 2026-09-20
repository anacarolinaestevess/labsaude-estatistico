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


def test_percentil_com_valores_conhecidos():
    dados = [0, 10, 20, 30]

    assert ms.percentil(dados, 0) == 0
    assert ms.percentil(dados, 25) == 7.5
    assert ms.percentil(dados, 50) == 15
    assert ms.percentil(dados, 100) == 30


@pytest.mark.parametrize(
    "p",
    [0, 10, 25, 50, 75, 90, 100]
)
def test_percentil_compara_com_numpy(p):
    resultado_proprio = ms.percentil(DADOS, p)

    resultado_numpy = np.percentile(
        DADOS,
        p,
        method="linear"
    )

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-6
    )


def test_percentil_lista_vazia():
    with pytest.raises(ValueError):
        ms.percentil([], 50)


def test_percentil_abaixo_de_zero():
    with pytest.raises(ValueError):
        ms.percentil([1, 2, 3], -1)


def test_percentil_acima_de_cem():
    with pytest.raises(ValueError):
        ms.percentil([1, 2, 3], 101)



def test_quartis_com_valores_conhecidos():
    resultado = ms.quartis([0, 10, 20, 30])

    assert resultado["Q1"] == 7.5
    assert resultado["Q2"] == 15.0
    assert resultado["Q3"] == 22.5


def test_quartis_compara_com_numpy():
    resultado_proprio = ms.quartis(DADOS)

    resultado_numpy = np.percentile(
        DADOS,
        [25, 50, 75],
        method="linear"
    )

    valores_proprios = [
        resultado_proprio["Q1"],
        resultado_proprio["Q2"],
        resultado_proprio["Q3"],
    ]

    assert np.allclose(
        valores_proprios,
        resultado_numpy,
        rtol=1e-6
    )


def test_quartis_lista_vazia():
    with pytest.raises(ValueError):
        ms.quartis([])

#TESTES PARA O COEFICIENTE DE VARIAÇÃO

def test_coeficiente_variacao_amostral_conhecido():
    resultado = ms.coeficiente_variacao(
        [10, 20, 30],
        amostral=True
    )

    assert np.isclose(
        resultado,
        50.0,
        rtol=1e-9
    )


def test_coeficiente_variacao_amostral_compara_numpy():
    resultado_proprio = ms.coeficiente_variacao(
        DADOS,
        amostral=True
    )

    resultado_numpy = (
        np.std(DADOS, ddof=1)
        / np.mean(DADOS)
    ) * 100

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_coeficiente_variacao_populacional_compara_numpy():
    resultado_proprio = ms.coeficiente_variacao(
        DADOS,
        amostral=False
    )

    resultado_numpy = (
        np.std(DADOS, ddof=0)
        / np.mean(DADOS)
    ) * 100

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_coeficiente_variacao_dados_constantes():
    resultado = ms.coeficiente_variacao(
        [5, 5, 5],
        amostral=True
    )

    assert resultado == 0.0


def test_coeficiente_variacao_media_zero():
    with pytest.raises(ValueError):
        ms.coeficiente_variacao(
            [-1, 0, 1],
            amostral=True
        )

# TESTE para covariância

def test_covariancia_amostral_compara_numpy():
    x = DADOS
    y = [2 * valor + 3 for valor in DADOS]

    resultado_proprio = ms.covariancia(
        x,
        y,
        amostral=True
    )

    resultado_numpy = np.cov(
        x,
        y,
        ddof=1
    )[0, 1]

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_covariancia_populacional_compara_numpy():
    x = DADOS
    y = [2 * valor + 3 for valor in DADOS]

    resultado_proprio = ms.covariancia(
        x,
        y,
        amostral=False
    )

    resultado_numpy = np.cov(
        x,
        y,
        ddof=0
    )[0, 1]

    assert np.isclose(
        resultado_proprio,
        resultado_numpy,
        rtol=1e-9
    )


def test_covariancia_negativa():
    resultado = ms.covariancia(
        [1, 2, 3],
        [6, 4, 2],
        amostral=True
    )

    assert resultado < 0


def test_covariancia_tamanhos_diferentes():
    with pytest.raises(ValueError):
        ms.covariancia(
            [1, 2, 3],
            [1, 2],
            amostral=True
        )


def test_covariancia_listas_vazias():
    with pytest.raises(ValueError):
        ms.covariancia(
            [],
            [],
            amostral=False
        )


def test_covariancia_amostral_com_um_par():
    with pytest.raises(ValueError):
        ms.covariancia(
            [1],
            [2],
            amostral=True
        )

# TESTES PARA CORRELAÇÃO DE PEARSON

def test_correlacao_positiva_perfeita():
    resultado = ms.correlacao_pearson(
        [1, 2, 3],
        [2, 4, 6]
    )

    assert np.isclose(
        resultado,
        1.0,
        rtol=1e-9
    )


def test_correlacao_negativa_perfeita():
    resultado = ms.correlacao_pearson(
        [1, 2, 3],
        [6, 4, 2]
    )

    assert np.isclose(
        resultado,
        -1.0,
        rtol=1e-9
    )


def test_correlacao_compara_com_scipy():
    x = DADOS

    y = [
        0.7 * valor + (indice % 5)
        for indice, valor in enumerate(DADOS)
    ]

    resultado_proprio = ms.correlacao_pearson(x, y)
    resultado_scipy = stats.pearsonr(x, y).statistic

    assert np.isclose(
        resultado_proprio,
        resultado_scipy,
        rtol=1e-9
    )


def test_correlacao_variavel_constante():
    with pytest.raises(ValueError):
        ms.correlacao_pearson(
            [1, 1, 1],
            [2, 3, 4]
        )


def test_correlacao_tamanhos_diferentes():
    with pytest.raises(ValueError):
        ms.correlacao_pearson(
            [1, 2, 3],
            [1, 2]
        )


def test_correlacao_com_um_par():
    with pytest.raises(ValueError):
        ms.correlacao_pearson(
            [1],
            [2]
        )