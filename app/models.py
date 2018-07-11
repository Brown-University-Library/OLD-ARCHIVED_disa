from werkzeug import security
from app import db


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
    citation = db.Column(db.String(500))
    zotero_id = db.Column(db.String(255))
    acknowledgements = db.Column(db.String(255))
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

    def __repr__(self):
        return '<Location {0}: {1}>'.format(self.id, self.name)

class RecordLocation(db.Model):
    __tablename__ = 'has_location'

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location_rank = db.Column(db.Integer)
    record = db.relationship(Record,
        primaryjoin=(record_id == Record.id),
        backref='locations')
    location = db.relationship(Location,
        primaryjoin=(location_id == Location.id),
        backref='records')

class Entrant(db.Model):
    __tablename__ = 'entrants'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'),
        nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'),
        nullable=True)
    roles = db.relationship('Role',
        secondary='has_role', back_populates='entrants')
    description = db.relationship('Description',
        backref='entrant', uselist=False)

    def __repr__(self):
        return '<Entrant {0}: {1} {2}>'.format(
            self.id, self.first_name, self.last_name)

class Description(db.Model):
    __tablename__ = 'entrant_description'

    id = db.Column(db.Integer, primary_key=True)    
    age = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    title = db.Column(db.String(255))
    race = db.Column(db.String(255))
    tribe = db.Column(db.String(255))
    origin = db.Column(db.String(255))
    vocation = db.Column(db.String(255))
    entrant_id = db.Column(db.Integer, db.ForeignKey('entrants.id'),
        nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    entrants = db.relationship('Entrant',
        secondary='has_role', back_populates='roles')
    record_types = db.relationship(
        'RecordType', secondary=recordtype_roles,
        back_populates='roles')

class EntrantRelationship(db.Model):
    __tablename__ = 'entrant_relationships'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('entrants.id'))
    object_id = db.Column(db.Integer, db.ForeignKey('entrants.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sbj = db.relationship(Entrant,
        primaryjoin=(subject_id == Entrant.id),
        backref='as_subject')
    obj = db.relationship(Entrant,
        primaryjoin=(object_id == Entrant.id),
        backref='as_object')
    related_as = db.relationship(Role,
        primaryjoin=(role_id == Role.id),
        backref='describes')

class RoleRelationship(db.Model):
    __tablename__ = 'role_relationships'

    id = db.Column(db.Integer, primary_key=True)
    role1 = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role2 = db.Column(db.Integer, db.ForeignKey('roles.id'))
    relationship_type = db.Column(db.Integer,
        db.ForeignKey('role_relationship_types.id'))
    alternate_text = db.Column(db.String(255))

class RoleRelationshipTypes(db.Model):
    __tablename__ = 'role_relationship_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    comments = db.Column(db.String(255))
    references = db.relationship('Entrant', backref='person', lazy=True)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64))
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)

class RecordEdit(db.Model):
    __tablename__ = 'record_edits'

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    datetime = db.Column(db.DateTime())
    edited = db.relationship(Record,
        primaryjoin=(record_id == Record.id),
        backref='edits')
    edited_by = db.relationship(User,
        primaryjoin=(user_id == User.id),
        backref='edits')