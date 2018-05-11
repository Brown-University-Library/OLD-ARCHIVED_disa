from flask import request, jsonify, render_template
from app import app, db
from app.models import Document
from app.forms import DocumentForm

@app.route('/')
def index():
    return 'Index for {}'.format(__name__)

@app.route('/documents', methods=['GET'])
def documents_index():
    all_docs = Document.query.all()
    return render_template('document_index.html', documents=all_docs)

@app.route('/documents/new', methods=['GET','POST'])
def new_document():
    form = DocumentForm()
    return render_template('new_document.html', form=form)