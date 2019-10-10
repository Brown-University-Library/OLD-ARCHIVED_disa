class CitationApp {

  constructor($elem, config, source, cDisplay, cForm, refMgmt) {
    this._$root = $elem;
    this._source = source;
    this._data = config._data;
    this._$edit_btn = $elem.find('#edit_citation');
    this.citation_id = $elem.attr('data-citation-id');
    this._cite_display = cDisplay;
    this._cite_form = cForm;
    this._ref_mgmt = refMgmt;

    this.setEvents();
    this.load();
  }

  load(data) {
    this._data = data || this._data;
    this._cite_display.show(this._data.citation);
    this._cite_form.load(this._data.citation);
    this._ref_mgmt.load(this._data.references);
    if (this.citation_id === 'new') {
      this._$edit_btn.prop('hidden', true);      
      this._cite_form.activate();
      this._ref_mgmt.hide();
    } else {
      this._$edit_btn.removeClass('hidden');
      this._cite_form.deactivate();
      this._ref_mgmt.show();
    }
  }

  editCitation() {
    this._cite_display.hide();
    this._cite_form.activate();
    this._ref_mgmt.deactivate();
    this._$edit_btn.addClass('hidden');
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
    this._$edit_btn.removeClass('hidden');
    this._ref_mgmt.activate();
  }

  changeCitationType(cType) {
    this._cite_form.changeCitationType(cType);
  }

  editReference(refId) {
    this._ref_mgmt.activateReference(refId);
    this._$edit_btn.prop('disabled', true);
  }

  deleteReference(refId) {
    this._source.deleteReference(refId);
  }

  referenceDeleted(data) {
    this._ref_mgmt.load(data.references);
    this._$edit_btn.prop('disabled', false);
  }

  resetReferences() {
    this._ref_mgmt.activate();
    this._$edit_btn.prop('disabled', false);
  }

  setEvents() {
    let app = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('edit-citation'):
          app.editCitation();
          break;
        default:
          return;
      }
    });
  }
}