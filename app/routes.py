from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db, models, forms

import datetime


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

@app.route('/editor/records')
@app.route('/editor/records/<recId>')
@login_required
def edit_record(recId=None):
    locs = [ { 'id': loc.id, 'value': loc.name,'label': loc.name }
        for loc in models.Location.query.all()]
    rec_types = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
        for rt in models.RecordType.query.all() ]
    if not recId:
        doc_id = request.args.get('doc')
        doc = models.Document.query.get(doc_id)
        return render_template(
            'record_edit.html', rec=None, doc=doc,
            rec_types=rec_types, locs=locs)
    rec = models.Record.query.get(recId)
    return render_template(
        'record_edit.html', rec=rec, doc=rec.document,
            rec_types=rec_types, locs=locs)

@app.route('/editor/person')
@app.route('/editor/person/<entId>')
@login_required
def edit_entrant(entId=None):
    if not entId:
        rec_id = request.args.get('rec')
        rec = models.Record.query.get(rec_id)
        return render_template(
            'entrant_edit.html', rec=rec, ent=None)
    ent = models.Entrant.query.get(entId)
    return render_template(
        'entrant_edit.html', rec=ent.record, ent=ent)

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

@app.route('/data/records/', methods=['GET'])
@app.route('/data/records/<recId>', methods=['GET'])
def read_record_data(recId=None):
    data = { 'rec': {} }
    if recId == None:
        return jsonify(data)
    rec = models.Record.query.get(recId)
    data['rec']['id'] = rec.id
    data['rec']['date'] = '{}/{}/{}'.format(rec.date.month,
        rec.date.day, rec.date.year)
    data['rec']['citation'] = rec.citation
    data['rec']['locations'] = [ 
        { 'label':l.location.name, 'value':l.location.name,
            'id': l.location.id } for l in rec.locations ]
    data['rec']['comments'] = rec.comments
    data['rec']['record_type'] = {'label': rec.record_type.name,
        'value': rec.record_type.name, 'id':rec.record_type.id }
    data['rec']['header'] = '{} {}'.format(
        rec.record_type.name, rec.citation or '').strip()
    return jsonify(data)


def get_or_create_type(typeData, typeModel):
    print(typeData)
    if typeData['id'] == -1:
        new_type = typeModel(name=typeData['value'])
        db.session.add(new_type)
        db.session.commit()
        return new_type
    elif typeData == '' or typeData['id'] == 0:
        unspec = typeModel.query.filter_by(name='unspecified').first()
        return unspec
    else:
        existing = typeModel.query.get(typeData['id'])
        return existing

def process_record_locations(locData, recObj):
    locations = []
    for loc in locData:
        if loc['id'] == -1:
            location = models.Location(name=loc['value'])
            db.session.add(location)
            db.session.commit()
        else:
            location = models.Location.query.get(loc['id'])
        locations.append(location)
    for loc in locations:
        rec_loc = models.RecordLocation()
        rec_loc.record = recObj
        rec_loc.location = loc
        rec_loc.location_rank = locations.index(loc)
        db.session.add(rec_loc)
    db.session.commit()
    return recObj


@app.route('/data/records/', methods=['POST'])
def create_record():
    data = request.get_json()
    print(data['document_id'])
    doc = models.Document.query.get(data['document_id'])
    if data['date']:
        date = datetime.datetime.strptime(data['date'], '%m/%d/%Y')
    else:
        date = doc.date
    record_type = get_or_create_type(data['record_type'], models.RecordType)
    rec = models.Record(citation=data['citation'],
        comments=data['comments'], date=date, document_id=doc.id,
        record_type_id=record_type.id)
    db.session.add(rec)
    db.session.commit()
    rec = process_record_locations(data['locations'], rec)
    return jsonify(
        { 'redirect': url_for('edit_record', recId=rec.id) })

@app.route('/data/records/', methods=['PUT'])
@app.route('/data/records/<recId>', methods=['PUT'])
def update_record_data(recId):
    data = request.get_json()
    if recId is None:
        return jsonify({})
    rec = models.Record.query.get(recId)
    rec.locations = []
    db.session.commit()
    rec = process_record_locations(data['locations'], rec)
    if data['date']:
        date = datetime.datetime.strptime(data['date'], '%m/%d/%Y')
    else:
        date = doc.date
    record_type = get_or_create_type(data['record_type'], models.RecordType)
    rec.citation = data['citation']
    rec.comments = data['comments']
    rec.date = date
    rec.record_type_id = record_type.id
    db.session.add(rec)
    db.session.commit()

    data = { 'rec': {} }
    data['rec']['id'] = rec.id
    data['rec']['date'] = '{}/{}/{}'.format(rec.date.month,
        rec.date.day, rec.date.year)
    data['rec']['citation'] = rec.citation
    data['rec']['comments'] = rec.comments
    data['rec']['locations'] = [ 
        { 'label':l.location.name, 'value':l.location.name,
            'id': l.location.id } for l in rec.locations ]
    data['rec']['record_type'] = {'label': rec.record_type.name,
        'value': rec.record_type.name, 'id':rec.record_type.id }
    return jsonify(data)