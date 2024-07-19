# portfolio/portfolio.py
import json

def carregar_configuracoes():
    with open('config.json', 'r') as f:
        configuracoes = json.load(f)
    return configuracoes

def calcular_crescimento_carteira(valor_inicial, deposito_mensal, taxas_crescimento_anuais):
    meses = 12
    total = [valor_inicial]
    emergencia = [valor_inicial * 0.2]  # Inicialmente 20% do valor inicial
    tesouro_direto = [valor_inicial * 0.2]  # Inicialmente 20% do valor inicial
    renda_fixa = [valor_inicial * 0.2]  # Inicialmente 20% do valor inicial
    bolsa_valores = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial
    fundo_investimento = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial

    taxa_cdi = 0.11679 / 12
    taxa_ipca = 0.0021
    taxa_selic = 0.0083
    taxa_fundo_investimento = 0.1374 / 12

    for mes in range(1, meses):
        emergencia.append(emergencia[-1] * (1 + taxa_cdi) + deposito_mensal * 0.2)
        tesouro_direto.append(tesouro_direto[-1] * (1 + taxa_ipca) + deposito_mensal * 0.2)
        renda_fixa.append(renda_fixa[-1] * (1 + taxa_selic) + deposito_mensal * 0.2)
        bolsa_valores.append(bolsa_valores[-1] * (1 + taxas_crescimento_anuais['bolsa_valores'] / 12) + deposito_mensal * 0.1)
        fundo_investimento.append(fundo_investimento[-1] * (1 + taxa_fundo_investimento) + deposito_mensal * 0.1)

        total_mes = (
            emergencia[-1] + tesouro_direto[-1] + renda_fixa[-1] + bolsa_valores[-1] + fundo_investimento[-1]
        )
        total.append(total_mes)

    return {
        'total': total,
        'emergencia': emergencia,
        'tesouro_direto': tesouro_direto,
        'renda_fixa': renda_fixa,
        'bolsa_valores': bolsa_valores,
        'fundo_investimento': fundo_investimento
    }
