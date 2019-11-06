class CitationDisplay extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._$templates = this.getTemplates(this._$root);
    this._$new_header = $elem.find('#display_header_new');
    this._$existing_header = $elem.find('#display_header_existing');
    this._$data_display = $elem.find('#citation_display_data');
  }

  displayCitationData(fieldData) {
    this._$data_display.empty();
    for (var i=0; i < fieldData.length; i++) {
      let data_field = fieldData[i];
      let $data_elem = this._$templates.display_data.clone();
      $data_elem.find('.display-field-name').text(
        data_field.name.toUpperCase());
      $data_elem.find('.display-field-value').text(
        data_field.value ? data_field.value : 'None');
      this._$data_display.append($data_elem);
    }
  }

  show(citation) {
    if (citation.citation_id === 'new') {
      this._$new_header.removeClass('hidden');
      this._$existing_header.addClass('hidden');
      this._$data_display.addClass('hidden');
    } else {
      let citation_data = citation.citation_fields.slice(0);
      citation_data.push(
        {'name': 'Comments', 'value': citation.comments });
      citation_data.push(
        {'name': 'Acknowledgements', 'value': citation.acknowledgements });
      this.displayCitationData(citation_data);
      this._$new_header.addClass('hidden');
      this._$existing_header.text(citation.display);
      this._$existing_header.removeClass('hidden');
      this._$data_display.removeClass('hidden');      
    }
      this._$root.removeClass('hidden');
  }

  hide() {
    this._$data_display.addClass('hidden');
  }
}