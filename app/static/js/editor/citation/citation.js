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

  constructor($elem, $templateField, fieldTypeMap) {
    this._$root = $elem;
    this._$type_selector = this._$root.find('#citation_type_selector');
    this._$field_list = this._$root.find('#citation_field_list');
    this._$template_field = $templateField;
    this._field_type_map = fieldTypeMap;
    this._data = {};
    this._field_map = {};
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
      let $field = this._$template_field.clone();
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

class CitationForm {

  constructor($elem, $template, config) {
    this._$root = $elem;
    // this._$form_groups = $elem.find('.citation-form-group');
    this._$cmmt = $elem.find('#comments_input');
    this._$ackn = $elem.find('#acknowledgements_input');
    this._$discard_btn = $elem.find('.discard-new-citation');
    this._$cancel_btn = $elem.find('.cancel-edit-citation');
    this._data = {};
    this._cmgmt = new CitationFieldManager(
      this._$root.find('#citation_field_mgmt'), $template, config);
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

class Reference {

  constructor($elem, refData) {
    this._$root = $elem;
    this._$ref_id = $elem.find('.reference-id');
    this._$ref_link = $elem.find('.reference-link');
    this._$ref_edited = $elem.find('.reference-edited');
    this._$ref_delete = $elem.find('.delete-reference');
    this._$ref_cancel = $elem.find('.cancel-delete-reference');
    this._$ref_confirm = $elem.find('.confirm-delete-reference');
    
    this._$ref_id.text(refData.id);
    this._$ref_link.attr('href', this._url_base + refData.id)
      .text(refData.reference_type);
    this._$ref_edited.text(refData.last_edit);
    this._$root.attr('data-reference-id', refData.id);
    this.reset();
  }

  enable() {
    this._$ref_cancel.removeClass('control-hide');
    this._$ref_confirm.removeClass('control-hide');
    this._$ref_delete.prop('disabled', false);
    this._$ref_delete.addClass('control-hide');
  }

  disable() {
    this._$ref_cancel.addClass('control-hide');
    this._$ref_confirm.addClass('control-hide');
    this._$ref_delete.prop('disabled', true);
    this._$ref_delete.removeClass('control-hide');
  }

  reset() {
    this._$ref_cancel.addClass('control-hide');
    this._$ref_confirm.addClass('control-hide');
    this._$ref_delete.prop('disabled', false);
    this._$ref_delete.removeClass('control-hide');
  }

  delete() {
    this._$root.remove();
  }
}

class ReferenceManager {

  constructor($elem, $templateReference, urlBaseReference) {
    this._$root = $elem;
    this._$empty_display = this._$root.find('#empty_reference_display');
    this._$ref_head = this._$root.find('#reference_list_header');
    this._$ref_list = this._$root.find('#reference_list');
    this._$ref_template = $templateReference;
    this._url_base = urlBaseReference;
    this._data = [];
    this._reference_map = {};
  }

  load(data) {
    this._data = data;
    if (data.length === 0) {
      this._$empty_display.prop('hidden', false);
      this._$ref_list.prop('hidden', true);
      this._$ref_head.prop('hidden', true);
    } else {
      this._$ref_list.empty();
      this._$empty_display.prop('hidden', true);
      this._$ref_list.prop('hidden', false);
      this._$ref_head.prop('hidden', false);
      for (const ref of data) {
        this.addReference(ref);
      }
    }
  }

  addReference(refData) {
    let $ref = this._$ref_template.clone();
    let reference = new Reference($ref, refData);
    this._reference_map[refData.id] = reference;
    this._$ref_list.append($ref);
  }

  removeReference(refId) {
    this._reference_map[refId].delete();
    delete this._reference_map[refId];
    for (var i=0; i < this._data.length;i++) {
      if (this.data[i].id === refId) {
        this._data.splice(i, 1);
        break;
      }
    }
  }

  activateReference(refId) {
    for (const ref in this._reference_map) {
      if (ref === refId) {
        this._reference_map[ref].enable();
      } else {
        this._reference_map[ref].disable();
      }
    }
  }

  show() {
    this._$root.prop('hidden',false);
  }

  hide() {
    this._$root.prop('hidden',true);
  }

  activate() {
    for (const ref in this._reference_map) {
      this._reference_map[ref].reset();
    }
  }

  deactivate() {
    for (const ref in this._reference_map) {
      this._reference_map[ref].disable();
    }
  }
}

class CitationDisplay {

  constructor($elem, dataTemplate) {
    this._$root = $elem;
    this._$data_template = dataTemplate;
    this._$new_header = $elem.find('#display_header_new');
    this._$existing_header = $elem.find('#display_header_existing');
    this._$data_display = $elem.find('#citation_display_data');
  }

  displayCitationData(fieldData) {
    this._$data_display.empty();
    for (var i=0; i < fieldData.length; i++) {
      let data_field = fieldData[i];
      let $data_elem = this._$data_template.clone();
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

class CitationPage {

  constructor($elem, source) {
    this._$root = $elem;
    this._source = source;
    this._data = {};
    this._$edit_btn = $elem.find('#edit_citation');
    this.citation_id = $elem.attr('data-citation-id');
    
    this.$templates = this.getPageTemplates(this._$root);    
    this._data = this.getPageConfigurationData(this._$root);

    this._cite_display = new CitationDisplay($elem.find('#citation_display'),
      this.$templates.display_data);
    this._cite_form = new CitationForm($elem.find('#citation_form'),
      this.$templates.citation_field, this._data.citationtype_fields);
    this._ref_mgmt = new ReferenceManager($elem.find('#reference_manager'),
      this.$templates.reference_row, 'http://foo.com/');

    this.registerEvents();
    this.load();
  }

  getPageTemplates($root) {
    let template_map = {};
    let $templates = $root.find('template');
    $templates.each(function() {
      let $tmpl = $( $(this).prop('content') ).children().first();
      $tmpl.detach();
      template_map[$tmpl.attr('id')] = $tmpl;
      $tmpl.removeAttr('id');
      $(this).remove();
    });

    return template_map;
  }

  getPageConfigurationData($root) {
    let config = {};
    let $config = $root.find('#configuration_data');
    return JSON.parse(
      $config.find('#config_data_json').attr('data-json'));
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
    // this._data.citation.citation_type = cType;
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

  registerEvents() {
    let app = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('edit-citation'):
          app.editCitation();
          break;
        case $btn.hasClass('save-citation'):
          app.saveCitation();
          break;
        case $btn.hasClass('cancel-edit-citation'):
          app.resetCitation();
          break;
        case $btn.hasClass('delete-reference'):
          app.editReference($btn.closest('.reference')
            .attr('data-reference-id'));
          break;
        case $btn.hasClass('confirm-delete-reference'):
          app.deleteReference($btn.closest('.reference')
            .attr('data-reference-id'));
          break;
        case $btn.hasClass('cancel-delete-reference'):
          app.resetReferences();
          break;
        default:
          return;
      }
    });

    this._$root.on('change', '#citation_type_selector', function(e){
      e.preventDefault();
      let $ctrl = $( this );
      app.changeCitationType($ctrl.val());
    });
  }
}