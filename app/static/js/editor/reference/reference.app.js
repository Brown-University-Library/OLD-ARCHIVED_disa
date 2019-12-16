class ReferenceState extends State {

  constructor() {
    super();
    this._slots = ['id', 'reference_type',
      'citation', 'locations', 'date',
      'national_context', 'transcription'];
  }

  getId() {
    return this.get('id');
  }

  getCitation() {
    return this.get('citation');
  }

  getRefType() {
    return this.get('reference_type');
  }

  getNatlContext() {
    return this.get('national_context');
  }

  getDate() {
    return this.get('date');
  }

  getTranscription() {
    return this.get('transcription');
  }

  getLocations() {
    return this.get('locations');
  }

  getLocationsByTypeName(name) {
    return this.get('locations').filter(
      loc => loc.location_type.name == name);
  }

  isNew() {
    return (this.get('id') === 'new');
  }

  displayCitation() {
    return this.get('citation').name;
  }

  displayRefType() {
    return this.get('reference_type').name;
  }

  displayNatlContext() {
    return this.get('national_context').name;
  }
}

class ReferentState extends State {

  constructor() {
    super();
    this._slots = ['id', 'first_name',
      'last_name', 'tags', 'referent_link'];
  }

  getId() {
    return this.get('id');
  }

  getFirstName() {
    return this.get('first_name');
  }

  getLastName() {
    return this.get('last_name');
  }

  getTags() {
    return this.get('tags');
  }

  getDetailsLink() {
    return this.get('referent_link');
  }
}

class ReferenceApp {

  constructor($elem, config, source, refDisplay, refForm, rntCtrl) {
    this._$root = $elem;
    this._source = source;
    this._configuration = config;
    this._reference_state = new ReferenceState();
    this._referents_state = [];
    this._$edit_ref = $elem.find('#edit_reference');
    this._$new_rnt = $elem.find('#new_referent');
    this._ref_display = refDisplay;
    this._ref_form = refForm;
    this._rnt_ctrl = rntCtrl;

    this.setEvents();
    this.load(config.get('data'));
  }

  getReference() {
    return this._reference_state;
  }

  setReference(data) {
    this._reference_state.update(data);
  }

  getReferents() {
    return this._referents_state;
  }

  setReferents(data) {
    this._referents_state = [];
    for (const ref_data of data) {
      let ref = new ReferentState();
      ref.update(ref_data);
      this._referents_state.push(ref);
    }
    this._rnt_ctrl.load( this.getReferents() );
  }

  load(data) {
    this.setReference(data.reference);
    this.setReferents(data.referents);
    if (this._reference_state.isNew()) {
      this.editReference();
    } else {
      this.displayReference();
    }
  }

  editReference() {
    this._ref_display.hide();
    this._rnt_ctrl.hide();
    this._$edit_ref.addClass('hidden');
    this._$new_rnt.addClass('hidden');
    this._ref_form.activate( this.getReference() );
  }

  saveReference() {
    let data; 

    data = this._ref_form.read();
    data.citation = this.getReference().getCitation();
    if ( this.getReference().isNew() ) {
      this._source.createReference(data);
    } else {
      this._source.updateReference(data);
    }
  }

  referenceSaved(data) {
    this.setReference(data.reference);
    this.displayReference();
  }

  displayReference() {
    this._ref_form.deactivate();
    this._$edit_ref.removeClass('hidden');
    this._$new_rnt.removeClass('hidden');
    this._ref_display.show( this.getReference() );
    this._rnt_ctrl.show( this.getReferents().length );
  }

  // changeReferenceType(cType) {
  //   this._cite_form.changeReferenceType(cType);
  // }

  // editReferent(rntId) {
  //   this._rnt_ctrl.activateReferent(rntId);
  //   this._$edit_ref.prop('disabled', true);
  //   this._$new_rnt.addClass('hidden');
  // }

  // deleteReferent(rntId) {
  //   this._source.deleteReferent(rntId);
  // }

  // referentDeleted(data) {
  //   this._rnt_ctrl.load(data.referents);
  //   this._$edit_ref.prop('disabled', false);
  //   this._$new_ref.removeClass('hidden');
  // }

  // resetReferents() {
  //   this._ref_ctrl.activate();
  //   this._$edit_cite.prop('disabled', false);
  //   this._$new_ref.removeClass('hidden');
  // }

  setEvents() {
    let app = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $clicked = $( this );

      switch ( true ){
        case $clicked.hasClass('edit-reference'):
          app.editReference();
          break;
        default:
          return;
      }
    });
  }
}