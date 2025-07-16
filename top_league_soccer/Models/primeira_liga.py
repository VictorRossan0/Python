from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup
import os
import logging

logging.basicConfig(level=logging.INFO)

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def find_table_by_xpath(driver, xpath):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element(By.XPATH, xpath)
    except TimeoutException:
        logging.error("A tabela não pôde ser encontrada.")
        return None

def save_table_to_file(table, filename):
    if table:
        ensure_dir_exists(os.path.dirname(filename))
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(table.get_attribute('outerHTML'))
            logging.info(f"Tabela salva em {filename}")
    else:
        logging.error("Não foi possível salvar a tabela, pois não foi encontrada.")

def read_table_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            table_html = file.read()
            soup = BeautifulSoup(table_html, 'html.parser')
            table = soup.find('table')
        return table
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {filename}: {e}")
        return None

def extract_data_from_table(table):
    if table is None:
        logging.error("Tabela não encontrada para extração de dados.")
        return []
    data = []
    headers = []
    for header in table.select('thead th'):
        if header.text.strip() != 'Regular Season':
            if header.find('use') is not None:
                icon_id = header.find('use')['xlink:href'].split('#')[-1]
                if icon_id == 'yellow-card':
                    headers.append('Cartões')
                elif icon_id == 'corner':
                    headers.append('Escanteios')
            else:
                headers.append(header.text.strip())
    data.append(headers)
    logging.info(f"Cabeçalhos: {headers}")

    for row in table.select('tbody tr'):
        row_data = []
        for idx, cell in enumerate(row.find_all(['th', 'td'])):
            if cell.find('svg') or (idx < len(headers) and headers[idx] == 'Regular Season'):
                continue
            row_data.append(cell.text.strip())
        data.append(row_data)
    logging.info(f"Dados extraídos: {data[:2]} ...")
    return data

def create_excel_from_data(data, filename):
    if not data or not data[0]:
        logging.error("Dados insuficientes para criar o Excel.")
        return
    try:
        df = pd.DataFrame(data[1:], columns=data[0])
        colunas_desejadas = ['#','Equipe', 'Cartões', 'Escanteios', '1.5+', '2.5+', 'Med. Gols']
        df_filtrado = df[colunas_desejadas].copy()
        ensure_dir_exists(os.path.dirname(filename))
        df_filtrado.to_excel(filename, index=False, sheet_name='Primeira Liga')
        logging.info(f"Dados salvos em {filename}")
    except Exception as e:
        logging.error(f"Erro ao criar o Excel: {e}")

def primeira_liga():
    logging.info("Abrindo o navegador")
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    
    try:
        url = 'https://redscores.com/pt-br/league/portugal/primeira-liga/462'
        driver.get(url)
        logging.info("Navegador aberto")

        tabela_xpath_simplificado = '//*[@id="snippet--standings"]/div[3]/div/table'
        tabela_simplificada = find_table_by_xpath(driver, tabela_xpath_simplificado)

        save_table_to_file(tabela_simplificada, 'TXT/tabela_primeira_liga.txt')
        table = read_table_from_file('TXT/tabela_primeira_liga.txt')
        data = extract_data_from_table(table)
        create_excel_from_data(data, 'Excel/dados_primeira_liga.xlsx')

    except Exception as e:
        logging.error(f"Erro ao processar Primeira Liga: {e}")
    finally:
        if driver:
            driver.quit()
