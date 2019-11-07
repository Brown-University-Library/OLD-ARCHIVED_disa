class CitationApp {

  constructor($elem, config, source, cDisplay, cForm, refCtrl) {
    this._$root = $elem;
    this._source = source;
    this._data = config._data;
    this._$edit_cite = $elem.find('#edit_citation');
    this._$new_ref = $elem.find('#new_reference');
    this.citation_id = $elem.attr('data-citation-id');
    this._cite_display = cDisplay;
    this._cite_form = cForm;
    this._ref_ctrl = refCtrl;

    this.setEvents();
    this.load();
  }

  load(data) {
    this._data = data || this._data;
    this._cite_display.show(this._data.citation);
    this._cite_form.load(this._data.citation);
    this._ref_ctrl.load(this._data.references);
    if (this.citation_id === 'new') {
      this._$edit_cite.addClass('hidden');
      this._$new_ref.addClass('hidden');
      this._cite_form.activate();
      this._ref_ctrl.hide();
    } else {
      this._$edit_cite.removeClass('hidden');
      this._$new_ref.removeClass('hidden');
      this._cite_form.deactivate();
      this._ref_ctrl.show();
    }
  }

  editCitation() {
    this._cite_display.hide();
    this._cite_form.activate();
    this._ref_ctrl.hide();
    this._$edit_cite.addClass('hidden');
    this._$new_ref.addClass('hidden');
  }

  saveCitation() {
    let data; 

    // if (!this._cite_form.diff(this.data.citation)) {
    //   this.loadCitation(this.data.citation);
    // } 
    data = this._cite_form.read();
    if (this.citation_id === 'new') {
      this._source.createNewCitation(data);
    } else {
      this._source.updateCitation(data);
    }
  }

  citationSaved(data) {
    this._data.citation = data.citation; 
    if (this.citation_id === 'new') {
      this.citation_id = data.citation_id;
    }
    this.resetCitation();
  }

  resetCitation() {
    this._cite_display.show(this._data.citation);
    this._cite_form.deactivate();
    this._cite_form.load(this._data.citation);
    this._$edit_cite.removeClass('hidden');
    this._$new_ref.removeClass('hidden');
    this._ref_ctrl.show();
  }

  changeCitationType(cType) {
    this._cite_form.changeCitationType(cType);
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
    this._ref_ctrl.load(data.references);
    this._$edit_cite.prop('disabled', false);
    this._$new_ref.removeClass('disabled');
  }

  resetReferences() {
    this._ref_ctrl.activate();
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