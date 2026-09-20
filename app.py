
from pathlib import Path
import pandas as pd
import streamlit as st

import minhastats as ms
import matplotlib.pyplot as plt
import math
import numpy as np

ARQUIVO_DADOS = Path(
    "dados/internacoes_sih_df_janeiro_2025.csv"
)

st.set_page_config(
    page_title="LabSaúde SUS",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def carregar_dados():
    """
    Carrega a base preparada do SIH/SUS.

    Os códigos de diagnóstico e procedimento são
    carregados como texto, pois não são quantidades.
    """
    return pd.read_csv(
        ARQUIVO_DADOS,
        dtype={
            "diagnostico_principal": str,
            "procedimento_realizado": str,
        }
    )


dados = carregar_dados()


st.title("LabSaúde SUS")

st.subheader(
    "Laboratório Estatístico das Internações Hospitalares"
)

st.write(
    "Dados do SIH/SUS referentes ao Distrito Federal, "
    "competência janeiro de 2025."
)

st.info(
    "Cada linha representa um registro de AIH. "
    "Uma mesma pessoa pode possuir mais de uma AIH."
)


coluna_1, coluna_2 = st.columns(2)

coluna_1.metric(
    "Registros de AIH",
    f"{len(dados):,}".replace(",", ".")
)

coluna_2.metric(
    "Variáveis disponíveis",
    dados.shape[1]
)


st.divider()

st.header("Estatística descritiva")

VARIAVEIS_NUMERICAS = [
    "idade_anos",
    "dias_permanencia",
    "quantidade_diarias",
    "dias_uti",
    "valor_total",
    "valor_uti",
]

variavel = st.selectbox(
    "Escolha uma variável numérica:",
    VARIAVEIS_NUMERICAS
)

valores = dados[variavel].dropna().tolist()

# CALCULO DAS MEDIDAS DESCRITIVAS

media = ms.media(valores)
mediana = ms.mediana(valores)
modas = ms.moda(valores)
amplitude = ms.amplitude(valores)
variancia = ms.variancia(valores, amostral=True)
desvio_padrao = ms.desvio_padrao(valores, amostral=True)
coeficiente_variacao = ms.coeficiente_variacao(valores)
quartis = ms.quartis(valores)

if modas:
    texto_moda = ", ".join(f"{valor:.2f}" for valor in modas[:3])
    if len(modas) > 3:
        texto_moda += "..."
else:
    texto_moda = "Amodal"

linha_1 = st.columns(4)
linha_1[0].metric("Número de observações", len(valores))
linha_1[1].metric("Média", f"{media:.2f}")
linha_1[2].metric("Mediana", f"{mediana:.2f}")
linha_1[3].metric("Moda", texto_moda)

linha_2 = st.columns(4)
linha_2[0].metric("Mínimo", f"{min(valores):.2f}")
linha_2[1].metric("Máximo", f"{max(valores):.2f}")
linha_2[2].metric("Amplitude", f"{amplitude:.2f}")
linha_2[3].metric("Variância amostral", f"{variancia:.2f}")

linha_3 = st.columns(4)
linha_3[0].metric("Desvio-padrão amostral", f"{desvio_padrao:.2f}")
linha_3[1].metric("Coeficiente de variação", f"{coeficiente_variacao:.2f}%")
linha_3[2].metric("1º quartil (Q1)", f"{quartis['Q1']:.2f}")
linha_3[3].metric("3º quartil (Q3)", f"{quartis['Q3']:.2f}")

# AMPLITUDE INTERQUARTIL (IQR) E VALORES EXTREMOS

q1 = quartis["Q1"]
q3 = quartis["Q3"]
intervalo_interquartil = q3 - q1

limite_inferior = q1 - 1.5 * intervalo_interquartil
limite_superior = q3 + 1.5 * intervalo_interquartil

valores_extremos = [
    valor
    for valor in valores
    if valor < limite_inferior or valor > limite_superior
]

st.subheader("Identificação de valores extremos")

linha_outliers = st.columns(4)
linha_outliers[0].metric(
    "Intervalo interquartil",
    f"{intervalo_interquartil:.2f}",
)
linha_outliers[1].metric(
    "Limite inferior",
    f"{limite_inferior:.2f}",
)
linha_outliers[2].metric(
    "Limite superior",
    f"{limite_superior:.2f}",
)
linha_outliers[3].metric(
    "Valores extremos",
    len(valores_extremos),
)

percentual_extremos = 100 * len(valores_extremos) / len(valores)

if limite_inferior < 0 and min(valores) >= 0:
    st.info(
        "O limite inferior calculado é negativo, mas a variável não possui "
        "valores negativos. Portanto, não há valores extremos abaixo desse limite."
    )
    
st.write(
    f"Foram identificadas **{len(valores_extremos)} observações** "
    f"fora dos limites definidos pelo método do intervalo interquartil, "
    f"correspondendo a **{percentual_extremos:.2f}%** dos registros."
)

# HISTOGRAMA E BLOCK PLOT

st.subheader("Visualização da distribuição")

numero_classes = st.slider(
    "Número de classes do histograma:",
    min_value=5,
    max_value=50,
    value=20,
)

coluna_histograma, coluna_boxplot = st.columns(2)

with coluna_histograma:
    st.write("**Histograma**")

    figura_histograma, eixo_histograma = plt.subplots()

    eixo_histograma.hist(
        valores,
        bins=numero_classes,
        color="#2E86AB",
        edgecolor="white",
    )

    eixo_histograma.set_xlabel(variavel)
    eixo_histograma.set_ylabel("Frequência")
    eixo_histograma.set_title(f"Distribuição de {variavel}")

    st.pyplot(figura_histograma)
    plt.close(figura_histograma)

with coluna_boxplot:
    st.write("**Boxplot**")

    figura_boxplot, eixo_boxplot = plt.subplots()

    eixo_boxplot.boxplot(
        valores,
        vert=True,
        patch_artist=True,
        boxprops={"facecolor": "#7AC7C4"},  
    )

    eixo_boxplot.set_ylabel(variavel)
    eixo_boxplot.set_title(f"Boxplot de {variavel}")
    eixo_boxplot.set_xticks([])

    st.pyplot(figura_boxplot)
    plt.close(figura_boxplot)

# INTERPRETAÇÃO AUTOMÁTICA

st.subheader("Interpretação automática")

diferenca = media - mediana
tolerancia = 0.1 * desvio_padrao

if abs(diferenca) <= tolerancia:
    interpretacao = (
        "A média e a mediana apresentam valores próximos, indicando uma "
        "distribuição aproximadamente simétrica."
    )
elif diferenca > 0:
    interpretacao = (
        "A média é maior que a mediana, sugerindo assimetria à direita. "
        "Isso indica a presença de valores elevados que aumentam a média."
    )
else:
    interpretacao = (
        "A média é menor que a mediana, sugerindo assimetria à esquerda. "
        "Isso indica a presença de valores baixos que reduzem a média."
    )

st.info(interpretacao)

if coeficiente_variacao < 15:
    interpretacao_variabilidade = "baixa"
elif coeficiente_variacao < 30:
    interpretacao_variabilidade = "moderada"
else:
    interpretacao_variabilidade = "elevada"

st.write(
    f"O coeficiente de variação foi de **{coeficiente_variacao:.2f}%**, "
    f"indicando variabilidade **{interpretacao_variabilidade}** em relação "
    f"à média."
)

# TABELA DE INTERPRETAÇÃO DE FREQUêNCIAS

st.subheader("Tabela de distribuição de frequências")

numero_classes_sturges = math.ceil(
    1 + 3.322 * math.log10(len(valores))
)

largura_classe = amplitude / numero_classes_sturges
valor_minimo = min(valores)

classes = []
frequencias = []

for indice in range(numero_classes_sturges):
    inicio = valor_minimo + indice * largura_classe
    fim = inicio + largura_classe

    if indice == numero_classes_sturges - 1:
        frequencia = sum(
            1 for valor in valores
            if inicio <= valor <= fim
        )
        intervalo = f"{inicio:.2f} ├─ {fim:.2f}"
    else:
        frequencia = sum(
            1 for valor in valores
            if inicio <= valor < fim
        )
        intervalo = f"{inicio:.2f} ├─ {fim:.2f}"

    classes.append(intervalo)
    frequencias.append(frequencia)

frequencias_relativas = [
    100 * frequencia / len(valores)
    for frequencia in frequencias
]

frequencias_acumuladas = []
acumulada = 0

for frequencia in frequencias:
    acumulada += frequencia
    frequencias_acumuladas.append(acumulada)

tabela_frequencias = pd.DataFrame(
    {
        "Intervalo de classe": classes,
        "Frequência absoluta": frequencias,
        "Frequência relativa (%)": frequencias_relativas,
        "Frequência acumulada": frequencias_acumuladas,
    }
)

tabela_frequencias["Frequência relativa (%)"] = (
    tabela_frequencias["Frequência relativa (%)"].round(2)
)

st.write(
    f"A regra de Sturges definiu **{numero_classes_sturges} classes** "
    f"para as {len(valores)} observações."
)

st.dataframe(
    tabela_frequencias,
    hide_index=True,
    use_container_width=True,
)

# Final da análise da variável numérica
st.caption(
    "As medidas exibidas são calculadas pelas funções próprias "
    "do arquivo minhastats.py."
)

# Início da análise categórica

st.divider()
st.header("Análise de variáveis categóricas")

VARIAVEIS_CATEGORICAS = [
    "sexo",
    "raca_cor",
    "carater_internacao",
    "complexidade",
    "obito",
]

variavel_categorica = st.selectbox(
    "Escolha uma variável categórica:",
    VARIAVEIS_CATEGORICAS,
)

categorias = dados[variavel_categorica].fillna("Não informado").tolist()

contagens = {}

for categoria in categorias:
    if categoria in contagens:
        contagens[categoria] += 1
    else:
        contagens[categoria] = 1

contagens_ordenadas = sorted(
    contagens.items(),
    key=lambda item: item[1],
    reverse=True,
)

tabela_categorica = pd.DataFrame(
    contagens_ordenadas,
    columns=["Categoria", "Frequência absoluta"],
)

tabela_categorica["Frequência relativa (%)"] = (
    100
    * tabela_categorica["Frequência absoluta"]
    / len(categorias)
).round(2)

st.dataframe(
    tabela_categorica,
    hide_index=True,
    use_container_width=True,
)

#GRAFICOS DADOS CATEGORICOS

coluna_barras, coluna_setores = st.columns(2)

with coluna_barras:
    st.write("**Gráfico de barras**")

    figura_barras, eixo_barras = plt.subplots()

    eixo_barras.bar(
        tabela_categorica["Categoria"].astype(str),
        tabela_categorica["Frequência absoluta"],
        color="#2E86AB",
    )

    eixo_barras.set_xlabel(variavel_categorica)
    eixo_barras.set_ylabel("Frequência")
    eixo_barras.tick_params(axis="x", rotation=45)

    figura_barras.tight_layout()
    st.pyplot(figura_barras)
    plt.close(figura_barras)

with coluna_setores:
    st.write("**Gráfico de setores**")

    figura_setores, eixo_setores = plt.subplots()

    eixo_setores.pie(
        tabela_categorica["Frequência absoluta"],
        labels=tabela_categorica["Categoria"],
        autopct="%1.1f%%",
        startangle=90,
    )

    eixo_setores.axis("equal")

    st.pyplot(figura_setores)
    plt.close(figura_setores)

#SIMULAÇÃO DE MONTE CARLO

st.divider()
st.header("Simulações de Monte Carlo")

st.subheader("Lei dos Grandes Números")

st.write(
    "Nesta simulação, os 20.996 registros de valor total das AIH "
    "formam a população empírica. Retiramos observações aleatórias "
    "com reposição e acompanhamos a convergência da média amostral "
    "para a média de todos os registros."
)

valores_valor_total = (
    dados["valor_total"]
    .dropna()
    .tolist()
)

media_populacional_valor = ms.media(valores_valor_total)

tamanho_amostra = st.slider(
    "Número de observações sorteadas:",
    min_value=100,
    max_value=20000,
    value=1000,
    step=100,
    key="tamanho_lgn_valor_total",
)

gerador_lgn = np.random.default_rng(seed=42)

amostra_valor_total = gerador_lgn.choice(
    valores_valor_total,
    size=tamanho_amostra,
    replace=True,
)

medias_acumuladas = []
soma_acumulada = 0

for posicao, valor in enumerate(amostra_valor_total, start=1):
    soma_acumulada += valor
    medias_acumuladas.append(soma_acumulada / posicao)

# GRÁFICO DA SIMULAÇÃO

figura_lgn, eixo_lgn = plt.subplots()

eixo_lgn.plot(
    range(1, tamanho_amostra + 1),
    medias_acumuladas,
    color="#2E86AB",
    label="Média acumulada da amostra",
)

eixo_lgn.axhline(
    media_populacional_valor,
    color="#D1495B",
    linestyle="--",
    label="Média dos 20.996 registros",
)

eixo_lgn.set_xlabel("Número de observações sorteadas")
eixo_lgn.set_ylabel("Valor médio da AIH (R$)")
eixo_lgn.set_title("Convergência da média do valor total")
eixo_lgn.legend()

st.pyplot(figura_lgn)
plt.close(figura_lgn)

st.write(
    f"A média dos 20.996 registros é "
    f"**R$ {media_populacional_valor:,.2f}**. "
    f"Após {tamanho_amostra} sorteios, a média acumulada foi "
    f"**R$ {medias_acumuladas[-1]:,.2f}**."
)

st.caption(
    "Os sorteios são feitos com reposição: um mesmo registro pode "
    "ser selecionado mais de uma vez, como é habitual em simulações "
    "de Monte Carlo."
)

# TEOREMA CENTRAL DO LIMITE

st.subheader("Teorema Central do Limite")

st.write(
    "Nesta simulação, retiramos repetidamente amostras aleatórias, "
    "com reposição, dos valores totais das 20.996 AIH. Para cada "
    "amostra, calculamos a média do valor total."
)

coluna_tamanho, coluna_repeticoes = st.columns(2)

with coluna_tamanho:
    tamanho_cada_amostra = st.slider(
        "Tamanho de cada amostra:",
        min_value=2,
        max_value=200,
        value=30,
        step=1,
        key="tamanho_tcl_valor_total",
    )

with coluna_repeticoes:
    numero_repeticoes = st.slider(
        "Número de amostras simuladas:",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
        key="repeticoes_tcl_valor_total",
    )

desvio_populacional_valor = ms.desvio_padrao(
    valores_valor_total,
    amostral=False,
)

gerador_tcl = np.random.default_rng(seed=42)

medias_amostrais = []

for _ in range(numero_repeticoes):
    amostra = gerador_tcl.choice(
        valores_valor_total,
        size=tamanho_cada_amostra,
        replace=True,
    )

    medias_amostrais.append(
        ms.media(amostra.tolist())
    )

# GRÁFICO DO TEOREMA CENTRAL DO LIMITE

figura_tcl, eixo_tcl = plt.subplots()

eixo_tcl.hist(
    medias_amostrais,
    bins=30,
    density=True,
    color="#7AC7C4",
    edgecolor="white",
    label="Médias simuladas",
)

erro_padrao = (
    desvio_populacional_valor
    / math.sqrt(tamanho_cada_amostra)
)

valores_x = np.linspace(
    min(medias_amostrais),
    max(medias_amostrais),
    300,
)

densidade_normal_tcl = (
    1 / (erro_padrao * math.sqrt(2 * math.pi))
    * np.exp(
        -0.5
        * (
            (valores_x - media_populacional_valor)
            / erro_padrao
        ) ** 2
    )
)

eixo_tcl.plot(
    valores_x,
    densidade_normal_tcl,
    color="#D1495B",
    linewidth=2,
    label="Distribuição normal teórica",
)

eixo_tcl.axvline(
    media_populacional_valor,
    color="black",
    linestyle="--",
    label="Média dos 20.996 registros",
)

eixo_tcl.set_xlabel("Média amostral do valor total (R$)")
eixo_tcl.set_ylabel("Densidade")
eixo_tcl.set_title("Distribuição das médias do valor total")
eixo_tcl.legend()

st.pyplot(figura_tcl)
plt.close(figura_tcl)

media_das_medias = ms.media(medias_amostrais)

st.info(
    f"A média dos 20.996 registros é "
    f"R$ {media_populacional_valor:,.2f}. "
    f"A média das {numero_repeticoes} médias amostrais foi "
    f"R$ {media_das_medias:,.2f}. À medida que o tamanho das "
    f"amostras aumenta, sua distribuição tende a se aproximar "
    f"de uma distribuição Normal."
)

# DISTRIBUIÇÃO DE PROBABILIDADE

st.divider()
st.header("Distribuições de probabilidade")

st.subheader("Distribuição Normal")

st.write(
    "Altere os parâmetros para observar como a média e o "
    "desvio-padrão modificam a distribuição."
)

coluna_media_normal, coluna_desvio_normal = st.columns(2)

with coluna_media_normal:
    media_normal = st.number_input(
        "Média da distribuição:",
        value=0.0,
        step=1.0,
    )

with coluna_desvio_normal:
    desvio_normal = st.number_input(
        "Desvio-padrão da distribuição:",
        min_value=0.1,
        value=1.0,
        step=0.1,
    )

coluna_inicio, coluna_fim = st.columns(2)

with coluna_inicio:
    inicio_intervalo = st.number_input(
        "Início do intervalo:",
        value=-1.0,
        step=0.1,
    )

with coluna_fim:
    fim_intervalo = st.number_input(
        "Fim do intervalo:",
        value=1.0,
        step=0.1,
    )

        # CALCULO DA DISTRIBUIÇÃO DE PROBABILIDADES
valores_normal = np.linspace(
    media_normal - 4 * desvio_normal,
    media_normal + 4 * desvio_normal,
    500,
)

densidade_normal_teorica = (
    1 / (desvio_normal * math.sqrt(2 * math.pi))
    * np.exp(
        -0.5
        * ((valores_normal - media_normal) / desvio_normal) ** 2
    )
)

if inicio_intervalo < fim_intervalo:
    z_inicio = (
        inicio_intervalo - media_normal
    ) / (desvio_normal * math.sqrt(2))

    z_fim = (
        fim_intervalo - media_normal
    ) / (desvio_normal * math.sqrt(2))

    probabilidade = 0.5 * (
        math.erf(z_fim) - math.erf(z_inicio)
    )

    # GRÁFICO DA DISTRIBUIÇÃO 

    figura_normal, eixo_normal = plt.subplots()

    eixo_normal.plot(
        valores_normal,
        densidade_normal_teorica,
        color="#2E86AB",
        linewidth=2,
    )

    mascara_intervalo = (
        (valores_normal >= inicio_intervalo)
        & (valores_normal <= fim_intervalo)
    )

    eixo_normal.fill_between(
        valores_normal,
        densidade_normal_teorica,
        where=mascara_intervalo,
        color="#7AC7C4",
        alpha=0.7,
    )

    eixo_normal.axvline(
        media_normal,
        color="#D1495B",
        linestyle="--",
        label="Média",
    )

    eixo_normal.set_xlabel("Valor")
    eixo_normal.set_ylabel("Densidade")
    eixo_normal.set_title("Curva da distribuição Normal")
    eixo_normal.legend()

    st.pyplot(figura_normal)
    plt.close(figura_normal)

    st.success(
        f"A probabilidade de um valor estar entre "
        f"{inicio_intervalo:.2f} e {fim_intervalo:.2f} é "
        f"**{probabilidade * 100:.2f}%**."
    )

else:
    st.error(
        "O início do intervalo deve ser menor que o final."
    )

# DISTRIBUIÇÃO BINOMIAL

st.subheader("Distribuição Binomial")

st.write(
    "A distribuição Binomial representa o número de ocorrências de "
    "um evento em uma quantidade fixa de observações. Nesta aplicação, "
    "o evento considerado é o registro de óbito em uma AIH."
)

obitos_booleanos = (
    dados["obito"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["sim", "1", "óbito", "obito"])
)

numero_obitos = int(obitos_booleanos.sum())
probabilidade_obito_observada = numero_obitos / len(dados)

st.write(
    f"Na base analisada, foram registrados **{numero_obitos} óbitos** "
    f"em **{len(dados)} AIH**, correspondendo a "
    f"**{probabilidade_obito_observada * 100:.2f}%**."
)

coluna_n, coluna_p = st.columns(2)

with coluna_n:
    numero_aihs = st.slider(
        "Número hipotético de AIH:",
        min_value=1,
        max_value=100,
        value=30,
        step=1,
    )

with coluna_p:
    probabilidade_obito = st.slider(
        "Probabilidade de óbito em cada AIH:",
        min_value=0.0,
        max_value=1.0,
        value=float(probabilidade_obito_observada),
        step=0.001,
        format="%.3f",
    )

numero_selecionado = st.slider(
    "Número de óbitos para calcular a probabilidade:",
    min_value=0,
    max_value=numero_aihs,
    value=min(1, numero_aihs),
    step=1,
)

valores_binomial = list(range(numero_aihs + 1))

probabilidades_binomial = []

for numero_eventos in valores_binomial:
    probabilidade = (
        math.comb(numero_aihs, numero_eventos)
        * probabilidade_obito ** numero_eventos
        * (1 - probabilidade_obito) ** (
            numero_aihs - numero_eventos
        )
    )

    probabilidades_binomial.append(probabilidade)

probabilidade_exata = probabilidades_binomial[
    numero_selecionado
]

probabilidade_acumulada = sum(
    probabilidades_binomial[:numero_selecionado + 1]
)

# GRÁFICO DA DISTRIBUIÇÃO BINOMIAL

figura_binomial, eixo_binomial = plt.subplots()

eixo_binomial.bar(
    valores_binomial,
    probabilidades_binomial,
    color="#7AC7C4",
    edgecolor="white",
)

eixo_binomial.bar(
    numero_selecionado,
    probabilidade_exata,
    color="#D1495B",
    label="Número selecionado",
)

eixo_binomial.set_xlabel("Número de óbitos")
eixo_binomial.set_ylabel("Probabilidade")
eixo_binomial.set_title("Distribuição Binomial")
eixo_binomial.legend()

st.pyplot(figura_binomial)
plt.close(figura_binomial)

coluna_exata, coluna_acumulada = st.columns(2)

coluna_exata.metric(
    f"P(X = {numero_selecionado})",
    f"{probabilidade_exata * 100:.2f}%",
)

coluna_acumulada.metric(
    f"P(X ≤ {numero_selecionado})",
    f"{probabilidade_acumulada * 100:.2f}%",
)

st.caption(
    "Esta é uma aplicação didática. O modelo Binomial pressupõe "
    "observações independentes e probabilidade constante. Além disso, "
    "a base contém registros de AIH, e não necessariamente pessoas únicas."
)

# CORRELAÇÃO E REGRESSÃO LINEAR

st.divider()
st.header("Correlação e regressão linear")

st.subheader("Correlação de Pearson")

st.write(
    "Selecione duas variáveis numéricas para avaliar a direção "
    "e a intensidade da relação linear entre elas."
)

coluna_x, coluna_y = st.columns(2)

with coluna_x:
    variavel_x = st.selectbox(
        "Variável explicativa (X):",
        VARIAVEIS_NUMERICAS,
        index=1,
        key="variavel_x_correlacao",
    )

with coluna_y:
    variavel_y = st.selectbox(
        "Variável resposta (Y):",
        VARIAVEIS_NUMERICAS,
        index=4,
        key="variavel_y_correlacao",
    )

if variavel_x == variavel_y:
    st.warning(
        "Escolha duas variáveis diferentes para realizar a análise."
    )

else:
    dados_correlacao = dados[
        [variavel_x, variavel_y]
    ].dropna()

    valores_x_correlacao = (
        dados_correlacao[variavel_x].tolist()
    )

    valores_y_correlacao = (
        dados_correlacao[variavel_y].tolist()
    )

    correlacao = ms.correlacao_pearson(
        valores_x_correlacao,
        valores_y_correlacao,
    )

    valor_absoluto_correlacao = abs(correlacao)

    if valor_absoluto_correlacao < 0.3:
        intensidade = "fraca"
    elif valor_absoluto_correlacao < 0.7:
        intensidade = "moderada"
    else:
        intensidade = "forte"

    if correlacao > 0:
        direcao = "positiva"
    elif correlacao < 0:
        direcao = "negativa"
    else:
        direcao = "nula"

    st.metric(
        "Coeficiente de correlação de Pearson",
        f"{correlacao:.4f}",
    )

    st.info(
        f"A correlação observada é **{direcao}** e "
        f"**{intensidade}**. Correlação não implica causalidade."
    )
    figura_correlacao, eixo_correlacao = plt.subplots()

    eixo_correlacao.scatter(
        valores_x_correlacao,
        valores_y_correlacao,
        alpha=0.3,
        color="#2E86AB",
        s=15,
    )

    eixo_correlacao.set_xlabel(variavel_x)
    eixo_correlacao.set_ylabel(variavel_y)
    eixo_correlacao.set_title(
        f"{variavel_x} × {variavel_y}"
    )

    st.pyplot(figura_correlacao)
    plt.close(figura_correlacao)    

    # REGRESSÃO LINEAR SIMPLES

    st.subheader("Regressão linear simples")

    intercepto, inclinacao, r_quadrado = ms.regressao_linear(
        valores_x_correlacao,
        valores_y_correlacao,
    )

    st.write(
        f"Equação estimada: **Y = {intercepto:.4f} "
        f"+ ({inclinacao:.4f} × X)**"
    )

    colunas_regressao = st.columns(3)

    colunas_regressao[0].metric(
        "Intercepto",
        f"{intercepto:.4f}",
    )

    colunas_regressao[1].metric(
        "Coeficiente angular",
        f"{inclinacao:.4f}",
    )

    colunas_regressao[2].metric(
        "Coeficiente de determinação (R²)",
        f"{r_quadrado:.4f}",
    )

# GRÁFICO DA REGRESSÃO LINEAR

    menor_x = min(valores_x_correlacao)
    maior_x = max(valores_x_correlacao)

    linha_x = np.array([menor_x, maior_x])
    linha_y = intercepto + inclinacao * linha_x

    figura_regressao, eixo_regressao = plt.subplots()

    eixo_regressao.scatter(
        valores_x_correlacao,
        valores_y_correlacao,
        alpha=0.25,
        color="#2E86AB",
        s=15,
        label="Registros observados",
    )

    eixo_regressao.plot(
        linha_x,
        linha_y,
        color="#D1495B",
        linewidth=2,
        label="Reta de regressão",
    )

    eixo_regressao.set_xlabel(variavel_x)
    eixo_regressao.set_ylabel(variavel_y)
    eixo_regressao.set_title("Regressão linear simples")
    eixo_regressao.legend()

    st.pyplot(figura_regressao)
    plt.close(figura_regressao)

    valor_para_previsao = st.number_input(
        f"Informe um valor de {variavel_x} para realizar uma previsão:",
        value=float(ms.media(valores_x_correlacao)),
        key="valor_previsao_regressao",
    )

    previsao = (
        intercepto
        + inclinacao * valor_para_previsao
    )

    st.success(
        f"Para {variavel_x} = {valor_para_previsao:.2f}, "
        f"o valor previsto de {variavel_y} é "
        f"**{previsao:.2f}**."
    )

    st.caption(
        "A previsão representa uma estimativa média baseada em uma "
        "relação linear. Ela não estabelece causalidade e deve ser "
        "interpretada dentro do intervalo observado dos dados."
    )