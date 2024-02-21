import openpyxl
from urllib.parse import quote
import webbrowser
from time import sleep
import pyautogui
import logging

# Configuração do logger
logging.basicConfig(filename='erros.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

webbrowser.open('https://web.whatsapp.com/')
sleep(30)

try:
    workbook = openpyxl.load_workbook('Enviar.xlsx')
    clientes = workbook['Planilha1']

    for linha in clientes.iter_rows(min_row=2):
        nome = linha[0].value
        telefone = linha[1].value
        data = linha[2].value

        if nome and telefone and data:
            mensagem = f'Olá {nome}, neste dia {data.strftime("%d/%m/%Y")} estará sendo enviado um teste em Python'
            link = f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}"
            webbrowser.open(link)
            sleep(10)
            seta = pyautogui.locateCenterOnScreen('Images/seta_whatsapp.png')
            if seta:
                sleep(10)
                pyautogui.click(seta[0], seta[1])
                sleep(10)
                pyautogui.hotkey('ctrl', 'w')
                sleep(10)
            else:
                logging.error(f'Não foi possível encontrar a seta de enviar para {nome}')
        else:
            logging.error(f'Dados inválidos para {nome}')
except Exception as e:
    logging.error(f'Erro inesperado: {str(e)}')
