from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from PIL import Image
from io import BytesIO
import os
from datetime import datetime, timedelta

# Função para calcular a data do dia anterior
def obter_data_dia_anterior():
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    return ontem.strftime("%d%m%Y")

# Função para obter a data de modificação de um arquivo
def obter_data_modificacao_arquivo(caminho_arquivo):
    data_modificacao_timestamp = os.path.getmtime(caminho_arquivo)
    data_modificacao = datetime.fromtimestamp(data_modificacao_timestamp)
    return data_modificacao.strftime("%d%m%Y")

# Inicializar o contador
contador = 0

# Carregar o valor do contador a partir de um arquivo
try:
    with open('contador.txt', 'r') as file:
        contador = int(file.read())
except FileNotFoundError:
    pass

# Função para baixar e salvar a imagem localmente
def baixar_imagem(url, caminho_local):
    global contador  # Acessar a variável global
    response = requests.get(url)
    if response.status_code == 200:
        imagem = Image.open(BytesIO(response.content))
        # Adicionar o contador ao nome do arquivo
        caminho_local_com_contador = f"{caminho_local}{contador}.png"
        imagem.save(caminho_local_com_contador)
        print(f"Imagem salva em: {caminho_local_com_contador}")
        # Incrementar o contador para a próxima execução
        contador += 1
        # Salvar o valor atual do contador no arquivo
        with open('contador.txt', 'w') as file:
            file.write(str(contador))
    else:
        print(f"Erro ao baixar a imagem. Status code: {response.status_code}")

# Caminho do diretório de imagens
caminho_diretorio_images = "Images"

# Calcular a data do dia anterior
data_dia_anterior = obter_data_dia_anterior()

# Excluir apenas as imagens do dia anterior
for arquivo in os.listdir(caminho_diretorio_images):
    caminho_arquivo = os.path.join(caminho_diretorio_images, arquivo)
    if os.path.isfile(caminho_arquivo):
        data_modificacao_arquivo = obter_data_modificacao_arquivo(caminho_arquivo)
        if data_modificacao_arquivo == data_dia_anterior:
            os.remove(caminho_arquivo)
            print(f"Imagem do dia anterior removida: {caminho_arquivo}")

# print("Abrindo o navegador")
# driver = webdriver.Edge()

# driver.get('https://secure.embratel.com.br/wfep/NovoLogin.aspx')
# print("Navegador aberto")
# time.sleep(10)

# # Encontrar o elemento da tag img
# elemento_img = driver.find_element(By.XPATH, '//img[contains(@src, "CaptchaImage.aspx")]')

# # Obter o URL da imagem diretamente do Selenium
# url_imagem = elemento_img.get_attribute('src')

# # Baixar e salvar a imagem localmente
# caminho_local_imagem = os.path.join(caminho_diretorio_images, "teste")
# baixar_imagem(url_imagem, caminho_local_imagem)

# # Fechar o navegador
# driver.quit()
