from keras.applications.resnet50 import ResNet50
import sys
import os
import glob
import re
import uuid
import numpy as np
import tensorflow as tf
import base64

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
MODEL_PATH = 'models/your_model.h5'

print('Model loading...')
model = ResNet50(weights='imagenet')
print('Model loaded. Started serving...')


def deleting_image(img_path):
    print('Deleting File at Path: ' + img_path)
    os.remove(img_path)
    print('Deleting File at Path - Success - ')


def model_predict(img_path, model):
    original = image.load_img(img_path, target_size=(224, 224))
    numpy_image = image.img_to_array(original)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = preprocess_input(image_batch, mode='caffe')
    preds = model.predict(processed_image)
    return preds

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.form['img']
        
        decoded = base64.b64decode(f)

        file_name =  f"{uuid.uuid4()}.png"

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(file_name))
        
        output_file = open(file_path, 'wb')
        output_file.write(decoded)

        print('Begin Model Prediction...')

        #preds = model_predict(file_path, model)

        print('End Model Prediction...')
        #pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        #result = str(pred_class[0][0][1])               # Convert to string

        deleting_image(file_path)

        return jsonify({"result": 1})
    return None


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True, threaded=False)
    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
