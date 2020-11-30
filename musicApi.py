from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'music api is working'

@app.route('/music')
def music():
    file = request.args.get('file')
    try:
        newFile = int(file)
    except:
        return { 'error': 'true', 'message': 'invalid file'}

    return { 'result': 'true', 'file': newFile }
 
if __name__ == '__main__':
    app.run()