from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Document, Record, Location, Entrant, Person
from models import EnslavedDescription, OwnerDescription, EntrantRole


@app.route('/')
def index():
    return 'Index for {}'.format(__name__)

if __name__ == '__main__':
    app.run()