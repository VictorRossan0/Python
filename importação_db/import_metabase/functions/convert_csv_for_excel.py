import os
import pandas as pd
from datetime import datetime

caminho_arquivo = 'C:\\Users\\Hitss\\Downloads\\test.csv'
diretorio_arquivo = os.path.dirname(caminho_arquivo)
df = pd.read_csv(caminho_arquivo, sep=';', decimal=',')

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nome_arquivo = f'test_{timestamp}.xlsx'
caminho_arquivo_excel = os.path.join(diretorio_arquivo, nome_arquivo)

df.to_excel(caminho_arquivo_excel, index=False)

print(f"Arquivo '{nome_arquivo}' salvo em '{diretorio_arquivo}' com sucesso.")
