#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:20:15 2024

@author: xuan
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import BlogPostForm
from ..dao import UserDAO 

blog = Blueprint('blog', __name__)
user_dao = UserDAO()

@blog.route('/<username>', methods=['POST', 'GET'])
def user_profile(username):
    form = BlogPostForm()

    # If the form is submitted via POST and is valid
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # Add the new blog post to the database
        user_dao.add_blog(username, title, content)
        flash('New Blog Added Successfully', 'success')  # Flash a success message
    
    # After adding a blog, or on page load, fetch the user's blog posts
    posts = user_dao.get_blogs_by_username(username)

    # Return the updated template with the list of posts
    return render_template('account.html', username=username, form=form, posts=posts)



@blog.route('/<username>/post/<int:post_id>', methods=['GET'])
def post_detail(username, post_id):
    # Fetch the blog post by title
    post = user_dao.get_blog_by_id(post_id)
    if post:
        post = post[0]
        return render_template('post_detail.html', post=post, username=username)
    else:
        flash('Post not found.', 'error')
        return redirect(url_for('blog.user_profile', username=username))

@blog.route('/<username>/allpost', methods = ['GET'])
def all_posts(username):
    posts = user_dao.get_user_allblogs(username)
    if posts:
        return render_template('all_posts.html', username=username, posts=posts)