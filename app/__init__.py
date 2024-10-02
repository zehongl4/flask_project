#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:16:31 2024

@author: xuan
"""

from flask import Flask, redirect, url_for, jsonify
from .extensions import db, bcrypt, csrf, login_manager  # Import db from extensions (or wherever it is initialized)
import os
from .models import User


app = Flask(__name__)

# Configure the app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-random-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')

# Initialize extensions
db.init_app(app)  # Ensure this line is present to bind db to the app instance
bcrypt.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Setup user loader for Flask-Login
@login_manager.user_loader
def load_user(username):
    # Load the user from the database by user_id (typically the primary key)
    return User.query.get(username)
    
# Register blueprints
from .auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

from .blog.routes import blog
app.register_blueprint(blog, url_prefix='/blog')

@app.route('/health')
def health_check():
    # Here you can include any logic to check the health of your application,
    # like database connectivity, external APIs status, etc.
    # For simplicity, this just returns a 'success' status.
    try:
        # Simulated database check (example)
        # db.session.execute('SELECT 1')
        return jsonify({"status": "ok", "description": "Service is up and running"}), 200
    except Exception as e:
        return jsonify({"status": "error", "description": str(e)}), 500

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    print(123)
    app.run(host='0.0.0.0', port=8000, debug=True)   # AWS







    




