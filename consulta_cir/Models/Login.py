from Models.Window import Window  # Importa a classe Window do módulo Models
from dotenv.main import load_dotenv  # Importa a função load_dotenv do módulo dotenv
from selenium.webdriver.common.keys import Keys  # Importa a classe Keys do módulo selenium.webdriver.common.keys
from selenium.webdriver.common.by import By  # Importa a classe By do módulo selenium.webdriver.common.by
import os  # Importa o módulo os
import time  # Importa o módulo time

class Login:

    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        # Define as variáveis de ambiente necessárias
        self.login_page = os.environ['SGP_LOGIN_PAGE']
        self.username = os.environ['SGP_USERNAME']
        self.password = os.environ['SGP_PASSWORD']
        
        # Abre a janela e redireciona para a página de login
        self.window = Window()
        self.window.redirect(self.login_page)
        self.do()

    def do(self):
        # Obtém os inputs para fazer o login
        input_username = self.window.driver.find_element(By.XPATH, "//input[@data-vv-as='Usuário']")
        input_password = self.window.driver.find_element(By.XPATH, "//input[@data-vv-as='Senha']")

        # Insere o nome de usuário
        input_username.click()
        input_username.clear()
        input_username.send_keys(self.username)
        
        # Insere a senha
        input_password.clear()
        input_password.send_keys(self.password)
        input_password.send_keys(Keys.RETURN)

        time.sleep(5)

    def undo(self):
        # Método não implementado, apenas imprime "fechou"
        print("fechou")

    @staticmethod
    def main():
        """Função principal para execução do login."""
        Login().do()  # Cria uma instância de Login e executa o método do
