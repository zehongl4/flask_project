#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:16:31 2024

@author: xuan
"""


from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-random-secret-key'
csrf = CSRFProtect(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Import blueprints after initializing extensions
from app.auth.routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# # Additional blueprints can be registered here
# from app.routes import main as main_blueprint
# app.register_blueprint(main_blueprint)
from app.blog.routes import blog as blog_blueprint
app.register_blueprint(blog_blueprint, url_prefix='/blog')

if __name__ == '__main__':
    app.run(port = 8000, debug=True)





