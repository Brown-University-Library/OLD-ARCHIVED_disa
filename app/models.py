from app import db, login

from werkzeug import security
from flask_login import UserMixin

has_role = db.Table('has_role',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('role', db.Integer, db.ForeignKey('roles.id'))
)

has_title = db.Table('has_title',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('title', db.Integer, db.ForeignKey('titles.id'))
)

has_vocation = db.Table('has_vocation',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('vocation', db.Integer, db.ForeignKey('vocations.id'))
)

has_tribe = db.Table('has_tribe',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('tribe', db.Integer, db.ForeignKey('tribes.id'))
)

has_race = db.Table('has_race',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('race', db.Integer, db.ForeignKey('races.id'))
)

has_origin = db.Table('has_origin',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('origin', db.Integer, db.ForeignKey('locations.id'))
)

enslaved_as = db.Table('enslaved_as',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('entrant', db.Integer, db.ForeignKey('entrants.id')),
    db.Column('enslavement', db.Integer,
        db.ForeignKey('enslavement_types.id'))
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
    comments = db.Column(db.UnicodeText())
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
    origin_for = db.relationship('Entrant',
        secondary='has_origin', back_populates='origins')

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

class NameType(db.Model):
    __tablename__ = 'name_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class EntrantName(db.Model):
    __tablename__ = 'entrant_names'

    id = db.Column(db.Integer, primary_key=True)
    entrant_id = db.Column(db.Integer, db.ForeignKey('entrants.id'))
    name_type_id = db.Column(db.Integer, db.ForeignKey('name_types.id'))
    first = db.Column(db.String(255))
    last = db.Column(db.String(255))
    name_type = db.relationship('NameType',
        primaryjoin=(name_type_id == NameType.id) )

class Entrant(db.Model):
    __tablename__ = 'entrants'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    primary_name_id = db.Column(db.Integer, 
        db.ForeignKey('entrant_names.id'))
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'),
        nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'),
        nullable=True)
    names = db.relationship('EntrantName',
        primaryjoin=(id == EntrantName.entrant_id) )
    primary_name = db.relationship('EntrantName',
        primaryjoin=(primary_name_id == EntrantName.id),
        post_update=True )
    roles = db.relationship('Role',
        secondary='has_role', back_populates='entrants')
    tribes = db.relationship('Tribe',
        secondary='has_tribe', back_populates='entrants')
    races = db.relationship('Race',
        secondary='has_race', back_populates='entrants')
    titles = db.relationship('Title',
        secondary='has_title', back_populates='entrants')
    vocations = db.relationship('Vocation',
        secondary='has_vocation', back_populates='entrants')
    origins = db.relationship('Location',
        secondary='has_origin', back_populates='origin_for')
    enslavements = db.relationship('EnslavementType',
        secondary='enslaved_as', back_populates='entrants')

    def __repr__(self):
        return '<Entrant {0}: {1} {2}>'.format(
            self.id, self.first_name, self.last_name)

class Title(db.Model):
    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    entrants = db.relationship('Entrant',
        secondary='has_title', back_populates='titles')

class Tribe(db.Model):
    __tablename__ = 'tribes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    entrants = db.relationship('Entrant',
        secondary='has_tribe', back_populates='tribes')

class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    entrants = db.relationship('Entrant',
        secondary='has_race', back_populates='races')

class Vocation(db.Model):
    __tablename__ = 'vocations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    entrants = db.relationship('Entrant',
        secondary='has_vocation', back_populates='vocations')

class EnslavementType(db.Model):
    __tablename__ = 'enslavement_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    entrants = db.relationship('Entrant',
        secondary='enslaved_as', back_populates='enslavements')

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

    @classmethod
    def filter_on_description(cls, desc):
        return cls.query.join(
            cls.references).join(Entrant.roles).filter(Role.name==desc)

class User(UserMixin, db.Model):
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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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