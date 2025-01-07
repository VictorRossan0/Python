import os
import cv2
import numpy as np

def load_images_from_folder(folder, img_size=(224, 224)):
    images = []
    labels = []
    for label in os.listdir(folder):
        label_path = os.path.join(folder, label)
        if os.path.isdir(label_path):
            for img_file in os.listdir(label_path):
                img_path = os.path.join(label_path, img_file)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.resize(img, img_size)
                    images.append(img)
                    labels.append(str(label))  # Converte para string normal
    return np.array(images), np.array(labels)

if __name__ == "__main__":
    images, labels = load_images_from_folder("data/train", img_size=(224, 224))
    print(f"Total de imagens carregadas: {len(images)}")
    print(f"Classes encontradas: {set(labels)}")
