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
        ('Smallpox inoculation notice','Smallpox inoculation notice'), ('Execution notice','Execution notice')])
    citation = StringField('Citation information')
    date = DateField('Date of publication')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create')

class EntrantForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    # roles = FieldList(SelectField('Role', choices=[('seller', 'Seller'),
    #     ('owner','Owner'), ('enslaved', 'Enslaved'), ('baptised', 'Baptised'),
    #     ('inoculated', 'Inoculated'), ('escaped', 'Escaped'),
    #     ('liberated', 'Liberated'), ('captured', 'Captured'),
    #     ('captor','Captor')]), min_entries=2)
    roles = FieldList(SelectField('Role', choices=[]), min_entries=2)
    submit = SubmitField('Add')