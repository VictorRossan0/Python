import pyautogui
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Models.Db import Db
from datetime import datetime
from Models.Functions.ficha_tecnica import ficha_tecnica

def inserir_dados_cir(driver, dados_cir_list):
    """
    Função para inserir dados CIR em um campo de pesquisa e realizar ações com base nos resultados.

    Parameters:
    - driver: Uma instância do driver do Selenium para interagir com o navegador.
    - dados_cir_list (list): Uma lista de strings contendo os dados CIR a serem inseridos.

    """
    
    print("Inserindo CIR para consulta")
    xpath_pesquisa = '/html/body/div[1]/div[1]/main/div/div/div[2]/div/div/div/div[1]/button/span'

    for dado in dados_cir_list:
        encontrado = False
        while not encontrado:
            pyautogui.click(315, 419)  # Click outside the field to remove any focus
            time.sleep(1)
            pyautogui.doubleClick(315, 419)  # Select all text (may need to adjust coordinates)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')  # Shortcut to select all text
            time.sleep(1)
            pyautogui.press('delete')  # Delete the selected text
            time.sleep(1)
            pyautogui.typewrite(dado)  # Type the new data
            time.sleep(1)
            pyautogui.press('enter')  # Press Enter to confirm insertion
            time.sleep(1)

            try:
                posicao_cir_out = pyautogui.locateOnScreen('Images/cir_out.png', confidence=0.9)
            except pyautogui.ImageNotFoundException:
                posicao_cir_out = None

            if posicao_cir_out:
                print("Nenhum resultado foi encontrado para sua pesquisa!")
                db_instance = Db()
                db_instance.update("consulta_cir", "updated_at", datetime.now(), f"cir = '{dado}'")
                db_instance.update("consulta_cir", "obs", "Nenhum resultado foi encontrado para sua pesquisa!", f"cir = '{dado}'")
                
                WebDriverWait(driver, 30).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'mdn-Spinner')))  # Wait until the spinner disappears
                elemento_pesquisa = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_pesquisa)))
                elemento_pesquisa.click()
                break  # Exit the loop for the next data
            else:
                print("Clicar na Ficha Técnica")
                posicao_ficha_tecnica = pyautogui.locateOnScreen('Images/ficha_tecnica.png', confidence=0.9)
                if posicao_ficha_tecnica:
                    WebDriverWait(driver, 30).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'mdn-Spinner')))  # Wait until the spinner disappears
                    x, y, width, height = posicao_ficha_tecnica
                    center_x = x + (width / 2)
                    center_y = y + (height / 2)
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.click()
                    print("Ficha Técnica aberta")
                    print(f"CIR: {dado}")
                    time.sleep(2)  # Wait for 2 seconds after clicking the Ficha Técnica
                    encontrado = True  # Set to True to exit the loop
                time.sleep(2)

            if not encontrado:  # If not found, move to the next data
                continue
            
            # Call the method 'ficha_tecnica' with 'dado' as an argument
            ficha_tecnica(dado)

            print("Clicar na Exibir Pesquisa")
            elemento_pesquisa = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_pesquisa)))
            elemento_pesquisa.click()
            time.sleep(2)