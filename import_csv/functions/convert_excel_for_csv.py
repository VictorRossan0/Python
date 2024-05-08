import pandas as pd

# Ler o arquivo Excel em um DataFrame
df = pd.read_excel('colunas_convertidas.xlsx')

# Salvar o DataFrame em um arquivo CSV
df.to_csv('dados_convertidos.csv', index=False, encoding='utf-8-sig')