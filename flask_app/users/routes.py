from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user

from ..models import User
from flask_app.extensions import bcrypt


from ..forms import RegistrationForm

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
