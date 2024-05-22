import pandas as pd

# Ler o arquivo Excel em um DataFrame chamado df
df = pd.read_excel('test.xlsx')

# Verificar os tipos de dados das colunas
tipos_de_dados = df.dtypes
print(tipos_de_dados)
