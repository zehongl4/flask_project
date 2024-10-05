#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:25:01 2024

@author: xuan
"""
import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from ..extensions import bcrypt
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from ..dao import UserDAO  # Import your DAO class
from flask_login import login_user, current_user, logout_user

auth = Blueprint('auth', __name__)
user_dao = UserDAO()  # Instantiate the DAO object

@auth.route('/login', methods=['POST', 'GET'])
def login():
    try:
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            uname = form.username.data
            pwd = form.password.data
            user = user_dao.get_user(uname)
            if user:
                if bcrypt.check_password_hash(user.password, pwd):
                    #logout_user()
                    login_user(user, remember=True)
                    print(user.username)
                    session['username'] = user.username  # Set username in session
                    print("Logged in:", session['username'])  # Debugging output
                    posts = user_dao.get_blogs_by_username(uname)
                    return render_template('account.html', username=uname, form=form, posts=posts)
                else:
                    flash('Invalid username/password', 'error')
            else:
                flash('Username not found', 'error')
            
        return render_template('login.html', form=form)
    except Exception as e:
        trace = traceback.format_exc()
        current_app.logger.error(f'Login error: {str(e)}\n{trace}')
        # Optionally, return a custom error message
        return 'An error occurred during login', 500  

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        uname = form.username.data
        pwd = form.password.data
        if user_dao.get_user(uname):
            flash("User already exists. Choose a different username.", 'error')
        else:       
            pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
            user_dao.add_user(uname, pwd_hash)
            flash("User registered successfully!", 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/new_password', methods=['POST', 'GET'])
def new_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        uname = form.username.data
        new_pwd = form.new_password.data
        pwd_hash = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
        if not user_dao.update_password(uname, pwd_hash):
            flash("User doesn't exist", 'error')
        else:
            flash("Password changed successfully!", 'success')
            return redirect(url_for('auth.login'))
    return render_template('modify.html', form=form)

@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))









