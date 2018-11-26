class RelationshipMgmt {
  constructor (sectionId, source, $elem) {
    this._section = sectionId;
    this._source = source;
    this._$root  = $elem;
    this._store = new RelationshipStore($elem.find('.rel-store'));
    this._adder = new RelationshipAdder($elem.find('.rel-adder'));
    this._$root[0].addEventListener('click', this);
    this.setUp = this.setUp.bind(this);
  }

  load() {
    this._source.getRelationships(this._section);
  }

  setUp(data) {
    this._store.load(data.store);
    this._adder.load(data.people, data.relationships);
  }

  handleEvent(event) {
    let target = event.target;

    switch(event.type) {
      case "click":
        if (target.classList.contains('add-rel')) {
          var obj = this._adder.getData();
          obj['section'] = this._section;
          this._source.addRelationship(obj);
        } else if (target.classList.contains('del-rel')) {
          var rel_id = parseInt(target.getAttribute('data-rel-id'));
          this._source.deleteRelationship(this._section, rel_id);
        }
        return;
      default:
        return;
    }
  }
}