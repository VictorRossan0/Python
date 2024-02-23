from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import subprocess
import pyautogui
import logging

logging.basicConfig(filename='whatsapp_automacao.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_chrome():
    chrome_process = "chrome.exe"
    chrome_open = chrome_process.encode() in subprocess.check_output('tasklist')

    if not chrome_open:
        logging.error("O Google Chrome não está aberto.")
        return False
    else:
        logging.info("Google Chrome encontrado.")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        return True

def send_whatsapp_message(numero_cliente, mensagem):
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)

    try:
        element = driver.find_element_by_css_selector('div[contenteditable="true"]')
        element.send_keys(numero_cliente + Keys.ENTER + mensagem)
        time.sleep(5)
        logging.info("Mensagem enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {str(e)}")
    finally:
        driver.quit()

def main():
    if not check_chrome():
        logging.error("Certifique-se de que o Google Chrome está instalado e aberto.")
        return

    numero_cliente = input("Por favor, insira o número do cliente: ")
    numero_cliente = re.sub(r'^\+?(\d{2})', r'https://wa.me/55\1', numero_cliente)

    confirmacao = input(f"Confirme o número {numero_cliente} (Ok/Cancelar): ")

    if confirmacao.lower() == 'ok':
        mensagem = input("Digite a mensagem que deseja enviar: ")
        send_whatsapp_message(numero_cliente, mensagem)

if __name__ == "__main__":
    main()