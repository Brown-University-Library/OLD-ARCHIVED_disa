from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms import HiddenField, SelectField, DateField
from wtforms import FieldList, IntegerField

class DocumentForm(FlaskForm):
    # From MongoDB document.sourceType field
    document_type = SelectField('Document Type')
    citation = TextAreaField('Citation')
#   context = StringField('National context')
    day = IntegerField('Day')
    month = SelectField('Month')
    century = SelectField()
    decade = SelectField()
    year = SelectField()
    zotero_id = StringField('Zotero ID')
    acknowledgements = TextAreaField('Acknowledgements')
    submit = SubmitField('Save')

class RecordForm(FlaskForm):
    # From MongoDB document.recordType field
    record_type = SelectField('Type')
    day = IntegerField('Day')
    month = SelectField('Month')
    century = SelectField()
    decade = SelectField()
    year = SelectField()
    citation = StringField('Citation information')
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