class ReferenceDisplay extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._state = {};
    this._month_name_map = {};
    this._loc_type_map = {};
    this._$templates = this.getTemplates(this._$root);
    this._$existing_header = $elem.find('#display_header_existing');
    this._$data_display = $elem.find('#reference_display_data');
  }

  configure(config) {
    let date_config = config.get('date');
    for (const month_data of date_config.months) {
      this._month_name_map[month_data.value] = month_data.label;
    }
  }

  formatDate(data) {
    var date_text;
    if (data.month && data.day && data.year) {
      date_text = `${ this._month_name_map[data.month] } ${data.day}, ${data.year}`;
    } else if (data.month && data.day && !data.year) {
      date_text = `${ this._month_name_map[data.month] } ${data.day}`;
    } else if (data.month && !data.day && data.year) {
      date_text = `${ this._month_name_map[data.month] } ${data.year}`;
    } else if (data.month && !data.day && !data.year ) {
      date_text = `${ this._month_name_map[data.month] }`;
    } else if (!data.month && data.day && !data.year ) {
      date_text = `${data.day}`;
    } else if (!data.month && data.day && data.year ) {
      date_text = `${data.day} ${data.year}`;
    } else if (!data.month && !data.day && data.year ) {
      date_text = `${data.year}`;
    } else {
      date_text = 'Unknown';
    }
    return date_text;
  }

  load(data) {
    this._state.header = data.reference_type.name;
    this._state.fields = {
      'source': data.citation_display,
      'description': data.reference_type.name,
      'national context': data.national_context.name,
      'colony/state' : data.locations.filter(
        loc => loc.location_type.name == 'Colony/State').map(
          loc => loc.name)[0] || 'None',
      'city' : data.locations.filter(
        loc => loc.location_type.name == 'City').map(
          loc => loc.name)[0] || 'None',
      'locale' : data.locations.filter(
        loc => loc.location_type.name == 'Locale').map(
          loc => loc.name)[0] || 'None',
      'date': this.formatDate(data.date),
      'transcription': data.transcription.slice(200)
    };
  }

  loadReferenceData(fieldData) {
    this._$data_display.empty();
    for (const field in fieldData) {
      let $data_elem = this._$templates.display_data.clone();
      $data_elem.find('.display-field-name').text(field.toUpperCase());
      $data_elem.find('.display-field-value').text(fieldData[field]);
      this._$data_display.append($data_elem);
    }
  }

  show() {
    this.loadReferenceData(this._state.fields);
    this._$existing_header.text(this._state.header);
    this._$existing_header.removeClass('hidden');
    this._$data_display.removeClass('hidden');
    this._$root.removeClass('hidden');
  }

  hide() {
    this._$data_display.addClass('hidden');
  }
}