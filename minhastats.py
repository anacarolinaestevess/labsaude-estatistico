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