import cv2
import os
import numpy as np
import pickle
from imutils import paths
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit

dados = []
rotulos = []
pasta_base_imagens = "base_numeros_letras"

imagens = list(paths.list_images(pasta_base_imagens))

# Mapear rótulos para números inteiros
rotulo_para_numero = {rotulo: i for i, rotulo in enumerate(os.listdir(pasta_base_imagens))}
print("Mapeamento rótulo para número:", rotulo_para_numero)

for arquivo in imagens:
    rotulo = os.path.basename(os.path.dirname(arquivo))  # Obtendo o rótulo do diretório
    numero_rotulo = rotulo_para_numero[rotulo]

    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # padronizar a imagem em 20x20
    imagem = resize_to_fit(imagem, 20, 20)

    # adicionar uma dimensão para o Keras poder ler a imagem
    imagem = np.expand_dims(imagem, axis=2)

    # adicionar às listas de dados e rótulos
    rotulos.append(numero_rotulo)
    dados.append(imagem)

dados = np.array(dados, dtype="float") / 255
rotulos = np.array(rotulos)

# Codificar rótulos de treinamento no formato one-hot
numero_classes = len(rotulo_para_numero)
rotulos = to_categorical(rotulos, numero_classes)

# separação em dados de treino (75%) e dados de teste (25%)
(X_train, X_test, Y_train, Y_test) = train_test_split(dados, rotulos, test_size=0.25, random_state=0)

# salvar o labelbinarizer em um arquivo com o pickle
with open('Database/rotulos_modelo.dat', 'wb') as arquivo_pickle:
    pickle.dump(rotulo_para_numero, arquivo_pickle)

# criar e treinar a inteligência artificial
modelo = Sequential()

# criar as camadas da rede neural
modelo.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# criar a 2ª camada
modelo.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# mais uma camada
modelo.add(Flatten())
modelo.add(Dense(500, activation="relu"))
# camada de saída
modelo.add(Dense(numero_classes, activation="softmax"))

# compilar todas as camadas
modelo.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# treinar a inteligência artificial
print("Training the model:")
print(f"X_train shape: {X_train.shape}")
print(f"Y_train shape: {Y_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"Y_test shape: {Y_test.shape}")

modelo.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=26, epochs=10, verbose=1)

# salvar o modelo em um arquivo
modelo.save("Database/modelo_treinado.hdf5")
