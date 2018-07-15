import json
import datetime
from app import db, models

def load_data(datafile):
    with open(datafile, 'r') as f:
        data = json.load(f)

    doc_types = models.DocumentType.query.all()
    rec_types = models.RecordType.query.all()
    roles = models.Role.query.all()
    users = models.User.query.all()

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
        rec.date = process_record_date(mongo_dict)
        rec.comments = mongo_dict['additionalInformation']
        rec.record_type = process_record_type(
            mongo_dict['document']['recordType'], rec_types)
        rec.document = doc
        db.session.add(rec)
        db.session.commit()

        admin = process_administrative_metadata(
            mongo_dict['meta'], users)
        for amn in admin:
            edit = models.RecordEdit(datetime=amn[1])
            edit.edited_by = amn[0]
            edit.edited = rec
            db.session.add(edit)
        db.session.commit()

        locs = process_location(mongo_dict['document'])
        for loc in locs:
            db.session.add(loc)
        db.session.commit()
        for loc in locs:
            rec_loc = models.RecordLocation()
            rec_loc.record = rec
            rec_loc.location = loc
            rec_loc.location_rank = locs.index(loc)
            db.session.add(rec_loc)
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
            mother.roles.extend([ role, parent_role ])
            person.roles.append(child_role)
            ers = process_entrant_relationship(
                mother, person, parent_role, child_role)
            entrants.append(mother)
            relationships.extend(ers)

        father = process_parent(mongo_dict['person']['father'])
        if father:
            role = process_enslavement_type(
                mongo_dict['person']['father']['status'], roles)
            father.roles.extend([ role, parent_role ])
            person.roles.append(child_role)
            ers = process_entrant_relationship(
                father, person, parent_role, child_role)
            entrants.append(father)
            relationships.extend(ers)
        
        children = [ process_child(child)
            for child in mongo_dict['person']['children'] ]
        for child in children:
            child.roles.extend([ enslaved_role, child_role])
            person.roles.append(parent_role)
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

        for e in entrants:
            prsn = models.Person(
                first_name=e.first_name, last_name=e.last_name)
            prsn.references.append(e)
            db.session.add(prsn)
        db.session.commit()
        counter += 1

def extract_zotero_id(citation):
    if citation.startswith('Zotero'):
        return (citation[11:20], citation[22:])
    elif citation.startswith('DISA'):
        return (citation[:9], citation[11:])
    elif '(DISA' in citation[-12:]:
        return (citation[-10:-1], citation[:-12])
    elif '; DISA' in citation[-12:]:
        return (citation[-9:], citation[:-11])
    else:
        print(citation)
        return ('', citation)

def process_document(docData):
    citation = docData['citation']
    zotero = ''
    if 'DISA' in citation:
        zotero, citation = extract_zotero_id(citation)
    date = process_date(docData['date'])
    existing = models.Document.query.filter_by(citation=citation, date=date).first()
    if existing:
        return existing
    doc = models.Document()
    doc.citation = citation
    doc.national_context = process_national_context(docData)
    doc.date = date
    doc.zotero_id = zotero
    return doc

def process_date(dateData):
    if dateData == {} or dateData == {'month': ''} \
        or dateData == {'year': '', 'month': '', 'day':''} :
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

def process_record_date(entryData):
    doc_date = process_date(entryData['document']['date'])
    record_date_fields = [ 'dateOfEmancipation',
        'dateOfMarriage', 'dateOfRunaway', 'dateOfDeath' ]
    record_dates = [ process_date( entryData.get(df, {}) ) 
        for df in record_date_fields ]
    clean_dates = [ d for d in record_dates
        if d != datetime.datetime(day=1, month=1, year=1) ]
    if len(clean_dates) > 1:
        raise
    elif clean_dates == []:
        return doc_date
    else:
        return clean_dates[0]

def process_person(personData):
    try:
        name = personData['names'][0]
    except IndexError:
        name = { 'firstName': '', 'lastName': '' }
    entrant = models.Entrant(
        first_name=name['firstName'].strip(), last_name=name['lastName'].strip())
    desc = models.Description(race=personData['race'], origin=personData['origin'],
        tribe=personData['tribe'], sex=personData['sex'], age=personData.get('age',0),
        vocation=personData['vocation'])
    entrant.description = desc
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
    entrant = models.Entrant(first_name=personData['name']['firstName'].strip(),
        last_name=personData['name']['lastName'].strip())
    desc = models.Description(race=personData['race'],
        origin=personData['origin'])
    entrant.description = desc
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
    entrant = models.Entrant(first_name=personData['name']['firstName'].strip(),
        last_name=personData['name']['lastName'].strip())
    return entrant

def process_other_person(personData):
    empty_data = {
        'firstName': '',
        'lastName': ''
    }
    if personData == {} or personData == empty_data:
        return None
    entrant = models.Entrant(first_name=personData['firstName'].strip(),
        last_name=personData['lastName'].strip())
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
    entrant = models.Entrant(first_name=personData['name']['firstName'].strip(),
        last_name=personData['name']['lastName'].strip())
    desc = models.Description(vocation=personData['vocation'],
        title=personData['name']['title'])
    entrant.description = desc
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
        'Newspaper; DISA00081' : 'newspaper',
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
        'British Honduras' : 'registry',
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
        'Slave Advertisment' : 'advertisement of sale',
        'Smallpox inoculation notice': 'smallpox inoculation notice'
    }
    return filter_collection(typeData, recTypes, type_map)

def process_enslavement_type(typeData, roles):
    type_map = {
        '': 'enslaved',
        '(maybe) ': 'enslaved',
        '(probably) ': 'enslaved',
        'Indenture': 'indentured servant',
        'Indenture, court-ordered' : 'indentured servant',
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

def process_national_context(docData):
    ctx_map = {
        '': 'unspecified',
        'American': 'American',
        'British': 'British',
        'British ': 'British',
        'British Coast': 'British',
        'French': 'French',
        'Honduras': 'British',
        'Spanish': 'Spanish',
        'USA': 'American',
        'United States': 'American'
    }
    return ctx_map[docData['nationalContext']]

def prep_location_text(loc):
    loc_map  = {
        'Massachussetts': 'Massachusetts',
        'Massuchesetts': 'Massachusetts',
        'Boson': 'Boston',
        'British': 'Britain',
        'American': 'United States',
        'British Coast': 'Britain',
        'French': 'France',
        'Spanish': 'Spain',
        'USA': 'United States',
        'Mosquito': 'Mosquito Coast',
        'Mosquito Shore': 'Mosquito Coast',
        'MD': 'Maryland',
        'Narraganset' : 'Narragansett'
    }
    no_parens = loc.strip(')').split('(')
    no_commas = []
    for p in no_parens:
        no_commas.extend( p.split(',') )
    cleaned = [ c.strip() for c in no_commas ]
    flipped = cleaned[::-1]
    mapped = [ loc_map.get(f) or f for f in flipped ]
    return mapped

def process_location(docData):
    location_names = []
    location_keys = [ 'nationalContext', 'colonyState', 'stringLocation', 'locale']
    for loc_key in location_keys:
        loc_text = docData.get(loc_key, None)
        if loc_text:
            prepped = prep_location_text(loc_text)
            for p in prepped:
                if p not in location_names:
                    location_names.append(p)
    locations = []
    for loc in location_names:
        location = models.Location.query.filter_by(name=loc).first()
        if not location:
            location = models.Location(name=loc)
        locations.append(location)
    return locations

def process_administrative_metadata(metaData, users):
    user_map = {
        '103795391716629952261': 'gwenyth_winship@brown.edu',
        '106123372953260397156': 'juan_bettancourt-garcia@brown.edu',
        '106895219236186746888': 'linfordfisher@gmail.com',
        '109503335312366098524': 'anne_grasberger@brown.edu',
        '112148132795694739523': 'marley-vincent_lindsey@brown.edu',
        '112487255676465508755': 'rose_lang-maso@brown.edu',
        '113112063790792171857': 'samuel_skinner@brown.edu',
        '117289295548725522159': 'jane.l.landers@vanderbilt.edu'
    }

    created_id = metaData['creator']
    editor_id = metaData['updatedBy']
    creator = filter_collection(created_id, users, user_map)
    editor = filter_collection(editor_id, users, user_map)
    dt = datetime.datetime.strptime(
        metaData['lastModified'], '%Y-%m-%dT%H:%M:%S.%fZ')
    users = [ (creator, dt) ]
    if creator != editor:
        dl = datetime.timedelta(days=1)
        users.append( (editor, dt + dl) )
    return users
