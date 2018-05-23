from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from app.models import Document, Record, Entrant, Role
from app.forms import DocumentForm, RecordForm, EntrantForm

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
    doc = Document.query.filter_by(id=docId).first_or_404()
    if request.method == 'POST':
        rec = Record(rectype = form.rectype.data, citation = form.citation.data,
            date=form.date.data, comments = form.comments.data, 
            document_id = docId)
        db.session.add(rec)
        db.session.commit()

        return redirect(url_for('get_document', docId = docId))
    return render_template('new_record.html', form = form, document = doc)

@app.route('/records/<recId>')
@app.route('/documents/<docId>/records/<recId>', methods = ['GET'])
def get_record(recId, docId=None):
    rec = Record.query.filter_by(id=recId).first_or_404()
    return render_template('record.html', docId = docId, record = rec)

@app.route('/records/<recId>/entrants/new',
    methods = ['GET','POST'])
@app.route('/documents/<docId>/records/<recId>/entrants/new',
    methods = ['GET','POST'])
def new_entrant(recId, docId=None):
    form = EntrantForm()
    for entry in form.roles.entries:
        entry.choices = [ (r.id, r.role) for r in Role.query.all() ]
    record = Record.query.filter_by(id=recId).first_or_404()
    if request.method == 'POST':
        role_objs = [ Role.query.filter_by(id=rid).first()
            for rid in form.roles.data ]
        ent = Entrant(first_name = form.first_name.data,
            last_name=form.last_name.data, roles = role_objs,
            record_id=record.id)
        db.session.add(ent)
        db.session.commit()

        return redirect(url_for('get_record', recId = recId))
    return render_template('new_entrant.html', form = form, record = record)

# @app.route('/entrants/<entId>/roles/add', methods = ['POST'])
# def add_role(entId):
#     form = RoleForm()
#     record = Record.query.filter_by(id=recId).first_or_404()
#     if request.method == 'POST':
#         role_objs = [ Role.query.filter_by(id=rid).first()
#             for rid in form.roles.data ]
#         ent = Entrant(first_name = form.first_name.data,
#             last_name=form.last_name.data, roles = role_objs,
#             record_id=record.id)
#         db.session.add(ent)
#         db.session.commit()

#         return redirect(url_for('get_record', recId = recId))
#     return render_template('new_entrant.html', form = form, record = record)


@app.route('/entrants/<entId>')
@app.route('/documents/<docId>/records/<recId>/entrants/<entId>', methods = ['GET'])
def get_entrant(entId, recId=None, docId=None):
    ent = Entrant.query.filter_by(id=entId).first_or_404()
    return render_template('entrant.html', entrant=ent, record = recId)