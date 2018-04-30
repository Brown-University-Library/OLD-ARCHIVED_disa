from app import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    doctype = db.Column(db.String())
    nation = db.Column(db.String())
    state = db.Column(db.String())
    date = db.Column(db.Date())
    citation = db.Column(db.String())
    records = db.relationship('records', backref='documents', lazy=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    rectype = db.Column(db.String())
    date = db.Column(db.Date())
    comments = db.Column(db.String())
    actors = db.relationship('actors', backref='records', lazy=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'),
        nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    age = db.Column(db.Integer)
    race = db.Column(db.String())
    tribe = db.Column(db.String())
    origin = db.Column(db.String())
    status = db.Column(db.String())
    vocation = db.Column(db.String())
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'),
        nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'),
        nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    references = db.relationship('actors', backref='people', lazy=True)

owned_by = db.Table('owned_by',
    db.Column('enslaved', db.Integer,
        db.ForeignKey('actors.id'), primary_key=True),
    db.Column('owner', db.Integer,
        db.ForeignKey('actors.id'), primary_key=True)
)

child_of = db.Table('child_of',
    db.Column('child', db.Integer,
        db.ForeignKey('actors.id'), primary_key=True),
    db.Column('parent', db.Integer,
        db.ForeignKey('actors.id'), primary_key=True)
)

has_spouse = db.Table('has_spouse',
    db.Column('spouse1', db.Integer,
        db.ForeignKey('actors.id'), primary_key=True),
    db.Column('spouse2', db.Integer,
        db.ForeignKey('actors.id'), primary_key=True)
)