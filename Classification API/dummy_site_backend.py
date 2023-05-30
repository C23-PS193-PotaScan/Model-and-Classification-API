from flask import Flask, render_template, request
from tensorflow.keras.models import load_model # untuk menggunakan fungsi load_model()
from tensorflow.keras.preprocessing.image import load_img, img_to_array # untuk menggunakan fungsi load_img()
from PIL import Image, ImageEnhance
import os
import tensorflow as tf
import numpy as np

model = load_model('./workspace/pld_model.h5')
uploadedImage = './images/'
IMAGE_SIZE = (256, 256)


def predict(uploadedImage, image_path):
    Class = ''
    for fn in os.listdir(uploadedImage):
        if fn.endswith('.jpg') or fn.endswith('.jpeg') or fn.endswith('.png'):

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


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def output():
    imagefile = request.files['imagefile']
    image_path = uploadedImage + imagefile.filename
    imagefile.save(image_path)
    return render_template('index.html', prediction = predict(uploadedImage, image_path))
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)