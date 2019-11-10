from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import dataserv
from .. import db, models, forms

import datetime as dt
import collections
from operator import itemgetter


@dataserv.before_request
@login_required
def before_request():
    pass


def stamp_edit(user, ref):
    edit = models.ReferenceEdit(reference_id=ref.id,
        user_id=user.id, timestamp=dt.datetime.utcnow())
    db.session.add(edit)
    db.session.commit()


@dataserv.route('/citations/', methods=['POST'])
@dataserv.route('/citations/<citeId>', methods=['PUT'])
def create_or_update_citation(citeId):
    if request.method == 'POST':
        cite = models.Citation()
    else:
        cite = models.Citation.query.get(refId)

    data = request.get_json()
    if not data['citation_type']['name']:
        cite.citation_type = models.CitationType.get_default()
    else:
        cite.citation_type = models.CitationType.query.filter_by(
            name=data['citation_type']['name'] ).first()
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
        now = dt.datetime.utcnow()
        cite.display = 'Document :: {}'.format(now.strftime('%Y %B %d'))
    else:
        vals = [ v[1] for v in sorted(citation_display) ]
        cite.display = ', '.join(vals + addendums)
    db.session.add(cite)
    db.session.commit()

    return jsonify({ 'citation': citation.to_dict() })


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


@dataserv.route('/references/', methods=['POST'])
@dataserv.route('/references/<refId>', methods=['PUT'])
def create_or_update_reference(refId=None):
    if request.method == 'POST':
        ref = models.Reference()
    else:
        ref = models.Reference.query.get(refId)

    data = request.get_json()
    ref.citation_id = data['citation']['id']
    if not data['reference_type']['name']:
        ref.reference_type = models.ReferenceType.get_default()
    else:
        ref.reference_type = models.ReferenceType.get_or_create(
            name=data['reference_type']['name'] )
    ref.national_context_id = data['national_context']['id']
    ref.transcription = data['transcription']
    ref.locations = [ models.ReferenceLocation(
        location=models.Location.get_or_create( name=loc['name'] ),
        location_type=models.LocationType.get_or_create(
                name=loc['location_type']['name']),
        location_rank=idx)
            for idx, loc in enumerate(data['locations']) ]
    ref.day = data['date']['day']
    ref.month = data['date']['month']
    ref.year = data['date']['year']
    ref.date_text = data['date']['date_text']
    try:
        ref.date = dt.datetime(year=ref.date or 1492, month=ref.month or 1,
            day=ref.day or 1)
    except:
        ref.date = None
    db.session.add(ref)
    db.session.commit()

    stamp_edit(current_user, ref)
    return jsonify({ 'reference': ref.to_dict() })


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
        'link': url_for('editor.edit_reference',
            citeId=citeId, refId=ref.id),
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