from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from ..models import User
from flask_app.extensions import bcrypt


from ..forms import RegistrationForm, LoginForm

users = Blueprint("users", __name__)

""" ************ User Management views ************ """
@users.route("/")
def index():
    return render_template("index.html")


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return render_template('isauth.html')


    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('users.index'))
        
    return render_template('register.html', form=form, title="NaviNews | Register")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template('account.html')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()  
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return render_template('account.html')
        else:
            flash("Login unsuccessful. Authenticate again.", "danger")

    return render_template('login.html', form=form, title="NaviNews | Login")



@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    greeting = f"Hello, {current_user.username}!"

    return render_template(
        'account.html', title="NaviNews | Settings",
        greeting=greeting
    )