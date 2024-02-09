import os
import shutil
import requests
from bs4 import BeautifulSoup

# Exemplo 1: Processamento de arquivos
def processar_arquivos():
    # Obter lista de arquivos em um diretório
    lista_arquivos = os.listdir('diretorio_origem')

    # Copiar arquivos para um diretório de destino
    for arquivo in lista_arquivos:
        caminho_origem = os.path.join('diretorio_origem', arquivo)
        caminho_destino = os.path.join('diretorio_destino', arquivo)
        shutil.copy(caminho_origem, caminho_destino)

# Exemplo 2: Extração de informações da web
def extrair_informacoes_web():
    # Fazer uma requisição HTTP para obter o conteúdo de uma página da web
    response = requests.get('https://www.example.com')

    # Analisar o conteúdo HTML usando BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar elementos específicos na página e extrair informações
    titulo = soup.find('h1').text
    paragrafos = soup.find_all('p')
    for paragrafo in paragrafos:
        print(paragrafo.text)

# Exemplo 3: Automação de tarefas de sistema
def automatizar_tarefas_sistema():
    # Executar um comando no terminal
    os.system('ls -l')

    # Criar um diretório
    os.mkdir('novo_diretorio')

    # Renomear um arquivo
    os.rename('arquivo_antigo.txt', 'arquivo_novo.txt')

    # Excluir um arquivo
    os.remove('arquivo.txt')

# Chamar as funções de automação de tarefas
processar_arquivos()
extrair_informacoes_web()
automatizar_tarefas_sistema()