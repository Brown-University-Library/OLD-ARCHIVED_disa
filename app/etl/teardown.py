from app import db, models

def clear_data(tables=[]):
    disa_models = [
        models.Person,
        models.EntrantRelationship,
        models.RecordLocation,
        models.RecordEdit,
        models.Description,
        models.Entrant,
        models.Role,
        models.Location,
        models.Record,
        models.RecordType,
        models.Document,
        models.DocumentType,
        models.User
    ]
    model_map = { 'documents' : models.Document,
        'records' : models.Record,
        'locations' : models.Location,
        'entrants' : models.Entrant,
        'roles' : models.Role,
        'people' : models.Person,
        'entrant_description' : models.Description,
        'record_types' : models.RecordType,
        'document_types': models.DocumentType
    }
    if not tables:
        del_tables = disa_models
    else:
        del_tables = [ model_map[t] for t in tables ]
    if not del_tables:
        print('Please provide tables to clear')
        return
    for table in del_tables:
        rows = table.query.delete()
        print('Cleared {} rows: {}'.format(rows, table.__tablename__))
        db.session.commit()