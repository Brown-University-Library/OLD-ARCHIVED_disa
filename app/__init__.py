from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

import os

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
    disa_models = [ models.Document, models.Record,
        models.Location, models.Entrant, models.Role,
        models.Person, models.EnslavedDescription,
        models.OwnerDescription ]
    model_map = { 'documents' : models.Document,
        'records' : models.Record,
        'locations' : models.Location,
        'entrants' : models.Entrant,
        'roles' : models.Role,
        'people' : models.Person,
        'description_of_enslaved' : models.EnslavedDescription,
        'description_of_owner' : models.OwnerDescription
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
        { 'name': 'probate' }
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
    for table_tup in tables:
        table = table_tup[0]
        for data in table_tup[1]:
            row = table(**data)
            db.session.add(row)
        db.session.commit()