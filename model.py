# -*- coding: utf-8 -*-
"""
Created on Tue May  9 13:11:08 2023

@author: delia
"""

from keras.models import load_model
from keras.utils import img_to_array
from keras.preprocessing import image
import keras.utils as image
#import numpy as np

from PIL import Image
import tensorflow as tf

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class ContactForm(FlaskForm):
    message = TextAreaField("Message")
    submit = SubmitField("Send")

img_height = 180
img_width = 180



model_food_prediction=load_model('MODEL_8.model')
model_aesthetics=load_model('model_aesthetics2.model')
def preprocess_image(image_path):

    op_img = Image.open(image_path)
    img_resize = op_img.resize((img_height, img_width))
    img2arr = img_to_array(img_resize)
    img_reshape = img2arr.reshape(1, img_height, img_width, 3)
    return img_reshape

def preprocess_aesthetics(image_path):
    img = image.load_img(image_path,target_size=(img_height,img_width,3))
    img = image.img_to_array(img)
    img = img/255
    img = img.reshape(1,img_height,img_width,3)
    return img
    


def predict_food(predict):
    pred_food = model_food_prediction.predict(predict)
    class_names = ['Food', 'Nonfood']
    if int(tf.round(pred_food[0][0])) == 0:
      prediction_class = class_names[1]
    if int(tf.round(pred_food[0][0])) == 1:
      prediction_class = class_names[0]
    #return pred[0][0], prediction_class
    return prediction_class

def predict_aesthetics(image):
    pred_aesthetics = model_aesthetics.predict(image)
    
    #Compute the aesthetics score
    score_max = 100
    features = 3
    score = (score_max/features)*(pred_aesthetics)
    
    score_final = sum(score[0])
    aesthetics = (round(score_final), 2)
    return aesthetics