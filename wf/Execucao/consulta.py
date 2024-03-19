import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from Execucao.login import By

def fazer_consulta(driver):
    # Exemplo de consulta utilizando XPath
    elemento_consulta = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="NavigationMenu"]/ul/li[5]/a'))
    )
    elemento_consulta.click()
    print("Click em 'Consulta'")

    # Aguardar até que o formulário 'Form1' esteja presente na página
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Form1"]'))
    )
    print("Página de consulta carregada com sucesso")

    # Realizar a próxima ação, como clicar na regional
    elemento_regional = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="MainContent_ddlRegional"]'))
    )
    elemento_regional.click()
    print("Click em 'Regional'")
    
    # Esperar até que o elemento select esteja presente e interagível
    elemento_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'MainContent_ddlRegional'))
    )

    # Criar um objeto Select a partir do elemento select
    select_regional = Select(elemento_select)

    # Selecionar a opção desejada por valor (substitua 'valor_da_opcao' pelo valor real)
    select_regional.select_by_value('2')  # Este exemplo seleciona 'RSC'
    print("Selecionando a Regional")
    # Aguardar um tempo para visualização (opcional)
    time.sleep(5)
