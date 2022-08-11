from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class VideoStream(FlaskForm):
    link = StringField('',
                           validators=[Length(min=2, max=50)], render_kw={"placeholder": "link"})
    submit = SubmitField('Enter')
