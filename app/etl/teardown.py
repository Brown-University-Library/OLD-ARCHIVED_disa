from app import db, models

def clear_data(tables=[]):
    many_to_many = [
        models.has_role,
        models.recordtype_roles,
        models.documenttype_recordtypes
    ]
    disa_models = [
        models.EntrantRelationship,
        models.RecordLocation,
        models.RecordEdit,
        models.Description,
        models.Entrant,
        models.Person,
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
    for table in many_to_many:
        db.engine.execute(table.delete())
    for table in del_tables:
        rows = table.query.delete()
        print('Cleared {} rows: {}'.format(rows, table.__tablename__))
        db.session.commit()