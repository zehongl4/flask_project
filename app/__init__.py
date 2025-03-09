#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:16:31 2024

@author: xuan
"""

from flask import Flask, redirect, url_for, jsonify, session, current_app
from .extensions import db, bcrypt, csrf, login_manager  # Import db from extensions (or wherever it is initialized)
import os

from dotenv import load_dotenv
from flask_mail import Mail, Message
import logging
from logging.handlers import RotatingFileHandler  # log file
from flask_migrate import Migrate

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("DATABASE_URL:", os.getenv('DATABASE_URL'))
app = Flask(__name__)
migrate = Migrate(app, db)
from .models import User, Blog, Comment, Like, Favorite


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['DEBUG'] = os.getenv('DEBUG') == 'True'  # Ensures the DEBUG is a boolean

app.config['SESSION_COOKIE_NAME'] = 'your_app_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


# Initialize extensions
db.init_app(app)  # Ensure this line is present to bind db to the app instance
migrate = Migrate(app, db)

bcrypt.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.session_form'

if not app.debug:
    file_handler = RotatingFileHandler('./flask-app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask app startup')
mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # using gmail
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'blogsender20@gmail.com'  # email
app.config['MAIL_PASSWORD'] = 'kgym ejvd axls rvpg'     # password
    
mail.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Setup user loader for Flask-Login
@login_manager.user_loader
def load_user(username):
    # Load the user from the database by user_id (typically the primary key)
    return User.query.get(username)
    
# Register blueprints
from .auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

from .blog import blog
app.register_blueprint(blog, url_prefix='/blog')

from .api import api
app.register_blueprint(api, url_prefix='/api')

# Logging function for session debugging
@app.before_request
def before_request_logging():
    if 'username' in session:
        print(f"Current session user_id: {session['username']}")
    else:
        print("No username in session")

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
    return redirect(url_for('auth.session_form'))

if __name__ == '__main__':
    print(123)
    app.run(host='0.0.0.0', port=8000, debug=True)   # AWS







    




