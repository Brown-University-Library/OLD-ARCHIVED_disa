import operator
import datetime as dt

from . import db, login_manager

from werkzeug import security
from flask_login import UserMixin

NEW_ID = 'new'


class TypeMixin(object):

    @classmethod
    def get_default(cls):
        with db.session.no_autoflush:
            if not cls._default:
                raise ReferenceError(
                            'No default instance set for {}'.format(
                                cls.__name__))
            try:
                default = cls.query.filter_by(**cls._default).first()
            except:
                raise ReferenceError(
                    'Default instance of {} not found'.format(
                        cls.__name__))
            return default

    def to_dict(self):
        return { 'id': self.id, 'name': self.name }

    def __repr__(self):
        return '<{0} {1}: {2}>'.format(self.__class__.__name__,
            self.id, self.name)


class TagMixin(TypeMixin):

    @classmethod
    def get_or_create(cls, commit=False, **kwargs):
        with db.session.no_autoflush:
            if not kwargs:
                raise KeyError(
                    'Missing required data for get or create {}'.format(
                        cls.__name__))
            existing = cls.query.filter_by(**kwargs).first()
            if existing:
                return existing
            else:
                created = cls(**kwargs)
                db.session.add(created)
                if commit:
                    db.session.commit()
                return created


has_role = db.Table('6_has_role',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('role', db.Integer, db.ForeignKey('1_roles.id'))
)

has_title = db.Table('6_has_title',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('title', db.Integer, db.ForeignKey('1_titles.id'))
)

has_vocation = db.Table('6_has_vocation',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('vocation', db.Integer, db.ForeignKey('1_vocations.id'))
)

has_tribe = db.Table('6_has_tribe',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('tribe', db.Integer, db.ForeignKey('1_tribes.id'))
)

has_race = db.Table('6_has_race',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('race', db.Integer, db.ForeignKey('1_races.id'))
)

has_origin = db.Table('6_has_origin',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('origin', db.Integer, db.ForeignKey('1_locations.id'))
)

enslaved_as = db.Table('6_enslaved_as',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('referent', db.Integer, db.ForeignKey('5_referents.id')),
    db.Column('enslavement', db.Integer,
        db.ForeignKey('1_enslavement_types.id'))
)

referencetype_roles = db.Table('2_referencetype_roles',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('reference_type', db.Integer, db.ForeignKey('1_reference_types.id')),
    db.Column('role', db.Integer, db.ForeignKey('1_roles.id'))
)

citationtype_referencetypes = db.Table('3_citationtype_referencetypes',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('citation_type', db.Integer, db.ForeignKey('2_citation_types.id')),
    db.Column('reference_type', db.Integer, db.ForeignKey('1_reference_types.id')),
)


class Citation(db.Model):
    __tablename__ = '3_citations'

    id = db.Column(db.Integer, primary_key=True)
    citation_type_id = db.Column(db.Integer, db.ForeignKey('2_citation_types.id'),
        nullable=False)
    display = db.Column(db.String(500))
    zotero_id = db.Column(db.String(255))
    comments = db.Column(db.UnicodeText())
    acknowledgements = db.Column(db.String(255))
    references = db.relationship('Reference', backref='citation', lazy=True)

    def to_dict(self=None):
        data = {
            'id': NEW_ID,
            'display': '',
            'acknowledgements': '',
            'comments': '',
            'citation_type': CitationType.get_default().to_dict(),
            'citation_fields': []
        }
        if self:
            data['id'] = self.id
            data['display'] = self.display
            data['comments'] = self.comments
            data['acknowledgements'] = self.acknowledgements
            data['citation_type'] = {'id': self.citation_type_id,
                'name': self.citation_type.name }
            data['citation_fields'] = [
                { 'name': f.field.name, 'value': f.field_data }
                    for f in self.citation_data  ]
        return data

    def __repr__(self):
        return '<Citation {0}: {1}>'.format(self.id, self.display)


class CitationType(TypeMixin, db.Model):
    __tablename__ = '2_citation_types'
    _default = {'name': 'Document'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    zotero_type_id = db.Column(db.Integer, db.ForeignKey('1_zotero_types.id'),
        nullable=False)
    reference_types = db.relationship(
        'ReferenceType', secondary=citationtype_referencetypes,
        back_populates='citation_types')
    citations = db.relationship('Citation',
        backref='citation_type', lazy=True)


class ZoteroType(db.Model):
    __tablename__ = '1_zotero_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) 
    creator_name = db.Column(db.String(255))
    citation_types = db.relationship('CitationType',
        backref='zotero_type', lazy=True)


class ZoteroField(db.Model):
    __tablename__ = '1_zotero_fields'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) 
    display_name = db.Column(db.String(255))


class ZoteroTypeField(db.Model):
    __tablename__ = '2_zoterotype_fields'

    id = db.Column(db.Integer, primary_key=True)
    zotero_type_id = db.Column(db.Integer, db.ForeignKey('1_zotero_types.id'))
    zotero_field_id = db.Column(db.Integer, db.ForeignKey('1_zotero_fields.id'))
    rank = db.Column(db.Integer)
    zotero_type = db.relationship(ZoteroType,
        primaryjoin=(zotero_type_id == ZoteroType.id),
        backref='template_fields')
    zotero_field = db.relationship(ZoteroField,
        primaryjoin=(zotero_field_id == ZoteroField.id),
        backref='templates')


class CitationField(db.Model):
    __tablename__ = '4_citation_fields'

    id = db.Column(db.Integer, primary_key=True)
    citation_id = db.Column(db.Integer, db.ForeignKey('3_citations.id'))
    field_id = db.Column(db.Integer, db.ForeignKey('1_zotero_fields.id'))
    field_data = db.Column(db.String(255))
    citation = db.relationship(Citation,
        primaryjoin=(citation_id == Citation.id),
        backref='citation_data')
    field = db.relationship(ZoteroField,
        primaryjoin=(field_id == ZoteroField.id),
        backref='citations')


class Reference(db.Model):
    __tablename__ = '4_references'

    id = db.Column(db.Integer, primary_key=True)
    citation_id = db.Column(db.Integer, db.ForeignKey('3_citations.id'),
        nullable=False)
    reference_type_id = db.Column(db.Integer, db.ForeignKey('1_reference_types.id'),
        nullable=False)
    national_context_id = db.Column(db.Integer, db.ForeignKey('1_national_context.id'),
        nullable=False)
    date = db.Column(db.DateTime())
    month = db.Column(db.Integer())
    day = db.Column(db.Integer())
    year = db.Column(db.Integer())
    date_text = db.Column(db.String(255))
    transcription = db.Column(db.UnicodeText())
    referents = db.relationship(
        'Referent', backref='reference', lazy=True, cascade="delete")

    def last_edit(self):
        edits = sorted([ (e.timestamp, e) for e in self.edits ],
             key=operator.itemgetter(0), reverse=True)
        return edits[0][1]

    def formatted_date(self):
        dt_str = '{} '.format(self.date_text) if self.date_text else ''
        day = self.day
        month = self.month
        year = self.year
        dt_data = dt.datetime(year=year or 1492, month=month or 1, day=day or 1)
        if month and day and year:
            dt_str += dt_data.strftime('%B %d %Y')
        elif month and day and not year:
            dt_str += dt_data.strftime('%B %d')
        elif month and not day and year:
            dt_str += dt_data.strftime('%B %Y')
        elif month and not day and not year:
            dt_str += dt_data.strftime('%B')
        elif not month and day and year:
            dt_str += dt_data.strftime('%d %Y')
        elif not month and day and not year:
            dt_str += dt_data.strftime('%d')
        elif not month and not day and year:
            dt_str += dt_data.strftime('%Y')
        elif not (month or day or year or dt_str) :
            dt_str = 'Unrecorded'
        return dt_str

    def to_dict(self=None):
        data = {
            'id': NEW_ID,
            'citation': {'id': '', 'name': '' },
            'reference_type': ReferenceType.get_default().to_dict(),
            'date': { 'day': 0, 'month': 0, 'year': 0, 'text': '' },
            'national_context': { 'id': '', 'name': '' },
            'locations': [],
            'transcription': '',
        }
        if self:
            data['citation'] = { 'id': self.citation_id,
                'name': self.citation.display }
            data['id'] = self.id
            data['reference_type'] = {'id': self.reference_type_id,
                'name': self.reference_type.name }
            data['date'] = { 'day': self.day, 'month': self.month,
                'year': self.year, 'date_text': self.date_text,
                'formatted': self.formatted_date() }
            data['national_context'] = { 'id': self.national_context_id,
                'name': self.national_context.name }
            data['locations'] = [ loc.to_dict() for loc in self.locations ]
            data['transcription'] = self.transcription
        return data

    def __repr__(self):
        return '<Reference {0}: {1} in Citation {2}>'.format(
            self.id, self.reference_type.name, self.citation_id)


class ReferenceType(TagMixin, db.Model):
    __tablename__ = '1_reference_types'
    _default = {'name': 'Unspecified'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    references = db.relationship('Reference',
        backref='reference_type', lazy=True)
    roles = db.relationship(
        'Role', secondary=referencetype_roles,
        back_populates='reference_types')
    citation_types = db.relationship(
        'CitationType', secondary=citationtype_referencetypes,
        back_populates='reference_types')


class Location(TagMixin, db.Model):
    __tablename__ = '1_locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    origin_for = db.relationship('Referent',
        secondary=has_origin, back_populates='origins')


class ReferenceLocation(db.Model):
    __tablename__ = '5_has_location'

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.Integer, db.ForeignKey('4_references.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('1_locations.id'))
    location_type_id = db.Column(db.Integer, db.ForeignKey('1_location_types.id'))
    location_rank = db.Column(db.Integer)
    reference = db.relationship(Reference,
        primaryjoin=(reference_id == Reference.id),
        backref='locations')
    location = db.relationship(Location,
        primaryjoin=(location_id == Location.id),
        backref='references')

    def to_dict(self):
        return {
            'id': self.location.id,
            'name': self.location.name,
            'location_type': self.location_type.to_dict(),
            'location_rank': self.location_rank
        }

    def __repr__(self):
        return '<Location for Reference {0}: {1} as {2}>'.format(
            self.reference_id, self.location.name, self.location_type.name)


class LocationType(TagMixin, db.Model):
    __tablename__ = '1_location_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    locations = db.relationship(
        'ReferenceLocation', backref='location_type', lazy=True)


class NationalContext(TypeMixin, db.Model):
    __tablename__ = '1_national_context'
    _default = {'name': 'Other'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    references = db.relationship('Reference', backref='national_context', lazy=True)


class NameType(db.Model):
    __tablename__ = '1_name_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<NameType {0}: {1}>'.format(self.id, self.name)


class ReferentName(db.Model):
    __tablename__ = '6_referent_names'

    id = db.Column(db.Integer, primary_key=True)
    referent_id = db.Column(db.Integer, db.ForeignKey('5_referents.id'))
    name_type_id = db.Column(db.Integer, db.ForeignKey('1_name_types.id'))
    first = db.Column(db.String(255))
    last = db.Column(db.String(255))
    name_type = db.relationship('NameType',
        primaryjoin=(name_type_id == NameType.id) )

class Referent(db.Model):
    __tablename__ = '5_referents'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    primary_name_id = db.Column(db.Integer, 
        db.ForeignKey('6_referent_names.id'),
        nullable=True)
    reference_id = db.Column(db.Integer, db.ForeignKey('4_references.id'),
        nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('1_people.id'),
        nullable=True)
    names = db.relationship('ReferentName',
        primaryjoin=(id == ReferentName.referent_id),
        backref='referent', cascade='delete')
    primary_name = db.relationship('ReferentName',
        primaryjoin=(primary_name_id == ReferentName.id),
        post_update=True )
    roles = db.relationship('Role',
        secondary=has_role, back_populates='referents')
    tribes = db.relationship('Tribe',
        secondary=has_tribe, back_populates='referents')
    races = db.relationship('Race',
        secondary=has_race, back_populates='referents')
    titles = db.relationship('Title',
        secondary=has_title, back_populates='referents')
    vocations = db.relationship('Vocation',
        secondary=has_vocation, back_populates='referents')
    origins = db.relationship('Location',
        secondary=has_origin, back_populates='origin_for')
    enslavements = db.relationship('EnslavementType',
        secondary=enslaved_as, back_populates='referents')

    def __repr__(self):
        return '<Referent {0}: {1}>'.format(
            self.id, self.display_name() )

    def display_name(self):
        display = "{0} {1}".format(
            self.primary_name.first, self.primary_name.last).strip()
        if display == "":
            return "Unknown"
        else:
            return display


class Title(TagMixin, db.Model):
    __tablename__ = '1_titles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    referents = db.relationship('Referent',
        secondary=has_title, back_populates='titles')


class Tribe(TagMixin, db.Model):
    __tablename__ = '1_tribes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    referents = db.relationship('Referent',
        secondary=has_tribe, back_populates='tribes')


class Race(TagMixin, db.Model):
    __tablename__ = '1_races'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    referents = db.relationship('Referent',
        secondary=has_race, back_populates='races')


class Vocation(TagMixin, db.Model):
    __tablename__ = '1_vocations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    referents = db.relationship('Referent',
        secondary=has_vocation, back_populates='vocations')


class EnslavementType(TagMixin, db.Model):
    __tablename__ = '1_enslavement_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    referents = db.relationship('Referent',
        secondary=enslaved_as, back_populates='enslavements')
    

class Role(TagMixin, db.Model):
    __tablename__ = '1_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    name_as_relationship = db.Column(db.String(255))
    referents = db.relationship('Referent',
        secondary=has_role, back_populates='roles')
    reference_types = db.relationship(
        'ReferenceType', secondary=referencetype_roles,
        back_populates='roles')


class ReferentRelationship(db.Model):
    __tablename__ = '6_referent_relationships'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('5_referents.id'))
    object_id = db.Column(db.Integer, db.ForeignKey('5_referents.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('1_roles.id'))
    sbj = db.relationship(Referent,
        primaryjoin=(subject_id == Referent.id),
        backref=db.backref('as_subject', cascade='delete'))
    obj = db.relationship(Referent,
        primaryjoin=(object_id == Referent.id),
        backref=db.backref('as_object', cascade='delete'))
    related_as = db.relationship(Role,
        primaryjoin=(role_id == Role.id),
        backref='describes')

    def entailed_relationships(self):
        implied = []
        entailed = RoleRelationship.query.filter_by(role1=self.role_id).all()
        for e in entailed:
            implied.append(e.entail_relationships(
                self.subject_id, self.object_id))
        return implied


class RoleRelationship(db.Model):
    __tablename__ = '2_role_relationships'

    id = db.Column(db.Integer, primary_key=True)
    role1 = db.Column(db.Integer, db.ForeignKey('1_roles.id'))
    role2 = db.Column(db.Integer, db.ForeignKey('1_roles.id'))
    relationship_type = db.Column(db.Integer,
        db.ForeignKey('1_role_relationship_types.id'))
    alternate_text = db.Column(db.String(255))

    def entail_role(self):
        pass

    def entail_relationships(self, sbjId, objId):
        if self.related_as.name == 'inverse':
            return ReferentRelationship(
                subject_id=objId, role_id=self.role2, object_id=sbjId)
        elif self.related_as.name == 'is_a':
            return ReferentRelationship(
                subject_id=sbjId, role_id=self.role2, object_id=objId)
        else:
            return


class RoleRelationshipType(TagMixin, db.Model):
    __tablename__ = '1_role_relationship_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    relationships = db.relationship(
        'RoleRelationship', backref='related_as', lazy=True)


class Person(db.Model):
    __tablename__ = '1_people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    comments = db.Column(db.String(255))
    references = db.relationship('Referent', backref='person', lazy=True)

    @classmethod
    def filter_on_description(cls, desc):
        return cls.query.join(
            cls.references).join(Referent.roles).filter(Role.name==desc)

    def display_name(self):
        display = "{0} {1}".format(
            self.first_name, self.last_name).strip()
        if display == "":
            return "Unknown"
        else:
            return display

    def display_attr(self, attr):
        vals = { desc.name for ref in self.references
            for desc in getattr(ref, attr) }
        return ', '.join(list(vals))


class User(UserMixin, db.Model):
    __tablename__ = '1_users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64))
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    created = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        try:
            return security.check_password_hash(self.password_hash, password)
        except:
            return None

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class ReferenceEdit(db.Model):
    __tablename__ = '5_reference_edits'

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.Integer, db.ForeignKey('4_references.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('1_users.id'))
    timestamp = db.Column(db.DateTime())
    edited = db.relationship(Reference,
        primaryjoin=(reference_id == Reference.id),
        backref='edits')
    edited_by = db.relationship(User,
        primaryjoin=(user_id == User.id),
        backref='edits')
