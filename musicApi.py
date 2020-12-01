from flask import Flask, request
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
FlaskJSON(app)

@app.route('/')
def index():
    now = datetime.utcnow()
    return json_response(time=now)

@app.route('/music', methods=['POST','GET'])
def music():
    file = request.args.get('file')
    try:
        newFile = int(file)
        return json_response(value=newFile)
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')

 
if __name__ == '__main__':
    app.run()