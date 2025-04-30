from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, URL

class UrlForm(FlaskForm):
    url = StringField(label='Url', validators=[DataRequired(), URL()])