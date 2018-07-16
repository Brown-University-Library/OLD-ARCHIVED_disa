from flask import request, jsonify, render_template, redirect, url_for, flash
from werkzeug.urls import url_parse
from app import app, db, models, forms
from app.models import Document, Record, Entrant, Role, DocumentType, RecordType
from app.forms import DocumentForm, RecordForm, EntrantForm, EntrantRelationshipForm

from flask_login import current_user, login_user, logout_user, login_required

import collections
import datetime


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
            next_page = url_for('editor_index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('browse'))

def sort_documents(wrappedDocs):
    merge = {}
    for w in wrappedDocs:
        if w[0].id not in merge or merge[w[0].id][0] < w[2]:
            merge[w[0].id] = (w[2], w[0])
        else:
            continue
    return sorted([ merge[w] for w in merge], reverse=True)
     

@app.route('/editor', methods=['GET'])
@login_required
def editor_index():
    all_docs = [ (doc, edit.user_id, edit.datetime)
                     for doc in models.Document.query.all()
                        for rec in doc.records
                            for edit in rec.edits
                                ]
    user_docs = [ wrapped for wrapped in all_docs
                    if wrapped[1] == current_user.id ]
    srtd_all = sort_documents(all_docs)
    srtd_user = sort_documents(user_docs)
    return render_template('document_index.html',
        user_documents=srtd_user, documents=srtd_all)

@app.route('/editor/documents')
@app.route('/editor/documents/<docId>')
@login_required
def edit_document(docId=None):
    if not docId:
        return render_template('document_edit.html', doc=None)
    doc = models.Document.query.get(docId)
    return render_template('document_edit.html', doc=doc)

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
    data['doc']['zotero_id'] = doc.zotero_id    
    data['doc']['acknowledgements'] = doc.acknowledgements
    data['doc']['document_type_id'] = doc.document_type_id
    return jsonify(data)

@app.route('/data/documents/', methods=['POST'])
def create_document():
    data = request.get_json()
    if data['citation'] == '':
        return {}
    doc_types = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.DocumentType.query.all() ]
    unspec = [ dt['id'] for dt in doc_types
        if dt['name'] == 'unspecified' ][0]
    date = data['date'] or '1/1/2001'
    data['date'] = datetime.datetime.strptime(date, '%m/%d/%Y')
    data['document_type_id'] = data['document_type_id'] or unspec
    doc = models.Document(**data)
    db.session.add(doc)
    db.session.commit()
    return jsonify(
        { 'redirect': url_for('edit_document', docId=doc.id) })

@app.route('/data/documents/', methods=['PUT'])
@app.route('/data/documents/<docId>', methods=['PUT'])
def update_document_data(docId):
    data = request.get_json()
    if docId is None or data['citation'] == '':
        return jsonify({})
    doc_types = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.DocumentType.query.all() ]
    unspec = [ dt['id'] for dt in doc_types
        if dt['name'] == 'unspecified' ][0]
    date = data['date'] or '1/1/2001'
    data['date'] = datetime.datetime.strptime(date, '%m/%d/%Y')
    data['document_type_id'] = data['document_type_id'] or unspec
    doc = models.Document.query.get(docId)
    doc.citation = data['citation']
    doc.date = data['date']
    doc.document_type_id = data['document_type_id']
    doc.zotero_id = data['zotero_id']
    doc.acknowledgements = data['acknowledgements']
    db.session.add(doc)
    db.session.commit()

    data = { 'doc': {} }
    data['doc_types'] = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.DocumentType.query.all() ]
    data['doc']['id'] = doc.id
    data['doc']['date'] = '{}/{}/{}'.format(doc.date.month,
        doc.date.day, doc.date.year)
    data['doc']['citation'] = doc.citation
    data['doc']['zotero_id'] = doc.zotero_id
    data['doc']['acknowledgements'] = doc.acknowledgements
    data['doc']['document_type_id'] = doc.document_type_id
    return jsonify(data)