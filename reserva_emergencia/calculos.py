def calcular_quantidade_por_investimento(dados):
    print("\n### CALCULAR QUANTIDADE NECESSÁRIA ###")
    valor_desejado = float(input("Informe o valor que deseja investir (R$): "))
    
    for ativo in set([d["Ativo/FII"] for d in dados]):
        preco_acao = float(dados[0]["Valor da Ação/FII (R$)"].replace("R$ ", "").replace(",", ""))
        valor_ja_investido = float(dados[0]["Valor Já Investido (R$)"].replace("R$ ", "").replace(",", ""))
        restante_investir = max(0, valor_desejado - valor_ja_investido)
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
        quantidade = valor_por_ativo // preco_acao
        print(f"Para investir aproximadamente R$ {valor_por_ativo:,.2f} em {ativo}, você precisará de {int(quantidade)} cotas.")

def calcular_rentabilidade(dados):
    print("\n### RELATÓRIO DE RENTABILIDADE ###")
    relatorio = []
    ativos = set([d["Ativo/FII"] for d in dados])
    
    for ativo in ativos:
        total_dividendos = sum(float(d["Total Recebido (R$)"].replace("R$ ", "").replace(",", "")) for d in dados if d["Ativo/FII"] == ativo)
        total_investido = sum(float(d["Valor Total Investido Ação/FII (R$)"].replace("R$ ", "").replace(",", "")) for d in dados if d["Ativo/FII"] == ativo)
        rentabilidade = (total_dividendos / total_investido) * 100 if total_investido > 0 else 0
        relatorio.append({"Ativo/FII": ativo, "Rentabilidade (%)": rentabilidade})
        print(f"Ativo: {ativo}, Rentabilidade: {rentabilidade:.2f}%")
    
    return relatorio
