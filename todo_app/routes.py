import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from todo_app import app, db, bcrypt, mail
from todo_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from todo_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        user_id = current_user.id
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        todos = Post.query.filter_by(user_id=user_id).filter_by(complete=False).order_by(Post.date_posted.desc()).all()
        completed = Post.query.filter_by(user_id=user_id).filter_by(complete=True).order_by(Post.date_posted.desc()).all()
        return render_template('home.html', todos=todos, completed=completed, image_file=image_file)
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Verify that you entered the correct email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been successfully updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post", methods=['POST'])
@login_required
def post():
    title = request.form.get("title")
    post = Post(title=title, complete=False, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    ## flash message... to use or not to use? ##
    # flash('You added a new To Do item!', 'success')
    return redirect(url_for('home'))


@app.route("/complete/<string:post_id>")
@login_required
def complete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.complete = not post.complete
    db.session.commit()

    ## flash message... to use or not to use? ##
    # if post.complete == True:
    #     flash('Great work! You completed one of the items on your To Do list!', 'success')
    # else:
    #     flash('We all get a bit ahead of ourselves sometimes...', 'light')
    return redirect(url_for('home'))


@app.route("/delete/<string:post_id>")
@login_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='noreply@demo.com', 
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made to your account.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent to {user.email} with instructions to reset you password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)