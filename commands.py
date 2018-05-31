import click
from app import app, db, models

# @app.cli.command()
# @click.option('--full', '-f', is_flag=True)
# @click.option('--table','-t', multiple=True)
@click.command()
def clear_data():
    click.echo('Inside function')
    click.echo('tables: %s' % tables)
    click.echo('full: %s' % full)
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


@app.cli.command()
def make_multivalued_attributes():
    roles = [ 'enslaved', 'owner', 'priest', 'inoculated',
        'escaped', 'captor', 'captured', 'baptised',
        'emancipated', 'executed' ]
    record_types = [ 'runaway advertisement', 'advertisement of sale',
        'baptism', 'runaway capture advertisement',
        'smallpox inoculation notice', 'execution notice', 'probate' ]

if __name__ == '__main__':
    