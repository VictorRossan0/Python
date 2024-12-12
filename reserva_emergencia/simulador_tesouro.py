import matplotlib.pyplot as plt

def calcular_tesouro_direto(valor_inicial, aporte_mensal, taxa_anual, meses, tipo, inflacao_anual=0):
    """
    Calcula a evolução do investimento no Tesouro Direto (Selic, Prefixado, IPCA+, IPCA+ com Juros, Renda+ ou Educa+).

    Args:
        valor_inicial (float): Valor inicial do investimento.
        aporte_mensal (float): Valor a ser aportado mensalmente.
        taxa_anual (float): Taxa de rendimento anual fixa ou adicional.
        meses (int): Período em meses.
        tipo (str): Tipo do título ('selic', 'prefixado', 'ipca', 'ipca_juros', 'renda+', 'educa+').
        inflacao_anual (float): Taxa de inflação anual (aplicável para IPCA+ e títulos relacionados).

    Returns:
        list: Saldo acumulado em cada mês.
    """
    if tipo.lower() == "selic":
        taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1  # Pós-fixado (base na Selic)
    elif tipo.lower() == "prefixado":
        taxa_mensal = taxa_anual / 12  # Prefixado
    elif tipo.lower() in ["ipca", "ipca_juros", "educa+"]:
        taxa_mensal = ((1 + inflacao_anual) * (1 + taxa_anual)) ** (1 / 12) - 1  # IPCA+ ou IPCA+ com Juros ou EDUCA+
    elif tipo.lower() == "renda+":
        taxa_mensal = ((1 + inflacao_anual) * (1 + taxa_anual)) ** (1 / 12) - 1  # Renda+ também é IPCA+
    else:
        raise ValueError("Tipo inválido. Use 'selic', 'prefixado', 'ipca', 'ipca_juros', 'renda+' ou 'educa+'.")

    saldo = valor_inicial
    saldos = [saldo]

    for mes in range(1, meses + 1):
        saldo = saldo * (1 + taxa_mensal) + aporte_mensal
        saldos.append(saldo)

    return saldos

def plotar_grafico(saldos, meses, tipo):
    """
    Plota a evolução do investimento no Tesouro Direto.

    Args:
        saldos (list): Lista de saldos acumulados.
        meses (int): Período em meses.
        tipo (str): Tipo do título ('selic', 'prefixado', 'ipca', 'ipca_juros', 'renda+', 'educa+').
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(saldos)), saldos, marker='o', linestyle='-', label=f'Saldo Acumulado ({tipo.capitalize()})')
    plt.title(f'Evolução do Investimento no Tesouro Direto ({tipo.capitalize()})')
    plt.xlabel('Meses')
    plt.ylabel('Saldo Acumulado (R$)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Parâmetros de entrada
valor_inicial = float(input("Digite o valor inicial do investimento (R$): "))
aporte_mensal = float(input("Digite o valor do aporte mensal (R$): "))
taxa_anual = float(input("Digite a taxa anual (exemplo: 0.1225 para 12,25%): "))
meses = int(input("Digite o período em meses: "))
tipo = input("Digite o tipo de título ('selic', 'prefixado', 'ipca', 'ipca_juros', 'renda+', 'educa+'): ")

# Apenas para títulos atrelados à inflação
inflacao_anual = 0
if tipo.lower() in ["ipca", "ipca_juros", "renda+", "educa+"]:
    inflacao_anual = float(input("Digite a taxa de inflação anual estimada (exemplo: 0.04 para 4%): "))

# Cálculo e exibição
saldos = calcular_tesouro_direto(valor_inicial, aporte_mensal, taxa_anual, meses, tipo, inflacao_anual)
plotar_grafico(saldos, meses, tipo)

print(f"Saldo final após {meses} meses: R${saldos[-1]:,.2f}")
