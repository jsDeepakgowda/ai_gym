def estimate_calories(exercise_type, duration):
    # Mock calorie estimation logic
    calories_per_minute = {
        0: 8,   # Example exercise type
        1: 10,  # Another exercise type
        2: 12   # And so on
    }
    calories = calories_per_minute.get(exercise_type, 8) * (duration / 60)
    return calories
