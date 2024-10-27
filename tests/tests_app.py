import unittest
from app.api import app
from app.exercise_detection import load_model, detect_exercise, real_time_feedback
from app.rep_counting import count_reps
from app.calorie_tracking import estimate_calories

class TestGymPlatform(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_analyze_workout(self):
        response = self.app.post('/analyze', content_type='multipart/form-data', data={
            'video': (open('path_to_test_video.mp4', 'rb'), 'test_video.mp4')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("exercise", response.json)
        self.assertIn("reps", response.json)
        self.assertIn("calories", response.json)
        self.assertIn("feedback", response.json)

if __name__ == "__main__":
    unittest.main()
