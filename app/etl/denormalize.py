from app import models

import collections
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
        'locations': [ l[1] for l in sorted(locs, reverse=True) ]
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
    out = []
    for p in persons:
        data = {}
        data['first_name'] = p.first_name
        data['last_name'] = p.last_name
        data['documents'] = collections.defaultdict(list)
        for ref in p.references:
            citation = ref.record.document.citation
            existing_ref_data = data['documents'][citation]
            new_ref_data = process_reference(ref)
            data['documents'][citation] = merge_ref_data(
                existing_ref_data, new_ref_data)
        out.append(data)
    return out