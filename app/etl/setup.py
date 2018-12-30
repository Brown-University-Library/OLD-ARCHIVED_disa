from app import db, models

def load_multivalued_attributes():
    roles = [
        {'name': 'Enslaved', 'name_as_relationship': 'enslaved by'},
        {'name': 'Owner', 'name_as_relationship': 'owner of'},
        {'name': 'Priest', 'name_as_relationship': 'priest for'},
        {'name': 'Inoculated', 'name_as_relationship': 'inoculated by'},
        {'name': 'Bought', 'name_as_relationship': 'bought by'},
        {'name': 'Sold', 'name_as_relationship': 'sold by'},
        {'name': 'Shipped', 'name_as_relationship': 'shipped by'},
        {'name': 'Arrived', 'name_as_relationship': 'delivered by'},
        {'name': 'Escaped', 'name_as_relationship': 'escaped from'},
        {'name': 'Captor', 'name_as_relationship': 'captured'},
        {'name': 'Captured', 'name_as_relationship': 'captured by'},
        {'name': 'Baptised', 'name_as_relationship': 'baptised by'},
        {'name': 'Emancipated', 'name_as_relationship': 'released by'},
        {'name': 'Executed', 'name_as_relationship': 'execeuted by'},
        {'name': 'Parent', 'name_as_relationship': 'parent of'},
        {'name': 'Spouse', 'name_as_relationship': 'spouse of'},
        {'name': 'Child', 'name_as_relationship': 'child of'},
        {'name': 'Mother', 'name_as_relationship': 'mother of'},
        {'name': 'Father', 'name_as_relationship': 'father of'},
        {'name': 'Buyer', 'name_as_relationship': 'buyer of'},
        {'name': 'Seller', 'name_as_relationship': 'seller of'}
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
    reference_types = [
        {'name': 'Baptism'},
        {'name': 'Runaway'},
        {'name': 'Sale'},
        {'name': 'Capture'},
        {'name': 'Inoculation'},
        {'name': 'Execution'},
        {'name': 'Manumission'},
        {'name': 'Entry'},
        {'name': 'Indenture'},
        {'name': 'Account'},
        {'name': 'Note'},
        {'name': 'Inventory'},
        {'name': 'Reference'}
    ]
    citation_types = [
        {'name': 'Runaway Advertisement'},
        {'name': 'Runaway Capture Advertisement'},
        {'name': 'Advertisement of Sale'},
        {'name': 'Smallpox Inoculation Notice'},
        {'name': 'Execution Notice'},
        {'name': 'Book'},
        {'name': 'Census'},
        {'name': 'Court Document'},
        {'name': 'Document'},
        {'name': 'Inventory'},
        {'name': 'Letter'},
        {'name': 'List'},
        {'name': 'Registry'},
        {'name': 'Newspaper Article'},
        {'name': 'Probate Record'},
        {'name': 'Record'},
        {'name': 'Registry'},
        {'name': 'Town Record'},
        {'name': 'Will'},
        {'name': 'Registry'},
        {'name': 'Section'},
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
    natl_ctx = [
        { 'name': 'British' },
        { 'name': 'American' },
        { 'name': 'French' },
        { 'name': 'Spanish' },
        { 'name': 'Other'}
    ]
    tables = [
        ( models.Role, roles ),
        ( models.ReferenceType, reference_types ),
        ( models.CitationType, citation_types ),
        ( models.Race, races ),
        ( models.Vocation, vocations ),
        ( models.Tribe, tribes ),
        ( models.Title, titles ),
        ( models.NameType, name_types ),
        ( models.EnslavementType, enslavements ),
        ( models.Location, origins ),
        ( models.NationalContext, natl_ctx)
    ]
    for pair in tables:
        table = pair[0]
        for data in pair[1]:
            row = table(**data)
            db.session.add(row)
            print('{}: value {}'.format(table.__tablename__, data))
        db.session.commit()

def load_many_to_many():
    referencetype_roles = [
        ('Manumission', ['Owner','Emancipated']),
        ('Runaway', ['Owner','Escaped']),
        ('Sale', ['Owner','Enslaved']),
        ('Baptism', ['Owner','Priest','Baptised']),
        ('Capture', ['Captor', 'Captured']),
        ('Inoculation', ['Inoculated','Owner']),
        ('Execution', ['Executed']),
    ]

    many_to_many = [
        (models.ReferenceType, models.Role, referencetype_roles,
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