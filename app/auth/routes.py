#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:25:01 2024

@author: xuan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import app, bcrypt, query_data, insert_or_update_data
from .forms import LoginForm, RegistrationForm, ChangePasswordForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        uname = form.username.data
        pwd = form.password.data

        if valid_login(uname, pwd):
            return log_the_user_in(uname)
        else:
            print("yyy")
            flash('Invalid username/password', 'error')
    else:
        # Print out form errors for debugging
        print("Form validation failed:")
        print(form.errors)
    
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    print("Request method:", request.method)  # Debugging print
    print("Form validation result:", form.validate_on_submit())  # Debugging print
    print("Form errors:", form.errors)  # Debugging print

    if request.method == 'POST' and form.validate_on_submit():
        uname = form.username.data
        pwd = form.password.data

        if query_data("SELECT password FROM user_log WHERE username = %s", (uname,)):
            flash("User already exists. Choose a different username.", 'error')
        else:
            pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
            insert_or_update_data("INSERT INTO user_log (username, password) VALUES (%s, %s)", (uname, pwd_hash))
            flash("User registered successfully!", 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth.route('/new_password', methods=['POST', 'GET'])
def new_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        uname = form.username.data
        new_pwd = form.new_password.data

        if not query_data("SELECT password FROM user_log WHERE username = %s", (uname,)):
            flash("User doesn't exist", 'error')
        else:
            pwd_hash = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
            insert_or_update_data("UPDATE user_log SET password = %s WHERE username = %s", (pwd_hash, uname))
            flash("Password changed successfully!", 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('modify.html', form=form)

def valid_login(username, password):
    result = query_data("SELECT password FROM user_log WHERE username = %s", (username,))
    
    if result:
        try:
            # Attempt to check the password using bcrypt
            if bcrypt.check_password_hash(result[0]["password"], password):
                return True
            else:
                flash('Incorrect password', 'error')
        except ValueError as e:
            # Catch the specific invalid salt error and log it
            print(f"Error checking password for user {username}: {e}")
            flash('Password validation error, please reset your password.', 'error')
            return False
    else:
        flash('Username not found', 'error')
    
    return False

def log_the_user_in(username):
    # This is a placeholder function; implement actual login logic here
    return f"Hello, {username}"







