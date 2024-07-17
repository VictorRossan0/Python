# main.py

from portfolio.portfolio import calcular_crescimento_carteira, carregar_configuracoes
from portfolio.export import exportar_resultados
from portfolio.historico import registrar_movimentacao
from portfolio.melhores_opcoes import tickers_acoes, tickers_fiis, tickers_bdrs, encontrar_melhores_opcoes_web_scraping

def main():
    configuracoes = carregar_configuracoes()
    resultado_carteira = calcular_crescimento_carteira(
        configuracoes['valor_inicial'],
        configuracoes['deposito_mensal'],
        configuracoes['taxas_crescimento_anuais']
    )

    # Registrar movimentações financeiras no histórico
    for mes in range(1, 13):
        registrar_movimentacao('crescimento_total', resultado_carteira['total'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('reserva_emergencia', resultado_carteira['emergencia'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('tesouro_ipca', resultado_carteira['tesouro_ipca'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('tesouro_selic', resultado_carteira['tesouro_selic'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('renda_fixa_cdb_13', resultado_carteira['renda_fixa_cdb_13'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('renda_fixa_cdb_124_cdi', resultado_carteira['renda_fixa_cdb_124_cdi'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('renda_fixa_cdb_140_cdi', resultado_carteira['renda_fixa_cdb_140_cdi'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('acoes_fiis', resultado_carteira['acoes_fiis'][mes - 1], f'{mes}/2024')
        registrar_movimentacao('fundo_investimento', resultado_carteira['fundo_investimento'][mes - 1], f'{mes}/2024')

    # Obter resultados de ações e FIIs usando melhores_opcoes.py
    resultado_acoes = encontrar_melhores_opcoes_web_scraping("acoes", tickers_acoes)
    resultado_fiis = encontrar_melhores_opcoes_web_scraping("fiis", tickers_fiis)
    result_bdrs = encontrar_melhores_opcoes_web_scraping('bdrs', tickers_bdrs)
    
    print("Melhores Ações:")
    print(resultado_acoes)

    print("\nMelhores FIIs:")
    print(resultado_fiis)

    print("\nMelhores BDRs:")
    print(result_bdrs)

    # Exportar todos os resultados
    exportar_resultados(resultado_carteira, resultado_acoes, resultado_fiis, result_bdrs)

if __name__ == '__main__':
    main()
