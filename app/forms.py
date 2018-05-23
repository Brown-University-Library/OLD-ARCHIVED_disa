from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import FieldList

class DocumentForm(FlaskForm):
    # From MongoDB document.sourceType field
    doctype = SelectField('Type', choices=[('news','Newspaper'),
        ('ltr','Letter'),('rgst','Registry'),('invt','Inventory'),
        ('cen','Census'),('court','Court Document'),
        ('prob','Probate Account'),('will','Will')])
    citation = StringField('Citation information')
    date = DateField('Date of publication')
    context = StringField('National context')
    zotero = StringField('Zotero ID')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create')

class RecordForm(FlaskForm):
    # From MongoDB document.recordType field
    rectype = SelectField('Type', choices=[('Manumission','Manumission'),
        ('Runaway advertisement','Runaway advertisement'),('Advertisement of Sale','Advertisement of Sale'),
        ('Baptism','Baptism'), ('Runaway capture advertisement','Runaway capture advertisement'),
        ('Smallpox inoculation notice','Smallpox inoculation notice'), ('Execution notice','Execution notice'),
        ('Probate', 'Probate')])
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