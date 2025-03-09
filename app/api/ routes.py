from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from ..models import Blog, Comment, Like, Favorite
from app.extensions import db

api = Blueprint('api', __name__, url_prefix='/api')

# API like functionality
@api.route('/blogs/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    # Check if blog exists
    post = Blog.query.get_or_404(post_id)

    # Look for existing like
    existing_like = Like.query.filter_by(username=current_user.username, blog_id=post.id).first()
    
    if existing_like:
        # Remove like if it exists
        db.session.delete(existing_like)
        action = 'unliked'
        is_liked = False
    else:
        # Add new like
        new_like = Like(username=current_user.username, blog_id=post.id)
        db.session.add(new_like)
        action = 'liked'
        is_liked = True
    
    db.session.commit()
    like_count = Like.query.filter_by(blog_id=post.id).count()
    
    return jsonify({
        'status': 'success',
        'post_id': post_id,
        'action': action,
        'is_liked': is_liked,
        'like_count': like_count
    }), 200

# API like functionality
@api.route('/blogs/<int:post_id>/favorite', methods=['POST'])
@login_required
def toggle_bookmark(post_id):
    post = Blog.query.get_or_404(post_id)

    existing_bookmark = Favorite.query.filter_by(username=current_user.username, blog_id=post.id).first()
    
    if existing_bookmark:
        # Remove bookmark if it exists
        db.session.delete(existing_bookmark)
        action = 'unfavorited'
        is_bookmarked = False
    else:
        # Add new bookmark
        new_bookmark = Favorite(username=current_user.username, blog_id=post.id)
        db.session.add(new_bookmark)
        action = 'favorited'
        is_bookmarked = True
    
    db.session.commit()
    
    
    return jsonify({
        'status': 'success',
        'post_id': post_id,
        'action': action,
        'is_bookmarked': is_bookmarked
    }), 200

#add comment
@api.route('/blogs/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    post = Blog.query.get_or_404(post_id)
    
    content = None
    if request.is_json:
        content = request.json.get('content')
    else:
        content = request.form.get('content')
    
    if not content:
        return jsonify({
            'status': 'error',
            'message': 'Content cannot be blank'
        }), 400
    
    comment = Comment(
        content=content,
        username=current_user.username,
        blog_id=post.id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'username': comment.username,
            'post_id': comment.blog_id,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
        }
    }), 201

# delete comments
@api.route('/blogs/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(post_id, comment_id):
    post = Blog.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    

    # Verify comment belongs to this blog
    if comment.blog_id != post_id:
        return jsonify({'status': 'error', 'message': 'Comment does not belong to this blog'}), 400
    
    # Check permissions (comment author or blog author can delete)
    if comment.username != current_user.username and post.username != current_user.username:
        return jsonify({'status': 'error', 'message': 'Unauthorized to delete this comment'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Comment deleted successfully',
        'comment_id': comment_id,
        'comment_count': Comment.query.filter_by(blog_id=post_id).count()  
    }), 200