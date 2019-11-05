class ReferenceDisplay extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._header_text = '';
    this._field_data = {};
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

  trimTranscription(trns) {
    // Special handling for rich text produced by TinyMCE
    if (trns.length > 550) {
      var trimmed, p_open, p_close;

      trimmed = trns.slice(0,550).trim();
      p_open = trimmed.lastIndexOf('<p>');
      p_close = trimmed.lastIndexOf('</p>');

      if (p_open === -1) {
        // no <p> found; not HTML
        trimmed += "...";
      }
      else if (p_open > p_close) {
        trimmed += "...</p>";
      } else {
        trimmed += "<p>...</p>";
      }
      return trimmed;
    }
    return trns.trim();
  }

  load(refState) {
    this._header_text = refState.displayRefType();
    this._field_data = {
      'source': refState.displayCitation(),
      'description': refState.displayRefType(),
      'national context': refState.displayNatlContext(),
      'colony/state' : refState.getLocationsByTypeName('Colony/State')
        .map( loc => loc.name )[0] || 'None',
      'city' : refState.getLocationsByTypeName('City')
        .map( loc => loc.name )[0] || 'None',
      'locale' : refState.getLocationsByTypeName('Locale')
        .map( loc => loc.name )[0] || 'None',
      'date': refState.getDate().formatted,
      'transcription': this.trimTranscription( refState.getTranscription() )
    };
  }

  loadReferenceData(fieldData) {
    this._$data_display.empty();
    for (const field in fieldData) {
      let $data_elem = this._$templates.display_data.clone();
      $data_elem.find('.display-field-name').text(field.toUpperCase());
      if (field === 'transcription') {
        $data_elem.find('.display-field-value').html(fieldData[field]);
      } else {
        $data_elem.find('.display-field-value').text(fieldData[field]);
      }
      this._$data_display.append($data_elem);
    }
  }

  show() {
    this.loadReferenceData(this._field_data);
    this._$existing_header.text(this._header_text);
    this._$existing_header.removeClass('hidden');
    this._$data_display.removeClass('hidden');
    this._$root.removeClass('hidden');
  }

  hide() {
    this._$data_display.addClass('hidden');
  }
}