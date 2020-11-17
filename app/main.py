from flask import Flask, request, jsonify
from flask_cors import CORS
from app.torch_utils import transform_image, get_prediction

app = Flask(__name__)
CORS(app)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error':'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error':'format not supported'})
    
        try:
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            prediction = get_prediction(tensor)
            data = {'prediction': classes[int(prediction[0])]}
            return jsonify(data)
        except:
            return jsonify({'error':'error during prediction'})
