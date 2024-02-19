from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup

def find_table_by_xpath(driver, xpath):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element(By.XPATH, xpath)
    except TimeoutException:
        print("A tabela não pôde ser encontrada.")
        return None

def save_table_to_file(table, filename):
    if table:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(table.get_attribute('outerHTML'))
            print(f"Tabela salva em {filename}")
    else:
        print("Não foi possível salvar a tabela, pois não foi encontrada.")

def read_table_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        table_html = file.read()
        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')
    return table

def extract_data_from_table(table):
    data = []
    # Extrair cabeçalhos da tabela
    headers = []
    for header in table.select('thead th'):
        if header.text.strip() != 'Regular Season':  # Ignorar o cabeçalho 'Regular Season'
            if header.find('use') is not None:
                # Se a célula contém um ícone SVG, obtemos o ID do ícone do atributo xlink:href
                icon_id = header.find('use')['xlink:href'].split('#')[-1]
                # Convertemos o ID do ícone em texto descritivo para o cabeçalho
                if icon_id == 'yellow-card':
                    headers.append('Cartões')
                elif icon_id == 'corner':
                    headers.append('Escanteios')
            else:
                headers.append(header.text.strip())
    data.append(headers)
    print("Cabeçalhos:", headers)  # Adiciona esta linha para imprimir os cabeçalhos
    
    # Extrair linhas da tabela
    for row in table.select('tbody tr'):
        row_data = []
        for idx, cell in enumerate(row.find_all(['th', 'td'])):
            # Ignorar células que contêm ícones SVG e células correspondentes ao cabeçalho 'Regular Season'
            if cell.find('svg') or headers[idx] == 'Regular Season':
                continue
            row_data.append(cell.text.strip())
        data.append(row_data)
    print("Dados:", data)  # Adiciona esta linha para imprimir os dados
    
    return data

def create_excel_from_data(data, filename):
    # Criar DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Filtrar as colunas desejadas
    colunas_desejadas = ['#','Equipe', 'Cartões', 'Escanteios', '1.5+', '2.5+', 'Med. Gols']
    df_filtrado = df[colunas_desejadas].copy()  # Criando uma cópia
    
    # Salvar no Excel
    df_filtrado.to_excel(filename, index=False, sheet_name='Primeira Liga')
    print(f"Dados salvos em {filename}")


def primeira_liga():
    print("Abrindo o navegador")
    firefox_options = Options()
    firefox_options.headless = True
    firefox_options.binary_location = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"  # Adicione o caminho para o executável do Firefox

    driver = webdriver.Firefox(options=firefox_options)

    url = 'https://redscores.com/pt-br/league/portugal/primeira-liga/462'
    driver.get(url)
    print("Navegador aberto")

    # Ou, alternativamente, você pode usar o XPath simplificado
    tabela_xpath_simplificado = '//*[@id="snippet--standings"]/div[3]/div/table'
    tabela_simplificada = find_table_by_xpath(driver, tabela_xpath_simplificado)

    # Salvar tabelas em arquivos de texto
    save_table_to_file(tabela_simplificada, 'TXT/tabela_primeira_liga.txt')

    # Ler a tabela do arquivo de texto
    table = read_table_from_file('TXT/tabela_primeira_liga.txt')

    # Extrair dados da tabela
    data = extract_data_from_table(table)

    # Criar Excel a partir dos dados extraídos
    create_excel_from_data(data, 'Excel/dados_primeira_liga.xlsx')

    # Quando terminar, não se esqueça de fechar o driver
    driver.quit()
