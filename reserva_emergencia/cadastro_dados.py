import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image

def cadastrar_dados():
    dados = []
    while True:
        print("\nCadastre os dados do ativo/FII:")
        ativo = input("Código do Ativo/FII: ")
        quantidade = int(input("Quantidade de Cotas/Ações: "))
        valor_acao = float(input("Valor da Ação/FII (R$): "))
        valor_dividendo = float(input("Valor do Dividendo (R$): "))
        data_pagamento = input("Data do Pagamento (dd/mm/aaaa): ")
        
        total_recebido = quantidade * valor_dividendo
        
        dados.append({
            "Data do Pagamento": data_pagamento,
            "Ativo/FII": ativo,
            "Quantidade": quantidade,
            "Valor da Ação/FII (R$)": valor_acao,
            "Valor do Dividendo (R$)": valor_dividendo,
            "Total Recebido (R$)": total_recebido
        })
        
        continuar = input("\nDeseja cadastrar outro ativo? (s/n): ").strip().lower()
        if continuar != 's':
            break
    return dados

def salvar_em_excel(dados):
    # Criar DataFrame
    df = pd.DataFrame(dados)

    # Salvar em Excel
    arquivo_excel = "dividendos.xlsx"
    with pd.ExcelWriter(arquivo_excel, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
        workbook = writer.book
        worksheet = writer.sheets["Dados"]

        # Criar gráfico
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df["Ativo/FII"], df["Total Recebido (R$)"], color="skyblue")
        ax.set_title("Dividendos Recebidos por Ativo")
        ax.set_xlabel("Ativo")
        ax.set_ylabel("Total Recebido (R$)")
        plt.tight_layout()

        # Salvar gráfico como imagem
        grafico_imagem = "grafico_dividendos.png"
        plt.savefig(grafico_imagem)
        plt.close()

        # Inserir gráfico no Excel
        img = Image(grafico_imagem)
        worksheet.add_image(img, "H2")
    
    print(f"\nArquivo Excel gerado: {arquivo_excel}")

def main():
    print("Bem-vindo ao Sistema de Cadastro de Dividendos!")
    dados = cadastrar_dados()
    salvar_em_excel(dados)

if __name__ == "__main__":
    main()
