from flask import Flask, request
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json


ALLOWED_EXTENSIONS = set(['mpg', 'mpeg', 'mp4'])
ALLOWED_SIZE = 10*1024*1024

def allowed_file(filename):
    if '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    return False


def allowed_size(file):
    if file.size < ALLOWED_SIZE:
        return True
    return False

app = Flask(__name__)
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
        elif file and allowed_file(file.filename):
            print('file', file)
            return json_response(
                filename=file.filename,
                description="original"
            )
        else:
            print('Some error occured.')
            raise JsonError(
                description="Some error occured."
            )

    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')

 
if __name__ == '__main__':
    app.run()