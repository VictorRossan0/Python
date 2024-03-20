import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from Execucao.login import By

def fazer_consulta(driver):
    def espera_gif_carregamento():
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loaderBackGround2"]'))
        )
        print("Gif de carregamento concluído")

    def espera_elemento_selecionavel(xpath):
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return elemento

    print("Iniciando consulta")

    elemento_consulta = espera_elemento_selecionavel('//*[@id="NavigationMenu"]/ul/li[5]/a')
    elemento_consulta.click()
    print("Click em 'Consulta'")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Form1"]'))
    )
    print("Página de consulta carregada com sucesso")

    elemento_regional = espera_elemento_selecionavel('//*[@id="MainContent_ddlRegional"]')
    elemento_regional.click()
    print("Click em 'Regional'")

    espera_gif_carregamento()

    select_regional = Select(elemento_regional)
    select_regional.select_by_value('2')  # Este exemplo seleciona 'RSC'
    print("Selecionando a Regional")

    espera_gif_carregamento()

    elemento_pesquisar = espera_elemento_selecionavel('//*[@id="MainContent_ddlCampoPesquisa_0"]')
    elemento_pesquisar.click()
    print("Click em 'Pesquisar Por'")

    select_pesquisar = Select(elemento_pesquisar)
    select_pesquisar.select_by_value('576_String_Cod. CIR 1')  # Este exemplo seleciona 'RSC'
    print("Selecionando a Cod. CIR 1")

    espera_gif_carregamento()

    elemento_input = espera_elemento_selecionavel('//*[@id="MainContent_txtValor_0"]')
    elemento_input.click()
    print("Click em 'Input'")
    # Enviar informações para o campo de entrada
    elemento_input.send_keys("123456")
    
    time.sleep(30)  # Espera 30 segundos para a próxima ação

    print("Consulta concluída")