import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from keras_vggface.utils import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Carregar o modelo FaceNet para extração de embeddings
facenet_model = load_model('facenet_keras.h5')  # Certifique-se de ter o modelo disponível
detector = MTCNN()

# Função para extrair embeddings de uma face
def extract_embeddings(face_image):
    face_image = cv2.resize(face_image, (160, 160))  # Redimensionar para 160x160 (requisito FaceNet)
    face_image = np.expand_dims(face_image, axis=0)
    face_image = preprocess_input(face_image.astype('float32'))
    embeddings = facenet_model.predict(face_image)
    return embeddings[0]

# Banco de dados fictício para correspondência
known_faces = {
    "Amy": np.random.rand(128),  # Substituir por embeddings reais
    "Raj": np.random.rand(128),
    "Leonard": np.random.rand(128),
    "Penny": np.random.rand(128),
    "Sheldon": np.random.rand(128),
    "Bernadette": np.random.rand(128),
}

# Função para reconhecer a face
def recognize_face(embeddings, known_faces, threshold=0.5):
    best_match = None
    highest_similarity = 0
    
    for name, known_embedding in known_faces.items():
        similarity = cosine_similarity([embeddings], [known_embedding])[0][0]
        if similarity > highest_similarity and similarity > threshold:
            highest_similarity = similarity
            best_match = name
    
    return best_match if best_match else "Unknown"

# Carregar e processar a imagem
image_path = 'image.png'
image = cv2.imread(image_path)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
faces = detector.detect_faces(rgb_image)

# Processar cada face detectada
for face in faces:
    x, y, width, height = face['box']
    x, y = abs(x), abs(y)  # Corrigir coordenadas negativas
    face_image = rgb_image[y:y+height, x:x+width]
    
    try:
        embeddings = extract_embeddings(face_image)
        name = recognize_face(embeddings, known_faces)

        # Desenhar bounding box e nome na imagem
        cv2.rectangle(rgb_image, (x, y), (x+width, y+height), (0, 255, 0), 2)
        cv2.putText(rgb_image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    except Exception as e:
        print("Erro ao processar face:", e)

# Exibir a imagem processada
plt.figure(figsize=(10, 10))
plt.imshow(rgb_image)
plt.axis('off')
plt.show()
