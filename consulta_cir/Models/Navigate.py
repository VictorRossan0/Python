import time
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Models.Db import Db
from Models.Functions.move_click import move_click
from Models.Functions.inserir_dados_cir import inserir_dados_cir

class Navigate:
    def __init__(self, window, lista):
        """
        Classe para navegar e interagir com elementos em uma página da web.

        Parameters:
        - window: Uma instância da janela do navegador.
        - lista: Uma lista de itens a serem processados.

        """
        self.driver = window.driver
        db_instance = Db()
        lista_de_cirs = db_instance.get_filtered_cirs()
        
        # XPATH para os elementos
        XPATH_BOTOES = {
            "MENU_SGP": '//*[@id="dashboard-header"]/div[1]/a[1]/i',
            "ACESSAR_PESQUISA": '/html/body/div[1]/div[2]/main/div/div/nav/div[1]/div/div[1]/div/div[2]/div/div/div[4]/div/div/a',
            "BUSCAR": '//div[label[text()="Buscar..."]]/input',
            "CÓDIGO_CIR": '//div[label[text()="Código Cir"]]/input',
            "TAREFA": '//*[@id="input-105"]'
        }
        
        # Realiza os cliques para acessar a lista desejada
        move_click(self.driver, XPATH_BOTOES["MENU_SGP"], "Menu SGP")
        move_click(self.driver, XPATH_BOTOES["ACESSAR_PESQUISA"], "Acessando Pesquisa")
        
        # Realiza cliques para listar todos os itens
        for _ in range(1):  # Realiza o mesmo clique uma vez
            if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body"))):
                move_click(self.driver, XPATH_BOTOES["TAREFA"], "Tarefa")
                time.sleep(2)
                pyautogui.moveTo(1197, 381, duration=0.5)
                for _ in range(34):
                    pyautogui.scroll(-1000)
                
                element = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="v-list-item__title" and text()="PA0201 - Agendar Atividade (6.6)"]'))
                )

                # element = WebDriverWait(self.driver, 20).until(
                #     EC.element_to_be_clickable((By.XPATH, '//*[@id="list-item-161-145"]/div[2]'))
                # )

                element.click()
                time.sleep(2)
                print("Pendencia 6.6 encontrado na tela, prosseguindo com o processo")
                move_click(self.driver, XPATH_BOTOES["CÓDIGO_CIR"], "Código CIR")
                time.sleep(2)
                inserir_dados_cir(self.driver, lista_de_cirs)
            time.sleep(3)

    def __del__(self):
        print("DESTRUINDO CLASSE")
