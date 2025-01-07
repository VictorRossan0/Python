import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
from data_loader import load_images_from_folder

# Suppress OneDNN warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Function to create the model
def create_model(input_shape=(224, 224, 3), num_classes=10):
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Freeze some layers
    for layer in base_model.layers[:143]:  # Freeze up to `conv4_block6_out`
        layer.trainable = False
    for layer in base_model.layers[143:]:
        layer.trainable = True

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Load data
images, labels = load_images_from_folder("data/train")

# Ensure images are NumPy arrays
images = np.array(images, dtype=np.float32)

# Normalize image pixel values to range [0, 1]
images = images / 255.0

# Convert labels to integer indices
label_to_index = {label: idx for idx, label in enumerate(set(labels))}
labels = np.array([label_to_index[label] for label in labels], dtype=np.int32)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    images, labels, test_size=0.2, random_state=42, stratify=labels
)

# Check dataset sizes and balance
print(f"Number of training samples: {len(X_train)}, Number of test samples: {len(X_test)}")
print("Training label distribution:", np.bincount(y_train))
print("Test label distribution:", np.bincount(y_test))

# Create and train the model
model = create_model(input_shape=X_train.shape[1:], num_classes=len(label_to_index))
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

# Save the model in the new format
model.save("models/model.keras")
