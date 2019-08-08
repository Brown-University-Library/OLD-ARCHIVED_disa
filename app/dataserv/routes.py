from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import dataserv
from .. import db, models, forms

import datetime
import collections
from operator import itemgetter


@dataserv.before_request
@login_required
def before_request():
    pass


def stamp_edit(user, ref):
    edit = models.ReferenceEdit(reference_id=ref.id,
        user_id=user.id, timestamp=datetime.datetime.utcnow())
    db.session.add(edit)
    db.session.commit()


@dataserv.route('/documents/', methods=['GET'])
@dataserv.route('/documents/<docId>', methods=['GET'])
def read_document_data(docId=None):
    data = { 'doc': {} }
    included = [ 'Book', 'Book Section', 'Document', 'Interview',
        'Journal Article', 'Magazine Article', 'Manuscript',
        'Newspaper Article', 'Thesis', 'Webpage' ]
    ct = models.CitationType.query.filter(
        models.CitationType.name.in_(included)).all()
    data['doc_types'] = [ { 'id': c.id, 'name': c.name } for c in ct ]
    if docId == None:
        return jsonify(data)
    doc = models.Citation.query.get(docId)
    data['doc']['id'] = doc.id
    data['doc']['citation'] = doc.display
    # data['doc']['zotero_id'] = doc.zotero_id   
    data['doc']['comments'] = doc.comments
    data['doc']['acknowledgements'] = doc.acknowledgements
    data['doc']['citation_type_id'] = doc.citation_type_id
    data['doc']['fields'] = { f.field.name: f.field_data for f in doc.citation_data }
    return jsonify(data)


@dataserv.route('/documents/', methods=['POST'])
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


@dataserv.route('/documents/', methods=['PUT'])
@dataserv.route('/documents/<citeId>', methods=['PUT'])
def update_citation(citeId):
    data = request.get_json()
    if citeId is None:
        return jsonify({})
    unspec = models.CitationType.query.filter_by(name='Document').first()
    data['citation_type_id'] = int(data['citation_type']) or unspec.id
    cite = models.Citation.query.get(citeId)
    cite.citation_type_id = data['citation_type']
    # doc.zotero_id = data['zotero_id']
    cite.comments = data['comments']
    cite.acknowledgements = data['acknowledgements']
    field_order_map = { f.zotero_field.name: f.rank
        for f in cite.citation_type.zotero_type.template_fields }
    citation_display = []
    cite.citation_data = []
    addendums = []
    for fieldData in data['citation_fields']:
        field = fieldData['name']
        val =  fieldData['value']
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

    citation = {
        'citation_id': cite.id,
        'display': cite.display,
        'acknowledgements': cite.acknowledgements,
        'comments': cite.comments,
        'citation_type': cite.citation_type.id,
        'citation_fields': [ { 'name': f.field.name, 'value': f.field_data }
            for f in cite.citation_data ]
    }
    return jsonify({ 'citation': citation })


@dataserv.route('/records/', methods=['GET'])
@dataserv.route('/records/<recId>', methods=['GET'])
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


@dataserv.route('/entrants/', methods=['GET'])
@dataserv.route('/entrants/<rntId>', methods=['GET'])
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

@dataserv.route('/records/', methods=['POST'])
@dataserv.route('/records/<refId>', methods=['PUT'])
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


@dataserv.route('/citations/<citeId>/references/')
@dataserv.route('/citations/<citeId>/references/<refId>',
    methods=['DELETE'])
def delete_citation_reference(citeId, refId=None):
    existing = models.Reference.query.get(refId)
    if existing:
        cite = existing.citation
        db.session.delete(existing)
        db.session.commit()
    cite = models.Citation.query.get(citeId)
    references = [
        { 'id': ref.id,
        'reference_type': ref.reference_type.name,
        'last_edit': ref.last_edit().timestamp.strftime("%Y-%m-%d")
        } for ref in cite.references ]
    return jsonify( {'references': references } )


@dataserv.route('/reference/<refId>', methods=['DELETE'])
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
    db.session.add(name)
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

@dataserv.route('/entrants/', methods=['POST'])
@dataserv.route('/entrants/<rntId>', methods=['PUT', 'DELETE'])
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

@dataserv.route('/entrants/details/', methods=['PUT'])
@dataserv.route('/entrants/details/<rntId>', methods=['PUT'])
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
        { 'redirect': url_for('editor.edit_record', recId=rnt.reference_id) })

@dataserv.route('/sections/<refId>/relationships/')
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

@dataserv.route('/relationships/', methods=['POST'])
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
        url_for('dataserv.relationships_by_reference', refId = ref.id),
        code=303 )

@dataserv.route('/relationships/<relId>', methods=['DELETE'])
def delete_relationship(relId):
    data = request.get_json()
    ref = models.Reference.query.get(data['section'])
    existing = models.ReferentRelationship.query.get(relId)
    if existing:
        db.session.delete(existing)
        db.session.commit()
        stamp_edit(current_user, ref)
    return redirect(
        url_for('dataserv.relationships_by_reference', refId = ref.id),
        code=303 )