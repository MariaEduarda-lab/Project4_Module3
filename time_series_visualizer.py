import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
np.float = float  # Corrige erro de compatibilidade com NumPy >= 1.20 (np.float foi removido)

# Importando dataframe, garantindo que as datas estarão em formato correto
# parse_dates=['date']: converte a coluna 'date' para tipo datetime
# index_col='date': define a coluna de data como índice do DataFrame (ótimo para séries temporais)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Remover primeiro quartil e terceiro quartil
# Filtra os dados para manter apenas os valores entre o percentil 2.5% e 97.5%
# Isso remove os outliers extremos (2,5% menores e 2,5% maiores valores)
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Criar uma figura e um eixo para o gráfico de linhas
    # figsize define o tamanho do gráfico (12 polegadas de largura, 6 de altura)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plotar os dados: índice (datas) no eixo X, valores (visualizações) no eixo Y
    # Linha vermelha com largura 1 para melhor visualização
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    # Definir título e rótulos dos eixos conforme exigido pelo projeto
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')           # Rótulo do eixo X
    ax.set_ylabel('Page Views')     # Rótulo do eixo Y

    # Salvar a figura como arquivo PNG
    fig.savefig('line_plot.png')
    
    # Retornar o objeto fig (necessário para os testes)
    return fig


def draw_bar_plot():
    # Fazer uma cópia dos dados limpos para não alterar o df original
    df_bar = df.copy()
    
    # Resetar o índice para poder acessar a coluna 'date' como uma coluna comum
    df_bar.reset_index(inplace=True)

    # Extrair o ano e o nome do mês de cada data
    df_bar['year'] = df_bar['date'].dt.year                    # Ano como número
    df_bar['month'] = df_bar['date'].dt.month_name()          # Nome completo do mês (ex: January)

    # Definir a ordem correta dos meses para garantir que apareçam na ordem certa no gráfico
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Transformar a coluna 'month' em categórica com ordem fixa
    # Isso garante que os meses apareçam na ordem cronológica, não alfabética
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Agrupar por ano e mês, calcular a média de visualizações diárias
    # .unstack(): transforma os meses em colunas para criar barras coloridas por mês
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Criar figura e eixo para o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotar gráfico de barras com legendas
    df_bar.plot(kind='bar', ax=ax, legend=True)

    # Definir rótulos dos eixos
    ax.set_xlabel('Years')                    # Rótulo do eixo X
    ax.set_ylabel('Average Page Views')       # Rótulo do eixo Y
    
    # Definir título da legenda
    ax.legend(title='Months', labels=month_order)

    # Corrigir os rótulos da legenda (garantir que apareçam na ordem certa)
    handles, _ = ax.get_legend_handles_labels()  # Pega os elementos da legenda
    ax.legend(handles, month_order, title='Months')  # Reaplica com a ordem correta

    # Salvar a figura
    fig.savefig('bar_plot.png')
    
    # Retornar o objeto fig
    return fig


def draw_box_plot():
    # Preparar dados para os gráficos de caixa
    # Fazer cópia e resetar índice para acessar a coluna 'date'
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # Extrair o ano diretamente da data
    df_box['year'] = [d.year for d in df_box.date]
    
    # Extrair o mês abreviado (ex: Jan, Feb) usando strftime('%b')
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Criar figura com dois subgráficos lado a lado (1 linha, 2 colunas)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    ax1, ax2 = axes  # Primeiro e segundo gráfico

    # Primeiro gráfico: Box plot por ano (tendência ao longo dos anos)
    sns.boxplot(data=df_box, x='year', y='value', ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')     # Título do gráfico
    ax1.set_xlabel('Year')                          # Rótulo do eixo X
    ax1.set_ylabel('Page Views')                    # Rótulo do eixo Y

    # Segundo gráfico: Box plot por mês (sazonalidade)
    # Definir a ordem dos meses para começar em Jan e seguir a ordem correta
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Usar seaborn para criar o gráfico, com ordem personalizada dos meses
    sns.boxplot(data=df_box, x='month', y='value', ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')  # Título do gráfico
    ax2.set_xlabel('Month')                             # Rótulo do eixo X
    ax2.set_ylabel('Page Views')                        # Rótulo do eixo Y

    # Salvar a figura como PNG
    fig.savefig('box_plot.png')
    
    # Retornar o objeto fig (esperado pelos testes)
    return fig