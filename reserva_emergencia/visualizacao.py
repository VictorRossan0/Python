import os
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image

def gerar_graficos(df: pd.DataFrame):
    """
    Gera gráficos de dividendos recebidos por quantidade de cotas/ações.
    Salva os gráficos como imagens em um diretório específico.
    """
    ativos = df["Ativo/FII"].unique()
    diretorio_graficos = "graficos"

    # Criar diretório para os gráficos, se não existir
    os.makedirs(diretorio_graficos, exist_ok=True)

    for ativo in ativos:
        subset = df[df["Ativo/FII"] == ativo]

        # Verificar se há dados suficientes para gerar o gráfico
        if subset.empty:
            print(f"Nenhum dado encontrado para o ativo {ativo}. Ignorando gráfico.")
            continue

        # Gráfico de Dividendos Recebidos
        plt.figure(figsize=(8, 5))
        plt.plot(
            subset["Quantidade"],
            subset["Total Recebido (R$)"].str.replace("R$ ", "").str.replace(",", "").astype(float),
            marker="o",
            label=f"Dividendos de {ativo}"
        )
        plt.title(f"Dividendos Recebidos - {ativo}")
        plt.xlabel("Quantidade de Cotas/Ações")
        plt.ylabel("Total Recebido (R$)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Salvar gráfico
        imagem_nome = os.path.join(diretorio_graficos, f"grafico_dividendos_{ativo}.png")
        plt.savefig(imagem_nome)
        plt.close()
        print(f"Gráfico salvo: {imagem_nome}")


def adicionar_graficos_excel(worksheet, df: pd.DataFrame):
    """
    Adiciona gráficos gerados ao arquivo Excel.
    """
    ativos = df["Ativo/FII"].unique()
    diretorio_graficos = "graficos"
    linha = 2

    for ativo in ativos:
        imagem_nome = os.path.join(diretorio_graficos, f"grafico_dividendos_{ativo}.png")
        
        # Verificar se a imagem existe antes de tentar adicioná-la
        if not os.path.exists(imagem_nome):
            print(f"Imagem não encontrada: {imagem_nome}")
            continue

        img = Image(imagem_nome)
        posicao = f"H{linha}"
        worksheet.add_image(img, posicao)
        linha += 20  # Ajusta a posição para não sobrepor gráficos

