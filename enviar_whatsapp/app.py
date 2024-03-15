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
sleep(10)
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
        designacao = linha[5].value
        terminal = linha[6].value
        
        if nome and telefone and data and seu_nome and seu_cargo and designacao:
            if datetime.now().hour >= 18:
                print("Horário limite atingido. Encerrando o envio de mensagens.")
                break
            
            if terminal == 0:
                mensagem = (
                    f"Olá, eu sou o {seu_nome}\n\n"
                    f"Faço parte da equipe de agendamento da Claro. Nos próximos dias, um dos nossos analistas entrará em contato por e-mail ou telefone para agendar Ativação/Alteração da designação {designacao}.\n\n"
                    f"Se você já recebeu essa mensagem, por favor, desconsidere.\n\n"
                    f"Atenciosamente,\n"
                    f"{seu_nome}\n"
                    f"{seu_cargo}\n"
                    f"Embratel"
                )
            else:
                mensagem = (
                    f"Olá, eu sou o {seu_nome}\n\n"
                    f"Faço parte da equipe de agendamento da Claro. Nos próximos dias, um dos nossos analistas entrará em contato por e-mail ou telefone para agendar Ativação/Alteração do terminal {terminal}.\n\n"
                    f"Se você já recebeu essa mensagem, por favor, desconsidere.\n\n"
                    f"Atenciosamente,\n"
                    f"{seu_nome}\n"
                    f"{seu_cargo}\n"
                    f"Embratel"
                )
            link = f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}"
            webbrowser.open(link)
            sleep(20)  # Tempo para abrir o WhatsApp e enviar a mensagem
            seta = pyautogui.locateCenterOnScreen('Images/seta_whatsapp_business.png')
            if seta:
                sleep(20)  # Tempo para encaminhar a mensagem
                pyautogui.click(seta[0], seta[1])
                print("Mensagem Encaminhada com sucesso!!!")
                sleep(20)  # Tempo para fechar a conversa
                pyautogui.hotkey('ctrl', 'w')
                print("Contato Finalizado com sucesso!!!")
                sleep(12)  # Tempo entre as mensagens
            else:
                logging.error(f'Não foi possível encontrar a seta de enviar para {nome}')
        else:
            logging.error(f'Dados inválidos para {nome}')
except Exception as e:
    logging.error(f'Erro inesperado: {str(e)}')
    
print("Atividade finalizada com sucesso pelo ROBS!!!")