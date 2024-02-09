from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from Models.resolver_captcha import quebrar_captcha
from Models.baixar_imagem import baixar_imagem

def limpar_diretorio(caminho_diretorio):
    for arquivo in os.listdir(caminho_diretorio):
        caminho_arquivo = os.path.join(caminho_diretorio, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao excluir {caminho_arquivo}: {e}")

def limpar_pycache():
    caminho_pycache = '__pycache__'
    limpar_diretorio(caminho_pycache)

def preencher_captcha_e_enviar(login, senha):
    print("Abrindo o navegador")
    driver = webdriver.Edge()

    driver.get('https://secure.embratel.com.br/wfep/NovoLogin.aspx')
    print("Navegador aberto")
    time.sleep(10)

    element_login = driver.find_element(By.ID, 'Login1')
    element_login.send_keys(login)
    
    element_senha = driver.find_element(By.ID, 'txtSenha')
    element_senha.send_keys(senha)

    # Encontrar o elemento da tag img
    elemento_img = driver.find_element(By.XPATH, '//img[contains(@src, "CaptchaImage.aspx")]')

    # Obter o URL da imagem diretamente do Selenium
    url_imagem = elemento_img.get_attribute('src')
    caminho_diretorio_images = 'Images'

    # Baixar e salvar a imagem localmente
    caminho_local_imagem = os.path.join(caminho_diretorio_images, "teste")
    baixar_imagem(url_imagem, caminho_local_imagem)

    # Chamar a função para quebrar o captcha
    texto_captcha = quebrar_captcha()

    # Preencher o campo de captcha
    element_captcha = driver.find_element(By.NAME, 'CaptchaControl1')

    # Encontrar o elemento do botão de login
    element_botao_login = driver.find_element(By.NAME, 'btnLogin')

    # Verificar se o texto_captcha não é None antes de enviar para o campo
    if texto_captcha is not None:
        element_captcha.send_keys(texto_captcha)
        # Clicar no botão de login
        element_botao_login.click()
        time.sleep(10)
        print("Login, senha e captcha enviados com sucesso")
    else:
        print("Aviso: Texto do captcha não foi extraído corretamente.")    # Submete o formulário
        element_botao_login.click()

        print("Login, senha e captcha enviados com sucesso")
        time.sleep(10)

if __name__ == "__main__":
    # Limpar o diretório __pycache__ antes de iniciar
    limpar_pycache()

    # Limpar o diretório Images antes de baixar novas imagens
    caminho_diretorio_images = 'Images'
    limpar_diretorio(caminho_diretorio_images)

    # Substitua 'seu_login' e 'sua_senha' pelos valores reais
    preencher_captcha_e_enviar('t3wlvdt', 'SenhaWF3')
