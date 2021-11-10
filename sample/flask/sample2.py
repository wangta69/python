from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return '<templates><body><h1>Hello World</h1></body></templates'


@app.route('/hello/<user>')
def hello_name(user):
    return render_template('templates.html', name=user)
    # return render_template('./templates/templates.templates', name=user)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=8000, host='127.0.0.1', debug = True)