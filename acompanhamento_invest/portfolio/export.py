# portfolio/export.py
import pandas as pd
import matplotlib.pyplot as plt
import os

def exportar_resultados(resultado_carteira, resultado_acoes, resultado_fiis, result_bdrs):
    # Criar DataFrames para ações e FIIs
    df_acoes = pd.DataFrame(resultado_acoes)
    df_fiis = pd.DataFrame(resultado_fiis)
    df_bdrs = pd.DataFrame(result_bdrs)
    
    meses = list(range(1, 13))
    
    df = pd.DataFrame({
        'Mes': meses,
        'Total': resultado_carteira['total'],
        'Reserva de Emergência': resultado_carteira['emergencia'],
        'Tesouro IPCA': resultado_carteira['tesouro_ipca'],
        'Tesouro Selic': resultado_carteira['tesouro_selic'],
        'Renda Fixa CDB 13%': resultado_carteira['renda_fixa_cdb_13'],
        'Renda Fixa CDB 124% CDI': resultado_carteira['renda_fixa_cdb_124_cdi'],
        'Renda Fixa CDB 140% CDI': resultado_carteira['renda_fixa_cdb_140_cdi'],
        'Ações/FIIs': resultado_carteira['acoes_fiis'],
        'Fundo de Investimento': resultado_carteira['fundo_investimento']
    })
    
    # Arredondar as colunas especificadas para duas casas decimais
    colunas_para_arredondar = [
        'Total', 'Reserva de Emergência', 'Tesouro IPCA', 'Tesouro Selic',
        'Renda Fixa CDB 13%', 'Renda Fixa CDB 124% CDI', 'Renda Fixa CDB 140% CDI',
        'Ações/FIIs', 'Fundo de Investimento'
    ]
    
    df[colunas_para_arredondar] = df[colunas_para_arredondar].round(2)
    
    # Criar diretórios se não existirem
    if not os.path.exists('excel'):
        os.makedirs('excel')
    if not os.path.exists('images'):
        os.makedirs('images')

    # Exportar para um único arquivo Excel com abas diferentes
    with pd.ExcelWriter('excel/resultados_portfolio.xlsx') as writer:
        df.to_excel(writer, sheet_name='Portfolio', index=False)
        df_acoes.to_excel(writer, sheet_name='Melhores Ações', index=False)
        df_fiis.to_excel(writer, sheet_name='Melhores FIIs', index=False)
        df_bdrs.to_excel(writer, sheet_name='Melhores BDRs', index=False)

    # Plotar crescimento total da carteira
    plt.figure(figsize=(10, 6))
    plt.plot(df['Mes'], df['Total'], label='Total')
    plt.xlabel('Meses')
    plt.ylabel('Valor (R$)')
    plt.title('Crescimento Total da Carteira ao Longo de 12 Meses')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/crescimento_total_carteira.png')

    # Plotar crescimento por categoria
    plt.figure(figsize=(10, 6))
    for coluna in df.columns[2:]:
        plt.plot(df['Mes'], df[coluna], label=coluna)
    plt.xlabel('Meses')
    plt.ylabel('Valor (R$)')
    plt.title('Crescimento por Categoria ao Longo de 12 Meses')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/crescimento_por_categoria.png')

    print("Resultados exportados com sucesso!")
