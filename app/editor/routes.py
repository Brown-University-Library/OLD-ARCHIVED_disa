from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import editor
from .. import db, models, forms

import datetime
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


@editor.route('/editor', methods=['GET'])
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


@editor.route('/editor/citations/<citeId>')
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
                'reference_type': ref.reference_type.name,
                'last_edit':
                    ref.last_edit().timestamp.strftime("%Y-%m-%d")
            } for ref in cite.references ]
    config['citation'] = citation
    return render_template('editor/citation.html', page_config=config)


@editor.route('/editor/records')
@editor.route('/editor/records/<recId>')
def edit_record(recId=None):
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


@editor.route('/editor/person')
@editor.route('/editor/person/<entId>')
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