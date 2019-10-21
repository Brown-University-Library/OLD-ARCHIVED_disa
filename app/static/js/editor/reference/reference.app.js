class ReferenceApp {

  constructor($elem, config, refDisplay) {
    this._$root = $elem;
    // this._source = source;
    this._data = config._data.data;
    // this._$edit_ref = $elem.find('#edit_reference');
    // this._$new_rnt = $elem.find('#new_referent');
    this._ref_id = $elem.attr('data-reference-id');
    this._ref_display = refDisplay;
    // this._ref_form = refForm;
    // this._rnt_ctrl = rntCtrl;

    this.setEvents();
    this.load();
  }

  load(data) {
    this._data = data || this._data;
    this._ref_display.show(this._data.display);
    // this._ref_form.load(this._data.reference;
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

  // editReference() {
  //   this._ref_display.hide();
  //   this._ref_form.activate();
  //   this._rnt_ctrl.hide();
  //   this._$edit_ref.addClass('hidden');
  //   this._$new_rnt.addClass('hidden');
  // }

  // saveReference() {
  //   let data; 

  //   data = this._ref_form.read();
  //   if (this._ref_id === 'new') {
  //     this._source.createNewReference(data);
  //   } else {
  //     this._source.updateReference(data);
  //   }
  // }

  // referenceSaved(data) {
  //   this._data.reference = data.reference; 
  //   if (this._ref_id === 'new') {
  //     this._ref_id = data.reference_id;
  //   }
  //   this.resetReference();
  // }

  // resetReference() {
  //   this._ref_display.show(this._data.reference);
  //   this._ref_form.deactivate();
  //   this._ref_form.load(this._data.citation);
  //   this._$edit_ref.removeClass('hidden');
  //   this._$new_rnt.removeClass('hidden');
  //   this._rnt_ctrl.show();
  // }

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

    this._$root.on('click', '.reference-app-event', function(e){
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