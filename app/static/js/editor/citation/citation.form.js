class CitationField {

  constructor($elem, fieldData) {
    this._$root = $elem;
    this._$root.attr('data-citation-field', fieldData.name);
    this._$input = $elem.find('.citation-field-input');
    this._$input.attr('placeholder', fieldData.display);
  }

  getName() {
    return this._$root.attr('data-citation-field');
  }

  getInput() {
    return this._$input.val();
  }

  setInput(data) {
    this._$input.val(data);
  }

  isEmpty() {
    return this._$input.val() == "";
  }
}

class CitationFieldManager {

  constructor($elem, $fieldTemplate) {
    this._$root = $elem;
    this._$type_selector = this._$root.find('#citation_type_selector');
    this._$field_list = this._$root.find('#citation_field_list');
    this._$field_template = $fieldTemplate;
    this._field_type_map = {};
    this._data = {};
    this._field_map = {};
  }

  setFieldTypeMap(data) {
    this._field_type_map = data;
  }

  load(data) {
    this._data = data;
    this.loadFields();
    this.loadFieldData();
  }

  loadFields(typeFields) {
    this._field_map = {};
    this._$field_list.empty();

    this._$type_selector.val(this._data.citation_type);
    for (const field of this._field_type_map[this._data.citation_type] ) {
      let $field = this._$field_template.clone();
      let citation_field = new CitationField($field, field);
      this._$field_list.append($field);
      this._field_map[field.name] = citation_field;
    }
  }

  loadFieldData() {
    for (const field of this._data.citation_fields) {
      if (field.name in this._field_map) {
        this._field_map[field.name].setInput(field.value);
      }
    }
  }

  read() {
    this._data.citation_type = this._$type_selector.val();

    this._data.citation_fields = [];
    for (const field_name in this._field_map) {
      let cfield = this._field_map[field_name];
      if (!cfield.isEmpty()) {
        this._data.citation_fields.push(
          {'name': cfield.getName(), 'value': cfield.getInput()});
      }
    }

    return this._data;
  }
}

class CitationForm extends Flow {

  constructor($elem, citationTypeFieldMap) {
    super()
    this._$root = $elem;
    // this._$form_groups = $elem.find('.citation-form-group');
    this._$cmmt = $elem.find('#comments_input');
    this._$ackn = $elem.find('#acknowledgements_input');
    this._$discard_btn = $elem.find('.discard-new-citation');
    this._$cancel_btn = $elem.find('.cancel-edit-citation');
    this._data = {};
    this._$templates = this.getTemplates(this._$root);
    this._cmgmt = new CitationFieldManager(
      this._$root.find('#citation_field_mgmt'),
      this._$templates.citation_field, citationTypeFieldMap);
  }

  configure(config) {
    this._cmgmt.setFieldTypeMap(config.get('citationtype_fields'));
  }

  load(data) {
    this._data = data;
    this._$cmmt.val(data.comments);
    this._$ackn.val(data.acknowledgements);
    this._cmgmt.load({
      'citation_type': data.citation_type,
      'citation_fields': data.citation_fields
    });
  }

  changeCitationType(cType) {
    this._cmgmt.load({
      'citation_type': cType,
      'citation_fields': this._data.citation_fields
    });
  }

  read() {
    let cdata = this._cmgmt.read();
    this._data.citation_type = cdata.citation_type;
    this._data.citation_fields = cdata.citation_fields;
    this._data.comments = this._$cmmt.val();
    this._data.acknowledgements = this._$ackn.val();

    return this._data;
  }

  activate() {
    if (this._data.citation_id === 'new') {
      this._$discard_btn.removeClass('hidden');
      this._$cancel_btn.addClass('hidden');
    } else {
      this._$discard_btn.addClass('hidden');
      this._$cancel_btn.removeClass('hidden');
    }
    this._$root.removeClass('hidden');
  }

  deactivate() {
    this._$root.addClass('hidden');
  }

  reset() {
    this.load(this._data);
    this.deactivate();
  }
}