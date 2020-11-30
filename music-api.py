from flask import Flask, request

api = Flask(__name__)

@api.route('/')
def index():
    return 'music api is working'

@api.route('/music')
def music():
    file = request.args.get('file')
    try:
        newFile = int(file)
    except:
        return { 'error': 'true', 'message': 'invalid file'}

    return { 'result': 'true', 'file': newFile }
 
if __name__ == '__main__':
    api.run()