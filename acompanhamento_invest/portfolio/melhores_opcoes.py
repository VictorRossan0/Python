import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def encontrar_melhores_opcoes_web_scraping(tipo_ativo, tickers):
    base_url = f"https://investidor10.com.br/{tipo_ativo}/"
    dados = {
        'Ativo': [],
        'Preço': [],
        'Dividend Yield': [],
        'P/L': [],
        'P/VP': [],
        'Crescimento Histórico (%)': []
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for ticker in tickers:
        url = base_url + ticker + "/"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            try:
                nome_ativo = soup.find('div', class_='name-ticker').find('h1').text.strip()
                dados['Ativo'].append(nome_ativo)
                
                preco_ativo = soup.find('div', class_='_card cotacao').find('span', class_='value').text.strip()
                dados['Preço'].append(preco_ativo)
                
                if tipo_ativo == 'acoes':
                    dividend_yield = soup.find('div', class_='_card dy').find('div', class_='_card-body').find('span').text.strip()
                    pl_ratio = soup.find('div', class_='_card pl').find('div', class_='_card-body').find('span').text.strip()
                    pv_ratio = soup.find('div', class_='_card vp').find('div', class_='_card-body').find('span').text.strip()
                    crescimento = soup.find('div', class_='_card val').find('div', class_='_card-body').find('span').text.strip()
                elif tipo_ativo == 'fiis':
                    dy_card = soup.find('div', class_='_card dy')
                    if dy_card:
                        dividend_yield = dy_card.find('div', class_='_card-body').find('span').text.strip()
                    
                    second_dy_card = soup.find_all('div', class_='_card dy')[1]
                    if second_dy_card:
                        crescimento = second_dy_card.find('div', class_='_card-body').find('span').text.strip()
                    else:
                        crescimento = ''
                    
                    pl_ratio = ''
                    pv_ratio = soup.find('div', class_='_card vp').find('div', class_='_card-body').find('span').text.strip()
                elif tipo_ativo == 'bdrs':
                    dividend_yield = soup.find('div', class_='_card dy').find('div', class_='_card-body').find('span').text.strip()
                    pl_ratio = soup.find('div', class_='_card val').find('div', class_='_card-body').find('span').text.strip()
                    pv_ratio = soup.find('div', class_='_card vp').find('div', class_='_card-body').find('span').text.strip()
                    crescimento = soup.find('div', class_='_card pl').find('div', class_='_card-body').find('span').text.strip()
                
                dados['Dividend Yield'].append(dividend_yield)
                dados['P/L'].append(pl_ratio)
                dados['P/VP'].append(pv_ratio)
                dados['Crescimento Histórico (%)'].append(crescimento)
                
            except Exception as e:
                print(f"Erro ao extrair dados de {ticker}: {str(e)}")
        
        else:
            print(f"Erro ao acessar a página {url}: {response.status_code}")
        
        time.sleep(1)
    
    df = pd.DataFrame(dados)
    df = df.sort_values(by='Dividend Yield', ascending=False).head(5)
    
    return df

tickers_acoes = ['petr4', 'vale3', 'bbas3', 'cpfe3', 'cple6', 'itsa4', 'itub4', 'jall3', 'kepl3', 'tgma3', 'ugpa3', 'vivt3', 'alup11']
tickers_fiis = ['knip11', 'hglg11', 'xplg11', 'cpts11', 'kncr11', 'knsc11', 'knri11', 'rbrr11', 'xpml11', 'irdm11', 'btlg11', 'visc11']
tickers_bdrs = ['aapl34', 'amzo34', 'gogl34', 'msft34', 'nflx34', 'coca34', 'inbr32', 'nvdc34', 'tsla34', 'meli34', 'jpmc34', 'ibmb34']
