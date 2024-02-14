from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup

def extract_data_from_table(table_element):
    data = []
    soup = BeautifulSoup(table_element.get_attribute('outerHTML'), 'html.parser')
    table = soup.find('table')
    if table:
        # Extrair cabeçalhos da tabela
        headers = []
        for header in table.select('thead th'):
            headers.append(header.text.strip())
        data.append(headers)

        # Extrair linhas da tabela
        for row in table.select('tbody tr'):
            row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
            data.append(row_data)

    return data


def create_excel_from_data(data, filename):
    # Criar DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Salvar no Excel
    df.to_excel(filename, index=False, sheet_name='Estatísticas TOP5 Ligas')
    print(f"Dados salvos em {filename}")

    # Abrir o arquivo Excel
    wb = Workbook()
    planilha = wb.active
    planilha.title = "Estatísticas TOP5 Ligas"

    # Escrever os cabeçalhos na planilha
    cabecalhos = data[0]
    planilha.append(cabecalhos)

    # Escrever os dados na planilha
    for linha in data[1:]:
        planilha.append(linha)

    # Ajuste automático da largura das colunas
    for col in planilha.columns:
        max_length = 0
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2  # Adding extra width for better readability
        planilha.column_dimensions[col[0].column_letter].width = adjusted_width

    # Salvando o arquivo Excel
    wb.save(filename)

    print("Arquivo Excel criado com sucesso.")


def extrair_dados_tabela():
    print("Abrindo o navegador")
    firefox_options = Options()
    firefox_options.set_headless(True)
    firefox_options.binary = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"  # Adicione o caminho para o executável do Firefox

    driver = webdriver.Firefox(options=firefox_options)

    url = 'https://redscores.com/pt-br/prognosticos/estatisticas-de-futbol/teams'
    driver.get(url)
    print("Navegador aberto")

    # Esperar até que a tabela esteja presente na página
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="league"]//table[@class="table-data__table"]'))
    )

    # Encontrar a tabela dentro da div com a classe "league"
    tabela_xpath = '//div[@class="league"]//table[@class="table-data__table"]'
    tabela_element = driver.find_element(By.XPATH, tabela_xpath)

    # Extrair os dados da tabela
    linhas = tabela_element.find_elements(By.XPATH, './/tbody/tr')

    # Extrair dados da tabela
    data = extract_data_from_table(tabela_element)

    print("Dados extraídos da tabela.")

    driver.quit()

    return data

def criar_excel():
    # Lendo os dados do arquivo TXT
    data = extrair_dados_tabela()

    # Selecionando apenas as colunas desejadas
    colunas_selecionadas = ["Ligas", "Gols", "+0.5", "+1.5", "+2.5", "Chutes", "Escanteios", "Cartões"]
    data_filtered = [row for row in data if row[0] != '' and row[0] != 'Ligas']  # Remove linhas vazias e cabeçalho
    data_selected_columns = [[row[i] for i in range(len(row)) if data[0][i] in colunas_selecionadas] for row in data_filtered]

    # Criando um novo arquivo Excel
    create_excel_from_data(data_selected_columns, 'Excel/estatisticas_Top5Leagues.xlsx')




if __name__ == "__main__":
    criar_excel()
