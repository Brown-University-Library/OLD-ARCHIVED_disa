from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

import os
import json
import datetime

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

import click

@app.cli.command()
@click.option('--full', '-f', is_flag=True)
@click.option('--tables','-t', multiple=True)
def clear_data(full, tables):
    disa_models = [ 
        models.Person,
        models.Description,
        models.Entrant,
        models.Role,
        models.Location,
        models.Record,
        models.RecordType,
        models.Document,
        models.DocumentType
    ]
    model_map = { 'documents' : models.Document,
        'records' : models.Record,
        'locations' : models.Location,
        'entrants' : models.Entrant,
        'roles' : models.Role,
        'people' : models.Person,
        'entrant_description' : models.Description,
        'record_types' : models.RecordType,
        'document_types': models.DocumentType
    }
    if full:
        del_tables = disa_models
    elif tables:
        del_tables = [ model_map[t] for t in tables ]
    else:
        click.echo('Please provide tables to clear')
    for table in del_tables:
        rows = table.query.all()
        for row in rows:
            db.session.delete(row)
        print('Clear: {}'.format(table.__tablename__))
        db.session.commit()

@app.cli.command()
def load_multivalued_attributes():
    roles = [
        { 'name': 'enslaved', 'description_group': 1},
        { 'name': 'owner', 'description_group': 2},
        { 'name': 'priest', 'description_group': 2},
        { 'name': 'inoculated', 'description_group': 1},
        { 'name': 'escaped', 'description_group': 1},
        { 'name': 'captor', 'description_group': 2},
        { 'name': 'captured', 'description_group': 1},
        { 'name': 'baptised', 'description_group': 1},
        { 'name': 'emancipated', 'description_group': 1},
        { 'name': 'executed', 'description_group': 1}
    ]
    record_types = [ 
        { 'name': 'runaway advertisement' },
        { 'name': 'advertisement of sale' },
        { 'name': 'baptism' },
        { 'name': 'runaway capture advertisement' },
        { 'name': 'smallpox inoculation notice' },
        { 'name': 'execution notice'},
        { 'name': 'probate' },
        { 'name': 'manumission'}
    ]
    document_types = [
        { 'name': 'newspaper' },
        { 'name': 'letter' },
        { 'name': 'registry' },
        { 'name': 'inventory' },
        { 'name': 'census' },
        { 'name': 'court document' },
        { 'name': 'probate account' },
        { 'name': 'will' }
    ]
    tables = [
        ( models.Role, roles ),
        ( models.RecordType, record_types ),
        ( models.DocumentType, document_types ),
    ]
    for pair in tables:
        table = pair[0]
        for data in pair[1]:
            row = table(**data)
            db.session.add(row)
            print('{}: value {}'.format(table.__tablename__, data))
        db.session.commit()

@app.cli.command()
def load_many_to_many():
    recordtype_roles = [
        ('manumission', ['owner','emancipated']),
        ('runaway advertisement', ['owner','escaped']),
        ('advertisement of sale', ['owner','enslaved']),
        ('baptism', ['owner','priest','baptised']),
        ('runaway capture advertisement', ['captor', 'captured']),
        ('smallpox inoculation notice', ['inoculated','owner']),
        ('execution notice', ['executed']),
        ('probate', ['owner','enslaved'])
    ]

    many_to_many = [
        (models.RecordType, models.Role, recordtype_roles,
            'name', 'name', 'roles')
    ]

    for many in many_to_many:
        model1 = many[0]
        model2 = many[1]
        for mapping in many[2]:
            query = { many[3]: mapping[0] }
            focus = model1.query.filter_by( **query ).first()
            opts  = model2.query.all()
            rel = [ o for o in opts if getattr(o, many[4]) in mapping[1] ]
            getattr(focus, many[5]).extend(rel)
            db.session.add(focus)
            print( "{}:{} asscoiated with {}:{}".format(
                model1.__tablename__, mapping[0],
                model2.__tablename__, mapping[1]) )
            db.session.commit()



@app.cli.command()
# @click.option('--full', '-f', is_flag=True)
def migrate_mongo_data(dataFile):
    with open(dataFile, 'r') as f:
        data = json.load(f)

    for mongo_dict in data:
        doc_data = mongo_dict.get('document', {})
        doc = process_document(doc_data)
        rec = Record()

def process_date(dateData):
    day = int(dateData.get('day', '1'))
    month = int(dateData.get('month', '1'))
    year = int(dateData.get('year','2018'))
    return datetime.datetime(day=day, month=month, year=year)

def process_document_type(doctype):
    pass

def process_record_type(rectype):
    pass

def process_document(docData):
    existing = models.Document.query.filter_by(citation=docData['citation']).first()
    if existing:
        return existing
    doc = models.Document()
    doc.citation = docData.get('citation','Unlabelled Document')
    doc.national_context = docData.get('nationalContext')
    doc.document_type = process_document_type(docData.get('source','unspecified'))
    doc.date = process_date(docData.get('date'), {})
    db.session.add(doc)
    db.session.commit()
    return doc