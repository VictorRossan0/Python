import openpyxl
from urllib.parse import quote
import webbrowser
from time import sleep
import pyautogui
import logging
from datetime import datetime

# Configuração do logger
logging.basicConfig(filename='erros.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

webbrowser.open('https://web.whatsapp.com/')
print("WhatsApp Aberto")
sleep(20)
print("ROBS sendo executado!!!")
try:
    # Obter a data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    print(f"Data atual: {data_atual}")
    # Criar o nome do arquivo com a data atual
    nome_arquivo = f'clientes_{data_atual}.xlsx'
    workbook = openpyxl.load_workbook(nome_arquivo)
    clientes = workbook['Worksheet']
    print("Leitura de arquivo feita com sucesso!!")
    for linha in clientes.iter_rows(min_row=2):
        nome = linha[0].value
        telefone = linha[1].value
        data = linha[2].value
        seu_nome = linha[3].value
        seu_cargo = linha[4].value
        numero_cir = linha[5].value

        if nome and telefone and data and seu_nome and seu_cargo and numero_cir:
            mensagem = (
                f"Bom dia,\n\n"
                f"Meu nome é {seu_nome}, e eu sou responsável pelo agendamento na Embratel. "
                f"Estou entrando em contato para tratar de questões referentes à ativação/alteração do CIR: {numero_cir}, "
                f"mas não consegui falar com você.\n\n"
                f"Enviei um e-mail com mais informações e ficaria grato(a) se você pudesse verificar e me retornar assim que for possível.\n\n"
                f"Para a sua comodidade, segue abaixo algumas opções de resposta rápida:\n\n"
                f"    - Se já respondeu ao e-mail, por favor, digite 1.\n"
                f"    - Se prefere que eu entre em contato novamente por este número, digite 2.\n"
                f"    - Caso queira que eu ligue para outro número, por favor, deixe-o abaixo, incluindo o DDD.\n\n"
                f"Agradeço pela sua atenção e estou à disposição para auxiliar na conclusão deste processo de agendamento.\n\n"
                f"Atenciosamente,\n"
                f"{seu_nome}\n"
                f"{seu_cargo}\n"
                f"Embratel"
            )
            link = f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}"
            webbrowser.open(link)
            sleep(10)
            seta = pyautogui.locateCenterOnScreen('Images/seta_whatsapp.png')
            if seta:
                sleep(10)
                pyautogui.click(seta[0], seta[1])
                print("Mensagem Encaminhada com sucesso!!!")
                sleep(10)
                pyautogui.hotkey('ctrl', 'w')
                print("Contato Finalizado com sucesso!!!")
                sleep(10)
            else:
                logging.error(f'Não foi possível encontrar a seta de enviar para {nome}')
        else:
            logging.error(f'Dados inválidos para {nome}')
except Exception as e:
    logging.error(f'Erro inesperado: {str(e)}')
    
print("Atividade finalizada com sucesso pelo ROBS!!!")
