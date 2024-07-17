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
    tesouro_ipca = [valor_inicial * 0.2]  # Inicialmente 20% do valor inicial
    tesouro_selic = [valor_inicial * 0.2]  # Inicialmente 20% do valor inicial
    renda_fixa_cdb_13 = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial
    renda_fixa_cdb_124_cdi = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial
    renda_fixa_cdb_140_cdi = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial
    acoes_fiis = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial
    fundo_investimento = [valor_inicial * 0.1]  # Inicialmente 10% do valor inicial

    taxa_cdi = 0.11679 / 12
    taxa_ipca = 0.0021
    taxa_selic = 0.0083
    taxa_renda_fixa_13 = 0.13 / 12
    taxa_renda_fixa_124_cdi = (1.24 * 0.11679) / 12
    taxa_renda_fixa_140_cdi = (1.40 * 0.11679) / 12
    taxa_fundo_investimento = 0.1374 / 12

    for mes in range(1, meses):
        emergencia.append(emergencia[-1] * (1 + taxa_cdi) + deposito_mensal * 0.2)
        tesouro_ipca.append(tesouro_ipca[-1] * (1 + taxa_ipca) + deposito_mensal * 0.2)
        tesouro_selic.append(tesouro_selic[-1] * (1 + taxa_selic) + deposito_mensal * 0.2)
        renda_fixa_cdb_13.append(renda_fixa_cdb_13[-1] * (1 + taxa_renda_fixa_13) + deposito_mensal * 0.1)
        renda_fixa_cdb_124_cdi.append(renda_fixa_cdb_124_cdi[-1] * (1 + taxa_renda_fixa_124_cdi) + deposito_mensal * 0.1)
        renda_fixa_cdb_140_cdi.append(renda_fixa_cdb_140_cdi[-1] * (1 + taxa_renda_fixa_140_cdi) + deposito_mensal * 0.1)
        acoes_fiis.append(acoes_fiis[-1] * (1 + taxas_crescimento_anuais['acoes_fiis'] / 12) + deposito_mensal * 0.1)
        fundo_investimento.append(fundo_investimento[-1] * (1 + taxa_fundo_investimento) + deposito_mensal * 0.1)

        total_mes = (
            emergencia[-1] + tesouro_ipca[-1] + tesouro_selic[-1] + renda_fixa_cdb_13[-1] +
            renda_fixa_cdb_124_cdi[-1] + renda_fixa_cdb_140_cdi[-1] +
            acoes_fiis[-1] + fundo_investimento[-1]
        )
        total.append(total_mes)

    return {
        'total': total,
        'emergencia': emergencia,
        'tesouro_ipca': tesouro_ipca,
        'tesouro_selic': tesouro_selic,
        'renda_fixa_cdb_13': renda_fixa_cdb_13,
        'renda_fixa_cdb_124_cdi': renda_fixa_cdb_124_cdi,
        'renda_fixa_cdb_140_cdi': renda_fixa_cdb_140_cdi,
        'acoes_fiis': acoes_fiis,
        'fundo_investimento': fundo_investimento
    }
