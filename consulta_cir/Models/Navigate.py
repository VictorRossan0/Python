from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pytesseract
import cv2
import pyautogui
import time

class Navigate:
    def __init__(self, window, lista):
        self.driver = window.driver
        lista_de_cirs = ['1317696/A', '2352769/A', '2352765/A']
        
        # XPATH para os elementos
        XPATH_BOTOES = {
            "MENU_SGP": '//*[@id="dashboard-header"]/div[1]/a[1]/i',
            "ABRIR_CATEGORIA_1": '//*[@id="app"]/div[2]/main/div/div/nav/div[1]/div/div[1]/div/div[1]',
            "ABRIR_CATEGORIA_2": '//*[@id="app"]/div[2]/main/div/div/nav/div[1]/div/div[2]/div/div[1]',
            "ACESSAR_PESQUISA": '/html/body/div[1]/div[2]/main/div/div/nav/div[1]/div/div[1]/div/div[2]/div/div/div[4]/div/div/a',
            "ACESSAR_LISTA_13": '//*[@id="app"]/div[2]/main/div/div/nav/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div/a',
            "ACESSAR_LISTA_11": '//*[@id="app"]/div[2]/main/div/div/nav/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div/div/a',
            "QTD REGISTROS": '//*[@id="app"]/div/main/div/div/div[2]/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]',
            "QTD REGISTROS 2": '/html/body/div[1]/div/main/div/div/div[2]/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/div[1]',
            "LISTAR_TODOS_START": '/html/body/div[1]/div[2]/div/div[6]/div',
            "LISTAR_TODOS_END": '/html/body/div[1]/div[2]/div/div[9]/div/div',
            "PAUSE": '//*[@id="app"]/div/main/div/div/div[2]/div/div/div/div[2]/div/div/div/button[2]/span',
            "FILTRO_AVANCADO": '//*[@id="app"]/div[1]/main/div/div/div[2]/div/div/div/div[1]/div[2]/button/span',
            "FILTRAR": '//*[@id="app"]/div[1]/main/div/div/div[2]/div/div/div/aside/div[1]/div/div[2]/div/div[2]/div/div[18]/button[1]',
            "BUSCAR": '//div[label[text()="Buscar..."]]/input',
            "CÓDIGO_CIR": '//div[label[text()="Código Cir"]]/input',
            "TAREFA": '//*[@id="input-101"]'
        }
        
        # XPath genérico para encontrar o elemento com base no texto
        xpath_listar_todos = "//div[contains(text(), 'Listar todos')]"

        # Realiza os cliques para acessar a lista desejada
        self.move_click(XPATH_BOTOES["MENU_SGP"], "Menu SGP")
        self.move_click(XPATH_BOTOES["ABRIR_CATEGORIA_1"], "Abrindo Categoria")
        self.move_click(XPATH_BOTOES["ACESSAR_PESQUISA"],"Acessando Pesquisa")
        
        # Realiza cliques para listar todos os itens
        for _ in range(1):  # Realiza o mesmo clique uma vez
            if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body"))):
                self.move_click(XPATH_BOTOES["TAREFA"], "Tarefa")
                time.sleep(3)
                pyautogui.moveTo(1700,800, duration=0.5)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.scroll(-700)
                pyautogui.moveTo(1000,800, duration=0.5)
                pyautogui.click()
                time.sleep(3)
                self.move_click(XPATH_BOTOES["CÓDIGO_CIR"], "Código CIR")
                time.sleep(3)
                self.inserir_dados_cir(lista_de_cirs)
            time.sleep(10)

    def __del__(self):
        print("DESTRUINDO CLASSE")

    def move_click(self, xpath, string):
        # Espera até que o elemento esteja clicável
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        # Espera até que o spinner desapareça
        WebDriverWait(self.driver, 20).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, 'mdn-Spinner'))
        )

        # Clica no elemento
        element.click()
        print(string)

    def inserir_dados_cir(self, dados_cir_list):
        print("Inserindo CIR para consulta")
        xpath_pesquisa = '/html/body/div[1]/div[1]/main/div/div/div[2]/div/div/div/div[1]/button/span'

        for dado in dados_cir_list:
            pyautogui.click(739, 648)  # Clica em uma posição fora do campo para remover qualquer foco
            time.sleep(1)
            pyautogui.doubleClick(739, 648)  # Seleciona todo o texto (pode ser necessário ajustar as coordenadas)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            pyautogui.press('delete')  # Apaga o texto selecionado
            time.sleep(1)
            pyautogui.typewrite(dado)  # Insere o novo dado
            time.sleep(1)
            pyautogui.press('enter')  # Pressiona Enter para confirmar a inserção
            time.sleep(1)
            
            print("Clicar na Ficha Técnica")
            pyautogui.click(225, 815)
            print("Ficha Técnica aberta")
            time.sleep(3)
            
            self.ficha_tecnica()
            
            print("Clicar na Exibir Pesquisa")
            elemento_pesquisa = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_pesquisa)))
            elemento_pesquisa.click()
            time.sleep(3)
            
    def ficha_tecnica(self):
        # Mover o scroll até encontrar o texto "Tratativa"
        print("Movendo a página")
        pyautogui.scroll(-700)  # Exemplo de rolar -700 pixels para baixo
        pyautogui.scroll(-700)
        pyautogui.scroll(-700)
        time.sleep(3)
        
        # Clicar no "Aprovisionar Serviço"
        print("Clicando em Aprovisionar Serviço")
        
        # Captura a tela inteira
        screenshot = pyautogui.screenshot()

        # Salva a imagem
        screenshot.save('Images/screenshot.png')
        
        # Passo 1: Ler a primeira imagem
        imagem_1 = cv2.imread("Images/screenshot.png")

        # Passo 2: Extrair texto da primeira imagem
        texto_1 = pytesseract.image_to_string(imagem_1, lang="por")

        # Procura pelo texto "Aprovisionar Serviço" na tela capturada
        if "Aprovisionar Serviço" in texto_1:
            # Localiza o centro do botão na tela
            posicao_botao = pyautogui.locateCenterOnScreen('Images/aprovisionar_servico.png')
            if posicao_botao:
                x, y = posicao_botao
                pyautogui.click(x, y)
            else:
                print("Botão 'Aprovisionar Serviço' não encontrado na tela")
        else:
            print("Texto 'Aprovisionar Serviço' não encontrado na tela")

        time.sleep(3)
        pyautogui.scroll(-100)
        pyautogui.scroll(-100)
        pyautogui.scroll(-100)
        screenshot2 = pyautogui.screenshot()
        screenshot2.save('Images/screenshot2.png')
        time.sleep(3)
        
        # Extrair informações dos campos específicos
        print("Clicando em Atividade Remota")
        # Passo 1: Ler a segunda imagem
        imagem_2 = cv2.imread("Images/screenshot2.png")

        # Passo 2: Extrair texto da segunda imagem
        texto_2 = pytesseract.image_to_string(imagem_2, lang="por")

        # Procura pelo texto "Atividade Remota" na tela capturada
        if "Atividade Remota" in texto_2:
            # Localiza o centro do botão na tela
            posicao_botao = pyautogui.locateCenterOnScreen('Images/atividade_remota.png', confidence=0.9)
            print(posicao_botao)
            if posicao_botao:
                x, y = posicao_botao
                pyautogui.moveTo(x, y)
                pyautogui.move(300, 0)
                pyautogui.doubleClick()
            else:
                print("Botão 'Atividade Remota' não encontrado na tela")
        else:
            print("Texto 'Atividade Remota' não encontrado na tela")
        time.sleep(3)
        
        print("Clicando em Agendamento PCL")
        # agendamento_pcl_x = 1457  # Coordenada x do campo "Agendamento PCL"
        # agendamento_pcl_y = 703  # Coordenada y do campo "Agendamento PCL"
        # pyautogui.doubleClick(agendamento_pcl_x, agendamento_pcl_y)
        # Procura pelo texto "Atividade Remota" na tela capturada
        if "Agendamento PCL" in texto_2:
            # Localiza o centro do botão na tela
            posicao_botao = pyautogui.locateCenterOnScreen('Images/pcl.png', confidence=0.9)
            print(posicao_botao)
            if posicao_botao:
                x, y = posicao_botao
                pyautogui.moveTo(x, y)
                pyautogui.move(300, 0)
                pyautogui.doubleClick()
            else:
                print("Botão 'Agendamento PCL' não encontrado na tela")
        else:
            print("Texto 'Agendamento PCL' não encontrado na tela")
        time.sleep(3)
        
        print("Movendo a página Novamente")
        pyautogui.scroll(700)  # Exemplo de rolar 700 pixels para cima
        pyautogui.scroll(700)
        pyautogui.scroll(700)
        pyautogui.scroll(700)
        time.sleep(3)
        
        print("Clicando em Check Agen")
        check_agen_x = 624  # Coordenada x do campo "Check Agen"
        check_agen_y = 270  # Coordenada y do campo "Check Agen"
        pyautogui.click(check_agen_x, check_agen_y)
        time.sleep(3)
        
        print("Clicando em Opções")
        opcoes_x = 251  # Coordenada x do campo "Opções"
        opcoes_y = 584  # Coordenada y do campo "Opções"
        pyautogui.click(opcoes_x, opcoes_y)
        time.sleep(3)
        
        print("Clicando em Extração de dados WF")
        wf_x = 452  # Coordenada x do campo "Extração de dados WF"
        wf_y = 605  # Coordenada y do campo "Extração de dados WF"
        pyautogui.click(wf_x, wf_y)
        time.sleep(3)
        
        print("Clicando em Cadastro OS")
        os_x = 532  # Coordenada x do campo "Cadastro OS"
        os_y = 525  # Coordenada y do campo "Cadastro OS"
        pyautogui.click(os_x, os_y)
        time.sleep(3)
        
        print("Carimbo Completo")
        pyautogui.scroll(-250)
        time.sleep(3)
        
        print("Clicando em SOLID") #Dentro de Carimbo ou Dentro da div onde consta Definir Solução de Acesso/SOL-ID CLA ou Preparar Ativação/Informação Adicional para Agendamento
        solid_x = 237  # Coordenada x do campo "SOLID"
        solid_y = 357  # Coordenada y do campo "SOLID"
        pyautogui.doubleClick(solid_x, solid_y)
        time.sleep(3)
        
        print("Clicando em Order Entry(OE)") #Dentro de Carimbo ou Dentro da div onde consta Adoção/Número da OE
        oe_x = 305  # Coordenada x do campo "Order Entry(OE)"
        oe_y = 446  # Coordenada y do campo "Order Entry(OE)"
        pyautogui.doubleClick(oe_x, oe_y)
        time.sleep(3)
        
        print("Clicando em OTS Serviço") #Dentro de Carimbo ou Dentro da div onde consta Adoção/Número OTS Ponta A(Ponta B)
        ots_x = 258  # Coordenada x do campo "OTS Serviço"
        ots_y = 489  # Coordenada y do campo "OTS Serviço"
        pyautogui.doubleClick(ots_x, ots_y)
        time.sleep(3)
        
        print("Clicando em Serviço") #Dentro de Carimbo ou Dentro da div onde consta Serviço/Modalidade
        servico_x = 419  # Coordenada x do campo "Serviço"
        servico_y = 570  # Coordenada y do campo "Serviço"
        pyautogui.doubleClick(servico_x, servico_y)
        time.sleep(3)
        
        print("Clicando em Atividade") #Dentro de Carimbo ou Dentro da div onde consta Adoção/Histórico/Ação Contratual
        atividade_x = 226  # Coordenada x do campo "Atividade"
        atividade_y = 613  # Coordenada y do campo "Atividade"
        pyautogui.doubleClick(atividade_x, atividade_y)
        time.sleep(3)
        
        print("Clicando em Velocidade") #Dentro de Carimbo ou Dentro da div onde consta Informações Circuito/Velocidade ou Adoção/Histórico/Velocidade
        velocidade_x = 260  # Coordenada x do campo "Velocidade"
        velocidade_y = 696  # Coordenada y do campo "Velocidade"
        pyautogui.doubleClick(velocidade_x, velocidade_y)
        time.sleep(3)
        
        # Pressiona Ctrl + W para fechar a aba atual
        print("Fechar aba atual")
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(3)