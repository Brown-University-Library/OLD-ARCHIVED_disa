from app import db, models
import datetime
import json

def load_existing_users():
    mongo_users = []

    for user in mongo_users:
        existing = models.User.query.filter_by(email=user['email']).first()
        if existing:
            raise
        row = models.User(name=user['email'],
            email=user['email'],role=user['role'],
            created=datetime.datetime.utcnow())
        db.session.add(row)
    db.session.commit()

def make_current_users(jsonFile):
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    new_users = []
    for user in data['active']:
        existing = models.User.query.filter_by(email=user['email']).first()
        if existing:
            continue
        user['created'] = datetime.datetime.utcnow()
        new_users.append(
            models.User(**user)
        )
    for user in new_users:
        db.session.add(user)
        print("Creating user: {}".format(user.email))
    db.session.commit()

def update_password(jsonFile, passw):
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    for user in data['passwords']:
        existing = models.User.query.filter_by(email=user['email']).first()
        if not existing:
            continue
        existing.set_password(passw)
        print("Password set for user {}".format(existing.email))
        db.session.add(existing)
    db.session.commit()

def remove_users(jsonFile):
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    for user in data['remove']:
        existing = models.User.query.filter_by(email=user['email']).first()
        if existing:
            print("Removing user by email: {}".format(existing.email))
            db.session.delete(existing)
    db.session.commit()