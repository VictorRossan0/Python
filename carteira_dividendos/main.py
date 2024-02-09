import pandas as pd
import yfinance as yf
from requests.exceptions import HTTPError
import numpy as np

# Função para obter dados da ação
def obter_dados_acao(ticker):
    try:
        acao = yf.Ticker(ticker)
        dados = acao.info
        return dados
    except HTTPError as e:
        print(f"Erro ao obter dados para o ticker {ticker}. Verifique se o ticker é válido ou se há problemas temporários no serviço.")
        return None

# Função para calcular indicadores
def calcular_indicadores(dados):
    if dados is not None:
        try:
            pl_ratio = dados.get('trailingPE')
            ev_ebitda = dados.get('enterpriseToEbitda')
            pv_ratio = dados.get('priceToBook')
            roe = round(dados.get('returnOnEquity', 0) * 100, 2)  # Convertendo ROE para porcentagem com duas casas decimais
            dy = round(dados.get('trailingAnnualDividendYield', 0) * 100, 2)  # Convertendo DY para porcentagem com duas casas decimais
            dlebitda_ratio = dados.get('debtToEbitda')
 
            # Adicionando cálculo DL/EBITDA
            debt = dados.get('totalDebt', 0)
            cash = dados.get('totalCash', 0)
            ebitda = dados.get('ebitda', 0)

            dlebitda_calculado = debt - cash if (debt is not None and cash is not None) else None
            dlebitda_ratio_calculado = dlebitda_calculado / ebitda if (dlebitda_calculado is not None and ebitda is not None and ebitda != 0) else None

            return {
                'P/L': pl_ratio,
                'EV/EBITDA': ev_ebitda,
                'P/VP': pv_ratio,
                'ROE': roe,
                'DY': dy,
                'DL/EBITDA': dlebitda_ratio_calculado
            }
        except KeyError:
            return None
    else:
        return None
# Lista de ações por mês
acoes_por_mes = {

    'Janeiro': ['ALUP3.SA', 'ALUP4.SA', 'CGAS3.SA', 'CGAS5.SA', 'EPAR3.SA', 'EVEN3.SA', 'FRAS3.SA', 'JHSF3.SA', 'MILS3.SA', 'POMO3.SA', 'POMO4.SA', 'RAPT3.SA', 'RAPT4.SA', 'SHUL4.SA', 'SLCE3.SA', 'SUZB3.SA', 'TAEE11.SA', 'TAEE3.SA', 'TAEE4.SA', 'VITT3.SA'],

    'Fevereiro': ['CRIV3.SA', 'CRIV4.SA', 'KLBN3.SA', 'KLBN4.SA', 'ODPV3.SA', 'PETR3.SA', 'PETR4.SA', 'VBBR3.SA', 'WLMM3.SA', 'WLMM4.SA'],
    
    'Março': ['ALLD3.SA', 'BBSE3.SA', 'CSMG3.SA', 'ETER3.SA', 'INTB3.SA', 'JHSF3.SA', 'MTSA3.SA', 'MTSA4.SA', 'PGMN3.SA', 'RAIZ4.SA', 'TUPY3.SA', 'WEGE3.SA'],
    
    'Abril': ['CMIG4.SA', 'ITSA4.SA', 'JHSF3.SA', 'KLBN11.SA', 'MDIA3.SA', 'SHUL4.SA', 'TFCO4.SA', 'TRPL3.SA', 'TRPL4.SA', 'VIVT3.SA'],
    
    'Maio': ['BMOB3.SA', 'CSMG3.SA', 'JHSF3.SA', 'KLBN11.SA', 'LEVE3.SA', 'ODER4.SA', 'PETZ3.SA', 'RADL3.SA', 'TASA4.SA', 'VAMO3.SA'],
    
    'Junho': ['ALLD3.SA', 'CMIG3.SA', 'CMIG4.SA', 'JHSF3.SA', 'MULT3.SA', 'ODER4.SA'],
    
    'Julho': ['CEGR3.SA', 'ITSA4.SA', 'JHSF3.SA', 'KLBN11.SA', 'MULT3.SA', 'ODER4.SA', 'TUPY3.SA', 'XPML11.SA', 'VGIR11.SA', 'KNRI11.SA'],
    
    'Agosto': ['ITSA4.SA', 'JHSF3.SA', 'MULT3.SA', 'ODER4.SA', 'TASA4.SA', 'TAEE11.SA'],
    
    'Setembro': ['CSMG3.SA', 'JHSF3.SA', 'MULT3.SA', 'ODER4.SA'],
    
    'Outubro': ['ITSA4.SA', 'JHSF3.SA', 'KLBN11.SA', 'MULT3.SA'],
    
    'Novembro': ['CMIG4.SA', 'ITSA4.SA', 'JHSF3.SA', 'TAEE11.SA', 'BOXP34.SA'],
    
    'Dezembro': ['CEEB3.SA', 'CEEB5.SA', 'CLSC3.SA', 'CLSC4.SA', 'EGIE3.SA', 'EUCA3.SA', 'EUCA4.SA', 'FRAS3.SA', 'GEPA3.SA', 'GEPA4.SA', 'JHSF3.SA', 'KLBN11.SA', 'MOAR3.SA', 'ODER4.SA', 'TAEE11.SA', 'VITT3.SA'],
}

print("Execução Iniciada")
# Criar um escritor de Excel
with pd.ExcelWriter('carteira_dividendos/indicadores_acoes_mensais.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'nan_inf_to_errors': True}}) as writer:
    workbook = writer.book

    # Criar uma aba para os "Melhores Resultados"
    top5_resultados = pd.DataFrame(columns=['Mês', 'Ticker', 'P/L', 'EV/EBITDA', 'P/VP', 'ROE(%)', 'DY(%)', 'DL/EBITDA'])

    # Iterar sobre os meses
    for mes, acoes in acoes_por_mes.items():
        dados_df = pd.DataFrame(columns=['Empresa', 'Ticker', 'P/L', 'EV/EBITDA', 'P/VP', 'ROE(%)', 'DY(%)', 'DL/EBITDA'])

        # Iterar sobre as ações do mês
        for ticker in acoes:
            dados_acao = obter_dados_acao(ticker)

            if dados_acao is not None:
                indicadores = calcular_indicadores(dados_acao)

                if indicadores is not None:
                    dados_df = dados_df.append({
                        'Empresa': dados_acao.get('longName', ''),
                        'Ticker': ticker,
                        'P/L': indicadores.get('P/L'), 
                        'EV/EBITDA': indicadores.get('EV/EBITDA'), 
                        'P/VP': indicadores.get('P/VP'), 
                        'ROE(%)': indicadores.get('ROE'), 
                        'DY(%)': indicadores.get('DY'), 
                        'DL/EBITDA': indicadores.get('DL/EBITDA')
                    }, ignore_index=True)

        # Substituir '0' por 0
        dados_df.replace('0', 0, inplace=True)

        # Converta as colunas numéricas para tipos numéricos
        colunas_numericas = dados_df.columns[2:]
        dados_df[colunas_numericas] = dados_df[colunas_numericas].apply(pd.to_numeric, errors='coerce')

        # Gravar os dados na aba do mês
        dados_df.to_excel(writer, sheet_name=mes, index=False)

        # Adicionar legenda das cores
        planilha = writer.sheets[mes]
        planilha.write('J1', 'Legenda de Cores', None)
        planilha.write('J2', 'Vermelho: Pior', None)
        planilha.write('J3', 'Amarelo: Mediano', None)
        planilha.write('J4', 'Verde: Melhor', None)

        # Adiciona o formato para cada cor
        formato_vermelho = workbook.add_format({'font_color': '#9C0006'})
        formato_amarelo = workbook.add_format({'font_color': '#9C6500'})
        formato_verde = workbook.add_format({'font_color': '#006100'})

        # Atualizar o DataFrame top5_resultados
        for coluna in dados_df.columns[2:]:
            col_index = dados_df.columns.get_loc(coluna)
            planilha.write(0, col_index, coluna, None)

            # Obtém os valores mínimo e máximo da coluna
            min_valor = dados_df[coluna].min()
            max_valor = dados_df[coluna].max()

            # Itera sobre as linhas da DataFrame e escreve os dados na planilha
            for i, row in dados_df.iterrows():
                valor = row[coluna]

                if isinstance(valor, (int, float)) and not pd.isna(valor):
                    formato_cor = None  # Inicializa o formato como nulo

                    if valor < 0:
                        formato_cor = formato_vermelho  # Números negativos em vermelho
                        print(f"Valor negativo em {mes} para {coluna}: {valor}")
                    elif coluna in ['ROE(%)', 'DY(%)']:
                        if valor == max_valor:
                            formato_cor = formato_verde
                        elif valor == min_valor:
                            formato_cor = formato_vermelho
                        elif min_valor < valor < max_valor:
                            formato_cor = formato_amarelo
                    else:
                        # Atribui a cor apropriada com base nas condições
                        if valor == min_valor:
                            formato_cor = formato_verde  # Melhor
                        elif valor == max_valor:
                            formato_cor = formato_vermelho  # Pior
                        elif min_valor < valor < max_valor:
                            formato_cor = formato_amarelo  # Mediano

                    planilha.write_number(i + 1, col_index, valor, formato_cor)  # Usando write_number para manter o formato numérico
                else:
                    planilha.write(i + 1, col_index, valor)

            coluna_resultados = dados_df[dados_df[coluna] >= 0].sort_values(by=coluna, ascending=coluna not in ['ROE(%)', 'DY(%)'])
            coluna_resultados = coluna_resultados.head(5) if not coluna_resultados.empty else coluna_resultados
            coluna_resultados['Mês'] = mes
            coluna_resultados = coluna_resultados[['Mês', 'Ticker', coluna]]

            if not coluna_resultados.empty:
                top5_resultados = pd.concat([top5_resultados, coluna_resultados])
                print(f"Melhores resultados em {mes} para {coluna}: {coluna_resultados}")

    # Substituir '0' por 0
    top5_resultados.replace('0', 0, inplace=True)

    # Exportar o DataFrame top5_resultados para um arquivo Excel
    top5_resultados.to_excel(writer, sheet_name='Melhores Resultados', index=False)
print("Execução Finalizada")