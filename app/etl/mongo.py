import json
import datetime
from app import db, models

def load_data(datafile):
    with open(datafile, 'r') as f:
        data = json.load(f)

    doc_types = models.DocumentType.query.all()
    rec_types = models.RecordType.query.all()
    roles = models.Role.query.all()
    parent_role = filter_collection('parent', roles)
    child_role = filter_collection('child', roles)
    owner_role = filter_collection('owner', roles)
    enslaved_role = filter_collection('enslaved', roles)
    
    counter = 0
    for mongo_dict in data:
        print(counter)
        doc = process_document(mongo_dict['document'])
        doc.document_type = process_document_type(
            mongo_dict['document']['sourceType'], doc_types)
        db.session.add(doc)
        db.session.commit()

        rec = models.Record()
        rec.record_type = process_record_type(
            mongo_dict['document']['recordType'], rec_types)
        rec.document = doc
        db.session.add(rec)
        db.session.commit()

        person = process_person(mongo_dict['person'])
        role = process_enslavement_type(
            mongo_dict['person']['typeKindOfEnslavement'], roles)
        person.roles.append(role)
        entrants = [ person ]
        relationships = []
        
        mother = process_parent(mongo_dict['person']['mother'])
        if mother:
            role = process_enslavement_type(
                mongo_dict['person']['mother']['status'], roles)
            mother.roles.append(role)
            ers = process_entrant_relationship(
                mother, person, parent_role, child_role)
            entrants.append(mother)
            relationships.extend(ers)

        father = process_parent(mongo_dict['person']['father'])
        if father:
            role = process_enslavement_type(
                mongo_dict['person']['father']['status'], roles)
            father.roles.append(role)
            ers = process_entrant_relationship(
                father, person, parent_role, child_role)
            entrants.append(father)
            relationships.extend(ers)
        
        children = [ process_child(child)
            for child in mongo_dict['person']['children'] ]
        for child in children:
            ers = process_entrant_relationship(
                person, child, parent_role, child_role)
            relationships.extend(ers)
        entrants.extend(children)
        
        owner = process_owner(mongo_dict['owner'])
        if owner:
            owner.roles.append(owner_role)
            ers = process_entrant_relationship(
                owner, person, owner_role, enslaved_role)
            entrants.append(owner)
            relationships.extend(ers)
        mother_owner = process_owner(mongo_dict['person']['mother']['owner'])
        if mother_owner:
            mother_owner.roles.append(owner_role)
            ers = process_entrant_relationship(
                mother_owner, mother, owner_role, enslaved_role)
            entrants.append(mother_owner)
            relationships.extend(ers)
        father_owner = process_owner(mongo_dict['person']['father']['owner'])
        if father_owner:
            father_owner.roles.append(owner_role)
            ers = process_entrant_relationship(
                father_owner, father, owner_role, enslaved_role)
            entrants.append(father_owner)
            relationships.extend(ers)
        
        for e in entrants:
            e.record = rec
            db.session.add(e)
        db.session.commit()

        for r in relationships:
            db.session.add(r)
        db.session.commit()
        counter += 1

def process_document(docData):
    citation = docData['citation']
    date = process_date(docData['date'])
    existing = models.Document.query.filter_by(citation=citation, date=date).first()
    if existing:
        return existing
    doc = models.Document()
    doc.citation = citation
    doc.national_context = docData['nationalContext']
    doc.date = date
    return doc

def process_date(dateData):
    if dateData == {} or dateData == {'month': ''}:
        dateData = { 'day':1, 'month':1, 'year':1 }
    try:
        day = int( dateData.get('day',1) or 1)
        month = int( dateData.get('month',1) or 1)
        year = int( dateData.get('year',1) or 1)
    except:
        day = 1
        month = 1
        year = 1
    return datetime.datetime(day=day, month=month, year=year)

def process_person(personData):
    try:
        name = personData['names'][0]
    except IndexError:
        name = { 'firstName': '', 'lastName': '' }
    entrant = models.Entrant(
        first_name=name['firstName'], last_name=name['lastName'])
    desc = models.Description(race=personData['race'], origin=personData['origin'],
        tribe=personData['tribe'], sex=personData['sex'], age=personData.get('age',0),
        vocation=personData['vocation'])
    desc.entrant = entrant
    return entrant

def process_parent(personData):
    empty_data = {
        'name': {
            'firstName': '',
            'lastName': ''
        },
        'origin': '',
        'owner': {
            'name': {
                'firstName': '',
                'lastName': '',
                'title': ''
            },
            'vocation': ''
        },
        'race': '',
        'status': ''
   }
    if personData == {} or personData == empty_data:
        return None
    entrant = models.Entrant(first_name=personData['name']['firstName'],
        last_name=personData['name']['lastName'])
    desc = models.Description(race=personData['race'],
        origin=personData['origin'])
    desc.entrant = entrant
    return entrant

def process_child(personData):
    empty_data = {
        'name' : {
            'firstName': '',
            'lastName': ''
        }
    }
    if personData == {} or personData == empty_data:
        return None
    entrant = models.Entrant(first_name=personData['name']['firstName'],
        last_name=personData['name']['lastName'])
    return entrant

def process_other_person(personData):
    empty_data = {
        'firstName': '',
        'lastName': ''
    }
    if personData == {} or personData == empty_data:
        return None
    entrant = models.Entrant(first_name=personData['firstName'],
        last_name=personData['lastName'])
    return entrant

def process_owner(personData):
    empty_data = {
        'name': {
            'firstName': '',
            'lastName': '',
            'title': ''
        },
        'vocation': ''
    }
    if personData == {} or personData == empty_data:
        return None
    entrant = models.Entrant(first_name=personData['name']['firstName'],
        last_name=personData['name']['lastName'])
    desc = models.Description(vocation=personData['vocation'],
        title=personData['name']['title'])
    desc.entrant = entrant
    return entrant

def filter_collection(fltr, coll, mapped={}):
    if mapped == {}:
        filtered = [ c for c in coll if c.name == fltr ]
    else:
        filtered = [ c for c in coll if c.name == mapped[fltr] ]
    if len(filtered) > 1:
        raise
    return filtered[0]    

def process_document_type(typeData, docTypes):
    type_map = {
        '': 'unspecified',
        'Archie': 'archive',
        'Archival': 'archive',
        'Archival ': 'archive',
        'Archive': 'archive',
        'Archive ': 'archive',
        'Book': 'book',
        'Census': 'census',
        'Court Documents': 'court documents',
        'Indenture': 'court documents',
        'Inventory': 'inventory',
        'Letter': 'letter',
        'Mosquito Coast ': 'archive',
        'Newsletter': 'newspaper',
        'Newspaper': 'newspaper',
        'Newspaper ': 'newspaper',
        'Printed primary source': 'newspaper',
        'Probate Account': 'court documents',
        'Probate note': 'court documents',
        'Registry': 'archive',
        'Runaway Advertisement': 'newspaper',
        'Runaway advertisement': 'newspaper',
        'Will': 'will',
        'Will Written': 'will'
    }
    return filter_collection(typeData, docTypes, type_map)

def process_record_type(typeData, recTypes):
    type_map = {'': 'unspecified',
        'Advertisement of Sale': 'advertisement of sale',
        'Advertisement of sale': 'advertisement of sale',
        'Archival': 'unspecified',
        'Archive': 'unspecified',
        'Book': 'unspecified',
        'Court Document': 'unspecified',
        'Execution notice': 'execution notice',
        'Honduras': 'unspecified',
        'Inventory': 'unspecified',
        'LIst': 'unspecified',
        'Letter': 'unspecified',
        'List': 'unspecified',
        'Listing': 'unspecified',
        'Manumission': 'manumission',
        'Manumission ': 'manumission',
        'News story': 'news story',
        'Newspaper': 'news story',
        'Probate': 'probate',
        'Registry': 'registry',
        'Registry ': 'registry',
        'Runaway Advertisement': 'runaway advertisement',
        'Runaway Advertisement ': 'runaway advertisement',
        'Runaway Advertisements': 'runaway advertisement',
        'Runaway Capture Advertisement': 'runaway capture advertisement',
        'Runaway advertisement': 'runaway advertisement',
        'Runaway capture advertisement': 'runaway capture advertisement',
        'Smallpox inoculation notice': 'smallpox inoculation notice'
    }
    return filter_collection(typeData, recTypes, type_map)

def process_enslavement_type(typeData, roles):
    type_map = {
        '': 'enslaved',
        '(maybe) ': 'enslaved',
        '(probably) ': 'enslaved',
        'Indenture': 'indentured servant',
        'Indentured servant': 'indentured servant',
        'Maid Servant': 'maidservant',
        'Maid servant': 'maidservant',
        'Man servant': 'manservant',
        'Man slave': 'manslave',
        'Manslave': 'manslave',
        'Pieza': 'pieza',
        'Servant': 'servant',
        'Enslaved': 'enslaved',
        'Slave': 'enslaved',
        'Woman servant': 'maidservant'
    }
    return filter_collection(typeData, roles, type_map)

def process_entrant_relationship(e1, e2, e1Role, e2Role):
    er1 = models.EntrantRelationship()
    er1.sbj = e1
    er1.obj = e2
    er1.related_as = e1Role
    er2 = models.EntrantRelationship()
    er2.sbj = e2
    er2.obj = e1
    er2.related_as = e2Role
    return [ er1, er2 ]