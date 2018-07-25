from app import models

import collections
import datetime
import json

def process_reference(entrant):
    rec = entrant.record
    locs = [ (loc.location_rank, loc.location.name)
                for loc in rec.locations ]
    ref_data = {
        'roles': collections.defaultdict(list),
        'date': {
            'year': rec.date.year,
            'month': rec.date.month,
            'day': rec.date.day
        },
        'locations': [ l[1] for l in sorted(locs, reverse=True) ],
        'comments': rec.comments
    }
    if entrant.description:
        ref_data['description'] = {
            'tribe': entrant.description.tribe,
            'sex': entrant.description.sex,
            'origin': entrant.description.origin,
            'vocation': entrant.description.vocation,
            'age': entrant.description.age,
            'race': entrant.description.race
        }
    for role in entrant.roles:
        ref_data['roles'][role.name] = []
    ers = entrant.as_subject
    for er in ers:
        role = er.related_as.name
        obj = er.obj
        # There is a data anomaly, likely due to merge
        if obj is None:
            continue
        other = "{} {}".format(obj.first_name, obj.last_name).strip()
        if other == '':
            other = 'unrecorded'
        ref_data['roles'][role].append(other)
    ref_data['roles'] = dict(ref_data['roles'])
    return ref_data

def merge_ref_data(existingDataList, newData):
    new_list = []
    merged = False
    for ex in existingDataList:
        ref_lock = (ex['date'], ex['locations'])
        ref_key = (newData['date'], newData['locations'])
        if ref_lock == ref_key:
            merged = merge_ref_roles(ex,newData)
            new_list.append(merged)
        else:
            new_list.append(ex)
    if not merged:
        new_list.append(newData)
    return new_list

def merge_ref_roles(o,n):
    for k in n['roles']:
        if k in o['roles']:
            o['roles'][k] = list(set(
                o['roles'][k] + n['roles'][k]))
    return o

def json_for_browse():
    persons = models.Person.query.all()
    owner_role = models.Role.query.filter_by(name='owner').first()
    ensl = list({ p for p in persons
        for r in p.references if owner_role not in r.roles })
    out = []
    for p in ensl:
        data = {}
        data['id'] = p.id
        data['first_name'] = p.first_name
        data['last_name'] = p.last_name
        if data['first_name'] == '' and data['last_name'] == '':
            data['first_name'] = 'unrecorded'
        data['documents'] = collections.defaultdict(list)
        data['description'] = {
            'tribe': '',
            'sex': '',
            'origin': '',
            'vocation': '',
            'age': '',
            'race': '',
            'title': ''
        }
        data['status'] = 'enslaved'
        data['owner'] = ''
        data['transcription'] = ''
        first_date = datetime.datetime(year=2018,day=1,month=1)
        for ref in p.references:
            citation = ref.record.document.citation
            new_date = ref.record.date
            if new_date < first_date:
                first_date = new_date
            existing_ref_data = data['documents'][citation]
            new_ref_data = process_reference(ref)
            data['documents'][citation] = merge_ref_data(
                existing_ref_data, new_ref_data)
            for d in data['documents'][citation]:
                if d.get('description'):
                    ex_desc = data['description']
                    new_desc = d['description']
                    ex_desc['tribe'] = new_desc['tribe'] \
                        if new_desc['tribe'] else ex_desc['tribe']
                    ex_desc['sex'] = new_desc['sex'] \
                        if new_desc['sex'] else ex_desc['sex']
                    ex_desc['origin'] = new_desc['origin'] \
                        if new_desc['origin'] else ex_desc['origin']
                    ex_desc['vocation'] = new_desc['vocation'] \
                        if new_desc['vocation'] else ex_desc['vocation']
                    ex_desc['age'] = new_desc['age'] \
                        if new_desc['age'] else ex_desc['age']
                    ex_desc['race'] = new_desc['race'] \
                        if new_desc['race'] else ex_desc['race']
            for ref in data['documents'][citation]:
                if 'enslaved' in ref['roles']:
                    if len(ref['roles']['enslaved']) > 0:
                        data['owner'] = ref['roles']['enslaved'][0]
            for ref in data['documents'][citation]:
                data['comments'] = ref['comments']
        data['date'] = {
            'year': first_date.year,
            'month': first_date.month,
            'day': first_date.day
        }
        out.append(data)
    return out