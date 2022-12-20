from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from keras.preprocessing import image
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf


app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024*1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = image.load_img(UPLOAD_FOLDER+'/'+filename,target_size=(128,128))
        X = image.img_to_array(img)
        X = np.expand_dims(X,axis=0)
        images = np.vstack([X])
        new_model=tf.keras.models.load_model('modelExp.h5')
        value = new_model.predict(images)
        print(value)
        ans=" "
        if value[0][0]>value[0][1]:
            ans = "Normal Road "
        else:
            ans="Broken Tree "
        
        prediction = "prediction :" + ans
        flash(prediction)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()