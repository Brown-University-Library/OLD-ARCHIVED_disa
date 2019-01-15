from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db, models, forms

import datetime
import collections


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
                     for doc in models.Citation.query.all()
                        for rec in doc.references
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
    doc = models.Citation.query.get(docId)
    return render_template('document_edit.html', doc=doc)

@app.route('/editor/records')
@app.route('/editor/records/<recId>')
@login_required
def edit_record(recId=None):
    locs = [ { 'id': loc.id, 'value': loc.name,'label': loc.name }
        for loc in models.Location.query.all()]
    rec_types = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
        for rt in models.ReferenceType.query.all() ]
    natl_ctxs = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
        for rt in models.NationalContext.query.all() ]
    roles = [ { 'id': role.id, 'value': role.name, 'name': role.name }
        for role in models.Role.query.all() ]
    if not recId:
        doc_id = request.args.get('doc')
        doc = models.Citation.query.get(doc_id)
        return render_template(
            'record_edit.html', rec=None, doc=doc, natl_ctxs=natl_ctxs,
            rec_types=rec_types, locs=locs, roles=roles)
    rec = models.Reference.query.get(recId)
    return render_template(
        'record_edit.html', rec=rec, doc=rec.citation, natl_ctxs=natl_ctxs,
            rec_types=rec_types, locs=locs, roles=roles)

@app.route('/editor/person')
@app.route('/editor/person/<entId>')
@login_required
def edit_entrant(entId=None):
    nametypes = [ { 'id': role.id, 'value': role.name, 'label': role.name }
        for role in models.NameType.query.all()]
    roles = [ { 'id': role.id, 'value': role.name, 'label': role.name }
        for role in models.Role.query.all()]
    # desc_data = models.Description.query.all()
    origins = [ { 'id': loc.id, 'value': loc.name, 'label': loc.name }
        for loc in models.Location.query.all()]
    races = [ { 'id': loc.id, 'value': loc.name, 'label': loc.name }
        for loc in models.Race.query.all()]
    tribes = [ { 'id': loc.id, 'value': loc.name, 'label': loc.name }
        for loc in models.Tribe.query.all()]
    titles = [ { 'id': loc.id, 'value': loc.name, 'label': loc.name }
        for loc in models.Title.query.all()]
    vocations = [ { 'id': loc.id, 'value': loc.name, 'label': loc.name }
        for loc in models.Vocation.query.all()]
    enslavements = [ { 'id': loc.id, 'value': loc.name, 'label': loc.name }
        for loc in models.EnslavementType.query.all()]
    if not entId:
        rec_id = request.args.get('rec')
        rec = models.Reference.query.get(rec_id)
        return render_template(
            'entrant_edit.html', roles=roles, rec=rec, ent=None)
    ent = models.Referent.query.get(entId)
    return render_template(
        'entrant_edit.html', rec=ent.reference, ent=ent,
        nametypes=nametypes,
        roles=roles, origins=origins, races=races, tribes=tribes,
        vocations=vocations, enslavements=enslavements,
        titles=titles)

@app.route('/data/documents/', methods=['GET'])
@app.route('/data/documents/<docId>', methods=['GET'])
def read_document_data(docId=None):
    data = { 'doc': {} }
    data['doc_types'] = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.CitationType.query.all() ]
    if docId == None:
        return jsonify(data)
    doc = models.Citation.query.get(docId)
    data['doc']['id'] = doc.id
    # data['doc']['date'] = '{}/{}/{}'.format(doc.date.month,
    #     doc.date.day, doc.date.year)
    data['doc']['citation'] = doc.display
    data['doc']['zotero_id'] = doc.zotero_id    
    data['doc']['comments'] = doc.comments
    data['doc']['acknowledgements'] = doc.acknowledgements
    data['doc']['document_type_id'] = doc.citation_type_id
    return jsonify(data)

@app.route('/data/documents/', methods=['POST'])
def create_document():
    data = request.get_json()
    if data['citation'] == '':
        data['citation'] = 'Citation'
    doc_types = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.CitationType.query.all() ]
    date = data['date'] or '1/1/2001'
    data['date'] = datetime.datetime.strptime(date, '%m/%d/%Y')
    data['document_type_id'] = data['document_type_id']
    doc = models.Citation(**data)
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
        for dt in models.CitationType.query.all() ]
    unspec = [ dt['id'] for dt in doc_types
        if dt['name'] == 'unspecified' ][0]
    date = data['date'] or '1/1/2001'
    data['date'] = datetime.datetime.strptime(date, '%m/%d/%Y')
    data['document_type_id'] = data['document_type_id'] or unspec
    doc = models.Citation.query.get(docId)
    doc.citation = data['citation']
    doc.date = data['date']
    doc.citation_type_id = data['document_type_id']
    doc.zotero_id = data['zotero_id']
    doc.comments = data['comments']
    doc.acknowledgements = data['acknowledgements']
    db.session.add(doc)
    db.session.commit()

    data = { 'doc': {} }
    data['doc_types'] = [ { 'id': dt.id, 'name': dt.name }
        for dt in models.CitationType.query.all() ]
    data['doc']['id'] = doc.id
    data['doc']['date'] = '{}/{}/{}'.format(doc.date.month,
        doc.date.day, doc.date.year)
    data['doc']['citation'] = doc.citation
    data['doc']['zotero_id'] = doc.zotero_id
    data['doc']['comments'] = doc.comments
    data['doc']['acknowledgements'] = doc.acknowledgements
    data['doc']['document_type_id'] = doc.citation_type_id
    return jsonify(data)

@app.route('/data/records/', methods=['GET'])
@app.route('/data/records/<recId>', methods=['GET'])
def read_record_data(recId=None):
    data = { 'rec': {}, 'entrants': [] }
    if recId == None:
        return jsonify(data)
    rec = models.Reference.query.get(recId)
    data['rec']['id'] = rec.id
    data['rec']['date'] = '{}/{}/{}'.format(rec.date.month,
        rec.date.day, rec.date.year)
    data['rec']['national_context'] = rec.national_context.id
    # data['rec']['locations'] = [ 
    #     { 'label':l.location.name, 'value':l.location.name,
    #         'id': l.location.id } for l in rec.locations ]
    data['rec']['transcription'] = rec.transcription
    data['rec']['record_type'] = {'label': rec.reference_type.name,
        'value': rec.reference_type.name, 'id':rec.reference_type.id }
    data['entrants'] = [ 
        {
            'name_id': ent.primary_name.id,
            'first': ent.primary_name.first,
            'last': ent.primary_name.last,
            'id': ent.id,
            'roles': [ role.id for role in ent.roles ]
        }
            for ent in rec.referents ]
    data['rec']['header'] = '{}'.format(
        rec.reference_type.name or '').strip()
    return jsonify(data)

@app.route('/data/entrants/', methods=['GET'])
@app.route('/data/entrants/<entId>', methods=['GET'])
def read_entrant_data(entId=None):
    data = { 'ent': {} }
    if entId == None:
        return jsonify(data)
    ent = models.Referent.query.get(entId)
    data['ent']['id'] = ent.id
    data['ent']['names'] = [
        { 'first': n.first, 'last': n.last,
            'name_type': n.name_type.name,
            'id': n.id } for n in ent.names ]
    data['ent']['age'] = ent.age
    data['ent']['sex'] = ent.sex
    data['ent']['races'] = [ 
        { 'label': r.name, 'value': r.name,
            'id': r.id } for r in ent.races ]
    data['ent']['tribes'] = [ 
        { 'label': t.name, 'value': t.name,
            'id': t.id } for t in ent.tribes ]
    data['ent']['origins'] = [ 
        { 'label': o.name, 'value': o.name,
            'id': o.id } for o in ent.origins ]
    data['ent']['titles'] = [ 
        { 'label': t.name, 'value': t.name,
            'id': t.id } for t in ent.titles ]
    data['ent']['vocations'] = [ 
        { 'label': v.name, 'value': v.name,
            'id': v.id } for v in ent.vocations ]
    data['ent']['enslavements'] = [ 
        { 'label': e.name, 'value': e.name,
            'id': e.id } for e in ent.enslavements ]
    return jsonify(data)


def get_or_create_type(typeData, typeModel):
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
        rec_loc = models.ReferenceLocation()
        rec_loc.reference = recObj
        rec_loc.location = loc
        rec_loc.location_rank = locations.index(loc)
        db.session.add(rec_loc)
    db.session.commit()
    return recObj


@app.route('/data/records/', methods=['POST'])
def create_record():
    data = request.get_json()
    doc = models.Citation.query.get(data['document_id'])
    if data['date']:
        date = datetime.datetime.strptime(data['date'], '%m/%d/%Y')
    else:
        date = doc.date
    record_type = get_or_create_type(data['record_type'], models.ReferenceType)
    rec = models.Reference(citation=data['citation'],
        comments=data['comments'], date=date, citation_id=doc.id,
        reference_type_id=reference_type.id)
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
    rec = models.Reference.query.get(recId)
    rec.locations = []
    db.session.commit()
    rec = process_record_locations(data['locations'], rec)
    if data['date']:
        date = datetime.datetime.strptime(data['date'], '%m/%d/%Y')
    else:
        date = doc.date
    record_type = get_or_create_type(data['record_type'], models.ReferenceType)
    rec.citation = data['citation']
    rec.comments = data['comments']
    rec.date = date
    rec.reference_type_id = reference_type.id
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
    data['rec']['record_type'] = {'label': rec.reference_type.name,
        'value': rec.reference_type.name, 'id':rec.reference_type.id }
    return jsonify(data)

def update_entrant_name(data):
    if data['id'] == 'name':
        name = models.ReferentName()
    else:
        name = models.ReferentName.query.get(data['id'])
    name.first = data['first']
    name.last = data['last']
    given = models.NameType.query.filter_by(name='Given').first()
    name.name_type_id = data.get('name_type', given.id)
    return name   

def get_or_create_entrant_attribute(data, attrModel):
    if data['id'] == data['name']:
        new_attr = attrModel(name=data['name'])
        db.session.add(new_attr)
        db.session.commit()
        return new_attr
    else:
        existing = attrModel.query.get(data['id'])
        return existing 

@app.route('/data/entrants/', methods=['POST'])
@app.route('/data/entrants/<entId>', methods=['PUT', 'DELETE'])
def update_entrant(entId=None):
    if request.method == 'DELETE':
        ent = models.Referent.query.get(entId)
        db.session.delete(ent)
        db.session.commit()
        return jsonify( { 'id': entId } )
    data = request.get_json()
    if request.method == 'POST':
        ent = models.Referent(reference_id=data['record_id'])
    if request.method == 'PUT':
        ent = models.Referent.query.get(entId)
    primary_name = update_entrant_name(data['name'])
    ent.names.append(primary_name)
    ent.primary_name = primary_name
    ent.roles = [ get_or_create_entrant_attribute(a, models.Role)
        for a in data['roles'] ]
    db.session.add(ent)
    db.session.commit()

    return jsonify({
        'name_id': ent.primary_name.id,
        'first': ent.primary_name.first,
        'last': ent.primary_name.last,
        'id': ent.id,
        'roles': [ role.id for role in ent.roles ] })

@app.route('/data/entrants/details/', methods=['PUT'])
@app.route('/data/entrants/details/<entId>', methods=['PUT'])
def update_entrant_details(entId):
    ent = models.Referent.query.get(entId)
    data = request.get_json()
    ent.names = [ update_entrant_name(n) for n in data['names'] ]
    ent.age = data['age']
    ent.sex = data['sex'] 
    ent.primary_name = ent.names[0]
    ent.races = [ get_or_create_entrant_attribute(a, models.Race)
        for a in data['races'] ]
    ent.tribes = [ get_or_create_entrant_attribute(a, models.Tribe)
        for a in data['tribes'] ]
    ent.origins = [ get_or_create_entrant_attribute(a, models.Location)
        for a in data['origins'] ]
    ent.titles = [ get_or_create_entrant_attribute(a, models.Title)
        for a in data['titles'] ]
    ent.enslavements = [ get_or_create_entrant_attribute(
        a, models.EnslavementType)
            for a in data['statuses'] ]
    ent.vocations = [ get_or_create_entrant_attribute(
        a, models.Vocation)
            for a in data['vocations'] ]
    db.session.add(ent)
    db.session.commit()

    return jsonify(
        { 'redirect': url_for('edit_record', recId=ent.reference_id) })

def parse_person_relations(personObj):
    rels = [ (r.related_as, r.obj) for e in personObj.references
                for r in e.as_subject ]
    grouped = collections.defaultdict(list)
    for r in rels:
        grouped[ r[0].name_as_relationship ].append(
            { 'id': r[1].person_id,
            'name': parse_person_name(r[1].person) } )
    out = [ { 'type': k, 'related': v } for k,v in grouped.items() ]
    return out

def parse_person_name(personObj):
    out = "{0} {1}".format(personObj.first_name, personObj.last_name).strip()
    if out == "":
        return "Unknown"
    return out

def parse_person_descriptors(personObj, descField):
    vals = { desc.name for ref in personObj.references
                for desc in getattr(ref, descField) }
    out = ', '.join(list(vals))
    return out if out else 'None'

@app.route('/people/')
def person_index():
    enslaved = [ p for p in models.Person.filter_on_description('Enslaved') ]
    return render_template('person_index.html', people=enslaved)

@app.route('/people/<persId>')
def get_person(persId):
    person = models.Person.query.get(persId)
    name = parse_person_name(person)
    tribes = parse_person_descriptors(person, 'tribes')
    origins = parse_person_descriptors(person, 'origins')
    races = parse_person_descriptors(person, 'races')
    statuses = parse_person_descriptors(person, 'enslavements')
    vocations = parse_person_descriptors(person, 'vocations')
    titles = parse_person_descriptors(person, 'titles')
    relations = parse_person_relations(person)
    return render_template('person_display.html',
        name=name, refs = person.references,
        origins=origins, tribes=tribes, titles=titles,
        races=races, vocations=vocations, statuses=statuses,
        relations=relations)

@app.route('/source/<srcId>')
def get_source(srcId):
    return 'Foo:' + srcId

@app.route('/record/relationships/<recId>')
def edit_relationships(recId):
    rec = models.Reference.query.get(recId)
    return render_template('record_relationships.html', sec=rec)

@app.route('/data/sections/<secId>/relationships/')
def relationships_by_section(secId):
    rec = models.Reference.query.get(secId)
    entrants = [ { 'id': e.id, 'name': e.display_name() }
        for e in rec.referents ]
    relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
        for r in models.Role.query.all() ]
    ent_map = { e['id']: e['name'] for e in entrants }
    rel_map = { r['id']: r['name'] for r in relationships }
    store = [
        {
        'id': r.id,
        'data':
            { 
            'sbj': { 'name': ent_map[r.subject_id], 'id': r.subject_id },
            'rel': { 'name': rel_map[r.role_id], 'id': r.role_id },
            'obj': { 'name': ent_map[r.object_id], 'id': r.object_id }
            }
        }
        for e in rec.referents
            for r in e.as_subject
    ]
    data = { 'store': store, 'people': entrants,
        'relationships': relationships }
    return jsonify(data)

@app.route('/data/relationships/', methods=['POST'])
def create_relationship():
    data = request.get_json()
    existing = models.ReferentRelationship.query.filter_by(
        subject_id=data['sbj'], role_id=data['rel'],
        object_id=data['obj']).first()
    if not existing:
        relt = models.ReferentRelationship(
            subject_id=data['sbj'], role_id=data['rel'],
            object_id=data['obj'])
        db.session.add(relt)
        implied = relt.entailed_relationships()
        for i in implied:
            existing = models.ReferentRelationship.query.filter_by(
                subject_id=i.subject_id, role_id=i.role_id,
                object_id=i.object_id).first()
            if not existing:
                db.session.add(i)
        db.session.commit()
    return redirect(
        url_for('relationships_by_section', secId = data['section']),
        code=303 )

@app.route('/data/relationships/<relId>', methods=['DELETE'])
def delete_relationship(relId):
    data = request.get_json()
    existing = models.ReferentRelationship.query.get(relId)
    if existing:
        db.session.delete(existing)
        db.session.commit()
    return redirect(
        url_for('relationships_by_section', secId = data['section']),
        code=303 )

@app.route('/data/sections/<secId>/locations/')
def locations_by_section(secId):
    rec = models.Reference.query.get(secId)
    locations = [
        { 'id': l.id, 'name': l.location.name,
            'loc_id': l.location.id, 'loc_type_id': l.location_type.id }
        for l in rec.locations ]
    location_types = { lt.id: {'id': lt.id, 'name': lt.name }
        for lt in models.LocationType.query.all() }
    locations_by_type = {}
    for lt_id in location_types:
        query = db.session.query(
            models.ReferenceLocation.location_id,
            models.Location.name,
            models.ReferenceLocation.location_type_id,
            models.LocationType.name).\
            join("location").join("location_type").\
            filter(models.ReferenceLocation.location_type_id == lt_id).\
            distinct().all()
        res = [ { 'loc_id': r[0], 'label': r[1], 'loc_type_id': r[2],
                    'category': r[3] } for r in query ]
        locations_by_type[lt_id] = res
    data = { 'reference_locations': locations,
        'location_types': location_types,
        'locations_by_type': locations_by_type }
    print(data)
    return jsonify(data)