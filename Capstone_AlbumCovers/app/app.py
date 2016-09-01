# This script runs the application on a local server.

import pandas as pd
import graphlab as gl
import pickle
from flask import (Flask,
                  render_template,
                  request,
                  jsonify,
                  url_for
                  )
import binascii
import requests
from werkzeug import secure_filename
from shutil import copyfile
import os

app = Flask(__name__)

#----------------- READ IN MODEL -----------------#

with open('../model_build/svm_ddecade_model.pkl', 'r') as picklefile:
    svm_d_model = pickle.load(picklefile)        

with open('../model_build/svm_g_model.pkl', 'r') as picklefile:
    svm_g_model = pickle.load(picklefile)

#---------------- SET ROUTE TO TAKE IMAGES AND DL TO LOCAL DIRECTORY ----------------#
#allowed extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#path to upload director
app.config['UPLOAD_FOLDER'] = 'uploads/'

#specify allowed files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route("/result", methods=['POST'])
def upload():
    file = request.files['user_upload']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#---------------- BEGIN TO RUN TRANSFORMATIONS ON IMAGE INPUTS ---------------- #

        pic = gl.Image("./uploads/"+filename)

        #loading in dummy image since deep feature extractor only works in dataframe
        pic = [gl.image_analysis.resize(pic, 100, 100, 3, decode=True), gl.Image("../image_data_dump/1.jpg")]
        pic = gl.SFrame(pic)

        #extract features
        extractor = gl.feature_engineering.DeepFeatureExtractor(features = "X1", model='auto')
        extractor_g = extractor.fit(pic)
        features_g = extractor_g.transform(pic)

        #predict probabilities
        d_values = svm_d_model.predict_proba(features_g[0]["deep_features.X1"])
        d_keys = svm_d_model.classes_

        g_values = svm_g_model.predict_proba(features_g[0]["deep_features.X1"])
        g_keys = svm_g_model.classes_

        #dictionary these
        d_values = d_values.tolist()
        d_values = [round(item,3) for sublist in d_values for item in sublist]
        d_dict = dict(zip(d_keys, d_values))

        g_values = g_values.tolist()
        g_values = [round(item,3) for sublist in g_values for item in sublist]
        g_dict = dict(zip(g_keys, g_values))

        #return results
        result = {'decade': d_dict, 'genre': g_dict}
        return jsonify(result)


#---------------- CREATING AN API ----------------#
# Initialize the app

@app.route('/')
def welcome():
   with open("page.html", 'r') as viz_file:
       return viz_file.read()


if __name__ == '__main__':
    '''Connects to the server'''
    app.run()
