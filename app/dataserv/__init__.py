from flask import Blueprint

dataserv = Blueprint('dataserv', __name__)

from . import routes