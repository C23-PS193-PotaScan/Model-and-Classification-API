import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model # untuk menggunakan fungsi load_model()
from tensorflow.keras.preprocessing.image import load_img, img_to_array # untuk menggunakan fungsi load_img()
from PIL import Image, ImageEnhance
import tensorflow as tf
import numpy as np


UPLOAD_FOLDER = './images/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

model = load_model('./workspace/pld_model.h5')
IMAGE_SIZE = (256, 256)

# This function to will return True if the file extension inside ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict(image_path):
    Class = ''

    img = load_img(image_path, target_size=IMAGE_SIZE)
    x = img_to_array(img)
    x /= 255 # normalize the pixel values of the image to be between 0 and 1
    x = np.expand_dims(x, axis=0) # add an extra dimension to match the input shape of the model
    images = np.vstack([x]) # stack the single image array into a batch of images

    prediction = model.predict(images, batch_size=10)
    predicted_class = np.argmax(prediction)

    if predicted_class == 0:
        Class = 'Early Blight'
    elif predicted_class == 1:
        Class = 'Healthy'
    else:
        Class = 'Late Blight'

    os.remove(image_path)
    return Class

app  = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def hello_world():
    return 'Response succes!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'anda belum mengunggah foto'}), 400
    file = request.files['file'] # 'file' adalah KEYnya
    if file.filename == '':
        return jsonify({'error' : 'tidak ada gambar yang dipilih'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'msg': 'foto berhasil diunggah', 'prediction':predict(file_path)})
    else:
        return jsonify({'error' : 'extensi file tidak sesuai, hanya menerima jpg, jpeg, dan png'}), 400

if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)))
