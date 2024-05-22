from selenium import webdriver  # Importa a classe webdriver do módulo selenium
from selenium.webdriver.firefox.options import Options  # Importa a classe Options do módulo selenium.webdriver.firefox.options
from selenium.webdriver.common.by import By  # Importa a classe By do módulo selenium.webdriver.common.by
import time  # Importa o módulo time para manipulação de tempo

class Window:
            
    def __init__(self):
        # Configurações do navegador Firefox
        firefox_options = Options()
        firefox_options.add_argument('--log-level=3')  # Define o nível de log como 3 (somente erros)

        # Inicializa o driver do Firefox com as opções configuradas
        # self.driver = webdriver.Firefox(executable_path=r"C:\xampp\htdocs\jarvas_agendamento\Drivers\geckodriver", options=firefox_options)
        self.driver = webdriver.Firefox(options=firefox_options)

    def redirect(self, url):
        # Abre a URL especificada no navegador
        self.driver.get(url)
