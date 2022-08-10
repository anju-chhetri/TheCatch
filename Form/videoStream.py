from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class VideoStream(FlaskForm):
    link = StringField('',
                           validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "link"})
    submit = SubmitField('Enter')
