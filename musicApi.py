from flask import Flask, request
from flask_json import json_response

app = Flask(__name__)

@app.route('/')
def index():
    return 'music api is working'

@app.route('/music', methods=['POST','GET'])
def music():
    file = request.args.get('file')
    try:
        newFile = int(file)
        data = { 'result': 'true', 'file': newFile }
    except:
        data = { 'error': 'true', 'message': 'invalid file'}

    return json_response(data=data)
 
if __name__ == '__main__':
    app.run()