from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from .client import NaviNewsClient


from .extensions import db, login_manager, bcrypt
movie_client = NaviNewsClient(os.getenv('NEWS_API_KEY'))

from .users.routes import users

def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("../config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)

    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"

    return app
