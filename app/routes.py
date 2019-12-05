import collections, datetime, json, logging, pprint

import flask

from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db, models, forms
from app.lib import version_helper

# import datetime
# import collections
# import logging, pprint


log = logging.getLogger( __name__ )
log.info( 'routes.py logging working' )


def stamp_edit(user, ref):
    edit = models.ReferenceEdit(reference_id=ref.id,
        user_id=user.id, timestamp=datetime.datetime.utcnow())
    db.session.add(edit)
    db.session.commit()

@app.route('/')
def browse():
    log.debug( 'starting route `/`' )
    return render_template('browse.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    log.debug( 'starting login()' )
    log.debug( f'current_user, ```{current_user.__dict__}```' )
    if current_user.is_authenticated:
        log.debug( 'user is authenticated' )
        return redirect(url_for('index_documents'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        log.debug( 'form `form.validate_on_submit()` was True' )
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('editor_index')
        user.last_login = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        return redirect(next_page)
    log.debug( 'i guess form `form.validate_on_submit()` was False' )
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('browse'))

def sort_documents(wrappedDocs):
    merge = {}
    for w in wrappedDocs:
        if w[0].id not in merge or merge[w[0].id][0] < w[2]:
            merge[w[0].id] = (w[2], w[3], w[0])
        else:
            continue
    return sorted([ merge[w] for w in merge], reverse=True)

@app.route('/editor', methods=['GET'])
@login_required
def editor_index():
    log.debug( 'starting editor_index' )
    all_cites = models.Citation.query.all()
    no_refs = [ (cite, current_user.id, datetime.datetime.now(), '')
        for cite in all_cites if len(cite.references) == 0 ]
    has_refs = [ cite for cite in all_cites if len(cite.references) > 0 ]
    wrapped_refs = [ (cite, edit.user_id, edit.timestamp, edit.edited_by.email)
                        for cite in has_refs
                            for ref in cite.references
                                for edit in ref.edits ]
    user_cites = [ wrapped for wrapped in wrapped_refs
                    if wrapped[1] == current_user.id ]
    srtd_all = sort_documents(no_refs + wrapped_refs)
    srtd_user = sort_documents(user_cites)
    return render_template('document_index.html',
        user_documents=srtd_user, documents=srtd_all)

@app.route('/editor/documents')
@app.route('/editor/documents/<citeId>')
@login_required
def edit_citation(citeId=None):
    log.debug( 'starting edit_citation' )
    included = [ 'Book', 'Book Section', 'Document', 'Interview',
        'Journal Article', 'Magazine Article', 'Manuscript',
        'Newspaper Article', 'Thesis', 'Webpage' ]
    ct = models.CitationType.query.filter(
        models.CitationType.name.in_(included)).all()
    ct_fields = {
        c.id: [ {   'name': f.zotero_field.name,
                    'rank': f.rank,
                    'display': f.zotero_field.display_name }
            for f in c.zotero_type.template_fields ]
                for c in ct }
    add_pages_field = ['Document', 'Book', 'Thesis', 'Manuscript']
    for c in ct:
        if c.name in add_pages_field:
            pages = { 'name': 'pages', 'display':'Pages' }
            fields = ct_fields[c.id]
            date = [ f for f in fields if f['name'] == 'date'][0]
            pages['rank'] = date['rank'] + 1
            for f in fields:
                if f['rank'] > date['rank']:
                    f['rank'] += 1
            ct_fields[c.id].append(pages)
    if not citeId:
        return render_template('document_edit.html',
            doc=None, ct_fields=ct_fields )
    cite = models.Citation.query.get(citeId)
    # citation_data = { f.field.name: f.field_data for f in cite.citation_data }
    return render_template('document_edit.html',
        doc=cite, ct_fields=ct_fields )

@app.route('/editor/records')
@app.route('/editor/records/<recId>')
@login_required
def edit_record(recId=None):
    log.debug( 'starting edit_record' )
    locs = models.ReferenceLocation.query.all()
    rec_types = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
        for rt in models.ReferenceType.query.all() ]
    roles = [ { 'id': role.id, 'value': role.name, 'name': role.name }
        for role in models.Role.query.all() ]
    natl_ctxs = [ { 'id': rt.id, 'value': rt.name, 'name': rt.name }
        for rt in models.NationalContext.query.all() ]
    uniq_cols = { (l.location.name, l.location_id)
        for l in locs if l.location_rank == 0 }
    uniq_town = { (l.location.name, l.location_id)
        for l in locs if l.location_rank == 1 }
    uniq_addl = { (l.location.name, l.location_id)
        for l in locs if l.location_rank == 2 and l.location_id is not None}
    col_state = [ {'id': loc[1], 'value': loc[0],'label': loc[0] }
        for loc in uniq_cols ]
    towns = [ {'id': loc[1], 'value': loc[0],'label': loc[0] }
        for loc in uniq_town ]
    addl_loc = [ {'id': loc[1], 'value': loc[0],'label': loc[0] }
        for loc in uniq_addl ]
    if not recId:
        doc_id = request.args.get('doc')
        doc = models.Citation.query.get(doc_id)
        return render_template(
            'record_edit.html',  rec=None, doc=doc,
            rec_types=rec_types, roles=roles,
            natl_ctxs=natl_ctxs, col_state=col_state,
            towns=towns, addl_loc=addl_loc)
    rec = models.Reference.query.get(recId)
    return render_template(
        'record_edit.html', rec=rec, doc=rec.citation,
            rec_types=rec_types, roles=roles,
            natl_ctxs=natl_ctxs, col_state=col_state,
            towns=towns, addl_loc=addl_loc)

@app.route('/editor/person')
@app.route('/editor/person/<entId>')
@login_required
def edit_entrant(entId=None):
    log.debug( 'starting edit_entrant' )
    nametypes = [ { 'id': role.id, 'value': role.name, 'label': role.name }
        for role in models.NameType.query.all()]
    roles = [ { 'id': role.id, 'value': role.name, 'label': role.name }
        for role in models.Role.query.all()]
    # desc_data = models.Description.query.all()
    origins = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
        for loc in models.Location.query.all()]
    races = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
        for loc in models.Race.query.all()]
    tribes = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
        for loc in models.Tribe.query.all()]
    titles = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
        for loc in models.Title.query.all()]
    vocations = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
        for loc in models.Vocation.query.all()]
    enslavements = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
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
@login_required
def read_document_data(docId=None):
    log.debug( f'starting "data/documents/" GET processing; docId, `{docId}`' )
    data = { 'doc': {} }
    included = [ 'Book', 'Book Section', 'Document', 'Interview',
        'Journal Article', 'Magazine Article', 'Manuscript',
        'Newspaper Article', 'Thesis', 'Webpage' ]
    ct = models.CitationType.query.filter(
        models.CitationType.name.in_(included)).all()
    log.debug( f'ct, ```{ct}```' )
    data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
    if docId == None:
        log.debug( f'returning data for docID equals None, ```{pprint.pformat(data)}```' )
        return jsonify(data)
    if docId == 'copy':
        last_edit = edit = models.ReferenceEdit.query.filter_by(
            user_id=current_user.id).order_by(
            models.ReferenceEdit.timestamp.desc()).first()
        log.debug( f'last_edit, ```{last_edit}```' )
        if not last_edit or not last_edit.edited:
            log.debug( f'returning data for docID equals copy with no last_edit, ```{pprint.pformat(data)}```' )
            return jsonify(data)
        doc = models.Citation.query.get(last_edit.edited.citation_id)
    else:
        doc = models.Citation.query.get(docId)
        data['doc']['id'] = doc.id
    data['doc']['citation'] = doc.display
    # data['doc']['zotero_id'] = doc.zotero_id
    data['doc']['comments'] = doc.comments
    data['doc']['acknowledgements'] = doc.acknowledgements
    if doc.citation_type_id not in [ c.id for c in ct ]:
        doctype_document = [ c for c in ct if c.name == 'Document'][0]
        data['doc']['citation_type_id'] = doctype_document.id
    else:
        data['doc']['citation_type_id'] = doc.citation_type_id
    data['doc']['fields'] = { f.field.name: f.field_data for f in doc.citation_data }
    log.debug( f'returning data for given docID, ```{pprint.pformat(data)}```' )
    return jsonify(data)

@app.route('/data/documents/', methods=['POST'])
@login_required
def create_citation():
    data = request.get_json()
    unspec = models.CitationType.query.filter_by(name='Document').first()
    data['citation_type_id'] = data['citation_type_id'] or unspec.id
    cite = models.Citation(citation_type_id=data['citation_type_id'],
        comments=data['comments'], acknowledgements=data['acknowledgements'])
    db.session.add(cite)
    db.session.commit()
    field_order_map = { f.zotero_field.name: f.rank
        for f in cite.citation_type.zotero_type.template_fields }
    citation_display = []
    for field, val in data['fields'].items():
        if val == '':
            continue
        zfield = models.ZoteroField.query.filter_by(name=field).first()
        cfield = models.CitationField(citation_id=cite.id,
            field_id=zfield.id, field_data=val)
        citation_display.append( (field_order_map[zfield.name], val) )
        db.session.add(cfield)
    if len(citation_display) == 0:
        now = datetime.datetime.utcnow()
        cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
    else:
        vals = [ v[1] for v in sorted(citation_display) ]
        cite.display = ' '.join(vals)
    db.session.add(cite)
    db.session.commit()
    return jsonify(
        { 'redirect': url_for('edit_citation', citeId=cite.id) })

@app.route('/data/documents/', methods=['PUT'])
@app.route('/data/documents/<citeId>', methods=['PUT'])
@login_required
def update_citation_data(citeId):
    data = request.get_json()
    if citeId is None:
        return jsonify({})
    unspec = models.CitationType.query.filter_by(name='Document').first()
    data['citation_type_id'] = data['citation_type_id'] or unspec.id
    cite = models.Citation.query.get(citeId)
    cite.citation_type_id = data['citation_type_id']
    # doc.zotero_id = data['zotero_id']
    cite.comments = data['comments']
    cite.acknowledgements = data['acknowledgements']
    field_order_map = { f.zotero_field.name: f.rank
        for f in cite.citation_type.zotero_type.template_fields }
    citation_display = []
    cite.citation_data = []
    addendums = []
    for field, val in data['fields'].items():
        if val == '':
            continue
        zfield = models.ZoteroField.query.filter_by(name=field).first()
        cfield = models.CitationField(citation_id=cite.id,
            field_id=zfield.id, field_data=val)
        try:
            citation_display.append( (field_order_map[zfield.name], val) )
        except KeyError:
            addendums.append(val)
        db.session.add(cfield)
    if len(citation_display) == 0:
        now = datetime.datetime.utcnow()
        cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
    else:
        vals = [ v[1] for v in sorted(citation_display) ]
        cite.display = ', '.join(vals + addendums)
    db.session.add(cite)
    db.session.commit()

    data = { 'doc': {} }
    included = [ 'Book', 'Book Section', 'Document', 'Interview',
        'Journal Article', 'Magazine Article', 'Manuscript',
        'Newspaper Article', 'Thesis', 'Webpage' ]
    ct = models.CitationType.query.filter(
        models.CitationType.name.in_(included)).all()
    data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
    data['doc']['id'] = cite.id
    data['doc']['citation'] = cite.display
    # data['doc']['zotero_id'] = doc.zotero_id
    data['doc']['comments'] = cite.comments
    data['doc']['acknowledgements'] = cite.acknowledgements
    data['doc']['citation_type_id'] = cite.citation_type_id
    return jsonify(data)

@app.route('/data/records/', methods=['GET'])
@app.route('/data/records/<recId>', methods=['GET'])
@login_required
def read_record_data(recId=None):
    data = { 'rec': {}, 'entrants': [] }
    if recId == None:
        return jsonify(data)
    rec = models.Reference.query.get(recId)
    data['rec']['id'] = rec.id
    data['rec']['date'] = None
    if rec.date:
        data['rec']['date'] = '{}/{}/{}'.format(rec.date.month,
            rec.date.day, rec.date.year)
    data['rec']['locations'] = [
        { 'label':l.location.name, 'value':l.location.name,
            'id': l.location.id } for l in rec.locations ]
    data['rec']['transcription'] = rec.transcription
    data['rec']['national_context'] = rec.national_context_id
    data['rec']['record_type'] = {'label': rec.reference_type.name,
        'value': rec.reference_type.name, 'id':rec.reference_type.id }
    data['entrants'] = [
        {
            'name_id': ent.primary_name.id,
            'first': ent.primary_name.first,
            'last': ent.primary_name.last,
            'id': ent.id,
            'person_id': ent.person_id,
            'roles': [ role.id for role in ent.roles ]
        }
            for ent in rec.referents ]
    data['rec']['header'] = '{}'.format(
        rec.reference_type.name or '').strip()
    return jsonify(data)

@app.route('/data/entrants/', methods=['GET'])
@app.route('/data/entrants/<rntId>', methods=['GET'])
@login_required
def read_referent_data(rntId=None):
    data = { 'ent': {} }
    if rntId == None:
        return jsonify(data)
    rnt = models.Referent.query.get(rntId)
    data['ent']['id'] = rnt.id
    data['ent']['names'] = [
        { 'first': n.first, 'last': n.last,
            'name_type': n.name_type.name,
            'id': n.id } for n in rnt.names ]
    data['ent']['age'] = rnt.age
    data['ent']['sex'] = rnt.sex
    data['ent']['races'] = [
        { 'label': r.name, 'value': r.name,
            'id': r.name } for r in rnt.races ]
    data['ent']['tribes'] = [
        { 'label': t.name, 'value': t.name,
            'id': t.name } for t in rnt.tribes ]
    data['ent']['origins'] = [
        { 'label': o.name, 'value': o.name,
            'id': o.name } for o in rnt.origins ]
    data['ent']['titles'] = [
        { 'label': t.name, 'value': t.name,
            'id': t.name } for t in rnt.titles ]
    data['ent']['vocations'] = [
        { 'label': v.name, 'value': v.name,
            'id': v.name } for v in rnt.vocations ]
    data['ent']['enslavements'] = [
        { 'label': e.name, 'value': e.name,
            'id': e.name } for e in rnt.enslavements ]
    return jsonify(data)


def get_or_create_type(typeData, typeModel):
    if typeData['id'] == -1:
        new_type = typeModel(name=typeData['value'])
        db.session.add(new_type)
        db.session.commit()
        return new_type
    elif typeData == '' or typeData['id'] == 0:
        unspec = typeModel.query.filter_by(name='Unspecified').first()
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
        elif loc['id'] == 0:
            continue
        else:
            location = models.Location.query.get(loc['id'])
        locations.append(location)
    clny_state = models.LocationType.query.filter_by(name='Colony/State').first()
    city = models.LocationType.query.filter_by(name='City').first()
    locale = models.LocationType.query.filter_by(name='Locale').first()
    loc_types = [ clny_state, city, locale ]
    for loc in locations:
        rec_loc = models.ReferenceLocation()
        rec_loc.reference = recObj
        rec_loc.location = loc
        idx = locations.index(loc)
        rec_loc.location_rank = idx
        if idx < len(loc_types):
            rec_loc.location_type = loc_types[idx]
        db.session.add(rec_loc)
    db.session.commit()
    return recObj

@app.route('/data/records/', methods=['POST'])
@app.route('/data/records/<refId>', methods=['PUT'])
@login_required
def update_reference_data(refId=None):
    data = request.get_json()
    reference_type = get_or_create_type(
        data['record_type'], models.ReferenceType)
    if request.method == 'POST':
        ref = models.Reference()
        ref.citation_id = data['citation_id']
        ref.national_context_id = data['national_context']
        ref.reference_type_id = reference_type.id
        db.session.add(ref)
        db.session.commit()
    else:
        ref = models.Reference.query.get(refId)
    ref.locations = []
    ref = process_record_locations(data['locations'], ref)
    try:
        ref.date = datetime.datetime.strptime(data['date'], '%m/%d/%Y')
    except:
        ref.date = None
    ref.reference_type_id = reference_type.id
    ref.national_context_id = data['national_context']
    ref.transcription = data['transcription']
    db.session.add(ref)
    db.session.commit()

    stamp_edit(current_user, ref)
    if request.method == 'POST':
        return jsonify(
            { 'redirect': url_for('edit_record', recId=ref.id) })
    data = { 'rec': {} }
    data['rec']['id'] = ref.id
    data['rec']['date'] = ''
    if ref.date:
        data['rec']['date'] = '{}/{}/{}'.format(ref.date.month,
            ref.date.day, ref.date.year)
    if request.method == 'POST':
        data['entrants'] = []
        data['rec']['header'] = '{}'.format(
            ref.reference_type.name or '').strip()
    data['rec']['citation'] = ref.citation.id
    data['rec']['transcription'] = ref.transcription
    data['rec']['national_context'] = ref.national_context_id
    data['rec']['locations'] = [
        { 'label':l.location.name, 'value':l.location.name,
            'id': l.location.id } for l in ref.locations ]
    data['rec']['record_type'] = {'label': ref.reference_type.name,
        'value': ref.reference_type.name, 'id':ref.reference_type.id }
    return jsonify(data)

@app.route('/data/reference/<refId>', methods=['DELETE'])
def delete_reference(refId):
    existing = models.Reference.query.get(refId)
    if existing:
        cite = existing.citation
        db.session.delete(existing)
        db.session.commit()
        return read_document_data(cite.id)
    return redirect(url_for('editor_index'), code=404)

def update_referent_name(data):
    if data['id'] == 'name':
        name = models.ReferentName()
    else:
        name = models.ReferentName.query.get(data['id'])
    name.first = data['first']
    name.last = data['last']
    given = models.NameType.query.filter_by(name='Given').first()
    name.name_type_id = data.get('name_type', given.id)
    return name

def get_or_create_referent_attribute(data, attrModel):
    existing = attrModel.query.filter_by(name=data['name']).first()
    if not existing:
        new_attr = attrModel(name=data['name'])
        db.session.add(new_attr)
        db.session.commit()
        return new_attr
    else:
        return existing

@app.route('/data/entrants/', methods=['POST'])
@app.route('/data/entrants/<rntId>', methods=['PUT', 'DELETE'])
@login_required
def update_referent(rntId=None):
    if request.method == 'DELETE':
        rnt = models.Referent.query.get(rntId)
        ref = rnt.reference
        rels_as_sbj = models.ReferentRelationship.query.filter_by(
            subject_id=rnt.id).all()
        rels_as_obj = models.ReferentRelationship.query.filter_by(
            object_id=rnt.id).all()
        for r in rels_as_sbj:
            db.session.delete(r)
        for r in rels_as_obj:
            db.session.delete(r)
        db.session.delete(rnt)
        db.session.commit()

        stamp_edit(current_user, ref)

        return jsonify( { 'id': rntId } )
    data = request.get_json()
    if request.method == 'POST':
        prs = models.Person()
        db.session.add(prs)
        db.session.commit()
        rnt = models.Referent(reference_id=data['record_id'])
        rnt.person = prs
    if request.method == 'PUT':
        rnt = models.Referent.query.get(rntId)
    primary_name = update_referent_name(data['name'])
    rnt.names.append(primary_name)
    rnt.primary_name = primary_name
    if request.method == 'POST':
        prs.first_name = primary_name.first
        prs.last_name = primary_name.last
        db.session.add(prs)
    rnt.roles = [ get_or_create_referent_attribute(a, models.Role)
        for a in data['roles'] ]
    db.session.add(rnt)
    db.session.commit()

    stamp_edit(current_user, rnt.reference)

    return jsonify({
        'name_id': rnt.primary_name.id,
        'first': rnt.primary_name.first,
        'last': rnt.primary_name.last,
        'id': rnt.id,
        'person_id': rnt.person_id,
        'roles': [ role.id for role in rnt.roles ] })

@app.route('/data/entrants/details/', methods=['PUT'])
@app.route('/data/entrants/details/<rntId>', methods=['PUT'])
@login_required
def update_referent_details(rntId):
    rnt = models.Referent.query.get(rntId)
    data = request.get_json()
    rnt.names = [ update_referent_name(n) for n in data['names'] ]
    rnt.age = data['age']
    rnt.sex = data['sex']
    rnt.primary_name = rnt.names[0]
    rnt.races = [ get_or_create_referent_attribute(a, models.Race)
        for a in data['races'] ]
    rnt.tribes = [ get_or_create_referent_attribute(a, models.Tribe)
        for a in data['tribes'] ]
    rnt.origins = [ get_or_create_referent_attribute(a, models.Location)
        for a in data['origins'] ]
    rnt.titles = [ get_or_create_referent_attribute(a, models.Title)
        for a in data['titles'] ]
    rnt.enslavements = [ get_or_create_referent_attribute(
        a, models.EnslavementType)
            for a in data['statuses'] ]
    rnt.vocations = [ get_or_create_referent_attribute(
        a, models.Vocation)
            for a in data['vocations'] ]
    db.session.add(rnt)
    db.session.commit()

    stamp_edit(current_user, rnt.reference)

    return jsonify(
        { 'redirect': url_for('edit_record', recId=rnt.reference_id) })

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

# @app.route('/people/')
# def person_index():
#     log.debug( 'starting people' )
#     people = [ p for p in models.Person.query.all() if p.references != [] ]
#     return render_template('person_index.html', people=people)

# @app.route('/people/')  # works -- looking for quicker way below
# def person_index():
#     log.debug( 'starting people' )
#     # people = [ p for p in models.Person.query.all() if p.references != [] ]
#     people = []
#     all_people = models.Person.query.all()
#     # people = all_people[1:]
#     for person in all_people:
#         log.debug( f'person.__dict__ initially, ```{person.__dict__}```' )
#         races = parse_person_descriptors(person, 'races')
#         log.debug( f'races, ```{races}```' )
#         person.races = races
#         log.debug( f'person.__dict__ now, ```{person.__dict__}```' )
#         gender = None
#         for ref in person.references:
#             gender = ref.sex
#             break
#         person.gender = gender
#         temp_str = f'race, `{races}`; gender, `{gender}`'
#         person.last_name = f'{person.last_name} ({temp_str})'
#         log.debug( f'person.__dict__ finally, ```{person.__dict__}```' )
#         people.append( person )
#         # break
#     return render_template('person_index.html', people=people)

# @app.route('/people/')
# def person_index():
#     log.debug( 'starting people' )
#     people = []
#     for (prsn, rfrnt) in db.session.query(models.Person, models.Referent).filter(models.Person.id==models.Referent.id).all():
#         gender = rfrnt.sex
#         age = rfrnt.age
#         temp_str = f'age, `{age}`; gender, `{gender}`'
#         prsn.last_name = f'{prsn.last_name} ({temp_str})'
#         people.append( prsn )
#     ps = people[0:2]
#     log.debug( f'ps, ```{ps}```' )
#     p = people[1]
#     log.debug( f'p.__dict__, ```{p.__dict__}```' )
#     return render_template('person_index.html', people=people)

# @app.route('/people/')
# def person_index():
#     log.debug( 'starting people' )
#     people = []
#     refs = []
#     for (prsn, rfrnt) in db.session.query(models.Person, models.Referent).filter(models.Person.id==models.Referent.id).all():
#         sex = rfrnt.sex if rfrnt.sex else "None"
#         age = rfrnt.age if rfrnt.age else "None"
#         race = None
#         try:
#             race = rfrnt.races[0].name
#         except:
#             log.exception( 'well, that did not work!' )
#         race = race if race else "None"
#         # temp_str = f'age, `{age}`; gender, `{gender}`'
#         temp_demographic = f'age, `{age}`; sex, `{sex}`; race, `{race}`'
#         prsn.tmp_dmgrphc = temp_demographic
#         # prsn.last_name = f'{prsn.last_name} ({temp_str})'
#         people.append( prsn )
#         refs.append( rfrnt )
#     p = people[1]
#     log.debug( f'p.__dict__, ```{p.__dict__}```' )
#     r = refs[1]
#     log.debug( f'r.__dict__, ```{r.__dict__}```' )
#     log.debug( f'race, r.races[0].__dict__, ```{r.races[0].__dict__}```' )
#     return render_template('person_index.html', people=people)


@app.route('/people/')
def person_index():
    log.debug( 'starting people' )
    people = []
    for (prsn, rfrnt) in db.session.query( models.Person, models.Referent ).filter( models.Person.id==models.Referent.id ).all():
        sex = rfrnt.sex if rfrnt.sex else "Not Listed"
        age = rfrnt.age if rfrnt.age else "Not Listed"
        race = None
        try:
            race = rfrnt.races[0].name
        except:
            log.debug( 'no race-name; races, ```{rfrnt.races}```' )
        race = race if race else "Not Listed"
        temp_demographic = f'age, `{age}`; sex, `{sex}`; race, `{race}`'
        # prsn.tmp_dmgrphc = temp_demographic
        # prsn.last_name = f'{prsn.last_name} ({temp_str})'
        prsn.calc_sex = sex
        prsn.calc_age = age
        prsn.calc_race = race
        people.append( prsn )
    p = people[1]
    log.debug( f'p.__dict__, ```{p.__dict__}```' )
    return render_template('person_index.html', people=people)


@app.route('/people/<persId>')
def get_person(persId):
    log.debug( 'starting get_person' )
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
        name=name, dbId=persId, refs = person.references,
        origins=origins, tribes=tribes, titles=titles,
        races=races, vocations=vocations, statuses=statuses,
        relations=relations)

@app.route('/source/<srcId>')
def get_source(srcId):
    return redirect(url_for('edit_record', recId=srcId))

@app.route('/record/relationships/<recId>')
@login_required
def edit_relationships(recId):
    log.debug( 'starting edit_relationships' )
    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rec = models.Reference.query.get(recId)
    # return render_template('record_relationships.html', sec=rec)
    base_segment = request.script_root
    return render_template('record_relationships.html', sec=rec, base_url_segment=base_segment )

@app.route('/data/sections/<refId>/relationships/')
@login_required
def relationships_by_reference(refId):
    ref = models.Reference.query.get(refId)
    referents = [ { 'id': e.id, 'name': e.display_name() }
        for e in ref.referents ]
    relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
        for r in models.Role.query.all()
        if r.name_as_relationship is not None ]
    rnt_map = { f['id']: f['name'] for f in referents }
    rel_map = { r['id']: r['name'] for r in relationships }
    store = [
        {
        'id': r.id,
        'data':
            {
            'sbj': { 'name': rnt_map[r.subject_id], 'id': r.subject_id },
            'rel': { 'name': rel_map[r.role_id], 'id': r.role_id },
            'obj': { 'name': rnt_map[r.object_id], 'id': r.object_id }
            }
        }
        for f in ref.referents
            for r in f.as_subject
    ]
    data = { 'store': store, 'people': referents,
        'relationships': relationships }
    return jsonify(data)

@app.route('/data/relationships/', methods=['POST'])
@login_required
def create_relationship():
    data = request.get_json()
    ref = models.Reference.query.get(data['section'])
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
        stamp_edit(current_user, ref)
    return redirect(
        url_for('relationships_by_reference', refId = ref.id),
        code=303 )

@app.route('/data/relationships/<relId>', methods=['DELETE'])
@login_required
def delete_relationship(relId):
    data = request.get_json()
    ref = models.Reference.query.get(data['section'])
    existing = models.ReferentRelationship.query.get(relId)
    if existing:
        db.session.delete(existing)
        db.session.commit()
        stamp_edit(current_user, ref)
    return redirect(
        url_for('relationships_by_reference', refId = ref.id),
        code=303 )


# ===========================
# for development convenience
# ===========================


@app.route( '/version' )
def version():
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = version_helper.get_commit()
    branch = version_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = version_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    # return jsonify( context_dct )
    return flask.current_app.response_class( output, mimetype='application/json' )


@app.route( '/error_check' )
def error_check():
    """ For an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug( f'TEMP: flask.request, ```{pprint.pformat(request.__dict__)}```' )
    log.debug( f'flask.request.host, ```{pprint.pformat(request.host)}```' )
    if request.host[0:9] == '127.0.0.1':
        1/0
    else:
        return '<div>404 / Not Found</div>'
