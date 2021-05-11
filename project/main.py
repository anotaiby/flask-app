# main.py

import os
from flask import Blueprint, render_template, redirect, flash, request, Flask
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import numpy as np
# Import keras
import tensorflow.keras as keras
from tensorflow.keras.models import load_model
from PIL import Image
import logging
import cv2
from numpy import array

main = Blueprint('main', __name__)
UPLOAD_FOLDER = 'project/static/uploads/'
DOWNLOAD_FOLDER = 'project/static/downloads/'
Best_models = 'project/model-090.model/'
ALLOWED_EXTENSIONS = {'jpg', 'png', '.jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/recognise', methods=['GET', 'POST'])
@login_required
def recognise():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # process_file(os.path.join(UPLOAD_FOLDER, filename), filename)
            m = load_model(os.path.join(Best_models))
            # logging.getLogger("tensorflow").setLevel(logging.WARNING)
            image1 = process_image(os.path.join(UPLOAD_FOLDER, filename))

            pred = model_prediction(m, image1)

            data = {
                # "processed_img": 'static/downloads/' + filename,
                "uploaded_img": '/static/uploads/' + filename,
                "pred": pred

            }
            return render_template("recognise.html", data=data, user=current_user.name)
    else:

        return render_template('recognise.html', user=current_user.name)


def process_image(filepath):
    return np.asarray(Image.open(filepath).resize((128, 128)).convert("L")) / 255.0


# Function to return prediction and probability
def model_prediction(model, img):
    predictions = model.predict(np.array([img]))

    if predictions[0][0] > predictions[0][1]:
        return f"powdery Mildew disease:{round(100 * predictions[0][0], 2)}%"
    elif predictions[0][1] > predictions[0][2]:
        return f"Downy Mildew disease:  {round(100 * predictions[0][1], 2)}%"
    else:
        return f"Black Rot disease: {round(100 * predictions[0][2], 2)}%"
