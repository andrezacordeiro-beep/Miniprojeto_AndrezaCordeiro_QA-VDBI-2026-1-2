
# BIBLIOTECAS ESSENCIAIS

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

"""Modulos necessários do Python
- Pandas
- Numpy
- Datetime
"""

"""SCRIPT DE ETL E LIMPEZA DE DADOS 
Objetivo: Análise Exploratória da base Varejo seguindo etapas claras, documentadas e reproduzíveis.

- Verificar e reportar ao menos dois problemas básicos: valores nulos por coluna, duplicatas e possíveis inconsistências (ex.: datas inválidas ou categorias vazias).
- Descarte de linhas com campos vazios ou nulos nas colunas PR_CAT: Categoria do produto adquirido e PR_NOME: Nome do produto adquirido, 
pois são essenciais para análises de vendas e comportamento do consumidor na escolha de produtos;
- Eliminar duplicatas relevantes CO_ID: Identificação do número de compra (número da nota fiscal) constando mesmo cliente,
data e produto (ex.: mesmo cliente comprando o mesmo produto no mesmo dia, indicando possível erro de digitação ou registro duplicado, o que pode distorcer análises de vendas e comportamento do consumidor);
- Ajustar tipos de dados (ex.: converter coluna DATA para datetime).
- Gerar estatísticas descritivas básicas para coluna de número de filhos do cliente (média; mediana; desvio padrão; moda; máximo; mínimo e contagem).
- Explorar padrões de agrupamento com pelo menos dois agrupamentos (por exemplo: gênero com mais vendas, compras), usando groupby().
- Salvar o DataFrame limpo como CSV."""
 
print("Carregamento de dados(extração)")  

# ============================================================
# 1. CARREGAMENTO DOS DADOS (EXTRATAÇÃO)
#    Objetivo: Importar a base bruta (raw) e informações iniciais sobre os dados.
# ============================================================

caminho_entrada = r"C:\Users\ANDREZA\Desktop\Miniprojeto_AndrezaCordeiro_QA VDBI 20261 2\base_varejo.csv"

varejo_csv = pd.read_csv(caminho_entrada, na_values=['#N/D'], sep=";")

print("Informações sobre os dados:")

# Mostrar quantos registros foram exportados
print("Quantidade de registros exportados:", len(varejo_csv))
# Verificar o número de linhas e colunas
print(varejo_csv.shape)
# Verificar os tipos de dados
print(varejo_csv.dtypes)
# Mostrar as primeiras linhas do DataFrame
print(varejo_csv.head())
# Mostrar informações gerais sobre o DataFrame
print(varejo_csv.info())
# Exibe o cabeçalho de cada coluna
print(varejo_csv.columns)


# ============================================================
# 2. SANEAMENTO FILTRAGEM E IMPUTAÇÃO DE DADOS
# ============================================================

print("[Etapa 2] Removendo valores nulos, duplicatas e ajustando tipos de dados.")
# Percentual de nulos por coluna


def calcular_percentual_nulos(varejo_csv):
    percentual_nulos = varejo_csv.isnull().mean() * 100
    return percentual_nulos


percentual_nulos = calcular_percentual_nulos(varejo_csv)
print("Percentual de valores nulos por coluna:")
print(percentual_nulos)

# Ordenando do maior para o menor
percentual_nulos = percentual_nulos.sort_values(ascending=False)
print("Percentual de valores ausentes por coluna:")
print(percentual_nulos.round())

# Remover linhas com qualquer nulo
varejo_csv_sem_nulos = varejo_csv.dropna()

print("Nulos restantes:", varejo_csv_sem_nulos.isnull().sum())


# Remoção de duplicatas parcial: mesma "DATA","CO_ID", "CL_ID", "PR_ID"

def print_duplicatas(varejo_csv, varejo_csv_name):
    print(f"Linhas antes: {len(varejo_csv)}")
    varejo_csv_sem_dup_parcial = varejo_csv.drop_duplicates(
        subset=["DATA","CO_ID", "CL_ID", "PR_ID"],
        keep="first"
    )
    print(f"Linhas depois: {len(varejo_csv_sem_dup_parcial)}")
    return varejo_csv_sem_dup_parcial  


varejo_csv_sem_dup_parcial = print_duplicatas(varejo_csv, "varejo_csv")

# TRATAMENTO DE DATAS
# Objetivo: Garantir que a coluna Data esteja no formato
datetime
varejo_csv['DATA'] = pd.to_datetime(varejo_csv['DATA'], dayfirst=True)
# Converte a coluna 'Data' para formato datetime considerando dia primeiro (padrão brasileiro)
print("Tipos de dados após ajuste:")
print(varejo_csv.dtypes)

# ============================================================
# 3. ANÁLISE ESTATÍSTICA E AGRUPAMENTOS
# ============================================================

# Estatísticas descritivas para a coluna de número de filhos do cliente
print("[Etapa 3] Estatísticas descritivas.")

minha_lista = [0, 1, 2, 3, 4]
CL_FHL = np.mean(minha_lista)

print("Estatísticas descritivas para a coluna 'CL_FHL':")
print("Média:", varejo_csv_sem_dup_parcial['CL_FHL'].mean())
print("Mediana:", varejo_csv_sem_dup_parcial['CL_FHL'].median())
print("Desvio Padrão:", varejo_csv_sem_dup_parcial['CL_FHL'].std())
print("Moda:", varejo_csv_sem_dup_parcial['CL_FHL'].mode()[0]if not varejo_csv_sem_dup_parcial['CL_FHL'].mode().empty else "Sem moda")   # A moda pode retornar mais de um valor, pegamos o primeiro
print("Máximo:", varejo_csv_sem_dup_parcial['CL_FHL'].max())
print("Mínimo:", varejo_csv_sem_dup_parcial['CL_FHL'].min())
print("Contagem:", varejo_csv_sem_dup_parcial['CL_FHL'].count())  # Contagem de valores não nulos

# Total de notas de vendas por genero.


def contar_notas_por_genero(df):
    notas_por_genero = varejo_csv_sem_dup_parcial.groupby('CL_GENERO')['CO_ID'].count()
    return notas_por_genero


notas_por_genero = contar_notas_por_genero(varejo_csv_sem_dup_parcial)
print("Total de notas de vendas por gênero:")
print(notas_por_genero)

# Total de notas de vendas por categoria de produto.


def contar_notas_por_categoria(varejo_csv_sem_dup_parcial):
    notas_por_categoria = varejo_csv_sem_dup_parcial.groupby('CO_ID')['PR_CAT'].count().sort_values(ascending=False)
    return notas_por_categoria


notas_por_categoria = contar_notas_por_categoria(varejo_csv_sem_dup_parcial)
print("Total de notas por categoria:")
print(notas_por_categoria)


def contar_variacoes_de_categoria_por_datas(varejo_csv_sem_dup_parcial):
    variacoes_de_categoria_por_datas = varejo_csv_sem_dup_parcial.groupby('DATA')['PR_CAT'].count().head(10).sort_values(ascending=False)  # Limitado a 10 para não lotar o terminal
    return variacoes_de_categoria_por_datas


contar_variacoes_de_categoria_por_datas = contar_variacoes_de_categoria_por_datas(varejo_csv_sem_dup_parcial)
print("Total de variações de categoria por datas:")
print(contar_variacoes_de_categoria_por_datas)


# ============================================================
# 4. CONCLUSÕES E INSIGHTS (Requisito do Mini-Projeto)
# ============================================================
print("[Etapa 4] Bloco de Conclusões e Insights ---")
conclusoes = """
1. Qualidade da Base: Foram identificadas e removidas linhas duplicadas e registros nulos em colunas essenciais (PR_CAT e PR_NOME).
2. Perfil Familiar: A análise descritiva da coluna 'CL_FHL' indicou que a maior parte dos clientes possui um perfil de [0] filhos (conforme o resultado da Moda/Mediana).
3. Preferência por Gênero: O gênero [F- Feminino] representa a maior volumetria de compras no período analisado.
4. Categorias de Destaque: A categoria de produto [PR_ID:81 = Higiene] é o principal motor de vendas do varejo em volume de transações.
5. Maior variação de categorias por datas: A data [2020-12-01] apresentou a maior variação de categorias, indicando um possível evento promocional ou sazonalidade que impactou as vendas.

"""

#==============================================================
# 5.Salvar como CSV
#==============================================================

print("[Etapa 5] Salvando o DataFrame limpo como CSV.")

varejo_csv_sem_dup_parcial.to_csv("varejo_limpo.csv",index=False)
