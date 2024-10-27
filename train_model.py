import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.optimizers import Adam
import os

# Ensure the 'models' directory exists
if not os.path.exists('models'):
    os.makedirs('models')

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')  # Example: 10 classes
])

# Compile the model
model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Example: Dummy data for illustration
import numpy as np
train_images = np.random.random((100, 224, 224, 3))
train_labels = np.random.randint(10, size=(100,))

# Fit the model on your training data
model.fit(train_images, train_labels, epochs=10)

# Save the trained model in the native Keras format
model.save('models/exercise_model.keras')
