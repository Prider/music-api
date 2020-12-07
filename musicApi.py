from flask import Flask, request
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json

from werkzeug.utils import secure_filename
import os

import librosa
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

ALLOWED_EXTENSIONS = set(['mpg', 'mpeg', 'mp4', 'mp3'])
UPLOAD_FOLDER = './uploads'
ALLOWED_SIZE = 10*1024*1024

def featureExtract(row, y, sr):
  rmse = librosa.feature.rms(y=y)
  spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
  spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
  rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
  zcr = librosa.feature.zero_crossing_rate(y)

  rmse = np.mean(rmse[0])
  spec_cent = np.mean(spec_cent[0])
  spec_bw = np.mean(spec_bw[0])
  rolloff = np.mean(rolloff[0])
  zcr = np.mean(zcr[0])

  row.update({
    'rmse': rmse,
    'spec_cent': spec_cent,
    'spec_bw': spec_bw,
    'rolloff': rolloff,
    'zcr': zcr
  })
  return row

def featureExtractMfcc(row, y, sr):
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    for index in range(len(mfcc)):
        row.update({'mfcc_{}'.format(index): str(np.mean(mfcc[index]))})
    return row

def predictAudio(filePath):
    y, sr  = librosa.load(filePath, mono=True, offset=5.0, duration=20.0) 

    row = {}
    row = featureExtract(row, y, sr)
    row = featureExtractMfcc(row, y, sr)
    x = pd.DataFrame()
    x = x.append(row, ignore_index=True)
    scaler = StandardScaler()
    scaled_x = scaler.fit_transform(x)
    scaled_x = scaled_x.astype('float32')
    happyModel = load_model('happy_birth_day_model.h5')
    result = happyModel.predict_classes(scaled_x)
    return result


def allowed_file(filename):
    if '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    return False

def allowed_size(file):
    if file.size < ALLOWED_SIZE:
        return True
    return False

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
FlaskJSON(app)

@app.route('/')
def index():
    now = datetime.utcnow()
    return json_response(time=now, description='music api is working')
    
@app.route('/music', methods=['POST'])
def music():
    try:
        file = request.files['file']
        size =  request.content_length
        if not file:
            print('file not found')
            raise JsonError(description='file not found')
        elif size > ALLOWED_SIZE:
            print('file size is more than allowed size')
            raise JsonError(
                description="file size is more than allowed size 10Mb."
            )
        elif not allowed_file(file.filename):
            print('This file extesion not allowed.')
            raise JsonError(
                description="This file extesion not allowed."
            )
        elif not file and not allowed_file(file.filename):
            print('Some error occured.')
            raise JsonError(
                description="Some error occured."
            )
        else:
            filename = secure_filename(file.filename)
            print('filename', filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            filePath = './uploads/{}'.format(file.filename);
            result = predictAudio(filePath)
            original = 'not original'
            if ( result and result[0] == 1):
                original = 'original'
            
            return json_response(
                filename=file.filename,
                description=original
            )
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')

 
if __name__ == '__main__':
    app.run()