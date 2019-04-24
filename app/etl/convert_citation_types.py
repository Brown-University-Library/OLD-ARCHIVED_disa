from app import models, db
import csv
import os

def map_citation_types():
    included = [ 'Book', 'Book Section', 'Document', 'Interview',
        'Journal Article', 'Magazine Article', 'Manuscript',
        'Newspaper Article', 'Thesis', 'Webpage' ]
    incl = models.CitationType.query.filter(
        models.CitationType.name.in_(included)).all()
    incl_ids = { c.id for c in incl }
    ct = models.CitationType.query.all()
    ct_map = { c.name: c.id for c in ct }
    mapped = { 'Runaway Capture Advertisement', 'Advertisement of Sale',
        'Runaway Advertisement' }
    cites = models.Citation.query.all()
    out = []
    for c in cites:
        ctype = c.citation_type_id
        if ctype in incl_ids:
            continue
        elif c.citation_type.name in mapped:
            mapped_id = ct_map['Newspaper Article']
        else:
            mapped_id = ct_map['Document']
        out.append(
            (c.id, mapped_id, c.citation_type_id, c.citation_type.name) )
    return out

def update_citations(mapped):
    for m in mapped:
        cite = models.Citation.query.get(m[0])
        cite.citation_type_id = m[1]
        db.session.add(cite)
    db.session.commit()

def convert(dataDir):
    mapped = map_citation_types()
    with open(os.path.join(dataDir, 'citation_type_mappings.csv'), 'w') as f:
        wrtr = csv.writer(f)
        for row in mapped:
            wrtr.writerow(row)
    update_citations(mapped)

if __name__ == '__main__':
    main()