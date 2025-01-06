import os
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows

def gerar_grafico_dividendos(ativo: str, df: pd.DataFrame, diretorio: str = "graficos"):
    """
    Gera um gráfico de dividendos para o ativo e salva no diretório especificado.
    
    :param ativo: Nome do ativo (ex: "MXRF11").
    :param df: DataFrame com os dados do ativo.
    :param diretorio: Diretório onde a imagem será salva.
    """
    # Garantir que o diretório exista
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ativos = df["Ativo/FII"].unique()
    
    # Gerar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df['Quantidade'], df['Total Recebido (R$)'], marker='o', color='b', label=df["Ativo/FII"])
    plt.title(f"Dividendos de {ativo}")
    plt.xlabel('Quantidade de Cotas/Ações')
    plt.ylabel('Total Recebido (R$)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Salvar o gráfico no diretório "graficos"
    caminho_imagem = os.path.join(diretorio, f"grafico_dividendos_{ativo}.png")
    plt.savefig(caminho_imagem)
    plt.close()
    print(f"Gráfico gerado e salvo em: {caminho_imagem}")
    return caminho_imagem


def adicionar_graficos_excel(writer, df_dados: pd.DataFrame, diretorio: str = "graficos"):
    """
    Adiciona gráficos gerados ao arquivo Excel.
    
    :param writer: Objeto de escrita do Excel.
    :param df_dados: DataFrame contendo os dados dos ativos.
    :param diretorio: Diretório onde os gráficos estão salvos.
    """
    # Aba "Gráficos"
    wb = writer.book
    ws = wb.create_sheet("Gráficos")
    
    # Gerar e adicionar gráficos para cada ativo
    for i, ativo in enumerate(df_dados['Ativo/FII'].unique()):
        # Filtrar dados do ativo
        df_ativo = df_dados[df_dados['Ativo/FII'] == ativo]
        
        # Gerar gráfico e obter o caminho da imagem
        caminho_imagem = gerar_grafico_dividendos(ativo, df_ativo, diretorio)
        
        # Inserir o gráfico na planilha
        img = Image(caminho_imagem)
        img.anchor = f'A{1 + i * 15}'  # Coloca o gráfico em uma posição espaçada
        ws.add_image(img)
        print(f"Gráfico do {ativo} inserido no Excel.")


def salvar_em_excel(dados: list, relatorio_rentabilidade: list, nome_arquivo: str = "relatorio_dividendos.xlsx"):
    """
    Salva os dados e o relatório de rentabilidade em um arquivo Excel, gerando gráficos e anexando-os ao relatório.

    :param dados: Lista de dicionários contendo os dados dos ativos.
    :param relatorio_rentabilidade: Lista de dicionários contendo os dados de rentabilidade.
    :param nome_arquivo: Nome do arquivo Excel a ser gerado.
    """
    # Converter listas para DataFrames
    df_dados = pd.DataFrame(dados)
    df_rentabilidade = pd.DataFrame(relatorio_rentabilidade)

    # Verificar se a coluna 'Ativo/FII' está presente
    if 'Ativo/FII' not in df_dados.columns:
        print("Erro: A coluna 'Ativo/FII' não foi encontrada no DataFrame.")
        return

    # Salvar dados e rentabilidade no Excel
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        # Aba "Dados"
        df_dados.to_excel(writer, index=False, sheet_name="Dados")

        # Aba "Rentabilidade"
        df_rentabilidade.to_excel(writer, index=False, sheet_name="Rentabilidade")

        # Adicionar gráficos ao Excel (aba "Gráficos")
        adicionar_graficos_excel(writer, df_dados)

    print(f"Relatório Excel salvo: {nome_arquivo}")


def carregar_relatorio_excel(nome_arquivo: str = "relatorio_dividendos.xlsx") -> pd.DataFrame:
    """
    Carrega os dados de um arquivo Excel existente.

    :param nome_arquivo: Nome do arquivo Excel a ser carregado.
    :return: DataFrame com os dados carregados.
    """
    try:
        # Carregar dados do Excel
        df = pd.read_excel(nome_arquivo, sheet_name="Dados")
        print(f"Relatório carregado: {nome_arquivo}")
        return df
    except FileNotFoundError:
        print("Arquivo Excel não encontrado. Certifique-se de que o arquivo existe.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o arquivo Excel: {e}")
        return pd.DataFrame()
