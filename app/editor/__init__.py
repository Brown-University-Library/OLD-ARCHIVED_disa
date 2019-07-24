from flask import Blueprint

editor = Blueprint('editor', __name__)

from . import routes