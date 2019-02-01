import json
import re
import datetime
from app import db, models

def titlecase(s):
    return re.sub(
        r"[A-Za-z\u00E1\u00ed]+('[A-Za-z\u00E1\u00ed]+)?",
        lambda mo: mo.group(0)[0].upper() +
        mo.group(0)[1:].lower(),
        s)

def clean_text(val):
    skipwords = { 'and', 'of', 'de', 'y', 'la', 'del', 'the' }
    stripped = val.strip()
    titled = [ v if v in skipwords else titlecase(v)
                for v in stripped.split() ]
    cleaned = ' '.join(titled)
    return cleaned

def filter_collection(fltr, coll, mapped={}):
    if mapped == {}:
        filtered = [ c for c in coll if c.name == fltr ]
    else:
        filtered = [ c for c in coll if c.name == mapped[fltr] ]
    if len(filtered) > 1:
        raise
    return filtered[0]

def process_multivalued_attr(attrStr, collection, mapped={}, nulls=[]):
    if attrStr.strip() in nulls:
        return []
    if attrStr.strip() in mapped:
        attrStr = mapped[attrStr.strip()]
    val = clean_text(attrStr)
    try:
        obj = filter_collection(val, collection)
        return [ obj ]
    except:
        print(attrStr)
        print(val)
        print(mapped)

def load_data(datafile):
    with open(datafile, 'r') as f:
        data = json.load(f)

    doc_types = models.CitationType.query.all()
    rec_types = models.ReferenceType.query.all()
    roles = models.Role.query.all()
    users = models.User.query.all()
    tribes = models.Tribe.query.all()
    races = models.Race.query.all()
    vocations = models.Vocation.query.all()
    enslavements = models.EnslavementType.query.all()
    titles = models.Title.query.all()
    locations = models.Location.query.all()
    name_types = models.NameType.query.all()
    natl_ctx = models.NationalContext.query.all()

    parent_role = filter_collection('Parent', roles)
    child_role = filter_collection('Child', roles)
    mother_role = filter_collection('Mother', roles)
    father_role = filter_collection('Father', roles)
    owner_role = filter_collection('Owner', roles)
    enslaved_role = filter_collection('Enslaved', roles)
    buyer_role = filter_collection('Buyer', roles)
    seller_role = filter_collection('Seller', roles)

    title_field = models.ZoteroField.query.filter_by(name='title').first()
    
    counter = 0
    for mongo_dict in data:
        print(counter)
        doc = process_document(mongo_dict['document'])
        doc.citation_type = process_document_type(
            mongo_dict['document']['sourceType'],
            mongo_dict['document']['recordType'], doc_types)
        doc.comments = mongo_dict['researcherNotes']
        db.session.add(doc)
        db.session.commit()

        cite_field = models.CitationField(citation_id=doc.id,
            field_id=title_field.id, field_data=doc.display)
        db.session.add(cite_field)
        db.session.commit()

        rec = models.Reference()
        rec.date = process_record_date(mongo_dict)
        rec.transcription = mongo_dict['additionalInformation']
        rec.national_context = process_national_context(
            mongo_dict['document'], natl_ctx)
        rec.reference_type = process_record_type(
            mongo_dict['document']['sourceType'],
            mongo_dict['document']['recordType'], rec_types)
        rec.citation = doc
        db.session.add(rec)
        db.session.commit()

        admin = process_administrative_metadata(
            mongo_dict['meta'], users)
        for amn in admin:
            edit = models.ReferenceEdit(timestamp=amn[1])
            edit.edited_by = amn[0]
            edit.edited = rec
            db.session.add(edit)
        db.session.commit()

        locs = process_location(mongo_dict['document'])
        for loc in locs:
            db.session.add(loc[0])
        db.session.commit()
        for loc in locs:
            rec_loc = models.ReferenceLocation()
            rec_loc.reference = rec
            rec_loc.location = loc[0]
            rec_loc.location_type = loc[1]
            rec_loc.location_rank = locs.index(loc)
            db.session.add(rec_loc)
        db.session.commit()

        valid_person = check_person(mongo_dict['person'], 'primary')
        if valid_person:
            person = process_person(valid_person, name_types,
                tribes, races, locations, vocations, enslavements)
            person.roles.append(enslaved_role)
        entrants = [ person ]
        relationships = []
        
        valid_mother = check_person(
            mongo_dict['person']['mother'], 'parent')
        if valid_mother:
            mother = process_parent( valid_mother, name_types, 
                races, locations, enslavements, 'Female',
                parent_role, mother_role)
            person.roles.append(child_role)
            ers = process_entrant_relationship(
                mother, person, mother_role, child_role)
            entrants.append(mother)
            relationships.extend(ers)

        valid_father = check_person(
            mongo_dict['person']['father'], 'parent')
        if valid_father:
            father = process_parent(valid_father, name_types,
                races, locations, enslavements, 'Male',
                parent_role, father_role)
            person.roles.append(child_role)
            ers = process_entrant_relationship(
                father, person, father_role, child_role)
            entrants.append(father)
            relationships.extend(ers)
        
        valid_children = [ check_person(child, 'child') 
            for child in mongo_dict['person']['children'] ]
        if valid_children:
            valid_children = [ v for v in valid_children if v ]
        children = []
        for child_data in valid_children:
            child = process_child(child_data, name_types, child_role)
            if person.sex == 'Male':
                person.roles.extend([parent_role, father_role])
                ers = process_entrant_relationship(
                    person, child, father_role, child_role)
                relationships.extend(ers)
            elif person.sex == 'Female':
                person.roles.extend([parent_role, mother_role])
                ers = process_entrant_relationship(
                    person, child, mother_role, child_role)
                relationships.extend(ers)
            else:
                person.roles.append(parent_role)
                ers = process_entrant_relationship(
                    person, child, gendered, child_role)
                relationships.extend(ers)
            children.append(child)
        entrants.extend(children)
        
        valid_owner = check_person(mongo_dict['owner'], 'owner')
        if valid_owner:
            owner = process_owner(valid_owner, name_types,
                titles, owner_role)
            ers = process_entrant_relationship(
                owner, person, owner_role, enslaved_role)
            entrants.append(owner)
            relationships.extend(ers)
        valid_mowner = check_person(
            mongo_dict['person']['mother']['owner'], 'owner')
        if valid_mowner:
            mother_owner = process_owner(valid_mowner,
                name_types, titles, owner_role)
            ers = process_entrant_relationship(
                mother_owner, mother, owner_role, enslaved_role)
            entrants.append(mother_owner)
            relationships.extend(ers)
        valid_fowner = check_person(
            mongo_dict['person']['father']['owner'], 'owner')
        if valid_fowner:
            father_owner = process_owner(valid_fowner,
                name_types, titles, owner_role)
            ers = process_entrant_relationship(
                father_owner, father, owner_role, enslaved_role)
            entrants.append(father_owner)
            relationships.extend(ers)
        
        valid_buyer = check_person(mongo_dict['buyer'], 'other')
        if valid_buyer:
            buyer = process_other(valid_buyer,
                name_types, buyer_role)
            ers = process_entrant_relationship(
                buyer, person, buyer_role, enslaved_role)
            entrants.append(buyer)
            relationships.extend(ers)
        valid_seller = check_person(mongo_dict['seller'], 'other')
        if valid_seller:
            seller = process_other(valid_seller,
                name_types, seller_role)
            ers = process_entrant_relationship(
                seller, person, seller_role, enslaved_role)
            entrants.append(seller)
            relationships.extend(ers)

        for e in entrants:
            e.reference = rec
            e.primary_name = e.names[0]
            db.session.add(e)
        db.session.commit()

        for r in relationships:
            db.session.add(r)
        db.session.commit()

        for e in entrants:
            prsn = models.Person()
            prsn.first_name = e.primary_name.first
            prsn.last_name = e.primary_name.last
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

def clean_citation(citation):
    cit = citation.strip()
    if "Tangier" in cit and ";" in cit:
        cit  = cit[:cit.index(';')]
    return cit

def process_document(docData):
    citation = docData['citation']
    zotero = ''
    if 'DISA' in citation:
        zotero, citation = extract_zotero_id(citation)
    citation = clean_citation(citation)
    existing = models.Citation.query.filter_by(display=citation).first()
    if existing:
        return existing
    doc = models.Citation()
    doc.display = citation
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
    bad_date = datetime.datetime(day=1, month=1, year=1)
    record_date_fields = [ 'dateOfEmancipation',
        'dateOfMarriage', 'dateOfRunaway', 'dateOfDeath' ]
    record_dates = [ process_date( entryData.get(df, {}) ) 
        for df in record_date_fields ]
    clean_dates = [ d for d in record_dates
        if d != bad_date ]
    if len(clean_dates) > 1:
        raise
    if clean_dates == []:
        if doc_date == bad_date:
            return None
        else:
            return doc_date
    else:
        return clean_dates[0]

def check_person(personData, personType):
    prs_templates = {
        'primary': {
            'names': [],
            'vocation': '',
            'children': [],
            'origin': '',
            'age': '',
            'sex': '',
            'race': '',
            'typeKindOfEnslavement': '',
            'tribe': '',
        },
        'owner' :     {
            'name': {
                'firstName': '',
                'lastName': '',
                'title': ''
            },
            'vocation': ''
        },
        'parent' : {
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
        },
        'child': {
            'name' : {
                'firstName': '',
                'lastName': ''
            }
        },
        'other': {
            'firstName': '',
            'lastName': ''
        }
    }
    if personData == prs_templates[personType]:
        return None
    return personData

def process_person(personData, nameTypes, tribes,
        races, origins, vocations, enslavements):
    ent = models.Referent()
    ent.names = process_names(personData['names'], nameTypes)
    ent.sex = personData['sex']
    ent.age = personData.get('age','')
    ent.tribes = process_tribe(personData['tribe'], tribes)
    ent.races = process_race(personData['race'], races)
    ent.origins = process_origin(personData['origin'], origins)
    ent.vocations = process_vocation(personData['vocation'], vocations)
    ent.enslavements = process_enslavement(
        personData['typeKindOfEnslavement'], enslavements)
    return ent

def process_parent(parentData, nameTypes, races, origins,
        enslavements, gender, parentRole, genderRole):
    ent = models.Referent()
    ent.sex = gender
    ent.names = process_name(parentData['name'], nameTypes)
    ent.races = process_race(parentData['race'], races)
    ent.origins = process_origin(parentData['origin'], origins)
    ent.enslavements = process_enslavement(
        parentData['status'], enslavements)
    ent.roles.extend([ parentRole, genderRole ])
    return ent

def process_child(childData, nameTypes, childRole):
    ent = models.Referent()
    ent.names = process_name(childData['name'], nameTypes)
    ent.roles.append(childRole)
    return ent

def process_owner(ownerData, nameTypes, titles, ownerRole):
    ent = models.Referent()
    ent.names = process_name(ownerData['name'], nameTypes)
    ent.titles = process_title(ownerData['name']['title'], titles)
    ent.roles.append(ownerRole)
    return ent

def process_other(otherData, nameTypes, otherRole):
    ent = models.Referent()
    ent.names = process_name(otherData, nameTypes)
    ent.roles.append(otherRole)
    return ent

def process_names(nameList, objs):
    names = []
    if nameList == []:
        nameList = [ 
            { 'firstName': '', 'lastName': '', 'type': 'Unknown' }
        ]
    for name_data in nameList:
        name_type = name_data['type'] or 'Given'
        names.extend( process_name(name_data, objs, name_type) )
    return names

def process_name(nameData, nameTypes, typeStr='Given'):
    if nameData == { 'firstName': '', 'lastName': '' }:
        typeStr = 'Unknown'
    type_obj = filter_collection(typeStr, nameTypes)
    name = models.ReferentName()
    name.first = nameData['firstName'].strip()
    name.last = nameData['lastName'].strip()
    name.name_type = type_obj
    return [ name ]

def process_origin(originStr, objs):
    nulls = [ '', 'ditto', 'Unspecified', 'The Valiante Nation',
        'Blanco']
    mapped = {
        'Allentown, PA' : 'Allentown',
        'Píritu (Cumaná province)' : 'Píritu',
        'Spanish' : 'Spain',
        'Y[iu]by' : 'Yiuby'
    }
    return process_multivalued_attr(originStr, objs,
        mapped, nulls)

def process_race(raceStr, objs):
    nulls = ['']
    mapped = {
        '"Part African and Part Indian"': 'Part African and Part Indian',
        'India' : 'Indian',
        'Surrinam Indian' : 'Surinam Indian'
    }
    return process_multivalued_attr(raceStr, objs, mapped, nulls)

def process_title(titleStr, objs):
    nulls = ['']
    mapped = {
        'Mr' : 'Mr.'
    }
    return process_multivalued_attr(titleStr, objs, mapped, nulls)

def process_tribe(tribeStr, objs):
    nulls = [ '', 'Unspecified', 'TEST' ]
    mapped = {
        'Blanco Nation' : 'Blanco',
        'Co[d]ira': 'Codira',
        'Eastern Pequot (?)': 'Eastern Pequot',
        'Mohegan (?)': 'Mohegan',
        'Naragansett (?)': 'Naragansett',
        'Noleva Indian' : 'Noleva',
        '[Nidwa]': 'Nidwa'
    }
    return process_multivalued_attr(tribeStr, objs,
        mapped, nulls)

def process_vocation(vocStr, objs):
    nulls = [ '','N/A','[Pos]']
    mapped = {
        'Shipcarpenter' : 'Ship Carpenter',
        'sargento mayor actual de esta cuidad' : 'sargento mayor actual de esta ciudad'
    }
    return process_multivalued_attr(vocStr, objs,
        mapped, nulls)

def process_enslavement(enslvStr, objs):
    nulls = ['']
    mapped = {
        '(maybe)': 'Enslaved',
        '(probably)': 'Enslaved',
        'Man servant': 'Manservant',
        'Man slave': 'Manslave',
        'Maid servant': 'Maidservant',
        'Maid Servant': 'Maidservant',
        'Indenture': 'Indentured Servant',
        'Unclear': 'Enslaved'
    }
    return process_multivalued_attr(enslvStr, objs, mapped, nulls)

def process_document_type(docTypeStr, recTypeStr, objs):
    pairs = {
        ('', ''): 'Document',
        ('', 'Archival'): 'Book',
        ('', 'Inventory'): 'Book',
        ('Archie', 'Manumission'): 'Letter',
        ('Archival', 'List'): 'List',
        ('Archival', 'Listing'): 'List',
        ('Archival', 'Registry'): 'Registry',
        ('Archival ', 'Listing'): 'List',
        ('Archive', ''): 'Book',
        ('Archive', 'LIst'): 'List',
        ('Archive', 'List'): 'List',
        ('Archive', 'Manumission'): 'Book',
        ('Archive', 'Manumission '): 'Book',
        ('Archive', 'Registry'): 'Registry',
        ('Archive', 'Registry '): 'Registry',
        ('Archive ', 'Registry'): 'Registry',
        ('Book', ''): 'Book',
        ('Book', 'Court Document'): 'Book',
        ('Census', ''): 'Census',
        ('Court Documents', 'Archival'): 'Document',
        ('Indenture', ''): 'Book',
        ('Indenture', 'Book'): 'Book',
        ('Inventory', ''): 'Book',
        ('Inventory', 'Archival'): 'Book',
        ('Inventory', 'Probate'): 'Book',
        ('Letter', 'Archival'): 'Letter',
        ('Mosquito Coast ', 'British Honduras'): 'Registry',
        ('Newsletter', 'Advertisement of sale'): 'Advertisement of Sale',
        ('Newsletter', 'Runaway Advertisement'): 'Runaway Advertisement',
        ('Newspaper', 'Advertisement of Sale'): 'Advertisement of Sale',
        ('Newspaper', 'Advertisement of sale'): 'Advertisement of Sale',
        ('Newspaper', 'Execution notice'): 'Execution Notice',
        ('Newspaper', 'News story'): 'Newspaper Article',
        ('Newspaper', 'Runaway Advertisement'): 'Runaway Advertisement',
        ('Newspaper', 'Runaway Advertisement '): 'Runaway Advertisement',
        ('Newspaper', 'Runaway Ad'): 'Runaway Advertisement',
        ('Newspaper', ''): 'Runaway Advertisement',
        ('Newspaper', 'Runaway Slave Ad'): 'Runaway Advertisement',
        ('Newspaper', 'Runaway Advertisements'): 'Runaway Advertisement',
        ('Newspaper', 'Runaway advertisement'): 'Runaway Advertisement',
        ('Newspaper', 'Runaway capture advertisement'): 'Runaway Capture Advertisement',
        ('Newspaper', 'Slave Advertisment'): 'Advertisement of Sale',
        ('Newspaper', 'Smallpox inoculation notice'): 'Smallpox Inoculation Notice',
        ('Newspaper ', 'Runaway Advertisement'): 'Runaway Advertisement',
        ('Newspaper; DISA00081', 'Runaway Advertisement '): 'Runaway Advertisement',
        ('Printed primary source', 'Letter'): 'Letter',
        ('Probate Account', 'Probate'): 'Book',
        ('Probate note', ''): 'Book',
        ('Registry', 'Archive'): 'Registry',
        ('Runaway Advertisement', 'Newspaper'): 'Runaway Advertisement',
        ('Runaway advertisement', 'Newspaper'): 'Runaway Advertisement',
        ('Will', 'Probate'): 'Book',
        ('Will Written', 'Probate'): 'Book',
    }
    if ( docTypeStr, recTypeStr ) in pairs:
        docTypeStr = pairs[( docTypeStr, recTypeStr )]
    else:
        raise
    return filter_collection(docTypeStr, objs) 

def process_record_type(recTypeStr, docTypeStr, objs):
    pairs = {
        ('', ''): 'Inventory',
        ('', 'Archival'): 'Inventory',
        ('', 'Inventory'): 'Inventory',
        ('Archie', 'Manumission'): 'Manumission',
        ('Archival', 'List'): 'Inventory',
        ('Archival', 'Listing'): 'Inventory',
        ('Archival', 'Registry'): 'Inventory',
        ('Archival ', 'Listing'): 'Inventory',
        ('Archive', ''): 'Reference',
        ('Archive', 'LIst'): 'Inventory',
        ('Archive', 'List'): 'Inventory',
        ('Archive', 'Manumission'): 'Manumission',
        ('Archive', 'Manumission '): 'Manumission',
        ('Archive', 'Registry'): 'Inventory',
        ('Archive', 'Registry '): 'Inventory',
        ('Archive ', 'Registry'): 'Inventory',
        ('Book', ''): 'Reference',
        ('Book', 'Court Document'): 'Reference',
        ('Census', ''): 'Reference',
        ('Court Documents', 'Archival'): 'Reference',
        ('Indenture', ''): 'Indenture',
        ('Indenture', 'Book'): 'Indenture',
        ('Inventory', ''): 'Inventory',
        ('Inventory', 'Archival'): 'Inventory',
        ('Inventory', 'Probate'): 'Inventory',
        ('Letter', 'Archival'): 'Reference',
        ('Mosquito Coast ', 'British Honduras'): 'Inventory',
        ('Newsletter', 'Advertisement of sale'): 'Sale',
        ('Newsletter', 'Runaway Advertisement'): 'Runaway',
        ('Newspaper', 'Advertisement of Sale'): 'Sale',
        ('Newspaper', 'Advertisement of sale'): 'Sale',
        ('Newspaper', 'Execution notice'): 'Execution',
        ('Newspaper', 'News story'): 'Reference',
        ('Newspaper', 'Runaway Advertisement'): 'Runaway',
        ('Newspaper', 'Runaway Advertisement '): 'Runaway',
        ('Newspaper', 'Runaway Advertisements'): 'Runaway',
        ('Newspaper', 'Runaway advertisement'): 'Runaway',
        ('Newspaper', 'Runaway Slave Ad'): 'Runaway',
        ('Newspaper', 'Runaway Ad'): 'Runaway',
        ('Newspaper', ''): 'Runaway',
        ('Newspaper', 'Runaway capture advertisement'): 'Capture',
        ('Newspaper', 'Slave Advertisment'): 'Sale',
        ('Newspaper', 'Smallpox inoculation notice'): 'Inoculation',
        ('Newspaper ', 'Runaway Advertisement'): 'Runaway',
        ('Newspaper; DISA00081', 'Runaway Advertisement '): 'Runaway',
        ('Printed primary source', 'Letter'): 'Reference',
        ('Probate Account', 'Probate'): 'Inventory',
        ('Probate note', ''): 'Inventory',
        ('Registry', 'Archive'): 'Inventory',
        ('Runaway Advertisement', 'Newspaper'): 'Runaway',
        ('Runaway advertisement', 'Newspaper'): 'Runaway',
        ('Will', 'Probate'): 'Inventory',
        ('Will Written', 'Probate'): 'Inventory',
    }
    if ( recTypeStr, docTypeStr ) in pairs:
        recTypeStr = pairs[( recTypeStr, docTypeStr )]
    else:
        print(recTypeStr, docTypeStr)
        raise
    return filter_collection(recTypeStr, objs)

def process_entrant_relationship(e1, e2, e1Role, e2Role):
    er1 = models.ReferentRelationship()
    er1.sbj = e1
    er1.obj = e2
    er1.related_as = e1Role
    er2 = models.ReferentRelationship()
    er2.sbj = e2
    er2.obj = e1
    er2.related_as = e2Role
    return [ er1, er2 ]

def process_national_context(docData, national_contexts):
    ctx_map = {
        '': 'Other',
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
    mapped = ctx_map[docData['nationalContext']]
    return filter_collection(mapped, national_contexts)

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
    location_keys = [ 'colonyState', 'stringLocation', 'locale']
    loc_key_map = {
        'colonyState' : 'Colony/State',
        'stringLocation' : 'String Location',
        'locale' : 'Locale'
    }
    for loc_key in location_keys:
        loc_text = docData.get(loc_key, None)
        if loc_text:
            loc_type_text = loc_key_map[loc_key]
            loc_type = models.LocationType.query.filter_by(name=loc_type_text).first()
            prepped = prep_location_text(loc_text)
            for p in prepped:
                if p not in location_names:
                    location_names.append((p, loc_type))
    locations = []
    for loc in location_names:
        location = models.Location.query.filter_by(name=loc[0]).first()
        if not location:
            location = models.Location(name=loc[0])
        locations.append( (location, loc[1]) )
    return locations

def process_administrative_metadata(metaData, users):
    user_map = {
        '103795391716629952261': 'linfordfisher@gmail.com',
        '106123372953260397156': 'juan_bettancourt-garcia@brown.edu',
        '106895219236186746888': 'disagrantreview@gmail.com',
        '109503335312366098524': 'anne_grasberger@brown.edu',
        '112148132795694739523': 'marley-vincent_lindsey@brown.edu',
        '112487255676465508755': 'rose_lang-maso@brown.edu',
        '113112063790792171857': 'samuel_skinner@brown.edu',
        '117289295548725522159': 'gwenyth_winship@brown.edu',
        '103765728548502769566': 'ashley_champagne@brown.edu',
        '114667147260750536832': 'cole_hansen@brown.edu'
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
