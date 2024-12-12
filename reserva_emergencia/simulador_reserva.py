import matplotlib.pyplot as plt

def calcular_reserva(valor_inicial, aporte_mensal, taxa_anual, meses):
    """
    Calcula a evolução da reserva de emergência com aportes mensais e juros compostos.

    Args:
        valor_inicial (float): Valor inicial da reserva.
        aporte_mensal (float): Valor a ser aportado mensalmente.
        taxa_anual (float): Taxa de juros anual (ex: CDI).
        meses (int): Período em meses.

    Returns:
        list: Saldo acumulado em cada mês.
    """
    taxa_diaria = taxa_anual / 252  # Aproximação da taxa diária
    dias_no_mes = 21  # Considerando 21 dias úteis por mês
    taxa_mensal = (1 + taxa_diaria) ** dias_no_mes - 1  # Taxa mensal aproximada
    saldo = valor_inicial
    saldos = [saldo]

    for mes in range(1, meses + 1):
        saldo = saldo * (1 + taxa_mensal) + aporte_mensal
        saldos.append(saldo)

    return saldos

def plotar_grafico(saldos, meses):
    """
    Plota a evolução da reserva de emergência ao longo do tempo.

    Args:
        saldos (list): Lista de saldos acumulados.
        meses (int): Período em meses.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(saldos)), saldos, marker='o', linestyle='-', color='b', label='Saldo Acumulado')
    plt.title('Evolução da Reserva de Emergência (100% CDI)')
    plt.xlabel('Meses')
    plt.ylabel('Saldo Acumulado (R$)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Parâmetros de entrada
valor_inicial = float(input("Digite o valor inicial da reserva (R$): "))
aporte_mensal = float(input("Digite o valor do aporte mensal (R$): "))
taxa_anual = 0.1084  # CDI anual de 10,84%
meses = int(input("Digite o período em meses: "))

# Cálculo e exibição
saldos = calcular_reserva(valor_inicial, aporte_mensal, taxa_anual, meses)
plotar_grafico(saldos, meses)

print(f"Saldo final após {meses} meses: R${saldos[-1]:,.2f}")
