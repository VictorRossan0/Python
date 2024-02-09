import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf
import os
import platform

def baixar_dados(tickers, inicio, fim):
    dados = yf.download(tickers, start=inicio, end=fim, progress=False)['Adj Close']
    return dados

def rastrear_carteira(tickers, pesos, inicio, fim):
    dados = baixar_dados(tickers, inicio, fim)
    retorno = dados.pct_change()
    retorno_ponderado = (retorno * pesos).sum(axis=1)
    carteira_acumulada = (1 + retorno_ponderado).cumprod()

    return carteira_acumulada

def baixar_benchmark(ticker, inicio, fim):
    benchmark = yf.download(ticker, start=inicio, end=fim, progress=False)['Adj Close']
    benchmark = benchmark / benchmark.iloc[0]
    return benchmark

def comparar_com_benchmark(carteira_acumulada, benchmark, nome_carteira='Carteira', nome_benchmark='Benchmark'):
    fig = go.Figure()

    # Adiciona as linhas da carteira e do benchmark ao gráfico
    fig.add_trace(go.Scatter(x=carteira_acumulada.index, y=carteira_acumulada, name=nome_carteira))
    fig.add_trace(go.Scatter(x=benchmark.index, y=benchmark, name=nome_benchmark))

    # Adiciona títulos e rótulos aos eixos
    fig.update_layout(
        title='Comparação com Benchmark',
        xaxis_title='Data',
        yaxis_title='Retorno Acumulado'
    )

    # Salva o gráfico como um arquivo HTML
    fig.write_html('carteira_dividendos/comparacao_benchmark.html')

    # Instrução para abrir o arquivo HTML no navegador padrão
    file_path = os.path.abspath('carteira_dividendos/comparacao_benchmark.html')

    if platform.system() == "Darwin":  # Para sistemas MacOS
        os.system(f'open {file_path}')
    elif platform.system() == "Windows":  # Para sistemas Windows
        os.system(f'start {file_path}')
    elif platform.system() == "Linux":  # Para sistemas Linux
        os.system(f'xdg-open {file_path}')

# Defina os tickers e pesos da sua carteira
tickers = ['TAEE11.SA', 'ITSA4.SA', 'BEES3.SA', 'BEES4.SA', 'SUZB3.SA']
pesos = [0.25, 0.25, 0.25, 0.25, 0.25]

# Defina o período desejado para análise
inicio = datetime(2020, 1, 1)
fim = datetime(2023, 1, 1)

# Rastreia a carteira
carteira_acumulada = rastrear_carteira(tickers, pesos, inicio, fim)

# Baixe o benchmark (Ibovespa)
ibovespa = baixar_benchmark('^BVSP', inicio, fim)

# Compare com o benchmark e plote o desempenho
comparar_com_benchmark(carteira_acumulada, ibovespa, nome_carteira='Minha Carteira', nome_benchmark='Ibovespa')