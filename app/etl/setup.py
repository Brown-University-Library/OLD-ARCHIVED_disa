from app import db, models

def load_multivalued_attributes():
    roles = [
        {'name': 'Enslaved'},
        {'name': 'Owner'},
        {'name': 'Priest'},
        {'name': 'Inoculated'},
        {'name': 'Bought'},
        {'name': 'Sold'},
        {'name': 'Shipped'},
        {'name': 'Arrived'},
        {'name': 'Escaped'},
        {'name': 'Captor'},
        {'name': 'Captured'},
        {'name': 'Baptised'},
        {'name': 'Emancipated'},
        {'name': 'Executed'},
        {'name': 'Parent'},
        {'name': 'Spouse'},
        {'name': 'Child'},
        {'name': 'Mother'},
        {'name': 'Father'},
        {'name': 'Buyer'},
        {'name': 'Seller'}
    ]
    tribes = [
        {'name': 'Blanco'},
        {'name': 'Bocotora'},
        {'name': 'Codira'},
        {'name': 'Eastern Pequot'},
        {'name': 'Mashantucket Pequot'},
        {'name': 'Mohegan'},
        {'name': 'Naragansett'},
        {'name': 'Nidwa'},
        {'name': 'Noleva'},
        {'name': 'Pequot'},
        {'name': 'Rocotora'},
        {'name': 'Sambo'},
        {'name': 'Shalliba'},
        {'name': 'Shatyana'},
        {'name': 'Tanybec'},
        {'name': 'Tenebec'},
        {'name': 'Tenybec'},
        {'name': 'Toluskey'},
        {'name': 'Valiante'},
        {'name': 'Wampanoag'},
        {'name': 'Woolwa'},
        {'name': 'de Nacion Caribe Cuchibero'}
    ]
    enslavements = [
        {'name': 'Enslaved'},
        {'name': 'Maidservant'},
        {'name': 'Manservant'},
        {'name': 'Indentured Servant'},
        {'name': 'Pieza'},
        {'name': 'Manslave'},
        {'name': 'Servant'},
        {'name': 'Slave'},
        {'name': 'Indenture, Court-Ordered'},
        {'name': 'Indenture, Parental'},
        {'name': 'Indenture, Voluntary'},
        {'name': 'Woman Servant'}
    ]
    races = [
        {'name': 'Part African and Part Indian'},
        {'name': 'Carolina Indian'},
        {'name': 'Creole'},
        {'name': 'Criollo'},
        {'name': 'East India Negro'},
        {'name': 'Half Indian'},
        {'name': 'Indian'},
        {'name': 'Indian Mulatto'},
        {'name': 'Indio'},
        {'name': "Martha's Vineyard Indian"},
        {'name': 'Mestiza'},
        {'name': 'Mestizo'},
        {'name': 'Mulatto'},
        {'name': 'Sambo'},
        {'name': 'Spanish Indian'},
        {'name': 'Surinam Indian'},
        {'name': 'Surrinam Indian'},
        {'name': 'West India Mulatto'}
    ]
    titles = [
        {'name': 'Bro.'},
        {'name': 'Capt.'},
        {'name': 'Captain'},
        {'name': 'Don'},
        {'name': 'Dr.'},
        {'name': 'Esq.'},
        {'name': 'Fray'},
        {'name': 'Hon. Col.'},
        {'name': 'Mistress'},
        {'name': 'Mr.'},
        {'name': 'Mrs.'},
        {'name': 'Reverend Mr.'},
        {'name': 'Widow'}
    ]
    vocations = [
        {'name': 'Baker'},
        {'name': 'Butcher'},
        {'name': 'Carpenter'},
        {'name': 'Chimney-Sweeper'},
        {'name': 'Chirurgeon'},
        {'name': 'Cooper'},
        {'name': 'Cordwainer'},
        {'name': 'Farmer'},
        {'name': 'Gentleman'},
        {'name': 'Gobernador y Capitan General of the Trinidad Island'},
        {'name': 'Governor'},
        {'name': 'Herald'},
        {'name': 'Household Work'},
        {'name': 'Husbandman'},
        {'name': 'Lawyer'},
        {'name': 'Leather Dresser'},
        {'name': 'Leatherer'},
        {'name': 'Malster'},
        {'name': 'Mariner'},
        {'name': 'Merchant'},
        {'name': 'Mineworker'},
        {'name': 'Minister'},
        {'name': 'Sadler'},
        {'name': 'Sailor'},
        {'name': 'Sargento Mayor Actual (De Esta Ciudad)'},
        {'name': 'Sawyer'},
        {'name': 'Sawyer & Carpenter'},
        {'name': 'Ship Carpenter'},
        {'name': 'Ship Captain'},
        {'name': 'Shipwright'},
        {'name': 'Shopkeeper'},
        {'name': 'Tailor'},
        {'name': 'Cura y Vicario de la Iglesia Parroquia de Esta Ciudad'},
        {'name': 'Guardián del Convento de San Francisco de Esta Ciudad'},
        {'name': 'of Bragmans'},
        {'name': 'Presbitero'},
        {'name': 'Sacristán Mayor'},
        {'name': 'Sargento Mayor Actual de Esta Ciudad'}
    ]
    origins = [
        { 'name': 'Allentown' },
        { 'name': 'Bermuda' },
        { 'name': 'Casanare' },
        { 'name': 'Casanave' },
        { 'name': 'Chabba' },
        { 'name': 'Jamaica' },
        { 'name': 'Pueblo de Casanare' },
        { 'name': 'Pueblo de Pauto' },
        { 'name': 'Píritu' },
        { 'name': 'Rio de Orinoco' },
        { 'name': 'Shangena' },
        { 'name': 'Spain' },
        { 'name': 'Yiuby' },
        { 'name': 'Yulusky' }
    ]
    record_types = [
        {'name': 'Runaway Advertisement'},
        {'name': 'Advertisement of Sale'},
        {'name': 'Baptism'},
        {'name': 'Runaway Capture Advertisement'},
        {'name': 'Smallpox Inoculation Notice'},
        {'name': 'Execution Notice'},
        {'name': 'Probate'},
        {'name': 'Manumission'},
        {'name': 'Registry'},
        {'name': 'News Story'},
        {'name': 'Section'},
        {'name': 'Listing'},
        {'name': 'Letter'},
        {'name': 'Indenture'},
        {'name': 'Court Document'},
        {'name': 'Account'},
        {'name': 'Note'},
    ]
    document_types = [
        {'name': 'Book'},
        {'name': 'Census'},
        {'name': 'Court Document'},
        {'name': 'Document'},
        {'name': 'Inventory'},
        {'name': 'Letter'},
        {'name': 'List'},
        {'name': 'Newsletter'},
        {'name': 'Newspaper'},
        {'name': 'Probate Record'},
        {'name': 'Record'},
        {'name': 'Registry'},
        {'name': 'Town Record'},
        {'name': 'Will'}
    ]
    name_types = [
        { 'name': 'Alias' },
        { 'name': 'Baptismal' },
        { 'name': 'English' },
        { 'name': 'European' },
        { 'name': 'Indian' },
        { 'name': 'Nickname' },
        { 'name': 'Given' },
        { 'name': 'Unknown' }
    ]
    tables = [
        ( models.Role, roles ),
        ( models.RecordType, record_types ),
        ( models.DocumentType, document_types ),
        ( models.Race, races ),
        ( models.Vocation, vocations ),
        ( models.Tribe, tribes ),
        ( models.Title, titles ),
        ( models.NameType, name_types ),
        ( models.EnslavementType, enslavements ),
        ( models.Location, origins )
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
        ('Manumission', ['Owner','Emancipated']),
        ('Runaway Advertisement', ['Owner','Escaped']),
        ('Advertisement of Sale', ['Owner','Enslaved']),
        ('Baptism', ['Owner','Priest','Baptised']),
        ('Runaway Capture Advertisement', ['Captor', 'Captured']),
        ('Smallpox Inoculation Notice', ['Inoculated','Owner']),
        ('Execution Notice', ['Executed']),
        ('Probate', ['Owner','Enslaved'])
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