class ReferenceDisplay extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._$templates = this.getTemplates(this._$root);
    this._$existing_header = $elem.find('#display_header_existing');
    this._$data_display = $elem.find('#reference_display_data');
  }

  loadReferenceData(fieldData) {
    this._$data_display.empty();
    for (var i=0; i < fieldData.length; i++) {
      let data_field = fieldData[i];
      let $data_elem = this._$templates.display_data.clone();
      $data_elem.find('.display-field-name').text(
        data_field.field);
      $data_elem.find('.display-field-value').text(
        data_field.data);
      this._$data_display.append($data_elem);
    }
  }

  show(displayData) {
    this.loadReferenceData(displayData.fields);
    this._$existing_header.text(displayData.header);
    this._$existing_header.removeClass('hidden');
    this._$data_display.removeClass('hidden');
    this._$root.removeClass('hidden');
  }

  hide() {
    this._$data_display.addClass('hidden');
  }
}