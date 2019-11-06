class ReferenceState extends State {

  constructor() {
    super();
    this._slots = ['id', 'reference_type',
      'citation_display', 'locations', 'date',
      'national_context', 'transcription'];
  }

  getId() {
    return this.get('id');
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
    return this.get('citation_display');
  }

  displayRefType() {
    return this.get('reference_type').name;
  }

  displayNatlContext() {
    return this.get('national_context').name;
  }
}

class ReferenceApp {

  constructor($elem, config, source, refDisplay, refForm) {
    this._$root = $elem;
    this._source = source;
    this._reference_state = new ReferenceState();
    this._$edit_ref = $elem.find('#edit_reference');
    // this._$new_rnt = $elem.find('#new_referent');
    this._ref_id = $elem.attr('data-reference-id');
    this._ref_display = refDisplay;
    this._ref_form = refForm;
    // this._rnt_ctrl = rntCtrl;

    this.setEvents();
    this.load(config.get('data'));
    this._ref_display.show();
  }

  getReference() {
    return this._reference_state;
  }

  setReference(data) {
    this._reference_state.update(data);
    this._ref_display.load( this.getReference() );
    this._ref_form.load( this.getReference() );
  }

  load(data) {
    this.setReference(data.reference);
    // this._rnt_ctrl.load(this._data.referents);
    // if (this._ref_id === 'new') {
    //   this._$edit_ref.addClass('hidden');
    //   this._$new_rnt.addClass('hidden');
    //   this._ref_form.activate();
    //   this._rnt_ctrl.hide();
    // } else {
    //   this._$edit_cite.removeClass('hidden');
    //   this._$new_ref.removeClass('hidden');
    //   this._cite_form.deactivate();
    //   this._ref_ctrl.show();
    // }
  }

  editReference() {
    this._ref_display.hide();
    this._ref_form.activate( this.getReference() );
    // this._rnt_ctrl.hide();
    this._$edit_ref.addClass('hidden');
    // this._$new_rnt.addClass('hidden');
  }

  saveReference() {
    let data; 

    data = this._ref_form.read();
    if ( this.getReference().isNew() ) {
      this._source.createReference(data);
    } else {
      this._source.updateReference( data, this.getReference().getId() );
    }
  }

  referenceSaved(data) {
    this.setReference(data.reference);
    this.resetReferenceDisplay();
  }

  resetReferenceDisplay() {
    this._ref_display.load( this.getReference() );
    this._ref_form.load( this.getReference() );
    this._ref_display.show();
    this._ref_form.deactivate();
    this._$edit_ref.removeClass('hidden');
    // this._$new_rnt.removeClass('hidden');
    // this._rnt_ctrl.show();
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