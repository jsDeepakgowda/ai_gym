from flask import Flask, request, jsonify, render_template, send_file
from .exercise_detection import load_model, detect_exercise, real_time_feedback
from .rep_counting import count_reps
from .calorie_tracking import estimate_calories
import cv2
import os
import numpy as np
import moviepy.editor as mpy
import imageio_ffmpeg as ffmpeg

# Ensure that imageio-ffmpeg is correctly installed
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg.get_ffmpeg_exe()

# Specify the path to the ImageMagick binary
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"  # Update this path if needed

app = Flask(__name__)
model = load_model('models/exercise_model.keras')  # Ensure correct model path
leaderboard = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/analyze", methods=["POST"])
def analyze_workout():
    video = request.files["video"]
    user_data = {
        "name": request.form["name"],
        "age": int(request.form["age"]),
        "weight": float(request.form["weight"]),
        "goals": request.form["goals"]
    }
    
    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    video_path = os.path.join("uploads", video.filename)
    video.save(video_path)
    frames = extract_frames(video_path)
    if not frames:
        return jsonify({"error": "Failed to extract frames from the video."}), 400
    exercise_type = int(detect_exercise(frames[0], model))  # Ensure it's a regular int
    reps = int(count_reps(frames))  # Ensure it's a regular int
    calories = float(estimate_calories(exercise_type, len(frames) / 30))  # Ensure it's a float
    feedback_frame, detailed_feedback = add_overlay_with_feedback(frames[0])  # Generate visual overlay and feedback
    feedback_path = os.path.join("uploads", "feedback_frame.jpg")
    cv2.imwrite(feedback_path, feedback_frame)
    badges = award_badges(reps, calories)
    workout_recommendations = recommend_workouts(user_data, exercise_type, reps, calories)
    update_leaderboard(user_data['name'], reps, calories, badges)

    # Auto-edit the video for social media
    edited_video_path = auto_edit_video(video_path)
    return jsonify({
        "exercise": exercise_type,
        "reps": reps,
        "calories": calories,
        "badges": badges,
        "workout_recommendations": workout_recommendations,
        "leaderboard": get_leaderboard(),
        "feedback_frame": feedback_path,  # Return the path to the feedback frame image
        "detailed_feedback": detailed_feedback,  # Return detailed feedback and suggestions
        "edited_video": edited_video_path  # Path to the edited video
    })

@app.route("/feedback_frame")
def feedback_frame():
    return send_file("uploads/feedback_frame.jpg", mimetype="image/jpeg")

@app.route("/edited_video")
def edited_video():
    return send_file("uploads/edited_video.mp4", mimetype="video/mp4")

def extract_frames(video_path):
    try:
        vidcap = cv2.VideoCapture(video_path)
        success, frame = vidcap.read()
        frames = []
        frame_rate = 5  # Extract every 5th frame
        count = 0
        while success:
            if count % frame_rate == 0:
                resized_frame = cv2.resize(frame, (224, 224))
                frames.append(resized_frame)
            success, frame = vidcap.read()
            count += 1
        return frames
    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

def recommend_workouts(user_data, exercise_type, reps, calories):
    # Example recommendation logic based on user goals and performance
    recommendations = []
    if "strength" in user_data["goals"].lower():
        recommendations.append("Strength training 3 times a week with progressive overload.")
    if "cardio" in user_data["goals"].lower():
        recommendations.append("Cardio exercises like running or cycling 4 times a week.")
    if "flexibility" in user_data["goals"].lower():
        recommendations.append("Flexibility exercises like yoga or pilates 3 times a week.")
    if not recommendations:
        recommendations.append("Balanced workout plan with a mix of cardio, strength, and flexibility exercises.")
    return recommendations

def award_badges(reps, calories):
    badges = []
    if reps >= 10:
        badges.append('10 Reps Badge')
    if calories >= 100:
        badges.append('100 Calories Badge')
    return badges

def update_leaderboard(name, reps, calories, badges):
    global leaderboard
    leaderboard.append({
        "name": name,
        "reps": reps,
        "calories": calories,
        "badges": badges
    })
    # Sort leaderboard by reps, then by calories
    leaderboard = sorted(leaderboard, key=lambda x: (x["reps"], x["calories"]), reverse=True)

def get_leaderboard():
    return leaderboard[:10]  # Return top 10

def add_overlay_with_feedback(frame):
    overlay = frame.copy()
    # Example: Draw a rectangle and provide feedback (replace with actual posture analysis)
    cv2.rectangle(overlay, (50, 50), (200, 200), (0, 255, 0), 2)
    feedback_text = "Keep your back straight and avoid leaning forward."
    alpha = 0.4  # Transparency factor
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    return frame, feedback_text

def auto_edit_video(video_path):
    # Ensure ffmpeg is in PATH or specify the path
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg.get_ffmpeg_exe()

    # Example auto-editing: Trim the first 5 seconds and add a title overlay
    clip = mpy.VideoFileClip(video_path).subclip(0, 5)
    txt_clip = mpy.TextClip("Workout Highlights", fontsize=50, color='white').set_position('center').set_duration(3)
    video = mpy.CompositeVideoClip([clip, txt_clip.set_start(0)], size=(640, 360))  # Resize for memory efficiency
    edited_video_path = "uploads/edited_video.mp4"
    video.write_videofile(edited_video_path, codec="libx264", audio_codec="aac", threads=1, preset="ultrafast")
    return edited_video_path

if __name__ == "__main__":
    app.run(debug=True)
