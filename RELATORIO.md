# Relatório do Laboratório Estatístico Interativo

## 1. Identificação

**Autora:** Ana Carolina Esteves da Silva Pereira
**Projeto:** LabSaúde SUS  
**Base de dados:** Sistema de Informações Hospitalares do SUS (SIH/SUS)  
**Recorte:** Distrito Federal, competência janeiro de 2025

## 2. Objetivo

Desenvolver um laboratório estatístico interativo em Python para aplicar conceitos de estatística descritiva, simulação de Monte Carlo, distribuições de probabilidade, correlação e regressão linear a dados públicos de saúde.

## 3. Base de dados

Foram utilizados dados públicos do Sistema de Informações Hospitalares do SUS, disponibilizados pelo DATASUS. O arquivo analisado contém registros de Autorizações de Internação Hospitalar do Distrito Federal referentes à competência janeiro de 2025.

A base original possuía 20.996 registros e 113 variáveis. Após o processamento, foram selecionadas 13 variáveis relevantes para o projeto:

- idade em anos;
- dias de permanência;
- quantidade de diárias;
- dias de UTI;
- valor total da AIH;
- valor de UTI;
- sexo;
- raça/cor;
- caráter da internação;
- diagnóstico principal;
- procedimento realizado;
- complexidade;
- ocorrência de óbito.

Cada linha representa um registro de AIH. Portanto, os dados não representam necessariamente pessoas únicas, pois uma mesma pessoa pode possuir mais de uma AIH.

## 4. Preparação dos dados

O arquivo original foi obtido no formato DBC. A conversão para DBF foi realizada com o pacote `pyreaddbc`, e a leitura foi feita com `dbfread` e `pandas`.

Foram selecionadas e renomeadas as variáveis utilizadas no projeto. A idade foi convertida para anos considerando o código da unidade de idade presente no SIH/SUS. As variáveis categóricas também receberam rótulos para facilitar sua interpretação.

A base processada possui 20.996 linhas, 13 colunas e não apresenta valores ausentes nas variáveis selecionadas.

## 5. Métodos estatísticos

Foi desenvolvido o módulo próprio `minhastats.py`, contendo implementações das seguintes medidas:

- média;
- mediana;
- moda;
- amplitude;
- variância populacional e amostral;
- desvio-padrão populacional e amostral;
- percentis;
- quartis;
- coeficiente de variação;
- covariância;
- correlação de Pearson;
- regressão linear simples por mínimos quadrados;
- coeficiente de determinação.

As funções foram verificadas por testes automatizados com `pytest` e comparadas, quando pertinente, com resultados do NumPy e do SciPy.

O aplicativo também apresenta tabelas de frequências, histogramas, boxplots, gráficos de barras e setores, além da identificação de valores extremos pelo método do intervalo interquartil.

Foram implementadas simulações da Lei dos Grandes Números e do Teorema Central do Limite por reamostragem, com reposição, dos valores totais das AIH.

Também foram incluídas aplicações interativas das distribuições Normal e Binomial.

## 6. Principais descobertas

### 6.1 AIH com registro de óbito

As AIH com registro de óbito apresentaram maior utilização de recursos e maior permanência hospitalar.

O valor médio dessas AIH foi de R$ 5.062,24, aproximadamente 3,4 vezes o valor médio das AIH sem óbito, de R$ 1.490,10.

A permanência média foi de 12,44 dias nas AIH com óbito e de 5,62 dias naquelas sem óbito. O número médio de dias em UTI foi de 5,03 e 0,56, respectivamente.

Esses resultados representam associações descritivas e não permitem concluir que uma dessas características tenha causado as demais.

### 6.2 Complexidade e valor da AIH

As AIH de alta complexidade apresentaram valor médio de R$ 8.125,97, enquanto as de média complexidade apresentaram valor médio de R$ 1.172,13. Assim, o valor médio da alta complexidade foi quase sete vezes maior.

Apesar da diferença de custo, a permanência média foi semelhante: 5,09 dias na alta complexidade e 5,88 dias na média complexidade.

O uso médio de UTI foi de 1,29 dia na alta complexidade e de 0,66 dia na média complexidade. Os resultados sugerem que a diferença de valor não é explicada apenas pela permanência hospitalar, podendo estar relacionada à intensidade assistencial e aos procedimentos realizados.

### 6.3 Permanência e valor total

Foi observada correlação linear positiva moderada entre o número de dias de permanência e o valor total da AIH, com coeficiente de Pearson igual a 0,3675.

A regressão linear estimou um acréscimo médio de R$ 203,57 no valor total para cada dia adicional de permanência.

O coeficiente de determinação foi de 0,1351. Portanto, o modelo linear com dias de permanência explicou 13,51% da variação observada no valor total das AIH. Isso indica que outros fatores também possuem papel importante na determinação dos valores.

## 7. Limitações

A análise apresenta as seguintes limitações:

- utilização de apenas uma competência mensal e uma unidade da Federação;
- análise de registros de AIH, e não de pessoas únicas;
- possibilidade de erros ou diferenças de preenchimento nos dados administrativos;
- ausência de ajuste por diagnóstico, procedimento, gravidade e outras características clínicas;
- resultados descritivos, sem possibilidade de estabelecer relações causais;
- a regressão linear simples pode não representar integralmente relações assimétricas ou não lineares.

## 8. Conclusão

O projeto permitiu aplicar conceitos estatísticos a uma base pública real do SUS e demonstrou como ferramentas computacionais podem apoiar a exploração de dados hospitalares.

Os resultados mostraram diferenças importantes nos valores e na utilização de recursos segundo ocorrência de óbito e complexidade assistencial. Também mostraram que a permanência hospitalar possui associação positiva com o valor total, embora explique apenas parte de sua variação.

O aplicativo possibilita explorar as variáveis de forma interativa e visualizar conceitos estatísticos por meio de dados reais e simulações.