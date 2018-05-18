from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField

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
    rectype = SelectField('Type', choices=['Manumission',
        'Runaway advertisement','Advertisement of Sale',
        'Baptism', 'Runaway capture advertisement',
        'Smallpox inoculation notice', 'Execution notice'])
    date = StringField('Date of publication')
    context = StringField('National context')
    citation = StringField('Citation information')
    zotero = StringField('Zotero ID')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create')