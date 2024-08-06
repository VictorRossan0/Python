import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Configurar Pandas para lidar com comportamento futuro
pd.set_option('future.no_silent_downcasting', True)

def exportar_resultados(resultado_carteira, resultado_acoes, resultado_fiis, result_bdrs):
    # Criar DataFrames para ações, FIIs e BDRs
    df_acoes = pd.DataFrame(resultado_acoes)
    df_fiis = pd.DataFrame(resultado_fiis)
    df_bdrs = pd.DataFrame(result_bdrs)
    
    # Função para limpar e converter colunas de porcentagens e números
    def limpar_e_converter_colunas(df):
        # Substituir valores vazios por NaN
        df.replace('', np.nan, inplace=True)
        
        # Função para converter colunas específicas
        def converter_coluna(coluna):
            if df[coluna].dtype == object:  # Verifica se a coluna é de string
                df[coluna] = df[coluna].astype(str)  # Garante que a coluna é do tipo string
                df[coluna] = df[coluna].str.replace('%', '').str.replace(',', '.')
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce')  # Converte para float e usa 'coerce' para erros
            return df
        
        # Converter as colunas de interesse
        df = converter_coluna('Dividend Yield')
        df = converter_coluna('P/L')
        df = converter_coluna('P/VP')
        df = converter_coluna('Variação(12M)')
        
        # Substituir NaN por 0, se necessário
        df.fillna(0, inplace=True)
        
        return df
    
    # Aplicar a limpeza e conversão em cada DataFrame
    df_acoes = limpar_e_converter_colunas(df_acoes)
    df_fiis = limpar_e_converter_colunas(df_fiis)
    df_bdrs = limpar_e_converter_colunas(df_bdrs)
    
    # Função para filtrar e ordenar os DataFrames
    def filtrar_e_ordenar(df, tipo_ativo):
        df_filtrado = df[df['Variação(12M)'] > 0]  # Filtra variação positiva
        if tipo_ativo == 'acoes':
            df_ordenado = df_filtrado.sort_values(by=['Dividend Yield', 'P/L', 'P/VP'], ascending=[False, True, True])
        elif tipo_ativo == 'fiis':
            df_ordenado = df_filtrado.sort_values(by=['Dividend Yield', 'P/VP'], ascending=[False, True])
        elif tipo_ativo == 'bdrs':
            df_ordenado = df_filtrado.sort_values(by=['Dividend Yield', 'P/L', 'P/VP'], ascending=[False, True, True])
        return df_ordenado
    
    df_acoes = filtrar_e_ordenar(df_acoes, 'acoes')
    df_fiis = filtrar_e_ordenar(df_fiis, 'fiis')
    df_bdrs = filtrar_e_ordenar(df_bdrs, 'bdrs')

    # Criar DataFrame da carteira
    meses = list(range(1, 13))
    
    df_carteira = pd.DataFrame({
        'Mes': meses,
        'Total': resultado_carteira['total'],
        'Reserva de Emergência': resultado_carteira['emergencia'],
        'Tesouro Direto': resultado_carteira['tesouro_direto'],
        'Renda Fixa': resultado_carteira['renda_fixa'],
        'Bolsa de Valores': resultado_carteira['bolsa_valores'],
        'Fundo de Investimento': resultado_carteira['fundo_investimento']
    })

    # Arredondar as colunas especificadas para duas casas decimais
    colunas_para_arredondar = [
        'Total', 'Reserva de Emergência', 'Tesouro Direto', 'Renda Fixa', 'Bolsa de Valores', 'Fundo de Investimento'
    ]
    
    df_carteira[colunas_para_arredondar] = df_carteira[colunas_para_arredondar].round(2)
    
    # Criar diretórios se não existirem
    if not os.path.exists('excel'):
        os.makedirs('excel')
    if not os.path.exists('images'):
        os.makedirs('images')

    # Exportar para um único arquivo Excel com abas diferentes
    with pd.ExcelWriter('excel/resultados_portfolio.xlsx') as writer:
        df_carteira.to_excel(writer, sheet_name='Portfolio', index=False)
        df_acoes.to_excel(writer, sheet_name='Melhores Ações', index=False)
        df_fiis.to_excel(writer, sheet_name='Melhores FIIs', index=False)
        df_bdrs.to_excel(writer, sheet_name='Melhores BDRs', index=False)
    
    print("Resultados exportados para Excel com sucesso!")
    
    # Função para plotar gráficos dos melhores ativos
    def plotar_grafico(df, tipo_ativo):
        plt.figure(figsize=(10, 6))
        for coluna in ['Dividend Yield', 'P/L', 'P/VP']:
            if coluna in df.columns:
                plt.plot(df['Ativo'], df[coluna], marker='o', label=coluna)
        plt.xlabel('Ativos')
        plt.ylabel('Indicadores')
        plt.title(f'Indicadores dos Melhores {tipo_ativo.capitalize()}')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'images/melhores_{tipo_ativo}.png')
        plt.close()
        print(f"Gráfico de Melhores {tipo_ativo.capitalize()} exportado com sucesso!")
    
    # Gerar gráficos para ações, FIIs e BDRs
    plotar_grafico(df_acoes, 'acoes')
    plotar_grafico(df_fiis, 'fiis')
    plotar_grafico(df_bdrs, 'bdrs')

    # Plotar crescimento total da carteira
    plt.figure(figsize=(10, 6))
    plt.plot(df_carteira['Mes'], df_carteira['Total'], label='Total')
    plt.xlabel('Meses')
    plt.ylabel('Valor (R$)')
    plt.title('Crescimento Total da Carteira ao Longo de 12 Meses')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/crescimento_total_carteira.png')
    print("Crescimento Total da Carteira ao Longo de 12 Meses feito")
    
    # Plotar crescimento por categoria
    plt.figure(figsize=(10, 6))
    for coluna in df_carteira.columns[2:]:
        plt.plot(df_carteira['Mes'], df_carteira[coluna], label=coluna)
    plt.xlabel('Meses')
    plt.ylabel('Valor (R$)')
    plt.title('Crescimento por Categoria ao Longo de 12 Meses')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/crescimento_por_categoria.png')
    print("Crescimento por Categoria ao Longo de 12 Meses feito")
    
    print("Todos os gráficos foram exportados com sucesso!")