import openpyxl
from urllib.parse import quote
import webbrowser
from time import sleep
import pyautogui
from datetime import datetime
from pyautogui import ImageNotFoundException

def salvar_log(arquivo, mensagem):
    # Função para salvar logs com data e hora
    with open(arquivo, 'w') as f:
        f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {mensagem}\n')

# Abrir o WhatsApp Web no navegador
webbrowser.open('https://web.whatsapp.com/')
print("WhatsApp Aberto")
sleep(5)  # Aguardar 5 segundos para o WhatsApp abrir completamente
print("ROBS sendo executado!!!")

contatos_processados = {}  # Dicionário para armazenar os contatos processados
contatos_informacoes = {}  # Dicionário para armazenar as informações dos contatos

try:
    # Obter a data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    print(f"Data atual: {data_atual}")
    # Criar o nome do arquivo com a data atual
    # nome_arquivo = f'C:\\Users\\Hitss\\Downloads\\clientes_{data_atual}.xlsx' # Máquina teste
    nome_arquivo = f'C:\\Users\\z085299\\Downloads\\clientes_{data_atual}.xlsx' # Máquina Server
    workbook = openpyxl.load_workbook(nome_arquivo)
    clientes = workbook['Worksheet']
    print("Leitura de arquivo feita com sucesso!!")
    for linha in clientes.iter_rows(min_row=2):
        # Extrair informações de cada linha do arquivo
        nome = linha[0].value
        telefone = linha[1].value
        data = linha[2].value
        seu_nome = linha[3].value
        seu_cargo = linha[4].value
        designacao = linha[5].value
        terminal = linha[6].value
        
        if nome and telefone and data and seu_nome and seu_cargo and designacao:
            # Verificar se o contato já foi processado
            if (nome, telefone) in contatos_processados:
                contatos_processados[(nome, telefone)].append((designacao, terminal))
            else:
                contatos_processados[(nome, telefone)] = [(designacao, terminal)]
                
            # Verificar se o contato já está nas informações
            if (nome, telefone) not in contatos_informacoes:
                contatos_informacoes[(nome, telefone)] = (seu_nome, seu_cargo)

    # Iterar sobre os contatos processados e enviar as mensagens
    for contato, designacoes in contatos_processados.items():
        nome, telefone = contato
        seu_nome, seu_cargo = contatos_informacoes[contato]
        
        if datetime.now().hour >= 18:
            print("Horário limite atingido. Encerrando o envio de mensagens.")
            break
        
        mensagem = (
            f"*Olá, eu sou o {seu_nome}*\n\n"
            f"Faço parte da equipe de agendamento da Claro. Nos próximos dias, um dos nossos analistas entrará em contato por e-mail ou telefone para agendar:\n\n"
        )
        
        for designacao, terminal in designacoes:
            if terminal == 0:
                mensagem += f"Ativação/Alteração da designação {designacao}\n\n"
            else:
                mensagem += f"Ativação/Alteração do terminal {terminal}\n\n"
        
        mensagem += (
            f"Digite abaixo qual a forma mais conveniente para entrarmos em contato?\n\n"
            f"° Email\n"
            f"° Telefone\n"
            f"° Whatsapp\n\n"
            f"Se você já recebeu essa mensagem, por favor, desconsidere.\n\n"
            f"Atenciosamente,\n"
            f"{seu_nome}\n"
            f"{seu_cargo}\n"
            f"Embratel"
        )

        # Montar o link com a mensagem para enviar pelo WhatsApp Web
        link = f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}"
        webbrowser.open(link)  # Abrir o link no navegador
        sleep(8)  # Aguardar 8 segundos para abrir o WhatsApp e enviar a mensagem
        try:
            # Localizar a seta de enviar no WhatsApp Web
            # seta = pyautogui.locateCenterOnScreen('Images/seta_whatsapp_maquina_local_teste.png') # Máquina teste
            seta = pyautogui.locateCenterOnScreen('Images/seta_whatsapp_business.png') # Máquina Server
            if seta:
                sleep(10)  # Aguardar 10 segundos para encaminhar a mensagem
                pyautogui.click(seta[0], seta[1])  # Clicar na seta de enviar
                print("Mensagem Encaminhada com sucesso!!!")
                salvar_log('Logs/info.log', f'Mensagem encaminhada com sucesso para {nome} - {telefone}')
                sleep(10)  # Aguardar 10 segundos para fechar a conversa
                pyautogui.hotkey('ctrl', 'w')  # Fechar a conversa no WhatsApp Web
                print("Contato Finalizado com sucesso!!!")
                sleep(10)  # Tempo entre as mensagens
            else:
                sleep(5)  # Aguardar 5 segundos para encaminhar a mensagem
                pyautogui.hotkey('ctrl', 'w')  # Fechar a conversa no WhatsApp Web
                salvar_log('Logs/error.log', f'Nao foi possível encontrar o {nome} - {telefone}')
                # Verificar se o texto de "url_invalido.png" está presente na tela
                if pyautogui.locateOnScreen('Images/url_invalido.png'):
                    print("O número de telefone compartilhado por url é inválido.")
                else:
                    print("Não foi possível encontrar a seta de enviar. Verifique se a imagem 'seta_whatsapp_business.png' está presente e visível.")
        except ImageNotFoundException:
            sleep(5)  # Aguardar 5 segundos para fechar a mensagem
            pyautogui.hotkey('ctrl', 'w')  # Fechar a conversa no WhatsApp Web
            salvar_log('Logs/error.log', f'Não foi possível encontrar a seta de enviar para {nome} - {telefone}')

    # Enviar mensagem para contato fixo
    contato_fixo = "19981706093"  # Nome do contato fixo
    mensagem_fixa = "Atividade finalizada com sucesso pelo ROBS!!!"

    # Montar o link com a mensagem fixa para enviar pelo WhatsApp Web
    link_fixo = f"https://web.whatsapp.com/send?phone={quote(contato_fixo)}&text={quote(mensagem_fixa)}"
    webbrowser.open(link_fixo)  # Abrir o link no navegador
    sleep(8)  # Aguardar 8 segundos para abrir o WhatsApp e enviar a mensagem
    try:
        # Localizar a seta de enviar no WhatsApp Web
        seta_fixa = pyautogui.locateCenterOnScreen('Images/seta_whatsapp_business.png') # Máquina Server
        # seta_fixa = pyautogui.locateCenterOnScreen('Images/seta_whatsapp_maquina_local_teste.png') # Máquina teste
        
        if seta_fixa:
            sleep(10)  # Aguardar 10 segundos para encaminhar a mensagem
            pyautogui.click(seta_fixa[0], seta_fixa[1])  # Clicar na seta de enviar
            print("Mensagem Fixa Encaminhada com sucesso!!!")
            salvar_log('Logs/info.log', f'Mensagem fixa encaminhada com sucesso para {contato_fixo}')
            sleep(10)  # Aguardar 10 segundos para fechar a conversa
            pyautogui.hotkey('ctrl', 'w')  # Fechar a conversa no WhatsApp Web
            print("Contato Fixo Finalizado com sucesso!!!")
        else:
            sleep(5)  # Aguardar 5 segundos para encaminhar a mensagem
            pyautogui.hotkey('ctrl', 'w')  # Fechar a conversa no WhatsApp Web
            salvar_log('Logs/error.log', f'Nao foi possível encontrar o {contato_fixo}')
            print("Não foi possível encontrar a seta de enviar. Verifique se a imagem 'seta_whatsapp_business.png' está presente e visível.")
    except ImageNotFoundException:
        sleep(5)  # Aguardar 5 segundos para fechar a mensagem
        pyautogui.hotkey('ctrl', 'w')  # Fechar a conversa no WhatsApp Web
        salvar_log('Logs/error.log', f'Não foi possível encontrar a seta de enviar para {contato_fixo}')

except Exception as e:
    salvar_log('Logs/error.log', f'Erro inesperado: {str(e)}')
    raise e

pyautogui.hotkey('ctrl', 'w')  # Fechar todas as conversas no WhatsApp Web
print("Atividade finalizada com sucesso pelo ROBS!!!")
