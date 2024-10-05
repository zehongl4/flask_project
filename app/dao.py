#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:00:39 2024

@author: xuan
"""

from app.models import User, Blog  # Import your models
from app.extensions import db  # Import db from extensions where it is initialized
from sqlalchemy import func

class UserDAO:

    def get_user(self, username):
        """Get a user by their username with case-sensitive comparison."""
        return User.query.filter(func.binary(User.username) == func.binary(username)).first()

    def add_user(self, username, password):
        """Add a new user to the database."""
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    def update_password(self, username, password):
        """Update the password for a specific user."""
        user = self.get_user(username)  # Use the case-sensitive get_user method
        if user:
            user.password = password # Hashing the new password
            db.session.commit()
            return True
        return False

    def add_blog(self, username, title, content):
        """Add a new blog post to the database."""
        new_blog = Blog(username=username, title=title, content=content)
        db.session.add(new_blog)
        db.session.commit()

    def get_blogs_by_username(self, username):
        """Get the latest 5 blog posts for a specific user."""
        return Blog.query.filter_by(username=username).order_by(Blog.created_at.desc()).limit(5).all()

    def get_blog_by_id(self, id):
        """Get a blog post by its ID."""
        return Blog.query.get(id)

    def get_user_allblogs(self, username):
        """Get all blog posts for a specific user."""
        return Blog.query.filter_by(username=username).order_by(Blog.created_at.desc()).all()
    
    def delete_blog_by_id(self, post_id):
        post = Blog.query.filter_by(id = post_id).first()
        db.session.delete(post)
        db.session.commit()
    
    def update_blog_post(self, post_id, title, content):
        post = Blog.query.filter_by(id = post_id).first()
        if post:
            post.title = title
            post.content = content
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
    def search_blogs_by_title(self, username, search_query):
        # query for blogs where the title contains 'query'
        blogs_with_query = Blog.query.filter(Blog.title.like(f'%{search_query}%')).all()
        return blogs_with_query

    def close(self):
        """Not needed in Flask-SQLAlchemy because db.session is automatically handled."""
        pass

    # def __query_data(self, sql, params=None):
    #     conn = self.conn_mysql()
    #     try:
    #         with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #             cursor.execute(sql, params)
    #             return cursor.fetchall()
    #     except pymysql.Error as error:
    #         print(f"Database error: {error}")
    #         return None
    #     finally:
    #         conn.close()

    # def __insert_or_update_data(self, sql, params=None):
    #     conn = self.conn_mysql()
    #     try:
    #         with conn.cursor() as cursor:
    #             cursor.execute(sql, params)
    #             conn.commit()
    #     except pymysql.Error as error:
    #         print(f"Database error: {error}")
    #         conn.rollback()
    #     finally:
    #         conn.close()
        

    # def get_user_password(self, username):
    #     print(self.__query_data("SELECT password FROM users WHERE username = %s", (username,)))
    #     return self.__query_data("SELECT password FROM users WHERE username = %s", (username,))

    # def check_user_exist(self, username):
    #     result = self.__query_data("SELECT password FROM users WHERE username = %s", (username,))
    #     print(result)
    #     return result != ()  # Check if the result is not empty

    # def add_user(self, username, password):
    #     self.__insert_or_update_data("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

    # def update_password(self, username, password):
    #     self.__insert_or_update_data("UPDATE users SET password = %s WHERE username = %s", (password, username))
    
    # def add_blog(self, username, title, content):
    #     print("yyy")
    #     self.__insert_or_update_data("INSERT INTO blogs (username, title, content) VALUES (%s, %s, %s)", (username, title, content))
    
    # def get_blogs_by_username(self, username):
    #     return self.__query_data("SELECT id, username, title, created_at FROM blogs WHERE username = %s ORDER BY created_at DESC Limit 5", (username,))
    
    # def get_blog_by_id(self, id):
    #     return self.__query_data("SELECT title, content, created_at FROM blogs WHERE id = %s", (id,))       
    # def get_user_allblogs(self, username):
    #     return self.__query_data("SELECT id, username, title, created_at FROM blogs WHERE username = %s ORDER BY created_at DESC", (username,))
