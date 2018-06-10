from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from app.models import Document, Record, Entrant, Role, DocumentType, RecordType
from app.forms import DocumentForm, RecordForm, EnslavedForm, OwnerForm

@app.route('/')
def index():
    #return 'Index for {}'.format(__name__)

    return render_template('index.html')

@app.route('/documents', methods=['GET'])
def index_documents():
    all_docs = Document.query.all()
    return render_template('document_index.html', documents=all_docs)

@app.route('/documents/<docId>', methods=['GET'])
def show_document(docId):
    doc = Document.query.get(docId)
    return render_template('document_show.html', document=doc)

@app.route('/documents/new', methods=['GET','POST'])
def new_document():
    form = DocumentForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        doctype = DocumentType.query.get(form.doctype.data)
        doc = Document(document_type=doctype,
            date=form.date.data, national_context=form.context.data,
            citation=form.citation.data, zotero_id=form.zotero.data,
            comments=form.comments.data)
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('show_document', docId=doc.id))
    form.doctype.choices = [
        (t.id, t.name) for t in DocumentType.query.order_by('name')]
    return render_template('document_new.html', form=form)

@app.route('/records/new', methods = ['GET','POST'])
def new_record():
    form = RecordForm()
    doc = Document.query.get(request.args['docId'])
    if request.method == 'POST':
        rectype = RecordType.query.get(form.rectype.data)
        rec = Record(record_type = rectype, citation = form.citation.data,
            date=form.date.data, comments = form.comments.data, 
            document = doc)
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for('show_record', recId = rec.id))
    form.rectype.choices = [
        (t.id, t.name) for t in RecordType.query.order_by('name')]
    return render_template('record_new.html', form = form, document = doc)

@app.route('/records/<recId>', methods = ['GET'])
def show_record(recId):
    rec = Record.query.get(recId)
    rel_roles = rec.record_type.roles
    existing_roles =  { role for entrant in rec.entrants
        for role in entrant.roles }
    unassigned_roles = [ role for role in rel_roles
        if role not in existing_roles ]
    return render_template('record_show.html', record = rec,
        unassigned_roles = unassigned_roles)

@app.route('/entrants/new', methods = ['GET','POST'])
def new_entrant():
    role = Role.query.get(request.args['role'])
    if role.description_group == 1:
        form = EnslavedForm()
    elif role.description_group == 2:
        form = OwnerForm()
    else:
        return "<h1>Invalid</h1>"
    record = Record.query.get(request.args['recId'])
    if request.method == 'POST':
        selected_role = Role.query.filter_by(role=role).first()
        ent = Entrant(first_name = form.first_name.data,
            last_name=form.last_name.data, roles = [ selected_role ],
            record_id=record.id)
        db.session.add(ent)
        db.session.commit()

        if form.person_match.data == True:
            return redirect(url_for('add_entrant_to_person', entId = ent.id))
        else:
            person_id = create_person(ent.id)
        return redirect(url_for('show_record', recId = recId)) 
    return render_template('entrant_new.html', form = form, record = record, role = role)

@app.route('/entrants/<entId>')
@app.route('/documents/<docId>/records/<recId>/entrants/<entId>', methods = ['GET'])
def get_entrant(entId, recId=None, docId=None):
    ent = Entrant.query.filter_by(id=entId).first_or_404()
    return render_template('entrant.html', entrant=ent, record = recId)


# def add_entrant_to_person(entId, personId):

# def new_document(data):
#     doc = Document(data)
#     db.session.add(doc)
#     db.session.commit()
#     return doc

# def update_document(doc):

# def new_record(doc, rectype):
#     rec = Record(document=doc.id)
    
# def match_entrant_to_existing_person()

# def create_person_from_entrant(entrantId):
#     ent = Entrant.query.filter_by(id=entrantId).first()
#     person = Person(first_name=ent.first_name, last_name=ent.last_name)
#     person.references.append(ent)
#     db.session.add(person)
#     db.session.commit()
#     return person.id