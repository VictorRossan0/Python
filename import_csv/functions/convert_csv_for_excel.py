import pandas as pd

# Especificar o caminho completo para o arquivo CSV
caminho_arquivo = 'C:\\Users\\Hitss\\Downloads\\Atualizacao_metabase_20240416.csv'

# Ler o arquivo CSV com separador ';' e decimal ','
df = pd.read_csv(caminho_arquivo, sep=';', decimal=',')

# Salvar como arquivo Excel
df.to_excel('test.xlsx', index=False)
