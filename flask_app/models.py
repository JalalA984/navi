

from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    preferred_categories = db.ListField(db.StringField())  # Store list of preferred news categories

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class SavedArticle(db.Document):
    user = db.ReferenceField(User, required=True)
    title = db.StringField(required=True)
    description = db.StringField()
    url = db.StringField(required=True)
    source = db.StringField()
    published_at = db.DateTimeField()

