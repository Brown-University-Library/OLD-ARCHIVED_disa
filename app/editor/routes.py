from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import editor
from .. import db, models, forms

import datetime
import calendar
import collections
from operator import itemgetter


@editor.before_request
@login_required
def before_request():
    pass


def sort_documents(wrappedDocs):
    merge = {}
    for w in wrappedDocs:
        if w[0].id not in merge or merge[w[0].id][0] < w[2]:
            merge[w[0].id] = (w[2], w[3], w[0])
        else:
            continue
    return sorted([ merge[w] for w in merge], reverse=True)


@editor.route('', methods=['GET'])
def editor_index():
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


@editor.route('/citations/<citeId>')
def edit_citation(citeId='new'):
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
    config = {
        'citationtype_fields': {
            str(cid): sorted(ct_fields[cid], key=itemgetter('rank'))
                for cid in ct_fields },
        'citation_types': [
            { 'id': c.id, 'name': c.name} for c in ct ],
        'references': []
    }
    citation = {
        'citation_id': '',
        'display': '',
        'acknowledgements': '',
        'comments': '',
        'citation_type': '',
        'citation_fields': []
    }
    default = [ c for c in ct if c.name == 'Document'][0]
    if citeId == 'new':
        citation['citation_id'] = citeId
        citation['citation_type'] = default.id
    else:
        cite = models.Citation.query.get(citeId)
        citation['citation_id'] = cite.id
        citation['display'] = cite.display
        citation['comments'] = cite.comments
        citation['acknowledgements'] = cite.acknowledgements
        if cite.citation_type.id not in { c['id'] for c in config['citation_types'] }:
            citation['citation_type'] = default.id
        else:
            citation['citation_type'] = cite.citation_type.id
        citation['citation_fields'] = [
            { 'name': f.field.name, 'value': f.field_data }
                for f in cite.citation_data ]
        config['references'] = [ { 'id': ref.id,
                'link': url_for('editor.edit_reference',
                    citeId=citeId, refId=ref.id),
                'reference_type': ref.reference_type.name,
                'last_edit':
                    ref.last_edit().timestamp.strftime("%Y-%m-%d")
            } for ref in cite.references ]
    config['citation'] = citation
    config['endpoints'] = {
        'updateCitation': url_for('dataserv.update_citation', citeId=citeId),
        'createCitation': url_for('dataserv.create_citation'),
        'newReference': url_for('editor.edit_reference',
            citeId=citeId, refId='new'),
        'deleteReference': url_for('dataserv.delete_citation_reference',
            citeId=citeId, refId=None)
    }
    return render_template('editor/citation.html', page_config=config)


@editor.route('/citations/<citeId>/references/<refId>')
def edit_reference(citeId, refId='new'):
    ref_types = [ rt.to_dict() for rt in models.ReferenceType.query.all() ]
    roles = [ role.to_dict() for role in models.Role.query.all() ]
    natl_ctxs = [ nc.to_dict() for nc in models.NationalContext.query.all() ]
    loc_types = [ lt.to_dict() for lt in models.LocationType.query.all() ]

    type_col_state = models.LocationType.query.filter_by(name="Colony/State").first()
    type_city = models.LocationType.query.filter_by(name="City").first()
    type_locale = models.LocationType.query.filter_by(name="Locale").first()
    # to do: assign all ReferenceLocations a LocationType
    col_states = models.Location.query.filter(
        models.Location.references.any(location_type_id=type_col_state.id)).all()
    cities = models.Location.query.filter(
        models.Location.references.any(location_type_id=type_city.id)).all()
    locales = models.Location.query.filter(
        models.Location.references.any(location_type_id=type_locale.id)).all()

    unknown_date = {'value': 0, 'label': 'Unknown' }
    months = [ unknown_date ]
    months.extend( [ {'value': m, 'label': calendar.month_name[m] }
        for m in range(1,13) ] )
    years = [ unknown_date ]
    years.extend( [ {'value': y, 'label': y } for y in range(1492,1900) ] )
    days = [ unknown_date ] 
    days.extend( [ {'value': d, 'label': d } for d in range(1,32) ] )

    config = {
        'data': {},
        'location_types': { lt['name']: lt['id'] for lt in loc_types },
        'national_contexts': natl_ctxs,
        'date': { 'years': years, 'months': months, 'days': days },
        'tags': roles,
        'reference_types': ref_types,
        'colony_states': [ l.to_dict() for l in col_states ],
        'cities': [ l.to_dict() for l in cities ],
        'locales': [ l.to_dict() for l in locales ],
    }

    if refId == 'new':
        config['data']['reference'] = models.Reference.to_dict()
    else:
        ref = models.Reference.query.get(refId)
        config['data']['reference'] = ref.to_dict()

        display = {
            'header': ref.reference_type.name,
            'fields': [
                {'field': 'SOURCE', 'data': ref.citation.display },
                {'field': 'DESCRIPTION', 'data': ref.reference_type.name },
                {'field': 'NATIONAL CONTEXT', 'data': ref.national_context.name },
                {'field': 'COLONY/STATE', 'data':  [ l.location.name
                    for l in ref.locations
                        if l.location_type_id == type_col_state.id ][:1] or 'None' },
                {'field': 'CITY', 'data': [ l.location.name
                    for l in ref.locations
                        if l.location_type_id == type_city.id ][:1] or 'None' },
                {'field': 'LOCALE', 'data': [ l.location.name
                    for l in ref.locations 
                        if l.location_type_id == type_locale.id ][:1] or 'None' },
                {'field': 'DATE', 'data': ref.date.strftime("%B %d, %Y")
                    if ref.date else 'None' },
                {'field': 'TRANSCRIPTION', 'data': ref.transcription[:200] },
            ]
        }
        config['data']['display'] = display

    config['endpoints'] = {
        'updateReference': url_for('dataserv.create_or_update_reference', refId=None),
    }
    return render_template('editor/reference.html', config=config)


@editor.route('/person')
@editor.route('/person/<entId>')
def edit_entrant(entId=None):
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


@editor.route('/record/relationships/<recId>')
def edit_relationships(recId):
    rec = models.Reference.query.get(recId)
    return render_template('record_relationships.html', sec=rec)