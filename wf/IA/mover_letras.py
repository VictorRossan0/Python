import os
import shutil
import pickle
from keras.models import load_model
from PIL import Image
import numpy as np

# Carregar modelo treinado
modelo = load_model('Database/modelo_treinado.hdf5')

# Carregar rótulos
with open('Database/rotulos_modelo.dat', 'rb') as f:
    rotulos = pickle.load(f)
    print("Rótulos carregados:", rotulos)

# Diretório de entrada
diretorio_entrada = 'IA/letras'

# Diretório de saída base
diretorio_saida_base = 'IA/base_numeros_letras'

# Dimensões da imagem
img_width, img_height = 20, 20  # Substitua pelas dimensões corretas do seu modelo

# Iterar sobre os arquivos no diretório de entrada
for arquivo in os.listdir(diretorio_entrada):
    caminho_arquivo = os.path.join(diretorio_entrada, arquivo)

    # Verificar se é um arquivo
    if os.path.isfile(caminho_arquivo):
        # Pré-processamento da imagem
        img = Image.open(caminho_arquivo).convert('L')  # Abrir a imagem em escala de cinza
        img = img.resize((img_width, img_height))  # Redimensionar para as dimensões do modelo
        img_array = np.array(img)  # Converter para array NumPy
        img_array = np.expand_dims(img_array, axis=0)  # Adicionar dimensão extra para o modelo Keras
        img_array = np.expand_dims(img_array, axis=-1)  # Adicionar dimensão de canal (escala de cinza)

        # Realizar previsão
        previsao = modelo.predict(img_array)

        # Verificar a saída da previsão
        print("Previsão:", previsao)

        # Encontrar o índice com a maior probabilidade na previsão
        indice_max_probabilidade = np.argmax(previsao)
        print("Índice com maior probabilidade:", indice_max_probabilidade)

        # Verificar se o índice está presente no dicionário de rótulos
        if indice_max_probabilidade in rotulos.values():
            rotulo_predito = [chave for chave, valor in rotulos.items() if valor == indice_max_probabilidade][0]
            print("Rótulo predito:", rotulo_predito)

            # Mover o arquivo para o diretório de saída correspondente
            diretorio_saida_rotulo = os.path.join(diretorio_saida_base, rotulo_predito)
        
            # Criar diretório de saída se não existir
            os.makedirs(diretorio_saida_rotulo, exist_ok=True)

            # Mover o arquivo para o diretório de saída correspondente
            shutil.move(caminho_arquivo, os.path.join(diretorio_saida_rotulo, arquivo))
        else:
            print(f"Índice {indice_max_probabilidade} não encontrado no dicionário de rótulos.")
