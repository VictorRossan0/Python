import pytesseract
import pyautogui
import time
import cv2

# # Passo 1: Ler a primeira imagem
# imagem_1 = cv2.imread("Images/aprovisionar_servico.png")

# # Passo 2: Extrair texto da primeira imagem
# texto_1 = pytesseract.image_to_string(imagem_1, lang="por")

# print("Texto da primeira imagem:")
# print(texto_1)

# # Passo 3: Ler a segunda imagem
# imagem_2 = cv2.imread("Images/pcl.png")

# # Passo 4: Extrair texto da segunda imagem
# texto_2 = pytesseract.image_to_string(imagem_2, lang="por")

# print("Texto da segunda imagem:")
# print(texto_2)

# # Passo 5: Ler a segunda imagem
# imagem_3 = cv2.imread("Images/atividade_remota.png")

# # Passo 6: Extrair texto da segunda imagem
# texto_3 = pytesseract.image_to_string(imagem_3, lang="por")

# print("Texto da terceira imagem:")
# print(texto_3)

#Manda pra área de trabalho
pyautogui.hotkey('winleft','d')

#Localiza a imagem

time.sleep(3)
image_path = 'C:\\Users\\Hitss\\Desktop\\postman.png'

img = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)

pyautogui.moveTo(img.x,img.y)