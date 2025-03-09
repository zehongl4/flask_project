#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:20:15 2024

@author: xuan
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .forms import BlogPostForm, SearchForm
from ..dao import UserDAO 
from flask_login import login_required, current_user
from flask import current_app
from ..models import User, Blog, Comment, Like, Favorite
from app.extensions import db
from . import blog
user_dao = UserDAO()

# Search resource
@blog.route('/search', methods=['GET'])
def search():
    """Display search form and results"""
    current_app.logger.info("Entering search function")
    
    form = SearchForm()
    search_query = request.args.get('content', '')
    author = request.args.get('author', '')
    
    if search_query or author:
        current_app.logger.info(f"content: {search_query}")
        current_app.logger.info(f"author: {author}")
        
        posts = user_dao.search(search_query, author)
        return render_template('search.html', form=form, posts=posts)
    
    current_app.logger.info("Rendering default search page")
    return render_template('search.html', form=form)

# User resource
@blog.route('/users/<username>', methods=['GET'])
@login_required
def user_profile(username):
    """Display user profile page"""
    if current_user.username != username:
        abort(403)  # Forbidden access

    posts = user_dao.get_blogs_by_username(username)
    drafts = user_dao.get_drafts_by_username(username)
    form = BlogPostForm()

    return render_template('account.html', username=username, form=form, posts=posts, drafts=drafts)

# Post creation
@blog.route('/users/<username>/posts', methods=['POST'])
@login_required
def create_post(username):
    """Create a new blog post"""
    if current_user.username != username:
        abort(403)
        
    form = BlogPostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_draft = request.form.get('is_draft') == 'on'
        is_public = not is_draft if is_draft else request.form.get('is_public') == 'on'
        
        user_dao.add_blog(username, title, content, is_draft=is_draft, is_public=is_public)
        
        if is_draft:
            flash('Draft saved successfully!', 'success')
        else:
            flash('Post published successfully!', 'success')
    
    return redirect(url_for('blog.user_profile', username=username))

# Post detail
@blog.route('/posts/<int:post_id>', methods=['GET'])
def view_post(post_id):
    """Display a single blog post"""
    post = user_dao.get_blog_by_id(id=post_id)

    if not post:
        abort(404)
    
    # Check access permissions
    if post.is_draft and (not current_user.is_authenticated or current_user.username != post.username):
        abort(404)
    if not post.is_public and (not current_user.is_authenticated or current_user.username != post.username):
        abort(404)
    
    # Get comments
    comments = Comment.query.filter_by(blog_id=post.id).order_by(Comment.created_at.desc()).all()
    
    # Get user like and bookmark status
    user_liked = False
    user_bookmarked = False
    if current_user.is_authenticated:
        user_liked = current_user.likes.filter_by(id=post.id).count() > 0
        user_bookmarked = current_user.favorites.filter_by(id=post.id).count() > 0
    
    like_count = post.likes.count()
    
    return render_template(
        'post_detail.html', 
        post=post, 
        comments=comments, 
        user_liked=user_liked,
        user_bookmarked=user_bookmarked,
        like_count=like_count
    )

# Post listing
@blog.route('/users/<username>/posts', methods=['GET'])
@login_required
def list_posts(username):
    """List all posts by a user"""
    if current_user.username != username:
        abort(403)
        
    form = BlogPostForm()
    search_query = request.args.get('search', '')
    if search_query:
        posts = user_dao.search_blogs_by_title(username, search_query).all()
    else:
        posts = user_dao.get_user_allblogs(username).all()
        
    return render_template('all_posts.html', username=username, form=form, posts=posts)

# Draft listing
@blog.route('/users/<username>/drafts', methods=['GET'])
@login_required
def list_drafts(username):
    """List all drafts by a user"""
    if current_user.username != username:
        abort(403)
        
    form = BlogPostForm()
    search_query = request.args.get('search', '')
    query = user_dao.get_user_alldrafts(username)
    if search_query:
        posts = query.filter(Blog.title.like(f'%{search_query}%'))
    else:
        posts = query.all()
        
    return render_template('all_posts.html', username=username, form=form, posts=posts)

# Favorites listing
@blog.route('/users/<username>/favorites', methods=['GET'])
@login_required
def list_favorites(username):
    """List all favorites by a user"""
    if current_user.username != username:
        abort(403)
        
    form = BlogPostForm()
    search_query = request.args.get('search', '')
    query = Favorite.get_user_favorites(username=username)
    
    if search_query:
        query = query.filter(Blog.title.like(f'%{search_query}%'))
    # order
    query = query.order_by(Blog.created_at.desc())
    # page
    page = request.args.get('page', 1, type=int)
    posts = query.paginate(page=page, per_page=10, error_out=False).items
        
    return render_template('all_posts.html', username=username, form=form, posts=posts)

# Liked posts listing
@blog.route('/users/<username>/likes', methods=['GET'])
@login_required
def list_liked_posts(username):
    """List all posts liked by a user"""
    if current_user.username != username:
        abort(403)
        
    form = BlogPostForm()
    search_query = request.args.get('search', '')
    query = Like.get_user_likes(username)
    
    if search_query:
        query = query.filter(Blog.title.like(f'%{search_query}%'))
    # order
    query = query.order_by(Blog.created_at.desc())
    # page
    page = request.args.get('page', 1, type=int)
    posts = query.paginate(page=page, per_page=10, error_out=False).items

    return render_template('all_posts.html', username=username, form=form, posts=posts)

# Post deletion
@blog.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post"""
    post = user_dao.get_blog_by_id(id=post_id)
    
    if not post or post.username != current_user.username:
        abort(403)
        
    user_dao.delete_blog_by_id(post_id)
    flash('Post has been deleted successfully!', 'success')
    
    return redirect(url_for('blog.user_profile', username=current_user.username))

# Post edit form
@blog.route('/posts/<int:post_id>/edit', methods=['GET'])
@login_required
def edit_post(post_id):
    """Display edit form for a blog post"""
    post = user_dao.get_blog_by_id(id=post_id)
    if not post:
        abort(404)
    
    if current_user.username != post.username:
        abort(403)
    
    return render_template('update.html', post=post)

# Post update
@blog.route('/posts/<int:post_id>', methods=['POST'])
@login_required
def update_post(post_id):
    """Update a blog post"""
    post = user_dao.get_blog_by_id(id=post_id)
    if not post or post.username != current_user.username:
        abort(403)
        
    title = request.form.get('title')
    content = request.form.get('content')
    is_draft = request.form.get('is_draft') == 'on'
    is_public = not is_draft if is_draft else request.form.get('is_public') == 'on'
    
    current_app.logger.info(f"is_draft: {is_draft}")
    current_app.logger.info(f"is_public: {is_public}")
    
    success = user_dao.update_blog_post(post_id, title, content, is_draft, is_public)
    
    if success:
        flash('Post has been modified successfully!', 'success')
    else:
        flash('Modification failed!', 'fail')
        
    return redirect(url_for('blog.view_post', post_id=post_id))

