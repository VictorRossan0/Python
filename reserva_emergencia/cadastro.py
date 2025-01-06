from utils import entrada_float, entrada_data, registrar_log

def cadastrar_dados():
    dados = []
    while True:
        print("\nCadastre os dados do ativo/FII:")
        ativo = input("Código do Ativo/FII: ")
        valor_acao = entrada_float("Valor da Ação/FII (R$): ")
        valor_dividendo = entrada_float("Valor do Dividendo por Cota/Ação (R$): ")
        data_pagamento = entrada_data("Data do Pagamento (dd/mm/aaaa): ")
        valor_investido = entrada_float("Valor já investido neste ativo (R$): ")

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
                "Valor da Ação/FII (R$)": f"R$ {valor_acao:,.2f}",  # Agora formatado como string
                "Valor do Dividendo (R$)": f"R$ {valor_dividendo:,.2f}",  # Formatado como string
                "Valor Total Investido Ação/FII (R$)": f"R$ {valor_total_investido:,.2f}",  # Formatado como string
                "Total Recebido (R$)": f"R$ {total_recebido:,.2f}",  # Formatado como string
                "Valor Já Investido (R$)": f"R$ {valor_investido:,.2f}"  # Formatado como string
            })

        registrar_log(f"Ativo {ativo} cadastrado com sucesso.")
        
        continuar = input("\nDeseja cadastrar outro ativo? (s/n): ").strip().lower()
        if continuar != 's':
            break
    return dados
