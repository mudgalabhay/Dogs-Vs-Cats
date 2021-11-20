import os
import time

from django.shortcuts import render

from tensorflow.keras import models
from tensorflow.keras.models import load_model
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def homepage(request):

    return render(request, "index.html")


# 1. Upload an image
# 2. Save the uploaded image
# 3. Function to make prediction on the image
# 4. Show the results

UPLOAD_FOLDER = "main/static/uploaded_images"


def predict(image_file):

    model = load_model('main/model_3.h5')

    pred_file_name = os.listdir(UPLOAD_FOLDER)

    pred_df = pd.DataFrame({'id': pred_file_name})

    pred_gen = ImageDataGenerator(rescale=1./255)

    pred_generator = pred_gen.flow_from_dataframe(
                    pred_df,

                    UPLOAD_FOLDER,

                    x_col='id',

                    y_col=None,

                    target_size=(150, 150),  # resize image to 150x150

                    class_mode=None,

                    shuffle=False,

                    validate_filenames=False)

    predictions = model.predict(pred_generator)

    pred = [1 if p > 0.5 else 0 for p in predictions]

    pred_df['category'] = pred

    pred_df['category'] = pred_df['category'].map({1: 'dog', 0: 'cat'})

    return list(pred_df[pred_df['id'] == image_file]['category'])[0]

def upload_predict(request):

    if request.method == "POST":

        image_file = request.FILES["uploaded_image"]

        file_name = str(time.strftime("%Y%m%d-%H%M%S")) + str(image_file)

        if image_file:

            image_loc = UPLOAD_FOLDER + "/" + str(time.strftime("%Y%m%d-%H%M%S")) + str(image_file)

            with open(image_loc, 'wb') as file:

                file.write(image_file.read())

            result = predict(str(time.strftime("%Y%m%d-%H%M%S")) + str(image_file))

            return render(request, "index.html", {'prediction': result, 'image_filename': file_name})

    return render(request, "index.html")

