from flask_wtf import Form
from wtforms import StringField
from wtforms import SubmitField


class LoginForm(Form):
    name = StringField("name")
    submit = SubmitField("Submit")
