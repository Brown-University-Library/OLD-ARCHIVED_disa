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

  read() {
    return {'name': this.getName(), 'value': this.getInput() };
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

  setFieldTypeMap(config) {
    this._field_type_map = config;
  }

  load(citeState) {
    this.loadFields( citeState );
    this.loadFieldData( citeState );
  }

  loadFields(citeState) {
    this._field_map = {};
    this._$field_list.empty();

    this._$type_selector.val( citeState.getCitationTypeId() );
    for (const field of this._field_type_map[ citeState.getCitationTypeId() ] ) {
      let $field = this._$field_template.clone();
      let citation_field = new CitationField($field, field);
      this._$field_list.append($field);
      this._field_map[ field.name ] = citation_field;
    }
  }

  loadFieldData(citeState) {
    for ( const name of citeState.getCitationFieldNames() ) {
      if ( name in this._field_map ) {
        this._field_map[ name ].setInput( citeState.getFieldValueByName(name) );
      }
    }
  }

  read() {
    let data = {
      'citation_type': this._$type_selector.val(),
      'citation_fields': []
    };
    for (const field_name in this._field_map) {
      let cfield = this._field_map[field_name];
      if (!cfield.isEmpty()) {
        data.citation_fields.push( cfield.read() );
      }
    }
    return data;
  }
}

class CitationForm extends Control {

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

    this.setEvents();
  }

  configure(config) {
    this._cmgmt.setFieldTypeMap(config.get('citationtype_fields'));
  }

  load(citeState) {
    this._$cmmt.val(citeState.getComments());
    this._$ackn.val(citeState.getAcknowledgements());
    this._cmgmt.load( citeState );
  }

  changeCitationType( citeState ) {
    this._cmgmt.load( citeState );
  }

  read() {
    let data = this._cmgmt.read();
    data.comments = this._$cmmt.val();
    data.acknowledgements = this._$ackn.val();

    return data;
  }

  activate( citeState ) {
    this.load( citeState );
    if ( citeState.isNew() ) {
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

  setEvents() {
    let cmp = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('save-citation'):
          cmp._app.saveCitation();
          break;
        case $btn.hasClass('cancel-edit-citation'):
          cmp._app.displayCitation();
          break;
        default:
          return;
      }
    });

    this._$root.on('change', '#citation_type_selector', function(e){
      e.preventDefault();
      let $ctrl = $( this );
      cmp._app.changeCitationType($ctrl.val());
    });
  }
}