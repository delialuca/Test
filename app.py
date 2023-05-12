# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:25:55 2023

@author: delia
"""

import os
from flask import Flask, flash, request, redirect, url_for
from flask import render_template 
from werkzeug.utils import secure_filename


import numpy as np
import pandas as pd

from tensorflow import keras
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from keras.backend import set_session
import tensorflow as tf
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


from model import preprocess_image, predict_food, preprocess_aesthetics, predict_aesthetics
from model import ContactForm

#import sqlite3
#connection=sqlite3.connect("feedback.db")
#print(connection.total_changes)       #checked connection
# cursor = connection.cursor()
# cursor.execute("CREATE TABLE feedback(feedback_text TEXT)")
# cursor.execute("INSERT INTO feedback VALUES('very pleased')")

# rows = cursor.execute("SELECT feedback_text FROM feedback").fetchall()
# print(rows)



#basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}

style = 'static/style.css'

F='Food'
N='Nonfood'

favicon='static/favicon.png'
intro_box='static/intro_box.svg'
adjust='static/adjust.jpg'

bg_index='static/bg_index.jpg'
bg_info='static/bg_info.jpg'





app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/', methods={'GET', 'POST'})
def upload_file():
    #initial webpage load
    if request.method == 'GET':
        return render_template('index.html', style=style, bg_index=bg_index)
    else: #request method is POST
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # If it doesn'y have the right extension
        if not allowed_file(file.filename):
            flash('I only accept files of types'+str(ALLOWED_EXTENSION))
            return redirect(request.url)
        
        ## When a user uploads a file with good parameters
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   ##upload the user file to my folder to apply the ML model on it
            #img = os.path.join(app.config['UPLOAD_FOLDER'], filename)
           
            #session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            
        return redirect(url_for('uploaded_file', filename=filename))
    
        
@app.route('/uploads/<filename>', methods={'GET', 'POST'})

def uploaded_file(filename):
    # from flask import send_from_directory
    # return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    


    test_image_f = preprocess_image(UPLOAD_FOLDER+'/'+filename)
    result_f = predict_food(test_image_f)
    
    test_image_a = preprocess_aesthetics(UPLOAD_FOLDER+'/'+filename)
    result_a = predict_aesthetics(test_image_a)
    #test_image_src = os.path.join(filename)
    
    if result_f == F:
        test_image_a = preprocess_aesthetics(UPLOAD_FOLDER+'/'+filename)
        result_a = predict_aesthetics(test_image_a)
        result = result_a
       # results.append(result_a)
    else:
        result = 'Not enough food in your image'
        
    return render_template("index.html", predictions = str(result), style=style, bg_index=bg_index)


            

  
    

        
    

    # #with mySession.as_default():
    # with myGraph.as_default():
    #         myModel = tf.keras.models.load_model('MODEL_8.model')
    #         #set_session(mySession)
    #         #myModel = load_model_from_file()
    #         result = myModel.predict(test_image)
    #         image_src = '/'+UPLOAD_FOLDER+'/'+filename
    #         if result[0] < 0.5:
    #             answer = "<div class='col text-center'><img width='255' height='255' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+F+" "+str(result[0])+"</h4></div><div class='col'></div><div class='w-100'></div>"  
    #         else:
    #             answer = "<div class='col'></div><div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+N+" "+str(result[0])+"</h4></div><div class='w-100'></div>"
    #             results.append(answer)
    #             return render_template('index.html',myX=F,myY=N,mySampleX=sampleX,mySampleY=sampleY,len=len(results),results=results)



        
   

@app.route('/info') 
def info():
    return render_template('info.html', bg_info=bg_info)         



@app.route('/index', methods =["GET", "POST"])
def home():
    #print(request.form.get("fb"))
    fb= request.form.get("fb")
    photo=request.form.get("photoname")
    feedback.append(fb)
    photos.append(photo)
    res=pd.DataFrame({'photo': photo,'feedback': fb}, index=[0])
    res.to_csv('./feedback.csv')
    #print("Data is saved")
    return render_template('index.html', style=style, bg_index=bg_index)
        

            
def main():
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_SIZE'] = 16 * 1024 * 1024  ##16Mb upload limit
    
    app.run(port=5000, debug=False)





## Create a list of results
#results = []
feedback = []
photos = []
#Launch everything
main()

# if __name__ == '__main__':
#     app.run(debug = True)