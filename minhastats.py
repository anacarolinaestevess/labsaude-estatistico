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