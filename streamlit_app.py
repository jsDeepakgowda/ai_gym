import streamlit as st
import requests
import os

st.set_page_config(page_title="AI-Powered Gym Platform", layout="wide")

st.title("AI-Powered Gym Platform")

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Collect user information
st.sidebar.header("User Information")
user_name = st.sidebar.text_input("Name")
user_age = st.sidebar.number_input("Age", min_value=0, max_value=100, step=1)
user_weight = st.sidebar.number_input("Weight (kg)", min_value=0, max_value=200, step=1)
user_goals = st.sidebar.text_area("Fitness Goals")

uploaded_video = st.file_uploader("Upload your workout video", type=["mp4", "mov"])

if uploaded_video is not None:
    video_path = os.path.join('uploads', 'video.mp4')
    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())
    st.success("Video uploaded successfully!")

if st.button("Analyze Workout"):
    if uploaded_video is not None:
        with st.spinner('Analyzing your video...'):
            response = requests.post("http://localhost:5000/analyze", 
                                     files={"video": open(video_path, "rb")},
                                     data={"name": user_name, "age": user_age, "weight": user_weight, "goals": user_goals})
            if response.status_code == 200:
                result = response.json()
                st.subheader("Analysis Results")
                st.write(f"**Exercise Type:** {result['exercise']}")
                st.write(f"**Reps:** {result['reps']}")
                st.write(f"**Calories Burned:** {result['calories']}")
                st.write(f"**Badges:** {result['badges']}")
                st.write(f"**Workout Recommendations:** {', '.join(result['workout_recommendations'])}")
                
                # Display visual feedback frame
                st.image(result['feedback_frame'], caption='Feedback Frame')
                
                # Display detailed feedback and suggestions
                st.subheader("Detailed Feedback and Suggestions")
                st.write(result.get('detailed_feedback', 'No feedback available'))

                # Display leaderboard
                st.subheader("Leaderboard")
                for entry in result['leaderboard']:
                    st.write(f"Name: {entry['name']}, Reps: {entry['reps']}, Calories: {entry['calories']}, Badges: {', '.join(entry['badges'])}")

                # Display auto-edited video for social media
                st.subheader("Edited Video for Social Media")
                st.video(result['edited_video'])
                
            else:
                st.error("Error analyzing the workout video.")
    else:
        st.write("Please upload a workout video.")
