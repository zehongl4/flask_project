#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:23:43 2024

@author: xuan
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from .extensions import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    # Assuming `username` is your primary key (replace if you use an `id` column)
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())

    # Flask-Login requires these methods
    def get_id(self):
        return str(self.username)  # Returns the username as the unique ID
    
class Blog(db.Model):
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(21844), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())



        
