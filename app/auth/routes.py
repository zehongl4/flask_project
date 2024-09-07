#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:25:01 2024

@author: xuan
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import bcrypt
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from .dao import UserDAO  # Import your DAO class

auth = Blueprint('auth', __name__)
user_dao = UserDAO()  # Instantiate the DAO object

@auth.route('/login', methods=['POST', 'GET'])
def login():
    print("aaa")
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        uname = form.username.data
        pwd = form.password.data
        if valid_login(uname, pwd):
            return log_the_user_in(uname)
        else:
            flash('Invalid username/password', 'error')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        uname = form.username.data
        pwd = form.password.data
        if user_dao.user_exists(uname):
            flash("User already exists. Choose a different username.", 'error')
        else:
            pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
            user_dao.insert_user(uname, pwd_hash)
            flash("User registered successfully!", 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/new_password', methods=['POST', 'GET'])
def new_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        uname = form.username.data
        new_pwd = form.new_password.data
        if not user_dao.user_exists(uname):
            flash("User doesn't exist", 'error')
        else:
            pwd_hash = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
            user_dao.update_password(uname, pwd_hash)
            flash("Password changed successfully!", 'success')
            return redirect(url_for('auth.login'))
    return render_template('modify.html', form=form)

def valid_login(username, password):
    result = user_dao.get_user_password(username)
    if result:
        try:
            if bcrypt.check_password_hash(result[0]["password"], password):
                return True
        except ValueError as e:
            print(f"Error checking password for user {username}: {e}")
            flash('Password validation error, please reset your password.', 'error')
    flash('Username not found', 'error')
    return False

def log_the_user_in(username):
    return f"Hello, {username}"  # Implement actual login logic here








