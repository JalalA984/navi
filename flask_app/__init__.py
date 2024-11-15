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




# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object("config")

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')