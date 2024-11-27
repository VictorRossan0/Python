import tensorflow as tf
from tensorflow.keras.models import load_model
from data_preprocessing import load_data

def evaluate_model():
    model = load_model('models/base_model.h5')
    _, val_gen = load_data('data/val')
    
    loss, acc = model.evaluate(val_gen)
    print(f"Acurácia do modelo: {acc * 100:.2f}%")

if __name__ == "__main__":
    evaluate_model()
