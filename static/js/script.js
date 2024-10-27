function analyzeWorkout() {
    let videoUpload = document.getElementById('video-upload').files[0];
    if (!videoUpload) {
        alert('Please upload a video file.');
        return;
    }

    let formData = new FormData();
    formData.append('video', videoUpload);

    fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerHTML = `
            <p>Exercise Type: ${data.exercise}</p>
            <p>Reps: ${data.reps}</p>
            <p>Calories Burned: ${data.calories}</p>
            <p>Feedback: ${data.feedback}</p>
        `;
    })
    .catch(error => console.error('Error:', error));
}
