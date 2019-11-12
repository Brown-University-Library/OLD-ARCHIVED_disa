class CitationState extends State {

  constructor() {
    super();
    this._slots = ['id', 'display', 'acknowledgements',
      'comments', 'citation_type', 'citation_fields'];
  }

  update(data) {
    super.update(data);
    this._citation_field_name_map = {};
    for (let field_data of this.get('citation_fields') ) {
      this._citation_field_name_map[ field_data.name ] = field_data.value;
    }
  }

  getId() {
    return this.get('id');
  }

  getCitationType() {
    return this.get('citation_type');
  }

  getCitationFields() {
    return this.get('citation_fields').slice(0);
  }

  getComments() {
    return this.get('comments');
  }

  getAcknowledgements() {
    return this.get('acknowledgements');
  }

  getDisplayText() {
    return this.get('display');
  }

  getCitationTypeId() {
    return this.get('citation_type').id;
  }

  getCitationFieldNames() {
    return Object.keys(this._citation_field_name_map);
  }

  getFieldValueByName( name ) {
    return this._citation_field_name_map[ name ];
  }

  isNew() {
    return (this.get('id') === 'new');
  }

  copy() {
    let data = {};
    let dupe = new CitationState();
    for (const slot of this._slots) {
      data[ slot ] = this.get( slot );
    }
    dupe.update(data);
    return dupe;
  }

  modifyCitationType( cType ) {
    let state_copy = this.copy();
    state_copy.set('citation_type', {'id': cType, 'name': ''});
    return state_copy;
  }
}

class ReferenceState extends State {

  constructor() {
    super();
    this._slots = ['id', 'reference_type',
      'link', 'last_edit'];
  }

  getId() {
    return this.get('id');
  }

  getLink() {
    return this.get('link');
  }

  getReferenceType() {
    return this.get('reference_type');
  }

  getLastEdit() {
    return this.get('last_edit');
  }
}

class CitationApp {

  constructor($elem, config, source, cDisplay, cForm, refCtrl) {
    this._$root = $elem;
    this._source = source;
    this._configuration = config;
    this._citation_state = new CitationState();
    this._references_state = [];
    this._$edit_cite = $elem.find('#edit_citation');
    this._$new_ref = $elem.find('#new_reference');
    this._cite_display = cDisplay;
    this._cite_form = cForm;
    this._ref_ctrl = refCtrl;

    this.setEvents();
    this.load(config.get('data'));
  }

  getCitation() {
    return this._citation_state;
  }

  getReferences() {
    return this._references_state;
  }

  setCitation(data) {
    this._citation_state.update(data);
    // this._cite_display.load( this.getCitation() );
    // this._cite_form.load( this.getCitation() );
  }

  setReferences(data) {
    this._references_state = [];
    for (const ref_data of data) {
      let ref = new ReferenceState();
      ref.update(ref_data);
      this._references_state.push(ref);
    }
    this._ref_ctrl.load( this.getReferences() );
  }

  load(data) {
    this.setCitation( data.citation );
    this.setReferences( data.references );

    if ( this.getCitation().isNew() ) {
      this.editCitation();
    } else {
      this.displayCitation();
    }
  }

  editCitation() {
    this._cite_display.show( this.getCitation() );
    this._cite_form.activate( this.getCitation() );
    this._cite_display.hide();
    this._ref_ctrl.hide();
    this._$edit_cite.addClass('hidden');
    this._$new_ref.addClass('hidden');
  }

  displayCitation() {
    this._cite_display.show( this.getCitation() );
    this._ref_ctrl.show( this.getReferences().length );
    this._cite_form.deactivate();
    this._$edit_cite.removeClass('hidden');
    this._$new_ref.removeClass('hidden');
  }

  saveCitation() {
    let data; 

    // if (!this._cite_form.diff(this.data.citation)) {
    //   this.loadCitation(this.data.citation);
    // } 
    data = this._cite_form.read();
    data.id = this.getCitation().getId();
    if ( this.getCitation().isNew() ) {
      this._source.createCitation(data);
    } else {
      this._source.updateCitation(data);
    }
  }

  citationSaved(data) {
    this.setCitation(data.citation);
    this.displayCitation();
  }

  changeCitationType(cType) {
    this._cite_form.changeCitationType(
      this.getCitation().modifyCitationType(cType) );
  }

  editReference(refId) {
    this._ref_ctrl.activateReference(refId);
    this._$edit_cite.prop('disabled', true);
    this._$new_ref.addClass('disabled');
  }

  deleteReference(refId) {
    this._source.deleteReference(refId);
  }

  referenceDeleted(data) {
    this.setReferences(data);
    this._ref_ctrl.show( this.getReferences() );
    this._$edit_cite.prop('disabled', false);
    this._$new_ref.removeClass('disabled');
  }

  resetReferences() {
    this._ref_ctrl.activateReferences();
    this._$edit_cite.prop('disabled', false);
    this._$new_ref.removeClass('disabled');
  }

  setEvents() {
    let app = this;

    this._$root.on('click', '.citation-app-event', function(e){
      e.preventDefault();
      let $clicked = $( this );

      switch ( true ){
        case $clicked.hasClass('edit-citation'):
          app.editCitation();
          break;
        default:
          return;
      }
    });
  }
}