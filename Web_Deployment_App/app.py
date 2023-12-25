from flask import Flask, render_template, request,jsonify
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import cv2
from keras.applications.vgg16 import preprocess_input

app = Flask(__name__,template_folder='')
model = load_model('model_web_app.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return render_template('index.html', prediction="No image uploaded.")

    img = request.files['image']
    img_array = preprocess_image(img)

    # Reshape the array to match the model input shape
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    predictions = model.predict(img_array)
    emotion_label = get_emotion_label(np.argmax(predictions))

    return jsonify({"prediction": emotion_label})

def preprocess_image(img):
    img_path = 'temp.jpg'  
    img.save(img_path)

    # Read the image using OpenCV and convert to grayscale
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48, 48))  

    # Ensure the image has only one channel (grayscale)
    img_array = np.expand_dims(img, axis=-1)

    # Preprocess the image
    img_array = img_array.astype('float32') / 255.0  # Normalize to [0, 1]

    return img_array


def get_emotion_label(emotion_idx):
    emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
    if 0 <= emotion_idx < len(emotion_labels):
        return emotion_labels[emotion_idx]
    else:
        return "Unknown Emotion"


if __name__ == '__main__':
    app.run(debug=True)
