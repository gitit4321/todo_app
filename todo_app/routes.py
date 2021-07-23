from flask import render_template, url_for, flash, redirect
from todo_app import app
from todo_app.forms import RegistrationForm, LoginForm
from todo_app.models import User, Post


posts = [
    {
        'author': "PDUB",
        'title': "Blog Post 1",
        'content': 'first post content',
        'date_posted': 'July 20, 2021'
    },
    {
        'author': "Speno",
        'title': "Blog Post 2",
        'content': 'second post content',
        'date_posted': 'July 21, 2021'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@todo.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)
