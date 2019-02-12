from app import db, models
import datetime

def load_existing_users():
    mongo_users = [
        { 'email':'cole_hansen@brown.edu', 'role':'Admin' },
        { 'email':'linfordfisher@gmail.com', 'role':'Admin' },
        { 'email':'elli_mylonas@brown.edu', 'role':'Admin' },
        { 'email':'anne_grasberger@brown.edu', 'role':'Admin' },
        { 'email':'marley-vincent_lindsey@brown.edu', 'role':'Admin' },
        { 'email':'rose_lang-maso@brown.edu', 'role':'Admin' },
        { 'email':'jane.l.landers@vanderbilt.edu', 'role':'User' },
        { 'email':'ymiki1@fordham.edu', 'role':'User' },
        { 'email':'gomalley@ucsc.edu', 'role':'User' },
        { 'email':'aresendez@ucdavis.edu', 'role':'User' },
        { 'email':'navandeu@gmail.com', 'role':'User' },
        { 'email':'brett.rushforth@gmail.com', 'role':'User' },
        { 'email':'paarul_sukanya_arulappa@brown.edu', 'role':'Admin' },
        { 'email':'samuel_skinner@brown.edu', 'role':'User' },
        { 'email':'luna_mcnulty@brown.edu', 'role':'Admin' },
        { 'email':'ashley_champagne@brown.edu', 'role':'Admin' },
        { 'email':'gwenyth_winship@brown.edu', 'role':'Admin' },
        { 'email':'juan_bettancourt-garcia@brown.edu', 'role':'Admin' },
        { 'email':'disagrantreview@gmail.com', 'role':'User'}
    ]

    for user in mongo_users:
        existing = models.User.query.filter_by(email=user['email']).first()
        if existing:
            raise
        row = models.User(name=user['email'],
            email=user['email'],role=user['role'],
            created=datetime.datetime.utcnow())
        db.session.add(row)
    db.session.commit()

def make_current_users(passw):
    to_be_created = [
        ('Antonio Taylor', 'antonio_taylor@brown.edu'),
        ('Anchita Dasgupta','anchita_dasgupta@brown.edu'),
        ('Juan Colin','juan_colin@brown.edu'),
        ('Jeanne Ernest','jeanne_ernest@brown.edu'),
        ('Alexander Samaha','alexander_samaha@brown.edu'),
        ('Frishta Qaderi','frishta_qaderi@brown.edu'),
        ('Ben Bienstock','benjamin_bienstock@brown.edu'),
        ('Justin Han','justin_han@brown.edu'),
        ('Kanha Prasad','kanha_prasad@brown.edu'),
        ('Ingrid Mader', 'ingrid_mader@brown.edu')
    ]
    new_users = []
    for user in to_be_created:
        existing = models.User.query.filter_by(email=user[1]).first()
        if existing:
            continue
        new_users.append(
            models.User(name=user[0],email=user[1],role='User',
            created=datetime.datetime.utcnow())
        )
    for user in new_users:
        db.session.add(user)
    db.session.commit()

    for user in new_users:
        print("Created user {} | email {}".format(user.name, user.email))
        user.set_password(passw)
        print("Password set for user {}".format(user.name))
        db.session.add(user)
    db.session.commit()