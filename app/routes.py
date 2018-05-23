from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from app.models import Document, Record, Entrant, Role
from app.forms import DocumentForm, RecordForm, EnslavedForm, OwnerForm

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
    record_roles = {
        'Manumission' : ['Owner','Emancipated'],
        'Runaway advertisement' : ['Owner','Escaped'],
        'Advertisement of Sale' : ['Owner','Enslaved'],
        'Baptism' : ['Owner','Priest','Baptised'],
        'Runaway capture advertisement' : ['Captor', 'Captured'],
        'Smallpox inoculation notice' : ['Inoculated','Owner'],
        'Execution notice' : ['Executed'],
        'Probate' : ['Owner','Enslaved']
    }
    rel_roles = record_roles[rec.rectype]
    existing_roles =  { role.role for entrant in rec.entrants
        for role in entrant.roles }
    unassigned_roles = [ role for role in rel_roles
        if role not in existing_roles ]
    return render_template('record.html', docId = docId, record = rec,
        unassigned_roles = unassigned_roles)

@app.route('/records/<recId>/entrants/new',
    methods = ['GET','POST'])
# @app.route('/documents/<docId>/records/<recId>/entrants/new',
#     methods = ['GET','POST'])
def new_entrant(recId=None):
    role = request.args['role']
    mapped_roles = {
        'Owner': 'owner',
        'Enslaved' : 'enslaved',
        'Escaped' : 'enslaved',
        'Baptised' : 'enslaved',
        'Emancipated' : 'enslaved',
        'Captor' : 'owner',
        'Inoculated' : 'enslaved',
        'Executed' : 'enslaved',
        'Priest' : 'owner'
    }
    role_type = mapped_roles[role]
    if role_type == 'enslaved':
        form = EnslavedForm()
    else:
        form = OwnerForm()
    # form.role.choices = [ (r.id, r.role) for r in Role.query.all() ]
    record = Record.query.filter_by(id=recId).first_or_404()
    if request.method == 'POST':
        selected_role = Role.query.filter_by(role=role).first()
        ent = Entrant(first_name = form.first_name.data,
            last_name=form.last_name.data, roles = [ selected_role ],
            record_id=record.id)
        db.session.add(ent)
        db.session.commit()

        return redirect(url_for('get_record', recId = recId))
    return render_template('new_entrant.html', form = form, record = record, role = role)

@app.route('/entrants/<entId>')
@app.route('/documents/<docId>/records/<recId>/entrants/<entId>', methods = ['GET'])
def get_entrant(entId, recId=None, docId=None):
    ent = Entrant.query.filter_by(id=entId).first_or_404()
    return render_template('entrant.html', entrant=ent, record = recId)