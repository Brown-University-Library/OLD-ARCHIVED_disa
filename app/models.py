from app import db

location_within = db.Table('location_within',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('contained', db.Integer, db.ForeignKey('locations.id')),
    db.Column('container', db.Integer, db.ForeignKey('locations.id'))
)

has_location = db.Table('has_location',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('record', db.Integer, db.ForeignKey('records.id')),
    db.Column('location', db.Integer, db.ForeignKey('locations.id')),
    db.Column('location_for', db.String(255))
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

has_role = db.Table('has_role',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('role', db.Integer, db.ForeignKey('roles.id'))
)

recordtype_roles = db.Table('recordtype_roles',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('record_type', db.Integer, db.ForeignKey('record_types.id')),
    db.Column('role', db.Integer, db.ForeignKey('roles.id'))
)

documenttype_recordtypes = db.Table('documenttype_recordtypes',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('document_type', db.Integer, db.ForeignKey('document_types.id')),
    db.Column('record_type', db.Integer, db.ForeignKey('record_types.id')),
)

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'),
        nullable=False)
    date = db.Column(db.DateTime())
    national_context = db.Column(db.String(255))
    citation = db.Column(db.String(500))
    zotero_id = db.Column(db.String(255))
    comments = db.Column(db.String(255))
    records = db.relationship('Record', backref='document', lazy=True)

    def __repr__(self):
        return '<Document {0}>'.format(self.id)

class DocumentType(db.Model):
    __tablename__ = 'document_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    record_types = db.relationship(
        'RecordType', secondary=documenttype_recordtypes,
        back_populates='document_types')
    documents = db.relationship('Document',
        backref='document_type', lazy=True)

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    record_type_id = db.Column(db.Integer, db.ForeignKey('record_types.id'),
        nullable=False)
    citation = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    comments = db.Column(db.String(255))
    entrants = db.relationship('Entrant', backref='record', lazy=True)
    locations = db.relationship(
        'Location', secondary=has_location,
        back_populates='records')
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'),
        nullable=False)

    def __repr__(self):
        return '<Record {0}>'.format(self.id)

class RecordType(db.Model):
    __tablename__ = 'record_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    records = db.relationship('Record',
        backref='record_type', lazy=True)
    roles = db.relationship(
        'Role', secondary=recordtype_roles,
        back_populates='record_types')
    document_types = db.relationship(
        'DocumentType', secondary=documenttype_recordtypes,
        back_populates='record_types')

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location_type = db.Column(db.String(255))

    within = db.relationship(
        'Location', secondary=location_within,
        primaryjoin=(location_within.c.contained == id),
        secondaryjoin=(location_within.c.container == id),
        backref=db.backref(
            'location_within', lazy='dynamic'), lazy='dynamic')

    records = db.relationship(
        'Record', secondary=has_location,
        back_populates='locations')

    def __repr__(self):
        return '<Location {0}: {1}>'.format(self.id, self.name)

    def place_within(self, locObj):
        self.within.append(locObj)

    def place_for(self, recObj):
        self.records.append(recObj)

class Entrant(db.Model):
    __tablename__ = 'entrants'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'),
        nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'),
        nullable=True)
    description = db.relationship(
        'Description', backref='entrant', lazy=True)
    roles = db.relationship('Role',
        secondary='has_role', back_populates='entrants')
    owners = db.relationship(
        'Entrant', secondary=owned_by,
        primaryjoin=(owned_by.c.enslaved == id),
        secondaryjoin=(owned_by.c.owner == id),
        backref=db.backref('owned_by', lazy='dynamic'), lazy='dynamic')
    parents = db.relationship(
        'Entrant', secondary=child_of,
        primaryjoin=(child_of.c.child == id),
        secondaryjoin=(child_of.c.parent == id),
        backref=db.backref('child_of', lazy='dynamic'), lazy='dynamic')
    spouses = db.relationship(
        'Entrant', secondary=has_spouse,
        primaryjoin=(has_spouse.c.spouse1 == id),
        secondaryjoin=(has_spouse.c.spouse2 == id),
        backref=db.backref('has_spouse', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Entrant {0}: {1} {2}>'.format(
            self.id, self.first_name, self.last_name)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description_group = db.Column(db.Integer)
    entrants = db.relationship('Entrant',
        secondary='has_role', back_populates='roles')
    record_types = db.relationship(
        'RecordType', secondary=recordtype_roles,
        back_populates='roles')

class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    comments = db.Column(db.String(255))
    references = db.relationship('Entrant', backref='person', lazy=True)

class Description(db.Model):
    __tablename__ = 'entrant_description'

    id = db.Column(db.Integer, primary_key=True)    
    age = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    title = db.Column(db.String(255))
    race = db.Column(db.String(255))
    tribe = db.Column(db.String(255))
    origin = db.Column(db.String(255))
    status = db.Column(db.String(255))
    vocation = db.Column(db.String(255))
    entrant_id = db.Column(db.Integer, db.ForeignKey('entrants.id'),
        nullable=False)
