import cv2
import os
import numpy as np
import pickle
from imutils import paths
from keras.models import load_model
from helpers import resize_to_fit

def quebrar_captcha():
    # Load the rotulo_para_numero object from the "rotulos_modelo.dat" file
    with open('Database/rotulos_modelo.dat', 'rb') as arquivo_pickle:
        rotulo_para_numero = pickle.load(arquivo_pickle)

    # Load the trained model
    modelo = load_model("Database/modelo_treinado.hdf5")

    # List all the files in the "Images" folder
    arquivos = list(paths.list_files("Images"))
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        # Convert to black and white
        _, imagem = cv2.threshold(imagem, 128, 255, cv2.THRESH_BINARY_INV)

        # Find contours for each letter
        contornos, _ = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        regiao_letras = []

        # Filter out the contours that are actually letters
        for i, contorno in enumerate(contornos, 1):
            (x, y, largura, altura) = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            if area > 5.5:
                regiao_letras.append((x, y, largura, altura))
                print(f"Contornos{i}", (x, y, largura, altura))

        regiao_letras = sorted(regiao_letras, key=lambda x: x[0])
        # Draw the contours and separate the letters into individual files
        imagem_final = cv2.merge([imagem] * 3)
        previsao = []

        for i, retangulo in enumerate(regiao_letras, 1):
            x, y, largura, altura = retangulo
            imagem_letra = imagem[y:y+altura+5, x:x+largura+5]

            # Give the letter to the AI to determine which letter it is
            imagem_letra = resize_to_fit(imagem_letra, 20, 20)

            # Preprocess the image for Keras
            imagem_letra = np.expand_dims(imagem_letra, axis=2)
            imagem_letra = np.expand_dims(imagem_letra, axis=0)

            letra_prevista = modelo.predict(imagem_letra)
            letra_prevista = np.argmax(letra_prevista)
            letra_prevista = list(rotulo_para_numero.keys())[list(rotulo_para_numero.values()).index(letra_prevista)]
            previsao.append(letra_prevista)

        texto_previsao = "".join(previsao)
        print(texto_previsao)
        return texto_previsao

if __name__ == "__main__":
    quebrar_captcha()