from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class DocumentForm(FlaskForm):
    name = StringField('Display name')
    date = StringField('Date of publication')
    context = StringField('National context')
    citation = StringField('Citation information')
    zotero = StringField('Zotero ID')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create')