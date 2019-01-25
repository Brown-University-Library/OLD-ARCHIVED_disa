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