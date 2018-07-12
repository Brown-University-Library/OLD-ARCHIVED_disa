from app import db, models
from collections import defaultdict

def extract_information():
    records = models.Record.query.all()
    for rec in records:
        converge_record_names(rec)

def converge_entrants(entrantList):
    preserve = entrantList[0]
    for rmv in entrantList[1:]:
        preserve.roles.extend(rmv.roles)
        preserve.as_subject.extend(rmv.as_subject)
        preserve.as_object.extend(rmv.as_object)
    db.session.add(preserve)
    db.session.commit()
    for rmv in entrantList[1:]:
        prs = rmv.person
        db.session.delete(prs)
        db.session.delete(rmv)
    db.session.commit()

def converge_record_names(record):
    to_converge = defaultdict(list)
    for e in record.entrants:
        formatted_name = '{} {}'.format(e.first_name, e.last_name).strip()
        to_converge[ formatted_name ].append(e)
    for c in to_converge:
        if len(to_converge[c]) > 1:
            if c != '' and c != 'John Brashaw':
                print('Converging {} for record {}'.format(c, record.id))
                converge_entrants(to_converge[c])

def add_manumisson(record):
    pass

def infer_roles_from_record_types(recordType, roles):
    pass