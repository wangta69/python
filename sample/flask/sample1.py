from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<templates><body><h1>Hello World</h1></body></templates'

if __name__ == '__main__':
    app.run(debug=True)