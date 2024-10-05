#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:20:15 2024

@author: xuan
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .forms import BlogPostForm
from ..dao import UserDAO 
from flask_login import login_required, current_user
from flask import abort
from .forms import BlogPostForm

blog = Blueprint('blog', __name__)
user_dao = UserDAO()


@blog.route('/<username>', methods=['POST', 'GET'])
@login_required
def user_profile(username):
    # log in user page
    form = BlogPostForm()
    if current_user.username != username:
        abort(403)  # Forbidden access

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
@login_required
def post_detail(username, post_id):
    # Fetch the blog post by title
    post = user_dao.get_blog_by_id(post_id)
    if post:
        return render_template('post_detail.html', post=post, username=username)
    else:
        flash('Post not found.', 'error')
        return redirect(url_for('blog.user_profile', username=username))

@blog.route('/<username>/allpost', methods = ['GET'])
@login_required
def all_posts(username):
    search_query = request.args.get('search', '')
    print(search_query)
    if search_query:
        posts = user_dao.search_blogs_by_title(username, search_query)
    else:
        posts = user_dao.get_blogs_by_username(username)
        print(posts[0].id)
    form = BlogPostForm()
    return render_template('all_posts.html', username=username, form = form, posts=posts)

@blog.route('/<username>/<post_id>/delete_post', methods = ['POST'])
@login_required
def delete_post(username, post_id):
    user_dao.delete_blog_by_id(post_id)
    flash('Post has been deleted successfully!', 'success')
    return redirect(url_for('blog.user_profile', username=username))

@blog.route('/<username>/<post_id>/update_post', methods = ['POST'])
@login_required
def update_post(username, post_id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    success = user_dao.update_blog_post(post_id, title, content)
    if success:
        flash('Post has been modified successfully!', 'success')
        return jsonify({'status': 'success', 'redirect_url': url_for('blog.user_profile', username=username)})
    else:
        flash('Modification failed!', 'fail')
        return jsonify({'status': 'fail', 'message': 'Modification failed!'}), 400