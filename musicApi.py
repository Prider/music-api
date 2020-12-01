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
        return json_response(success=True, file=newFile)
    except:

        return json_response(error=True, messsage='invalid file')

 
if __name__ == '__main__':
    app.run()