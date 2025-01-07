import numpy as np
from PIL import Image  # Ensure you import PIL for image processing
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from tensorflow.keras.models import load_model
import tensorflow as tf  # Add this to fix `tf` reference

# Load the trained model
model = load_model("models/model.keras")

# Remove the final classification layer to get embeddings
model = tf.keras.Model(inputs=model.input, outputs=model.layers[-2].output)

# Load embeddings and labels
with open("models/embeddings.pkl", "rb") as f:
    embeddings = pickle.load(f)

with open("models/labels.pkl", "rb") as f:
    labels = pickle.load(f)

def recommend(image, top_k=5):
    # Preprocess the input image
    image = image.astype("float32") / 255.0  # Normalize to [0, 1]
    embedding = model.predict(np.expand_dims(image, axis=0))

    # Compute cosine similarities
    similarities = cosine_similarity(embedding, embeddings)

    # Get top-k indices
    top_indices = np.argsort(similarities[0])[-top_k:][::-1]

    # Return the top-k most similar images and their labels
    return [(labels[i], similarities[0][i]) for i in top_indices]


# Example usage
if __name__ == "__main__":
    # Load a query image
    query_image_path = "data/train"  # Replace with the actual path
    query_image = np.array(Image.open(query_image_path).resize((224, 224)))

    # Get recommendations
    recommendations = recommend(query_image, top_k=5)

    # Print recommendations
    for label, similarity in recommendations:
        print(f"Label: {label}, Similarity: {similarity}")
