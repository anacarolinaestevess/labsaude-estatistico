# MEDIA

def media(dados):
    """
    Calcula a média aritmética de uma sequência numérica.

    A média corresponde à soma dos valores dividida
    pelo número de observações.
    """
    if len(dados) == 0:
        raise ValueError(
            "Média de sequência vazia é indefinida."
        )

    return sum(dados) / len(dados)

# MEDIANA

def mediana(dados):
    """
    Calcula a mediana de uma sequência numérica.

    A mediana é o valor central dos dados ordenados.
    Quando a quantidade de valores é par, corresponde
    à média dos dois valores centrais.
    """
    if len(dados) == 0:
        raise ValueError(
            "Mediana de sequência vazia é indefinida."
        )

    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)
    posicao_central = n // 2

    if n % 2 == 1:
        return dados_ordenados[posicao_central]

    valor_esquerdo = dados_ordenados[posicao_central - 1]
    valor_direito = dados_ordenados[posicao_central]

    return (valor_esquerdo + valor_direito) / 2

# MODA

def moda(dados):
    """
    Calcula a moda de uma sequência numérica.

    Retorna uma lista porque uma sequência pode ter
    mais de uma moda. Se nenhum valor se repetir,
    retorna uma lista vazia.
    """
    if len(dados) == 0:
        raise ValueError(
            "Moda de sequência vazia é indefinida."
        )

    frequencias = {}

    for valor in dados:
        if valor in frequencias:
            frequencias[valor] += 1
        else:
            frequencias[valor] = 1

    maior_frequencia = max(frequencias.values())

    if maior_frequencia == 1:
        return []

    modas = []

    for valor, frequencia in frequencias.items():
        if frequencia == maior_frequencia:
            modas.append(valor)

    return sorted(modas)

# AMPLITUDE

def amplitude(dados):
    """
    Calcula a amplitude total de uma sequência numérica.

    A amplitude corresponde à diferença entre
    o maior e o menor valor.
    """
    if len(dados) == 0:
        raise ValueError(
            "Amplitude de sequência vazia é indefinida."
        )

    return max(dados) - min(dados)

# VARIÂNCIA

def variancia(dados, amostral=True):
    """
    Calcula a variância de uma sequência numérica.

    Se amostral=True, divide por n - 1.
    Se amostral=False, divide por n.
    """
    n = len(dados)

    if n == 0:
        raise ValueError(
            "Variância de sequência vazia é indefinida."
        )

    if amostral and n < 2:
        raise ValueError(
            "Variância amostral exige pelo menos dois valores."
        )

    media_dos_dados = media(dados)

    soma_dos_quadrados = sum(
        (valor - media_dos_dados) ** 2
        for valor in dados
    )

    if amostral:
        divisor = n - 1
    else:
        divisor = n

    return soma_dos_quadrados / divisor

# DESVIO PADRÃO

def desvio_padrao(dados, amostral=True):
    """
    Calcula o desvio-padrão de uma sequência numérica.

    Se amostral=True, utiliza a variância amostral.
    Se amostral=False, utiliza a variância populacional.
    """
    return variancia(
        dados,
        amostral=amostral
    ) ** 0.5

# PERCENTIL

def percentil(dados, p):
    """
    Calcula um percentil utilizando interpolação linear.

    O percentil p deve estar entre 0 e 100.
    A posição é calculada por:
    h = (n - 1) * p / 100
    """
    if len(dados) == 0:
        raise ValueError(
            "Percentil de sequência vazia é indefinido."
        )

    if p < 0 or p > 100:
        raise ValueError(
            "O percentil deve estar entre 0 e 100."
        )

    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)

    posicao = (n - 1) * p / 100

    indice_inferior = int(posicao)
    indice_superior = min(
        indice_inferior + 1,
        n - 1
    )

    fracao = posicao - indice_inferior

    valor_inferior = dados_ordenados[indice_inferior]
    valor_superior = dados_ordenados[indice_superior]

    return (
        valor_inferior
        + fracao * (valor_superior - valor_inferior)
    )

# QUARTIS

def quartis(dados):
    """
    Calcula o primeiro, o segundo e o terceiro quartil.

    Retorna um dicionário com Q1, Q2 e Q3.
    """
    return {
        "Q1": percentil(dados, 25),
        "Q2": percentil(dados, 50),
        "Q3": percentil(dados, 75),
    }

# Coeficiente de variação

def coeficiente_variacao(dados, amostral=True):
    """
    Calcula o coeficiente de variação em percentual.

    Se amostral=True, utiliza o desvio-padrão amostral.
    Se amostral=False, utiliza o desvio-padrão populacional.
    """
    media_dos_dados = media(dados)

    if abs(media_dos_dados) < 1e-12:
        raise ValueError(
            "O coeficiente de variação é indefinido "
            "quando a média é zero ou muito próxima de zero."
        )

    desvio = desvio_padrao(
        dados,
        amostral=amostral
    )

    return (desvio / media_dos_dados) * 100

# COVARIÂNCIA

def covariancia(x, y, amostral=True):
    """
    Calcula a covariância entre duas sequências numéricas.

    Se amostral=True, divide por n - 1.
    Se amostral=False, divide por n.
    """
    if len(x) != len(y):
        raise ValueError(
            "As sequências devem ter o mesmo tamanho."
        )

    n = len(x)

    if n == 0:
        raise ValueError(
            "Covariância de sequências vazias é indefinida."
        )

    if amostral and n < 2:
        raise ValueError(
            "Covariância amostral exige pelo menos dois pares."
        )

    media_x = media(x)
    media_y = media(y)

    soma_dos_produtos = sum(
        (valor_x - media_x) * (valor_y - media_y)
        for valor_x, valor_y in zip(x, y)
    )

    if amostral:
        divisor = n - 1
    else:
        divisor = n

    return soma_dos_produtos / divisor

# CORRELAÇÃO DE PEARSON

def correlacao_pearson(x, y):
    """
    Calcula o coeficiente de correlação de Pearson.

    O resultado varia de -1 a 1:
    - próximo de 1: associação linear positiva;
    - próximo de -1: associação linear negativa;
    - próximo de 0: pouca associação linear.
    """
    if len(x) != len(y):
        raise ValueError(
            "As sequências devem ter o mesmo tamanho."
        )

    if len(x) < 2:
        raise ValueError(
            "A correlação exige pelo menos dois pares."
        )

    desvio_x = desvio_padrao(
        x,
        amostral=True
    )

    desvio_y = desvio_padrao(
        y,
        amostral=True
    )

    if abs(desvio_x) < 1e-12 or abs(desvio_y) < 1e-12:
        raise ValueError(
            "A correlação é indefinida para variável constante."
        )

    covariancia_xy = covariancia(
        x,
        y,
        amostral=True
    )

    return covariancia_xy / (desvio_x * desvio_y)