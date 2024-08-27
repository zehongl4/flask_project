
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request

from flask import url_for

import pprint
import pymysql
from pymysql import cursors
from flask_bcrypt import Bcrypt


def conn_mysql():
    return pymysql.connect(
        host="127.0.0.1",  # This is typically localhost IP address
        port=3306,         # Standard MySQL port number
        user="root",       # Your MySQL username
        password="lanzehong0997",  # Replace 'yourpassword' with your actual root password
        database="flask_db",  # Correct database name containing the user_log table
        charset="utf8"     # Charset for encoding the data
    )

#query
def query_data(sql, params=None):
    conn = conn_mysql()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        conn.close()



#update or insert
def insert_or_update_data(sql, params=None):
    conn = conn_mysql()  # Make sure conn_mysql() correctly configures the connection
    try:
        cursor = conn.cursor()
        # Execute SQL with params if they exist
        if params is not None:
            cursor.execute(sql, params)  # Pass the parameters here
        else:
            cursor.execute(sql)  # Only if you really mean to execute without params
        conn.commit()
        
    except pymysql.Error as error:
        print(f"Database error: {error}")
        # It might be useful to rollback in case of an error
        conn.rollback()
    finally:
        conn.close()




app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)



@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if valid_login(uname,pwd):
            return log_the_user_in(uname)
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_form', methods=['POST', 'GET'])
def register_form():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if not pwd:
            error = "Password is needed"
            return render_template('register.html', error=error)
        if uname.isalnum():
            sql1 = "SELECT password FROM user_log WHERE username = %s"
            result = query_data(sql1, (uname,)) 
            if result:
                error = "User Exists"
            else:
                pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
                sql2 = "INSERT INTO user_log (username, password) VALUES (%s, %s)"
                data = (uname, pwd_hash)
                insert_or_update_data(sql2, data)
                return "User registered successfully!"
        else:
            error = 'Invalid username/'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('register.html', error=error)

@app.route('/modify', methods=['POST', 'GET'])
def modify():
    return render_template("modify.html")

@app.route('/new_password', methods=['POST', 'GET'])
def new_password():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if not pwd:
            error = "Password is needed"
            return render_template('modify.html', error=error)
        if uname.isalnum():
            sql1 = "SELECT password FROM user_log WHERE username = %s"
            result = query_data(sql1, (uname,)) 
            if not result:
                error = "User Doesn't Exist"
            else:
                pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
                sql2 = "UPDATE user_log SET password = %s WHERE username = %s"
                print(pwd_hash)
                data = (pwd_hash, uname)
                insert_or_update_data(sql2, data)
                return "Change Password successfully!"
        else:
            error = 'Invalid username/'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('modify.html', error=error)



def valid_login(username, password):
    sql = "SELECT password FROM user_log WHERE username = %s"
    result = query_data(sql, (username,))
    if result and bcrypt.check_password_hash(result[0]["password"], password):
        return True
    else:
        return False

def log_the_user_in(username):
    return f"Hello, {username}"


