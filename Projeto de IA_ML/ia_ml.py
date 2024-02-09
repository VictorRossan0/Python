import tensorflow as tf
from tensorflow import keras

# Carregar o conjunto de dados MNIST (dígitos escritos à mão)
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Pré-processamento dos dados
x_train = x_train / 255.0
x_test = x_test / 255.0

# Construir o modelo de rede neural
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Compilar e treinar o modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5)

# Avaliar o modelo
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Acurácia do teste:', test_acc)