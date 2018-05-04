from app import db

location_within = db.Table('location_within',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('contained', db.Integer, db.ForeignKey('locations.id')),
    db.Column('container', db.String())
)

has_location = db.Table('has_location',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('event', db.Integer, db.ForeignKey('records.id')),
    db.Column('location', db.Integer, db.ForeignKey('locations.id')),
    db.Column('location_for', db.String())
)

owned_by = db.Table('owned_by',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('enslaved', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('owner', db.Integer, db.ForeignKey('entrants.id'))
)

child_of = db.Table('child_of',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('child', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('parent', db.Integer, db.ForeignKey('entrants.id'))
)

has_spouse = db.Table('has_spouse',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('spouse1', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('spouse2', db.Integer, db.ForeignKey('entrants.id'))
)

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    doctype = db.Column(db.String())
    date = db.Column(db.Date())
    national_context = db.Column(db.String())
    citation = db.Column(db.String())
    comments = db.Column(db.String())
    records = db.relationship('Record', backref='document', lazy=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    rectype = db.Column(db.String())
    date = db.Column(db.Date())
    comments = db.Column(db.String())
    entrants = db.relationship('Entrant', backref='record', lazy=True)
    locations = within = db.relationship(
        'Location', secondary=has_location,
        primaryjoin=(has_location.c.event == id),
        secondaryjoin=(has_location.c.location == id),
        backref=db.backref(
            'has_location', lazy='dynamic'), lazy='dynamic')
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'),
        nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    location_type = db.Column(db.String())

    within = db.relationship(
        'Location', secondary=location_within,
        primaryjoin=(location_within.c.contained == id),
        secondaryjoin=(location_within.c.container == id),
        backref=db.backref(
            'location_within', lazy='dynamic'), lazy='dynamic')
    contains = db.relationship(
        'Location', secondary=location_within,
        primaryjoin=(location_within.c.container == id),
        secondaryjoin=(location_within.c.contained == id),
        backref=db.backref(
            'location_within', lazy='dynamic'), lazy='dynamic')

    scenes = db.relationship(
        'Record', secondary=has_location,
        primaryjoin=(has_location.c.location == id),
        secondaryjoin=(has_location.c.event == id),
        backref=db.backref(
            'has_location', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Entrant(db.Model):
    __tablename__ = 'entrants'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'),
        nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'),
        nullable=True)
    desc_ensl = db.relationship(
        'EnslavedDescription', backref='entrant', lazy=True)
    desc_owner = db.relationship(
        'OwnerDescription', backref='entrant', lazy=True)
    has_owner = db.relationship(
        'Entrant', secondary=owned_by,
        primaryjoin=(owned_by.c.enslaved == id),
        secondaryjoin=(owned_by.c.owner == id),
        backref=db.backref('owned_by', lazy='dynamic'), lazy='dynamic')
    owns = db.relationship(
        'Entrant', secondary=owned_by,
        primaryjoin=(owned_by.c.owner == id),
        secondaryjoin=(owned_by.c.enslaved == id),
        backref=db.backref('owned_by', lazy='dynamic'), lazy='dynamic')
    has_parent = db.relationship(
        'Entrant', secondary=child_of,
        primaryjoin=(child_of.c.child == id),
        secondaryjoin=(child_of.c.parent == id),
        backref=db.backref('child_of', lazy='dynamic'), lazy='dynamic')
    parent_of = db.relationship(
        'Entrant', secondary=child_of,
        primaryjoin=(child_of.c.parent == id),
        secondaryjoin=(child_of.c.child == id),
        backref=db.backref('child_of', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    comments = db.Column(db.String())
    references = db.relationship('Entrant', backref='person', lazy=True)

class EnslavedDescription(db.Model):
    __tablename__ = 'description_of_enslaved'

    id = db.Column(db.Integer, primary_key=True)    
    age = db.Column(db.Integer)
    race = db.Column(db.String())
    tribe = db.Column(db.String())
    origin = db.Column(db.String())
    status = db.Column(db.String())
    vocation = db.Column(db.String())
    entrant_id = db.Column(db.Integer, db.ForeignKey('entrants.id'),
        nullable=False)

class OwnerDescription(db.Model):
    __tablename__ = 'description_of_owner'

    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String())
    vocation = db.Column(db.String())
    entrant_id = db.Column(db.Integer, db.ForeignKey('entrants.id'),
        nullable=False)

# location_within = db.Table('location_within',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('contained', db.Integer, db.ForeignKey('location.id')),
#     db.Column('container', db.String())
# )

# has_location = db.Table('has_location',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('event', db.Integer, db.ForeignKey('record.id')),
#     db.Column('location', db.Integer, db.ForeignKey('location.id')),
#     db.Column('location_for', db.String())
# )

# owned_by = db.Table('owned_by',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('enslaved', db.Integer, db.ForeignKey('entrants.id')),
#     db.Column('owner', db.Integer, db.ForeignKey('entrants.id'))
# )

# child_of = db.Table('child_of',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('child', db.Integer, db.ForeignKey('entrants.id')),
#     db.Column('parent', db.Integer, db.ForeignKey('entrants.id'))
# )

# has_spouse = db.Table('has_spouse',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('spouse1', db.Integer, db.ForeignKey('entrants.id')),
#     db.Column('spouse2', db.Integer, db.ForeignKey('entrants.id'))
# )