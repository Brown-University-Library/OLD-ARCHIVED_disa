from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import FieldList

class DocumentForm(FlaskForm):
    # From MongoDB document.sourceType field
    doctype = SelectField('Type')
    citation = StringField('Citation information')
    date = DateField('Date of publication')
    context = StringField('National context')
    zotero = StringField('Zotero ID')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create')

class RecordForm(FlaskForm):
    # From MongoDB document.recordType field
    rectype = SelectField('Type')
    citation = StringField('Citation information')
    date = DateField('Date of publication')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create')

class EnslavedForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    age = StringField('Age')
    sex = StringField('Sex')
    race = StringField('Race')
    tribe = StringField('Tribe')
    origin = StringField('Origin')
    status = StringField('Status')
    vocation = StringField('Vocation')
    submit = SubmitField('Add')

class OwnerForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    title = StringField('Title')
    vocation = StringField('Vocation')
    submit = SubmitField('Add')