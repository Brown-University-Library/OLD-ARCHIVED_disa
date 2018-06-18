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
        { 'name': 'executed', 'description_group': 1},
        { 'name': 'maidservant', 'description_group': 1},
        { 'name': 'manservant', 'description_group': 1},
        { 'name': 'indentured servant', 'description_group': 1},
        { 'name': 'pieza', 'description_group': 1},
        { 'name': 'manslave', 'description_group': 1},
        { 'name': 'servant', 'description_group': 1}
    ]
    record_types = [ 
        { 'name': 'runaway advertisement' },
        { 'name': 'advertisement of sale' },
        { 'name': 'baptism' },
        { 'name': 'runaway capture advertisement' },
        { 'name': 'smallpox inoculation notice' },
        { 'name': 'execution notice'},
        { 'name': 'probate' },
        { 'name': 'manumission'},
        { 'name': 'registry'},
        { 'name': 'news story'},
        { 'name': 'unspecified' }
    ]
    document_types = [
        { 'name': 'newspaper' },
        { 'name': 'letter' },
        { 'name': 'archive' },
        { 'name': 'inventory' },
        { 'name': 'census' },
        { 'name': 'court documents' },
        { 'name': 'book' },
        { 'name': 'will' },
        { 'name': 'unspecified' }
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
@click.argument('datafile')
def migrate_mongo_data(datafile):
    with open(datafile, 'r') as f:
        data = json.load(f)

    counter = 0
    for mongo_dict in data:
        print(counter)
        doc = process_document(mongo_dict['document'])
        db.session.add(doc)
        db.session.commit()

        rec = process_record(mongo_dict)
        rec.document = doc
        db.session.add(rec)
        db.session.commit()

        entrants = process_person(mongo_dict['person'])
        owner = process_owner(mongo_dict['owner'])
        entrants.extend(owner)
        for e in entrants:
            e.record = rec
            db.session.add(e)
        db.session.commit()
        # entrants[0].owners.extend(owner)
        # db.session.add(entrants[0])
        # db.session.commit()
        counter += 1

def process_date(dateData):
    if dateData == {} or dateData == {'month': ''}:
        dateData = { 'day':1, 'month':1, 'year':1 }
    try:
        day = int( dateData.get('day',1) or 1)
        month = int( dateData.get('month',1) or 1)
        year = int( dateData.get('year',1) or 1)
    except:
        day = 1
        month = 1
        year = 1
    return datetime.datetime(day=day, month=month, year=year)

def process_other_person(personData):
    empty_data = {
        'firstName': '',
        'lastName': ''
    }
    if personData == {} or personData == empty_data:
        return []
    entrant = models.Entrant(first_name=personData['firstName'],
        last_name=personData['lastName'])
    return  [ entrant ]

def process_owner(personData):
    # role = models.Role.query.filter_by(name='owner').first()
    empty_data = {
        'name': {
            'firstName': '',
            'lastName': '',
            'title': ''
        },
        'vocation': ''
    }
    if personData == {} or personData == empty_data:
        return []
    entrant = models.Entrant(first_name=personData['name']['firstName'],
        last_name=personData['name']['lastName'])
    desc = models.Description(vocation=personData['vocation'],
        title=personData['name']['title'])
    desc.entrant = entrant
    # entrant.roles.append(role)
    return [ entrant ]

def process_parent(personData):
    empty_data = {
        'name': {
            'firstName': '',
            'lastName': ''
        },
        'origin': '',
        'owner': {
            'name': {
                'firstName': '',
                'lastName': '',
                'title': ''
            },
            'vocation': ''
        },
        'race': '',
        'status': ''
   }
    if personData == {} or personData == empty_data:
        return []
    entrant = models.Entrant(first_name=personData['name']['firstName'],
        last_name=personData['name']['lastName'])
    desc = models.Description(race=personData['race'], origin=personData['origin'],
        status=personData['status'])
    desc.entrant = entrant
    out = [ entrant ]
    owner = process_owner(personData['owner'])
    out.extend(owner)
    return out

def process_child(personData):
    empty_data = {
        'name' : {
            'firstName': '',
            'lastName': ''
        }
    }
    if personData == {} or personData == empty_data:
        return []
    entrant = models.Entrant(first_name=personData['name']['firstName'],
        last_name=personData['name']['lastName'])
    return  [ entrant ]

def process_children(childDataList):
    entrants = []
    for child in childDataList:
        entrants.extend( process_child(child) )
    return entrants

def process_enslavement_type(typeStr):
    type_map = {
        '': 'enslaved',
        '(maybe) ': 'enslaved',
        '(probably) ': 'enslaved',
        'Indenture': 'indentured servant',
        'Indentured servant': 'indentured servant',
        'Maid Servant': 'maidservant',
        'Maid servant': 'maidservant',
        'Man servant': 'manservant',
        'Man slave': 'manslave',
        'Manslave': 'manslave',
        'Pieza': 'pieza',
        'Servant': 'servant',
        'Slave': 'enslaved',
        'Woman servant': 'maidservant'
    }
    type_obj = models.Role.query.filter_by(
        name=type_map[typeStr]).first()
    return type_obj

def process_person(personData):
    try:
        name = personData['names'][0]
    except IndexError:
        name = { 'firstName': '', 'lastName': '' }
    entrant = models.Entrant(
        first_name=name['firstName'], last_name=name['lastName'])
    role = process_enslavement_type(personData['typeKindOfEnslavement'])
    entrant.roles.append(role) 
    desc = models.Description(race=personData['race'], origin=personData['origin'],
        tribe=personData['tribe'], sex=personData['sex'], age=personData.get('age',0),
        vocation=personData['vocation'])
    desc.entrant = entrant
    child_entrants = process_children(personData['children'])
    mom_entrants = process_parent(personData['mother'])
    dad_entrants = process_parent(personData['father'])
    out = [ entrant ]
    out.extend(child_entrants)
    out.extend(mom_entrants)
    out.extend(dad_entrants)
    return out

def process_document_type(typeStr):
    type_map = {
        '': 'unspecified',
        'Archie': 'archive',
        'Archival': 'archive',
        'Archival ': 'archive',
        'Archive': 'archive',
        'Archive ': 'archive',
        'Book': 'book',
        'Census': 'census',
        'Court Documents': 'court documents',
        'Indenture': 'court documents',
        'Inventory': 'inventory',
        'Letter': 'letter',
        'Mosquito Coast ': 'archive',
        'Newsletter': 'newspaper',
        'Newspaper': 'newspaper',
        'Newspaper ': 'newspaper',
        'Printed primary source': 'newspaper',
        'Probate Account': 'court documents',
        'Probate note': 'court documents',
        'Registry': 'archive',
        'Runaway Advertisement': 'newspaper',
        'Runaway advertisement': 'newspaper',
        'Will': 'will',
        'Will Written': 'will'
    }
    type_obj = models.DocumentType.query.filter_by(
        name=type_map[typeStr]).first()
    return type_obj

def process_document(docData):
    existing = models.Document.query.filter_by(citation=docData['citation']).first()
    if existing:
        return existing
    doc = models.Document()
    doc.citation = docData['citation']
    doc.national_context = docData['nationalContext']
    doc.document_type = process_document_type(docData['sourceType'])
    doc.date = process_date(docData['date'])
    return doc

def process_record_type(typeStr):
    type_map = {'': 'unspecified',
        'Advertisement of Sale': 'advertisement of sale',
        'Advertisement of sale': 'advertisement of sale',
        'Archival': 'unspecified',
        'Archive': 'unspecified',
        'Book': 'unspecified',
        'Court Document': 'unspecified',
        'Execution notice': 'execution notice',
        'Honduras': 'unspecified',
        'Inventory': 'unspecified',
        'LIst': 'unspecified',
        'Letter': 'unspecified',
        'List': 'unspecified',
        'Listing': 'unspecified',
        'Manumission': 'manumission',
        'Manumission ': 'manumission',
        'News story': 'news story',
        'Newspaper': 'news story',
        'Probate': 'probate',
        'Registry': 'registry',
        'Registry ': 'registry',
        'Runaway Advertisement': 'runaway advertisement',
        'Runaway Advertisement ': 'runaway advertisement',
        'Runaway Advertisements': 'runaway advertisement',
        'Runaway Capture Advertisement': 'runaway capture advertisement',
        'Runaway advertisement': 'runaway advertisement',
        'Runaway capture advertisement': 'runaway capture advertisement',
        'Smallpox inoculation notice': 'smallpox inoculation notice'
    }
    type_obj = models.RecordType.query.filter_by(
        name=type_map[typeStr]).first()
    return type_obj

def process_record(data):
    rec = models.Record()
    rec.record_type = process_record_type(data['document']['recordType'])
    return rec
