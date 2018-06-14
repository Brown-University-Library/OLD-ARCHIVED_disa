from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from app.models import Document, Record, Entrant, Role, DocumentType, RecordType
from app.forms import DocumentForm, RecordForm, EntrantForm, EntrantRelationshipForm

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
    form = EntrantForm()
    if request.method == 'POST':
        ent = Entrant(first_name = form.first_name.data,
            last_name=form.last_name.data)
        record = Record.query.get(form.record.data)
        ent.record = record
        role = Role.query.get(form.role.data)
        ent.roles.append(role)
        db.session.add(ent)
        db.session.commit()
        return redirect(url_for('show_record', recId = record.id))
    record = Record.query.get(request.args['recId'])
    form.record.data = record.id
    form.role.choices = [
        (r.id, r.name) for r in Role.query.order_by('name')]
    if request.args.get('role', None):
        form.role.data = request.args['role']
    return render_template('entrant_new.html', form = form, record = record)

@app.route('/entrants/<entId>')
def show_entrant(entId):
    ent = Entrant.query.get(entId)
    return render_template('entrant_show.html', entrant=ent)

@app.route('/entrants/<entId>/relationships')
def entrant_relationships(entId):
    ent = Entrant.query.get(entId)
    return render_template('entrant_relationships.html', entrant = ent)

@app.route('/entrants/<entId>/relationships/add', methods=['GET','POST'])
def add_entrant_relationships(entId):
    form  = EntrantRelationshipForm()
    if request.method == 'POST':
        ent = Entrant.query.get(form.entrant.data)
        other = Entrant.query.get(form.other.data)
        rel_opt = int(form.related_as.data)
        if rel_opt == 1:
            ent.spouses.append(other)
        elif rel_opt == 2:
            ent.parents.append(other)
        elif rel_opt == 3:
            ent.owners.append(other)
        db.session.add(ent)
        db.session.commit()
        return redirect(url_for('entrant_relationships', entId = ent.id))
    ent = Entrant.query.get(entId)
    form.entrant.data = ent.id
    form.other.choices = [ (e.id, e.first_name + ' ' + e.last_name)
        for e in Entrant.query.filter_by(record_id=ent.record_id)
        if e.id != ent.id ]
    form.related_as.choices = [ (1, 'spouse'), (2, 'child of'), (3, 'owned by') ]
    return render_template('entrant_relationships.html', form = form, entrant = ent)