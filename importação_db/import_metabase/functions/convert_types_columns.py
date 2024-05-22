import pandas as pd
import numpy as np

# Ler o arquivo Excel em um DataFrame
df = pd.read_excel('test.xlsx')

# Remover o símbolo de porcentagem da coluna 'EBITDA Real Mensal'
df['EBITDA Real Mensal'] = df['EBITDA Real Mensal'].str.replace('%', '')
df['EBITDA Real Consolidado'] = df['EBITDA Real Consolidado'].str.replace('%', '')

# Substituir vírgulas por pontos na coluna 'EBITDA Real Mensal'
df['EBITDA Real Mensal'] = df['EBITDA Real Mensal'].str.replace(',', '.')
df['EBITDA Real Consolidado'] = df['EBITDA Real Consolidado'].str.replace(',', '.')

df['EBITDA Real Mensal'] = df['EBITDA Real Mensal'].astype(np.float64)  # Decimal
df['EBITDA Real Consolidado'] = df['EBITDA Real Consolidado'].astype(np.float64)  # Decimal

# Salvar o DataFrame modificado em um novo arquivo Excel
df.to_excel('colunas_convertidas.xlsx', index=False)