from app import db, models

def load_multivalued_attributes():
    roles = [
        { 'name': 'enslaved' },
        { 'name': 'owner' },
        { 'name': 'priest' },
        { 'name': 'inoculated' },
        { 'name': 'escaped' },
        { 'name': 'captor' },
        { 'name': 'captured' },
        { 'name': 'baptised' },
        { 'name': 'emancipated' },
        { 'name': 'executed' },
        { 'name': 'maidservant' },
        { 'name': 'manservant' },
        { 'name': 'indentured servant' },
        { 'name': 'pieza' },
        { 'name': 'manslave' },
        { 'name': 'servant' }
    ]
    record_types = [ 
        { 'name': 'runaway advertisement' },
        { 'name': 'advertisement of sale' },
        { 'name': 'baptism' },
        { 'name': 'runaway capture advertisement' },
        { 'name': 'smallpox inoculation notice' },
        { 'name': 'execution notice'},
        { 'name': 'probate' },
        { 'name': 'manumission'},
        { 'name': 'registry'},
        { 'name': 'news story'},
        { 'name': 'unspecified' }
    ]
    document_types = [
        { 'name': 'newspaper' },
        { 'name': 'letter' },
        { 'name': 'archive' },
        { 'name': 'inventory' },
        { 'name': 'census' },
        { 'name': 'court documents' },
        { 'name': 'book' },
        { 'name': 'will' },
        { 'name': 'unspecified' }
    ]
    tables = [
        ( models.Role, roles ),
        ( models.RecordType, record_types ),
        ( models.DocumentType, document_types ),
    ]
    for pair in tables:
        table = pair[0]
        for data in pair[1]:
            row = table(**data)
            db.session.add(row)
            print('{}: value {}'.format(table.__tablename__, data))
        db.session.commit()

def load_many_to_many():
    recordtype_roles = [
        ('manumission', ['owner','emancipated']),
        ('runaway advertisement', ['owner','escaped']),
        ('advertisement of sale', ['owner','enslaved']),
        ('baptism', ['owner','priest','baptised']),
        ('runaway capture advertisement', ['captor', 'captured']),
        ('smallpox inoculation notice', ['inoculated','owner']),
        ('execution notice', ['executed']),
        ('probate', ['owner','enslaved'])
    ]

    many_to_many = [
        (models.RecordType, models.Role, recordtype_roles,
            'name', 'name', 'roles')
    ]

    for many in many_to_many:
        model1 = many[0]
        model2 = many[1]
        for mapping in many[2]:
            query = { many[3]: mapping[0] }
            focus = model1.query.filter_by( **query ).first()
            opts  = model2.query.all()
            rel = [ o for o in opts if getattr(o, many[4]) in mapping[1] ]
            getattr(focus, many[5]).extend(rel)
            db.session.add(focus)
            print( "{}:{} asscoiated with {}:{}".format(
                model1.__tablename__, mapping[0],
                model2.__tablename__, mapping[1]) )
            db.session.commit()

def load_self_references():
    tables = [ (models.Role, 'roles') ]

    role_references = [
        ('captor', 'captured')
    ]
    references = {}