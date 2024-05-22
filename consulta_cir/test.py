import pytesseract
import cv2
import os

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Passo 1: Ler a primeira imagem
# imagem_1 = cv2.imread("Images/header.png")
imagem_1 = cv2.imread("Screenshots/solid.png")

# Passo 2: Extrair texto da primeira imagem
texto_1 = pytesseract.image_to_string(imagem_1, lang="por")

print("Texto da primeira imagem:")
print(texto_1)

imagem_2 = cv2.imread("Images/solid.png")

texto_2 = pytesseract.image_to_string(imagem_2, lang="por")

print("Texto da segunda imagem:")
print(texto_2)

