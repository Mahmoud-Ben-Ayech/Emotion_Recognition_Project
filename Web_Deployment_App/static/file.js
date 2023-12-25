document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const predictionText = document.getElementById('prediction-text');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // Parse JSON response
        .then(data => {
            predictionText.innerHTML = `<strong>Predicted Emotion:</strong> ${data.prediction}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
