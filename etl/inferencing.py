from app import db, models
from collections import defaultdict

def extract_information():
    records = models.Reference.query.all()
    for rec in records:
        converge_record_names(rec)

    docs = models.Citation.query.all()
    for doc in docs:
        converge_document_people(doc)

def converge_persons(peopleList):
    preserve = peopleList[0]
    for rmv in peopleList[1:]:
        preserve.references.extend(rmv.references)
    db.session.add(preserve)
    db.session.commit()
    for rmv in peopleList[1:]:
        db.session.delete(rmv)
    db.session.commit()

def converge_document_people(doc):
    to_converge = defaultdict(list)
    for rec in doc.references:
        for e in rec.referents:
            person = e.person
            formatted_name = '{} {}'.format(
                person.first_name.strip(),
                person.last_name.strip() ).strip()
            to_converge[ formatted_name ].append(person)
    for c in to_converge:
        if len(to_converge[c]) > 1:
            if c != '' and c != 'John Brashaw' and c != 'Catalina':
                print('Converging {} for document {}'.format(c, doc.id))
                converge_persons(to_converge[c])

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
    for e in record.referents:
        formatted_name = '{} {}'.format(
            e.primary_name.first.strip(),
            e.primary_name.last.strip() ).strip()
        to_converge[ formatted_name ].append(e)
    for c in to_converge:
        if len(to_converge[c]) > 1:
            if c != '' and c != 'John Brashaw' and c != 'Catalina':
                print('Converging {} for record {}'.format(c, record.id))
                converge_entrants(to_converge[c])

def add_manumisson(record):
    pass

def infer_roles_from_record_types(recordType, roles):
    pass