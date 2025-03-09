#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:25:01 2024

@author: xuan
"""
import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, jsonify
from ..extensions import bcrypt
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, EmailForm, VerifyUserForm
from ..dao import UserDAO  # Import your DAO class
from flask_login import login_user, current_user, logout_user
from .utils import send_verification_email
from datetime import datetime, timedelta
import random

auth = Blueprint('auth', __name__)
user_dao = UserDAO()  # Instantiate the DAO object

#error function
def error_response(message, status_code):
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'status': 'error', 'message': message}), status_code
    flash(message, 'error')
    return None

#success function
def success_response(message, data=None):
    if request.headers.get('Accept') == 'application/json':
        response = {'status': 'success', 'message': message}
        if data:
            response['data'] = data
        return jsonify(response)
    flash(message, 'success')
    return None

#sessions
@auth.route('/sessions', methods=['GET'])
def session_form():
    """load session form"""
    if current_user.is_authenticated:
        return redirect(url_for('blog.user_profile', username=current_user.username))
    form = LoginForm()
    return render_template('login.html', form=form)

@auth.route('/sessions', methods=['POST'])
def create_session():
    """create session"""
    try:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data
            user = user_dao.get_user_email(email)
            if not user:
                response = error_response('Email not found', 404)
                if response:
                    return response
                else:
                    return render_template('login.html', form=form)
            if not bcrypt.check_password_hash(user.password, pwd):
                response = error_response('Invalid email/password', 401)
                if response:
                    return response
                return render_template('login.html', form=form)                
            
            login_user(user, remember=True)
            session['email'] = user.email  # Set username in session

            next_page = request.form.get('next')
            current_app.logger.info(f"saved page: {next_page}") 

            response = success_response('Login successful')
            if response:
                return response
            
            if next_page:
                return redirect(next_page)
            return redirect(url_for('blog.user_profile', username=user.username))
            
        return render_template('login.html', form=form)
    except Exception as e:
        trace = traceback.format_exc()
        current_app.logger.error(f'Login error: {str(e)}\n{trace}')
        # Optionally, return a custom error message
        return 'An error occurred during login', 500  

@auth.route('/sessions', methods=['DELETE'])
def delete_session():
    # check session
    if session.get('logged_out'):
        return redirect(url_for('auth.session_form'))
    

    logout_user()
    for key in ['email', 'is_verified', 'verification_code', 'code_expiry']:
        if key in session:
            session.pop(key)
    
    # mark logged out
    session['logged_out'] = True
    flash('Logged out successfully', 'success')
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'status': 'success', 'message': 'Logged out successfully'})
    
    return redirect(url_for('auth.session_form'))

@auth.route('/users/new', methods=['GET'])
def registration_form():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@auth.route('/users', methods=['POST'])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        uname = form.username.data
        email = form.email.data
        pwd = form.password.data       
        if user_dao.get_user_uname(uname):
            response = error_response("User already exists. Choose a different username.", 409) 
            if response:
                return response
            return render_template('register.html', form=form)
        if user_dao.get_user_email(email):
            response = error_response("Email already exists. Choose a different email.", 409) 
            if response:
                return response
            return render_template('register.html', form=form)
        pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
        user_dao.add_user(uname, email, pwd_hash)
        response = success_response("User registered successfully!")
        if response:
            return response
        
        return redirect(url_for('auth.session_form'))
    
    return render_template('register.html', form=form)

@auth.route('/password-reset/request', methods=['GET'])
def password_reset_form():
    form = EmailForm()
    return render_template('verify.html', form=form)

@auth.route('/password-reset/verification', methods=['POST'])
def create_verification():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        if not user_dao.get_user_email(email):
            response = error_response('Email not found', 404)
            if response:
                return response
            return render_template('verify.html', form=form)
        
        # generate code
        verification_code = ''.join(random.choices('0123456789', k=6))
        session['code_expiry'] = (datetime.now() + timedelta(minutes=10)).timestamp()

        # send and store in session
        if send_verification_email(email, verification_code):
            session['verification_code'] = verification_code
            session['email'] = email
            response = success_response('Verification code has been sent to your email')
            if response:
                return response
            
            return render_template('verify.html', form=VerifyUserForm())
        else:
            response = error_response('Failed to send verification code', 500)
            if response:
                return response
            return render_template('verify.html', form=form)

    return render_template('verify.html', form=form)

@auth.route('/password-reset/verification/validate', methods=['POST'])
def verify_code():
    form = VerifyUserForm()
    #verify code in session
    if 'code_expiry' in session:
        if datetime.now().timestamp() > session['code_expiry']:
            response = error_response('Verification code has expired', 410)  # Gone
            if response:
                return response
            return render_template('verify.html', form=form)
    
    if form.validate_on_submit():
        if form.email.data != session.get('email'):
            response = error_response('Email does not match', 400)
            if response:
                return response
            return render_template('verify.html', form=form)
        
        if form.verification_code.data == session.get('verification_code'):
            # success
            session['is_verified'] = True
            
            response = success_response('Verification successful!')
            if response:
                return response
            
            return redirect(url_for('auth.update_password'))
        else:
            response = error_response('Invalid verification code. Try again!', 400)
            if response:
                return response
            return render_template('verify.html', form=form)
    
    return render_template('verify.html', form=form)

@auth.route('/password-reset/password', methods=['GET'])
def password_form():
    if not session.get('is_verified'):
        response = error_response('Please verify your email first', 403)
        if response:
            return response
        return redirect(url_for('auth.password_reset_form'))
    
    form = ChangePasswordForm()
    return render_template('modify.html', form=form)

@auth.route('/password-reset/password', methods=['POST'])
def update_password():
    form = ChangePasswordForm()
    if not session.get('is_verified'):
        response = error_response('Please verify your email first', 403)
        if response:
            return response
        return redirect(url_for('auth.password_reset_form'))
    
    # gain email
    email = session.get('email')
    if not email:
        response = error_response('Email not found', 400)
        if response:
            return response
        return redirect(url_for('auth.password_reset_form'))
    
    # reset password
    if form.validate_on_submit():
        new_pwd = form.new_password.data
        pwd_hash = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
        
        if not user_dao.update_password(email, pwd_hash):
            response = error_response("User doesn't exist", 404)
            if response:
                return response
            return render_template('modify.html', form=form)
        
        for key in ['is_verified', 'verification_code', 'email', 'code_expiry']:
            if key in session:
                session.pop(key)
        
        response = success_response("Password changed successfully!")
        if response:
            return response
        
        return redirect(url_for('auth.session_form'))
    
    return render_template('modify.html', form=form)












