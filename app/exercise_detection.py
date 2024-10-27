import tensorflow as tf
import cv2
import numpy as np

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

def detect_exercise(frame, model):
    input_image = cv2.resize(frame, (224, 224))
    input_image = np.expand_dims(input_image, axis=0)
    predictions = model.predict(input_image)
    exercise_type = np.argmax(predictions, axis=1)[0]  # Get the index of the highest prediction
    return exercise_type

def real_time_feedback(frame, model):
    # Add detailed feedback logic
    feedback = []
    
    # Example mock feedback logic
    feedback.append("Keep your back straight to avoid strain.")
    feedback.append("Ensure your knees are aligned with your toes.")
    feedback.append("Keep your core engaged for better stability.")

    # Add visual overlays
    overlay = frame.copy()
    cv2.rectangle(overlay, (50, 50), (200, 200), (0, 255, 0), 2)  # Example rectangle
    alpha = 0.4  # Transparency factor
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame, feedback
