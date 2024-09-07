#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:16:31 2024

@author: xuan
"""

from flask import Flask
from flask_bcrypt import Bcrypt
import pymysql

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-random-secret-key'


# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Database connection function
def conn_mysql():
    return pymysql.connect(
        host="127.0.0.1", 
        port=3306, 
        user="root", 
        password="lanzehong0997", 
        database="flask_db", 
        charset="utf8"
    )


print("kjkjk")
# Register blueprints
def create_app():
    print("Creating app...")
    
    from app.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # Import blueprints at the end to avoid circular imports
    
    # from app.routes import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    
    # from app.blog.routes import blog as blog_blueprint
    # app.register_blueprint(blog_blueprint, url_prefix='/blog')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)




