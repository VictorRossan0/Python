from datetime import datetime, timedelta

def calcular_rendimento_cdi(valor_inicial, cdi_anual, dias_uteis):
    """
    Calcula o rendimento da caixinha com base no CDI diário.

    :param valor_inicial: Valor inicial na caixinha (float).
    :param cdi_anual: CDI anual em decimal (ex: 0.1215 para 12,15%).
    :param dias_uteis: Número de dias úteis no mês (int).
    :return: Rendimento acumulado no mês (float).
    """
    taxa_diaria = (1 + cdi_anual) ** (1 / 252) - 1
    rendimento_acumulado = 0

    for _ in range(dias_uteis):
        rendimento_diario = valor_inicial * taxa_diaria
        rendimento_acumulado += rendimento_diario
        valor_inicial += rendimento_diario

    return rendimento_acumulado

# Valores fornecidos
valor_quadra = 550.00
valor_avulso = 10.00

# Entrada do usuário para os mensalistas
num_mensalistas = int(input("Digite a quantidade de mensalistas no mês: "))
mensalistas = []
for i in range(num_mensalistas):
    valor_mensalista = float(input(f"Digite o valor pago pelo mensalista {i + 1}: "))
    mensalistas.append(valor_mensalista)

# Entrada do usuário para quantidade de avulsos
num_avulsos = int(input("Digite a quantidade de avulsos no mês: "))

cdi_anual = 0.1215  # CDI anual em decimal
dias_uteis_mes = 21  # Aproximadamente 21 dias úteis em um mês

# Cálculo do valor arrecadado
valor_arrecadado = sum(mensalistas) + (valor_avulso * num_avulsos)

# Cálculo do rendimento da caixinha
rendimento = calcular_rendimento_cdi(valor_arrecadado, cdi_anual, dias_uteis_mes)

# Resultado final
print("--- Resultado ---")
print(f"Valor arrecadado: R$ {valor_arrecadado:.2f}")
print(f"Rendimento da caixinha no mês: R$ {rendimento:.2f}")
print(f"Total disponível (arrecadado + rendimento): R$ {valor_arrecadado + rendimento:.2f}")
print(f"Diferença em relação ao valor da quadra: R$ {valor_arrecadado + rendimento - valor_quadra:.2f}")
