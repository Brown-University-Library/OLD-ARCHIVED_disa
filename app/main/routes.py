from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import main
from .. import db, models, forms

import datetime
import collections
from operator import itemgetter


@main.route('/')
def browse():
    return render_template('browse.html')
     

def parse_person_relations(personObj):
    rels = [ (r.related_as, r.obj) for e in personObj.references
                for r in e.as_subject ]
    grouped = collections.defaultdict(list)
    for r in rels:
        grouped[ r[0].name_as_relationship ].append(
            { 'id': r[1].person_id,
            'name': parse_person_name(r[1].person) } )
    out = [ { 'type': k, 'related': v } for k,v in grouped.items() ]
    return out


def parse_person_name(personObj):
    out = "{0} {1}".format(personObj.first_name, personObj.last_name).strip()
    if out == "":
        return "Unknown"
    return out


def parse_person_descriptors(personObj, descField):
    vals = { desc.name for ref in personObj.references
                for desc in getattr(ref, descField) }
    out = ', '.join(list(vals))
    return out if out else 'None'


@main.route('/people/')
def person_index():
    people = [ p for p in models.Person.query.all() if p.references != [] ]
    return render_template('person_index.html', people=people)


@main.route('/people/<persId>')
def get_person(persId):
    person = models.Person.query.get(persId)
    name = parse_person_name(person)
    tribes = parse_person_descriptors(person, 'tribes')
    origins = parse_person_descriptors(person, 'origins')
    races = parse_person_descriptors(person, 'races')
    statuses = parse_person_descriptors(person, 'enslavements')
    vocations = parse_person_descriptors(person, 'vocations')
    titles = parse_person_descriptors(person, 'titles')
    relations = parse_person_relations(person)
    return render_template('person_display.html',
        name=name, dbId=persId, refs = person.references,
        origins=origins, tribes=tribes, titles=titles,
        races=races, vocations=vocations, statuses=statuses,
        relations=relations)


@main.route('/source/<srcId>')
def get_source(srcId):
    return redirect(url_for('editor.edit_record', recId=srcId))