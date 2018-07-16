from flask import request, jsonify, render_template, redirect, url_for, flash
from werkzeug.urls import url_parse
from app import app, db, models, forms
from app.models import Document, Record, Entrant, Role, DocumentType, RecordType
from app.forms import DocumentForm, RecordForm, EntrantForm, EntrantRelationshipForm

from flask_login import current_user, login_user, logout_user, login_required

import collections
import datetime

def parse_date_data(form):
    dt = datetime.datetime.strptime("{}-{}-{}{}{}".format(
        form.day.data or '1', form.month.data or '1',
        form.century.data or '20', form.decade.data or '0',
        form.year.data or '0'), "%d-%m-%Y" )
    return dt

def prep_record_form(form, rec=None):
    form.record_type.choices = [
        (t.id, t.name) for t in RecordType.query.order_by('name')]
    months = [ datetime.date(year=1900,month=m,day=1) for m in range(1,13) ]
    form.month.choices = [ ( m.month, m.strftime("%B") ) for m in months ]
    form.century.choices = [ (c, c) for c in range(14,21) ]
    form.decade.choices = [ (d, d) for d in range(10)]
    form.year.choices = [ (y, y) for y in range(10)]
    if not rec:
        return form   

    form.citation.data = rec.citation
    form.comments.data = rec.comments
    form.record_type.data = str(rec.record_type.id)
    form.day.data = getattr(rec.date, 'day', '')
    form.month.data = str(getattr(rec.date, 'month', 1) )
    form.century.data = str( getattr(rec.date, 'year', 14) // 100 ), 
    form.decade.data = str( getattr(rec.date, 'year',0) % 100 // 10)
    form.year.data = str( getattr(rec.date, 'year',0) % 10)
    return form

def prep_document_form(form, doc=None):
    form.document_type.choices = [
        (t.id, t.name) for t in DocumentType.query.order_by('name')]
    months = [ datetime.date(year=1900,month=m,day=1) for m in range(1,13) ]
    form.month.choices = [ ( m.month, m.strftime("%B") ) for m in months ]
    form.century.choices = [ (c, c) for c in range(14,21) ]
    form.decade.choices = [ (d, d) for d in range(10)]
    form.year.choices = [ (y, y) for y in range(10)]
    if not doc:
        return form   

    form.citation.data = doc.citation
    form.zotero_id.data = doc.zotero_id
    form.acknowledgements.data = doc.acknowledgements
    form.document_type.data = str(doc.document_type.id)
    form.day.data = doc.date.day
    form.month.data = str(doc.date.month)
    form.century.data = str(doc.date.year // 100)
    form.decade.data = str(doc.date.year % 100 // 10)
    form.year.data = str(doc.date.year % 10)
    return form

def make_person_dict(p):
    data = {
        'first_name': p.first_name,
        'last_name': p.last_name,
        'reference_details': collections.defaultdict(list)
    }
    for entrant in p.references:
        rec = entrant.record 
        ref_data = { 'roles': [] }
        if len(entrant.as_subject) > 0:
            ers = entrant.as_subject
            for er in ers:
                role = er.related_as.name
                obj = er.obj
                if obj is None:
                    print(er.id)
                    continue
                other = "{} {}".format(obj.first_name, obj.last_name).strip()
                ref_data['roles'].append('{}: {}'.format(role, other))
        else:
            ref_data['roles'] = [ role.name for role in entrant.roles ]
        ref_data['date'] = {
            'year': rec.date.year,
            'month': rec.date.month,
            'day': rec.date.day
        }
        doc = rec.document.citation
        data['reference_details'][doc].append(ref_data)
    data['references'] = sorted(data['reference_details'].keys())
    data['reference_details'] = dict(data['reference_details'])
    return (p, data)

def stub_json(entrant):
    jdata = {}
    jdata['_id'] = entrant.id
    jdata['person'] = {
        'names': [
            {
                'firstName': entrant.first_name,
                'lastName': entrant.last_name
            }
        ],
        'typeKindOfEnslavement': entrant.roles[0].name
    }
    jdata['document'] = {
        'date': {
            'year': entrant.record.date.year,
            'month': entrant.record.date.month,
            'day': entrant.record.date.day,
        },
        'citation': entrant.record.document.citation,
        'stringLocation': '',
        'nationalContext': '',
        'colonyState': ''   
    }
    description = getattr(entrant,'description')
    if description:
        jdata['person']['tribe'] = description.tribe
        jdata['person']['sex'] = description.sex
        jdata['person']['origin'] = description.origin
        jdata['person']['vocation'] = description.vocation
    jdata['additionalInformation'] = ''
    jdata['researcherNotes'] = ''
    jdata['dateOfRunaway'] =''
    jdata['dateOfMarriage'] =''
    jdata['dateOfDeath'] =''
    jdata['dateOfEmancipation'] =''
    jdata['dateOfSale'] = ''
    return jdata

@app.route('/browsedata')
def get_browse_data(opts=None):
    persons = models.Person.query.all()
    person_data = [ make_person_dict(p) for p in persons ]
    to_merge = [] 
    for p in person_data:
        for e in p[0].references:
            to_merge.append( (p[1], stub_json(e)) )
    data = []
    for d in to_merge:
        d[1]['agg'] = d[0]
        data.append(d[1])
    return jsonify(data)

@app.route('/')
def browse():
    return render_template('browse.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_documents'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index_documents')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('browse'))

@app.route('/documents', methods=['GET'])
@login_required
def index_documents():
    all_docs = Document.query.all()
    return render_template('document_index.html', documents=all_docs)

@app.route('/edit/documents')
@app.route('/edit/documents/<docId>')
@login_required
def edit_document(docId=None):
    if not docId:
        return render_template('document_edit.html', doc=None)
    doc = models.Document.query.get(docId)
    return render_template('document_edit.html', doc=doc)

@app.route('/documents/<docId>', methods=['GET','POST'])
@login_required
def show_document(docId):
    doc = Document.query.get(docId)
    form = DocumentForm()
    if request.method == 'POST':
        doc.citation = form.citation.data
        doc.zotero_id = form.zotero_id.data
        doc.document_type = DocumentType.query.get(form.document_type.data)
        doc.date = parse_date_data(form)
        doc.acknowledgements = form.acknowledgements.data
        db.session.add(doc)
        db.session.commit()
        form = prep_document_form(form, doc)
        return render_template('document_show.html', document=doc, form=form)
        
    if request.args.get('edit', False):
        form = prep_document_form(form, doc)
        return render_template(
            'document_show.html', document=doc, form=form, edit=True)
    return render_template('document_show.html', document=doc)

@app.route('/documents/new', methods=['GET','POST'])
def new_document():
    form = DocumentForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        doc = Document(citation=form.citation.data,
            # national_context=form.national_context.data,
            acknowledgements=form.acknowledgements.data,
            zotero_id=form.zotero_id.data)
        doc.document_type = DocumentType.query.get(form.document_type.data)
        doc.date = parse_date_data(form)
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('show_document', docId=doc.id))

    form = prep_document_form(form)
    return render_template('document_new.html', form=form)

@app.route('/records/new', methods = ['GET','POST'])
def new_record():
    form = RecordForm()
    doc = Document.query.get(request.args['docId'])
    if request.method == 'POST':
        rectype = RecordType.query.get(form.record_type.data)
        rec = Record(record_type = rectype, citation = form.citation.data,
            date=form.date.data, comments = form.comments.data, 
            document = doc)
        rec.date = parse_date_data(form)
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for('show_record', recId = rec.id))
    form = prep_record_form(form)
    return render_template('record_new.html', form = form, document = doc)

@app.route('/records/<recId>', methods = ['GET','POST'])
def show_record(recId):
    rec = Record.query.get(recId)
    form = RecordForm()
    if request.args.get('edit', False):
        form = prep_record_form(form, rec)
        return render_template(
            'record_show.html', record=rec, form=form, edit=True)
    if request.method == 'POST':
        rec.citation = form.citation.data
        rec.record_type = RecordType.query.get(form.record_type.data)
        rec.date = parse_date_data(form)
        rec.comments = form.comments.data
        db.session.add(rec)
        db.session.commit()
        
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

@app.route('/data/documents/', methods=['GET'])
@app.route('/data/documents/<docId>', methods=['GET'])
def read_document_data(docId=None):
    data = { 'doc': {} }
    data['doc_types'] = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.DocumentType.query.all() ]
    if docId == None:
        return jsonify(data)
    doc = models.Document.query.get(docId)
    data['doc']['id'] = doc.id
    data['doc']['date'] = '{}/{}/{}'.format(doc.date.month,
        doc.date.day, doc.date.year)
    data['doc']['citation'] = doc.citation
    data['doc']['zotero'] = doc.zotero_id    
    data['doc']['acknowledgements'] = doc.acknowledgements
    data['doc']['doc_type_id'] = doc.document_type_id 
    return jsonify(data)

@app.route('/data/documents/', methods=['PUT'])
@app.route('/data/documents/<docId>', methods=['PUT'])
def update_document_data(docId=None):
    if docId is None:
        return jsonify({})
    print(request.get_json())
    return jsonify({"ricky": "you're the best"})