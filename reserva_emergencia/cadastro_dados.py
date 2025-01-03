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
        valor_acao = float(input("Valor da Ação/FII (R$): "))
        valor_dividendo = float(input("Valor do Dividendo por Cota/Ação (R$): "))
        data_pagamento = input("Data do Pagamento (dd/mm/aaaa): ")
        valor_investido = float(input("Valor já investido neste ativo (R$): "))  # Novo campo
        
        # Quantidades padrão
        quantidades = [1, 10, 100, 1000, 10000]

        # Calcular dividendos e valor investido para cada quantidade
        for qtd in quantidades:
            total_recebido = qtd * valor_dividendo
            valor_total_investido = qtd * valor_acao
            dados.append({
                "Data do Pagamento": data_pagamento,
                "Ativo/FII": ativo,
                "Quantidade": qtd,
                "Valor da Ação/FII (R$)": f"R$ {valor_acao:,.2f}",
                "Valor do Dividendo (R$)": f"R$ {valor_dividendo:,.2f}",
                "Valor Total Investido Ação/FII (R$)": f"R$ {valor_total_investido:,.2f}",
                "Total Recebido (R$)": f"R$ {total_recebido:,.2f}",
                "Valor Já Investido (R$)": f"R$ {valor_investido:,.2f}"  # Novo campo
            })
        
        continuar = input("\nDeseja cadastrar outro ativo? (s/n): ").strip().lower()
        if continuar != 's':
            break
    return dados

def calcular_quantidade_por_investimento(dados):
    print("\n### CALCULAR QUANTIDADE NECESSÁRIA ###")
    valor_desejado = float(input("Informe o valor que deseja investir (R$): "))
    
    for ativo in set([d["Ativo/FII"] for d in dados]):
        preco_acao = float(dados[0]["Valor da Ação/FII (R$)"].replace("R$ ", "").replace(",", ""))
        valor_ja_investido = float(dados[0]["Valor Já Investido (R$)"].replace("R$ ", "").replace(",", ""))
        restante_investir = max(0, valor_desejado - valor_ja_investido)  # Considera o que já foi investido
        quantidade = restante_investir // preco_acao
        print(f"Para investir R$ {valor_desejado:,.2f} em {ativo}, você precisará de {int(quantidade)} cotas adicionais.")

def calcular_diversificacao_por_investimento(dados):
    print("\n### CALCULAR DIVERSIFICAÇÃO DO INVESTIMENTO ###")
    valor_total = float(input("Informe o valor total que deseja investir (R$): "))
    num_ativos = int(input("Informe o número de ativos para diversificar: "))
    
    ativos = list(set([d["Ativo/FII"] for d in dados]))
    if num_ativos > len(ativos):
        print("Número de ativos informado é maior que o número de ativos cadastrados.")
        return
    
    valor_por_ativo = valor_total / num_ativos
    for ativo in ativos[:num_ativos]:
        preco_acao = float(dados[0]["Valor da Ação/FII (R$)"].replace("R$ ", "").replace(",", ""))
        valor_ja_investido = float(dados[0]["Valor Já Investido (R$)"].replace("R$ ", "").replace(",", ""))
        restante_investir = max(0, valor_por_ativo - valor_ja_investido)  # Considera o que já foi investido
        quantidade = restante_investir // preco_acao
        print(f"Para investir aproximadamente R$ {valor_por_ativo:,.2f} em {ativo}, você precisará de {int(quantidade)} cotas adicionais.")

def salvar_em_excel(dados):
    # Criar DataFrame
    df = pd.DataFrame(dados)

    # Salvar em Excel
    arquivo_excel = "dividendos_atualizado.xlsx"
    with pd.ExcelWriter(arquivo_excel, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
        worksheet = writer.sheets["Dados"]

        # Criar gráfico
        fig, ax = plt.subplots(figsize=(8, 5))
        ativos = df["Ativo/FII"].unique()
        for ativo in ativos:
            subset = df[df["Ativo/FII"] == ativo]
            ax.plot(
                subset["Quantidade"],
                subset["Total Recebido (R$)"].str.replace("R$ ", "").str.replace(",", "").astype(float),
                marker='o',
                label=ativo
            )

        ax.set_title("Dividendos Recebidos por Quantidade")
        ax.set_xlabel("Quantidade de Cotas/Ações")
        ax.set_ylabel("Total Recebido (R$)")
        ax.legend()
        plt.grid(True)
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
    calcular_quantidade_por_investimento(dados)
    calcular_diversificacao_por_investimento(dados)
    salvar_em_excel(dados)

if __name__ == "__main__":
    main()
