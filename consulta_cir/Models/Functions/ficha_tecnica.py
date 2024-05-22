import cv2
import pyautogui
import time
import pyperclip
import pytesseract
from Models.Db import Db

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ficha_tecnica(dado):
        """
        Função para realizar a varredura de campos específicos dentro de um determinado CIR.
        
        """
        start_time = time.time()  # Armazena o tempo inicial
        time.sleep(2)

        header = pyautogui.screenshot()
        header.save('Screenshots/header.png')
        img = cv2.imread('Screenshots/header.png')
        text = pytesseract.image_to_string(img, lang="por")
        
        if 'Aviso de multa' in text:
            for posicao in pyautogui.locateAllOnScreen('Images/aviso_multa.png', confidence=0.9):
                x, y, _, _ = posicao
                pyautogui.moveTo(x, y)
                print(posicao)
                pyautogui.move(404,26) # movimentação até a posição do 'x'
                pyautogui.click()
            print("Aviso de multa encontrado e fechado")
        elif 'Solicitação de mobilidade' in text:
            for posicao in pyautogui.locateAllOnScreen('Images/header.png', confidence=0.9):
                x, y, _, _ = posicao
                pyautogui.moveTo(x, y)
                print(posicao)
                pyautogui.move(404,26)
                pyautogui.click()
                print("Solicitação de mobilidade encontrada e fechada")
        else:
            print("Solicitação de mobilidade não encontrada, prosseguindo com o processo") 
            print("Aviso de multa não encontrado, prosseguindo com o processo")       
        
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save('Screenshots/velocidade.png')

        print("Clicando em Velocidade")
        imagem = cv2.imread("Screenshots/velocidade.png")
        texto = pytesseract.image_to_string(imagem, lang="por")
        
        if "Velocidade" in texto:
            posicao_botao = pyautogui.locateCenterOnScreen('Images/velocidade.png', confidence=0.9)
            if posicao_botao:
                x, y = posicao_botao
                
                pyautogui.moveTo(x, y)
                pyautogui.move(300, 0)
                pyautogui.doubleClick()
                pyautogui.sleep(1)
                pyautogui.hotkey('ctrl', 'c')
                valor_velocidade = pyperclip.paste()
                print(f"Velocidade: {valor_velocidade}")
                
                db_instance = Db()
                db_instance.update("consulta_cir", "velocidade", valor_velocidade, f"cir = '{dado}'")
        else:
            print("Texto 'Velocidade' não encontrado na tela")

        print("Clicando em Adoção")
        adocao_encontrado = False
        max_repeticoes_adoc = 10  # Número máximo de repetições
        for i in range(max_repeticoes_adoc):
            time.sleep(2)
            if not adocao_encontrado:
                pyautogui.scroll(-400)
                screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
                screenshot.save(f'Screenshots/adocao{i}.png')
                imagem = cv2.imread(f"Screenshots/adocao{i}.png")
                texto = pytesseract.image_to_string(imagem, lang="por")

                # Verificar se o texto "Adoção" aparece na imagem
                try:
                    posicao_adocao = pyautogui.locateCenterOnScreen('Images/adocao.png', confidence=0.9)
                    if posicao_adocao:
                        print("Adoção encontrado")
                        x, y = posicao_adocao
                        for _ in range(2):
                            pyautogui.click(x, y)
                            time.sleep(1)
                            pyautogui.doubleClick()  # Perform an additional click to ensure the button is clicked
                            time.sleep(1)
                        adocao_encontrado = True
                        pyautogui.scroll(-50)
                    else:
                        print("Adoção não encontrado")
                except pyautogui.ImageNotFoundException as e:
                    print(f"Error: {e}")
                    print("Imagem 'Images/adocao.png' não encontrada na tela.")
            else:
                break
            if adocao_encontrado:
                max_repeticoes_adoc = i + 1  # Ajuste o número máximo de repetições
        time.sleep(2)

        print("Clicando em Order Entry(OE)")
        screenshot5 = pyautogui.screenshot()  # Captura a tela inteira
        screenshot5.save('Screenshots/oe.png')  # Salva a imagem
        imagem5 = cv2.imread("Screenshots/oe.png")
        texto5 = pytesseract.image_to_string(imagem5, lang="por")

        if "Número da OE" in texto5:
            posicao_botao = pyautogui.locateCenterOnScreen('Images/oe.png', confidence=0.9)
            if posicao_botao:
                x, y = posicao_botao
                
                pyautogui.moveTo(x, y)
                pyautogui.move(300, 0)
                pyautogui.doubleClick()
                pyautogui.sleep(1)  # Aguardar um momento para o texto ser selecionado
                pyautogui.hotkey('ctrl', 'c')  # Copiar o texto selecionado para a área de transferência
                valor_oe = pyperclip.paste()  # Obter o texto da área de transferência
                print(f"Order Entry(OE): {valor_oe}")
                
                # Salvar o Order Entry(OE) no banco de dados
                db_instance = Db()
                db_instance.update("consulta_cir", "oe", valor_oe, f"cir = '{dado}'")
            else:
                print("Texto 'Order Entry(OE)' não encontrado na tela")
        time.sleep(2)
        
        print("Clicando em Aprovisionar Serviço")
        aprovisionar_servico_encontrado = False
        max_repeticoes_aprov = 10  # Número máximo de repetições
        for i in range(max_repeticoes_aprov):
            time.sleep(2)
            if not aprovisionar_servico_encontrado:
                pyautogui.scroll(-350)
                screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
                screenshot.save(f'Screenshots/aprovisionar_servico{i}.png')
                imagem6 = cv2.imread(f"Screenshots/aprovisionar_servico{i}.png")
                texto6 = pytesseract.image_to_string(imagem6, lang="por")
                try:
                    posicao_aprov = pyautogui.locateCenterOnScreen('Images/aprovisionar_servico.png', confidence=0.9)
                    if posicao_aprov:
                        print("Aprovisionar Serviço encontrado")
                        x, y = posicao_aprov
                        pyautogui.click(x, y)
                        time.sleep(1)
                        pyautogui.click()  # Perform an additional click to ensure the button is clicked
                        time.sleep(1)
                        pyautogui.click()  # Perform an additional click to ensure the button is clicked
                        time.sleep(1)
                        aprovisionar_servico_encontrado = True
                        pyautogui.scroll(-150)
                except pyautogui.ImageNotFoundException:
                    print("Erro: imagem 'Images/aprovisionar_servico.png' não encontrada na tela.")
            else:
                break
            # Ajustar o número máximo de repetições com base na necessidade
            if aprovisionar_servico_encontrado:
                max_repeticoes_aprov = i + 1  # Ajuste o número máximo de repetições
        time.sleep(2)
        
        print("Clicando em Agendamento PCL")
        agendamento_pcl_encontrado = False
        max_repeticoes_agendamento = 3
        for i in range(max_repeticoes_agendamento):
            pyautogui.scroll(-100)
            screenshot = pyautogui.screenshot()
            screenshot.save(f'Screenshots/pcl{i}.png')
            imagem7 = cv2.imread(f"Screenshots/pcl{i}.png")
            texto7 = pytesseract.image_to_string(imagem7, lang="por")
            
            if "Agendamento PCL" in texto7:
                posicao_botao = pyautogui.locateCenterOnScreen('Images/pcl.png', confidence=0.8)
                if posicao_botao:
                    x, y = posicao_botao
                    pyautogui.moveTo(x, y)
                    pyautogui.move(300, 0)
                    pyautogui.doubleClick()
                    time.sleep(1)  # Aguardar um momento para o texto ser selecionado
                    pyautogui.hotkey('ctrl', 'c')  # Copiar o texto selecionado para a área de transferência
                    valor_pcl = pyperclip.paste()  # Obter o texto da área de transferência
                    print(f"Agendamento PCL: {valor_pcl}")
                    
                    # Salvar o Agendamento PCL no banco de dados
                    db_instance = Db()
                    db_instance.update("consulta_cir", "pcl", valor_pcl, f"cir = '{dado}'")
                    
                    agendamento_pcl_encontrado = True
                    break
                else:
                    print("Botão não encontrado na tela.")
                    # Salvar o Agendamento PCL no banco de dados
                    db_instance = Db()
                    db_instance.update("consulta_cir", "pcl", "Não", f"cir = '{dado}'")
            else:
                print("Texto não encontrado na imagem.")
                # Salvar o Agendamento PCL no banco de dados
                db_instance = Db()
                db_instance.update("consulta_cir", "pcl", "Não", f"cir = '{dado}'")

            if agendamento_pcl_encontrado:
                max_repeticoes_agendamento = i + 1  # Ajustar o número máximo de repetições

        if not agendamento_pcl_encontrado:
            print(f"Limite de repetições ({max_repeticoes_agendamento}) atingido. O Agendamento PCL não foi encontrado.")

        # print("Clicando em Designação MLPPP/MULTIPATH")
        # designacao_encontrada = False
        # max_repeticoes_designacao = 5
        # for i in range(max_repeticoes_designacao):
        #     pyautogui.scroll(-100)
        #     screenshot = pyautogui.screenshot()
        #     screenshot.save(f'Screenshots/desig{i}.png')
        #     imagem = cv2.imread(f"Screenshots/desig{i}.png")
        #     texto = pytesseract.image_to_string(imagem, lang="por")
            
        #     if "Designação MLPPP/MULTIPATH" in texto:
        #         posicao_botao = pyautogui.locateCenterOnScreen('Images/desig.png', confidence=0.9)
        #         if posicao_botao:
        #             x, y = posicao_botao
                
        #             pyautogui.moveTo(x, y)
        #             pyautogui.move(300, 0)
        #             for _ in range(3):
        #                 pyautogui.click()
        #             time.sleep(1)  # Aguardar um momento para o texto ser selecionado
        #             pyautogui.hotkey('ctrl', 'c')  # Copiar o texto selecionado para a área de transferência
        #             valor_designacao = pyperclip.paste()  # Obter o texto da área de transferência
        #             print(f"Designação MLPPP/MULTIPATH: {valor_designacao}")
                    
        #             # Salvar a Designação MLPPP/MULTIPATH no banco de dados
        #             db_instance = Db()
        #             db_instance.update("consulta_cir", "designacao_voz", valor_designacao, f"cir = '{dado}'")
                    
        #             designacao_encontrada = True
        #             break
        #         else:
        #             print("Botão não encontrado na tela.")
        #     else:
        #         print("Texto não encontrado na imagem.")

        #     if designacao_encontrada:
        #         max_repeticoes_designacao = i + 1  # Ajustar o número máximo de repetições

        # if not designacao_encontrada:
        #     print(f"Limite de repetições ({max_repeticoes_designacao}) atingido. A Designação MLPPP/MULTIPATH não foi encontrada.")

        print("Clicando em Definir Solução de Acesso")
        definir_solucao_encontrado = False
        max_repeticoes_definir = 5
        for i in range(max_repeticoes_definir):
            time.sleep(2)
            if not definir_solucao_encontrado:
                pyautogui.scroll(100)
                screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
                screenshot.save(f'Screenshots/definir_solucao{i}.png')
                imagem9 = cv2.imread(f"Screenshots/definir_solucao{i}.png")
                texto9 = pytesseract.image_to_string(imagem9, lang="por")

                try:
                    posicao_def = pyautogui.locateCenterOnScreen('Images/definir_solucao.png', confidence=0.9)
                    if posicao_def:
                        print("Definir Solução encontrado")
                        x, y = posicao_def
                        pyautogui.click(x, y)
                        time.sleep(1)
                        pyautogui.click()  # Perform an additional click to ensure the button is clicked
                        time.sleep(1)
                        pyautogui.click()  # Perform an additional click to ensure the button is clicked
                        time.sleep(1)
                        definir_solucao_encontrado = True
                    else:
                        print("Texto 'Definir Solução de Acesso' não encontrado na tela")
                except pyautogui.ImageNotFoundException:
                    print("Erro: imagem 'Images/definir_solucao.png' não encontrada na tela.")
            else:
                break
            # Ajustar o número máximo de repetições com base na necessidade
            if definir_solucao_encontrado:
                max_repeticoes_definir = i + 1  # Ajuste o número máximo de repetições
        time.sleep(2)
        
        print("Clicando em SOL-ID CLA")
        # Captura a tela e salva como imagem
        screenshot = pyautogui.screenshot()
        screenshot.save('Screenshots/solid.png')

        # Carrega a imagem capturada
        imagem_sol = cv2.imread("Screenshots/solid.png")

        # Usa o Tesseract para reconhecer texto na imagem
        texto_sol = pytesseract.image_to_string(imagem_sol, lang="por")

        # Procura pela palavra "SOL" na tela capturada
        if "SOL" in texto_sol or "SOL-ID CLA" in texto_sol or "SOL-D CLA" in texto_sol:
            
            try:
                # Tenta localizar a imagem 'Images/solid.png' na tela
                posicao_botao = pyautogui.locateCenterOnScreen('Images/solid.png', confidence=0.85)
                
                # Se a posição do botão for encontrada
                if posicao_botao:
                    x, y = posicao_botao
                    
                    pyautogui.moveTo(x, y)
                    pyautogui.move(300, 0)
                    pyautogui.doubleClick()
                    pyautogui.sleep(1) # Aguardar um momento para o texto ser selecionado
                    pyautogui.hotkey('ctrl', 'c') # Copiar o texto selecionado para a área de transferência
                    valor_solid = pyperclip.paste() # Obter o texto da área de transferência
                    print(f"SOL-ID CLA: {valor_solid}")
                    
                    # Salvar o SOL-ID CLA no banco de dados
                    db_instance = Db()
                    db_instance.update("consulta_cir", "solid", valor_solid, f"cir = '{dado}'")
                else:
                    # Se a posição do botão não for encontrada
                    print("Botão 'SOL-ID CLA' não encontrado na tela")
                    # Atualize o banco de dados com "N/A" ou qualquer outra ação necessária
                    db_instance = Db()
                    db_instance.update("consulta_cir", "solid", "N/A", f"cir = '{dado}'")
            except pyautogui.ImageNotFoundException:
                # Se a exceção ImageNotFoundException for levantada (ou seja, a imagem não é encontrada na tela)
                print("Imagem 'Images/solid.png' não encontrada na tela")
                # Atualize o banco de dados com "N/A" ou qualquer outra ação necessária
                db_instance = Db()
                db_instance.update("consulta_cir", "solid", "N/A", f"cir = '{dado}'")
        else:
            print("Texto 'SOL-ID CLA' não encontrado na tela")
            # Atualize o banco de dados com "N/A" ou qualquer outra ação necessária
            db_instance = Db()
            db_instance.update("consulta_cir", "solid", "N/A", f"cir = '{dado}'")
        
        time.sleep(2)
        print("Fechar aba atual")
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(1)
        end_time = time.time()  # Armazena o tempo final
        execution_time = end_time - start_time  # Calcula o tempo de execução
        print(f"Tempo de execução da função ficha_tecnica para o dado '{dado}': {execution_time:.2f} segundos")