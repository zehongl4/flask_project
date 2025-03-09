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
    

    username = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())

    blogs = db.relationship("Blog", back_populates="author", lazy="dynamic")
    comments = db.relationship("Comment", back_populates="author", lazy="dynamic")
    likes = db.relationship("Like", back_populates="user", lazy="dynamic")
    favorites = db.relationship("Favorite", back_populates="user", lazy="dynamic")

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
    is_draft = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)

    author = db.relationship("User", back_populates="blogs")
    comments = db.relationship("Comment", back_populates="blog", cascade="all, delete-orphan", lazy="dynamic")
    likes = db.relationship("Like", back_populates="blog", cascade="all, delete-orphan", lazy="dynamic")
    favorites = db.relationship("Favorite", back_populates="blog", cascade="all, delete-orphan", lazy="dynamic")

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    
    author = db.relationship("User", back_populates="comments")
    blog = db.relationship("Blog", back_populates="comments")
    
    def __repr__(self):
        return f'<Comment {self.id}>'  

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    
    user = db.relationship("User", back_populates="likes")
    blog = db.relationship("Blog", back_populates="likes")
    
    __table_args__ = (
        db.UniqueConstraint('username', 'blog_id', name='uix_user_blog_like'),
    )
    
    def __repr__(self):
        return f'<Like {self.id}>'
    
    @classmethod
    def get_user_likes(cls, username):
        return Blog.query.join(cls).filter(cls.username == username)
 


class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    
    # define relationship
    user = db.relationship("User", back_populates="favorites")
    blog = db.relationship("Blog", back_populates="favorites")
    
    # ensure a user can only fav a post once
    __table_args__ = (
        db.UniqueConstraint('username', 'blog_id', name='uix_user_blog_favorite'),
    )
    
    def __repr__(self):
        return f'<Favorite {self.id}>'
    
    
    @classmethod
    def get_user_favorites(cls, username):
        return Blog.query.join(cls).filter(cls.username == username)



        
