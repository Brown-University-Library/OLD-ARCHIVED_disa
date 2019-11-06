import os
import json
from flask_migrate import Migrate
from app import create_app, db
from app import models

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


# CLI
from etl import teardown, setup, mongo, users, inferencing
from etl import denormalize, convert_citation_types
import click

@app.cli.command()
@click.option('--tables','-t', multiple=True)
def empty_tables(tables=[]):
    teardown.clear_data(tables)

@app.cli.command()
def seed():
    setup.load_multivalued_attributes()
    setup.load_many_to_many()

@app.cli.command()
@click.argument('datafile')
def mongo_migration(datafile):
    mongo.load_data(datafile)

@app.cli.command()
def rebuild():
    teardown.clear_data()
    users.add_users('data/disa_users.json')
    setup.load_multivalued_attributes()
    setup.load_many_to_one()
    setup.load_many_to_many()
    setup.load_many_to_many_with_attr()
    setup.load_role_relationships()
    mongo.load_data(os.path.join(
        app.config['APP_DIR'], 'data/mongo/entries_01_31.json') )
    inferencing.extract_information()

@app.cli.command()
def browse_data():
    with open('app/static/data/denormalized.json','w') as f:
        data = denormalize.json_for_browse()
        json.dump(data, f)

@app.cli.command()
def convert_citations():
    convert_citation_types.convert(
        os.path.join(app.config['APP_DIR'], 'data') )

# END CLI

# TEMPLATES
@app.template_filter('century')
def get_century_from_year(yearInt):
  return yearInt // 100

@app.template_filter('decade')
def get_decade_from_year(yearInt):
  return yearInt % 100 // 10

@app.template_filter('year')
def get_year_from_datetime(yearInt):
  return yearInt % 10