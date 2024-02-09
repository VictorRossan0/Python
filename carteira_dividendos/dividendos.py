import yfinance as yf
import plotly.express as px

# Obtém dados
papel = yf.Ticker('WEGE3.SA')
dados = papel.history(start='2022-01-01', end='2024-01-01')

# Filtra dividendos diferentes de zero
dividendos = dados.Dividends[dados.Dividends != 0]

# Cria um gráfico de barras interativo com Plotly Express
fig = px.bar(dividendos, labels={'value': 'Dividendos'}, title='Dividendos por Mês')
fig.update_layout(xaxis_tickangle=0)

# Exibe o gráfico interativo em um navegador
fig.show()