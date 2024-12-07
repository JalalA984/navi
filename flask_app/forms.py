from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User



class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    
    email = StringField("Email", validators=[InputRequired(), Email()])
    
    password = PasswordField("Password", validators=[InputRequired()])
    
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")




class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    search_query = StringField(
    "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class SaveArticleForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = StringField('Description')
    url = StringField('URL', validators=[InputRequired()])
    source = StringField('Source')

    submit = SubmitField('SAVE')
    
    
class PreferCategoryForm(FlaskForm):
    category = StringField("Category", validators=[InputRequired()])
    submit = SubmitField('FAVORITE')