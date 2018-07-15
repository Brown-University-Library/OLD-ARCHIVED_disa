from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import TextAreaField
from wtforms import HiddenField, SelectField, DateField,TextAreaField
from wtforms import FieldList, IntegerField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

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
    first_name = StringField('First')
    last_name = StringField('Last')
    age = StringField('Age')
    gender = RadioField('Gender', choices=[
        ('1','Male'),('2','Female'),('3','Other/Unknown')],default='3')
    title = StringField('Title')
    race = StringField('Race')
    tribe = StringField('Tribe')
    origin = StringField('Origin')
    status = SelectField('Status')
    vocation = StringField('Vocation')
    submit = SubmitField('Save')

class EntrantRelationshipForm(FlaskForm):
    entrant = HiddenField('Entrant')
    other = SelectField('Person')
    related_as = SelectField('Relationship')
    submit = SubmitField('Add')