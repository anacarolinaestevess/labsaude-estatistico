
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

st.caption(
    "As medidas exibidas são calculadas pelas funções "
    "próprias do arquivo minhastats.py."
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
    "A simulação mostra como a média observada se aproxima da média "
    "teórica à medida que o tamanho da amostra aumenta."
)

tamanho_amostra = st.slider(
    "Número de observações da simulação:",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100,
)

media_teorica = 50
desvio_teorico = 10

gerador = np.random.default_rng(seed=42)

amostra_simulada = gerador.normal(
    loc=media_teorica,
    scale=desvio_teorico,
    size=tamanho_amostra,
)

medias_acumuladas = []

for tamanho_atual in range(1, tamanho_amostra + 1):
    media_atual = ms.media(
        amostra_simulada[:tamanho_atual].tolist()
    )
    medias_acumuladas.append(media_atual)

    # GRÁFICO DA SIMULAÇÃO

figura_lgn, eixo_lgn = plt.subplots()

eixo_lgn.plot(
    range(1, tamanho_amostra + 1),
    medias_acumuladas,
    color="#2E86AB",
    label="Média acumulada",
)

eixo_lgn.axhline(
    media_teorica,
    color="#D1495B",
    linestyle="--",
    label="Média teórica",
)

eixo_lgn.set_xlabel("Tamanho da amostra")
eixo_lgn.set_ylabel("Média acumulada")
eixo_lgn.set_title("Convergência da média amostral")
eixo_lgn.legend()

st.pyplot(figura_lgn)
plt.close(figura_lgn)

st.write(
    f"Com **{tamanho_amostra} observações**, a média obtida foi "
    f"**{medias_acumuladas[-1]:.2f}**, enquanto a média teórica "
    f"da distribuição é **{media_teorica:.2f}**."
)

# TEOREMA CENTRAL DO LIMITE

st.subheader("Teorema Central do Limite")

st.write(
    "Nesta simulação, retiramos várias amostras de uma população "
    "exponencial e calculamos a média de cada amostra."
)

coluna_tamanho, coluna_repeticoes = st.columns(2)

with coluna_tamanho:
    tamanho_cada_amostra = st.slider(
        "Tamanho de cada amostra:",
        min_value=2,
        max_value=200,
        value=30,
        step=1,
    )

with coluna_repeticoes:
    numero_repeticoes = st.slider(
        "Número de amostras simuladas:",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
    )

media_populacional = 10

gerador_tcl = np.random.default_rng(seed=42)

medias_amostrais = []

for _ in range(numero_repeticoes):
    amostra = gerador_tcl.exponential(
        scale=media_populacional,
        size=tamanho_cada_amostra,
    )

    medias_amostrais.append(
        ms.media(amostra.tolist())
    )

 # GRÁFICO DA SIMULAÇÃO

figura_tcl, eixo_tcl = plt.subplots()

eixo_tcl.hist(
    medias_amostrais,
    bins=30,
    density=True,
    color="#7AC7C4",
    edgecolor="white",
    label="Médias simuladas",
)

erro_padrao = media_populacional / math.sqrt(tamanho_cada_amostra)

valores_x = np.linspace(
    min(medias_amostrais),
    max(medias_amostrais),
    300,
)

densidade_normal = (
    1 / (erro_padrao * math.sqrt(2 * math.pi))
    * np.exp(
        -0.5
        * ((valores_x - media_populacional) / erro_padrao) ** 2
    )
)

eixo_tcl.plot(
    valores_x,
    densidade_normal,
    color="#D1495B",
    linewidth=2,
    label="Distribuição normal teórica",
)

eixo_tcl.axvline(
    media_populacional,
    color="black",
    linestyle="--",
    label="Média populacional",
)

eixo_tcl.set_xlabel("Média amostral")
eixo_tcl.set_ylabel("Densidade")
eixo_tcl.set_title("Distribuição das médias amostrais")
eixo_tcl.legend()

st.pyplot(figura_tcl)
plt.close(figura_tcl)

media_das_medias = ms.media(medias_amostrais)

st.info(
    f"A população original é assimétrica, mas a distribuição das "
    f"médias torna-se aproximadamente normal. A média das médias "
    f"foi {media_das_medias:.2f}, próxima da média populacional "
    f"teórica de {media_populacional:.2f}."
)