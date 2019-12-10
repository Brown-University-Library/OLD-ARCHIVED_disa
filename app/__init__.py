import json, logging, os, pprint
from logging.config import dictConfig  # <https://flask.palletsprojects.com/en/1.1.x/logging/>
from logging.handlers import SMTPHandler

import shellvars
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


## load up env vars
envar_dct = shellvars.get_vars( os.environ['DISA_FL__SETTINGS_PATH'] )
for ( key, val ) in envar_dct.items():
    os.environ[key.decode('utf-8')] = val.decode('utf-8')

## set up logging -- TODO: clean this up
dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            # 'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            'format': "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
            }
        },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',  # note: configure server to use system's log-rotate to avoid permissions issues
            'filename': os.environ['DISA_FL__LOGFILE_PATH'],
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        # 'handlers': ['wsgi']
        'handlers': ['logfile']
    }
})
log = logging.getLogger( __name__ )
log.info( '__init__.py logging working' )

## main work
app = Flask(__name__)
try:
    app.config.from_object(os.environ['APP_SETTINGS'])  # loads env from `dotenv` module
except:
    raise Exception( f'envars, ```{pprint.pformat(os.environ.__dict__)}```' )

## other config...
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.environ['DISA_FL__MAIL_SERVER']
app.config['MAIL_PORT'] = int( os.environ['DISA_FL__MAIL_PORT'] )
app.config['MAIL_USE_TLS'] = 1
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['ADMINS'] = json.loads( os.environ.get('DISA_FL__MAIL_ADMINS_JSON') )
app.config['GIT_DIR'] = os.environ['DISA_FL__GIT_DIR']
app.config['README_URL'] = os.environ['DISA_FL__README_URL']
log.debug( f'app.config, ```{pprint.pformat(app.config)}```' )

## enable email-on-error (credit: <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling>)
if app.config['MAIL_SERVER']:
    # log.debug( 'hereA' )
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject='DISA web-app error',
        credentials=auth, secure=secure)
    mail_handler.setLevel( logging.ERROR )
    app.logger.addHandler(mail_handler)

## app-vars
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models  # hmm -- is this used?

## CLI
from app.etl import teardown, setup, mongo, users, inferencing
from app.etl import denormalize, convert_citation_types
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
