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
    app.run(debug=True, port=5000)

'''
The ALLOWED_EXTENSIONS set is defined with the allowed file extensions as its elements. In this case, the allowed extensions are 'jpg', 'jpeg', and 'png'.
The allowed_file function takes a filename as input.
The function uses the rsplit method to split the filename into two parts based on the rightmost occurrence of the '.' character. This will separate the filename and the file extension.
The second part of the split result, obtained with [1], represents the file extension.
The function checks if the file extension obtained from step 4 is in lowercase and matches any of the allowed extensions defined in the ALLOWED_EXTENSIONS set.
If the file extension is in lowercase and matches one of the allowed extensions, the function returns True, indicating that the file is allowed. Otherwise, it returns False.

rsplit('.', 1) is used to split the filename into two parts based on the rightmost occurrence of the '.' character.

The second parameter, 1, in rsplit('.', 1) specifies the maximum number of splits to perform. In this case, setting it to 1 means that the string will be split into two parts at most.
Here's how it works:
The rsplit method starts searching for the '.' character from the right side of the string (hence the 'r' in rsplit).
When it finds the rightmost '.' character, it splits the string into two parts. The part before the '.' character becomes the first part, and the part after the '.' character becomes the second part.
By setting the second parameter to 1, it ensures that only one split is performed. This is useful when dealing with filenames because it allows you to extract the file extension while preserving the rest of the filename intact.
For example, if the filename is "image.jpg", filename.rsplit('.', 1) will return a list with two elements: ['image', 'jpg']. The first element is the filename without the extension, and the second element is the file extension.
Overall, rsplit('.', 1) splits the filename into two parts at the rightmost occurrence of the '.' character, allowing you to extract the file extension.

'''

'''
First, an instance of the Flask application is created with app = Flask(__name__). This initializes the Flask application.
The UPLOAD_FOLDER variable is set as a configuration option in the Flask app using app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER. This specifies the folder where the uploaded files will be stored.
The @app.route('/upload', methods=['POST']) decorator defines a route for the '/upload' URL with the HTTP method 'POST'. This means that this route will be triggered when a POST request is made to the '/upload' URL.
The upload_file() function is the handler for the '/upload' route. It is executed when a POST request is made to the '/upload' URL.
Inside the upload_file() function, it checks if the 'file' key is present in the request files using 'file' not in request.files. If it is not present, it returns a JSON response with an error message and a status code of 400 (Bad Request).
If the 'file' key is present, it retrieves the uploaded file from the request using file = request.files['file']. The 'file' here corresponds to the name of the file input field in the HTML form that submits the file.
It checks if the filename is empty with file.filename == ''. If it is empty, it returns a JSON response with an error message and a status code of 400.
If the filename is not empty and the file has an allowed file extension (checked using the allowed_file() function), it proceeds to save the file.
The secure_filename() function is used to ensure that the filename is secure and does not contain any potentially dangerous characters.
The file is saved to the specified upload folder by joining the UPLOAD_FOLDER path with the secure filename using os.path.join(app.config['UPLOAD_FOLDER'], filename).
Finally, it returns a JSON response with a success message and any additional information you want to include, such as a prediction result.
Overall, this code handles file uploads by checking for the presence of the file, validating the filename and file extension, and saving the file to the specified upload folder. It provides appropriate error messages in case of missing or invalid files and returns a success message upon successful file upload.
'''