from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms import HiddenField, SelectField, DateField
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

class EntrantForm(FlaskForm):
    record = HiddenField('Record')
    role = SelectField('Type')
    first_name = StringField('First name')
    last_name = StringField('Last name')
    age = StringField('Age')
    sex = StringField('Sex')
    title = StringField('Title')
    race = StringField('Race')
    tribe = StringField('Tribe')
    origin = StringField('Origin')
    status = StringField('Status')
    vocation = StringField('Vocation')
    submit = SubmitField('Add')

class EntrantRelationshipForm(FlaskForm):
    entrant = HiddenField('Entrant')
    other = SelectField('Person')
    related_as = SelectField('Relationship')
    submit = SubmitField('Add')