from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from app.models import Document, Record
from app.forms import DocumentForm, RecordForm

@app.route('/')
def index():
    #return 'Index for {}'.format(__name__)
    return render_template('index.html')

@app.route('/documents', methods=['GET'])
def documents_index():
    all_docs = Document.query.all()
    return render_template('document_index.html', documents=all_docs)

@app.route('/documents/<docId>', methods=['GET'])
def get_document(docId):
    doc = Document.query.filter_by(id=docId).first_or_404()
    return render_template('document.html', document=doc)

@app.route('/documents/new', methods=['GET','POST'])
def new_document():
    form = DocumentForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        doc = Document(doctype=form.doctype.data,
            date=form.date.data, national_context=form.context.data,
            citation=form.citation.data, zotero_id=form.zotero.data,
            comments=form.comments.data)
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('get_document', docId=doc.id))
    return render_template('new_document.html', form=form)


@app.route('/documents/<docId>/records/new', methods = ['GET','POST'])
def new_record(docId):
	form = RecordForm()
	if request.method == 'POST':
		rec = Record(rectype = form.rectype.data, citation = form.citation.data,
			date=form.date.data, comments = form.comments.data, 
			document_id = docId)
		db.session.add(rec)
		db.session.commit()

		return redirect(url_for('get_document', docId = docId))
	return render_template('new_record.html', form = form)

@app.route('/documents/<docId>/records/<recId>', methods = ['GET'])
def get_record(docId, recId):
    rec = Record.query.filter_by(id=recId).first_or_404()
    return render_template('record.html', doc = docId, record = rec)