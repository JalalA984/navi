from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    # profile_pic = db.StringField()  # Store URL or path to profile picture
    preferred_categories = db.ListField(db.StringField())  # Store list of preferred news categories

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class SavedArticle(db.Document):
    user = db.ReferenceField(User, required=True)
    title = db.StringField(required=True, max_length=200)
    description = db.StringField(max_length=500)
    url = db.URLField(required=True)
    source = db.StringField(required=True, max_length=100)
    published_at = db.DateTimeField(required=True)
    content = db.StringField()
    url_to_image = db.URLField()
    saved_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': [
            'user',
            'saved_at'
        ]
    }
