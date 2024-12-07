from flask import Flask, render_template
import os
from navi.config import Config
from .client import NaviNewsClient

from .extensions import db, login_manager, bcrypt
movie_client = NaviNewsClient(os.getenv('NEWS_API_KEY'))

from .users.routes import users
from .articles.routes import articles

def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(articles)

    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"

    return app