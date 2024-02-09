from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import paramiko

# Automação de tarefas na web usando Selenium
def automacao_web():
    # Inicializar o driver do Selenium (nesse exemplo, usando o Chrome)
    driver = webdriver.Chrome()

    # Abrir uma página da web
    driver.get('https://www.example.com')

    # Interagir com elementos na página
    input_element = driver.find_element_by_name('q')
    input_element.send_keys('Exemplo de pesquisa')
    input_element.send_keys(Keys.ENTER)

    # Fechar o navegador
    driver.quit()

# Automação de tarefas em servidores remotos usando Paramiko
def automacao_servidor():
    # Estabelecer conexão SSH com o servidor remoto
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('endereco_servidor', username='usuario', password='senha')

    # Executar comandos no servidor remoto
    stdin, stdout, stderr = client.exec_command('ls -l')
    print(stdout.read().decode())

    # Encerrar a conexão SSH
    client.close()

# Chamar as funções de automação de tarefas
automacao_web()
automacao_servidor()