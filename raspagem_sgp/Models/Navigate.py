from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time

class Navigate:
    
    def __init__(self, window, lista):

        #PRIMEIRO CLICK (MENU SGP)
        self.primeiro_botao_x = 24
        self.primeiro_botao_y = 99

        #QUINTO CLICK (ABRIR FILTRO)
        self.quinto_botao_x = 1296
        self.quinto_botao_y = 291

        #SEXTO CLICK (LISTAR TODOS)
        self.sexto_botao_x = 1170
        self.sexto_botao_y = 315

        self.do(window, lista)

    def __del__(self):
        print("DESTRUINDO CLASSE")

    def do(self, window, lista):
        #CLICKS NO PRIMEIRO BOTAO DO MENU
        if(int(lista) == int(13)):
            self.move_click(self.primeiro_botao_x, self.primeiro_botao_y, "MENU SGP")
            self.move_click(105, 207, "ABRINDO CATEGORIA")
            self.move_click(154, 297, "ACESSANDO LISTA 13")
        else:
            self.move_click(self.primeiro_botao_x, self.primeiro_botao_y, "MENU SGP")
            self.move_click(105, 207, "ABRINDO CATEGORIA")
            self.move_click(154, 253, "ACESSANDO LISTA 11")
        
        time.sleep(15)
        # FILTROS AVANÇADOS
        # self.move_click(1215, 170, "ABRINDO FILTRO")
        # time.sleep(5)
        # pyautogui.scroll(-1500)
        # pyautogui.scroll(-1500)
        # time.sleep(2)
        # self.move_click(1120, 680, "LIMPANDO")
        # time.sleep(6)
        # self.move_click(1284, 227, "ABRINDO STATUS")
        # time.sleep(5)
        # self.move_click(1100, 230, "NAO INICIADO")
        # time.sleep(1)
        # self.move_click(1100, 276, "EM ANDAMENTO")
        # time.sleep(2)
        # # self.move_click(1150, 640, "DESABILITANDO PROJ MIGRAÇÃO")
        # self.move_click(1028, 695, "FILTRAR")
        # time.sleep(10)
        
        #CLICKS NO SEGUNDO BOTAO DO MENU
        if WebDriverWait(window.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body"))):
            self.move_click(self.quinto_botao_x, self.quinto_botao_y, "LISTAR TODOS - START") 
            pyautogui.moveTo(1310, 400, 0.07, pyautogui.easeInQuad)
            menu = window.driver.find_element(By.XPATH, "//div[contains(@class, 'menuable__content__active')]")
            lis = menu.find_elements(By.XPATH, ".//div[contains(@id, 'list-item')]")
            time.sleep(2)
            r,g,b = pyautogui.pixel(1310, 400)
            if r == 166 and g == 166 and b == 166:
                pyautogui.scroll(-60)
            pyautogui.moveTo(1310, self.sexto_botao_y, 0.07, pyautogui.easeInQuad)
            i = 1
            nova_localizacao = self.sexto_botao_y
            for i in range(i, len(lis)):
                if(i <= 6):
                    nova_localizacao += 40
                    i += 1
            time.sleep(2)
            self.move_click(self.sexto_botao_x, nova_localizacao, "LISTAR TODOS - END")
        time.sleep(10)
        #CLICK LISTAR TODOS #2
        if WebDriverWait(window.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body"))):
            self.move_click(self.quinto_botao_x, self.quinto_botao_y, "LISTAR TODOS - START") 
            pyautogui.moveTo(1310, 400, 0.07, pyautogui.easeInQuad)
            menu = window.driver.find_element(By.XPATH, "//div[contains(@class, 'menuable__content__active')]")
            lis = menu.find_elements(By.XPATH, ".//div[contains(@id, 'list-item')]")
            time.sleep(2)
            r,g,b = pyautogui.pixel(1310, 400)
            if r == 166 and g == 166 and b == 166:
                pyautogui.scroll(-60)
            pyautogui.moveTo(1310, self.sexto_botao_y, 0.07, pyautogui.easeInQuad)
            i = 1
            nova_localizacao = self.sexto_botao_y
            for i in range(i, len(lis)):
                if(i <= 6):
                    nova_localizacao += 40
                    i += 1
            time.sleep(2)
            self.move_click(self.sexto_botao_x, nova_localizacao, "LISTAR TODOS - END")
            time.sleep(20)
            self.move_click(1299, 227, "PAUSE")
        time.sleep(10)
        #FIM DOS CLICKS NAVIGATE

    def move_click(self, x, y, string):
        pyautogui.moveTo(x, y, 0.01, pyautogui.easeInQuad)
        pyautogui.click()
        print(string)
