from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.uploads import UploadSet, IMAGES



class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PhotoForm(Form):
    photo = FileField('image', validators=[ FileRequired(), FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'])])
    description = StringField('describe your photo')
    submit = SubmitField('Submit')

