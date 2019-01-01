from app import db, models

def clear_data(tables=[]):
    many_to_many = [
        models.has_role,
        models.has_title,
        models.has_vocation,
        models.has_race,
        models.has_tribe,
        models.has_origin,
        models.enslaved_as,
        models.referencetype_roles,
        models.citationtype_referencetypes,
        models.zoterotype_fields
    ]
    disa_models = [
        models.ReferentRelationship,
        models.ReferenceLocation,
        models.ReferenceEdit,
        models.Tribe,
        models.Race,
        models.Title,
        models.Vocation,
        models.EnslavementType,
        models.ReferentName,
        models.NameType,
        models.Referent,
        models.Person,
        models.Role,
        models.Location,
        models.Reference,
        models.ReferenceType,
        models.CitationField,
        models.Citation,
        models.CitationType,
        models.User,
        models.ZoteroType,
        models.ZoteroField
    ]
    model_map = { 'citations' : models.Citation,
        'references' : models.Reference,
        'locations' : models.Location,
        'referents' : models.Referent,
        'roles' : models.Role,
        'people' : models.Person,
        'reference_types' : models.ReferenceType,
        'citation_types': models.CitationType
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