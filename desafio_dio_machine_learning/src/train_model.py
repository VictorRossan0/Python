import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from data_preprocessing import load_data

def create_model():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    for layer in base_model.layers:
        layer.trainable = False  # Congela as camadas do modelo base
    
    x = Flatten()(base_model.output)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(2, activation='softmax')(x)  # Altere o número de classes conforme necessário
    
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    train_gen, val_gen = load_data('data/train')
    
    model = create_model()
    
    history = model.fit(train_gen, validation_data=val_gen, epochs=10)
    model.save('models/base_model.h5')
    print("Modelo salvo com sucesso!")
