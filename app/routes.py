from flask import request, jsonify
from app import app, db
from app.models import Document

@app.route('/')
def index():
    return 'Index for {}'.format(__name__)

@app.route('/documents', methods=['GET'])
def documents_index():
    all_docs = Document.query.all()
    ids = [ doc.id for doc in all_docs ]
    return jsonify(ids)