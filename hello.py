
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request

from flask import url_for



app = Flask(__name__)
# @app.route('/')
# def index():
#     return 'index'

# @app.route('/login')
# def login():
#     return 'login'

# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)



@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)

def valid_login(username, password):
    dic = dict()
    dic["xuan"] = "20001020"
    if username not in dic:
        return False
    if dic[username] == password:
        return True
    else:
        return False

def log_the_user_in(username):
    return f"Hello, {username}"

