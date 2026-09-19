from pathlib import Path

import pandas as pd
from dbfread import DBF
from pyreaddbc.readdbc import dbc2dbf


# Define os caminhos dos arquivos
ARQUIVO_DBC = Path("dados/brutos/RDDF2501.dbc")
PASTA_PROCESSADOS = Path("dados/processados")
ARQUIVO_DBF = PASTA_PROCESSADOS / "RDDF2501.dbf"


# Verifica se o arquivo original existe
if not ARQUIVO_DBC.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {ARQUIVO_DBC}"
    )


# Cria a pasta de dados processados
PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)


# Converte o arquivo DBC em DBF
if not ARQUIVO_DBF.exists():
    print("Convertendo o arquivo DBC para DBF...")

    dbc2dbf(
        str(ARQUIVO_DBC),
        str(ARQUIVO_DBF)
    )


# Lê o arquivo DBF e transforma em uma tabela do Pandas
tabela_dbf = DBF(
    str(ARQUIVO_DBF),
    encoding="latin-1",
    load=True
)

dados = pd.DataFrame(iter(tabela_dbf))


# Apresenta informações básicas
print("\nArquivo lido com sucesso!")
print(f"Número de internações: {dados.shape[0]}")
print(f"Número de variáveis: {dados.shape[1]}")

print("\nPrimeiras cinco linhas:")
print(dados.head())

print("\nNomes das variáveis:")
print(dados.columns.tolist())

# Variáveis inicialmente selecionadas para o laboratório
VARIAVEIS_SELECIONADAS = [
    "IDADE",
    "DIAS_PERM",
    "QT_DIARIAS",
    "UTI_MES_TO",
    "VAL_TOT",
    "VAL_UTI",
    "NUM_PROC",
    "SEXO",
    "RACA_COR",
    "CAR_INT",
    "DIAG_PRINC",
    "PROC_REA",
    "COMPLEX",
    "MORTE",
]

dados_selecionados = dados[VARIAVEIS_SELECIONADAS].copy()


print("\nTipos das variáveis selecionadas:")
print(dados_selecionados.dtypes)

print("\nQuantidade de valores ausentes:")
print(dados_selecionados.isna().sum())

print("\nQuantidade de valores distintos:")
print(dados_selecionados.nunique())


VARIAVEIS_CATEGORICAS = [
    "SEXO",
    "RACA_COR",
    "CAR_INT",
    "COMPLEX",
    "MORTE",
]

for variavel in VARIAVEIS_CATEGORICAS:
    print(f"\nFrequências de {variavel}:")
    print(dados_selecionados[variavel].value_counts(dropna=False))# Variáveis inicialmente selecionadas para o laboratório
VARIAVEIS_SELECIONADAS = [
    "IDADE",
    "DIAS_PERM",
    "QT_DIARIAS",
    "UTI_MES_TO",
    "VAL_TOT",
    "VAL_UTI",
    "NUM_PROC",
    "SEXO",
    "RACA_COR",
    "CAR_INT",
    "DIAG_PRINC",
    "PROC_REA",
    "COMPLEX",
    "MORTE",
]

dados_selecionados = dados[VARIAVEIS_SELECIONADAS].copy()


print("\nTipos das variáveis selecionadas:")
print(dados_selecionados.dtypes)

print("\nQuantidade de valores ausentes:")
print(dados_selecionados.isna().sum())

print("\nQuantidade de valores distintos:")
print(dados_selecionados.nunique())


VARIAVEIS_CATEGORICAS = [
    "SEXO",
    "RACA_COR",
    "CAR_INT",
    "COMPLEX",
    "MORTE",
]

for variavel in VARIAVEIS_CATEGORICAS:
    print(f"\nFrequências de {variavel}:")
    print(dados_selecionados[variavel].value_counts(dropna=False))

    # Variáveis selecionadas para o laboratório
VARIAVEIS_SELECIONADAS = [
    "IDADE",
    "DIAS_PERM",
    "QT_DIARIAS",
    "UTI_MES_TO",
    "VAL_TOT",
    "VAL_UTI",
    "NUM_PROC",
    "SEXO",
    "RACA_COR",
    "CAR_INT",
    "DIAG_PRINC",
    "PROC_REA",
    "COMPLEX",
    "MORTE",
]

dados_selecionados = dados[VARIAVEIS_SELECIONADAS].copy()

print("\nTipos das variáveis selecionadas:")
print(dados_selecionados.dtypes)

print("\nQuantidade de valores ausentes:")
print(dados_selecionados.isna().sum())

print("\nQuantidade de valores distintos:")
print(dados_selecionados.nunique())

VARIAVEIS_CATEGORICAS = [
    "SEXO",
    "RACA_COR",
    "CAR_INT",
    "COMPLEX",
    "MORTE",
]

for variavel in VARIAVEIS_CATEGORICAS:
    print(f"\nFrequências de {variavel}:")
    print(dados_selecionados[variavel].value_counts(dropna=False))

print("\nFrequências do código da idade:")
print(dados["COD_IDADE"].value_counts(dropna=False))

print("\nFaixa da variável IDADE por código:")
print(
    dados.groupby("COD_IDADE")["IDADE"]
    .agg(["min", "max", "count"])
)

# Cria a base final utilizada pelo laboratório
dados_finais = dados[
    [
        "IDADE",
        "COD_IDADE",
        "DIAS_PERM",
        "QT_DIARIAS",
        "UTI_MES_TO",
        "VAL_TOT",
        "VAL_UTI",
        "SEXO",
        "RACA_COR",
        "CAR_INT",
        "DIAG_PRINC",
        "PROC_REA",
        "COMPLEX",
        "MORTE",
    ]
].copy()


def converter_idade_para_anos(linha):
    """Converte a idade do SIH/SUS para uma única unidade: anos."""
    idade = linha["IDADE"]
    codigo = linha["COD_IDADE"]

    if codigo == "2":
        return idade / 365

    if codigo == "3":
        return idade / 12

    if codigo == "4":
        return idade

    if codigo == "5":
        return 100 + idade

    return None


dados_finais["idade_anos"] = dados_finais.apply(
    converter_idade_para_anos,
    axis=1
)


# Traduz códigos categóricos para rótulos compreensíveis
dados_finais["SEXO"] = dados_finais["SEXO"].map(
    {
        "1": "Masculino",
        "3": "Feminino",
    }
)

dados_finais["RACA_COR"] = dados_finais["RACA_COR"].map(
    {
        "01": "Branca",
        "02": "Preta",
        "03": "Parda",
        "04": "Amarela",
        "05": "Indígena",
        "99": "Sem informação",
    }
)

dados_finais["CAR_INT"] = dados_finais["CAR_INT"].map(
    {
        "01": "Eletiva",
        "02": "Urgência",
        "03": "Acidente no local de trabalho",
        "04": "Acidente no trajeto para o trabalho",
        "05": "Outros acidentes de trânsito",
        "06": "Outras lesões e envenenamentos",
    }
)

dados_finais["COMPLEX"] = dados_finais["COMPLEX"].map(
    {
        "02": "Média complexidade",
        "03": "Alta complexidade",
    }
)

dados_finais["MORTE"] = dados_finais["MORTE"].map(
    {
        0: "Não",
        1: "Sim",
    }
)


# Remove as colunas originais da idade e renomeia as demais
dados_finais = dados_finais.drop(
    columns=["IDADE", "COD_IDADE"]
)

dados_finais = dados_finais.rename(
    columns={
        "DIAS_PERM": "dias_permanencia",
        "QT_DIARIAS": "quantidade_diarias",
        "UTI_MES_TO": "dias_uti",
        "VAL_TOT": "valor_total",
        "VAL_UTI": "valor_uti",
        "SEXO": "sexo",
        "RACA_COR": "raca_cor",
        "CAR_INT": "carater_internacao",
        "DIAG_PRINC": "diagnostico_principal",
        "PROC_REA": "procedimento_realizado",
        "COMPLEX": "complexidade",
        "MORTE": "obito",
    }
)


# Organiza a ordem das colunas
dados_finais = dados_finais[
    [
        "idade_anos",
        "dias_permanencia",
        "quantidade_diarias",
        "dias_uti",
        "valor_total",
        "valor_uti",
        "sexo",
        "raca_cor",
        "carater_internacao",
        "diagnostico_principal",
        "procedimento_realizado",
        "complexidade",
        "obito",
    ]
]


# Salva o conjunto final em CSV
ARQUIVO_CSV = Path(
    "dados/internacoes_sih_df_janeiro_2025.csv"
)

dados_finais.to_csv(
    ARQUIVO_CSV,
    index=False,
    encoding="utf-8-sig"
)

print("\nBase final criada com sucesso!")
print(f"Local: {ARQUIVO_CSV}")
print(f"Dimensão: {dados_finais.shape}")
print("\nTipos das variáveis finais:")
print(dados_finais.dtypes)