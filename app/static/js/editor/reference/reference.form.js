class AutoCompleteInput {

  constructor($input) {
    this._$input = $input;
    this._auto_data = [];
    this._state = { 'id': '', 'name': '' };
  }

  setAutoComplete(autoCompleteValues, settings) {
    let cmpt = this;
    for (var i=0; i < autoCompleteValues.length; i++) {
      var acObj = autoCompleteValues[i];
      this._auto_data.push({
        'id': acObj.id,
        'value': acObj.name,
        'label': acObj.name
      })
    }

    this._$input.autocomplete({
        source: cmpt._auto_data,
        minLength: settings.minLength,
        delay: settings.delay,
        autoFocus: settings.autoFocus,
        response: function (event, ui) {
          if (ui.content.length == 0) {
            ui.content.push({
              label: cmpt._$input.val(),
              value: cmpt._$input.val(),
              id: 'new'
            });
          }
        },
        change: function (event, ui) {
          let data = { 'id': '', 'name': ''};
          if (ui.item) {
            data.id = ui.item.id;
            data.name = ui.item.value;
          }
          cmpt.load(data);
        }
    });
  }

  load(data) {
    this._state = data;
    this._$input.val(data.name);
  }

  isEmpty() {
    return this._state.name === '';
  }

  read() {
    return this._state ;
  }
}

class RichTextInput {

  constructor($elem) {
    this._$input = $elem;
    this._id = $elem.attr('id');
    this._settings = {};
  }

  setEditor(settings) {
    settings.selector = `#${this._id}`;
    this._settings = settings;
  }

  load(data) {
    if (!tinymce.get(this._id)) {
      let cmpt = this;
      tinymce.init(this._settings)
        .then(function(editors) {
          cmpt._$input.val(data);
          tinymce.get(cmpt._id).load();
        });
    } else {
      this._$input.val(data);
      tinymce.get(this._id).load();
    }
  }

  read(data) {
    tinymce.triggerSave();
    return this._$input.val();
  }
}

class LocationField extends AutoCompleteInput {

  constructor($elem) {
    super($elem);
    this._$root = $elem;
    this._location_type = {};
  }

  getType() {
    return this._location_type.id;
  }

  setType(data) {
    this._location_type = data;
  }

  read() {
    let ac_data = super.read();
    return {
      'id': ac_data.id,
      'name': ac_data.name,
      'location_type': this._location_type
    };
  }
}

class DateSelect {

  constructor($elem) {
    this._$root = $elem;
    this._$day = $elem.find('#date_day');
    this._$month = $elem.find('#date_month');
    this._$year = $elem.find('#date_year');
    this._$text = $elem.find('#date_text');
  }

  read() {
    return {
      'day': this._$day.val(),
      'month': this._$month.val(),
      'year': this._$year.val(),
      'date_text': this._$text.val()
    }
  }

  load(data) {
    this._$day.val(data.day);
    this._$month.val(data.month);
    this._$year.val(data.year);
    this._$text.val(data.date_text);
  }
}

class ReferenceForm extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._$discard_btn = $elem.find('.discard-new-reference');
    this._$cancel_btn = $elem.find('.cancel-edit-reference');
    this._$natl_context = $elem.find('#natl_ctx_select');

    this._data = {};
    this._loc_fields_by_type = {};

    this._ref_type = new AutoCompleteInput($elem.find('#reference_type_input'));
    this._col_state = new LocationField($elem.find('#colony_state_input'));
    this._city = new LocationField($elem.find('#city_input'));
    this._locale = new LocationField($elem.find('#locale_input'));
    this._date = new DateSelect($elem.find('#date_selector'));
    this._trsc = new RichTextInput($elem.find('#transcription_input'));

    this.setEvents();
  }

  configure(config, autoCmplSettings, richTextSettings) {
    this._trsc.setEditor(richTextSettings);

    this._ref_type.setAutoComplete(config.get('reference_types'),
      autoCmplSettings);

    let loc_types = config.get('location_types');
    this._col_state.setAutoComplete(
      config.get('colony_states'), autoCmplSettings);
    this._col_state.setType(
      loc_types.filter(ltype => ltype.name ==='Colony/State')[0] );
    this._city.setAutoComplete(
      config.get('cities'), autoCmplSettings);
    this._city.setType(
      loc_types.filter(ltype => ltype.name ==='City')[0] );
    this._locale.setAutoComplete(
      config.get('locales'), autoCmplSettings);
    this._locale.setType(
      loc_types.filter(ltype => ltype.name ==='Locale')[0] );
    // Reference location fields by sequence
    this._locations = [ this._col_state, this._city, this._locale ];
    // Reference locations fields by location type
    for (var i=0; i < this._locations.length; i++) {
      let loc_field = this._locations[i];
      this._loc_fields_by_type[ loc_field.getType() ] = loc_field;
    }
  }

  load(refState) {
    this._$natl_context.val(refState.getNatlContext().id);
    this._ref_type.load(refState.getRefType());
    for (const loc of refState.getLocations()) {
      this._loc_fields_by_type[ loc.location_type.id ].load(loc);
    }
    this._date.load(refState.getDate());
    this._trsc.load(refState.getTranscription());
  }

  read() {
    let data = {};
    data.locations = [];
    for (var i=0; i < this._locations.length; i++) {
      let loc = this._locations[i];
      if (!loc.isEmpty()) {
        data.locations.push(loc.read());
      }
    }
    data.reference_type = this._ref_type.read();
    data.national_context = {
      'id': this._$natl_context.val(),
      'name': this._$natl_context.find(":selected").text()
    };
    data.date = this._date.read();
    data.transcription = this._trsc.read();
    return data;
  }

  activate(refState) {
    if ( refState.isNew() ) {
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
    this.load(this._app.getReference());
    this.deactivate();
  }

  setEvents() {
    let cmp = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('save-reference'):
          cmp._app.saveReference();
          break;
        case $btn.hasClass('cancel-edit-reference'):
          cmp._app.displayReference();
          break;
        default:
          return;
      }
    });
  }
}