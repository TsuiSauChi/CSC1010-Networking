from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [
        DataRequired(),
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')