from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Post
from app import db
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
@main.route('/index')
@login_required
def index():
    posts = current_user.followed_posts().all()
    return render_template('index.html', posts=posts)

@main.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@main.route('/post', methods=['POST'])
@login_required
def post():
    body = request.form.get('body')
    if body:
        post = Post(body=body, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
    return redirect(url_for('main.index'))

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@main.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('main.user', username=current_user.username))
    
    file = request.files['avatar']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('main.user', username=current_user.username))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"avatar_{current_user.id}_{file.filename}")
        avatar_path = os.path.join('app', 'static', 'avatars', filename)
        file.save(avatar_path)
        
        # Update user's avatar path in database
        current_user.avatar_path = url_for('static', filename=f'avatars/{filename}')
        db.session.commit()
        flash('Avatar updated successfully!')
    else:
        flash('Invalid file type. Please upload a PNG, JPG, JPEG, or GIF file.')
    
    return redirect(url_for('main.user', username=current_user.username))

@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}!')
    return redirect(url_for('main.user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}.')
    return redirect(url_for('main.user', username=username))
