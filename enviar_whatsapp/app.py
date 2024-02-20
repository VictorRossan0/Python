import openpyxl
from urllib.parse import quote
import webbrowser
from time import sleep
import pyautogui

webbrowser.open('https://web.whatsapp.com/')
sleep(30)

workbook = openpyxl.load_workbook('Enviar.xlsx')

clientes = workbook['Planilha1']

for linha in clientes.iter_rows(min_row=2):
    nome = linha[0].value
    telefone = linha[1].value
    data = linha[2].value
    
    try:
        mensagem = f'Olá {nome}, neste dia {data.strftime('%d/%m/%Y')} estará sendo enviado um teste em Python'
        link = f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}"
        webbrowser.open(link)
        sleep(10)
        seta = pyautogui.locateCenterOnScreen('Images/seta_whatsapp.png')
        sleep(10)
        pyautogui.click(seta[0],seta[1])
        sleep(10)
        pyautogui.hotkey('ctrl','w')
        sleep(10)
    except:
        print(f'Não foi possível enviar mensagem para {nome}')
        with open('erros.csv', 'a',newline='',encoding='utf-8') as arquivo:
            arquivo.write(f'{nome},{telefone}')