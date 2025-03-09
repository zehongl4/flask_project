#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:00:39 2024

@author: xuan
"""

from app.models import User, Blog  # Import your models
from app.extensions import db  # Import db from extensions where it is initialized
from sqlalchemy import func
from flask import current_app

class UserDAO:

    def get_user_uname(self, username):
        """Get a user by their username with case-sensitive comparison."""
        return User.query.filter(func.binary(User.username) == func.binary(username)).first()

    def get_user_email(self, email):
        """Get a user by their username with case-sensitive comparison."""
        return User.query.filter(func.binary(User.email) == func.binary(email)).first() 

    def add_user(self, username, email, password):
        """Add a new user to the database."""
        new_user = User(username=username, email = email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def update_password(self, email, password):
        """Update the password for a specific user."""
        user = self.get_user_email(email)  # Use the case-sensitive get_user method
        if user:
            user.password = password # Hashing the new password
            db.session.commit()
            return True
        return False

    def add_blog(self, username, title, content, is_draft, is_public):
        """Add a new blog post to the database."""
        new_blog = Blog(username=username, title=title, content=content, is_draft = is_draft, is_public = is_public)
        db.session.add(new_blog)
        db.session.commit()

    def get_blogs_by_username(self, username):
        """Get the latest 5 blog posts for a specific user."""
        return Blog.query.filter_by(username=username, is_draft = False).order_by(Blog.created_at.desc()).limit(5).all()

    def get_drafts_by_username(self, username):
        """Get the latest 5 blog posts for a specific user."""
        return Blog.query.filter_by(username=username, is_draft = True).order_by(Blog.created_at.desc()).limit(5).all()


    def get_user_allblogs(self, username):
        """Get all blog posts for a specific user."""
        return Blog.query.filter_by(username=username, is_draft = False).order_by(Blog.created_at.desc())

    def get_user_alldrafts(self, username):
        """Get all blog posts for a specific user."""
        return Blog.query.filter_by(username=username, is_draft = True).order_by(Blog.created_at.desc())

    def get_blog_by_id(self, id):
        """Get a blog post by its ID."""
        return Blog.query.get(id)
    
    def delete_blog_by_id(self, post_id):
        post = Blog.query.filter_by(id = post_id).first()
        db.session.delete(post)
        db.session.commit()
    
    def update_blog_post(self, post_id, title, content, is_draft, is_public):
        post = Blog.query.filter_by(id = post_id).first()
        if post:
            post.title = title
            post.content = content
            post.is_draft = is_draft
            post.is_public = is_public
            current_app.logger.info("object input")
            current_app.logger.info(f"is_draft: {post.is_draft}")
            current_app.logger.info(f"is_public: {post.is_public}")
            try:
                # Commit the changes to the database
                db.session.commit()
                return True  # Return True to indicate success
            except Exception as e:
                # If there is any exception during the commit, rollback the session
                db.session.rollback()
                print(f"An error occurred: {e}")  # Log the error for debugging
                return False  # Return False to indicate failure
        else:
            # Return False if no post is found with the provided `post_id`
            print(f"No post found with ID {post_id}")
            return False
    
    def search(self, content, author):
        query = Blog.query
        if content:
            query = query.filter(Blog.content.ilike(f'%{content}%'))
        if author:
            query = query.filter(Blog.username.ilike(f'%{author}%'))
        query = query.filter_by(is_draft=False, is_public=True)
        posts = query.order_by(Blog.created_at.desc()).all()
        return posts

    def search_blogs_by_title(self, username, search_query):
        # query for blogs where the title contains 'query'
        blogs_with_query = Blog.query.filter(Blog.title.like(f'%{search_query}%')).all()
        return blogs_with_query

    def close(self):
        """Not needed in Flask-SQLAlchemy because db.session is automatically handled."""
        pass

 